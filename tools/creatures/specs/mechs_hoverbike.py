"""Hover Bike - fast rideable sci-fi speeder with twin thrusters.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#7f8892"
DARK   = "#464b53"
PLATE  = "#69717b"
JOINT  = "#15181c"
PIST   = "#c2ccd2"
EXH    = "#ff7a1f"
EXH_H  = "#ffe0a0"
GLASS  = "#5fd0ff"
RUST   = "#6d4527"
HAZ    = "#d8b24a"
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
    n = noise3(x, y, z, seed, 3.0)
    c = mix(dark, base, 0.26 + 0.74 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 7, 1.1))
    if panel(x) or panel(z):
        c = shade(c, 0.72)
    if rivets(x, y, z):
        c = shade(c, 0.62)
    if p.face == "top":
        c = shade(c, 1.16)
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
    return metal(p, PLATE, "#1c2127", 21)


def gun(p):
    return metal(p, "#60666d", "#2a2f35", 31)


def joint(p):
    x, y, z = p.p
    return shade(mix(JOINT, "#2b3138", noise3(x, y, z, 61, 2.0)), 0.85 + 0.3 * noise3(x, y, z, 63, 1.0))


def piston(p):
    x, y, z = p.p
    c = mix("#8f9aa0", PIST, 0.35 + 0.65 * noise3(x, y, z, 51, 2.2))
    if abs((y % 3.0) - 1.5) < 0.7:
        c = shade(c, 0.5)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def glass(p):
    x, y, z = p.p
    c = mix("#10465e", GLASS, 0.3 + 0.7 * noise3(x, y, z, 71, 2.0))
    if abs((x % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.6)
    return glow(c)


def exhaust(p):
    x, y, z = p.p
    return glow(mix(EXH, EXH_H, 0.3 + 0.7 * noise3(x, y, z, 81, 1.3)))


def hazard(p):
    x, y, z = p.p
    s = math.sin((x + z) * 1.4)
    c = HAZ if s > 0 else "#15181c"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def accent(p):
    x, y, z = p.p
    c = mix(ACC, "#7a4a10", 0.3 + 0.7 * noise3(x, y, z, 85, 1.6))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 87, 1.0))


def badge(p):
    x, y, z = p.p
    c = BADGE
    if y < 5.4 or y > 9.6 or z < -7.6 or z > -2.4:
        c = "#1b1f24"
    elif y > 7.4 and abs(z + 5.0) < 1.2:
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


# ----------------------------------------------------------------- fuselage
body_cubes = [
    {"o": [-4, 4, -12], "s": [8, 8, 24], "skin": "steel"},
    {"o": [-3, 3, -11], "s": [6, 2, 22], "skin": "plate"},
    {"o": [-2, 12, -9], "s": [4, 2, 18], "skin": "plate"},
    {"o": [-3, 5, 9], "s": [6, 8, 5], "skin": "joint"},
    {"o": [-2, 12, 9], "s": [4, 2, 4], "skin": "joint"},
]
sym(body_cubes, {"o": [4, 5, -9], "s": [1, 6, 18], "skin": "accent"})
sym(body_cubes, {"o": [-3, 2, -7], "s": [3, 1, 13], "skin": "vent_glow"})
sym(body_cubes, {"o": [-3, 2, 3], "s": [3, 1, 8], "skin": "vent_glow"})
sym(body_cubes, {"o": [3, 8, -12], "s": [2, 3, 4], "skin": "joint"})
sym(body_cubes, {"o": [-2.5, 6, 12], "s": [5, 4, 2], "skin": "hazard"})
sym(body_cubes, {"o": [3.1, 6, -6], "s": [1, 4, 4], "skin": "badge"})

# ----------------------------------------------------------------- nose
nose_cubes = [
    {"o": [-3, 5, -20], "s": [6, 6, 9], "skin": "steel", "rot": [14, 0, 0], "pivot": [0, 8, -12]},
    {"o": [-2, 4, -24], "s": [4, 4, 5], "skin": "plate", "rot": [14, 0, 0], "pivot": [0, 8, -12]},
    {"o": [-2, 9, -19], "s": [4, 2, 8], "skin": "plate", "rot": [14, 0, 0], "pivot": [0, 8, -12]},
    {"o": [-1.5, 4, -26], "s": [3, 3, 3], "skin": "joint", "rot": [14, 0, 0], "pivot": [0, 8, -12]},
]
sym(nose_cubes, {"o": [-3.5, 5, -18], "s": [1, 4, 6], "skin": "hazard", "rot": [14, 0, 0], "pivot": [0, 8, -12]})

# ----------------------------------------------------------------- forward fins
fin_l = [
    {"o": [3, 6, -18], "s": [2, 3, 10], "skin": "plate", "rot": [0, 0, -22], "pivot": [4, 9, -14]},
    {"o": [3, 6, -10], "s": [2, 2, 5], "skin": "accent", "rot": [0, 0, -22], "pivot": [4, 9, -14]},
]
fin_r = [
    {"o": [-5, 6, -18], "s": [2, 3, 10], "skin": "plate", "rot": [0, 0, 22], "pivot": [-4, 9, -14]},
    {"o": [-5, 6, -10], "s": [2, 2, 5], "skin": "accent", "rot": [0, 0, 22], "pivot": [-4, 9, -14]},
]

# ----------------------------------------------------------------- saddle + cockpit
seat_cubes = [
    {"o": [-3, 11, -7], "s": [6, 3, 10], "skin": "joint"},
    {"o": [-2, 13, -5], "s": [4, 2, 6], "skin": "plate"},
    {"o": [-3, 10, 3], "s": [6, 2, 3], "skin": "plate"},
]
handle_cubes = [
    {"o": [-5, 13, -10], "s": [10, 2, 2], "skin": "joint"},
    {"o": [-1, 12, -10], "s": [2, 5, 3], "skin": "piston"},
]
sym(handle_cubes, {"o": [4, 13, -11], "s": [2, 2, 3], "skin": "accent"})
windscreen_cubes = [
    {"o": [-3, 14, -12], "s": [6, 5, 1], "skin": "glass", "rot": [-20, 0, 0], "pivot": [0, 14, -12]},
    {"o": [-3, 13, -12], "s": [6, 2, 2], "skin": "joint"},
]

# ----------------------------------------------------------------- thrusters
thruster_l = [
    {"o": [1, 4, 11], "s": [5, 6, 7], "skin": "steel"},
    {"o": [1.5, 5, 17], "s": [4, 4, 4], "skin": "gun"},
    {"o": [2, 6, 20], "s": [3, 3, 2], "skin": "exhaust"},
    {"o": [1, 3, 12], "s": [5, 2, 6], "skin": "hazard"},
]
thruster_r = [
    {"o": [-6, 4, 11], "s": [5, 6, 7], "skin": "steel"},
    {"o": [-5.5, 5, 17], "s": [4, 4, 4], "skin": "gun"},
    {"o": [-5, 6, 20], "s": [3, 3, 2], "skin": "exhaust"},
    {"o": [-6, 3, 12], "s": [5, 2, 6], "skin": "hazard"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 8, 0], "cubes": body_cubes},
    {"name": "nose", "parent": "body", "pivot": [0, 8, -12], "cubes": nose_cubes},
    {"name": "fin_l", "parent": "body", "pivot": [4, 9, -14], "cubes": fin_l},
    {"name": "fin_r", "parent": "body", "pivot": [-4, 9, -14], "cubes": fin_r},
    {"name": "seat", "parent": "body", "pivot": [0, 11, -7], "cubes": seat_cubes},
    {"name": "handlebar", "parent": "body", "pivot": [0, 12, -10], "cubes": handle_cubes},
    {"name": "windscreen", "parent": "handlebar", "pivot": [0, 14, -12], "cubes": windscreen_cubes},
    {"name": "thruster_l", "parent": "body", "pivot": [3, 7, 13], "cubes": thruster_l},
    {"name": "thruster_r", "parent": "body", "pivot": [-3, 7, 13], "cubes": thruster_r},
]

anims = {
    "move": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 180) * 0.35", "0"]}},
        {"body": {"rotation": ["math.cos(query.modified_distance_moved * 22) * 3 * query.modified_move_speed", "0",
                               "math.sin(query.modified_distance_moved * 22) * 7 * query.modified_move_speed"]}},
        {"fin_l": {"rotation": ["0", "0", "math.sin(query.life_time * 260) * 10"]}},
        {"fin_r": {"rotation": ["0", "0", "math.sin(query.life_time * 260 + 1.5) * 10"]}},
        {"nose": {"rotation": ["math.cos(query.modified_distance_moved * 22) * 2 * query.modified_move_speed", "0", "0"]}},
        {"thruster_l": {"rotation": ["math.sin(query.life_time * 300) * 2", "0", "0"]}},
        {"thruster_r": {"rotation": ["math.sin(query.life_time * 300 + 0.8) * 2", "0", "0"]}},
    )),
    "idle": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 150) * 0.3", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 75) * 1.5", "0", "0"]}},
        {"fin_l": {"rotation": ["0", "0", "math.sin(query.life_time * 220) * 7"]}},
        {"fin_r": {"rotation": ["0", "0", "math.sin(query.life_time * 220 + 1.2) * 7"]}},
        {"thruster_l": {"rotation": ["math.sin(query.life_time * 320) * 1.5", "0", "0"]}},
        {"thruster_r": {"rotation": ["math.sin(query.life_time * 320 + 0.6) * 1.5", "0", "0"]}},
        {"handlebar": {"rotation": ["math.sin(query.life_time * 90) * 1.2", "0", "0"]}},
        {"windscreen": {"rotation": ["math.sin(query.life_time * 130) * 0.8", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -12", "0", "0"]}},
        {"nose": {"rotation": ["math.sin(variable.attack_time * 180) * 8", "0", "0"]}},
        {"fin_l": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 24"]}},
        {"fin_r": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * -24"]}},
        {"thruster_l": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 1.6"]}},
        {"thruster_r": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 1.6"]}},
    ), loop=False),
}

SPEC = {
    "id": "hoverbike",
    "name": "Hover Bike",
    "egg": ("#59626d", "#ff7a1f"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.5, 2.2, 0.6],
    "bones": bones,
    "skins": {"default": metal, "steel": metal, "plate": plate, "gun": gun, "joint": joint,
              "piston": piston, "glass": glass, "exhaust": exhaust, "vent_glow": exhaust,
              "hazard": hazard, "accent": accent, "badge": badge},
    "anims": anims,
    "play": [{"move": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 40, "speed": 0.5, "damage": 4, "box": [1.2, 1.4],
        "hover": True, "fly_speed": 0.5, "family": ["mech"],
        "ride": {"seats": [[0, 0.85, -0.35]], "jump": 0.5},
        "loot": [("minecraft:iron_ingot", 2, 4), ("minecraft:redstone", 1, 3), ("minecraft:copper_ingot", 1, 2)],
        "sound": ("golem", [0.9, 1.2]),
        "xp": 6,
    },
}
