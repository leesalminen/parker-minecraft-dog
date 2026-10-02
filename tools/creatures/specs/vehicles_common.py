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


# ====================================================================== realism helpers (added for v1.8)
def loft(stations, skin, dz=4, x0=0.0):
    """Stack thin slabs along Z to make a smooth tapered body (fuselage, tail boom, hull, nose cone).
    stations: [(z, half_width, y_bottom, y_top), ...] ascending in z; values are linearly interpolated."""
    out = []
    z = stations[0][0]
    end = stations[-1][0]
    while z < end - 1e-6:
        step = min(dz, end - z)
        zc = z + step / 2.0
        for a, b in zip(stations, stations[1:]):
            if a[0] <= zc <= b[0]:
                t = (zc - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0
                hw = a[1] + (b[1] - a[1]) * t
                y0 = a[2] + (b[2] - a[2]) * t
                y1 = a[3] + (b[3] - a[3]) * t
                break
        out.append({"o": [x0 - hw, y0, z], "s": [max(1, round(2 * hw)), max(1, round(y1 - y0)), max(1, round(step))],
                    "skin": skin})
        z += step
    return out


def wheel_cubes(cx, cy, cz, D, w, skin="tire"):
    """Round wheel about the X axis: four D x (0.414 D) slabs at 0/45/90/135 degrees make an octagon.
    Pair with tire_round() as the skin painter (it reads radius/angle from the cube, so seams vanish)."""
    s = max(2, round(D * 0.4142))
    return [{"o": [cx - w / 2.0, cy - D / 2.0, cz - s / 2.0], "s": [int(w), int(D), int(s)], "skin": skin,
             "rot": [a, 0, 0], "pivot": [cx, cy, cz]} for a in (0, 45, 90, 135)]


def tire_round(hub="#c3ccd2", lugs=0, lug_depth=0.55, rim_frac=0.56, bolts=5, tread="#15181b", side="#1c1f23"):
    """Painter for wheel_cubes: true radial rings on the sidewall, lugged or ribbed tread on the outer facets."""
    def fn(p):
        c = p.cube
        cy, cz = c["pivot"][1], c["pivot"][2]
        th = math.radians(c["rot"][0])
        x, y, z = p.p
        dy, dz = y - cy, z - cz
        r = math.hypot(dy, dz)
        R = c["s"][1] / 2.0
        ang = math.atan2(dy, dz) + th
        if p.face in ("east", "west"):
            if r > R * 0.985:
                return shade(side, 0.8)
            if r > R * rim_frac + 2.0:
                base = mix(side, "#2b3036", noise3(x, y, z, 7, 1.6))
                base = shade(base, 0.9 + 0.2 * noise3(x, y, z, 8, 0.7))
                if r > R * 0.9 and hash01(int(ang * 9), int(r), 3) > 0.985:
                    base = shade(base, 1.4)               # sidewall lettering fleck
                return base
            if r > R * rim_frac - 0.6:
                return shade(hub, 0.55)                    # rim lip shadow
            k = mix(hub, "#59636b", 0.2 + 0.5 * noise3(x, y, z, 9, 1.4))
            if r < R * 0.16:
                return shade("#3a4148", 0.9)
            for i in range(bolts):
                ba = 2 * math.pi * i / bolts
                bx, by = math.cos(ba) * R * 0.3, math.sin(ba) * R * 0.3
                px_, py_ = math.cos(ang) * r, math.sin(ang) * r
                if math.hypot(px_ - bx, py_ - by) < max(0.9, R * 0.06):
                    return shade(hub, 1.25)
            if R * 0.36 < r < R * 0.4:
                return shade(k, 0.7)
            return k
        # tread facets
        col = mix(tread, "#2d3237", noise3(x, y, z, 11, 1.5))
        if lugs:
            f = ((ang / (2 * math.pi)) * lugs) % 1.0
            u = p.x / max(1.0, p.fw - 1)
            block = (f < 0.5) != (abs(u - 0.5) < 0.16 and False)
            if f < 0.42:
                col = shade(col, 1.18)
            else:
                col = shade(col, 1 - lug_depth * 0.6)
            if abs(p.x + 0.5 - p.fw / 2.0) < 0.6 and p.fw > 6:
                col = shade(col, 0.75)                     # centre groove
        else:
            for g in (0.25, 0.5, 0.75):
                if abs((p.x + 0.5) / p.fw - g) < 0.05:
                    col = shade(col, 0.6)
        return col
    return fn


def seat_set(x, y, z, w=14, d=13, back_h=20, skin="fabric", trim="under", head=True, lean=-8):
    """A bucket seat: cushion, leaning backrest, headrest, side bolsters.  (x, z) = centre of cushion, y = cushion bottom."""
    cs = [
        {"o": [x - w / 2.0, y, z - d / 2.0], "s": [w, 4, d], "skin": skin},
        {"o": [x - w / 2.0, y + 4, z - d / 2.0 + 1], "s": [2, 2, d - 2], "skin": skin},
        {"o": [x + w / 2.0 - 2, y + 4, z - d / 2.0 + 1], "s": [2, 2, d - 2], "skin": skin},
        {"o": [x - w / 2.0, y + 4, z + d / 2.0], "s": [w, back_h, 3], "skin": skin, "rot": [lean, 0, 0],
         "pivot": [x, y + 4, z + d / 2.0]},
        {"o": [x - w / 2.0 + 1, y + 4 + back_h - 1, z + d / 2.0 + 0.5], "s": [2, 1, 3], "skin": trim, "rot": [lean, 0, 0],
         "pivot": [x, y + 4, z + d / 2.0]},
    ]
    if head:
        cs.append({"o": [x - 3.5, y + 4 + back_h, z + d / 2.0 + 0.4], "s": [7, 5, 3], "skin": skin, "rot": [lean, 0, 0],
                   "pivot": [x, y + 4, z + d / 2.0]})
    return cs


def cyl_z(cx, cy, z0, length, D, skin):
    """Octagonal cylinder along Z (nacelle, barrel): four D x 0.414D slabs at 0/45/90/135 degrees."""
    D = int(D); t = max(2, int(round(D * 0.4142)))
    return [{"o": [cx - D / 2.0, cy - t / 2.0, z0], "s": [D, t, int(length)], "skin": skin,
             "rot": [0, 0, a], "pivot": [cx, cy, z0 + length / 2.0]} for a in (0, 45, 90, 135)]


def ring_z(cx, cy, z, R, t, dz, skin):
    """Hollow regular-octagon frame (apothem R) in the XY plane, open in the middle so a pilot inside can see out."""
    out = []
    side = max(2, int(round(R * 0.8284 + t * 0.8)))
    for k in range(8):
        th = k * 45
        a = R - t / 2.0
        bx, by = cx + a * math.sin(math.radians(th)), cy + a * math.cos(math.radians(th))
        c = {"o": [bx - side / 2.0, by - t / 2.0, z], "s": [side, int(t), int(dz)], "skin": skin}
        if th:
            c["rot"] = [0, 0, th]; c["pivot"] = [bx, by, z + dz / 2.0]
        out.append(c)
    return out


def panel_paint(cy, R, base="#1d2a3a", frame="#8b949c", spoke="#4a535c"):
    """Hexagonal solar-panel painter (pointy-top hexagon in the YZ plane centred at height cy, z=0)."""
    def fn(p):
        x, y, z = p.p
        if p.face not in ("east", "west"):
            return shade(mix("#2a2f35", frame, 0.4 + 0.4 * noise3(x, y, z, 5, 2.0)), 0.9 if p.face == "bottom" else 1.0)
        yy, zz = y - cy, z
        hn = max(abs(yy), abs(yy) * 0.5 + abs(zz) * 0.866)
        if hn > R - 3.2:
            return shade(frame, 0.85 + 0.2 * noise3(x, y, z, 6, 1.5))
        ang = math.degrees(math.atan2(zz, yy)) % 60.0
        if min(ang, 60.0 - ang) * math.pi / 180 * max(hn, 1) < 0.9 or hn < 5:
            return shade(spoke, 0.9 + 0.2 * noise3(x, y, z, 7, 1.2))
        for rr in (R * 0.36, R * 0.68):
            if abs(hn - rr) < 0.8:
                return shade(spoke, 0.95)
        c = mix(base, "#34506e", noise3(x, y, z, 8, 3.0))
        return shade(c, 0.9 + 0.2 * noise3(x, y, z, 9, 0.8))
    return fn


def cyl_y(cx, cz, y0, h, D, skin):
    """Upright octagonal prism (rocket body, tank): four D x 0.414D slabs turned 0/45/90/135 degrees about Y."""
    D = int(D); t = max(2, int(round(D * 0.4142)))
    return [{"o": [cx - D / 2.0, y0, cz - t / 2.0], "s": [D, int(h), t], "skin": skin,
             "rot": [0, a, 0], "pivot": [cx, y0 + h / 2.0, cz]} for a in (0, 45, 90, 135)]
