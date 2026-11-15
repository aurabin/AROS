#!/usr/bin/env python3
"""Odyssey integration preflight tests (stdlib only).

These tests verify helper script invariants; they do NOT validate browser
runtime behavior or Chromium compatibility.
"""
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "odyssey"


class IntegrationPreflight(unittest.TestCase):
    def test_scripts_exist(self):
        for name in ("fetch_upstream.sh", "build_x86_64.sh"):
            with self.subTest(name=name):
                self.assertTrue((TOOLS / name).is_file())

    def test_bash_syntax(self):
        for name in ("fetch_upstream.sh", "build_x86_64.sh"):
            with self.subTest(name=name):
                result = subprocess.run(
                    ["bash", "-n", str(TOOLS / name)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_build_requires_real_toolchain(self):
        data = (TOOLS / "build_x86_64.sh").read_text()
        self.assertIn("x86_64-aros-gcc", data)
        self.assertIn("x86_64-aros-g++", data)
        self.assertIn("rebuild.sh", data)

    def test_upstream_branch_is_explicit(self):
        data = (TOOLS / "fetch_upstream.sh").read_text()
        self.assertIn("--branch odyssey", data)
        self.assertIn("deadwood2/OdysseyWebBrowser", data)


if __name__ == "__main__":
    unittest.main()
