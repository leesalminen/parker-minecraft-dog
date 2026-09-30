"""Shared painters / helpers for the Galaxy vehicles (car, plane, helicopter).  Not a spec itself."""
import math
from lib import *


def paint(base, dark, seed=1, period=12.0, edge_dark=0.78):
    """Painted sheet metal: soft mottling, panel seams, rivets, top faces catch light."""
    def fn(p):
        x, y, z = p.p
        c = mix(dark, base, 0.55 + 0.45 * noise3(x, y, z, seed, 4.0))
        c = shade(c, 0.94 + 0.12 * noise3(x, y, z, seed + 5, 1.2))
        if (x % period) < 0.6 or (z % period) < 0.6 or (y % period) < 0.6:
            c = shade(c, edge_dark)
        dx = min(x % period, period - x % period)
        dz = min(z % period, period - z % period)
        if dx < 0.7 and dz < 0.7:
            c = shade(c, 0.85)
        if p.face == "top":
            c = shade(c, 1.12)
        elif p.face == "bottom":
            c = shade(c, 0.72)
        if hash01(x, y, z, seed + 9) > 0.97:
            c = shade(c, 1.2)
        return c
    return fn


def chrome(p):
    x, y, z = p.p
    c = mix("#6d7780", "#e6eef2", 0.35 + 0.65 * noise3(x, y, z, 401, 1.6))
    if abs((x + z) % 4.0 - 2.0) < 0.5:
        c = shade(c, 1.15)
    return shade(c, 0.92 + 0.14 * noise3(x, y, z, 403, 0.9))


def rubber(p):
    x, y, z = p.p
    return shade(mix("#101215", "#24282d", noise3(x, y, z, 411, 1.8)), 0.92 + 0.16 * noise3(x, y, z, 413, 0.8))


def dark_metal(p):
    x, y, z = p.p
    c = mix("#1c2026", "#3b424a", noise3(x, y, z, 421, 2.2))
    if (x % 6.0) < 0.5 or (z % 6.0) < 0.5:
        c = shade(c, 0.7)
    return c


def tire(hub="#b9c2c8"):
    """Round wheel painter: tyre ring + hub on the side faces, plain rubber on the tread."""
    def fn(p):
        x, y, z = p.p
        if p.face in ("east", "west"):
            dx, dy = p.x + 0.5 - p.fw / 2.0, p.y + 0.5 - p.fh / 2.0
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            R = min(p.fw, p.fh) / 2.0
            if r > R - 1.7:
                c = mix("#111316", "#2b3036", 0.3 + 0.5 * noise3(x, y, z, 7, 1.4))
                if ((a + math.pi) / (math.pi / 6)) % 1.0 < 0.45:
                    c = shade(c, 0.62)
            else:
                c = mix(hub, "#5a636a", 0.25 + 0.5 * noise3(x, y, z, 9, 1.5))
                k = ((a + math.pi) / (math.pi / 2.5)) % 1.0
                if k < 0.16 or k > 0.84:
                    c = shade(c, 0.5)
                if r < 1.0:
                    c = shade(c, 0.45)
        else:
            c = mix("#111316", "#272b30", 0.3 + 0.6 * noise3(x, y, z, 11, 1.4))
        return c
    return fn


def glass(tint="#8fd8ff"):
    """Mostly see-through window: only a frame edge and sheen streaks are opaque (alpha-test pack)."""
    def fn(p):
        edge = p.x < 1 or p.y < 1 or p.x >= p.fw - 1 or p.y >= p.fh - 1
        if edge:
            return mix("#1d2a33", "#3e5460", hash01(p.x, p.y, 3))
        s = (p.x * 0.9 + p.y * 1.4) % 9.0
        if s < 1.1:
            return mix(tint, "#ffffff", 0.35)
        return None
    return fn


def glass_solid(tint="#5fd0ff"):
    def fn(p):
        x, y, z = p.p
        c = mix("#10465e", tint, 0.3 + 0.7 * noise3(x, y, z, 71, 2.0))
        return shade(c, 0.92 + 0.14 * noise3(x, y, z, 73, 1.0))
    return fn


def lamp(color):
    def fn(p):
        x, y, z = p.p
        return glow(shade(color, 0.85 + 0.3 * noise3(x, y, z, 431, 1.0)))
    return fn


def fabric(base="#2b2f38", top="#3a4050", seed=77):
    def fn(p):
        x, y, z = p.p
        c = mix(base, top, 0.3 + 0.7 * noise3(x, y, z, seed, 2.4))
        if (int(x) + int(z)) % 3 == 0:
            c = shade(c, 0.92)
        return shade(c, 0.92 + 0.16 * noise3(x, y, z, seed + 2, 0.9))
    return fn


def stripe(c1, c2, axis="z", w=4.0, seed=91):
    def fn(p):
        x, y, z = p.p
        v = {"x": x, "y": y, "z": z}[axis]
        c = c1 if (v // w) % 2 == 0 else c2
        return shade(c, 0.92 + 0.16 * noise3(x, y, z, seed, 1.0))
    return fn


def plate_fn(bg="#f2f0e4"):
    def fn(p):
        edge = p.x < 1 or p.y < 1 or p.x >= p.fw - 1 or p.y >= p.fh - 1
        if edge:
            return "#7a7a72"
        return "#3a5a9a" if (p.x % 3 == 1 and 1 < p.y < p.fh - 2) else bg
    return fn


def sym(cubes, c):
    """Append cube c and its X-mirror (a separate cube, so it gets its own UVs)."""
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "body")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)
