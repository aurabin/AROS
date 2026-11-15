#!/usr/bin/env python3
"""Conservative third-party license manifest validator. No legal conclusions."""
import argparse
import json
import pathlib
import sys

REQUIRED = ("name", "source_url", "revision", "license_expression", "copyright", "notice_path", "review_status")
STATUSES = {"approved", "pending", "rejected"}

def validate(data, root):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("components"), list):
        return ["manifest must contain a components array"]
    for i, item in enumerate(data["components"]):
        prefix = f"components[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        for key in REQUIRED:
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{prefix}: missing {key}")
        if item.get("review_status") not in STATUSES:
            errors.append(f"{prefix}: invalid review_status")
        if item.get("review_status") == "approved" and not item.get("review_reference"):
            errors.append(f"{prefix}: approved requires review_reference")
        notice = item.get("notice_path")
        if isinstance(notice, str) and notice.strip():
            p = pathlib.PurePosixPath(notice)
            if p.is_absolute() or ".." in p.parts or not (root / notice).is_file():
                errors.append(f"{prefix}: notice_path must reference a repository file")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=pathlib.Path)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."))
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors = validate(data, args.root.resolve())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"Validated {len(data['components'])} third-party manifest entries (metadata only; not legal approval)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
