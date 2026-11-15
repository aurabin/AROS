#!/usr/bin/env bash
set -euo pipefail
# Diagnose only: never download or execute unverified toolchain binaries.
missing=0
for tool in git cmake make python3 x86_64-aros-gcc x86_64-aros-g++; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'OK %-20s %s\n' "$tool" "$(command -v "$tool")"
  else
    printf 'MISSING %s\n' "$tool" >&2
    missing=1
  fi
done
if [[ "$missing" -ne 0 ]]; then
  cat >&2 <<'EOF'
AROS cross-toolchain is not available.
Install a trusted x86_64-aros GCC cross-toolchain and matching AROS SDK
using the documented upstream build instructions. Add the compiler bin/
directory to PATH. Verify compiler target, sysroot, and required headers.
Do not attempt a full Odyssey build until these checks pass.
EOF
  exit 2
fi
target="$(x86_64-aros-gcc -dumpmachine)"
case "$target" in
  *aros*) printf 'Target: %s\n' "$target";;
  *) printf 'Unexpected compiler target: %s\n' "$target" >&2; exit 2;;
esac
printf 'Toolchain preflight passed (not a compilation test).\n'
