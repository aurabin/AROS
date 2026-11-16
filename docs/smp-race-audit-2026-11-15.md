# SMP race audit — 2026-11-15

Branch: work/native-smp-stabilization. This audit does not claim a completed SMP protocol.

## Verified source paths
- rom/exec/prepareexecbase.c initializes 11 Exec list spinlocks declared in rom/exec/exec_intern.h.
- rom/exec/exec_locks.c uses EXEC_SPINLOCK_LOCK/UNLOCK for mapped Exec system lists; flags independently select Disable and Forbid.
- rom/exec/semaphores.c uses Forbid/Permit to arbitrate ss_Owner, ss_NestCount, ss_QueueCount and ss_WaitQueue; Forbid is not a cross-CPU lock.
- rom/exec/releasesemaphore.c calls Signal/ReplyMsg while under Forbid, with stack-backed SemaphoreRequest waiters.
- rom/exec/wait.c checks tc_SigRecvd before setting tc_State = TS_WAIT and KrnSwitch; no common lock with Signal has been identified.
- rom/exec/signal.c atomically ORs tc_SigRecvd on SMP and calls krnSysCallReschedTask for TS_WAIT; the transition handshake remains unproven.
- Signal() can be called from interrupt context, so GET_THIS_TASK can be NULL; commit 3ed68b23 guards the priority comparison.

## Blocking design questions before editing semaphore arbitration
1. Locate krnSysCallReschedTask and KrnSwitch implementations for each supported SMP architecture.
2. Identify the authoritative lock protecting tc_State transitions and ready/wait queue membership.
3. Define lock ordering for task-state, signal bits, semaphore state and scheduler queues; include interrupt and IPI paths.
4. Design a stable semaphore lock mapping without changing public SignalSemaphore layout; document lifetime, aliasing, initialization and hashing collision behavior.
5. Preserve the stack-backed waiter lifetime and ensure no wakeup can occur before waiter state is published; never block holding a spinlock.
6. Verify shared/exclusive waiter ordering and reply-message handling before moving Signal/ReplyMsg outside the critical section.

## Validation requirements
- Compile SMP and UP targets and run the tests in tests/.
- Host tests alone are not evidence of race freedom.
- Reproduce signal-before-wait, signal-during-wait, concurrent releases, shared/exclusive contention and CPU migration.
- Run instrumented 2/4/8 CPU stress and capture logs.

## Status
No new semaphore spinlock or Wait/Signal synchronization protocol was committed in this audit because scheduler lock semantics have not been verified. Existing ABI is unchanged.
