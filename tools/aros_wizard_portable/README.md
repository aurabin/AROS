# AROS Wizard portable host editions (early prototype)

Three intended editions: Linux, BSD (FreeBSD/OpenBSD/NetBSD/DragonFly), and Haiku OS.

This first implementation is a **portable command-line skeleton**, not the existing AROS Wizard GUI, an installer, or a working AROS configuration tool. No existing Wizard source was identified during this initial repository search. The program has no external runtime dependencies and performs read-only diagnostics.

## Build on each target host

Requires a C99 compiler and CMake.

```sh
cmake -S tools/aros_wizard_portable -B build/aros-wizard-portable
cmake --build build/aros-wizard-portable
ctest --test-dir build/aros-wizard-portable --output-on-failure
./build/aros-wizard-portable/aros-wizard --diagnose
```

Linux, BSD and Haiku builds need testing on the corresponding actual host or CI runner. Cross-compiling is not equivalent to runtime testing. No native GUI, AROS driver management, image creation or installation functionality is provided yet.

## Roadmap

1. Locate or import the actual AROS Wizard application source, preserving original license and attribution.
2. Separate platform-independent wizard logic from OS-specific backends.
3. Add Linux backend, BSD backends, and Haiku backend using their native APIs.
4. Add GUI with a supported toolkit, package installers and host-specific tests.
5. Preserve AROS root LICENSE/LEGAL and record new dependencies in the third-party license manifest.
