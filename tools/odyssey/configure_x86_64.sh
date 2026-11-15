#!/usr/bin/env bash
set -euo pipefail
# Noninteractive Odyssey x86_64 AROS CMake configuration.
# Avoids upstream rebuild.sh's machine-specific SDK_DIR and rm -rf behavior.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="${ODYSSEY_SOURCE:-$ROOT/external-src/OdysseyWebBrowser}"
SDK="${AROS_SDK_DIR:-}"
BUILD="${ODYSSEY_BUILD_DIR:-$SOURCE/cross-build-x86_64-aros}"
if [[ -z "$SDK" || ! -d "$SDK/include" || ! -d "$SDK/lib" ]]; then
  echo 'Set AROS_SDK_DIR to the matching AROS Development directory (include/ and lib/ required).' >&2
  exit 2
fi
for required in "$SDK/include/cairo" "$SDK/include/freetype" "$SDK/include/libxml2" "$SDK/lib/libz.a"; do
  if [[ ! -e "$required" ]]; then
    printf 'Missing AROS SDK dependency: %s\n' "$required" >&2
    exit 2
  fi
done
# Resolve ICU from the target SDK. The MUI port enables ICU without finding it.
for required in include/unicode/ustring.h lib/libicui18n.a lib/libicuuc.a lib/libicudata.a; do
  if [[ ! -f "$SDK/$required" ]]; then
    printf 'Missing AROS ICU dependency: %s\n' "$SDK/$required" >&2
    exit 2
  fi
done
if [[ ! -f "$SOURCE/Source/cmake/AROS.cmake" ]]; then
  echo 'Odyssey Source/cmake/AROS.cmake missing; fetch upstream first.' >&2
  exit 2
fi
for cmd in cmake x86_64-aros-gcc x86_64-aros-g++; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing: $cmd" >&2; exit 2; }
done
if [[ -e "$BUILD/CMakeCache.txt" && "${ODYSSEY_RECONFIGURE:-0}" != 1 ]]; then
  echo 'Existing CMake cache found; set ODYSSEY_RECONFIGURE=1 to reconfigure without deleting files.' >&2
  exit 2
fi
# Exercise both ICU APIs and the static target archives before configuring WebKit.
probe_dir="$(mktemp -d)"
trap 'rm -f -- "$probe_dir/icu-check" "$probe_dir/icu-check.cpp"; rmdir -- "$probe_dir"' EXIT
cat > "$probe_dir/icu-check.cpp" <<'EOF'
#include <unicode/ucol.h>
#include <unicode/ustring.h>

int main()
{
    UErrorCode status = U_ZERO_ERROR;
    UCollator* collator = ucol_open("en", &status);
    ucol_close(collator);
    const UChar value[] = { 0 };
    return U_FAILURE(status) || u_strlen(value);
}
EOF
icu_libraries=("$SDK/lib/libicui18n.a" "$SDK/lib/libicuuc.a" "$SDK/lib/libicudata.a")
x86_64-aros-g++ -static-libstdc++ -I"$SDK/include" "$probe_dir/icu-check.cpp" \
  "${icu_libraries[@]}" -o "$probe_dir/icu-check"

cmake -S "$SOURCE" -B "$BUILD" \
  -DCMAKE_TOOLCHAIN_FILE="$SOURCE/Source/cmake/AROS.cmake" \
  -DCMAKE_EXE_LINKER_FLAGS=-static-libstdc++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DPORT=MUI \
  -DCMAKE_SYSTEM_PROCESSOR=x86_64 \
  -DCMAKE_C_COMPILER=x86_64-aros-gcc \
  -DCMAKE_CXX_COMPILER=x86_64-aros-g++ \
  -DCAIRO_INCLUDE_DIRS="$SDK/include/cairo/" \
  -DFREETYPE_INCLUDE_DIRS="$SDK/include/freetype/" \
  -DLIBXML2_INCLUDE_DIR="$SDK/include/libxml2/" \
  -DICU_INCLUDE_DIRS="$SDK/include" \
  "-DICU_LIBRARIES=${icu_libraries[0]};${icu_libraries[1]};${icu_libraries[2]}" \
  -DZLIB_LIBRARIES="$SDK/lib/libz.a"
