# SMP-safe Exec SignalSemaphore design (proposed; not implemented)

## Problem and invariants

`Forbid()/Permit()` prevent task switches locally, not concurrent writes on other CPUs. `InternalObtainSemaphore`, `InternalAttemptSemaphore` and `ReleaseSemaphore` mutate `ss_QueueCount`, `ss_NestCount`, `ss_Owner`, and `ss_WaitQueue` under Forbid only. `Wait(SIGF_SINGLE)` breaks Forbid; `Signal()` interacts with `TS_WAIT` and `krnSysCallReschedTask()`. Replacing Forbid with a spinlock around the existing function would block while holding that lock and deadlock.

Required invariants:
1. All reads/writes of semaphore ownership, counters, and wait queue during arbitration are serialized across CPUs.
2. A waiter is enqueued and its wakeup condition armed before releasing the arbitration lock.
3. No spinlock is held during `Wait()`, `Signal()`, `ReplyMsg()`, or a potentially scheduling call.
4. An early wakeup cannot be lost between enqueue and sleep. Verify this against `Wait()` / `Signal()` / scheduler state transitions, not just signal-bit atomics.
5. Release transfers ownership exactly once; shared and exclusive queue ordering and nesting counts retain current semantics.
6. Preserve public `struct SignalSemaphore` layout, m68k legacy initialization behavior, and single-CPU semantics.
7. Interrupt-context calls, nested Forbid/Disable, and initialization before execlock.resource availability must be explicitly accounted for.

## Proposed implementation sequence

**A. Verify primitives first.** Trace execlock.resource's `ObtainLock/ReleaseLock` and initialization; identify existing atomic spinlock operations, IRQ-safe variants and memory-order guarantees. Check whether these primitives are safe in Exec pre-init. Do not cast a semaphore wait queue to a system-lock list without verifying the implementation.

**B. Introduce private arbitration.** Prefer a fixed, statically initialized set of internal hashed locks keyed by semaphore address, or a dedicated private lock table with guaranteed early initialization. Hash collisions reduce concurrency but must not change correctness. Ensure lock acquisition is safe for the call context. Avoid adding fields to the public semaphore structure. Non-SMP retains its established behavior.

**C. Split acquisition into phases.** Under the arbitration lock: validate, decide immediate acquisition vs enqueue, clear/arm SIGF_SINGLE atomically, enqueue waiter and update counts. Release lock before blocking. If enqueued, `Wait(SIGF_SINGLE)` must tolerate a signal delivered immediately after unlock. Prove the scheduler's TS_WAIT transition cannot overwrite an already-queued wakeup. Restore nesting/Forbid behavior exactly as documented.

**D. Split release into phases.** Under the same lock: validate counts, select and detach eligible waiter(s), update owner/nesting/counts, and capture wakeup actions. Unlock before invoking Signal/ReplyMsg. A stack-allocated `SemaphoreRequest` must not be dereferenced after the waiter can resume: copy wakeup targets while locked and ensure any message storage lifetime is safe. Shared wakeups require a bounded, allocation-safe strategy; never retain pointers to waiter stack frames across unlock.

**E. Prove lock order.** Document ordering among semaphore arbitration, TaskWait/TaskReady locks, interrupt masking and IPI paths. Do not acquire a scheduler lock under the semaphore lock if the reverse order is possible.

## Mandatory tests before calling this fixed

- Static audit: `python3 tests/smp_semaphore_audit.py` (expected to fail until cross-CPU arbitration is implemented).
- Single-core regression: exclusive/shared acquisition, recursive acquisition, failed attempts, mixed wait queue ordering, semaphore messages, pre-init.
- SMP stress: 2/4/8 CPUs, 100k+ iterations, simultaneous acquire/release, preemption, immediate wakeups, interrupt-triggered Signal, randomized scheduling.
- Race tests: release between enqueue and Wait, multiple concurrent releases, shared waiter batches, waiter termination.
- Build targets independently; record toolchain and commit SHA. No QEMU requirement. No merge into master or release without validated tests.

## Status

Design only. No kernel synchronization fix or hardware validation is claimed. Implement after reviewing execlock.resource, architecture spinlock definitions, and the kernel scheduler transition.
