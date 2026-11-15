#!/usr/bin/env python3
"""Static integration checks; not an Odyssey browser runtime test."""
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools" / "odyssey"
SCRIPTS = ("fetch_upstream.sh", "build_x86_64.sh", "toolchain_preflight.sh")


class IntegrationPreflight(unittest.TestCase):
    def test_scripts_exist(self):
        for name in SCRIPTS:
            with self.subTest(name=name):
                self.assertTrue((TOOLS / name).is_file())

    def test_bash_syntax(self):
        for name in SCRIPTS:
            with self.subTest(name=name):
                result = subprocess.run(
                    ["bash", "-n", str(TOOLS / name)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_build_requires_cross_compiler(self):
        data = (TOOLS / "build_x86_64.sh").read_text()
        self.assertIn("x86_64-aros-gcc", data)
        self.assertIn("x86_64-aros-g++", data)
        self.assertIn("rebuild.sh", data)

    def test_upstream_revision_is_not_falsely_pinned(self):
        data = (TOOLS / "fetch_upstream.sh").read_text()
        self.assertIn("--branch odyssey", data)
        self.assertIn("deadwood2/OdysseyWebBrowser", data)
        self.assertIn("ODYSSEY_COMMIT", data)
        self.assertIn("Checked-out commit:", data)

    def test_toolchain_preflight(self):
        data = (TOOLS / "toolchain_preflight.sh").read_text()
        self.assertIn("-dumpmachine", data)
        self.assertIn("x86_64-aros-gcc", data)


if __name__ == "__main__":
    unittest.main()
