# AROS kernel modernization: compatibility-first SMP

Status: engineering specification, NOT an implemented Linux-equivalent kernel.
Target: work/native-smp-stabilization. Do not change master.

## Compatibility invariants
- Preserve public Exec ABI, struct layouts, library vectors and Amiga API semantics.
- Preserve uniprocessor behavior; gate SMP-only implementation under __AROSEXEC_SMP__.
- Forbid/Permit remain task-local scheduling suppression, not an inter-CPU mutex.
- Wait() breaks Forbid/Disable as documented; never hold a spinlock across Wait(), ReplyMsg(), or blocking operations.
- Keep legacy m68k semaphore initialization behavior.

## Required SMP synchronization protocol
1. Locate the existing scheduler state locks and their initialization before adding any lock.
2. Establish one lock ordering across task state, run/wait queues, semaphore ownership and signal bits.
3. Enqueue a semaphore waiter and publish the wait predicate under the appropriate lock.
4. Transition RUN -> WAIT atomically with respect to signal delivery, or recheck the predicate under the same synchronization before switching.
5. Release all spinlocks before context switching or blocking.
6. Signal delivery must atomically publish the signal and transition WAIT -> READY exactly once.
7. ReleaseSemaphore must transfer ownership and detach waiters under lock, then signal detached waiters outside the lock. Prove stack-allocated waiter lifetime.
8. Audit exception paths, interrupts, cross-CPU IPIs, and task removal.

## Validation gates
- Compile SMP and non-SMP kernels with the supported cross-toolchain.
- Static checks: lock acquisition/release balance, no blocking under spinlock, no unsafe task-state writes.
- Race tests: signal-before-wait, signal-during-wait, signal-after-wait, shared/exclusive contention, nested Forbid/Permit.
- Stress on 2, 4, 8 CPUs, at least 100,000 iterations per configuration.
- Verify ABI/layout unchanged and existing Amiga-compatible tests pass.
- Never label stable without reproducible build logs and runtime evidence.

## Known outstanding risks
- Wait/Signal transition not yet proven race-free.
- Semaphore arbitration remains based on Forbid in existing code.
- Spinlock initialization and ordering not fully audited.
- No confirmed SMP runtime or full kernel build.
