#!/usr/bin/env bash
set -euo pipefail

# Build Odyssey for AROS x86-64 using the upstream documented toolchain.
# This does not replace Odyssey's GUI or change its WebKit engine.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="${ODYSSEY_SOURCE:-$ROOT/external-src/OdysseyWebBrowser}"

for cmd in git cmake make x86_64-aros-gcc x86_64-aros-g++; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'MISSING: %s\n' "$cmd" >&2
    exit 2
  fi
done

if [[ ! -f "$SOURCE/rebuild.sh" ]]; then
  printf 'Odyssey source missing: %s\nRun tools/odyssey/fetch_upstream.sh first.\n' "$SOURCE" >&2
  exit 2
fi
branch="$(git -C "$SOURCE" branch --show-current)"
if [[ "$branch" != odyssey ]]; then
  printf 'Expected Odyssey branch odyssey; got %s\n' "$branch" >&2
  exit 2
fi
printf 'Odyssey commit: %s\n' "$(git -C "$SOURCE" rev-parse HEAD)"
printf 'C compiler: %s\n' "$(x86_64-aros-gcc -dumpversion)"
printf 'C++ compiler: %s\n' "$(x86_64-aros-g++ -dumpversion)"
printf 'Upstream expects AROS/contrib release-20241102 and GCC 6.5.0.\n'
printf 'Build step 1: cd %q && ./rebuild.sh (choose option 11, x86_64-aros Release)\n' "$SOURCE"
printf 'Build step 2: cd %q && make -j<safe-job-count>\n' "$SOURCE/cross-build-x86_64-aros"
if [[ "${1:-}" == "--run-configure" ]]; then
  cd "$SOURCE"
  ./rebuild.sh
fi
