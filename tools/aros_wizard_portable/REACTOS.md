# AROS Wizard for ReactOS — Win32 preview

ReactOS aims to support Win32 applications. This prototype uses only standard Win32 user32/gdi32 interfaces and can also be tried on Windows.

## Build

From the repository root with MinGW-w64 on Linux:

```sh
i686-w64-mingw32-gcc -std=c99 -Wall -Wextra -municode -x c /dev/null -o /tmp/ignore.exe
```

The line above is **not** the application build. Use the actual application command:

```sh
i686-w64-mingw32-gcc -std=c99 -Wall -Wextra -mwindows tools/aros_wizard_portable/reactos_gui.c -o aros-wizard-reactos.exe -luser32 -lgdi32
```

Alternatively, use CMake on a Windows-compatible MinGW or MSVC toolchain with `-DAROS_WIZARD_REACTOS_GUI=ON`.

Run the resulting executable inside a **ReactOS virtual machine**. Compatibility has not yet been verified on ReactOS. No privileged operations, AROS installation, or system modifications are implemented.

The ReactOS edition is a proof-of-concept GUI. Actual AROS Wizard logic must be integrated after locating the original application sources. Keep existing AROS licensing and attribution.
