# AROS Wizard — integration roadmap

Status: design proposal; not implemented or hardware-tested.

## Scope
AROS Wizard is an AROS-wide configuration and diagnostic project, **not** part of BOINC. This document collects proposed work for review before any implementation is merged into master.

### 1. GUI and theme system
- Modular theme loader with versioned theme manifests and fallback to a built-in safe theme.
- Mac-inspired desktop theme with Workbench 1.3 color palette; alternative KDE and Haiku-inspired layouts.
- Keep UI style separate from platform services, device drivers and installer logic.
- Keyboard navigation, localization and low-memory fallback.

### 2. QEMU virtual test field
- Reproducible QEMU machine profiles for supported AROS architectures.
- Capture boot logs, serial output, device inventories and regression artifacts.
- Explicitly distinguish simulated device behavior from real-hardware verification.

### 3. Driver diagnostics and development assistance
- Enumerate known devices and record IDs, resources and driver binding.
- Compare expected and observed behavior; produce actionable reports.
- AI-assisted code proposals must undergo code review, static checks, emulation and physical hardware testing before use.
- Never auto-load untrusted generated kernel drivers into a production installation.

### 4. Integration targets
- SMP: map current support and isolate testable milestones.
- HDToolBox: prioritize safe device enumeration, read-only diagnostics and partition safety.
- Networking and browser: identify supported stacks, dependencies and compatibility gaps.
- Multiplatform: preserve ABIv0 (32-bit), ABIv11 (64-bit) and AxRuntime build distinctions.

## Proposed implementation sequence
1. Audit upstream deadwood2/AROS and this fork, existing Wizard sources, build scripts and CI.
2. Write architecture decision record for Wizard boundaries and plugin interfaces.
3. Build a minimal theme-switching prototype with tests.
4. Add QEMU smoke-test harness and machine-readable diagnostics.
5. Prototype device inventory and reporting without modifying drivers.
6. Submit focused changes for review, with test logs and platform compatibility notes.

## Acceptance criteria
- Builds on declared targets with reproducible instructions.
- No regressions in boot, GUI startup or existing device drivers.
- Theme fallback and invalid-manifest handling tested.
- Driver changes never claimed verified solely from QEMU.
- Documentation clearly separates completed work, proposals and untested components.

## Collaboration
Discuss technical feasibility and ownership with upstream maintainers before broad integration. Keep BOINC-Client-for-AROS as a separate repository.
