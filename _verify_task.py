# -*- coding: utf-8 -*-
# Task-owned temporary verification: run in a real console, import the module,
# calibrate, and dump the measured glyph widths + key UI string widths.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_verify_out.txt")
sys.path.insert(0, HERE)

res = []
try:
    import ddos_art as A
    res.append("import ok")
    res.append("color = %s" % A.init())
    res.append("calibrated glyphs = %d" % len(A._GLYPH_W))
    for ch in ["\u2605", "\u263e", "\u2550", "\u2551", "\U0001d4e1", "\u211b",
               "\u207a", "\u208a", "\u6f22", "\u2019", "\u00a9"]:
        res.append("  %r measured=%s plain=%s" % (ch, A._GLYPH_W.get(ch), A._plain(ch)))

    label = "\u2605 \U0001d4f8\U0001d4f7\U0001d4f5\U0001d4fe \U0001d4ef\U0001d4f8\U0001d4fb "\
            "\U0001d4fd\U0001d4ee\U0001d4fc\U0001d4fd\U0001d4f2\U0001d4f7\U0001d4f0 \u2605"
    res.append("label width = %d" % A._plain(label))
    welcome = "Welcome to \U0001d4e1\U0001d4ea\U0001d4f2\U0001d4f7\U0001d4ec2 made by "\
              "\U0001d4e2\U0001d4ee\U0001d4f8\U0001d4f1\U0001d4fe"
    res.append("welcome width = %d" % A._plain(welcome))
    disc = "\u263e\u207a\u208a \U0001d4f3\U0001d4f8\U0001d4f2\U0001d4f7"
    res.append("discord-ish width = %d" % A._plain(disc))
    res.append("box H width = %d" % A._plain("\u2550" * 10))
    res.append("plain ASCII width = %d" % A._plain("hello world"))
except Exception as exc:
    import traceback
    res.append("ERROR: %s" % exc)
    res.append(traceback.format_exc())

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(res))
