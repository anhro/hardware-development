#!/usr/bin/env python3
"""Шукає вузькі язики заливки GND на зовнішніх шарах плати KiCad.

Вузький язик — ділянка полігону, вужча за --width (типово 1 мм): смужка між
доріжками, вздовж краю плати, між падами. Такі ділянки погано зʼєднані з
рештою землі й працюють як антени, тому їх прибирають Rule Area «No copper
fill» або привʼязують stitching via.

Алгоритм: заливка шару растеризується з кроком --res, потім морфологічне
відкриття (ерозія + дилатація квадратом --width). Пікселі, які зникли після
відкриття, — вузькі місця. Їх групують у звʼязні ділянки й відкидають дрібні
(--min-area, --min-length).

Скрипт аналізує заповнені полігони (`filled_polygon`), збережені в `.kicad_pcb`.
З --refill він спершу копіює проєкт у тимчасову папку і перезаливає полігони
через `kicad-cli pcb drc --refill-zones --save-board`; вихідний файл не
змінюється. Без --refill потрібно, щоб плату зберегли після заливки (`B`).

Обмеження: спиці термобарʼєрів і хрестики навколо THT-падів теж потрапляють у
вузькі місця — у списку їх відсікають пороги площі й довжини, на карті вони
видні як червоні плями біля падів. Це оцінка, а не точна метрика.

Потрібно: Python 3 + Pillow; для --refill — KiCad 10 (`kicad-cli`).

Використання:
    tools/check-gnd-tongues.py motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb --refill
    tools/check-gnd-tongues.py PCB --refill --png assignments/homework_15/images/gnd-tongues.png
    tools/check-gnd-tongues.py PCB --net GND --layer F.Cu --layer B.Cu --top 30
"""
from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
except ImportError:
    sys.exit("Потрібен Pillow: pip install pillow")

ZONE_RE = re.compile(r"\n\t\(zone\n(.*?)\n\t\)", re.S)
XY_RE = re.compile(r"\(xy ([-\d.]+) ([-\d.]+)\)")


def refill_copy(pcb: Path, tmp: Path) -> Path:
    """Копіює проєкт у tmp і перезаливає полігони kicad-cli."""
    src = pcb.parent
    for f in src.iterdir():
        if f.name.startswith("~") or f.name.startswith(".") or f.suffix in (".lck", ".bak"):
            continue
        dst = tmp / f.name
        if f.is_dir():
            if f.name == "lib":
                shutil.copytree(f, dst)
        else:
            shutil.copy2(f, dst)
    board = tmp / pcb.name
    r = subprocess.run(
        ["kicad-cli", "pcb", "drc", "--refill-zones", "--save-board",
         "-o", str(tmp / "drc.rpt"), str(board)],
        capture_output=True, text=True)
    if r.returncode != 0 or not board.exists():
        sys.exit(f"kicad-cli завершився з помилкою:\n{r.stdout}{r.stderr}")
    return board


def board_bbox(text: str) -> tuple[float, float, float, float]:
    """Габарити плати за Edge.Cuts (лінії, дуги, прямокутники)."""
    xs, ys = [], []
    for m in re.finditer(r"\n\t\(gr_\w+\s(.*?)\n\t\)", text, re.S):
        body = m.group(1)
        if '(layer "Edge.Cuts")' not in body:
            continue
        for x, y in re.findall(r"\((?:start|end|mid|center|xy) ([-\d.]+) ([-\d.]+)\)", body):
            xs.append(float(x))
            ys.append(float(y))
    if not xs:
        sys.exit("Не знайдено контур Edge.Cuts")
    return min(xs), min(ys), max(xs), max(ys)


def footprints(text: str) -> list[tuple[str, float, float]]:
    out = []
    for f in re.split(r"\n\t\(footprint ", text)[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', f)
        at = re.search(r"\n\t\t\(at ([-\d.]+) ([-\d.]+)", f)
        if ref and at:
            out.append((ref[1], float(at[1]), float(at[2])))
    return out


def vias(text: str, net: str) -> list[tuple[float, float]]:
    out = []
    for m in re.finditer(r"\n\t\(via\s*\(at ([-\d.]+) ([-\d.]+)\).*?\(net (?:\d+ )?\"([^\"]*)\"\)", text, re.S):
        if m[3] == net:
            out.append((float(m[1]), float(m[2])))
    return out


def fill_mask(text: str, net: str, layer: str, origin, size, res) -> Image.Image:
    x0, y0 = origin
    im = Image.new("L", size, 0)
    draw = ImageDraw.Draw(im)
    for z in ZONE_RE.findall(text):
        if f'(net "{net}")' not in z or "teardrop" in z:
            continue
        for fp in re.findall(r'\(filled_polygon\s*\(layer "%s"\)(.*?)\n\t\t\)' % re.escape(layer), z, re.S):
            pts = [((float(a) - x0) / res, (float(b) - y0) / res) for a, b in XY_RE.findall(fp)]
            if len(pts) > 2:
                draw.polygon(pts, fill=255)
    return im


def thin_parts(mask: Image.Image, width: float, res: float) -> Image.Image:
    k = max(3, int(round(width / res)) | 1)  # непарний розмір ядра
    opened = mask.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    return ImageChops.subtract(mask, opened)


def components(img: Image.Image) -> list[list[tuple[int, int]]]:
    w, h = img.size
    px = img.load()
    seen = set()
    out = []
    for y in range(h):
        for x in range(w):
            if not px[x, y] or (x, y) in seen:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            comp = []
            while stack:
                a, b = stack.pop()
                comp.append((a, b))
                for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if 0 <= q[0] < w and 0 <= q[1] < h and px[q] and q not in seen:
                        seen.add(q)
                        stack.append(q)
            out.append(comp)
    return out


def render(panels: list[tuple[str, Image.Image, Image.Image]], origin, res, out: Path) -> None:
    x0, y0 = origin
    tiles = []
    for layer, mask, thin in panels:
        gray = mask.point(lambda v: 200 if v else 255)
        rgb = Image.merge("RGB", (gray, gray, gray))
        rgb.paste(Image.new("RGB", rgb.size, (220, 0, 0)), mask=thin.filter(ImageFilter.MaxFilter(5)))
        d = ImageDraw.Draw(rgb)
        step = int(round(10 / res))
        gx0 = math.ceil(x0 / 10) * 10
        gy0 = math.ceil(y0 / 10) * 10
        for gx in range(int((gx0 - x0) / res), rgb.width, step):
            d.line([(gx, 0), (gx, rgb.height)], fill=(170, 170, 255))
            d.text((gx + 2, 2), f"{x0 + gx * res:.0f}", fill=(0, 0, 200))
        for gy in range(int((gy0 - y0) / res), rgb.height, step):
            d.line([(0, gy), (rgb.width, gy)], fill=(170, 170, 255))
            d.text((2, gy + 2), f"{y0 + gy * res:.0f}", fill=(0, 0, 200))
        d.text((rgb.width // 2 - 20, rgb.height - 14), layer, fill=(0, 0, 0))
        tiles.append(rgb)
    gap = 20
    img = Image.new("RGB", (sum(t.width for t in tiles) + gap * (len(tiles) - 1), tiles[0].height), "white")
    x = 0
    for t in tiles:
        img.paste(t, (x, 0))
        x += t.width + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pcb", type=Path, help="файл .kicad_pcb")
    ap.add_argument("--refill", action="store_true", help="перезалити полігони в тимчасовій копії проєкту")
    ap.add_argument("--net", default="GND", help="мережа полігонів (типово GND)")
    ap.add_argument("--layer", action="append", help="шар; можна кілька (типово F.Cu і B.Cu)")
    ap.add_argument("--width", type=float, default=1.0, help="поріг ширини, мм (типово 1.0)")
    ap.add_argument("--res", type=float, default=0.1, help="крок растра, мм (типово 0.1)")
    ap.add_argument("--min-area", type=float, default=0.4, help="мінімальна площа язика, мм² (типово 0.4)")
    ap.add_argument("--min-length", type=float, default=2.0, help="мінімальна довжина язика, мм (типово 2.0)")
    ap.add_argument("--top", type=int, default=20, help="скільки язиків показати на шар (типово 20)")
    ap.add_argument("--png", type=Path, help="зберегти карту: сіре — заливка, червоне — вузькі місця")
    args = ap.parse_args()
    layers = args.layer or ["F.Cu", "B.Cu"]

    if not args.pcb.exists():
        sys.exit(f"Немає файлу {args.pcb}")
    with tempfile.TemporaryDirectory() as tmp:
        pcb = refill_copy(args.pcb.resolve(), Path(tmp)) if args.refill else args.pcb
        text = pcb.read_text(encoding="utf-8")

    bx0, by0, bx1, by1 = board_bbox(text)
    origin = (bx0, by0)
    size = (int(math.ceil((bx1 - bx0) / args.res)) + 1, int(math.ceil((by1 - by0) / args.res)) + 1)
    refs = footprints(text)
    gnd_vias = vias(text, args.net)

    def near(x: float, y: float) -> str:
        return ",".join(r[0] for r in sorted(refs, key=lambda r: math.hypot(r[1] - x, r[2] - y))[:2])

    panels = []
    for layer in layers:
        mask = fill_mask(text, args.net, layer, origin, size, args.res)
        if not mask.getbbox():
            print(f"== {layer}: заливки {args.net} немає")
            continue
        thin = thin_parts(mask, args.width, args.res)
        panels.append((layer, mask, thin))
        found = []
        for comp in components(thin):
            area = len(comp) * args.res ** 2
            xs = [bx0 + c[0] * args.res for c in comp]
            ys = [by0 + c[1] * args.res for c in comp]
            length = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
            if area < args.min_area or length < args.min_length:
                continue
            has_via = any(min(xs) - 0.5 < vx < max(xs) + 0.5 and min(ys) - 0.5 < vy < max(ys) + 0.5
                          for vx, vy in gnd_vias)
            cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            found.append((area, length, min(xs), min(ys), max(xs), max(ys), near(cx, cy), has_via))
        found.sort(reverse=True)
        total = sum(f[0] for f in found)
        print(f"== {layer}: {len(found)} язиків (площа ≥ {args.min_area} мм², довжина ≥ {args.min_length} мм, "
              f"ширина < {args.width} мм), сумарно {total:.1f} мм²")
        for a, ln, x0, y0, x1, y1, ref, v in found[:args.top]:
            print(f"  {a:5.1f} мм²  L={ln:4.1f} мм  ({x0:.1f}, {y0:.1f})–({x1:.1f}, {y1:.1f})  біля {ref}"
                  f"{'  [via]' if v else ''}")

    if args.png and panels:
        render(panels, origin, args.res, args.png)
        print(f"Карта: {args.png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
