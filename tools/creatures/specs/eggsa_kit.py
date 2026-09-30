"""Shared helpers for the eggsa_* prehistoric creature specs (not a creature itself).
Units are 1/16 block. Model faces -Z (front), tail towards +Z, ground y=0."""
import math
from lib import *


# ------------------------------------------------------------------ geometry helpers
def cube(o, s, skin=None, rot=None, pivot=None, inflate=None):
    c = {"o": [float(v) if v != int(v) else int(v) for v in o], "s": [max(1, int(round(v))) for v in s]}
    if skin: c["skin"] = skin
    if rot:
        c["rot"] = list(rot)
        c["pivot"] = list(pivot) if pivot else [c["o"][0] + c["s"][0] / 2, c["o"][1] + c["s"][1] / 2, c["o"][2] + c["s"][2] / 2]
    if inflate: c["inflate"] = inflate
    return c


def mirror(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"])}
    if "skin" in c: m["skin"] = c["skin"]
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c: m["inflate"] = c["inflate"]
    return m


def pair(cubes, c):
    """Append c (drawn on the +x side) and its mirror."""
    cubes.append(c); cubes.append(mirror(c))


def bone(name, parent, pivot, cubes=None, rotation=None):
    b = {"name": name, "parent": parent, "pivot": list(pivot), "cubes": cubes if cubes is not None else []}
    if rotation: b["rotation"] = list(rotation)
    return b


def get(bones, name):
    for b in bones:
        if b["name"] == name: return b
    raise KeyError(name)


def eyes(cubes, x, y, z, size=2, skin="eye", depth=1):
    """Front-facing eye pair on a head whose front face is at z. x = centre offset of each eye."""
    pair(cubes, cube([x - size / 2, y, z - depth + 0.0], [size, size, depth + 0], skin))


def side_eyes(cubes, x, y, z, size=2, skin="eye"):
    """Eyes on the side faces of a head (x = head half-width)."""
    pair(cubes, cube([x, y, z], [1, size, size], skin))


def quad(W, H, L, leg_h, lw, ld, skin="body", leg_skin="leg", foot_skin=None, toe_skin=None, toes=0,
         fz=1.0, bz=1.0, inset=0.0, overlap=1, front_lw=None, front_ld=None, body_y_extra=0):
    """Standard quadruped: body + 4 legs pivoting at body underside. Returns bones list."""
    bones = [bone("body", None, [0, leg_h + H / 2, 0], [cube([-W / 2, leg_h + body_y_extra, -L / 2], [W, H, L], skin)])]
    flw = front_lw or lw; fld = front_ld or ld
    for nm, sx, zc, w_, d_ in (("leg_fl", 1, -L / 2 + fld / 2 + fz, flw, fld), ("leg_fr", -1, -L / 2 + fld / 2 + fz, flw, fld),
                               ("leg_bl", 1, L / 2 - ld / 2 - bz, lw, ld), ("leg_br", -1, L / 2 - ld / 2 - bz, lw, ld)):
        xc = sx * (W / 2 - w_ / 2 - inset)
        cs = [cube([xc - w_ / 2, 0, zc - d_ / 2], [w_, leg_h + overlap, d_], leg_skin)]
        if foot_skin:
            cs.append(cube([xc - w_ / 2 - 0.5, 0, zc - d_ / 2 - 0.5], [w_ + 1, 2, d_ + 1], foot_skin))
        if toes:
            tw = w_ / toes
            for i in range(toes):
                cs.append(cube([xc - w_ / 2 + i * tw + (tw - 1) / 2 if tw >= 1 else xc - w_ / 2 + i, 0, zc - d_ / 2 - 1.5], [1, 1, 2], toe_skin or "claw"))
        bones.append(bone(nm, "body", [xc, leg_h + 1, zc], cs))
    return bones


def biped(W, H, L, leg_h, lw, ld, skin="body", leg_skin="leg", foot_len=0, foot_skin=None, toes=3, gap=0.0, bz=0.0,
          hip_z=0.0, thigh_h=None):
    """Bipedal dino: body (horizontal) with two legs (thigh+shin pivot as one bone) and clawed feet."""
    bones = [bone("body", None, [0, leg_h + H / 2, 0], [cube([-W / 2, leg_h, -L / 2], [W, H, L], skin)])]
    for nm, sx in (("leg_l", 1), ("leg_r", -1)):
        xc = sx * (W / 2 - lw / 2 + gap)
        zc = hip_z
        cs = [cube([xc - lw / 2, 0, zc - ld / 2], [lw, leg_h + 2, ld], leg_skin)]
        if thigh_h:
            cs.append(cube([xc - lw / 2 - 0.5, leg_h - thigh_h + 2, zc - ld / 2 - 0.5], [lw + 1, thigh_h, ld + 1], leg_skin))
        fl = foot_len or ld + 3
        cs.append(cube([xc - lw / 2 - 0.5, 0, zc - ld / 2 - fl + ld], [lw + 1, 2, fl], foot_skin or leg_skin))
        for i in range(toes):
            tx = xc - lw / 2 - 0.5 + i * (lw + 1 - 1) / max(1, toes - 1) if toes > 1 else xc - 0.5
            cs.append(cube([tx, 0, zc - ld / 2 - fl + ld - 2], [1, 2, 2], "claw"))
        bones.append(bone(nm, "body", [xc, leg_h + 1, zc], cs))
    return bones


def tail(bones, parent, y, z, n, w, h, l, taper=0.8, rise=0.0, skin="tail", name="tail", tip_skin=None, fall=0.0):
    prev = parent; zc = z; yc = y
    for i in range(n):
        wi = max(1, int(round(w * taper ** i))); hi = max(1, int(round(h * taper ** i)))
        sk = tip_skin if (tip_skin and i == n - 1) else skin
        bones.append(bone(f"{name}{i}", prev, [0, yc + hi / 2, zc], [cube([-wi / 2, yc, zc], [wi, hi, l], sk)]))
        prev = f"{name}{i}"; zc += l; yc += rise - fall
    return prev


# ------------------------------------------------------------------ painters
def pelt(base, alt=None, belly=None, belly_y=None, seed=1, patch=5.0, fine=0.16, stripes=None, spots=None,
         cells=0, top=None, top_y=None):
    """General organic painter. stripes=(color,freq,thr,axis) spots=(color,scale,thr) top=(color,mix) above top_y."""
    alt = alt or shade(base, 0.72)

    def fn(p):
        x, y, z = p.p
        c = mix(alt, base, noise3(x, y, z, seed, patch))
        if cells:
            c = shade(c, 0.86 + 0.28 * hash01(math.floor(x / cells), math.floor(y / cells), math.floor(z / cells), seed + 3))
        c = shade(c, 1 - fine + 2 * fine * noise3(x * 1.7, y * 1.7, z * 1.7, seed + 7, 1.0))
        if stripes:
            col, freq, thr, ax = stripes
            v = {"x": x, "y": y, "z": z}[ax]
            s = math.sin(v * freq + noise3(x, y, z, seed + 9, 4.0) * 3.0)
            if s > thr: c = mix(c, col, min(0.85, 0.35 + (s - thr) * 2))
        if spots:
            col, sc, thr = spots
            if noise3(x, y, z, seed + 11, sc) > thr: c = mix(c, col, 0.85)
        if top and top_y is not None and y > top_y:
            c = mix(c, top[0], top[1])
        if belly and belly_y is not None and y < belly_y:
            c = mix(c, belly, min(1.0, (belly_y - y) / 2.5))
        return c
    return fn


def solid(color, var=0.10, seed=5):
    def fn(p):
        x, y, z = p.p
        return shade(color, 1 - var + 2 * var * noise3(x * 1.4, y * 1.4, z * 1.4, seed, 1.0))
    return fn


def plates(base, edge=0.72, ridge=None):
    """Bevelled plate: darker rim per face, optional lighter centre ridge."""
    def fn(p):
        x, y = p.x, p.y
        e = min(x, p.fw - 1 - x, y, p.fh - 1 - y)
        c = shade(base, edge) if e == 0 else base
        if ridge and e >= 1 and p.fw >= 4: c = mix(c, ridge, 0.35)
        return shade(c, 0.94 + 0.12 * hash01(p.x, p.y, p.fw, p.fh, len(p.bone)))
    return fn


def shell(base, line, cell=4):
    """Armour-shell grid pattern continuous across cubes."""
    def fn(p):
        x, y, z = p.p
        gx = (x % cell + cell) % cell; gy = (y % cell + cell) % cell; gz = (z % cell + cell) % cell
        lines = (gx < 1) + (gy < 1) + (gz < 1)
        c = base
        if lines >= 2: c = line
        elif lines == 1: c = mix(base, line, 0.45)
        return shade(c, 0.9 + 0.2 * noise3(x, y, z, 21, 2.0))
    return fn


def eye_dark(p):
    """Cute glossy black eye with a white highlight."""
    if p.face in ("top", "bottom", "back"): return "#141018"
    if p.x == 0 and p.y == 0: return "#ffffff"
    return "#141018"


def eye_color(iris, pupil="#0e0c10"):
    def fn(p):
        if p.face in ("top", "bottom", "back"): return shade(iris, 0.6)
        if p.fw >= 3 and p.fh >= 3:
            if abs(p.x + .5 - p.fw / 2) < 0.9 and abs(p.y + .5 - p.fh / 2) < p.fh / 2: return pupil
        elif p.fw == 2:
            return pupil if p.x == 1 else iris
        return iris
    return fn


def tooth(p):
    return shade("#f1ead6", 0.92 + 0.16 * noise3(*p.p, 91, 1.0))


def claw_paint(color="#2b2622"):
    return solid(color, 0.12, 87)


def flat(color):
    return lambda p: color


# ------------------------------------------------------------------ animation kits
def quad_anims(tail_bones=(), head="head", amp=32, freq=40, ears=(), extra_idle=None, extra_walk=None, legs=None,
               neck=None, bob_amp=0.4):
    fl, fr, bl, br = legs or ("leg_fl", "leg_fr", "leg_bl", "leg_br")
    walk = [quad_walk(fl, fr, bl, br, amp, freq)]
    if tail_bones:
        walk.append(swing({t: (0 if i % 2 == 0 else 180) for i, t in enumerate(tail_bones)}, 7, 1, freq))
    walk.append({"body": {"rotation": ["0", "0", f"math.sin(query.modified_distance_moved * {freq} + 0) * 1.5 * query.modified_move_speed"]}})
    if extra_walk: walk.append(extra_walk)
    idle = [bob("body", bob_amp, 80)]
    for i, t in enumerate(tail_bones):
        idle.append(sway(t, 6 + 2 * i, 40 - 3 * i, 1, i * 0.8))
    if head:
        idle.append({head: {"rotation": ["math.sin(query.life_time * 70) * 3", "math.sin(query.life_time * 37) * 7", "0"]}})
    for i, e in enumerate(ears):
        idle.append(sway(e, 6, 90, 2, i * 1.7))
    if extra_idle: idle.append(extra_idle)
    return {"walk": anim(merge(*walk)), "idle": anim(merge(*idle))}


def biped_anims(tail_bones=(), head="head", amp=34, freq=44, arms=(), extra_idle=None, extra_walk=None, legs=("leg_l", "leg_r"),
                bob_amp=0.5, neck=None):
    walk = [biped_walk(legs[0], legs[1], amp, freq)]
    if tail_bones:
        walk.append(swing({t: (0 if i % 2 == 0 else 180) for i, t in enumerate(tail_bones)}, 8, 1, freq))
    if arms:
        walk.append(swing({a: (0 if i % 2 == 0 else 180) for i, a in enumerate(arms)}, 14, 0, freq))
    if neck: walk.append(swing({neck: 0}, 5, 0, freq))
    if extra_walk: walk.append(extra_walk)
    idle = [bob("body", bob_amp, 85)]
    for i, t in enumerate(tail_bones):
        idle.append(sway(t, 5 + 3 * i, 40 - 3 * i, 1, i * 0.9))
    if head:
        idle.append({head: {"rotation": ["math.sin(query.life_time * 90) * 4", "math.sin(query.life_time * 47) * 8", "0"]}})
    for i, a in enumerate(arms):
        idle.append(sway(a, 6, 75, 0, i * 1.3))
    if extra_idle: idle.append(extra_idle)
    return {"walk": anim(merge(*walk)), "idle": anim(merge(*idle))}


def bite_anim(jaw="jaw", head="head", neck=None, amt=40):
    t = "variable.attack_time * 180"
    d = {head: {"rotation": [f"math.sin({t}) * 22", "0", "0"]}}
    if jaw: d[jaw] = {"rotation": [f"math.sin({t}) * {amt}", "0", "0"]}
    if neck: d[neck] = {"rotation": [f"math.sin({t}) * 14", "0", "0"]}
    return anim(d, loop=False)


# ------------------------------------------------------------------ finishing
def extent(bones):
    mx = mz = my = 0.0
    for b in bones:
        for c in b.get("cubes", []):
            o, s = c["o"], c["s"]
            r = 0
            if c.get("rot"):
                r = max(s) * 0.5
            mx = max(mx, abs(o[0]) + r, abs(o[0] + s[0]) + r)
            mz = max(mz, abs(o[2]) + r, abs(o[2] + s[2]) + r)
            my = max(my, o[1] + s[1] + r)
    return mx, my, mz


def finish(spec_id, name, egg, bones, skins, anims, play, behavior, glow_flag=False, margin=1.25):
    mx, my, mz = extent(bones)
    r = max(mx, mz) * 2 / 16 * margin + 0.6
    H = my / 16 * margin + 0.6
    spec = {
        "id": spec_id, "name": name, "egg": egg, "glow": glow_flag, "scale": 1.0,
        "visible": [math.ceil(r * 100) / 100, math.ceil(H * 100) / 100, math.floor(H / 2 * 100) / 100 - 0.01],
        "bones": bones, "skins": skins, "anims": anims, "play": play, "behavior": behavior,
    }
    return spec


STD_PLAY = [{"walk": "query.modified_move_speed > 0.02"}, "idle"]
STD_PLAY_ATK = [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"]
