# -*- coding: utf-8 -*-
# Task-owned temporary launcher: run the verification in a real console window.
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, "_verify_task.py")],
               creationflags=0x00000010, timeout=60)   # CREATE_NEW_CONSOLE
