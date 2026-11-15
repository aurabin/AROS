# Native SMP stabilization: architecture compatibility and verification

Status: engineering plan, NOT a validated fix. Scope: aurabin/AROS work/native-smp-stabilization. No QEMU.

## Verified source findings (2026-11-15)
- rom/exec/semaphores.c: InternalObtainSemaphore and InternalAttemptSemaphore protect ss_QueueCount, ss_NestCount, ss_Owner and ss_WaitQueue with Forbid/Permit; both contain SMP spinlock TODOs.
- rom/exec/releasesemaphore.c: ReleaseSemaphore also uses Forbid/Permit while updating these fields, removing waiter nodes and calling Signal/ReplyMsg.
- rom/exec/initsemaphore.c: InitSemaphore initializes the public semaphore layout; do not change public ABI without migration.
- rom/exec/schedule.c: Schedule is an unimplemented entry point, not the actual context-switch implementation.

## Required implementation sequence
1. Locate real architecture-specific scheduler, dispatch, interrupt entry/exit, and Forbid/Permit semantics. Confirm whether Forbid is CPU-local in each target.
2. Inventory all semaphore users, including message-based and shared requests. Establish lock ordering against task, signal, message-port, scheduler and memory allocator locks.
3. Implement SMP-safe semaphore arbitration without sleeping while holding a spinlock. Prove waiter insertion, signal clearing, ownership handoff and wake-up ordering cannot lose a wake-up. Keep the public SignalSemaphore ABI unchanged. Preserve non-SMP builds.
4. Review CPU feature discovery and AP startup for native x86/x86_64 Intel and AMD: CPUID, topology, local APIC/x2APIC, IOAPIC, IPI delivery, TSC assumptions, memory barriers and cache coherency. Gate optional features on detection; define safe fallback and diagnostics.
5. Audit architecture-independent SMP primitives before expanding to other supported CPU architectures. Do not assume x86 memory ordering on ARM, PPC or RISC-V.
6. Add compile-time and runtime diagnostics for unsupported CPU/APIC configurations and AP startup failures. Preserve single-core fallback.
7. Build each supported native target with clean logs, run static checks and stress tests: exclusive/shared semaphore contention, nested acquisition, timeout-free wake-up, cross-CPU signaling, concurrent interrupts, CPU bring-up/shutdown and driver stress.
8. Only commit reviewed, testable patches to this development branch. Do not merge master or publish release without native hardware evidence.

## Release gates
- Build log and toolchain versions recorded for each architecture.
- No known lock-order inversions or lost wake-ups in stress tests.
- Verified native boot and multicore load on representative Intel and AMD CPUs; documented fallbacks on unsupported hardware.
- Explicitly label unrun tests and unverified architectures; no blanket compatibility claims.

## Current blockers
- No native build logs or physical Intel/AMD test results collected in this review.
- Spinlock APIs and full scheduler call graph not yet verified; a blind Forbid-to-spinlock replacement would be unsafe.
