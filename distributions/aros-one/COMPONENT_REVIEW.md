# AROS One component compatibility review

This is a **preliminary triage**, not legal advice, a compatibility certification, or a completed component audit. Upstream release notes and distribution descriptions do not establish each bundled file's license.

| Candidate | Technical scope | Licensing/provenance action | Decision |
|---|---|---|---|
| AROS core updates already present upstream | ABI-specific kernel, libraries, drivers | Compare source commits and APL/LEGAL notices; avoid copying compiled system files | Review upstream patches individually |
| Wanderer preferences and configurations | Desktop preferences | Determine authorship, file-level license and redistribution permissions; check API/config compatibility | Hold |
| AROS One themes, icons, backgrounds, sounds | Artwork/assets | Require explicit artwork licensing and attribution; software licenses do not automatically cover art | Hold |
| DOpus / Magellan integration | Third-party desktop/file manager | Verify exact component versions, licenses and distribution conditions | Hold |
| OWB browser configurations | Browser settings | Verify provenance and config file rights; test against target ABI | Hold |
| SMB2 handler and other networking tools | Third-party application or system add-on | Check individual upstream licenses, dependency notices and ABI | Hold |
| AROS One installation scripts | Distribution-specific scripts | Obtain script source and permission; audit destructive disk operations | Hold |
| Bundled games, demos, emulators | Mixed third-party software and media | Per-package review, including artwork/audio rights | Exclude by default |

## Review checklist

For each proposed import, record:

- Exact upstream URL, release, source commit and checksum.
- File list, copyright holder(s), SPDX identifier where supported, full license and NOTICE texts.
- Whether the rights holder authorizes modification and redistribution.
- AROS APL 1.1 interaction and component-specific LEGAL obligations.
- ABI and architecture (ABIv0/i386 vs ABIv11/x86_64).
- Build steps, dependency versions, tests, and rollback plan.
- Reviewer identity, review date and evidence reference.

**Decision rule:** No component is automatically approved because it is included in AROS One. AROS One remains a separately maintained distribution.
