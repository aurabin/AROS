#!/usr/bin/env bash
set -euo pipefail
# External source checkout; no vendoring into the AROS source tree.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="${1:-$ROOT/external-src/OdysseyWebBrowser}"
if [[ -e "$DEST" ]]; then
  echo "Destination already exists: $DEST" >&2
  exit 2
fi
mkdir -p "$(dirname "$DEST")"
git clone --branch odyssey --single-branch https://github.com/deadwood2/OdysseyWebBrowser.git "$DEST"
if [[ -n "${ODYSSEY_COMMIT:-}" ]]; then
  git -C "$DEST" checkout --detach "$ODYSSEY_COMMIT"
  printf 'Requested pinned revision: %s\n' "$ODYSSEY_COMMIT"
else
  printf 'WARNING: upstream odyssey branch is moving; set ODYSSEY_COMMIT to pin a revision.\n' >&2
fi
printf 'Odyssey source checkout: %s\n' "$DEST"
printf 'Checked-out commit: '
git -C "$DEST" rev-parse HEAD
printf 'Follow upstream README for matching cross-compiler and SDK requirements.\n'
