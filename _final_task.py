# -*- coding: utf-8 -*-
# Task-owned temporary final check: capture the main screen layout, confirm the
# blank line between boxes, and confirm every input() prompt uses the gradient box.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_final_out.txt")
sys.path.insert(0, HERE)

import ddos_art as A

A.init()
A._COLOR = True
res = ["calibrated glyphs = %d" % len(A._GLYPH_W)]

def strip(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)

# ---- capture main screen layout ----
caps = []
A.typewrite = lambda text, delay=None, end="\n": caps.append(text)
A.print = lambda *a, **k: caps.append("__BLANK__" if not a else " ".join(str(x) for x in a))
A.clear_screen = lambda: None
A.show_main_screen(0)

res.append("[main screen] captured lines (ANSI stripped):")
for ln in caps:
    tag = "" if ln != "__BLANK__" else "  <-- blank print()"
    res.append("   w=%3d | %s%s" % (A._plain(ln), strip(ln), tag))

# locate the three boxes: rows starting with ╔
box_starts = [i for i, l in enumerate(caps) if strip(l).lstrip().startswith("\u2554")]
res.append("box top-row indices = %s" % box_starts)
# check blank print between box1 block and box2 block
res.append("blank line(s) present after box1 = %s"
           % any(caps[i] == "__BLANK__" for i in range(
               box_starts[0], box_starts[1] + 1) if i < len(caps)))
# verify each box's rows are width-uniform
for bi, start in enumerate(box_starts):
    rows = []
    for i in range(start, len(caps)):
        s = strip(caps[i])
        if s.lstrip().startswith(("\u2554", "\u2551", "\u255a")) or \
           s.lstrip().startswith(("\U0001d4f8", "\U0001d4f3", "\u263e")):
            rows.append(caps[i])
        else:
            break
    w = sorted({A._plain(r) for r in rows})
    res.append("box%d rows=%d widths=%s" % (bi + 1, len(rows), w))

# ---- confirm all input() prompts use the gradient box ----
cap = {}
A._b.input = lambda p="": cap.setdefault("p", p) or "x"
A._ask("SELECT METHOD (name or number)", "GET")
p = cap["p"]
res.append("[prompt] _ask prompt has black-on-gradient box = %s"
           % ("38;5;0;48;5;" in p and p.endswith("\x1b[0m")))
res.append("   sample = %r" % p[:90])

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(res))
