# -*- coding: utf-8 -*-
# Task-owned temporary smoke launcher: run ddos_art.py in a real console window
# and record the return code (real console => UTF-16 WriteConsoleW output path).
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
rc = subprocess.run([sys.executable, os.path.join(HERE, "ddos_art.py")],
                    creationflags=0x00000010, timeout=120).returncode
with open(os.path.join(HERE, "_smoke_rc.txt"), "w", encoding="utf-8") as fh:
    fh.write("returncode=%d\n" % rc)
