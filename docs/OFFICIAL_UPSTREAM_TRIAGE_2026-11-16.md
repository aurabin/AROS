# AROS upstream follow-up — 2026-11-16

This update records new upstream triage without claiming a merge or build.

## Verified fork state

The previous GitHub comparison against deadwood2:master showed 63 commits ahead, zero behind, with merge-base 5b5fd4cfd4f039927c0d1bb9cdd7f4fc8644d23e. Counts can change after new commits.

## New review candidates

The official AROS weekly report for November 1–7 describes 179 master commits, a large graphics subsystem rename from nouveau.hidd to nvgfx.hidd and the addition of NVK, Zink and Lavapipe. These are substantial architectural changes and must **not** be blindly cherry-picked into the deadwood-based ABIv11 fork.

Source: https://mail.arosworld.org/infusions/forum/viewthread.php?rowstart=20&thread_id=2153

Candidate priority:
1. SMP and networking correctness patches with narrow diffs and explicit ABI review.
2. Filesystem integrity and USB xHCI fixes, subject to source comparison.
3. Graphics modernization only as a separately scoped experimental branch with dependencies and build tests.

## Next execution gate

Run tools/upstream/audit-official-aros.sh in a full clean checkout with network access. Capture commit IDs and relevant diff hunks; compare with existing deadwood patches. Do not import binaries or merge incompatible ABI branches. Require compilation and QEMU boot logs for any kernel changes.

## Actual outcome

Status note updated; no official commits fetched into a local checkout here, no patches applied, and no build or boot tests performed.
