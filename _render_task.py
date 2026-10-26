# -*- coding: utf-8 -*-
# Task-owned temporary render check: rebuild box1/box2 + labels exactly as
# show_main_screen does, then verify every row of a box shares one display width.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_render_out.txt")
sys.path.insert(0, HERE)

import ddos_art as A

A.init()                       # calibrates real console widths
A._COLOR = True                # keep the same paint()/gradient behavior as the app

res = []
res.append("calibrated glyphs = %d" % len(A._GLYPH_W))

def strip(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)

# --- box 1 (welcome) exactly as in show_main_screen ---
welcome = [
    A.paint("Welcome to \U0001d4e1\U0001d4ea\U0001d4f2\U0001d4f7\U0001d4ec2 made by "
            "\U0001d4e2\U0001d4ee\U0001d4f8\U0001d4f1\U0001d4fe", A.C.W, bold=True),
    A.paint("Type HELP for a list of All C2 Commands.", A.C.Y, bold=True),
]
box1 = A.dbl_panel(welcome, indent=2, width=48, text_center=True)
A._engrave_top(box1, A.paint("\u2605 \U0001d4f8\U0001d4f7\U0001d4f5\U0001d4fe "
                             "\U0001d4ef\U0001d4f8\U0001d4fb \U0001d4fd\U0001d4ee\U0001d4fc"
                             "\U0001d4fd\U0001d4f2\U0001d4f7\U0001d4f0 \u2605",
                             A.C.Y, bold=True))
res.append("[box1] row display-widths:")
for ln in box1:
    res.append("   w=%3d | %s" % (A._plain(ln), strip(ln)))

# --- box 2 (copyright) ---
copyr = [A.paint("Copyright \u00a9 2026 RAIN, All Rights Reserved!", A.C.CY, bold=True)]
box2 = A.dbl_panel(copyr, indent=2, width=70, text_center=True)
res.append("[box2] row display-widths:")
for ln in box2:
    res.append("   w=%3d | %s" % (A._plain(ln), strip(ln)))

# --- box2 decorative label (as _label_over builds it) ---
top = box2[0]
indent = len(top) - len(top.lstrip())
inner_w = len(top.lstrip()) - 2
label = A.paint("\u263e\u207a\u208a \U0001d4f3\U0001d4f8\U0001d4f2\U0001d4f7 "
                "\U0001d4ed\U0001d4f2\U0001d4fc\U0001d4ec\U0001d4f8\U0001d4fb\U0001d4ed"
                ".\U0001d4f0\U0001d4f0/\U0001d4ea56\U0001d4a3\U0001d4d4\U0001d4d9"
                "6\U0001d4f3  \u263e\u207a\u208a", A.C.M, bold=True)
off = indent + max(0, (inner_w - A._plain(label)) // 2)
lab_line = " " * off + label
res.append("[box2 label] inner_w=%d label_w=%d offset=%d" % (inner_w, A._plain(label), off))
res.append("   w=%3d | %s" % (A._plain(lab_line), strip(lab_line)))
res.append("   centered over box2 width %d ? start_col=%d end_col=%d"
           % (A._plain(top), off, off + A._plain(label)))

# --- gradient prompt bar (colors must survive) ---
prompt = A._grad_prompt("  \u211b\U0001d4b6\U0001d4be\U0001d4c3 \u263e\u207a\u208a >> ")
res.append("[prompt] plain width = %d" % A._plain(prompt))
res.append("   raw = %r" % prompt)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(res))
