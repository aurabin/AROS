# AROS third-party license integration policy (draft)

This document does **not** relicense AROS or authorize importing arbitrary code.

## Rules

1. Keep existing AROS source under its existing license and preserve copyright notices.
2. Record every imported component's source URL, revision, SPDX license identifier (if applicable), copyright holders, notices, modifications, and distribution obligations.
3. Review compatibility for the **specific** AROS component and combination (static linking, dynamic linking, process separation, distribution). License names alone do not establish compatibility.
4. Permissive MIT/BSD/ISC code: check attribution and notice conditions before inclusion.
5. Apache-2.0, MPL-2.0, LGPL, GPL, AGPL and other copyleft or patent-bearing licenses: require documented legal/technical review before combining or distributing; prefer isolated packages where appropriate.
6. Proprietary, source-available, unknown, custom, or missing licenses: do not import without explicit authorization and review.
7. Maintain a component-level license manifest and upstream LEGAL/NOTICE files where required.
8. Never change upstream licenses, strip notices, or claim that all licenses can be merged.

## Proposed CI checks (not yet implemented)

- Detect SPDX identifiers and missing license metadata.
- Generate a third-party component manifest and attribution report.
- Flag potentially incompatible combinations for human review; do not treat automated flags as legal conclusions.
- Fail imports with unknown license or missing provenance until reviewed.

## Status

Policy proposal only. No external code merged; no license compatibility audit or build tests performed by this document.
