#!/usr/bin/env python3
"""Static SMP semaphore audit for the AROS Exec implementation.

Run from the repository root: python3 tests/smp_semaphore_audit.py
This is a regression guard, NOT a concurrency or hardware test.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "rom/exec/semaphores.c": ("InternalObtainSemaphore", "InternalAttemptSemaphore"),
    "rom/exec/releasesemaphore.c": ("ReleaseSemaphore",),
}
MUTATIONS = re.compile(r"sigSem->(?:ss_QueueCount|ss_NestCount|ss_Owner|ss_WaitQueue)")
WAIT = re.compile(r"\bWait\s*\(")
WAKE = re.compile(r"\b(?:Signal|ReplyMsg)\s*\(")
failed = False

for name, functions in FILES.items():
    path = ROOT / name
    if not path.is_file():
        print(f"FAIL missing: {name}")
        failed = True
        continue
    source = path.read_text(encoding="utf-8")
    for function in functions:
        if function not in source:
            print(f"FAIL missing function: {name}: {function}")
            failed = True
    mutations = len(MUTATIONS.findall(source))
    print(f"{name}: {mutations} semaphore field references; "
          f"Wait={len(WAIT.findall(source))}; wake={len(WAKE.findall(source))}")
    if mutations == 0:
        print(f"FAIL unexpected empty semaphore access set: {name}")
        failed = True
    # Flag scheduling and wakeup boundaries for manual review.
    if name.endswith("/semaphores.c") and WAIT.search(source):
        print("REVIEW: Wait() must release cross-CPU locks and avoid lost wakeups")
    if name.endswith("/releasesemaphore.c") and WAKE.search(source):
        print("REVIEW: wakeup must preserve ownership handoff and lock ordering")
    if name.endswith("/releasesemaphore.c") and "ss_NestCount--" in source:
        if not re.search(r"ss_NestCount\s*<=\s*0", source):
            print("REVIEW: release has no explicit nest-count underflow guard")
    # A Forbid/Permit pair is not proof of cross-CPU exclusion.
    if re.search(r"\bForbid\s*\(", source) and re.search(r"\bPermit\s*\(", source):
        print(f"UNRESOLVED SMP REVIEW: {name} uses Forbid/Permit for arbitration")
        failed = True

if failed:
    print("FAIL: SMP semaphore synchronization not verified; do not claim kernel is fixed.")
    sys.exit(1)
print("PASS: no known Forbid/Permit arbitration pattern detected; manual concurrency review still required.")
