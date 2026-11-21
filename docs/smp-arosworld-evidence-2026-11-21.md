# SMP status and upstream evidence — 2026-11-21

## Confirmed public demonstration

AROSWorld thread: https://www.arosworld.org/infusions/forum/viewthread.php?pid=15935&thread_id=2211

Danilos reports that AROSA ran with four logical processors active, while networking, browsing, rendering and monitoring were in progress. The same thread explicitly cautions that intermittent freezes, locking issues, and single-processor assumptions remain. This is a milestone demonstration, **not** a stable-SMP certification for this fork.

A discussion of the upstream `rom/exec/signal.c` notes that the wakeup path chooses the first CPU allowed by the affinity mask rather than the least busy CPU. This is a possible performance issue; it is not proof of the cause of the observed freezes. Reference: https://github.com/aros-development-team/AROS/blob/58b0682b/rom/exec/signal.c#L164-L204

## Verified failure in this repository

GitHub Actions run: https://github.com/aurabin/AROS_Kindergarten/actions/runs/43778993139

The `Validate lock flag bitmasks` job printed:
- `PASS: SMP Exec lock acquisition uses individual bitwise flag tests`
- `FAIL: SMP Wait must acknowledge the observed signal mask`

The workflow executes `python3 tests/smp_exec_lock_flags.py` followed by `python3 tests/smp_wait_signal_ack.py`. The latter fails. This is a reproducible static regression failure in the run; it does not independently prove a runtime SMP failure.

## Observed source-level risks

The fork's `rom/exec/signal.c` uses a CPU-affinity-based IPI path and selects the first eligible CPU when the target is not running. In SMP mode it atomically ORs `tc_SigRecvd`, but the task-state checks and wait/ready transitions require a verified shared synchronization contract. Local interrupt disabling alone is not cross-CPU mutual exclusion.

## Required next steps before changing kernel behavior

1. Compare current upstream `Wait()`, `Signal()`, scheduler and semaphore implementation against this fork using exact commit IDs.
2. Inspect `tests/smp_wait_signal_ack.py` alongside `rom/exec/wait.c`; distinguish a stale parser expectation from an actual missing acknowledgment.
3. Design and review cross-CPU synchronization with explicit lock ordering, interrupt-context constraints and ABI compatibility.
4. Build both uniprocessor and SMP x86-64 images, then run reproducible 2/4/8-CPU stress tests with trace logs.
5. Benchmark wakeup latency and useful throughput before changing CPU selection heuristics.
6. Keep pull request #2 in draft until the above evidence is available.

No claim of a completed SMP repair, successful kernel build or multicore stress test is made here.
