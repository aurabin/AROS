# AROS One distribution integration (staging)

AROS One is an **independent AROS distribution** maintained upstream by AMIGASYSTEM. This directory is a non-invasive integration and review area, **not a redistribution of AROS One** and not an assertion of upstream endorsement.

## Official upstream

- AROS One homepage: https://sites.google.com/view/arosone
- 64-bit edition: ABIv11, version 1.3 (as listed on the upstream homepage at initial review).
- 32-bit edition: ABIv0, version 2.9 (as listed on the upstream homepage at initial review).

These are **different ABI targets**. Never copy ABIv0 executables into ABIv11 system images, or assume 32-bit compatibility without explicit runtime testing.

## Integration boundaries

1. Preserve the root AROS `LICENSE` (APL 1.1), `LEGAL`, and component-specific licensing.
2. Keep AROS One artwork, branding, themes, configurations and third-party packages outside the core source tree until redistribution permission and provenance are verified.
3. Do not import AROS One binaries, ISO/USB images, or bundled applications based only on their presence in an upstream distribution.
4. Import components individually only after source, version, license, notices, copyright, build integration and ABI have been reviewed.
5. Prefer a separate, reproducible distribution overlay with upstream download instructions and optional locally provided files. Do not modify the AROS base build by default.
6. Document approvals and component hashes in the distribution manifest before enabling packaging.

## Status

This directory contains metadata and review templates only. **No AROS One code, icons, images, or binaries have been imported.** No integration build or compatibility test has been performed.

See `COMPONENT_REVIEW.md` and `distribution.json`.
