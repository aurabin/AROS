#!/usr/bin/env python3
"""Compare Odyssey UI screenshots against approved baselines.

Requires Python 3 standard library only. Compares identical PNG file bytes;
for pixel-level comparisons use a separate reviewed imaging dependency.
This tool does not modify Odyssey or claim browser compatibility.
"""
import argparse
import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('current', type=Path)
    args = parser.parse_args()
    for path in (args.baseline, args.current):
        if not path.is_file() or path.suffix.lower() != '.png':
            parser.error(f'Expected an existing PNG file: {path}')
    if digest(args.baseline) == digest(args.current):
        print('PASS: PNG files are byte-identical')
        return 0
    print('DIFFERENT: PNG files are not byte-identical; inspect visual changes')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
