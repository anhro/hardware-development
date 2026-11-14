#!/usr/bin/env python3
"""Шукає паралельні ділянки між аналоговими лініями та лініями PWM на платі KiCad.

Читає `.kicad_pcb` як текст (KiCad не потрібен), бере всі відрізки доріжок
(`segment`) і для кожної пари «жертва» (аналогова лінія) + «агресор» (лінія
з фронтами PWM) на одному шарі рахує:
  - довжину ділянки, де відрізки паралельні (кут ≤ --angle) і перекриваються
    в проєкції;
  - зазор між краями доріжок (відстань між осями мінус половини ширин).

Результат: сумарна довжина паралельних ділянок для кожного порогу зазору
і найгірші пари з координатами.

Обмеження: тільки прямі відрізки на одному шарі (дуги, полігони і сусідні
шари не враховуються); одна ділянка може порахуватися двічі, якщо поруч
кілька сегментів того самого агресора. Це оцінка, а не точна метрика.

Використання:
    tools/check-parallel.py motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb
    tools/check-parallel.py PCB --victim '/Inverter/SH_' --victim 'CS.SN' \\
        --aggressor 'GATE.' --gaps 1 2 3 --top 5
"""
from __future__ import annotations
import argparse
import collections
import math
import re
import sys
from pathlib import Path

SEGMENT = re.compile(
    r'\(segment\s+\(start ([\d.-]+) ([\d.-]+)\)\s*\(end ([\d.-]+) ([\d.-]+)\)'
    r'\s*\(width ([\d.]+)\)\s*\(layer "([^"]+)"\)\s*\(net (?:\d+ )?"([^"]*)"\)')

# Типові групи мереж для плати motor-drive-controller (ДЗ 13).
DEFAULT_VICTIMS = ['/Inverter/SH_', 'CS.SN']
DEFAULT_AGGRESSORS = ['GATE.', '/Gate Driver/PH.S', 'DRV.IN']


def load_segments(pcb: Path) -> list[tuple]:
    return [(float(x1), float(y1), float(x2), float(y2), float(w), layer, net)
            for x1, y1, x2, y2, w, layer, net in SEGMENT.findall(pcb.read_text())]


def parallel(a: tuple, b: tuple, min_cos: float, min_len: float):
    """Довжина спільної паралельної ділянки і зазор між краями (або (0, None))."""
    ax, ay, bx, by = a[:4]
    cx, cy, dx, dy = b[:4]
    la, lb = math.hypot(bx - ax, by - ay), math.hypot(dx - cx, dy - cy)
    if la < min_len or lb < min_len:
        return 0.0, None
    ux, uy = (bx - ax) / la, (by - ay) / la
    vx, vy = (dx - cx) / lb, (dy - cy) / lb
    if abs(ux * vx + uy * vy) < min_cos:
        return 0.0, None
    t1 = (cx - ax) * ux + (cy - ay) * uy
    t2 = (dx - ax) * ux + (dy - ay) * uy
    lo, hi = max(0.0, min(t1, t2)), min(la, max(t1, t2))
    if hi <= lo:
        return 0.0, None
    gap = abs((cx - ax) * uy - (cy - ay) * ux) - (a[4] + b[4]) / 2
    return hi - lo, gap


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('pcb', type=Path, help='файл .kicad_pcb')
    p.add_argument('--victim', action='append',
                   help='підрядок назви мережі аналогової лінії (можна кілька)')
    p.add_argument('--aggressor', action='append',
                   help='підрядок назви мережі лінії PWM (можна кілька)')
    p.add_argument('--gaps', type=float, nargs='+', default=[1.0, 2.0, 3.0],
                   help='пороги зазору між краями, мм (типово 1 2 3)')
    p.add_argument('--angle', type=float, default=14.0,
                   help='максимальний кут між відрізками, градуси (типово 14)')
    p.add_argument('--min-len', type=float, default=0.3,
                   help='коротші відрізки ігноруються, мм (типово 0.3)')
    p.add_argument('--top', type=int, default=5, help='скільки найгірших пар показати')
    args = p.parse_args()

    victims = args.victim or DEFAULT_VICTIMS
    aggressors = args.aggressor or DEFAULT_AGGRESSORS
    min_cos = math.cos(math.radians(args.angle))

    segs = load_segments(args.pcb)
    if not segs:
        print(f'{args.pcb}: доріжок не знайдено', file=sys.stderr)
        return 1
    vic = [s for s in segs if any(v in s[6] for v in victims)]
    agg = [s for s in segs if any(a in s[6] for a in aggressors)]
    print(f'{args.pcb.name}: {len(segs)} відрізків, жертв {len(vic)}, агресорів {len(agg)}')
    print(f'Жертви: {", ".join(victims)}')
    print(f'Агресори: {", ".join(aggressors)}')

    for limit in sorted(args.gaps):
        total = collections.defaultdict(float)
        worst = {}
        for a in vic:
            for b in agg:
                if a[5] != b[5]:
                    continue
                length, gap = parallel(a, b, min_cos, args.min_len)
                if length and gap < limit:
                    key = (a[6].split('/')[-1], b[6].split('/')[-1], a[5])
                    total[key] += length
                    if key not in worst or gap < worst[key][0]:
                        worst[key] = (gap, b[0], b[1])
        print(f'\nЗазор < {limit:g} мм: {sum(total.values()):.1f} мм')
        for key, length in sorted(total.items(), key=lambda kv: -kv[1])[:args.top]:
            gap, x, y = worst[key]
            print(f'  {length:5.1f} мм  зазор {gap:.2f} мм  {key[0]} <-> {key[1]}'
                  f'  {key[2]} біля ({x:.1f}, {y:.1f})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
