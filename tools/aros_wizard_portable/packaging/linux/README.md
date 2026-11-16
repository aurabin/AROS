# Linux desktop integration

The combined cat-and-penguin SVG is installed as the AROS Wizard application icon.

The desktop entry currently launches the **command-line diagnostic program** in a terminal. It is not a graphical wizard and does not install AROS.

Build and install with CMake. For example:

```sh
cmake -S tools/aros_wizard_portable -B build/aros-wizard -DCMAKE_INSTALL_PREFIX="$HOME/.local"
cmake --build build/aros-wizard
cmake --install build/aros-wizard
```

The desktop entry is installed under `share/applications`, and the icon under `share/icons/hicolor/scalable/apps`. A desktop environment may need to refresh its application cache. The launcher assumes `aros-wizard` is in the user's PATH; for local installations, ensure `$HOME/.local/bin` is in PATH.

This change has not been tested on an actual Linux desktop.
