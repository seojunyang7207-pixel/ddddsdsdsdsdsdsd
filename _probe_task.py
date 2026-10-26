# -*- coding: utf-8 -*-
# Task-owned temporary probe: measure real console cell width of glyphs.
import ctypes, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_probe_out.txt")
res = []


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
allocated = bool(k32.AllocConsole())

k32.GetStdHandle.argtypes = [ctypes.c_ulong]
k32.GetStdHandle.restype = ctypes.c_void_p
k32.GetConsoleScreenBufferInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(CSBI)]
k32.GetConsoleScreenBufferInfo.restype = ctypes.c_int
k32.SetConsoleCursorPosition.argtypes = [ctypes.c_void_p, COORD]
k32.SetConsoleCursorPosition.restype = ctypes.c_int
k32.WriteConsoleW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_ulong,
                              ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p]
k32.WriteConsoleW.restype = ctypes.c_int
k32.GetConsoleFontInfo = None  # not used
h = k32.GetStdHandle(-11)

res.append("AllocConsole = %s  handle = %r" % (allocated, h))


def cursor_x():
    c = CSBI()
    if not k32.GetConsoleScreenBufferInfo(h, ctypes.byref(c)):
        return None
    return c.dwCursorPosition.X


def write(s):
    n = ctypes.c_ulong(0)
    k32.WriteConsoleW(h, s, len(s), ctypes.byref(n), None)


def measure(sample, reps):
    """Return cells-per-glyph for sample repeated reps times (None on failure)."""
    if k32.SetConsoleCursorPosition(h, COORD(0, 6)) == 0:
        return None
    x0 = cursor_x()
    if x0 is None:
        return None
    write("abcdefgh")            # 8 ascii cells to align
    x1 = cursor_x()
    write(sample * reps)
    x2 = cursor_x()
    if None in (x1, x2):
        return None
    return (x2 - x1) / float(reps), (x1 - x0)


_c = CSBI()
if k32.GetConsoleScreenBufferInfo(h, ctypes.byref(_c)):
    res.append("buffer: %sx%s" % (_c.dwSize.X, _c.dwSize.Y))
else:
    res.append("buffer: <unavailable>")
for label, sample, reps in [
    ("astral math script R", "\U0001d4e1", 4),
    ("astral math script u", "\U0001d4fe", 4),
    ("BMP black star", "\u2605", 4),
    ("BMP moon", "\u263e", 4),
    ("box double H", "\u2550", 4),
    ("box double V", "\u2551", 4),
    ("CJK han", "\u6f22", 4),
    ("ascii A", "A", 4),
]:
    res.append("%-22s cells/glyph = %s" % (label, measure(sample, reps)))

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(str(r) for r in res))
