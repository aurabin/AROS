# AROS Wizard for macOS

Native Cocoa/Objective-C **development prototype** for macOS. The app shows host information in a native window. It does not install AROS or implement the full Wizard.

Build on macOS with Xcode Command Line Tools and CMake:

```sh
cmake -S tools/aros_wizard_portable -B build/aros-wizard-macos
cmake --build build/aros-wizard-macos
ctest --test-dir build/aros-wizard-macos --output-on-failure
open build/aros-wizard-macos/AROS\ Wizard.app
```

For single-config CMake generators the .app bundle should be in the build directory; multi-config generators may place it in a configuration subdirectory.

No Apple code signing, notarization, DMG installer or actual macOS runtime testing has been completed. The app is not an official release. A macOS application icon (.icns) has not yet been added.
