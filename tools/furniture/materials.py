"""Procedural 32x32 tiles for Galaxy Home furniture.  MATERIALS maps name -> (painter(x, y) -> colour|None,
render_method).  Painters are deterministic (hash-based), so the PNGs are reproducible."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "creatures"))
from lib import rgb, shade, hash01
import lib as _lib


def mix(a, b, t):
    return _lib.mix(a, b, max(0.0, min(1.0, t)))

T = 32


def flat(c, n=0.06, seed=1):
    return lambda x, y: shade(c, 1 + (hash01(x, y, seed) - .5) * 2 * n)


def grain(c, n=0.09, seed=2, plank=8):
    def f(x, y):
        k = 1 + (hash01(y, seed) - .5) * n * 2 + (hash01(x // 5, y, seed) - .5) * n
        if y % plank == 0: k *= 0.78
        if (x + (y // plank) * 11) % 32 == 0: k *= 0.85
        return shade(c, k)
    return f


def weave(c, n=0.05, seed=3):
    return lambda x, y: shade(c, (1.06 if (x + y) % 2 else 0.95) + (hash01(x, y, seed) - .5) * n)


def tiles(c, g, size=8, seed=4):
    def f(x, y):
        if x % size == 0 or y % size == 0: return g
        return shade(c, 1 + (hash01(x // size, y // size, seed) - .5) * .06 + (hash01(x, y, seed) - .5) * .03)
    return f


def metal(c, seed=5):
    return lambda x, y: shade(c, 1 + (hash01(x // 16, y, seed) - .5) * .1 + (0.05 if x % 8 == 0 else 0))


def brick(seed=6):
    def f(x, y):
        row = y // 4
        if y % 4 == 0 or (x + (row % 2) * 8) % 16 == 0: return "#8a8580"
        return shade("#a8523c", .88 + hash01((x + (row % 2) * 8) // 16, row, seed) * .3)
    return f


def marble():
    def f(x, y):
        v = math.sin((x * .45 + y * .27) + 3 * hash01(x // 6, y // 6, 7)) * .5 + .5
        c = mix("#f1f1f3", "#a9adb5", 1 if v > .93 else 0)
        return shade(c, 1 + (hash01(x, y, 8) - .5) * .04)
    return f


def granite():
    def f(x, y):
        h = hash01(x, y, 9)
        if h > .86: return "#7a7d86"
        if h < .12: return "#15161a"
        return "#2a2b30"
    return f


def glass():
    def f(x, y):
        edge = x in (0, T - 1) or y in (0, T - 1)
        a = 170 if edge else 60
        if (x - y) % 16 in (0, 1) and not edge: a = 110
        return (200, 232, 245, a)
    return f


def water():
    return lambda x, y: (60, 140, 205, 170 + int(30 * hash01(x // 3, y // 3, 10)))


def leaves(dots=None):
    def f(x, y):
        if hash01(x // 2, y // 2, 11) < .28: return None
        if dots and hash01(x, y, 12) > .93: return dots
        return shade("#3f8a3c", .7 + hash01(x, y, 13) * .55)
    return f


def mirror():
    def f(x, y):
        c = mix("#cfe3ee", "#8fb0c6", (x + y) / 64)
        if (x + y) % 22 < 2: c = "#f4fbff"
        return c
    return f


def books():
    cols = ["#a33a3a", "#3a5fa3", "#3f8a55", "#d0a53a", "#6a3f8a", "#c8c2b0", "#8a5a2a", "#2f6f7a"]
    # precompute spine boundaries so the painter is O(1)
    spines, x, i = [], 0, 0
    while x < T:
        w = 2 + int(hash01(i, 14) * 3)
        spines.append((x, x + w, 3 + int(hash01(i, 15) * 8), cols[int(hash01(i, 16) * len(cols))]))
        x += w; i += 1
    def f(px, py):
        if py >= 29: return "#3a2414"
        for (a, b, top, c) in spines:
            if a <= px < b:
                if py < top: return "#2a1a0e"
                if px == a: c = shade(c, .7)
                if py in (top + 3, top + 4, 24): c = mix(c, "#e8d8a0", .5)
                return shade(c, 1 + (hash01(px, py, 17) - .5) * .06)
        return "#2a1a0e"
    return f


def screen_on():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#101014"
        if y > 18 + 4 * math.sin(x / 5): return mix("#2c7a3c", "#14421f", (y - 18) / 14)
        if (x - 24) ** 2 + (y - 8) ** 2 < 14: return "#fff1a0"
        return mix("#2f6fd0", "#9fd7ff", y / 20)
    return f


def screen_off():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#0b0b0e"
        return "#16171d" if (x + y) % 19 > 3 else "#262833"
    return f


def painting():
    def f(x, y):
        if x < 2 or y < 2 or x > 29 or y > 29: return "#b58a3a" if (x + y) % 5 else "#8a6520"
        if (x - 22) ** 2 + (y - 9) ** 2 < 16: return "#ffe27a"
        h = 16 + 5 * math.sin(x / 4.0) + 3 * math.sin(x / 9.0)
        if y > h: return mix("#3b7a3a", "#1e4a22", (y - 16) / 14) if y > h + 5 else "#4c8f45"
        return mix("#f2b68a", "#7fb4e8", y / 16)
    return f


def cab_door(base="#f3f1ea"):
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return shade(base, .78)
        if x == 16: return shade(base, .78)
        if x in (14, 18) and 3 < y < 13: return "#b8bcc2" if x == 14 else "#7d8288"
        if x in (2, 13, 19, 29) or y in (2, 29):
            if 2 <= x <= 29 and 2 <= y <= 29: return shade(base, .9)
        return shade(base, 1.0 + (hash01(x, y, 58) - .5) * .02)
    return f


def drawers(base, n, knob="#d1a94a"):
    h = T // n
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return shade(base, .7)
        if y % h in (0, h - 1): return shade(base, .62)
        if y % h == 1 or x in (1, T - 2): return shade(base, 1.12)
        if 13 <= x <= 18 and (y % h) in (h // 2 - 1, h // 2, h // 2 + 1): return knob
        return shade(base, 1 + (hash01(x // 7, y, 19) - .5) * .07)
    return f


def wardrobe(base):
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return shade(base, .7)
        if x in (15, 16): return shade(base, .55)
        if x in (1, 14, 17, 30) or y in (1, 30): return shade(base, 1.12)
        if x in (12, 19) and 12 <= y <= 20: return "#d1a94a"
        return shade(base, 1 + (hash01(x // 9, y, 20) - .5) * .08)
    return f


def fridge():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#b9bec4"
        if y in (10, 11): return "#8f959b"
        if 25 <= x <= 27 and (3 <= y <= 8 or 15 <= y <= 27): return "#4d5259"
        return shade("#eceff2", 1 + (hash01(x, y, 21) - .5) * .02)
    return f


def oven():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#7c8188"
        if 3 <= x <= 28 and y in (4, 5): return "#e2e5e8"
        if 5 <= x <= 26 and 10 <= y <= 26:
            return mix("#15161a", "#3a3d46", ((x + y) % 12) / 24) if (x + y) % 9 else "#5d6270"
        return shade("#aeb3b9", 1 + (hash01(x // 8, y, 22) - .5) * .06)
    return f


def stove_top():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#4a4d55"
        for cx, cy in ((8, 8), (24, 8), (8, 24), (24, 24)):
            d = math.hypot(x - cx, y - cy)
            if d < 3: return "#0a0a0c"
            if 5 < d < 6.5 or 7.5 < d < 8.5: return "#54575f"
        return shade("#1b1c20", 1 + (hash01(x, y, 23) - .5) * .1)
    return f


def round_front(body, trim, glass_c, seed=24):
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return shade(body, .8)
        if y < 7:
            if y == 6: return shade(body, .8)
            if (x in (5, 6, 7) or x in (24, 25, 26)) and 2 <= y <= 4: return "#5a5f68"
            if 11 <= x <= 14 and 2 <= y <= 3: return "#4f90d8"
            return trim
        d = math.hypot(x - 15.5, y - 18.5)
        if d < 3: return "#8fb8d8"
        if d < 9: return mix("#0f1218", glass_c, max(0, 1 - d / 9) * .6)
        if d < 10.5: return "#c9ced4"
        return shade(body, 1 + (hash01(x, y, seed) - .5) * .02)
    return f


def microwave():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#7c8188"
        if x == 21: return "#5d6270"
        if 3 <= x <= 20 and 4 <= y <= 27: return "#1d1f26" if (x + y) % 11 else "#4a4f5c"
        if 24 <= x <= 28 and 4 <= y <= 8: return "#37d17a"
        if 24 <= x <= 28 and y >= 10 and y % 4 == 0: return "#2c2f36"
        return shade("#b7bcc2", 1 + (hash01(x, y, 25) - .5) * .06)
    return f


def filing():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#6c727a"
        if y in (15, 16): return "#4d5259"
        yy = y % 16
        if 10 <= x <= 21 and 3 <= yy <= 6: return "#eee7c6"
        if 8 <= x <= 23 and 9 <= yy <= 11: return "#d8dce0"
        return shade("#9aa1a9", 1 + (hash01(x // 8, y, 26) - .5) * .06)
    return f


def fire():
    def f(x, y):
        top = 8 + int(hash01(x // 2, 5, 27) * 12) + int(4 * math.sin(x / 3.0))
        if y < top: return None
        t = (y - top) / max(1, 31 - top)
        return mix("#ffe97a", "#e2581f", t / .55) if t < .55 else mix("#e2581f", "#8d1b0c", (t - .55) / .45)
    return f


def embers():
    def f(x, y):
        h = hash01(x, y, 28)
        if h > .82: return "#ff9a2a"
        if h > .6: return "#b23a12"
        return shade("#26221f", .8 + h * .5)
    return f


def rug(a, b, c):
    def f(x, y):
        m = min(x, y, T - 1 - x, T - 1 - y)
        if m < 2: return b
        if m < 4: return a if m == 3 else c
        dd = abs(x - 15.5) + abs(y - 15.5)
        if dd < 9: return b if dd > 6 else c
        return shade(a, 1 + (hash01(x, y, 29) - .5) * .08) if (x + y) % 2 else shade(a, .93)
    return f


def play_mat():
    cols = ["#e8484a", "#4a8fe8", "#f0c93a", "#4ec26a"]
    def f(x, y):
        c = cols[((x // 8) + (y // 8)) % 4]
        if x % 8 in (0, 7) or y % 8 in (0, 7): c = shade(c, .82)
        if abs(x - (4 + (x // 8) * 8)) + abs(y - (4 + (y // 8) * 8)) < 2: c = "#ffffff"
        return c
    return f


def wicker():
    def f(x, y):
        k = 1.12 if ((x // 3) + (y // 3)) % 2 == 0 else .9
        if x % 3 == 0 or y % 3 == 0: k *= .82
        return shade("#c9a25c", k)
    return f


def terracotta():
    def f(x, y):
        if y % 16 == 15: return "#8a4526"
        return shade("#b8623c", (1.12 if y % 16 < 3 else 1) + (hash01(x, y, 32) - .5) * .12)
    return f


def quilt(a, b):
    return lambda x, y: (shade(a, .75) if (x % 8 == 0 or y % 8 == 0) else
                         shade(mix(a, b, .35 * ((x // 8 + y // 8) % 2)), 1 + (hash01(x, y, 33) - .5) * .04))


def stripe(a, b, w=4):
    return lambda x, y: shade(a if (y // w) % 2 == 0 else b, 1 + (hash01(x, y, 34) - .5) * .05)


def _rainbow(t):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(t % 1.0, 0.85, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255), 255)


def pc_front():
    """Black mesh front panel with three glowing RGB fan rings."""
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#0a0b0d"
        for cy in (6, 16, 26):
            d = math.hypot(x - 15.5, y - cy)
            if 4.4 < d < 5.6: return _rainbow(math.atan2(y - cy, x - 15.5) / 6.283 + cy / 40)
            if d <= 4.4:
                if d < 1.5: return "#1a1c20"
                return "#15171b" if (int(math.atan2(y - cy, x - 15.5) * 2.5) % 2) else "#22252a"
        return "#101115" if (x + y) % 3 else "#191b20"
    return f


def pc_side():
    """Tempered-glass side panel: see-through with a lit motherboard, GPU and RGB strip visible inside."""
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return (20, 22, 26, 255)
        if 4 <= y <= 9 and 3 <= x <= 28:                       # graphics card
            if y == 9: return _rainbow(x / 26.0)
            return (28, 30, 36, 255) if (x % 9) > 1 else (60, 64, 72, 255)
        if 14 <= y <= 24 and 6 <= x <= 12: return (44, 48, 56, 255)      # cooler block
        if 3 <= x <= 5 and 12 <= y <= 28: return _rainbow(y / 20.0)      # RAM strip
        if (x - y) % 16 in (0, 1): return (150, 200, 220, 60)
        return (20, 30, 40, 70)
    return f


def rgb_strip():
    return lambda x, y: _rainbow((x + y) / 32.0)


def gaming_screen():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#08080b"
        base = mix("#1a0b3a", "#0a2a52", y / 32.0)
        if y > 22:                                         # neon grid floor
            if y % 4 == 0 or (x + (y - 22) * (x - 16) // 6) % 8 == 0: return "#ff3df0"
            return mix("#12082a", "#3a0a5a", (y - 22) / 10)
        if (x - 16) ** 2 + (y - 12) ** 2 < 36: return mix("#ffd23d", "#ff4d7a", (y - 6) / 12)   # sun
        return base
    return f


def keyboard():
    def f(x, y):
        if x in (0, T - 1) or y in (0, T - 1): return "#0c0d10"
        if x % 4 in (1, 2) and y % 4 in (1, 2): return _rainbow((x + y) / 40.0)
        return "#15171b"
    return f


MATERIALS = {
    "oak": (grain("#b8945a"), "opaque"),
    "dark_wood": (grain("#5a3b22", seed=40), "opaque"),
    "walnut": (grain("#7a4a2c", seed=41), "opaque"),
    "birch": (grain("#dcc994", seed=42), "opaque"),
    "white_wood": (grain("#efece4", n=.04, seed=43), "opaque"),
    "fab_gray": (weave("#7d8794"), "opaque"),
    "fab_blue": (weave("#3f6fa8"), "opaque"),
    "fab_navy": (weave("#26355e"), "opaque"),
    "fab_red": (weave("#a83a3a"), "opaque"),
    "fab_green": (weave("#4e8a5a"), "opaque"),
    "fab_cream": (weave("#e6dcc4"), "opaque"),
    "fab_pink": (weave("#e59ab8"), "opaque"),
    "fab_yellow": (weave("#e8c545"), "opaque"),
    "fab_purple": (weave("#7a5aa8"), "opaque"),
    "fab_white": (weave("#f3f3f1", .03), "opaque"),
    "fab_brown": (weave("#b98a55", .09), "opaque"),
    "fab_black": (weave("#26272b"), "opaque"),
    "leather": (flat("#7a4a2a", .07, 44), "opaque"),
    "marble": (marble(), "opaque"),
    "granite": (granite(), "opaque"),
    "brick": (brick(), "opaque"),
    "stone": (flat("#8b8d92", .1, 45), "opaque"),
    "bathtile": (tiles("#dff0f5", "#a9c9d3"), "opaque"),
    "steel": (metal("#c4c9cf"), "opaque"),
    "iron": (metal("#3a3d43", 46), "opaque"),
    "chrome": (metal("#eef2f6", 47), "opaque"),
    "brass": (metal("#c9a24a", 48), "opaque"),
    "porcelain": (flat("#f6f8fa", .015, 49), "opaque"),
    "glass": (glass(), "blend"),
    "water": (water(), "blend"),
    "mirror": (mirror(), "opaque"),
    "books": (books(), "opaque"),
    "screen_on": (screen_on(), "opaque"),
    "screen_off": (screen_off(), "opaque"),
    "painting": (painting(), "opaque"),
    "cab_door": (cab_door(), "opaque"),
    "cab_door_dark": (cab_door("#4e5a68"), "opaque"),
    "drawers2": (drawers("#7a4a2c", 2), "opaque"),
    "drawers3": (drawers("#7a4a2c", 3), "opaque"),
    "drawers3_white": (drawers("#efece4", 3, "#b8bcc2"), "opaque"),
    "wardrobe_front": (wardrobe("#7a4a2c"), "opaque"),
    "fridge_front": (fridge(), "opaque"),
    "oven_front": (oven(), "opaque"),
    "stove_top": (stove_top(), "opaque"),
    "micro_front": (microwave(), "opaque"),
    "filing_front": (filing(), "opaque"),
    "washer_front": (round_front("#f1f3f5", "#dfe3e8", "#3f7fb0"), "opaque"),
    "dryer_front": (round_front("#e9ecef", "#cfd4da", "#b06f3f", seed=50), "opaque"),
    "fire": (fire(), "alpha_test"),
    "embers": (embers(), "opaque"),
    "rug_red": (rug("#a3323a", "#e8d9a8", "#5a1a22"), "opaque"),
    "rug_blue": (rug("#2f5a94", "#e8e2cf", "#1b2f55"), "opaque"),
    "play_mat": (play_mat(), "opaque"),
    "wicker": (wicker(), "opaque"),
    "awning": (lambda x, y: shade("#d84a4a" if (x // 4) % 2 == 0 else "#f4f0e6", 1 + (hash01(x, y, 30) - .5) * .05), "opaque"),
    "soil": (lambda x, y: shade("#4a3524", .7 + hash01(x, y, 31) * .6), "opaque"),
    "terracotta": (terracotta(), "opaque"),
    "leaves": (leaves(), "alpha_test"),
    "flowers_red": (leaves("#e23a4a"), "alpha_test"),
    "flowers_yellow": (leaves("#f2d23a"), "alpha_test"),
    "quilt_blue": (quilt("#3f6fa8", "#7fa6d4"), "opaque"),
    "quilt_rose": (quilt("#b8506a", "#e69ab0"), "opaque"),
    "towel_stripe": (stripe("#4a8fb8", "#f3f3f1"), "opaque"),
    "lampshade": (lambda x, y: shade("#ffe7a8", 1 + (hash01(x, y, 35) - .5) * .06 + (.08 if y % 8 == 0 else 0)), "opaque"),
    "bulb": (lambda x, y: "#fff6c8" if (x + y) % 5 else "#ffe27a", "opaque"),
    "paint_red": (flat("#d84040", .03, 51), "opaque"),
    "paint_blue": (flat("#3f7fe0", .03, 52), "opaque"),
    "paint_yellow": (flat("#f0c93a", .03, 53), "opaque"),
    "paint_green": (flat("#4ec26a", .03, 54), "opaque"),
    "charcoal": (flat("#2b2a2a", .12, 55), "opaque"),
    "mail_blue": (metal("#3f6fc0", 56), "opaque"),
    "concrete": (flat("#a9a9a6", .07, 57), "opaque"),
    "pc_front": (pc_front(), "opaque"),
    "pc_side": (pc_side(), "blend"),
    "rgb_strip": (rgb_strip(), "opaque"),
    "gaming_screen": (gaming_screen(), "opaque"),
    "keyboard": (keyboard(), "opaque"),
    "mousepad": (flat("#14161c", .05, 58), "opaque"),
}
