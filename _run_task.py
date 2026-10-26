# -*- coding: utf-8 -*-
# Task-owned temporary generic launcher: run a script in a real console window.
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, sys.argv[1])],
               creationflags=0x00000010, timeout=60)   # CREATE_NEW_CONSOLE
