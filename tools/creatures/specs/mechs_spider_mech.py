"""Arachno-Mech - hostile six-legged armored crawler with sensor dome.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

CHIT   = "#737982"
DARK   = "#43484e"
PLATE  = "#5f656d"
JOINT  = "#15181c"
PIST   = "#c2ccd2"
EYE    = "#ff2e2e"
EYE_H  = "#ffb0b0"
VENT   = "#ff7a1f"
RUST   = "#6d4527"
HAZ    = "#d8b24a"
BLADE  = "#9aa3ab"


def panel(v, period=10.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, z, period=10.0, r=0.6):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def metal(p, base=CHIT, dark=DARK, seed=11):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.0)
    c = mix(dark, base, 0.25 + 0.75 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 7, 1.1))
    if panel(x) or panel(z):
        c = shade(c, 0.55)
    if rivets(x, y, z):
        c = shade(c, 0.4)
    if p.face == "top":
        c = shade(c, 1.18)
    if p.face == "bottom":
        c = shade(c, 0.80)
    if hash01(x, y, z, seed + 3) > 0.95:
        c = shade(c, 1.32)
    if hash01(x, y, z, seed + 4) > 0.968:
        c = shade(c, 0.5)
    r = noise3(x, y, z, seed + 9, 1.7)
    if r > 0.80:
        c = mix(c, RUST, (r - 0.80) * 1.4)
    return c


def plate(p):
    return metal(p, PLATE, "#1b1f24", 21)


def joint(p):
    x, y, z = p.p
    return shade(mix(JOINT, "#2b3138", noise3(x, y, z, 61, 2.0)), 0.85 + 0.3 * noise3(x, y, z, 63, 1.0))


def piston(p):
    x, y, z = p.p
    c = mix("#8f9aa0", PIST, 0.35 + 0.65 * noise3(x, y, z, 51, 2.4))
    if abs((y % 3.0) - 1.5) < 0.7:
        c = shade(c, 0.5)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def eye(p):
    x, y, z = p.p
    c = mix("#8a0f0f", EYE, 0.3 + 0.7 * noise3(x, y, z, 71, 2.0))
    if abs((x % 2.0) - 1.0) < 0.5:
        c = shade(c, 0.6)
    return glow(c)


def ventglow(p):
    x, y, z = p.p
    return glow(mix("#ff6a12", "#ffd08a", 0.35 + 0.65 * noise3(x, y, z, 81, 1.4)))


def hazard(p):
    x, y, z = p.p
    s = math.sin((x + z) * 1.5)
    c = HAZ if s > 0 else "#15181c"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def blade(p):
    x, y, z = p.p
    c = mix("#5a636b", BLADE, 0.3 + 0.7 * noise3(x, y, z, 111, 2.0))
    if p.face == "top":
        c = shade(c, 1.3)
    if hash01(x, y, z, 113) > 0.9:
        c = shade(c, 1.25)
    return shade(c, 0.95)


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "chit")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- carapace body
body_cubes = [
    {"o": [-8, 12, -8], "s": [16, 10, 16], "skin": "chit"},
    {"o": [-7, 22, -7], "s": [14, 3, 14], "skin": "plate"},
    {"o": [-8, 10, -8], "s": [16, 3, 16], "skin": "joint"},
    {"o": [-6, 20, -6], "s": [12, 3, 12], "skin": "plate"},
    {"o": [-2, 25, -2], "s": [4, 3, 4], "skin": "joint"},
    {"o": [-1, 28, -1], "s": [2, 3, 2], "skin": "piston"},
]
sym(body_cubes, {"o": [8, 13, -7], "s": [2, 7, 12], "skin": "plate", "rot": [0, 0, -12], "pivot": [8, 18, -7]})
sym(body_cubes, {"o": [7, 19, -4], "s": [2, 4, 8], "skin": "hazard"})
sym(body_cubes, {"o": [-1.5, 22, 6], "s": [3, 3, 3], "skin": "joint"})

# ----------------------------------------------------------------- sensor head
head_cubes = [
    {"o": [-5, 13, -15], "s": [10, 8, 8], "skin": "chit"},
    {"o": [-4, 20, -14], "s": [8, 2, 6], "skin": "plate"},
    {"o": [-3, 16, -17], "s": [6, 5, 3], "skin": "eye"},
    {"o": [-4, 13, -16], "s": [8, 3, 2], "skin": "joint"},
]
sym(head_cubes, {"o": [3, 17, -15], "s": [3, 3, 5], "skin": "piston"})
sym(head_cubes, {"o": [-1.5, 21, -13], "s": [3, 2, 2], "skin": "vent_glow"})

mand_l = [
    {"o": [3, 11, -17], "s": [2, 5, 9], "skin": "blade", "rot": [0, 0, -18], "pivot": [4, 15, -17]},
    {"o": [3, 9, -21], "s": [1, 3, 5], "skin": "blade", "rot": [0, 0, -24], "pivot": [4, 11, -19]},
]
mand_r = [
    {"o": [-5, 11, -17], "s": [2, 5, 9], "skin": "blade", "rot": [0, 0, 18], "pivot": [-4, 15, -17]},
    {"o": [-4, 9, -21], "s": [1, 3, 5], "skin": "blade", "rot": [0, 0, 24], "pivot": [-4, 11, -19]},
]

# ----------------------------------------------------------------- abdomen pod
abdomen_cubes = [
    {"o": [-6, 11, 8], "s": [12, 10, 12], "skin": "chit"},
    {"o": [-5, 21, 9], "s": [10, 3, 10], "skin": "plate"},
    {"o": [-5, 10, 9], "s": [10, 3, 10], "skin": "joint"},
    {"o": [-4, 8, 19], "s": [8, 5, 3], "skin": "joint"},
]
sym(abdomen_cubes, {"o": [6, 11, 8], "s": [2, 11, 13], "skin": "plate", "rot": [0, 0, -10], "pivot": [6, 16, 9]})
sym(abdomen_cubes, {"o": [8, 13, 9], "s": [1, 6, 9], "skin": "vent_glow"})
sym(abdomen_cubes, {"o": [-3, 16, 19], "s": [6, 3, 2], "skin": "hazard"})

# ----------------------------------------------------------------- legs (6, two segments each)
def leg_up(hip_x, hip_z, yaw):
    return [{"o": [hip_x, 11, hip_z - 3], "s": [12, 5, 5], "skin": "chit",
             "rot": [0, yaw, 46], "pivot": [hip_x, 18, hip_z]},
            {"o": [hip_x + 2, 13, hip_z - 3], "s": [9, 2, 6], "skin": "plate",
             "rot": [0, yaw, 46], "pivot": [hip_x, 18, hip_z]},
            {"o": [hip_x + 3, 10, hip_z - 3], "s": [4, 4, 5], "skin": "joint",
             "rot": [0, yaw, 46], "pivot": [hip_x, 18, hip_z]}]

def leg_lo(knee_x, knee_z):
    return [{"o": [knee_x - 2, 0, knee_z - 2], "s": [5, 10, 5], "skin": "chit"},
            {"o": [knee_x - 2, 6, knee_z - 2], "s": [4, 4, 5], "skin": "joint"},
            {"o": [knee_x - 2.5, 0, knee_z - 4], "s": [6, 2, 6], "skin": "plate"},
            {"o": [knee_x - 1.5, 0, knee_z - 5], "s": [4, 1, 3], "skin": "blade"}]

def mirror(cubes):
    out = []
    for c in cubes:
        m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c["skin"]}
        if "rot" in c:
            m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
            m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
        out.append(m)
    return out

leg_fl_up = leg_up(6, -6, -16)
leg_ml_up = leg_up(6, 0, 0)
leg_bl_up = leg_up(6, 6, 16)
leg_fl_lo = leg_lo(15, -6)
leg_ml_lo = leg_lo(15, 0)
leg_bl_lo = leg_lo(15, 6)

leg_fr_up = mirror(leg_fl_up)
leg_mr_up = mirror(leg_ml_up)
leg_br_up = mirror(leg_bl_up)
leg_fr_lo = mirror(leg_fl_lo)
leg_mr_lo = mirror(leg_ml_lo)
leg_br_lo = mirror(leg_bl_lo)

bones = [
    {"name": "body", "parent": None, "pivot": [0, 17, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 17, -8], "cubes": head_cubes},
    {"name": "mand_l", "parent": "head", "pivot": [4, 15, -17], "cubes": mand_l},
    {"name": "mand_r", "parent": "head", "pivot": [-4, 15, -17], "cubes": mand_r},
    {"name": "abdomen", "parent": "body", "pivot": [0, 16, 8], "cubes": abdomen_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [6, 18, -6], "cubes": leg_fl_up},
    {"name": "leg_fl_lo", "parent": "leg_fl", "pivot": [14, 10, -6], "cubes": leg_fl_lo},
    {"name": "leg_ml", "parent": "body", "pivot": [6, 18, 0], "cubes": leg_ml_up},
    {"name": "leg_ml_lo", "parent": "leg_ml", "pivot": [14, 10, 0], "cubes": leg_ml_lo},
    {"name": "leg_bl", "parent": "body", "pivot": [6, 18, 6], "cubes": leg_bl_up},
    {"name": "leg_bl_lo", "parent": "leg_bl", "pivot": [14, 10, 6], "cubes": leg_bl_lo},
    {"name": "leg_fr", "parent": "body", "pivot": [-6, 18, -6], "cubes": leg_fr_up},
    {"name": "leg_fr_lo", "parent": "leg_fr", "pivot": [-14, 10, -6], "cubes": leg_fr_lo},
    {"name": "leg_mr", "parent": "body", "pivot": [-6, 18, 0], "cubes": leg_mr_up},
    {"name": "leg_mr_lo", "parent": "leg_mr", "pivot": [-14, 10, 0], "cubes": leg_mr_lo},
    {"name": "leg_br", "parent": "body", "pivot": [-6, 18, 6], "cubes": leg_br_up},
    {"name": "leg_br_lo", "parent": "leg_br", "pivot": [-14, 10, 6], "cubes": leg_br_lo},
]

def knee(name, phase):
    return {name: {"rotation": ["0", "0", f"math.cos(query.modified_distance_moved * 40 + {phase}) * 16 * query.modified_move_speed"]}}

anims = {
    "walk": anim(merge(
        hex_walk(["leg_fl", "leg_fr", "leg_mr", "leg_ml", "leg_bl", "leg_br"], amp=22, freq=40),
        knee("leg_fl_lo", 0), knee("leg_ml_lo", 180), knee("leg_bl_lo", 0),
        knee("leg_fr_lo", 180), knee("leg_mr_lo", 0), knee("leg_br_lo", 180),
        {"body": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 20)) * 0.6 * query.modified_move_speed", "0"]}},
        {"abdomen": {"rotation": ["0", "math.cos(query.modified_distance_moved * 20) * 4 * query.modified_move_speed", "0"]}},
    )),
    "idle": anim(merge(
        bob("body", amp=0.5, rate=55),
        sway("head", amp=9, rate=25, axis=1),
        {"mand_l": {"rotation": ["math.sin(query.life_time * 60) * 5", "0", "0"]}},
        {"mand_r": {"rotation": ["math.sin(query.life_time * 60 + 0.8) * 5", "0", "0"]}},
        sway("abdomen", amp=3, rate=30, axis=1, off=1.2),
        {"leg_ml": {"rotation": ["0", "math.sin(query.life_time * 40) * 3", "0"]}},
        {"leg_mr": {"rotation": ["0", "math.sin(query.life_time * 40 + 3.14) * 3", "0"]}},
    )),
    "attack": anim(merge(
        {"mand_l": {"rotation": ["0", "math.sin(variable.attack_time * 180) * -40", "0"]}},
        {"mand_r": {"rotation": ["0", "math.sin(variable.attack_time * 180) * 40", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "0", "0"]}},
        {"body": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.0"]}},
        {"abdomen": {"rotation": ["math.sin(variable.attack_time * 180) * -8", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "spider_mech",
    "name": "Arachno-Mech",
    "egg": ("#3c424a", "#ff2e2e"),
    "glow": True,
    "scale": 1.0,
    "visible": [4.5, 3.0, 1.0],
    "bones": bones,
    "skins": {"default": metal, "chit": metal, "plate": plate, "joint": joint, "piston": piston,
              "eye": eye, "vent_glow": ventglow, "hazard": hazard, "blade": blade},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 60, "speed": 0.3, "damage": 6, "box": [2.2, 1.4],
        "climb": True, "family": ["mech", "spider"],
        "loot": [("minecraft:iron_ingot", 1, 3), ("minecraft:redstone", 1, 2), ("minecraft:copper_ingot", 0, 2)],
        "sound": ("silverfish", [0.5, 0.7]),
        "xp": 10,
    },
}
