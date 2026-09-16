#!/usr/bin/env bash
# git textconv для LTspice: *.asc/*.plt бувають у UTF-16LE — показуємо diff як UTF-8.
# Підключається командою `make setup` (git config diff.ltspice.textconv).
set -euo pipefail
if head -c 4096 "$1" | grep -qaP '\x00'; then
  iconv -f UTF-16LE -t UTF-8 "$1" | tr -d '\r'
else
  iconv -f LATIN1 -t UTF-8 "$1" | tr -d '\r'
fi
