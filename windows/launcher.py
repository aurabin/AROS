"""Experimental Windows launcher for an existing AROS boot ISO.

This launcher does not build AROS or claim driver compatibility.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def qemu_command(qemu: str, iso: str, memory_mb: int = 2048) -> list[str]:
    """Validate inputs and construct a safe, single-CPU QEMU invocation."""
    executable = Path(qemu).expanduser()
    image = Path(iso).expanduser()
    if not executable.is_file():
        raise ValueError("QEMU executable does not exist")
    if not image.is_file() or image.suffix.lower() != ".iso":
        raise ValueError("Select an existing .iso file")
    if memory_mb not in (1024, 2048, 4096):
        raise ValueError("Unsupported RAM setting")
    return [
        str(executable), "-machine", "pc", "-m", str(memory_mb),
        "-smp", "1", "-cdrom", str(image), "-boot", "d",
        "-vga", "std", "-device", "AC97", "-nic", "user,model=rtl8139",
    ]


def main() -> None:
    root = tk.Tk()
    root.title("AROS Kindergarten – Windows QEMU (experimental)")
    root.geometry("680x230")
    qemu = tk.StringVar(value="qemu-system-x86_64.exe")
    iso = tk.StringVar()
    memory = tk.IntVar(value=2048)

    def browse(variable: tk.StringVar, filetypes: list[tuple[str, str]]) -> None:
        result = filedialog.askopenfilename(filetypes=filetypes)
        if result:
            variable.set(result)

    for row, (label, variable, types) in enumerate((
        ("QEMU executable", qemu, [("Executable", "*.exe"), ("All files", "*.*")]),
        ("AROS ISO", iso, [("ISO image", "*.iso")]),
    )):
        ttk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=12, pady=10)
        ttk.Entry(root, textvariable=variable, width=55).grid(row=row, column=1, sticky="ew")
        ttk.Button(root, text="Browse", command=lambda v=variable, t=types: browse(v, t)).grid(row=row, column=2, padx=8)
    ttk.Label(root, text="RAM (MB)").grid(row=2, column=0, padx=12, sticky="w")
    ttk.Combobox(root, textvariable=memory, values=(1024, 2048, 4096), state="readonly", width=12).grid(row=2, column=1, sticky="w")

    def launch() -> None:
        try:
            cmd = qemu_command(qemu.get(), iso.get(), memory.get())
            subprocess.Popen(cmd, shell=False)
        except (ValueError, OSError) as exc:
            messagebox.showerror("AROS launch failed", str(exc))

    ttk.Button(root, text="Start AROS in QEMU", command=launch).grid(row=3, column=1, pady=20)
    root.columnconfigure(1, weight=1)
    root.mainloop()


if __name__ == "__main__":
    main()
