# AROS Wizard — Microsoft Store product plan

## Product goal
Publish **AROS Wizard** as a Windows application in the Microsoft Store with a target **one-time retail price of EUR 10.00**. This is a product objective, not an existing listing or confirmed release.

## Intended audience and functionality
- Windows 10/11 users exploring and managing AROS installations.
- Guided installation and configuration of supported AROS images.
- QEMU virtual machine setup, launch, logging and reproducible diagnostic profiles.
- Selectable visual themes, including a Mac-inspired Workbench 1.3 palette and optional alternative layouts.
- Hardware inventory and safe diagnostic reporting; AI-assisted suggestions only after review.
- Clear separation of AROS Wizard from BOINC.

## Engineering milestones
1. Audit existing repository, identify any executable Wizard code, determine license compatibility and upstream attribution.
2. Choose Windows packaging technology, establish a reproducible signed release build and CI checks.
3. Implement minimum viable product: GUI, image selection, QEMU setup and launch, diagnostics export, error recovery.
4. Test on supported Windows versions, with clean-install, update, uninstall and accessibility checks.
5. Prepare Store assets: description, screenshots, privacy policy, support contact, age rating and package metadata.
6. Register/configure Microsoft Partner Center developer account, validate current Store policies, fees and supported payment/pricing setup.
7. Submit for Store certification and address review feedback before launch.

## Commercial and legal considerations
- EUR 10.00 is the intended customer price, not net revenue; taxes and any applicable Store fees require confirmation.
- Review licenses of AROS, QEMU, bundled drivers, artwork, third-party components and trademark/branding permissions.
- Keep required source-code notices, attribution and source availability where licenses require them.
- Do not imply official endorsement from Microsoft, Apple, KDE, Haiku or AROS maintainers.

## Definition of done
A tested, installable, signed Windows package; verified licensing; working Store listing; successful certification; price set to EUR 10.00 in the applicable market(s).

**Status:** planning only. No Store submission, certification, or commercial release has been completed by this document.
