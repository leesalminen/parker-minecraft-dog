"""Shared helpers for the eggsd_* sci-fi / alien / robot / bug creature specs (no SPEC here on purpose)."""
import math
from lib import *


# ------------------------------------------------------------------ geometry helpers
def C(o, s, skin=None, **kw):
    d = {"o": list(o), "s": list(s)}
    if skin: d["skin"] = skin
    d.update(kw)
    return d


def mir(c):
    """Mirror a cube across x=0 (rotations flip consistently)."""
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"])}
    for k in ("skin", "inflate"):
        if k in c: m[k] = c[k]
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    return m


def pair(*cubes):
    out = []
    for c in cubes: out += [c, mir(c)]
    return out


def B(name, parent, pivot, cubes=None, **kw):
    b = {"name": name, "parent": parent, "pivot": list(pivot), "cubes": list(cubes or [])}
    b.update(kw)
    return b


def mirror_bone(b, newname, newparent=None):
    m = {"name": newname, "parent": newparent if newparent else b["parent"],
         "pivot": [-b["pivot"][0], b["pivot"][1], b["pivot"][2]],
         "cubes": [mir(c) for c in b["cubes"]]}
    return m


def auto_visible(bones, scale):
    mx = mz = my = 0.0
    for b in bones:
        for c in b.get("cubes", []):
            inf = c.get("inflate", 0) + 2
            x0, y0, z0 = c["o"]; w, h, d = c["s"]
            mx = max(mx, abs(x0) + inf, abs(x0 + w) + inf)
            mz = max(mz, abs(z0) + inf, abs(z0 + d) + inf)
            my = max(my, y0 + h + inf)
    r = max(mx, mz)
    return [round(2 * r / 16 * scale * 1.15 + 0.6, 2), round(my / 16 * scale * 1.15 + 0.8, 2),
            round((my / 16 * scale * 1.15 + 0.8) / 2, 2)]


def make(cid, name, egg, bones, skins, anims, play, behavior, scale=1.0, glow=False):
    return {"id": cid, "name": name, "egg": egg, "glow": glow, "scale": scale,
            "visible": auto_visible(bones, scale), "bones": bones, "skins": skins,
            "anims": anims, "play": play, "behavior": behavior}


def N(p, seed=1, sc=3.0):
    return noise3(p.p[0], p.p[1], p.p[2], seed, sc)


# ------------------------------------------------------------------ painters (return fn(p))
def organic(base, alt=None, seed=1, sc=3.0, grain=0.10, top=1.0, bottom=1.0):
    alt = alt or shade(base, 0.78)
    def f(p):
        c = mix(alt, base, N(p, seed, sc))
        c = shade(c, 1 - grain + 2 * grain * hash01(p.p[0] * 3, p.p[1] * 3, p.p[2] * 3, seed))
        if p.face == "top": c = shade(c, 1.1 * top)
        if p.face == "bottom": c = shade(c, 0.78 * bottom)
        return c
    return f


def belly(fn, col, ymax, soft=3.0, amt=0.85):
    def f(p):
        c = fn(p)
        if c is None: return c
        y = p.p[1]
        if y < ymax:
            t = min(1.0, (ymax - y) / soft)
            c = mix(c, col, amt * t)
        return c
    return f


def spotted(base, spot, seed=5, sc=1.6, thr=0.72, alt=None):
    bf = organic(base, alt, seed + 1, 4.0, 0.06)
    def f(p):
        if N(p, seed, sc) > thr: return shade(spot, 0.9 + 0.2 * hash01(p.p[0], p.p[1], p.p[2], seed))
        return bf(p)
    return f


def starry(base, alt, star, seed=7, density=0.045, glowing=True):
    bf = organic(base, alt, seed, 3.5, 0.08)
    def f(p):
        if hash01(p.p[0] * 2, p.p[1] * 2, p.p[2] * 2, seed + 11) < density:
            return glow(star) if glowing else star
        return bf(p)
    return f


def metal(base, seam=None, seed=3, rivet=True, hi=1.14, split=0):
    seam = seam or shade(base, 0.58)
    def f(p):
        c = shade(base, 0.92 + 0.16 * N(p, seed, 1.6))
        w, h = p.fw, p.fh
        if w >= 4 and h >= 4:
            if p.x == 0 or p.y == 0: return shade(c, 1.15) if (p.x == 0 and p.y == 0) else seam
            if p.x == w - 1 or p.y == h - 1: return shade(seam, 0.85)
            if rivet and w >= 6 and h >= 6 and p.x in (1, w - 2) and p.y in (1, h - 2): return shade(c, 1.3)
            if split and w >= 8 and p.x == w // 2: return shade(seam, 1.1)
        if p.face == "top": c = shade(c, hi)
        if p.face == "bottom": c = shade(c, 0.75)
        return c
    return f


def lit(col, seed=9, var=0.12):
    """Emissive flat colour with slight variation."""
    def f(p): return glow(shade(col, 1 - var + 2 * var * hash01(p.p[0], p.p[1], p.p[2], seed)))
    return f


def flat(col, grain=0.06, seed=4):
    def f(p): return shade(col, 1 - grain + 2 * grain * hash01(p.p[0], p.p[1], p.p[2], seed))
    return f


def eyes(white, iris, pupil, glowing=False, back=None):
    """Painter for a small eye cube: front face shows iris+pupil, rest = white/dim."""
    def f(p):
        if p.face == "front":
            cx, cy = p.fw / 2, p.fh / 2
            dx, dy = abs(p.x + .5 - cx), abs(p.y + .5 - cy)
            if dx < 0.75 and dy < 0.75 and p.fw > 1 and p.fh > 1: return pupil
            if p.fw <= 2 and p.fh <= 2: return glow(iris) if glowing else iris
            if p.x + p.y == 0 and p.fw > 2: return "#ffffff"
            return glow(iris) if glowing else iris
        return back or white
    return f


def slit_eyes(iris, pupil="#101018"):
    def f(p):
        if p.face == "front":
            if p.x == p.fw // 2: return pupil
            return glow(iris)
        return shade(iris, 0.7)
    return f


def dot_eye(col, pupil="#101018", glowing=True):
    return eyes(col, col, pupil, glowing)


def stripes(base, stripe, period=5.0, width=1.6, axis=2, seed=2):
    bf = organic(base, None, seed, 3.0, 0.06)
    def f(p):
        v = p.p[axis] % period
        if v < width: return shade(stripe, 0.92 + 0.16 * hash01(p.p[0], p.p[1], p.p[2], seed))
        return bf(p)
    return f


def chitin(base, hi, seed=6, seam_axis=None, period=6.0):
    def f(p):
        n = N(p, seed, 2.5)
        c = mix(base, hi, 0.15 + 0.7 * n)
        y = p.p[1]
        c = shade(c, 0.85 + 0.3 * hash01(p.p[0] * 2, y * 2, p.p[2] * 2, seed))
        if p.face == "top": c = shade(c, 1.18)
        if p.face == "bottom": c = shade(c, 0.7)
        if seam_axis is not None and (p.p[seam_axis] % period) < 0.7: c = shade(c, 0.55)
        # glossy highlight streak
        if (p.p[0] * 0.7 + p.p[2] * 0.4) % 9 < 0.8 and p.face in ("top", "front", "east", "west"):
            c = shade(c, 1.2)
        return c
    return f


def rounded(fn):
    """Cut the 4 corner pixels of the side faces to make cubes look rounder (leave transparent)."""
    def f(p):
        if p.face in ("front", "back", "east", "west") and p.fw >= 5 and p.fh >= 5:
            if p.x in (0, p.fw - 1) and p.y in (0, p.fh - 1): return None
        return fn(p)
    return f


# ------------------------------------------------------------------ limb builders
def leg(name, parent, x, ytop, z, w, h, d, skin, foot=None, foot_skin=None, px=None):
    cubes = [C([x, ytop - h, z], [w, h, d], skin)]
    if foot:
        fw, fh, fd = foot
        cubes.append(C([x + w / 2 - fw / 2, ytop - h, z + d / 2 - fd / 2], [fw, fh, fd], foot_skin or skin))
    return B(name, parent, [x + w / 2, ytop, z + d / 2], cubes)


def wave(bone, amp, rate=70, axis=1, off=0.0):
    r = ["0", "0", "0"]
    r[axis] = f"math.sin(query.life_time * {rate} + {off}) * {amp}"
    return {bone: {"rotation": r}}


def hop(bone, amp=1.5):
    return {bone: {"position": ["0", f"math.abs(math.sin(query.modified_distance_moved * 60)) * {amp} * query.modified_move_speed * 3", "0"]}}
