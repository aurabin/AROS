#!/usr/bin/env python3
"""Static regression guard for SMP Wait() signal acknowledgement."""
from pathlib import Path
import re
import sys

src = (Path(__file__).resolve().parents[1] / "rom/exec/wait.c").read_text()
smp = re.search(r"#if defined\(__AROSEXEC_SMP__\)\s*__AROS_ATOMIC_AND_L\(thisTask->tc_SigRecvd,\s*~rcvd\);", src)
errors = []
if not smp:
    errors.append("SMP Wait must acknowledge the observed signal mask")
if re.search(r"__AROS_ATOMIC_AND_L\(thisTask->tc_SigRecvd,\s*~signalSet\)", src):
    errors.append("SMP Wait must not clear the entire requested mask")
if not re.search(r"rcvd\s*=\s*\(thisTask->tc_SigRecvd\s*&\s*signalSet\)", src):
    errors.append("Wait must capture received signal bits before acknowledgement")
if errors:
    print("FAIL: " + "; ".join(errors))
    sys.exit(1)
print("PASS: SMP Wait acknowledges observed bits only")
