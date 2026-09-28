"""Probe Droid - hostile hovering sensor sphere with dangling articulated arms.  Model faces -Z, y up."""
import math
from lib import *

METAL  = "#6f767f"
METAL_D= "#3f454c"
DARK   = "#22262b"
LIGHT  = "#b8bec6"
RED    = "#ff2a20"
RED_H  = "#ffb0a0"
BLUE   = "#6fd0ff"
PIPE   = "#565c64"


def panel(v, period=8.0, w=0.5):
    d = v % period
    return d < w or d > period - w


def rivets(x, z, period=8.0, r=0.55):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def paint(p, base, dark, seed):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.6)
    c = mix(dark, base, 0.28 + 0.72 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 5, 1.1))
    if panel(x) or panel(z):
        c = shade(c, 0.74)
    if rivets(x, z):
        c = shade(c, 0.58)
    if hash01(x, y, z, seed + 2) > 0.955:
        c = shade(c, 1.30)
    if hash01(x, y, z, seed + 3) > 0.970:
        c = shade(c, 0.45)
    if p.face == "top":
        c = shade(c, 1.12)
    if p.face == "bottom":
        c = shade(c, 0.78)
    return c


def metal(p):
    return paint(p, METAL, METAL_D, 11)


def dark(p):
    x, y, z = p.p
    c = mix("#141719", DARK, 0.3 + 0.7 * noise3(x, y, z, 31, 3.2))
    if abs((z % 4.0) - 2.0) < 0.7:
        c = shade(c, 0.65)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 33, 1.2))


def light(p):
    return paint(p, LIGHT, "#6f767f", 41)


def pipe(p):
    x, y, z = p.p
    c = mix("#3a4048", PIPE, 0.3 + 0.7 * noise3(x, y, z, 51, 3.0))
    if abs((y % 2.0) - 1.0) < 0.5:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.2))


def redeye(p):
    x, y, z = p.p
    return glow(mix(RED_H, RED, 0.25 + 0.75 * noise3(x, y, z, 61, 2.2)))


def bluelight(p):
    x, y, z = p.p
    return glow(mix("#dff4ff", BLUE, 0.3 + 0.7 * noise3(x, y, z, 63, 2.6)))


def mir(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "metal")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def sym(cubes, c):
    cubes.append(c)
    cubes.append(mir(c))


# ---------------------------------------------------------------- body shell (sphere, centre y=20, R=11)
body_cubes = [
    {"o": [-11, 15, -11], "s": [22, 10, 22], "skin": "metal"},
    {"o": [-8.5, 11, -8.5], "s": [17, 4, 17], "skin": "metal"},
    {"o": [-4.5, 9, -4.5], "s": [9, 2, 9], "skin": "dark"},
    {"o": [-8.5, 25, -8.5], "s": [17, 4, 17], "skin": "metal"},
    {"o": [-4.5, 29, -4.5], "s": [9, 2, 9], "skin": "dark"},
    # equator armour bands
    {"o": [-11.5, 18, -11.5], "s": [23, 2, 23], "skin": "dark"},
    {"o": [-11.5, 22, -11.5], "s": [23, 2, 23], "skin": "dark"},
    {"o": [-9, 16, -9], "s": [18, 6, 18], "skin": "light"},
    # greebles / ports
    {"o": [9, 19, -3], "s": [3, 4, 6], "skin": "pipe"},
    {"o": [-12, 19, -3], "s": [3, 4, 6], "skin": "pipe"},
    {"o": [-3, 30, -2], "s": [6, 2, 4], "skin": "dark"},
    {"o": [6, 26, 6], "s": [3, 3, 3], "skin": "pipe"},
    {"o": [-8, 26, 6], "s": [3, 3, 3], "skin": "pipe"},
    {"o": [-2, 10, -8], "s": [4, 3, 3], "skin": "dark"},
]
sym(body_cubes, {"o": [4, 16, -11.5], "s": [3, 4, 2], "skin": "bluelight"})
sym(body_cubes, {"o": [-8, 21, -11], "s": [4, 2, 2], "skin": "bluelight"})
sym(body_cubes, {"o": [9, 24, 3], "s": [3, 4, 3], "skin": "dark"})
sym(body_cubes, {"o": [7, 11, 7], "s": [3, 3, 3], "skin": "pipe"})

# ---------------------------------------------------------------- sensor eye (front, tracks target)
head_cubes = [
    {"o": [-6, 16, -11.6], "s": [12, 7, 1], "skin": "dark"},
    {"o": [-5, 17, -12.6], "s": [10, 5, 1], "skin": "redeye"},
    {"o": [-2, 19, -13.1], "s": [4, 1, 1], "skin": "light"},
    {"o": [-6.5, 16, -11.2], "s": [13, 8, 1], "skin": "dark"},
]
sym(head_cubes, {"o": [-7, 16, -11.6], "s": [1, 7, 2], "skin": "light"})

# ---------------------------------------------------------------- dish antenna (rotating)
dish_cubes = [
    {"o": [-1, 31, -1], "s": [2, 3, 2], "skin": "pipe"},
    {"o": [-1.5, 33, -1.5], "s": [3, 1, 3], "skin": "dark"},
    {"o": [-5, 33.5, -5], "s": [10, 1, 10], "skin": "metal", "rot": [22, 0, 0], "pivot": [0, 34, 0]},
    {"o": [-3, 34, -3], "s": [6, 1, 6], "skin": "dark", "rot": [22, 0, 0], "pivot": [0, 34, 0]},
    {"o": [-1, 35, -1], "s": [2, 3, 2], "skin": "pipe", "rot": [22, 0, 0], "pivot": [0, 34, 0]},
    {"o": [-0.5, 38, -0.5], "s": [1, 1, 1], "skin": "bluelight", "rot": [22, 0, 0], "pivot": [0, 34, 0]},
]

# ---------------------------------------------------------------- 5 dangling articulated arms
R = 8.0
arms = {}
arm_bones = []
for i in range(5):
    th = math.radians(90 + i * 72)
    cx, cz = R * math.cos(th), R * math.sin(th)
    tilt = [8 * math.sin(th), 0, -8 * math.cos(th)]
    seg1 = [
        {"o": [cx - 1, 5, cz - 1], "s": [2, 6, 2], "skin": "pipe", "rot": tilt, "pivot": [cx, 11, cz]},
        {"o": [cx - 1, 9, cz - 1], "s": [2, 2, 2], "skin": "dark"},
    ]
    seg2 = [
        {"o": [cx - 1, 0, cz - 1], "s": [2, 5, 2], "skin": "pipe", "rot": tilt, "pivot": [cx, 5, cz]},
        {"o": [cx - 1.5, 4, cz - 1.5], "s": [3, 1, 3], "skin": "dark"},
    ]
    claw = [
        {"o": [cx - 1.5, 0, cz - 1.5], "s": [3, 1, 3], "skin": "dark"},
        {"o": [cx - 0.5, 0, cz - 2.5], "s": [1, 2, 1], "skin": "light"},
        {"o": [cx - 0.5, 0, cz + 1.5], "s": [1, 2, 1], "skin": "light"},
    ]
    arms[i] = (seg1, seg2, claw)
    arm_bones += [
        {"name": f"arm{i}", "parent": "body", "pivot": [cx, 11, cz], "cubes": seg1},
        {"name": f"arm{i}b", "parent": f"arm{i}", "pivot": [cx, 5, cz], "cubes": seg2},
        {"name": f"arm{i}c", "parent": f"arm{i}b", "pivot": [cx, 0, cz], "cubes": claw},
    ]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 20, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 20, 0], "cubes": head_cubes},
    {"name": "dish", "parent": "body", "pivot": [0, 31, 0], "cubes": dish_cubes},
] + arm_bones

arm_sway = {}
for i in range(5):
    arm_sway[f"arm{i}"] = {"rotation": ["math.sin(query.life_time * 30 + %d) * 9" % (i * 1.3), "0",
                                          "math.cos(query.life_time * 26 + %d) * 7" % (i * 1.7)]}
    arm_sway[f"arm{i}b"] = {"rotation": ["math.sin(query.life_time * 34 + %d) * 12" % (i * 2.1), "0",
                                            "math.cos(query.life_time * 28 + %d) * 9" % (i * 2.5)]}
    arm_sway[f"arm{i}c"] = {"rotation": ["math.sin(query.life_time * 40 + %d) * 10" % (i * 2.9), "0", "0"]}

trail = {}
for i in range(5):
    trail[f"arm{i}"] = {"rotation": ["query.modified_move_speed * 14 + math.cos(query.modified_distance_moved * 22 + %d) * 6 * query.modified_move_speed" % (i * 40), "0", "0"]}
    trail[f"arm{i}b"] = {"rotation": ["query.modified_move_speed * 16 + math.cos(query.modified_distance_moved * 22 + %d) * 9 * query.modified_move_speed" % (i * 40 + 90), "0", "0"]}

attack_arms = {}
for i in range(5):
    attack_arms[f"arm{i}"] = {"rotation": ["math.sin(variable.attack_time * 180) * -46", "0", "0"]}
    attack_arms[f"arm{i}b"] = {"rotation": ["math.sin(variable.attack_time * 180) * -30", "0", "0"]}

anims = {
    "walk": anim(merge(
        {"body": {"rotation": ["query.modified_move_speed * 12 + math.cos(query.modified_distance_moved * 20) * 5 * query.modified_move_speed", "0", "0"]}},
        {"dish": {"rotation": ["0", "query.modified_distance_moved * 5", "0"]}},
        trail,
    )),
    "idle": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 55) * 1.6", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 55) * 3", "0", "math.cos(query.life_time * 40) * 2"]}},
        {"dish": {"rotation": ["math.sin(query.life_time * 33) * 6", "math.sin(query.life_time * 41) * 55", "0"]}},
        {"head": {"rotation": ["math.sin(query.life_time * 27) * 4", "0", "0"]}},
        arm_sway,
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -16", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * -6", "0", "0"]}},
        attack_arms,
        {"dish": {"rotation": ["math.sin(variable.attack_time * 180) * -20", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "probe_droid",
    "name": "Probe Droid",
    "egg": ("#6f767f", "#ff2a20"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.0, 3.2, 1.3],
    "bones": bones,
    "skins": {"default": metal, "metal": metal, "dark": dark, "light": light, "pipe": pipe,
              "redeye": redeye, "bluelight": bluelight},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 30, "speed": 0.22, "damage": 4, "box": [1.0, 1.4],
        "hover": True, "ranged": True, "range": 20, "projectile": "minecraft:arrow",
        "family": ["droid", "probe"],
        "loot": [("minecraft:iron_ingot", 1, 3), ("minecraft:redstone", 1, 3), ("minecraft:copper_ingot", 1, 2)],
        "sound": ("vex", [0.45, 0.65]),
        "xp": 8,
    },
}
