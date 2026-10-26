# -*- coding: utf-8 -*-
# Task-owned temporary probe v2: unambiguous per-glyph console cell width.
import ctypes, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_probe2_out.txt")
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
k32.GetStdHandle.argtypes = [ctypes.c_ulong]
k32.GetStdHandle.restype = ctypes.c_void_p
k32.GetConsoleScreenBufferInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(CSBI)]
k32.GetConsoleScreenBufferInfo.restype = ctypes.c_int
k32.SetConsoleCursorPosition.argtypes = [ctypes.c_void_p, COORD]
k32.SetConsoleCursorPosition.restype = ctypes.c_int
k32.WriteConsoleW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_ulong,
                              ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p]
k32.WriteConsoleW.restype = ctypes.c_int
h = k32.GetStdHandle(-11)


def cursor_x():
    c = CSBI()
    if not k32.GetConsoleScreenBufferInfo(h, ctypes.byref(c)):
        return None
    return c.dwCursorPosition.X


def write(s):
    n = ctypes.c_ulong(0)
    units = len(s.encode("utf-16-le")) // 2     # TCHARs (UTF-16 units)
    k32.WriteConsoleW(h, s, units, ctypes.byref(n), None)
    return n.value


def measure(s):
    if k32.SetConsoleCursorPosition(h, COORD(0, 6)) == 0:
        return None
    write("abcdefgh")
    x1 = cursor_x()
    wrote = write(s)
    x2 = cursor_x()
    if x1 is None or x2 is None:
        return None
    return "%d cells for %r (units written=%s)" % (x2 - x1, s, wrote)


res.append("CSBI ok = %s" % bool(k32.GetConsoleScreenBufferInfo(h, ctypes.byref(CSBI()))))
for label, s in [
    ("astral R x1", "\U0001d4e1"),
    ("astral R x6", "\U0001d4e1" * 6),
    ("astral u x6", "\U0001d4fe" * 6),
    ("script 'Rainc2'", "\U0001d4e1\U0001d4ea\U0001d4f2\U0001d4f7\U0001d4ec2"),
    ("BMP star x6", "\u2605" * 6),
    ("BMP moon x6", "\u263e" * 6),
    ("box H x6", "\u2550" * 6),
    ("box V x6", "\u2551" * 6),
    ("CJK x6", "\u6f22" * 6),
    ("ascii x6", "A" * 6),
    ("label full", "\u2605 " + "\U0001d4f8\U0001d4f7\U0001d4f5\U0001d4fe "
                   "\U0001d4ef\U0001d4f8\U0001d4fb \U0001d4fd\U0001d4ee\U0001d4fc\U0001d4fd\U0001d4f2\U0001d4f7\U0001d4f0 \u2605"),
]:
    res.append("%-18s -> %s" % (label, measure(s)))

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(str(r) for r in res))
