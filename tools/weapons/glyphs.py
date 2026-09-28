"""Generate the private-use glyph sheet used for scopes, reticles and HUD readouts.

Bedrock loads `font/glyph_<page>.png` directly for its code page (no JSON provider needed).
Page **E2** is chosen because vanilla leaves E2..F8 free, so overwriting it cannot clobber
a vanilla emoji cell (the engine prompt's "glyph_E1.png etc.").

Sheet is 256x256 = 16x16 cells of 16x16 px.  Cell index i -> codepoint 0xE200 + i,
row = i // 16, col = i % 16.  `CHARS` maps a glyph name to the character to paste into a
title/subtitle/actionbar string.
"""
import lib
from lib import RP, write_png

PAGE = 0xE200
SHEET = 256
CELL = 16
GRID = 16

# ------------------------------------------------------------------ primitives
def _buf():
    return [[(0, 0, 0, 0)] * CELL for _ in range(CELL)]


def _px(b, x, y, c):
    if 0 <= x < CELL and 0 <= y < CELL:
        b[int(y)][int(x)] = lib.rgb(c)


def _rect(b, x0, y0, x1, y1, c):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            _px(b, x, y, c)


def _disc(b, cx, cy, r, c):
    for y in range(CELL):
        for x in range(CELL):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                _px(b, x, y, c)


def _ring(b, cx, cy, r, thick, c):
    for y in range(CELL):
        for x in range(CELL):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if abs(d - r) <= thick:
                _px(b, x, y, c)


def _line(b, x0, y0, x1, y1, w, c):
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        _disc(b, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w, c)


WHITE = "#ffffff"
CYAN = "#7fe8ff"
GREEN = "#7cff9a"
RED = "#ff5a4a"
GOLD = "#ffd45a"
VIOLET = "#c08aff"
ICE = "#bfe6ff"
DARK = "#000000cc"


# ------------------------------------------------------------------ glyphs
def g_spacer(b):
    pass


def g_pip_full(b):
    _rect(b, 3, 6, 12, 9, WHITE)


def g_pip_empty(b):
    _rect(b, 3, 6, 12, 9, "#ffffff40")


def g_bar_full(b):
    _rect(b, 0, 6, 15, 9, WHITE)


def g_bar_mid(b):
    _rect(b, 0, 6, 15, 9, "#ffffffcc")


def g_bar_low(b):
    _rect(b, 0, 6, 15, 9, "#ff8a4acc")


def g_bar_empty(b):
    _rect(b, 0, 6, 15, 9, "#ffffff30")


def g_slider_mark(b):
    _rect(b, 7, 4, 8, 11, WHITE)


def g_cell(b):
    _rect(b, 4, 2, 11, 13, "#8fe0ff")
    _rect(b, 6, 4, 9, 11, "#eaffff")


def g_heat_cool(b):
    _rect(b, 5, 10, 10, 13, "#6fe0ff")


def g_heat_warm(b):
    _rect(b, 5, 6, 10, 13, "#ffd45a")


def g_heat_hot(b):
    _rect(b, 5, 2, 10, 13, "#ff5a4a")


def g_charge0(b):
    _rect(b, 1, 7, 3, 8, "#ffffff55")


def g_charge1(b):
    _rect(b, 1, 6, 5, 9, WHITE)


def g_charge2(b):
    _rect(b, 1, 6, 8, 9, WHITE)


def g_charge3(b):
    _rect(b, 1, 6, 11, 9, WHITE)


def g_charge4(b):
    _rect(b, 1, 6, 14, 9, WHITE)


def g_scope_corner_tl(b):
    _rect(b, 0, 0, 15, 1, DARK)
    _rect(b, 0, 0, 1, 15, DARK)
    _ring(b, 15, 15, 14, 1, "#00000099")


def g_scope_corner_tr(b):
    _rect(b, 0, 0, 15, 1, DARK)
    _rect(b, 14, 0, 15, 15, DARK)
    _ring(b, 0, 15, 14, 1, "#00000099")


def g_scope_corner_bl(b):
    _rect(b, 0, 14, 15, 15, DARK)
    _rect(b, 0, 0, 1, 15, DARK)
    _ring(b, 15, 0, 14, 1, "#00000099")


def g_scope_corner_br(b):
    _rect(b, 0, 14, 15, 15, DARK)
    _rect(b, 14, 0, 15, 15, DARK)
    _ring(b, 0, 0, 14, 1, "#00000099")


def g_scope_edge_top(b):
    _rect(b, 0, 0, 15, 1, DARK)


def g_scope_edge_bottom(b):
    _rect(b, 0, 14, 15, 15, DARK)


def g_scope_edge_left(b):
    _rect(b, 0, 0, 1, 15, DARK)


def g_scope_edge_right(b):
    _rect(b, 14, 0, 15, 15, DARK)


def g_scope_ring_big(b):
    _ring(b, 7.5, 7.5, 7, 0.6, WHITE)


def g_scope_ring_med(b):
    _ring(b, 7.5, 7.5, 5, 0.6, WHITE)


def g_scope_ring_small(b):
    _ring(b, 7.5, 7.5, 3, 0.6, WHITE)


def g_scope_tick(b):
    _line(b, 7.5, 0, 7.5, 3, 0.4, WHITE)


def g_scope_mildot(b):
    _line(b, 7.5, 7.5, 7.5, 14, 0.4, WHITE)
    _disc(b, 7.5, 12, 0.8, WHITE)


def g_scope_center(b):
    _disc(b, 7.5, 7.5, 0.9, RED)


def g_scope_lock(b):
    _line(b, 0, 0, 4, 0, 0.5, RED)
    _line(b, 0, 0, 0, 4, 0.5, RED)
    _line(b, 15, 15, 11, 15, 0.5, RED)
    _line(b, 15, 15, 15, 11, 0.5, RED)


def g_scope_rangefinder(b):
    _rect(b, 0, 6, 2, 9, "#ffffffaa")
    _rect(b, 13, 6, 15, 9, "#ffffffaa")


def g_hourglass(b):
    _line(b, 3, 2, 12, 2, 0.6, WHITE)
    _line(b, 3, 13, 12, 13, 0.6, WHITE)
    _line(b, 4, 3, 11, 12, 0.6, WHITE)
    _line(b, 11, 3, 4, 12, 0.6, WHITE)


def g_crosshair_dot(b):
    _disc(b, 7.5, 7.5, 1.2, WHITE)


def g_crosshair_cross(b):
    _line(b, 7.5, 2, 7.5, 13, 0.5, WHITE)
    _line(b, 2, 7.5, 13, 7.5, 0.5, WHITE)


def g_crosshair_ring(b):
    _ring(b, 7.5, 7.5, 5, 0.6, WHITE)
    _disc(b, 7.5, 7.5, 0.8, WHITE)


def g_crosshair_brackets(b):
    _line(b, 2, 2, 5, 2, 0.5, WHITE)
    _line(b, 2, 2, 2, 5, 0.5, WHITE)
    _line(b, 13, 2, 10, 2, 0.5, WHITE)
    _line(b, 13, 2, 13, 5, 0.5, WHITE)
    _line(b, 2, 13, 5, 13, 0.5, WHITE)
    _line(b, 2, 13, 2, 10, 0.5, WHITE)
    _line(b, 13, 13, 10, 13, 0.5, WHITE)
    _line(b, 13, 13, 13, 10, 0.5, WHITE)


def g_marker_hit(b):
    _line(b, 3, 3, 12, 12, 0.7, WHITE)
    _line(b, 12, 3, 3, 12, 0.7, WHITE)


def g_marker_kill(b):
    _line(b, 3, 8, 6, 12, 0.8, GOLD)
    _line(b, 6, 12, 13, 3, 0.8, GOLD)


def g_marker_heart(b):
    _disc(b, 5, 6, 2.6, "#ff7ab0")
    _disc(b, 10, 6, 2.6, "#ff7ab0")
    _line(b, 2, 7, 13, 7, 2.4, "#ff7ab0")
    _line(b, 2, 8, 13, 8, 2.2, "#ff7ab0")
    _disc(b, 7.5, 9, 3.4, "#ff7ab0")
    _line(b, 3, 10, 12, 10, 1.6, "#ff7ab0")


def g_marker_bone(b):
    _line(b, 4, 5, 11, 11, 1.6, WHITE)
    _disc(b, 3.5, 4.5, 2, WHITE)
    _disc(b, 11.5, 11.5, 2, WHITE)


def g_marker_paw(b):
    _disc(b, 7.5, 10, 3, "#ffd7ea")
    for dx, dy in ((-4, -3), (-1.4, -5), (1.4, -5), (4, -3)):
        _disc(b, 7.5 + dx, 10 + dy, 1.4, "#ffd7ea")


def g_vignette_frost(b):
    _rect(b, 0, 0, 15, 15, "#bfe6ff22")
    _line(b, 1, 14, 4, 11, 0.5, "#bfe6ff88")


def g_vignette_whiteout(b):
    _rect(b, 0, 0, 15, 15, "#ffffffdd")


def g_vignette_heat(b):
    _rect(b, 0, 0, 15, 15, "#ff4a0022")
    _line(b, 0, 15, 15, 0, 0.5, "#ff8a4a55")


def g_vignette_void(b):
    _rect(b, 0, 0, 15, 15, "#120020cc")


def g_vignette_toxic(b):
    _rect(b, 0, 0, 15, 15, "#7cff3a1e")


def g_thermal_tint(b):
    _rect(b, 0, 0, 15, 15, "#2a5aff22")


def g_arrow_down(b):
    _line(b, 7.5, 3, 7.5, 12, 0.6, GOLD)
    _line(b, 4, 9, 7.5, 13, 0.6, GOLD)
    _line(b, 11, 9, 7.5, 13, 0.6, GOLD)


def g_dot_small(b):
    _disc(b, 7.5, 7.5, 0.8, WHITE)


def g_dot_med(b):
    _disc(b, 7.5, 7.5, 1.6, WHITE)


def g_hex(b):
    import math
    pts = [(7.5 + 6 * math.cos(math.radians(60 * i)), 7.5 + 6 * math.sin(math.radians(60 * i))) for i in range(6)]
    for i in range(6):
        _line(b, pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1], 0.6, WHITE)


def g_ring_big(b):
    _ring(b, 7.5, 7.5, 6, 1.0, WHITE)


def g_ring_med(b):
    _ring(b, 7.5, 7.5, 4, 1.0, WHITE)


def g_ring_small(b):
    _ring(b, 7.5, 7.5, 2, 1.0, WHITE)


def g_star(b):
    _line(b, 7.5, 1, 7.5, 14, 0.6, WHITE)
    _line(b, 1, 7.5, 14, 7.5, 0.6, WHITE)
    _line(b, 3, 3, 12, 12, 0.4, WHITE)
    _line(b, 12, 3, 3, 12, 0.4, WHITE)


def g_shield(b):
    _line(b, 3, 2, 12, 2, 0.6, CYAN)
    _line(b, 3, 2, 3, 9, 0.6, CYAN)
    _line(b, 12, 2, 12, 9, 0.6, CYAN)
    _line(b, 3, 9, 7.5, 14, 0.6, CYAN)
    _line(b, 12, 9, 7.5, 14, 0.6, CYAN)


def g_battery(b):
    _rect(b, 2, 4, 12, 12, "#ffffff44")
    _rect(b, 2, 9, 7, 12, CYAN)
    _rect(b, 5, 2, 9, 4, CYAN)


def g_fuel(b):
    _rect(b, 2, 3, 7, 13, "#ff8a4acc")
    _rect(b, 2, 8, 7, 13, "#ffd45a")
    _rect(b, 9, 4, 12, 13, "#ffffff44")


def g_vent(b):
    for i in range(4):
        _rect(b, 2 + i * 3, 4, 3 + i * 3, 12, "#8fe0ff")


GLYPHS = [
    ("spacer", g_spacer), ("pip_full", g_pip_full), ("pip_empty", g_pip_empty),
    ("bar_full", g_bar_full), ("bar_mid", g_bar_mid), ("bar_low", g_bar_low),
    ("bar_empty", g_bar_empty), ("slider_mark", g_slider_mark), ("cell", g_cell),
    ("heat_cool", g_heat_cool), ("heat_warm", g_heat_warm), ("heat_hot", g_heat_hot),
    ("charge0", g_charge0), ("charge1", g_charge1), ("charge2", g_charge2),
    ("charge3", g_charge3), ("charge4", g_charge4),
    ("scope_corner_tl", g_scope_corner_tl), ("scope_corner_tr", g_scope_corner_tr),
    ("scope_corner_bl", g_scope_corner_bl), ("scope_corner_br", g_scope_corner_br),
    ("scope_edge_top", g_scope_edge_top), ("scope_edge_bottom", g_scope_edge_bottom),
    ("scope_edge_left", g_scope_edge_left), ("scope_edge_right", g_scope_edge_right),
    ("scope_ring_big", g_scope_ring_big), ("scope_ring_med", g_scope_ring_med),
    ("scope_ring_small", g_scope_ring_small), ("scope_tick", g_scope_tick),
    ("scope_mildot", g_scope_mildot), ("scope_center", g_scope_center),
    ("scope_lock", g_scope_lock), ("scope_rangefinder", g_scope_rangefinder),
    ("hourglass", g_hourglass),
    ("crosshair_dot", g_crosshair_dot), ("crosshair_cross", g_crosshair_cross),
    ("crosshair_ring", g_crosshair_ring), ("crosshair_brackets", g_crosshair_brackets),
    ("marker_hit", g_marker_hit), ("marker_kill", g_marker_kill),
    ("marker_heart", g_marker_heart), ("marker_bone", g_marker_bone), ("marker_paw", g_marker_paw),
    ("vignette_frost", g_vignette_frost), ("vignette_whiteout", g_vignette_whiteout),
    ("vignette_heat", g_vignette_heat), ("vignette_void", g_vignette_void),
    ("vignette_toxic", g_vignette_toxic), ("thermal_tint", g_thermal_tint),
    ("arrow_down", g_arrow_down), ("dot_small", g_dot_small), ("dot_med", g_dot_med),
    ("hex", g_hex), ("ring_big", g_ring_big), ("ring_med", g_ring_med), ("ring_small", g_ring_small),
    ("star", g_star), ("shield", g_shield), ("battery", g_battery), ("fuel", g_fuel), ("vent", g_vent),
]

CHARS = {}


def write_font():
    """Write font/glyph_E2.png and return {name: character}."""
    px = [(0, 0, 0, 0)] * (SHEET * SHEET)
    for i, (name, fn) in enumerate(GLYPHS):
        b = _buf()
        fn(b)
        ox, oy = (i % GRID) * CELL, (i // GRID) * CELL
        for y in range(CELL):
            for x in range(CELL):
                px[(oy + y) * SHEET + ox + x] = b[y][x]
        CHARS[name] = chr(PAGE + i)
    write_png(RP / "font/glyph_E2.png", px, SHEET, SHEET)
    return CHARS
