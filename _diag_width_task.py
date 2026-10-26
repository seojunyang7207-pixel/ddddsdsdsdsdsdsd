# -*- coding: utf-8 -*-
# Task-owned temporary diagnostic (delete after use)
import os, sys, unicodedata, ctypes, locale, io

samples = {
    "U+2605 BLACK STAR": "\u2605",
    "U+263E MOON": "\u263e",
    "U+207A sup plus": "\u207a",
    "U+208A sub plus": "\u208a",
    "R math bold script": "\U0001d4e1",
    "u math bold script": "\U0001d4fe",
    "2 ascii": "2",
    "box H": "\u2550",
    "box V": "\u2551",
}
lines = []
lines.append("preferred encoding = %s" % locale.getpreferredencoding(False))
lines.append("stdout isatty = %s" % (sys.stdout.isatty(),))
for name, ch in samples.items():
    lines.append("%-22s ord=%#x eaw=%s isprintable=%s" % (
        name, ord(ch), unicodedata.east_asian_width(ch), ch.isprintable()))

# --- try to measure true rendered width on the real console ---
measured = None
try:
    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    class SMALL_RECT(ctypes.Structure):
        _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                    ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]
    class CSBI(ctypes.Structure):
        _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                    ("wAttributes", ctypes.c_ushort), ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", COORD)]
    k32 = ctypes.windll.kernel32
    k32.GetStdHandle.argtypes = [ctypes.c_ulong]
    k32.GetStdHandle.restype = ctypes.c_void_p
    k32.GetConsoleScreenBufferInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(CSBI)]
    k32.GetConsoleScreenBufferInfo.restype = ctypes.c_int
    k32.SetConsoleCursorPosition.argtypes = [ctypes.c_void_p, COORD]
    k32.SetConsoleCursorPosition.restype = ctypes.c_int
    h = k32.GetStdHandle(-11)
    lines.append("stdout handle = %r" % (h,))
    csbi = CSBI()
    ok = k32.GetConsoleScreenBufferInfo(h, ctypes.byref(csbi))
    lines.append("GetConsoleScreenBufferInfo ok = %s" % bool(ok))
    if ok:
        lines.append("buffer size = %sx%s window = (%s,%s)-(%s,%s) cursor=(%s,%s)" % (
            csbi.dwSize.X, csbi.dwSize.Y,
            csbi.srWindow.Left, csbi.srWindow.Top, csbi.srWindow.Right, csbi.srWindow.Bottom,
            csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y))
except Exception as exc:
    lines.append("console measure error: %r" % (exc,))

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diag_out.txt"),
          "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
