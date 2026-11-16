# Official AROS upstream synchronization policy

## Repositories and provenance

- Official upstream: https://github.com/aros-development-team/AROS (master)
- Intermediate lineage: https://github.com/deadwood2/AROS
- Development fork: https://github.com/aurabin/AROS (work/native-smp-stabilization)

GitHub reports aurabin/AROS as a fork of deadwood2/AROS. Do not describe fork commits as original upstream work. Preserve author, license, copyright, and original commit provenance.

## Compatibility boundary

Official upstream's new-ABI nightly binaries are not interchangeable with older ABI distributions. AROS One's i386 ABIv0 and x86_64 ABIv11 editions remain separately staged. Do not import binary artifacts across these targets. The AROS Wizard host application is separate from the AROS OS core.

## Safe synchronization workflow

1. Create a dedicated integration branch from a known, tested fork commit; never overwrite master or work/native-smp-stabilization.
2. In a local checkout, add upstream remotes and fetch full history:
   ```sh
   git remote add official https://github.com/aros-development-team/AROS.git
   git remote add deadwood https://github.com/deadwood2/AROS.git
   git fetch official master
   git fetch deadwood
   git merge-base HEAD official/master
   git log --oneline --left-right --cherry-pick HEAD...official/master
   ```
3. Group candidate changes by subsystem, inspect actual diffs, build prerequisites, author and license metadata.
4. Prioritize security and correctness patches for USB xHCI teardown, PCI BAR/interrupt handling, filesystem integrity, C runtime and SMP locking. Verify whether patches are already present through deadwood before applying.
5. Port narrowly scoped patches with original attribution, preferably by traceable cherry-picks where histories permit. If manually adapted, cite the original upstream commit and explain the changes.
6. Compile and run relevant unit tests, then boot target-specific images in QEMU with serial logs. Never claim boot success without logs.
7. Require review before merge, especially for ABI, scheduler, spinlocks, interrupt paths and disk-writing components.

## Release gates

- Keep root LICENSE, LEGAL and all component-specific notices intact.
- No silent rebranding of upstream code or binaries.
- No mixing ABIv0 and ABIv11 system libraries or executables.
- No unreviewed AROS One component redistribution.
- No merging unbuilt/unbooted kernel changes into a stable release.
- Report exact commit IDs, test logs, targets and remaining failures.

## Current status (2026-11-16)

Repository lineage was inspected through GitHub metadata. Official upstream news and repository identity were checked. A full commit graph comparison, patch integration, compilation and boot tests have **not** been completed. This document defines the workflow; it is not evidence of successful synchronization.
