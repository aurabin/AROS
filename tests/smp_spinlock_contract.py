#!/usr/bin/env python3
"""Static SMP spinlock contract checks; no runtime or build claim."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
intern = (root / "rom/exec/exec_intern.h").read_text()
prepare = (root / "rom/exec/prepareexecbase.c").read_text()
locks = (root / "rom/exec/exec_locks.c").read_text()
names = re.findall(r"spinlock_t\s+(\w+SpinLock|TaskSpinningLock)\s*;", intern)
assert names, "no Exec spinlocks found"
for name in names:
    assert f"EXEC_SPINLOCK_INIT(&PrivExecBase(SysBase)->{name});" in prepare, f"uninitialized: {name}"
for name in ("ExecLock__InternObtainSystemLock", "ExecLock__ObtainLock"):
    start = locks.index("int " + name + "(")
    end = locks.index("EXEC_SPINLOCK_LOCK(", start)
    body = locks[start:end]
    assert "mode != SPINLOCK_MODE_READ && mode != SPINLOCK_MODE_WRITE" in body, name
    assert body.index("mode != SPINLOCK_MODE_READ") < body.index("Disable();"), name
assert "flags && LOCKF_" not in locks
print(f"PASS: {len(names)} declared Exec spinlocks initialized; invalid modes rejected before state changes")
