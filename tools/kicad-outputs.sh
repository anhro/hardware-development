#!/usr/bin/env bash
# Генерує артефакти KiCad-проєкту в build/hardware/:
#   <name>-erc.rpt, <name>-schematic.pdf   — перевірка й документація
#   manufacturing/                         — файли для виробництва
#     gerber/      Gerber, Excellon (.drl), карти свердління
#     assembly/    BOM (.csv), файл позиціонування компонентів (.csv)
#     <name>-fab.zip  вміст gerber/ — архів для завантаження на завод
# Gerber, drill і позиції — лише для плати з контуром (порожня плата прототипу пропускається).
# Використання: kicad-outputs.sh [<папка проєкту>] [all|fab]   (fab — лише manufacturing/)
# ERC_STRICT=1 — завершитися з помилкою, якщо ERC знайшов помилки (severity error).
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd)"
KICAD_IMAGE="kicad/kicad:10.0"

project_dir="${1:-motor-drive-controller/hardware/kicad}"
what="${2:-all}"
pro="$(ls "$ROOT/$project_dir"/*.kicad_pro)"
name="$(basename "$pro" .kicad_pro)"
out="build/hardware"
mfg="$out/manufacturing"
gerber="$mfg/gerber"
assembly="$mfg/assembly"
mkdir -p "$ROOT/$out" "$ROOT/$assembly"

kicad() {
  if command -v kicad-cli >/dev/null; then
    kicad-cli "$@"
  else
    docker run --rm -u "$(id -u):$(id -g)" -e HOME=/tmp -v "$ROOT:/data" -w /data "$KICAD_IMAGE" kicad-cli "$@"
  fi
}

cd -- "$ROOT" >/dev/null
sch="$project_dir/$name.kicad_sch"
pcb="$project_dir/$name.kicad_pcb"

if [[ "$what" == all ]]; then
  erc_args=(sch erc --output "$out/$name-erc.rpt")
  [[ "${ERC_STRICT:-0}" == 1 ]] && erc_args+=(--severity-error --exit-code-violations)
  kicad "${erc_args[@]}" "$sch"
  kicad sch export pdf --output "$out/$name-schematic.pdf" "$sch"
fi

kicad sch export bom --output "$assembly/$name-bom.csv" \
  --fields 'Reference,${QUANTITY},Value,MaxVoltage,Footprint,Manufacturer,MPN,Supplier' \
  --labels 'Refs,Qty,Value,MaxVoltage,Footprint,Manufacturer,MPN,Supplier' \
  --group-by Value,MaxVoltage,Footprint,MPN --exclude-dnp --ref-range-delimiter '' "$sch"

if [[ -f "$pcb" ]] && grep -q '"Edge.Cuts"' "$pcb"; then
  # Gerber: ті самі шари й опції, що в діалозі Plot (ДЗ 16, п. 3). Задані явно, бо
  # --board-plot-params у kicad-cli 10.0.5 ігнорує вимкнений X2 і прапорець --no-x2.
  # Drill: ті самі параметри, що в діалозі Generate Drill Files (ДЗ 16, п. 4):
  # PTH і NPTH в одному файлі, без карти свердління.
  rm -rf "$gerber"   # без застарілих файлів від попередніх експортів
  mkdir -p "$gerber"
  kicad pcb export gerbers --output "$gerber/" --check-zones --no-x2 --subtract-soldermask \
    --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts \
    "$pcb"
  kicad pcb export drill --output "$gerber/" --format excellon --drill-origin absolute \
    --excellon-units mm --excellon-zeros-format decimal --excellon-oval-format alternate "$pcb"
  rm -f "$mfg/$name-fab.zip"
  (cd -- "$gerber" >/dev/null && python3 -m zipfile -c "../$name-fab.zip" *)

  # Позиції компонентів для автоматичного монтажу: лише SMD (THT, кріпильні отвори,
  # тестові точки паяються вручну), обидві сторони, мм, без DNP
  kicad pcb export pos --output "$assembly/$name-all-pos.csv" --format csv --units mm \
    --side both --exclude-dnp --smd-only "$pcb"
fi

find "$out" -type f | sort
