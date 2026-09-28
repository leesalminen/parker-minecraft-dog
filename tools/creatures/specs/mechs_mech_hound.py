"""Mech Hound - small tameable robot dog companion.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#838c96"
DARK   = "#484f57"
PLATE  = "#69717b"
JOINT  = "#15181c"
PIST   = "#c2ccd2"
VISOR  = "#4fd8ff"
VISOR_H= "#d8f7ff"
VENT   = "#ff7a1f"
RUST   = "#6d4527"
ACC    = "#e0862a"
BADGE  = "#e8e4d8"


def panel(v, period=10.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, z, period=10.0, r=0.6):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def metal(p, base=STEEL, dark=DARK, seed=11):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 2.6)
    c = mix(dark, base, 0.25 + 0.75 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 7, 1.1))
    if panel(x) or panel(z):
        c = shade(c, 0.72)
    if rivets(x, y, z):
        c = shade(c, 0.62)
    if p.face == "top":
        c = shade(c, 1.18)
    if p.face == "bottom":
        c = shade(c, 0.80)
    if hash01(x, y, z, seed + 3) > 0.95:
        c = shade(c, 1.32)
    if hash01(x, y, z, seed + 4) > 0.968:
        c = shade(c, 0.5)
    r = noise3(x, y, z, seed + 9, 1.5)
    if r > 0.80:
        c = mix(c, RUST, (r - 0.80) * 1.4)
    return c


def plate(p):
    return metal(p, PLATE, "#1c2127", 21)


def joint(p):
    x, y, z = p.p
    return shade(mix(JOINT, "#2b3138", noise3(x, y, z, 61, 1.8)), 0.85 + 0.3 * noise3(x, y, z, 63, 1.0))


def piston(p):
    x, y, z = p.p
    c = mix("#8f9aa0", PIST, 0.35 + 0.65 * noise3(x, y, z, 51, 2.0))
    if abs((y % 2.5) - 1.25) < 0.6:
        c = shade(c, 0.5)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def visor(p):
    x, y, z = p.p
    c = mix("#0f5f7a", VISOR, 0.3 + 0.7 * noise3(x, y, z, 71, 1.8))
    if abs((x % 2.0) - 1.0) < 0.5:
        c = shade(c, 0.55)
    return glow(c)


def ventglow(p):
    x, y, z = p.p
    return glow(mix("#ff6a12", "#ffd08a", 0.35 + 0.65 * noise3(x, y, z, 81, 1.2)))


def accent(p):
    x, y, z = p.p
    c = mix(ACC, "#7a4a10", 0.3 + 0.7 * noise3(x, y, z, 85, 1.6))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 87, 1.0))


def badge(p):
    x, y, z = p.p
    c = BADGE
    if y < 9.4 or y > 13.6 or z < -3.6 or z > 1.6:
        c = "#1b1f24"
    elif y > 11.4 and abs(z + 1.0) < 1.2:
        c = "#1f6fa0"
    return shade(c, 0.93 + 0.14 * noise3(x, y, z, 99, 1.0))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "steel")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- torso
body_cubes = [
    {"o": [-5, 8, -7], "s": [10, 8, 14], "skin": "steel"},
    {"o": [-4, 7, -6], "s": [8, 2, 12], "skin": "plate"},
    {"o": [-4, 15, -6], "s": [8, 3, 12], "skin": "plate"},
    {"o": [-3, 16, -5], "s": [6, 2, 9], "skin": "joint"},
    {"o": [-4, 9, 7], "s": [8, 6, 3], "skin": "plate"},
    {"o": [-2, 12, 7], "s": [4, 4, 3], "skin": "vent_glow"},
    {"o": [-1, 15, -1], "s": [2, 2, 6], "skin": "piston"},
    {"o": [-2, 16, 4], "s": [4, 3, 5], "skin": "plate"},
    {"o": [-1.5, 16, 7], "s": [3, 2, 3], "skin": "joint"},
    {"o": [-1, 17, 5], "s": [2, 1, 2], "skin": "vent_glow"},
]
sym(body_cubes, {"o": [5, 9, -5], "s": [2, 7, 11], "skin": "plate", "rot": [0, 0, -10], "pivot": [5, 13, -5]})
sym(body_cubes, {"o": [6.1, 9, -2], "s": [1, 4, 4], "skin": "badge"})
sym(body_cubes, {"o": [-3, 14, 4], "s": [6, 3, 2], "skin": "accent"})
sym(body_cubes, {"o": [2, 12, -6], "s": [2, 2, 3], "skin": "joint"})

# ----------------------------------------------------------------- head
head_cubes = [
    {"o": [-4, 10, -13], "s": [8, 7, 8], "skin": "steel"},
    {"o": [-3, 16, -12], "s": [6, 2, 6], "skin": "plate"},
    {"o": [-3, 13, -14], "s": [6, 3, 1], "skin": "visor"},
    {"o": [-3, 10, -14], "s": [6, 3, 2], "skin": "joint"},
    {"o": [-2, 9, -15], "s": [4, 3, 4], "skin": "joint"},
    {"o": [-1.5, 9, -17], "s": [3, 2, 2], "skin": "joint"},
]
sym(head_cubes, {"o": [2, 15, -12], "s": [2, 4, 3], "skin": "plate", "rot": [0, 0, -18], "pivot": [2, 15, -12]})
sym(head_cubes, {"o": [-2, 17, -11], "s": [4, 1, 1], "skin": "accent"})

antenna_cubes = [
    {"o": [-1, 15, 8], "s": [2, 2, 6], "skin": "piston"},
    {"o": [-1, 15, 14], "s": [2, 2, 2], "skin": "accent"},
    {"o": [-1, 16, 15.5], "s": [2, 1, 2], "skin": "vent_glow"},
]

# ----------------------------------------------------------------- legs (4, articulated)
def leg_up(hip_x, hip_z):
    return [{"o": [hip_x, 4, hip_z - 3], "s": [3, 9, 4], "skin": "steel"},
            {"o": [hip_x + 2.5, 6, hip_z - 3], "s": [2, 6, 4], "skin": "plate"},
            {"o": [hip_x + 1, 9, hip_z - 4], "s": [3, 3, 4], "skin": "joint"},
            {"o": [hip_x + 0.5, 5, hip_z + 1], "s": [2, 7, 2], "skin": "piston"}]

def leg_lo(knee_x, knee_z):
    return [{"o": [knee_x, 0, knee_z - 3], "s": [3, 5, 3], "skin": "steel"},
            {"o": [knee_x - 0.5, 0, knee_z - 4], "s": [4, 3, 5], "skin": "plate"},
            {"o": [knee_x, 0, knee_z - 3], "s": [2, 3, 3], "skin": "joint"}]

leg_fl_up = leg_up(2.5, -5)
leg_fr_up = leg_up(-5.5, -5)
leg_bl_up = leg_up(2.5, 5)
leg_br_up = leg_up(-5.5, 5)
leg_fl_lo = leg_lo(2.5, -5)
leg_fr_lo = leg_lo(-5.5, -5)
leg_bl_lo = leg_lo(2.5, 5)
leg_br_lo = leg_lo(-5.5, 5)

bones = [
    {"name": "body", "parent": None, "pivot": [0, 11, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 13, -7], "cubes": head_cubes},
    {"name": "tail", "parent": "body", "pivot": [0, 15, 7], "cubes": antenna_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [4, 11, -4], "cubes": leg_fl_up},
    {"name": "leg_fl_lo", "parent": "leg_fl", "pivot": [4, 4, -4], "cubes": leg_fl_lo},
    {"name": "leg_fr", "parent": "body", "pivot": [-4, 11, -4], "cubes": leg_fr_up},
    {"name": "leg_fr_lo", "parent": "leg_fr", "pivot": [-4, 4, -4], "cubes": leg_fr_lo},
    {"name": "leg_bl", "parent": "body", "pivot": [4, 11, 5], "cubes": leg_bl_up},
    {"name": "leg_bl_lo", "parent": "leg_bl", "pivot": [4, 4, 5], "cubes": leg_bl_lo},
    {"name": "leg_br", "parent": "body", "pivot": [-4, 11, 5], "cubes": leg_br_up},
    {"name": "leg_br_lo", "parent": "leg_br", "pivot": [-4, 4, 5], "cubes": leg_br_lo},
]

anims = {
    "walk": anim(merge(
        quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", amp=32, freq=46),
        {"leg_fl_lo": {"rotation": ["math.cos(query.modified_distance_moved * 46 + 180) * 18 * query.modified_move_speed", "0", "0"]}},
        {"leg_fr_lo": {"rotation": ["math.cos(query.modified_distance_moved * 46) * 18 * query.modified_move_speed", "0", "0"]}},
        {"leg_bl_lo": {"rotation": ["math.cos(query.modified_distance_moved * 46) * 18 * query.modified_move_speed", "0", "0"]}},
        {"leg_br_lo": {"rotation": ["math.cos(query.modified_distance_moved * 46 + 180) * 18 * query.modified_move_speed", "0", "0"]}},
        {"body": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 23)) * 0.5 * query.modified_move_speed", "0"]}},
        {"head": {"rotation": ["math.cos(query.modified_distance_moved * 46) * 3 * query.modified_move_speed", "0", "0"]}},
        {"tail": {"rotation": ["0", "math.cos(query.modified_distance_moved * 23) * 6 * query.modified_move_speed", "0"]}},
    )),
    "idle": anim(merge(
        bob("body", amp=0.3, rate=80),
        sway("tail", amp=16, rate=140, axis=1, off=0.4),
        {"head": {"rotation": ["math.sin(query.life_time * 60) * 2", "math.sin(query.life_time * 28) * 22", "0"]}},
        {"leg_fl": {"rotation": ["0", "0", "math.sin(query.life_time * 95) * 4"]}},
        {"leg_fr": {"rotation": ["0", "0", "math.sin(query.life_time * 95 + 1.6) * 4"]}},
    )),
    "attack": anim(merge(
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 26", "0", "0"]}},
        {"body": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * -1.6"]}},
        {"leg_fl": {"rotation": ["math.sin(variable.attack_time * 180) * -16", "0", "0"]}},
        {"leg_fr": {"rotation": ["math.sin(variable.attack_time * 180) * -16", "0", "0"]}},
        {"tail": {"rotation": ["0", "math.sin(variable.attack_time * 180) * -30", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "mech_hound",
    "name": "Mech Hound",
    "egg": ("#5f6873", "#4fd8ff"),
    "glow": True,
    "scale": 1.0,
    "visible": [2.5, 1.8, 0.6],
    "bones": bones,
    "skins": {"default": metal, "steel": metal, "plate": plate, "joint": joint, "piston": piston,
              "visor": visor, "vent_glow": ventglow, "accent": accent, "badge": badge},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "companion",
        "health": 24, "speed": 0.35, "damage": 5, "box": [0.8, 1.1],
        "family": ["mech", "dog"],
        "tame_items": ["minecraft:iron_ingot"],
        "ranged": True, "range": 12, "projectile": "minecraft:arrow",
        "loot": [("minecraft:iron_ingot", 1, 2), ("minecraft:redstone", 0, 2)],
        "sound": ("wolf", [0.6, 0.8]),
        "xp": 5,
        "spawn": {"biomes": ["plains"], "weight": 1, "herd": [1, 1]},
    },
}
