# AROS Universal License Compatibility Framework (initial release)

This is a **metadata validation tool**, not a universal license or an automated legal compatibility determination. It does not relicense any existing AROS files.

## Scope

Existing AROS components remain governed by their existing licenses, including the root `LICENSE`, `LEGAL`, and component-specific notices. The new JSON manifest is for **future third-party imports only**; it is intentionally empty at initial publication. An empty manifest does not mean there are no third-party dependencies.

## New import process

1. Verify the source, ownership, revision, redistribution permission, and license terms.
2. Record component name, upstream URL, immutable revision, SPDX license expression (when known), copyright, local notice path and review status in `third_party_manifest.json`.
3. Keep the upstream license and notices; update root `LEGAL` and other required attribution files as appropriate.
4. Request human review of linking, copyleft, patent and distribution obligations. Set `approved` only with a traceable `review_reference`.
5. Run `python tools/license_framework/check_manifest.py tools/license_framework/third_party_manifest.json --root .` and `cd tools/license_framework && python -m unittest discover -v`.

The validator checks required fields and notice-file existence, **not** whether a license is compatible or a review is correct. Unknown, custom, missing, proprietary, GPL/AGPL/LGPL/MPL/Apache and other licenses must not be assumed compatible based on a string match. No automatic source import or relicensing is performed.

See `docs/THIRD_PARTY_LICENSE_INTEGRATION.md` for the proposed policy.
