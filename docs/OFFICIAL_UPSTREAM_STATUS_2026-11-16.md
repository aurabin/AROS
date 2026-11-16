# Official AROS upstream status — 2026-11-16

## Verified repository relationship

- `aurabin/AROS` is a GitHub fork of `deadwood2/AROS`.
- Comparison of `work/native-smp-stabilization` against `deadwood2:master`: ahead 63, behind 0, common ancestor `5b5fd4cfd4f039927c0d1bb9cdd7f4fc8644d23e` at the time of the comparison.
- Cross-repository compare using `aros-development-team:master` returned HTTP 404, **not** proof of unrelated histories. Full Git fetch/merge-base is still needed.

## Public upstream status

- Official source: https://github.com/aros-development-team/AROS
- Official development news (October 27, 2026): https://www.aros.org/pl/news/
- Official nightly archive: https://sourceforge.net/projects/aros/files/nightly2/
- A November 14, 2026 nightly directory contains x86_64 SMP boot ISO and regular x86_64 boot ISO archives.
- Recent upstream work covers xHCI teardown/use-after-free, PCI BAR/interrupt handling, SMP networking, filesystem integrity, new toolchains and graphics.

## Import priority (not yet applied)

1. Inspect official upstream xHCI teardown and PCI interrupt/BAR changes; confirm applicability to the deadwood-based ABI.
2. Audit scheduler, spinlocks and semaphore/wakeup changes against `work/native-smp-stabilization`; no blind cherry-picks.
3. Review filesystem error propagation and bounds-checking changes.
4. Evaluate networking fixes with ABI checks.
5. Test in QEMU and on appropriate targets before merging.

## Required verification

Run `tools/upstream/audit-official-aros.sh` in a clean full checkout with network access. Record exact candidate commit hashes and diff summaries. Then create a dedicated integration branch, compile, run tests and boot images. No upstream patches have been merged, no official kernel build has been verified, and no ISO has been repackaged as a result of this status update.

Do not mix ABIv0 and ABIv11 binaries or change upstream licenses and notices.
