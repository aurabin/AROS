#!/usr/bin/env python3
"""Static regression for Signal() from interrupt context.

Does not establish scheduler or SMP race freedom.
"""
from pathlib import Path
import re

source = (Path(__file__).resolve().parents[1] / "rom/exec/signal.c").read_text()
assert "if (!task)" in source, "NULL signal target must be rejected"
assert re.search(r"thisTask\s*!=\s*NULL\s*&&\s*task->tc_Node\.ln_Pri\s*>\s*thisTask->tc_Node\.ln_Pri", source), (
    "priority comparison must not dereference absent current task"
)
assert "if (thisTask->tc_State == TS_RUN)" in source, "reschedule state guard unexpectedly missing"
print("PASS: Signal() priority comparison guards absent current task")
