# AROS Kindergarten – Windows experiment

This directory contains an experimental launcher for **QEMU-based** AROS on Windows.
It does not replace the separate native Windows-hosted AROS code in `arch/all-mingw32`.

## Requirements

- Windows 10/11 with Python 3 and Tkinter
- QEMU for Windows (`qemu-system-x86_64.exe`)
- A separately built or obtained, legally distributable AROS x86-64 boot ISO

Run `python windows/launcher.py` from the repository root and select the QEMU executable and ISO.
The launcher uses one virtual CPU, 2 GiB RAM by default, standard VGA, AC97 audio,
RTL8139 user-mode networking and CD-ROM boot.

## Verification

`python -m unittest discover -s windows/tests -v`

Unit tests verify command construction only. They do **not** demonstrate a successful
AROS build, guest boot, graphics mode change, audio playback or network connectivity.
Test these separately and record QEMU version, guest ISO SHA-256 and observed results.

## Safety and scope

No shell command interpolation is used. The launcher does not download binaries,
alter system settings, install drivers or write to the original `master` branch.
AC97 and RTL8139 are candidates for guest testing, not confirmed working devices.
SMP remains disabled pending separate synchronization and multicore validation.
