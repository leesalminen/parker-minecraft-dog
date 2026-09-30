"""Shared toolkit for the toy-car add-ons (LEGO-style brick cars + die-cast cars).
Not a spec module itself (no SPEC/SPECS): imported by toycars_lego.py and toycars_diecast.py.
Units: 1/16 block. Models face -Z, ground y=0. Brick grid: studs on a 4-unit pitch, x = -8 + 4i, z = -12 + 4k."""
import math
from lib import *


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def wobble(p, seed, scale=1.0, amp=0.06):
    x, y, z = p.p
    return 1.0 + amp * (noise3(x, y, z, seed, scale) * 2 - 1)


# ============================================================================ brick-plastic painter
def lego(base, decal=None, smooth=False, seed=5):
    """Glossy moulded-plastic brick. Handles stud cubes (2x1x2), stud-ring shadows on top faces,
    bevelled edges, gloss streaks and optional position-based decals (decal(p) -> colour|None)."""
    def f(p):
        x, y, z = p.p
        c = None
        if decal is not None:
            c = decal(p)
        if c is None:
            c = base
        c = rgb(c)
        is_stud = (p.w == 2 and p.h == 1 and p.d == 2)
        k = 1.0
        if is_stud:
            if p.face == "top":
                k = (1.28, 1.10, 1.04, 0.84)[(p.y & 1) * 2 + (p.x & 1)]
                if p.x == 0 and p.y == 0:
                    return tuple(min(255, int(v * 1.28 + 30)) for v in c[:3]) + (255,)
            else:
                k = 0.86 if p.face in ("east", "back") else 0.98
        else:
            e = min(p.x, p.fw - 1 - p.x, p.y, p.fh - 1 - p.y)
            if p.face == "top":
                k = 1.06
                if not smooth and p.fw >= 3 and p.fh >= 3:
                    u = (x + 8.0) % 4.0
                    v = (z + 12.0) % 4.0
                    if u < 1.0 or u >= 3.0 or v < 1.0 or v >= 3.0:
                        k = 0.86
                        if u < 1.0 and v < 1.0 or u >= 3.0 and v >= 3.0:
                            k = 0.8
                if e == 0:
                    k *= 0.9
            elif p.face == "bottom":
                k = 0.6
            else:
                k = {"front": 0.96, "back": 0.9, "east": 0.84, "west": 1.0}[p.face]
                if p.fh >= 3:
                    if p.y == 0:
                        k *= 1.12
                    elif p.y == p.fh - 1:
                        k *= 0.82
                if e == 0 and p.fw >= 2:
                    k *= 0.9
                # soft gloss streak on the vertical faces
                if p.fh >= 4 and p.x == 1 and p.fw >= 4:
                    k *= 1.1
        k *= wobble(p, seed, 0.9, 0.05)
        return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
    return f


def brick_palette(decals=None, seed=5):
    """{colour: painter, colour+'_s': smooth painter}. decals: {colour: fn}"""
    cols = {"red": "#c9161f", "blue": "#0d5fb8", "yellow": "#f6c90e", "white": "#eef0ee", "black": "#191b1f",
            "green": "#1c9a49", "orange": "#f26a12", "grey": "#9aa0a6", "dgrey": "#4a4f57", "tan": "#d2b680",
            "teal": "#12a3a5", "lime": "#8fd12a", "purple": "#6a2fa0"}
    decals = decals or {}
    out = {}
    for i, (n, c) in enumerate(cols.items()):
        out[n] = lego(c, decals.get(n), False, seed + i)
        out[n + "_s"] = lego(c, decals.get(n), True, seed + i)
    return out


# ============================================================================ glass / chrome / lights / rubber
def glass(tint="#7fc4ff", dark="#274a72"):
    def f(p):
        x, y, z = p.p
        t = 0.35 + 0.3 * noise3(x, y, z, 17, 3.0)
        c = mix(dark, tint, t)
        s = math.sin((x + z) * 0.8 + y * 0.55)
        if s > 0.82:
            c = mix(c, "#ffffff", 0.55)
        e = min(p.x, p.fw - 1 - p.x, p.y, p.fh - 1 - p.y)
        if e == 0:
            c = shade(c, 0.75)
        return c
    return f


def chrome(horizon=6.0, tint=None):
    """Fake environment-map chrome: sky above the horizon, dark horizon line, sandy ground below, moving streaks."""
    def f(p):
        x, y, z = p.p
        h = horizon
        if y > h + 0.8:
            t = clamp((y - h) / 9.0)
            c = mix("#f1f8ff", "#3f74c2", t)
        elif y > h - 0.8:
            c = rgb("#1b2233")
        else:
            t = clamp((h - y) / 6.0)
            c = mix("#7f8b9c", "#20252d", t)
        s = math.sin((x * 0.9 + z * 0.7) + y * 0.45)
        if s > 0.86:
            c = mix(c, "#ffffff", 0.7)
        elif s < -0.9:
            c = shade(c, 0.7)
        k = {"top": 1.08, "bottom": 0.6, "front": 0.95, "back": 0.9, "east": 0.85, "west": 1.0}[p.face]
        c = shade(c, k * wobble(p, 23, 0.8, 0.05))
        if tint:
            c = mix(c, tint, 0.28)
        return c
    return f


def lamp(colour):
    def f(p):
        x, y, z = p.p
        c = mix(colour, "#ffffff", 0.25 + 0.4 * noise3(x, y, z, 29, 1.6))
        if p.face in ("east", "west", "back") and min(p.x, p.y) == 0:
            c = shade(c, 0.8)
        return glow(c)
    return f


def matte(base, seed=41, grain=0.12, panel=None):
    """Matte moulded/painted surface with grain and optional panel-line period."""
    def f(p):
        x, y, z = p.p
        c = rgb(base)
        k = 1.0 + grain * (noise3(x, y, z, seed, 1.2) * 2 - 1)
        if panel:
            if (x % panel) < 0.9 or (z % panel) < 0.9:
                k *= 0.8
        if p.face == "top":
            k *= 1.08
        elif p.face == "bottom":
            k *= 0.6
        e = min(p.x, p.fw - 1 - p.x, p.y, p.fh - 1 - p.y)
        if e == 0:
            k *= 0.85
        return shade(c, k)
    return f


def hubcap(fn):
    """Wrap a painter so the corners of square hub blocks are transparent on the wheel sides (round cap)."""
    def f(p):
        if p.face in ("east", "west") and p.fw >= 4:
            if math.hypot(p.x + 0.5 - p.fw / 2.0, p.y + 0.5 - p.fh / 2.0) > p.fw / 2.0 + 0.2:
                return None
        return fn(p)
    return f


def rubber():
    def f(p):
        x, y, z = p.p
        return shade(mix("#101215", "#24282d", noise3(x, y, z, 47, 1.4)), 1.0)
    return f


# ============================================================================ wheels
def tire_painter(tire="#15171a", rim="#c8ccd2", rim_dark="#5b6068", lug=False, spokes=8, rim_frac=0.62, accent=None):
    """Side faces: tyre ring + rim with spokes. Tread faces: grooves / lugs (rolling direction = texel y)."""
    def f(p):
        x, y, z = p.p
        if p.face in ("east", "west"):
            hx, hy = p.fw / 2.0, p.fh / 2.0
            dx, dy = p.x + 0.5 - hx, p.y + 0.5 - hy
            a = math.atan2(dy, dx)
            cy = p.cube["o"][1] + p.cube["s"][1] / 2.0
            if p.fw > 3 and math.hypot(dx, dy) > cy + 0.15 and True:
                return None                       # clip the block corners -> round silhouette
            rn = math.hypot(dx, dy) / cy
            if rn > rim_frac + 0.10:
                c = mix(tire, "#2c3036", noise3(x, y, z, 53, 1.2))
                if 0.9 < rn < 0.96:
                    c = shade(c, 1.9)             # moulded sidewall ring
                if lug and int((a + math.pi) / (math.pi / 8)) % 2 == 0:
                    c = shade(c, 0.7)
                return c
            if rn > rim_frac:
                return shade(rim_dark, 0.9)
            if rn < 0.16:
                return accent or shade(rim, 0.6)
            if rn < 0.30:
                return shade(rim, 1.05)
            k = ((a + math.pi) / (2 * math.pi / spokes)) % 1.0
            if k < 0.22 or k > 0.78:
                c = shade(rim, 0.85 + 0.25 * (1 - rn))
            else:
                c = shade(rim_dark, 0.65)
            return c
        # tread
        c = mix(tire, "#2a2e33", noise3(x, y, z, 59, 1.0))
        if lug:
            if (p.y % 4) < 2 and ((p.x + (p.y // 4)) % 3) != 1:
                c = shade(c, 1.35)
            else:
                c = shade(c, 0.75)
        else:
            if p.y % 3 == 0:
                c = shade(c, 0.65)
            if p.x == p.fw // 2:
                c = shade(c, 0.85)
        return c
    return f


# ============================================================================ decal helpers
def flame_decal(z_start, z_end, y_base, y_top, x_min=None, seed=3, faces=("east", "west")):
    """Painted tongues of flame licking from z_start back to z_end (z_start < z_end = toward the tail).
    Position-based so it stays continuous across all the body slices."""
    def d(p):
        if p.face not in faces:
            return None
        x, y, z = p.p
        if not (z_start <= z <= z_end):
            return None
        u = (z - z_start) / float(z_end - z_start)
        t = (z * 0.42 + (y - y_base) * 0.5) % 1.0
        saw = 1.0 - abs(2 * t - 1.0)
        top = y_base + (y_top - y_base) * (1.0 - u) ** 0.65 * (0.35 + 0.65 * saw)
        if y < y_base or y > top:
            return None
        v = (y - y_base) / max(0.5, top - y_base)
        if v > 0.85:
            return "#c81808"
        if v > 0.55:
            return "#ff5a12"
        if v > 0.25:
            return "#ff9d1a"
        return "#ffe15a"
    return d


def overlay(*decals):
    def d(p):
        for f in decals:
            c = f(p)
            if c is not None:
                return c
        return None
    return d


def checker(p, size=2.0, a="#f2f2f2", b="#15171a"):
    x, y, z = p.p
    return a if (int(math.floor(z / size)) + int(math.floor(y / size))) % 2 == 0 else b


# ============================================================================ Car builder
class Car:
    def __init__(self, pivot_y=4):
        self.bones = []
        self.by = {}
        self.bone("body", None, [0, pivot_y, 0])
        self.wheels = []          # (bone, rate)

    def bone(self, name, parent="body", pivot=(0, 0, 0), rotation=None):
        b = {"name": name, "parent": parent, "pivot": list(pivot), "cubes": []}
        if rotation:
            b["rotation"] = list(rotation)
        self.bones.append(b)
        self.by[name] = b
        return b

    def cube(self, bone, o, s, skin, **kw):
        c = {"o": [o[0], o[1], o[2]], "s": [int(round(v)) for v in s], "skin": skin}
        c.update(kw)
        self.by[bone]["cubes"].append(c)

    def sym(self, bone, o, s, skin, **kw):
        """Mirror across x=0 (cube origin x mirrored). Use for x-symmetric detail."""
        self.cube(bone, o, s, skin, **kw)
        self.cube(bone, [-o[0] - s[0], o[1], o[2]], s, skin, **kw)

    def brick(self, bone, i, k, ni, nk, y, h, skin, studs=True, skip=()):
        x0, z0 = -8 + 4 * i, -12 + 4 * k
        self.cube(bone, [x0, y, z0], [4 * ni, h, 4 * nk], skin + ("" if studs else "_s"))
        if studs:
            for a in range(ni):
                for b in range(nk):
                    if (i + a, k + b) in skip:
                        continue
                    self.cube(bone, [x0 + 4 * a + 1, y + h, z0 + 4 * b + 1], [2, 1, 2], skin)

    def minifig(self, bone, x, y, z, torso, legs, hat=None, head_dir=0):
        """Tiny 1/16-scale figure: leg block, torso, arms, yellow head with face (front = -Z), optional hat."""
        self.cube(bone, [x - 2, y, z - 1], [4, 3, 2], legs)
        self.cube(bone, [x - 2, y + 3, z - 1], [4, 4, 2], torso)
        self.cube(bone, [x - 3, y + 3, z - 1], [1, 3, 2], torso)
        self.cube(bone, [x + 2, y + 3, z - 1], [1, 3, 2], torso)
        self.cube(bone, [x - 1.5, y + 7, z - 1.5], [3, 3, 3], "minihead")
        if hat:
            self.cube(bone, [x - 2, y + 10, z - 2], [4, 1, 4], hat)
            self.cube(bone, [x - 1.5, y + 11, z - 1.5], [3, 1, 3], hat)

    def wheel(self, name, x, z, r, width, tire, hub, parent="body"):
        """Round wheel: four bars through the centre (0, 45, 90, 135 deg) whose union is a 16-gon of radius ~r.
        Spins about X around its centre. Use 8-fold symmetric rim patterns (spokes 4/8) so the bars agree."""
        L = int(round(r * 1.848))
        T = max(1, int(round(r * 0.765)))
        cy = r * 0.97
        self.bone(name, parent, [x, cy, z])
        ox = x - width / 2.0
        piv = [x, cy, z]
        self.cube(name, [ox, cy - T / 2.0, z - L / 2.0], [width, T, L], tire)
        self.cube(name, [ox, cy - L / 2.0, z - T / 2.0], [width, L, T], tire, inflate=0.01)
        self.cube(name, [ox, cy - T / 2.0, z - L / 2.0], [width, T, L], tire, rot=[45, 0, 0], pivot=piv, inflate=0.02)
        self.cube(name, [ox, cy - T / 2.0, z - L / 2.0], [width, T, L], tire, rot=[-45, 0, 0], pivot=piv, inflate=0.03)
        hs = max(2, int(round(cy * 0.62)))
        self.cube(name, [x - (width + 1) / 2.0, cy - hs / 2.0, z - hs / 2.0], [width + 1, hs, hs], hub)
        self.wheels.append((name, 916.0 / max(2.0, cy)))
        return cy

    def mirror_wheels(self, prefix, x, z, r, width, tire, hub):
        self.wheel(prefix + "l", x, z, r, width, tire, hub)
        self.wheel(prefix + "r", -x, z, r, width, tire, hub)


def spin_anim(car):
    return {n: {"rotation": [f"query.modified_distance_moved * {rate:.1f}", "0", "0"]} for n, rate in car.wheels}


def make_anims(car, body_extra=None, move_extra=None, idle_extra=None, fx=None, bump=0.18):
    """roll (always), move (speed>0), idle, fx (always). *_extra: {bone: {...}} dicts merged in."""
    roll = merge(spin_anim(car), body_extra or {})
    move = merge(
        {"body": {"position": ["0", f"math.sin(query.life_time * 1500) * {bump}", "0"]}},
        {"body": {"rotation": [f"math.sin(query.life_time * 1100) * 0.9 - query.modified_move_speed * 3",
                               "0", f"math.sin(query.life_time * 830) * 0.8"]}},
        move_extra or {})
    idle = merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 200) * 0.06", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 120) * 0.4", "0", "0"]}},
        idle_extra or {})
    out = {"roll": anim(roll), "move": anim(move), "idle": anim(idle)}
    if fx:
        out["fx"] = anim(fx)
    return out


PLAY = ["roll", {"move": "query.modified_move_speed > 0.02"}, {"idle": "query.modified_move_speed <= 0.02"}, "fx"]


def make_spec(car, cid, name, egg, skins, anims, hp=24, speed=0.62, box=(1.3, 0.9), seat=(0, 0.3, 0.0),
              visible=(3.0, 1.8, 0.55), family=("vehicle", "toycar"), has_fx=True):
    skins = dict(skins)
    skins.setdefault("default", next(iter(skins.values())))
    play = [x for x in PLAY if x != "fx" or has_fx]
    return {
        "id": cid, "name": name, "egg": egg, "glow": True, "scale": 1.0,
        "visible": list(visible), "bones": car.bones, "skins": skins, "anims": anims, "play": play,
        "behavior": {
            "role": "mount", "health": hp, "speed": speed, "damage": 0, "box": list(box),
            "knockback_resist": 0.6, "family": list(family), "step_height": 0.6,
            "ride": {"seats": [list(seat)], "jump": 0.5},
            "sound": ("golem", [1.5, 1.8]),
        },
    }


# ============================================================================ minifig skins
def minihead(p):
    x, y, z = p.p
    c = rgb("#f7d21a")
    if p.face == "front":
        # two eyes and a smile on a 3x3 face
        if p.y == 0 and p.x in (0, 2):
            return rgb("#1a1a1a")
        if p.y == 2 and p.x == 1:
            return rgb("#7a2a12")
    k = {"top": 1.1, "bottom": 0.6, "front": 1.0, "back": 0.9, "east": 0.85, "west": 1.0}[p.face]
    return shade(c, k)


# ============================================================================ die-cast toolkit
def dc_paint(base, decal=None, spec_y=8.0, flake=0.06, seed=71, glass_fn=None, chrome_fn=None):
    """Metallic clear-coat die-cast paint. decal(p) may return a colour, None, 'GLASS' or 'CHROME'."""
    glass_fn = glass_fn or glass("#8fc4ff", "#1a2b47")
    chrome_fn = chrome_fn or chrome(7.0)

    def f(p):
        x, y, z = p.p
        d = decal(p) if decal else None
        if d == "GLASS":
            return glass_fn(p)
        if d == "CHROME":
            return chrome_fn(p)
        c = rgb(d if d is not None else base)
        k = 1.0
        if p.face == "top":
            k = 1.10 - 0.025 * abs(x)
            hl = math.exp(-((abs(x) - 3.2) ** 2) / 1.6)
            c = mix(c, "#ffffff", 0.32 * hl)
        elif p.face == "bottom":
            k = 0.55
        else:
            t = clamp((y - 3.0) / 9.0)
            k = (0.66 + 0.5 * t) * {"front": 1.0, "back": 0.9, "east": 0.88, "west": 1.0}[p.face]
            hl = math.exp(-((y - spec_y) ** 2) / 0.7)
            c = mix(c, "#ffffff", 0.34 * hl)
            hl2 = math.exp(-((y - spec_y + 3.2) ** 2) / 1.4)
            c = shade(c, 1.0 - 0.15 * hl2)
        if hash01(x, y, z, seed) > 0.965:
            k *= 1.22
        k *= wobble(p, seed + 2, 1.3, flake)
        e = min(p.x, p.fw - 1 - p.x, p.y, p.fh - 1 - p.y)
        if e == 0 and p.fw > 2 and p.fh > 2:
            k *= 0.9
        return shade(c, k)
    return f


def slices(car, bone, z0, z1, step, xh, yb, yt, skin):
    """Extrude a side profile along Z in `step`-unit slabs. xh/yb/yt are functions of slab-centre z."""
    z = z0
    while z < z1 - 1e-6:
        zc = z + step / 2.0
        w, b, t = xh(zc), yb(zc), yt(zc)
        if w > 0 and t > b:
            wi = max(1, int(round(2 * w)))
            car.cube(bone, [-wi / 2.0, b, z], [wi, int(round(t - b)), step], skin)
        z += step


def pipes_skin(p):
    return chrome(5.0)(p)


def engine_skin(base="#3a3f47", hi="#c9ced6"):
    """Cast-iron engine block: fins, bolts, darker crevices."""
    def f(p):
        x, y, z = p.p
        c = mix(base, "#15181c", 0.25 + 0.5 * noise3(x, y, z, 83, 1.6))
        if int(math.floor(z)) % 2 == 0 and p.face in ("east", "west", "top"):
            c = mix(c, hi, 0.35)                      # cooling fins
        if hash01(x, y, z, 89) > 0.94:
            c = shade(c, 1.5)
        if p.face == "top":
            c = shade(c, 1.15)
        return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 0.9))
    return f


def dc_skins(body, decal=None, spec_y=8.0, extra=None, accent="#ff6a00", rim_spokes=8):
    s = {
        "paint": dc_paint(body, decal, spec_y),
        "glass": glass("#8fc4ff", "#1a2b47"),
        "chrome": chrome(5.5), "chrome_lo": chrome(4.0),
        "black": matte("#16181c", 101, 0.15),
        "dark": matte("#2a2e35", 103, 0.2, 6.0),
        "orange": dc_paint(accent, None, spec_y),
        "engine": engine_skin(),
        "seat": matte("#1b1d21", 107, 0.25),
        "seat_o": matte(accent, 109, 0.15),
        "tire": tire_painter("#111316", "#d8dde4", "#4c5058", False, rim_spokes, 0.78, accent),
        "hub": hubcap(chrome(9.0)),
        "lamp_y": lamp("#fff2b0"), "lamp_r": lamp("#ff2a1a"), "lamp_o": lamp("#ff9a1f"),
        "lamp_c": lamp("#7be9ff"), "flame": lamp("#ff8a1a"),
        "head": headlamp,
        "grille": grille,
        "default": dc_paint(body, decal, spec_y),
    }
    if extra:
        s.update(extra)
    return s


def headlamp(p):
    """Chrome bezel around a warm glowing lens (only the front face is a lens)."""
    if p.face == "front":
        rn = math.hypot(p.x + 0.5 - p.fw / 2.0, p.y + 0.5 - p.fh / 2.0) / (p.fw / 2.0)
        if rn < 0.72:
            return glow(mix("#fff4c8", "#ffffff", 0.5 if rn < 0.35 else 0.0))
        return chrome(9.0)(p)
    return chrome(9.0)(p)


def grille(p):
    x, y, z = p.p
    if p.face == "front":
        if p.x % 2 == 0:
            return chrome(5.5)(p)
        return "#0b0c0e"
    return chrome(7.0)(p)


def door_lines(p, z_front, z_back, y_lo, y_hi, handle=True):
    """Panel gaps + handle for a door between z_front..z_back on side faces. Returns colour or None."""
    x, y, z = p.p
    if p.face not in ("east", "west") or not (y_lo <= y <= y_hi):
        return None
    if abs(z - z_front) < 0.5 or abs(z - z_back) < 0.5:
        return "#0d0f14"
    if handle and abs(z - (z_back - 1.8)) < 0.9 and abs(y - (y_hi - 1.4)) < 0.5:
        return "CHROME"
    return None
