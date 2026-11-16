#!/usr/bin/env python3
"""Fail-closed metadata checks for AROS One staging; no downloading or installation."""
import json
import pathlib
import sys

def validate(data):
    errors = []
    if data.get("distribution") != "AROS One":
        errors.append("unexpected distribution")
    if data.get("integration_status") != "metadata-only":
        errors.append("integration status must remain metadata-only until reviewed")
    editions = data.get("editions", [])
    if not isinstance(editions, list) or {e.get("id") for e in editions if isinstance(e, dict)} != {"x86_64-abiv11", "i386-abiv0"}:
        errors.append("both ABI-separated editions are required")
    if any(e.get("enabled") for e in editions if isinstance(e, dict)):
        errors.append("unreviewed edition cannot be enabled")
    if data.get("redistribution_authorized") is not False:
        errors.append("redistribution must remain disabled until authorized")
    if data.get("components") != []:
        errors.append("components require separate audited import workflow")
    return errors

def main():
    p = pathlib.Path(__file__).with_name("distribution.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, ValueError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2
    for err in errors:
        print("ERROR:", err, file=sys.stderr)
    if errors:
        return 1
    print("AROS One staging metadata valid; no redistribution enabled")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
