#!/usr/bin/env bash
# Генерує артефакти KiCad-проєкту в build/hardware/:
#   ERC-звіт, схема у PDF, BOM у CSV.
# ERC_STRICT=1 — завершитися з помилкою, якщо ERC знайшов помилки (severity error).
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd)"
KICAD_IMAGE="kicad/kicad:10.0"

project_dir="${1:-motor-drive-controller/hardware/kicad}"
pro="$(ls "$ROOT/$project_dir"/*.kicad_pro)"
name="$(basename "$pro" .kicad_pro)"
out="build/hardware"
mkdir -p "$ROOT/$out"

kicad() {
  if command -v kicad-cli >/dev/null; then
    kicad-cli "$@"
  else
    docker run --rm -u "$(id -u):$(id -g)" -e HOME=/tmp -v "$ROOT:/data" -w /data "$KICAD_IMAGE" kicad-cli "$@"
  fi
}

cd -- "$ROOT" >/dev/null
sch="$project_dir/$name.kicad_sch"

erc_args=(sch erc --output "$out/$name-erc.rpt")
[[ "${ERC_STRICT:-0}" == 1 ]] && erc_args+=(--severity-error --exit-code-violations)
kicad "${erc_args[@]}" "$sch"
kicad sch export pdf --output "$out/$name-schematic.pdf" "$sch"
kicad sch export bom --output "$out/$name-bom.csv" \
  --fields 'Reference,Value,Footprint,${QUANTITY},${DNP}' \
  --labels 'Refs,Value,Footprint,Qty,DNP' \
  --group-by Value,Footprint --ref-range-delimiter '' "$sch"

ls -1 "$out"
