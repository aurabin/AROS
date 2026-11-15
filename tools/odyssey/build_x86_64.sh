#!/usr/bin/env bash
set -euo pipefail
# Odyssey build preflight. Preserves upstream browser sources and GUI.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="${ODYSSEY_SOURCE:-$ROOT/external-src/OdysseyWebBrowser}"
for cmd in git cmake make x86_64-aros-gcc x86_64-aros-g++; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'MISSING: %s\n' "$cmd" >&2
    exit 2
  fi
done
if [[ ! -f "$SOURCE/rebuild.sh" ]]; then
  printf 'Odyssey source missing: %s\n' "$SOURCE" >&2
  exit 2
fi
branch="$(git -C "$SOURCE" branch --show-current)"
if [[ "$branch" != odyssey && -z "${ODYSSEY_COMMIT:-}" ]]; then
  printf 'Expected branch odyssey or explicit ODYSSEY_COMMIT; got %s\n' "$branch" >&2
  exit 2
fi
if [[ -n "${ODYSSEY_COMMIT:-}" && "$(git -C "$SOURCE" rev-parse HEAD)" != "$(git -C "$SOURCE" rev-parse "$ODYSSEY_COMMIT^{commit}")" ]]; then
  echo 'Checked-out Odyssey revision does not match ODYSSEY_COMMIT' >&2
  exit 2
fi
printf 'Odyssey commit: %s\n' "$(git -C "$SOURCE" rev-parse HEAD)"
printf 'C compiler: %s\n' "$(x86_64-aros-gcc -dumpversion)"
printf 'C++ compiler: %s\n' "$(x86_64-aros-g++ -dumpversion)"
if [[ "${1:-}" == '--run-configure' ]]; then
  cd "$SOURCE"
  ./rebuild.sh
fi
