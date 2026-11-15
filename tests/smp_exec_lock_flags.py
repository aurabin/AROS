#!/usr/bin/env python3
"""Regression check for SMP Exec lock flag selection.

Static source check only; does not replace a kernel build or SMP runtime test.
Run from repository root: python3 tests/smp_exec_lock_flags.py
"""
from pathlib import Path
import re
import sys

source = (Path(__file__).resolve().parents[1] / "rom/exec/exec_locks.c").read_text()
functions = ("ExecLock__InternObtainSystemLock", "ExecLock__ObtainLock")
errors = []
for name in functions:
    match = re.search(r"\b(?:int|void)\s+" + name + r"\s*\(", source)
    if not match:
        errors.append(f"missing {name}")
        continue
    start = source.find("{", match.end())
    depth = 0
    end = start
    for i in range(start, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    body = source[start:end]
    for flag in ("LOCKF_DISABLE", "LOCKF_FORBID"):
        if not re.search(r"if\s*\(\s*flags\s*&\s*" + flag + r"\s*\)", body):
            errors.append(f"{name}: missing bitwise check for {flag}")
        if re.search(r"flags\s*&&\s*" + flag, body):
            errors.append(f"{name}: incorrect logical check for {flag}")
# Validate the truth table for the two independent lock flags.
# This is a host-side model of the C bitmask conditions, not a kernel runtime test.
LOCKF_DISABLE = 1
LOCKF_FORBID = 2
for flags, expected in ((0, (False, False)), (1, (True, False)),
                        (2, (False, True)), (3, (True, True))):
    actual = (bool(flags & LOCKF_DISABLE), bool(flags & LOCKF_FORBID))
    if actual != expected:
        errors.append(f"incorrect flag truth table for {flags}")

if errors:
    print("FAIL: " + "; ".join(errors))
    sys.exit(1)
print("PASS: SMP Exec lock acquisition uses individual bitwise flag tests")
