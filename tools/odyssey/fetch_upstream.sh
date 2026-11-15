#!/usr/bin/env bash
set -euo pipefail
# Source integration only: do not vendor large third-party trees into AROS.
# Odyssey's development branch is 'odyssey', not 'master'.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="${1:-$ROOT/external-src/OdysseyWebBrowser}"
if [[ -e "$DEST" ]]; then
  echo "Destination already exists: $DEST" >&2
  exit 2
fi
mkdir -p "$(dirname "$DEST")"
git clone --branch odyssey --single-branch https://github.com/deadwood2/OdysseyWebBrowser.git "$DEST"
printf 'Odyssey source checkout: %s\n' "$DEST"
printf 'Pinned commit: '
git -C "$DEST" rev-parse HEAD
printf 'Before building, follow upstream README cross-compiler/SDK instructions.\n'
