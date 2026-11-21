"""Tests for command generation; no emulator or guest boot required."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "launcher.py"
spec = importlib.util.spec_from_file_location("aros_windows_launcher", MODULE)
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def test_valid_command(self):
        with tempfile.TemporaryDirectory() as directory:
            exe, iso = Path(directory) / "qemu.exe", Path(directory) / "aros.iso"
            exe.touch()
            iso.touch()
            cmd = launcher.qemu_command(str(exe), str(iso))
            self.assertEqual(cmd[0], str(exe))
            self.assertIn("AC97", cmd)
            self.assertIn("user,model=rtl8139", cmd)
            self.assertEqual(cmd[cmd.index("-smp") + 1], "1")

    def test_missing_executable(self):
        with self.assertRaises(ValueError):
            launcher.qemu_command("missing-qemu.exe", "missing.iso")

    def test_invalid_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            exe, iso = Path(directory) / "qemu.exe", Path(directory) / "aros.iso"
            exe.touch()
            iso.touch()
            with self.assertRaises(ValueError):
                launcher.qemu_command(str(exe), str(iso), 999)


if __name__ == "__main__":
    unittest.main()
