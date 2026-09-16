#!/usr/bin/env bash
# Генерує .docx зі звіту в Markdown.
#   tools/build-report.sh assignments/homework_07            -> build/reports/homework_07.docx
#   tools/build-report.sh motor-drive-controller/docs/design-notes.md
# Pandoc береться локальний, якщо встановлено, інакше — Docker-образ.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd)"
PANDOC_IMAGE="pandoc/core:3.6"

src="${1:?вкажіть директорію з README.md або .md-файл}"
[[ -d "$src" ]] && src="$src/README.md"
[[ -f "$src" ]] || { echo "Файл не знайдено: $src" >&2; exit 1; }

src_abs="$(cd -- "$(dirname -- "$src")" >/dev/null && pwd)/$(basename -- "$src")"
src_rel="${src_abs#"$ROOT"/}"
src_dir_rel="$(dirname "$src_rel")"
name="$(basename "$src_rel" .md)"
[[ "$name" == README ]] && name="$(basename "$src_dir_rel")"

out_rel="build/reports/${name}.docx"
mkdir -p "$ROOT/build/reports"

# Посилання в .docx ведуть на ту версію файлів, з якої зібрано звіт
ref="$(git -C "$ROOT" describe --tags --exact-match 2>/dev/null || git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo master)"
remote="$(git -C "$ROOT" remote get-url origin 2>/dev/null | sed -E 's#^git@github.com:#https://github.com/#; s#\.git$##')"

args=(
  --from gfm+raw_html --to docx
  --lua-filter tools/pandoc/report.lua
  --resource-path "$src_dir_rel"
  --metadata "author=$(git -C "$ROOT" config user.name || echo '')"
  --metadata "date=$(date +%Y-%m-%d)"
  --output "$out_rel"
)
[[ -n "$remote" ]] && args+=(--metadata "repo_blob=$remote/blob/$ref/$src_dir_rel")
[[ -f "$ROOT/tools/pandoc/reference.docx" ]] && args+=(--reference-doc tools/pandoc/reference.docx)

cd -- "$ROOT" >/dev/null
if command -v pandoc >/dev/null; then
  pandoc "${args[@]}" "$src_rel"
else
  docker run --rm -u "$(id -u):$(id -g)" -v "$ROOT:/data" -w /data "$PANDOC_IMAGE" "${args[@]}" "$src_rel"
fi
echo "$out_rel"
