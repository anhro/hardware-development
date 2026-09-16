#!/usr/bin/env python3
"""Відновлює datasheets за маніфестами `datasheets.txt`.

Формат маніфесту (один документ на рядок, `#` — коментар):

    <ім'я файлу>  <URL>

Файли завантажуються в ту саму директорію, де лежить маніфест. Уже наявні
файли не перезавантажуються (прапорець --force змінює це).

Використання:
    tools/fetch-datasheets.py                 # усі маніфести в репозиторії
    tools/fetch-datasheets.py path/to/datasheets.txt
    tools/fetch-datasheets.py --check         # лише звіт: чого бракує, що не описано
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = "datasheets.txt"
# Частина виробників відхиляє запити без "браузерного" User-Agent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
TIMEOUT_S = 60


def parse(manifest: Path) -> list[tuple[str, str]]:
    entries = []
    for n, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or "/" in parts[0]:
            sys.exit(f"{manifest}:{n}: очікується '<ім'я файлу> <URL>', отримано: {line!r}")
        entries.append((parts[0], parts[1]))
    return entries


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"})
    tmp = dest.with_name(dest.name + ".part")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp, open(tmp, "wb") as out:
            head = resp.read(5)
            # Сайти часто віддають HTML-сторінку з кодом 200 замість файлу
            if dest.suffix.lower() == ".pdf" and head != b"%PDF-":
                raise ValueError("відповідь не є PDF (ймовірно, сторінка входу/капчі)")
            out.write(head)
            while chunk := resp.read(1 << 16):
                out.write(chunk)
        tmp.replace(dest)  # атомарно: ніколи не лишаємо напівзавантажений файл під справжнім ім'ям
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifests", nargs="*", type=Path)
    ap.add_argument("--force", action="store_true", help="перезавантажити наявні файли")
    ap.add_argument("--check", action="store_true", help="нічого не завантажувати, лише звіт")
    args = ap.parse_args()

    manifests = args.manifests or sorted(p.relative_to(ROOT) for p in ROOT.rglob(MANIFEST) if ".git" not in p.parts)
    failed = missing = 0
    for manifest in manifests:
        manifest = manifest if manifest.is_absolute() or args.manifests else ROOT / manifest
        folder = manifest.parent
        entries = parse(manifest)
        print(f"== {manifest}")
        for name, url in entries:
            dest = folder / name
            if dest.exists() and not args.force:
                print(f"   ok       {name}")
                continue
            if args.check:
                print(f"   missing  {name}")
                missing += 1
                continue
            try:
                download(url, dest)
                print(f"   fetched  {name}")
            except Exception as e:  # мережеві помилки не мають зупиняти інші завантаження
                failed += 1
                print(f"   FAILED   {name}: {e}\n            завантажте вручну: {url}")
        listed = {name for name, _ in entries} | {MANIFEST}
        for extra in sorted(p.name for p in folder.iterdir() if p.is_file() and p.name not in listed):
            print(f"   unlisted {extra}  <- додайте в {MANIFEST}, інакше не відновиться після клонування")
    if failed or missing:
        print(f"\nНе вистачає файлів: {failed + missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
