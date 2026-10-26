# -*- coding: utf-8 -*-
# Task-owned temporary launcher: run the probe in a real console window.
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CREATE_NEW_CONSOLE = 0x00000010
subprocess.run([sys.executable, os.path.join(HERE, "_probe2_task.py")],
               creationflags=CREATE_NEW_CONSOLE, timeout=60)
