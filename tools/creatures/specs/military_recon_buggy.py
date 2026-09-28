"""Dune Recon Buggy - small fast rideable 4-wheel buggy with roll cage and light bar.
Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#8a929a"
DARK   = "#3c4249"
PLATE  = "#9aa2a9"
STRUCT = "#4e545b"
TUBE   = "#5b626a"
RUBBER = "#1a1d21"
HAZ    = "#d8b24a"
SAND   = "#a58a5c"
OLIVE  = "#5c6a44"
LIGHT  = "#fff0c4"
OPTIC  = "#8fd8ff"
VENT   = "#ff8a2a"
HOT    = "#ffe0a0"


def armor(p, base=STEEL, dark=DARK, seed=11, period=14.0, edge=1.0):
    x, y, z = p.p
    c = mix(base, dark, 0.18 + 0.55 * noise3(x, y, z, seed, 3.2))
    if (x % period) < edge or (y % period) < edge or (z % period) < edge:
        c = shade(c, 0.64)
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    if dx < 0.8 and dz < 0.8:
        c = shade(c, 0.8)
    h = hash01(x, y, z, seed)
    if h > 0.93:
        c = shade(c, 0.75)
    elif h < 0.05:
        c = mix(c, "#7a6a52", 0.5)
    return shade(c, 0.92 + 0.18 * noise3(x, y, z, seed + 3, 1.0))


def steel(p):  return armor(p, STEEL, DARK, 11)
def plate(p):  return armor(p, PLATE, "#22272d", 21, 11.0)
def struct(p): return armor(p, STRUCT, "#191d22", 31, 8.0)


def tube(p):
    x, y, z = p.p
    c = mix(TUBE, "#20252b", 0.2 + 0.6 * noise3(x, y, z, 37, 2.4))
    if abs((x % 3.0) - 1.5) < 0.4:
        c = shade(c, 0.7)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 39, 1.0))


def wheel(p):
    x, y, z = p.p
    if p.face in ("east", "west", "north", "south"):
        dx, dy = p.x - p.fw / 2.0, p.y - p.fh / 2.0
        r = math.hypot(dx, dy)
        a = math.atan2(dy, dx)
        if r > 4.9:
            c = mix("#14171a", "#2c3137", 0.3 + 0.5 * noise3(x, y, z, 7, 2.0))
            if ((a + math.pi) / (math.pi / 4)) % 1.0 < 0.5:
                c = shade(c, 0.6)
        else:
            c = mix("#7c828a", "#2e3238", 0.3 + 0.4 * noise3(x, y, z, 9, 2.0))
            k = ((a + math.pi) / (math.pi / 2)) % 1.0
            if k < 0.2 or k > 0.8:
                c = shade(c, 0.5)
            if r < 1.4:
                c = shade(c, 0.4)
    else:
        c = mix("#141719", "#262a2f", 0.3 + 0.6 * noise3(x, y, z, 11, 2.0))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 13, 1.0))


def hazard(p):
    x, y, z = p.p
    c = HAZ if math.sin(x * 0.7 + z * 1.6) > 0 else "#15181c"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def sand(p):
    x, y, z = p.p
    c = mix(SAND, "#6f5a3a", 0.25 + 0.6 * noise3(x, y, z, 51, 2.6))
    if abs((z % 6.0) - 3.0) < 0.8:
        c = shade(c, 0.85)
    return shade(c, 0.92 + 0.16 * noise3(x, y, z, 53, 1.0))


def jerry(p):
    x, y, z = p.p
    c = mix(OLIVE, "#333b26", 0.3 + 0.6 * noise3(x, y, z, 71, 3.0))
    if abs((x % 4.0) - 2.0) < 0.5:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 73, 1.0))


def seat(p):
    x, y, z = p.p
    c = mix("#2b2f34", "#16191c", 0.3 + 0.6 * noise3(x, y, z, 77, 3.0))
    if y > 13.5:
        c = mix("#3a3f45", "#1d2125", 0.4)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 79, 1.0))


def light(p): return glow(LIGHT)


def optic(p):
    x, y, z = p.p
    return glow(mix("#1f6f9c", OPTIC, 0.4 + 0.6 * noise3(x, y, z, 87, 2.0)))


def exhaust(p):
    x, y, z = p.p
    return glow(shade(mix(VENT, HOT, 0.25 + 0.7 * noise3(x, y, z, 93, 1.6)),
                      0.85 + 0.3 * noise3(x, y, z, 95, 1.0)))


def mc(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c["skin"]}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def sym(cubes, c):
    cubes.append(c)
    cubes.append(mc(c))


# ----------------------------------------------------------------- chassis
body_cubes = [
    {"o": [-9, 6, -18], "s": [18, 3, 36], "skin": "steel"},
    {"o": [-9, 5, -16], "s": [18, 2, 30], "skin": "struct"},
    {"o": [-7, 9, -10], "s": [14, 2, 18], "skin": "plate"},
    {"o": [-7, 11, -9], "s": [14, 3, 2], "skin": "plate"},
    {"o": [-1, 9, -2], "s": [2, 5, 8], "skin": "struct"},
    {"o": [-6, 9, 10], "s": [12, 7, 8], "skin": "steel"},
    {"o": [-6, 16, 10], "s": [12, 2, 8], "skin": "plate"},
    {"o": [-7, 9, 4], "s": [14, 4, 5], "skin": "struct"},
    {"o": [-10, 7, -20], "s": [20, 3, 3], "skin": "hazard"},
    {"o": [-9, 8, -18], "s": [18, 6, 2], "skin": "steel"},
    {"o": [-9, 8, 16], "s": [18, 6, 2], "skin": "steel"},
]
sym(body_cubes, {"o": [9, 8, -18], "s": [2, 6, 36], "skin": "steel"})
sym(body_cubes, {"o": [9, 10, -15], "s": [4, 3, 9], "skin": "sand"})
sym(body_cubes, {"o": [9, 10, 9], "s": [4, 3, 9], "skin": "sand"})
sym(body_cubes, {"o": [9, 7, -14], "s": [3, 3, 8], "skin": "struct"})
sym(body_cubes, {"o": [9, 7, 10], "s": [3, 3, 8], "skin": "struct"})
sym(body_cubes, {"o": [-9, 6, -18], "s": [1, 1, 36], "skin": "hazard"})

# ----------------------------------------------------------------- seats
seat_cubes = [
    {"o": [-6, 11, -6], "s": [4, 4, 4], "skin": "seat"},
    {"o": [1, 11, -6], "s": [4, 4, 4], "skin": "seat"},
    {"o": [-6, 14, -9], "s": [4, 3, 2], "skin": "seat"},
    {"o": [1, 14, -9], "s": [4, 3, 2], "skin": "seat"},
]

# ----------------------------------------------------------------- roll cage
rollcage_cubes = [
    {"o": [-8, 14, -9], "s": [1, 7, 1], "skin": "tube"},
    {"o": [7, 14, -9], "s": [1, 7, 1], "skin": "tube"},
    {"o": [-8, 14, 4], "s": [1, 7, 1], "skin": "tube"},
    {"o": [7, 14, 4], "s": [1, 7, 1], "skin": "tube"},
    {"o": [-8, 20, -9], "s": [1, 1, 14], "skin": "tube"},
    {"o": [7, 20, -9], "s": [1, 1, 14], "skin": "tube"},
    {"o": [-8, 19, -9], "s": [16, 1, 1], "skin": "tube"},
    {"o": [-8, 19, 4], "s": [16, 1, 1], "skin": "tube"},
    {"o": [-1, 14, 4], "s": [1, 7, 8], "skin": "tube", "rot": [24, 0, 0], "pivot": [0, 14, 4]},
]

# ----------------------------------------------------------------- light bar
lightbar_cubes = [
    {"o": [-6, 21, -9], "s": [12, 2, 3], "skin": "struct"},
    {"o": [-5, 22, -10], "s": [4, 1, 1], "skin": "light"},
    {"o": [-1, 22, -10], "s": [2, 1, 1], "skin": "light"},
    {"o": [1, 22, -10], "s": [4, 1, 1], "skin": "light"},
]

# ----------------------------------------------------------------- spare + jerry cans + bull bar + exhaust + antenna
spare_cubes = [
    {"o": [-6, 6, 19], "s": [12, 12, 6], "skin": "wheel"},
    {"o": [-4, 8, 18], "s": [8, 8, 2], "skin": "struct"},
]
jerry_cubes = [
    {"o": [-8, 14, 17], "s": [3, 5, 3], "skin": "jerry"},
    {"o": [-8, 19, 17], "s": [3, 1, 3], "skin": "struct"},
]
sym(jerry_cubes, {"o": [5, 14, 17], "s": [3, 5, 3], "skin": "jerry"})
bullbar_cubes = [
    {"o": [-9, 8, -22], "s": [18, 2, 2], "skin": "tube"},
    {"o": [-9, 12, -22], "s": [18, 2, 2], "skin": "tube"},
]
sym(bullbar_cubes, {"o": [-9, 8, -22], "s": [2, 8, 2], "skin": "tube"})
sym(bullbar_cubes, {"o": [-6, 10, -22], "s": [1, 6, 1], "skin": "tube"})
exhaust_cubes = [
    {"o": [6, 12, 17], "s": [2, 6, 2], "skin": "struct"},
    {"o": [5.5, 18, 16.5], "s": [3, 1, 3], "skin": "exhaust"},
]
antenna_cubes = [
    {"o": [-9, 14, 6], "s": [2, 2, 2], "skin": "struct"},
    {"o": [-8.5, 16, 6.5], "s": [1, 7, 1], "skin": "tube"},
    {"o": [-8.5, 23, 6.5], "s": [1, 1, 1], "skin": "optic"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 10, 0], "cubes": body_cubes},
    {"name": "seats", "parent": "body", "pivot": [0, 11, -6], "cubes": seat_cubes},
    {"name": "rollcage", "parent": "body", "pivot": [0, 14, 0], "cubes": rollcage_cubes},
    {"name": "lightbar", "parent": "rollcage", "pivot": [0, 21, -6], "cubes": lightbar_cubes},
    {"name": "spare", "parent": "body", "pivot": [0, 12, 22], "cubes": spare_cubes},
    {"name": "jerry", "parent": "body", "pivot": [0, 16, 18], "cubes": jerry_cubes},
    {"name": "bullbar", "parent": "body", "pivot": [0, 10, -21], "cubes": bullbar_cubes},
    {"name": "exhaust", "parent": "body", "pivot": [7, 15, 18], "cubes": exhaust_cubes},
    {"name": "antenna", "parent": "body", "pivot": [-8.5, 14, 6.5], "cubes": antenna_cubes},
]
for name, x, z in (("wheel_fl", 13, -14), ("wheel_fr", -13, -14),
                   ("wheel_rl", 13, 14), ("wheel_rr", -13, 14)):
    bones.append({"name": name, "parent": "body", "pivot": [x, 6, z], "cubes": [
        {"o": [x - 3, 0, z - 6], "s": [6, 12, 12], "skin": "wheel"},
        {"o": [x - 4, 3, z - 3], "s": [8, 6, 6], "skin": "struct"},
    ]})

WHEELS = ["wheel_fl", "wheel_fr", "wheel_rl", "wheel_rr"]


def spin(names, rate=150):
    return {n: {"rotation": [f"query.modified_distance_moved * {rate}", "0", "0"]} for n in names}


anims = {
    "move": anim(merge(
        spin(WHEELS),
        {"body": {"position": ["0", "math.sin(query.life_time * 260) * 0.3", "0"]}},
        {"body": {"rotation": ["math.cos(query.modified_distance_moved * 40) * 3 * query.modified_move_speed",
                               "0", "math.sin(query.modified_distance_moved * 40) * 5 * query.modified_move_speed"]}},
        {"rollcage": {"rotation": ["math.sin(query.life_time * 260 + 0.4) * 2", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 320) * 14"]}},
        {"exhaust": {"position": ["0", "math.sin(query.life_time * 300) * 0.2", "0"]}},
        {"jerry": {"rotation": ["math.sin(query.life_time * 260) * 3", "0", "0"]}},
        {"spare": {"rotation": ["math.sin(query.life_time * 260 + 0.8) * 2.5", "0", "0"]}},
        {"bullbar": {"rotation": ["math.sin(query.life_time * 260) * 2", "0", "0"]}},
    )),
    "idle": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 160) * 0.12", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 70) * 1.2", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 120) * 8"]}},
        {"lightbar": {"rotation": ["math.sin(query.life_time * 90) * 1.5", "0", "0"]}},
        {"exhaust": {"position": ["0", "math.sin(query.life_time * 200) * 0.1", "0"]}},
        {"rollcage": {"rotation": ["math.sin(query.life_time * 110) * 0.8", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -14", "0", "0"]}},
        {"body": {"position": ["0", "math.sin(variable.attack_time * 180) * 0.6", "0"]}},
        {"rollcage": {"rotation": ["math.sin(variable.attack_time * 180) * 6", "0", "0"]}},
        {"bullbar": {"rotation": ["math.sin(variable.attack_time * 180) * 10", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 24"]}},
        {"jerry": {"rotation": ["math.sin(variable.attack_time * 180) * 8", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "military_recon_buggy",
    "name": "Dune Recon Buggy",
    "egg": ("#a58a5c", "#8fd8ff"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.4, 2.0, 0.75],
    "bones": bones,
    "skins": {"default": steel, "steel": steel, "plate": plate, "struct": struct, "tube": tube,
              "wheel": wheel, "hazard": hazard, "sand": sand, "jerry": jerry, "seat": seat,
              "light": light, "optic": optic, "exhaust": exhaust},
    "anims": anims,
    "play": [{"move": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 40, "speed": 0.45, "damage": 3, "box": [1.9, 1.5],
        "knockback_resist": 0.3, "family": ["mech", "vehicle"],
        "ride": {"seats": [[-0.25, 0.72, -0.3], [0.2, 0.72, -0.3]], "jump": 0.5},
        "loot": [("minecraft:iron_ingot", 2, 4), ("minecraft:copper_ingot", 1, 3)],
        "sound": ("golem", [0.8, 1.05]),
        "xp": 8,
    },
}
