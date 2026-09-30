"""Shared builders for the eggs-B mythical roster (specs/eggsb_*.py).  Not a spec module itself.
Units are model pixels (16 = 1 block), model faces -Z, ground y=0.  Cube sizes are ints, origins may be floats."""
import math
from lib import *


# ------------------------------------------------------------------ cubes
def C(o, s, skin=None, **kw):
    d = {"o": list(o), "s": list(s)}
    if skin: d["skin"] = skin
    d.update(kw)
    return d

def mirror(c):
    m = dict(c); m["o"] = [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]]; m["s"] = list(c["s"])
    if c.get("rot"):
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        pv = c.get("pivot", [0, 0, 0]); m["pivot"] = [-pv[0], pv[1], pv[2]]
    return m

def pair(c):
    return [c, mirror(c)]

def bone(name, parent, pivot, cubes, rotation=None):
    flat = []
    for c in cubes:
        if isinstance(c, list): flat.extend(c)
        else: flat.append(c)
    b = {"name": name, "parent": parent, "pivot": list(pivot), "cubes": flat}
    if rotation: b["rotation"] = rotation
    return b

def by(bones, name):
    return next(b for b in bones if b["name"] == name)

def add(bones, name, *cubes):
    for c in cubes:
        if isinstance(c, list): by(bones, name)["cubes"].extend(c)
        else: by(bones, name)["cubes"].append(c)

def eyes(x, y, front_z, skin="eye", size=2):
    """pair of eyes, x = inner edge distance from centre on +x side; protrude 0.5px."""
    return pair(C([x, y, front_z - 0.5], [size, size, 1], skin))


def side_eyes(face_x, y, z, skin="eye", size=2):
    """Eyes on the side faces of a head (horse-style); face_x = half head width."""
    c = C([face_x - 0.5, y, z], [1, size, size], skin)
    return pair(c)


# ------------------------------------------------------------------ painters
def coat(base, dark=None, light=None, under=None, under_y=None, seed=1, patch=4.0, fine=1.0, extra=None):
    dark = dark or shade(base, 0.72); light = light or shade(base, 1.18)
    def fn(p):
        x, y, z = p.p
        n = noise3(x * 1.7, y * 1.7, z * 1.1, seed, fine)
        m = noise3(x, y, z, seed + 7, patch)
        c = mix(dark, base, 0.35 + 0.65 * m)
        c = mix(c, light, max(0.0, m - 0.62) * 1.6)
        c = shade(c, 0.87 + 0.26 * n)
        if under is not None and (p.face == "bottom" or (under_y is not None and y < under_y)):
            c = mix(c, under, 0.85)
        if extra: c = extra(p, c) or c
        return c
    return fn

def scales(base, dark=None, light=None, cell=2.0, under=None, under_y=None, seed=1, extra=None):
    """Offset-grid scale/brick pattern, continuous across cubes."""
    dark = dark or shade(base, 0.7); light = light or shade(base, 1.2)
    def fn(p):
        x, y, z = p.p
        s = (x + z) * 0.95 / cell; v = y / cell
        row = math.floor(v); u = s + 0.5 * (row % 2)
        fu, fv = u - math.floor(u), v - row
        h = hash01(math.floor(u), row, seed)
        c = mix(base, light if h > 0.5 else dark, 0.25 + 0.35 * abs(h - 0.5) * 2)
        if fv < 0.18 or fu < 0.14: c = mix(c, dark, 0.7)
        elif fv > 0.75: c = shade(c, 0.94)
        if under is not None and (p.face == "bottom" or (under_y is not None and y < under_y)):
            c = mix(c, under, 0.85)
        if extra: c = extra(p, c) or c
        return c
    return fn

def solid(c, var=0.12, seed=3):
    def fn(p):
        return shade(c, 1 - var / 2 + var * noise3(p.p[0] * 1.5, p.p[1] * 1.5, p.p[2] * 1.5, seed, 1.0))
    return fn

def eye(iris="#3a2a10", pupil="#0a0a10", glint=True, white=None):
    def fn(p):
        if p.face not in ("front", "east", "west") or (p.face != "front" and p.d < 2 and p.w > 1): return shade(pupil, 1.0)
        if p.fw >= 3 and p.fh >= 3:
            cx, cy = p.fw / 2, p.fh / 2
            if abs(p.x + .5 - cx) < 1 and abs(p.y + .5 - cy) < 1: return pupil
            return white or iris
        if glint and p.x == 0 and p.y == 0: return "#ffffff"
        if p.y == p.fh - 1 and p.fh > 1: return iris
        return pupil
    return fn

def glow_eye(c="#ff3a2a"):
    return lambda p: glow(c)

def gl(c, var=0.1, seed=5):
    def fn(p):
        return glow(shade(c, 1 - var / 2 + var * noise3(p.p[0] * 2, p.p[1] * 2, p.p[2] * 2, seed, 1.0)))
    return fn

def face_detail(base_fn, nostril="#2a1a1a", mouth=None):
    """muzzle painter: nostrils on the front face (2 dark pixels near the top corners)."""
    def fn(p):
        c = base_fn(p)
        if p.face == "front" and p.fw >= 3 and p.y == max(0, p.fh // 2 - 1) and p.x in (1, p.fw - 2):
            return nostril
        if mouth and p.face == "front" and p.y == p.fh - 1: return mouth
        return c
    return fn


# ------------------------------------------------------------------ body plans
def leg(name, cx, cz, w, d, h, skin, foot_h=0, foot_skin=None, parent="body", top=None):
    """Leg hanging from y=top (default h) down to 0, pivot at the top."""
    top = h if top is None else top
    cubes = []
    if foot_h:
        cubes.append(C([cx - w / 2, 0, cz - d / 2], [w, foot_h, d], foot_skin or skin))
        cubes.append(C([cx - w / 2, foot_h, cz - d / 2], [w, h - foot_h, d], skin))
    else:
        cubes.append(C([cx - w / 2, 0, cz - d / 2], [w, h, d], skin))
    return bone(name, parent, [cx, top, cz], cubes)


def quad(bw, bh, bl, leg_h, lw, head, head_y, head_dz=0, skin="coat", leg_skin=None, foot_h=0,
         foot_skin="hoof", neck=None, head_skin=None, name_prefix="leg", leg_ld=None, leg_span=None):
    """Quadruped skeleton: body, head (+neck cube inside head bone), four legs.
    head = (hw,hh,hd); head_y = y of head bottom; head_dz shifts head along z (neg = forward).
    neck = (nw, nl, angle_deg) cube from body front-top."""
    top = leg_h + bh
    lsk = leg_skin or skin; hs = head_skin or skin
    hw, hh, hd = head
    fz = -bl / 2
    bones = [bone("body", None, [0, leg_h + bh / 2, 0], [C([-bw / 2, leg_h, -bl / 2], [bw, bh, bl], skin)])]
    hc = [C([-hw / 2, head_y, fz - hd + 2 + head_dz], [hw, hh, hd], hs)]
    if neck:
        nw, nl, ang = neck
        hc.append(C([-nw / 2, top - 3, fz - 1], [nw, nl, nw], skin, rot=[ang, 0, 0], pivot=[0, top - 3, fz + nw / 2]))
    bones.append(bone("head", "body", [0, top - 2, fz], hc))
    ld = leg_ld or lw
    lx = (leg_span if leg_span is not None else bw / 2 - lw / 2)
    zf = fz + ld / 2 + 0.0
    zb = bl / 2 - ld / 2
    for nm, sx, zz in (("fl", 1, zf), ("fr", -1, zf), ("bl", 1, zb), ("br", -1, zb)):
        bones.append(leg(f"{name_prefix}_{nm}", sx * lx, zz, lw, ld, leg_h, lsk, foot_h, foot_skin))
    return bones


def biped(bw, bh, bd, leg_h, lw, ld, arm_h, aw, ad, head, skin="body", head_skin=None, leg_skin=None, arm_skin=None,
          foot_h=0, foot_skin=None, leg_x=None, arm_dx=0, shoulder_drop=2, head_dy=0, head_dz=0, hand_h=0, hand_skin=None):
    """Humanoid skeleton: body, head, arm_l/arm_r (pivot at shoulder), leg_l/leg_r.  +x is the character's left."""
    top = leg_h + bh
    hw, hh, hd = head
    lx = leg_x if leg_x is not None else lw / 2
    bones = [bone("body", None, [0, leg_h + bh / 2, 0], [C([-bw / 2, leg_h, -bd / 2], [bw, bh, bd], skin)])]
    bones.append(bone("head", "body", [0, top, 0], [C([-hw / 2, top + head_dy, -hd / 2 + head_dz], [hw, hh, hd], head_skin or skin)]))
    ax = bw / 2 + aw / 2 + arm_dx
    for nm, s in (("l", 1), ("r", -1)):
        cubes = [C([s * ax - aw / 2, top - arm_h - shoulder_drop + 0, -ad / 2], [aw, arm_h, ad], arm_skin or skin)]
        if hand_h:
            cubes = [C([s * ax - aw / 2, top - arm_h - shoulder_drop, -ad / 2], [aw, hand_h, ad], hand_skin or arm_skin or skin),
                     C([s * ax - aw / 2, top - arm_h - shoulder_drop + hand_h, -ad / 2], [aw, arm_h - hand_h, ad], arm_skin or skin)]
        bones.append(bone(f"arm_{nm}", "body", [s * ax, top - shoulder_drop, 0], cubes))
    for nm, s in (("l", 1), ("r", -1)):
        bones.append(leg(f"leg_{nm}", s * lx, 0, lw, ld, leg_h, leg_skin or skin, foot_h, foot_skin, parent=None))
    return bones


def wing(name, parent, side, px, py, pz, span, chord, arm_skin, feather_skin, tip_skin=None, fingers=3, thick=1):
    """One wing bone extending along +x*side from the shoulder, feathers trail toward +z. Flap = rotate Z."""
    cubes = []
    aw = max(2, int(span * 0.55))
    cubes.append(C([px, py - 1, pz - 1], [aw, 2, 3], arm_skin))
    cubes.append(C([px + 1, py - 0.5, pz + 2], [span - 1, thick, chord], feather_skin))
    for i in range(fingers):
        ln = max(2, int((span - 2) * (1 - i * 0.16)))
        cubes.append(C([px + span - ln, py - 0.5 - 0.0, pz + 2 + chord + i * 3], [ln, thick, 3], tip_skin or feather_skin))
    if tip_skin:
        cubes.append(C([px + aw, py - 1, pz - 1], [span - aw, 1, 2], tip_skin))
    if side < 0:
        cubes = [mirror(c) for c in cubes]
    return bone(name, parent, [side * px, py, pz], cubes)


def bat_wing(name, parent, side, px, py, pz, span, drop, arm_skin, membrane):
    """Bat-style: arm + membrane sheet + finger struts."""
    cubes = [C([px, py - 1, pz - 1], [span, 2, 2], arm_skin),
             C([px + 1, py - 0.5, pz + 1], [span - 2, 1, drop], membrane)]
    for i in range(3):
        f = span - 2 - i * 2
        cubes.append(C([px + span - f, py - 0.5, pz + 1 + drop * (i + 1) // 3], [f, 1, 1], arm_skin))
    if side < 0: cubes = [mirror(c) for c in cubes]
    return bone(name, parent, [side * px, py, pz], cubes)


# ------------------------------------------------------------------ animation kits
def quad_anims(tail=None, tail_amp=10, walk_amp=38, head_bob=True, ears=(), freq=38.17, extra_idle=None, extra_walk=None,
               prefix="leg"):
    n = lambda s: f"{prefix}_{s}"
    walk = [quad_walk(n("fl"), n("fr"), n("bl"), n("br"), amp=walk_amp, freq=freq)]
    if tail: walk.append(sway(tail, amp=tail_amp, rate=60, axis=1))
    if extra_walk: walk.append(extra_walk)
    idle = [bob("body", 0.4, 80)]
    if tail: idle.append(sway(tail, amp=tail_amp, rate=40, axis=1))
    for i, e in enumerate(ears): idle.append(sway(e, amp=8, rate=70 + i * 13, axis=2, off=i * 1.7))
    if head_bob:
        idle.append({"head": {"rotation": ["math.sin(query.life_time * 60) * 3", "math.sin(query.life_time * 33) * 6", "0"]}})
    if extra_idle: idle.append(extra_idle)
    return {"walk": anim(merge(*walk)), "idle": anim(merge(*idle))}

def biped_anims(walk_amp=40, arm_amp=None, extra_walk=None, extra_idle=None, freq=38.17, prefix="leg", body_bob=0.3):
    l, r = f"{prefix}_l", f"{prefix}_r"
    aa = walk_amp * 0.8 if arm_amp is None else arm_amp
    walk = [biped_walk(l, r, amp=walk_amp, freq=freq), swing({"arm_l": 180, "arm_r": 0}, amp=aa, axis=0, freq=freq)]
    if extra_walk: walk.append(extra_walk)
    idle = [bob("body", body_bob, 80), sway("arm_l", 4, 70, axis=2), sway("arm_r", 4, 70, axis=2, off=3.1),
            {"head": {"rotation": ["math.sin(query.life_time * 60) * 3", "math.sin(query.life_time * 33) * 8", "0"]}}]
    if extra_idle: idle.append(extra_idle)
    return {"walk": anim(merge(*walk)), "idle": anim(merge(*idle))}

def flap_anim(wl, wr, amp=35, rate=300, extra=None):
    d = flap({wl: 1, wr: -1}, amp=amp, rate=rate)
    return anim(merge(d, extra or {}))


PLAY_WALK_IDLE = [{"walk": "query.modified_move_speed > 0.02"}, "idle"]
PLAY_FLY = [{"walk": "query.modified_move_speed > 0.02 && query.is_on_ground"},
            {"flap": "!query.is_on_ground"}, "idle"]


def fold(wl, wr, ang=65, amp=3, rate=70):
    """Resting wing pose (folded up over the back) with a slight breathing sway; use inside idle/walk."""
    return {wl: {"rotation": ["0", "0", f"{-ang} + math.sin(query.life_time * {rate}) * {amp}"]},
            wr: {"rotation": ["0", "0", f"{ang} - math.sin(query.life_time * {rate}) * {amp}"]}}


def with_visible(spec, margin=1.2):
    """Compute visible bounds from the cubes (ignores per-cube rotation, generous margin)."""
    xs = zs = ys = 0
    for b in spec["bones"]:
        flat = []
        for c in b.get("cubes", []):
            flat.extend(c) if isinstance(c, list) else flat.append(c)
        b["cubes"] = flat
        for c in b.get("cubes", []):
            o, s = c["o"], c["s"]
            xs = max(xs, abs(o[0]), abs(o[0] + s[0])); zs = max(zs, abs(o[2]), abs(o[2] + s[2])); ys = max(ys, o[1] + s[1])
    sc = spec.get("scale", 1.0)
    w = 2 * max(xs, zs) / 16 * sc + margin
    h = ys / 16 * sc + 0.6
    spec["visible"] = [round(w, 2), round(h, 2), round(h / 2 - 0.1, 2)]
    return spec
