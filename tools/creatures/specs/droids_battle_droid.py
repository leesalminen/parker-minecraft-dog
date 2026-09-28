"""Battle Droid - thin tan/brown hostile biped trooper with blaster rifle.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

TAN    = "#c8b184"
TAN_D  = "#9d8557"
BROWN  = "#6a5236"
BROWN_D= "#463625"
DARK   = "#37301f"
GUN    = "#575c61"
GUN_D  = "#2c3035"
EYE    = "#ffd24a"


def panel(v, period=9.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, period=9.0, r=0.6):
    dx = min(x % period, period - x % period)
    dy = min(y % period, period - y % period)
    return dx < r and dy < r


def paint(p, base, dark, seed):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.4)
    c = mix(dark, base, 0.28 + 0.72 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 5, 1.1))
    if panel(x) or panel(y):
        c = shade(c, 0.76)
    if rivets(x, y):
        c = shade(c, 0.58)
    if hash01(x, y, z, seed + 2) > 0.955:
        c = shade(c, 1.24)
    if hash01(x, y, z, seed + 3) > 0.972:
        c = shade(c, 0.5)
    if p.face == "top":
        c = shade(c, 1.13)
    if p.face == "bottom":
        c = shade(c, 0.80)
    return c


def tan(p):
    return paint(p, TAN, TAN_D, 11)


def brown(p):
    return paint(p, BROWN, BROWN_D, 21)


def dark(p):
    x, y, z = p.p
    c = mix("#211c13", DARK, 0.3 + 0.7 * noise3(x, y, z, 31, 3.0))
    if abs((z % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 33, 1.2))


def gun(p):
    x, y, z = p.p
    c = mix(GUN_D, GUN, 0.3 + 0.7 * noise3(x, y, z, 41, 3.6))
    if abs((z % 6.0) - 3.0) < 0.7:
        c = shade(c, 0.7)
    if hash01(x, y, z, 45) > 0.96:
        c = shade(c, 1.3)
    return shade(c, 0.92 + 0.16 * noise3(x, y, z, 43, 1.1))


def eye(p):
    x, y, z = p.p
    return glow(mix("#fff0b0", EYE, 0.35 + 0.65 * noise3(x, y, z, 51, 2.4)))


def stripe(p):
    x, y, z = p.p
    c = mix("#7d2b20", "#d8452f", 0.4 + 0.6 * noise3(x, y, z, 71, 2.4))
    if math.sin((x + z) * 1.3) > 0:
        c = shade(c, 0.62)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 73, 1.2))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "tan")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


def mir(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "tan")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def mirror(cubes):
    return [mir(c) for c in cubes]


# ---------------------------------------------------------------- legs
foot_l = [
    {"o": [1, 0, -4], "s": [4, 2, 9], "skin": "tan"},
    {"o": [1, 0, -4], "s": [4, 2, 3], "skin": "brown"},
]
shin_l = [
    {"o": [1.5, 2, -2], "s": [3, 8, 4], "skin": "tan"},
    {"o": [1.5, 3, -2.5], "s": [3, 2, 1], "skin": "brown"},
    {"o": [1.5, 8, -2.5], "s": [3, 2, 1], "skin": "brown"},
]
thigh_l = [
    {"o": [1.5, 10, -2], "s": [3, 7, 4], "skin": "tan"},
    {"o": [1.5, 14, -2.5], "s": [3, 2, 1], "skin": "brown"},
    {"o": [4.5, 11, -1.5], "s": [1, 5, 3], "skin": "dark"},
]
foot_r, shin_r, thigh_r = mirror(foot_l), mirror(shin_l), mirror(thigh_l)

# ---------------------------------------------------------------- pelvis
pelvis_cubes = [
    {"o": [-4, 16, -3], "s": [8, 5, 6], "skin": "tan"},
    {"o": [-3.5, 16, -3.5], "s": [7, 2, 1], "skin": "brown"},
    {"o": [-2, 20, -2], "s": [4, 1, 4], "skin": "dark"},
]
sym(pelvis_cubes, {"o": [-3.5, 17, -3], "s": [7, 2, 6], "skin": "dark"})
sym(pelvis_cubes, {"o": [3, 17, -2.5], "s": [1, 3, 5], "skin": "brown"})

# ---------------------------------------------------------------- torso
torso_cubes = [
    {"o": [-3.5, 20, -2.5], "s": [7, 8, 5], "skin": "tan"},
    {"o": [-3, 21, -4], "s": [6, 5, 2], "skin": "brown"},
    {"o": [-2.5, 23, -4.6], "s": [5, 2, 1], "skin": "stripe"},
    {"o": [-3.5, 20, -2.5], "s": [7, 2, 1], "skin": "brown"},
    {"o": [-3.5, 24, -2.5], "s": [7, 2, 1], "skin": "brown"},
    {"o": [-2.5, 22, 2.5], "s": [5, 5, 3], "skin": "brown"},
    {"o": [-2, 23, 5.5], "s": [4, 3, 1], "skin": "dark"},
    {"o": [-1, 21, -4.6], "s": [2, 2, 1], "skin": "dark"},
    {"o": [-3, 27.5, -2.5], "s": [6, 1, 5], "skin": "dark"},
]
sym(torso_cubes, {"o": [3, 24, -2], "s": [2, 4, 4], "skin": "brown", "rot": [0, 0, -10], "pivot": [4, 28, -2]})
sym(torso_cubes, {"o": [-3, 20.5, -4.5], "s": [2, 4, 1], "skin": "brown"})

# ---------------------------------------------------------------- neck + head
neck_cubes = [
    {"o": [-1, 28, -1], "s": [2, 4, 2], "skin": "brown"},
    {"o": [-1.5, 29, -1.5], "s": [3, 1, 3], "skin": "dark"},
]
head_cubes = [
    {"o": [-2.5, 31, -2], "s": [5, 6, 5], "skin": "tan"},
    {"o": [-2, 32, -7], "s": [4, 3, 6], "skin": "tan"},
    {"o": [-2.5, 36, -1], "s": [5, 1, 4], "skin": "brown"},
    {"o": [-2, 31.5, -6.6], "s": [4, 1, 1], "skin": "brown"},
    {"o": [-2, 34.5, -2], "s": [4, 1, 5], "skin": "brown"},
    {"o": [-1, 37, -0.5], "s": [1, 3, 1], "skin": "dark"},
    {"o": [-0.5, 40, -0.5], "s": [1, 1, 1], "skin": "eye"},
]
sym(head_cubes, {"o": [0.4, 33.6, -7.3], "s": [1, 2, 1], "skin": "eye"})
sym(head_cubes, {"o": [-2.5, 33, -2], "s": [5, 1, 1], "skin": "dark"})

# ---------------------------------------------------------------- arms
arm_l_up = [
    {"o": [4, 20, -1], "s": [3, 7, 3], "skin": "tan"},
    {"o": [4, 26, -1], "s": [3, 2, 4], "skin": "brown"},
]
arm_l_fore = [
    {"o": [4, 13, -1], "s": [3, 7, 3], "skin": "tan"},
    {"o": [4, 19, -1.5], "s": [3, 2, 1], "skin": "brown"},
]
arm_l_hand = [
    {"o": [4, 11, -2], "s": [3, 3, 5], "skin": "dark"},
]
arm_r_up, arm_r_fore, arm_r_hand = mirror(arm_l_up), mirror(arm_l_fore), mirror(arm_l_hand)

# ---------------------------------------------------------------- blaster rifle (held in right hand)
rifle_cubes = [
    {"o": [-6.5, 12.5, -8], "s": [3, 3, 10], "skin": "gun"},
    {"o": [-6, 13, -16], "s": [2, 2, 8], "skin": "gun"},
    {"o": [-6.5, 12.5, -18], "s": [3, 3, 2], "skin": "gun"},
    {"o": [-6.5, 15.5, -6], "s": [3, 2, 4], "skin": "gun"},
    {"o": [-6.5, 11, -3], "s": [3, 2, 3], "skin": "dark"},
    {"o": [-6.5, 12.5, 2], "s": [3, 3, 3], "skin": "brown"},
    {"o": [-6, 14.5, -15], "s": [2, 1, 1], "skin": "eye"},
]

bones = [
    {"name": "pelvis", "parent": None, "pivot": [0, 17, 0], "cubes": pelvis_cubes},
    {"name": "torso", "parent": "pelvis", "pivot": [0, 20, 0], "cubes": torso_cubes},
    {"name": "neck", "parent": "torso", "pivot": [0, 28, 0], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 30, 0], "cubes": head_cubes},
    {"name": "arm_l_up", "parent": "torso", "pivot": [5.5, 27, 0], "cubes": arm_l_up},
    {"name": "arm_l_fore", "parent": "arm_l_up", "pivot": [5.5, 20, 0], "cubes": arm_l_fore},
    {"name": "arm_l_hand", "parent": "arm_l_fore", "pivot": [5.5, 13, 0], "cubes": arm_l_hand},
    {"name": "arm_r_up", "parent": "torso", "pivot": [-5.5, 27, 0], "cubes": arm_r_up},
    {"name": "arm_r_fore", "parent": "arm_r_up", "pivot": [-5.5, 20, 0], "cubes": arm_r_fore},
    {"name": "arm_r_hand", "parent": "arm_r_fore", "pivot": [-5.5, 13, 0], "cubes": arm_r_hand},
    {"name": "rifle", "parent": "arm_r_hand", "pivot": [-5.5, 13, 0], "cubes": rifle_cubes},
    {"name": "thigh_l", "parent": "pelvis", "pivot": [3, 17, 0], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [3, 10, 0], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [3, 2, 0], "cubes": foot_l},
    {"name": "thigh_r", "parent": "pelvis", "pivot": [-3, 17, 0], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-3, 10, 0], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-3, 2, 0], "cubes": foot_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=34, freq=40),
        {"shin_l": {"rotation": ["math.cos(query.modified_distance_moved * 40 + 180) * 22 * query.modified_move_speed", "0", "0"]}},
        {"shin_r": {"rotation": ["math.cos(query.modified_distance_moved * 40) * 22 * query.modified_move_speed", "0", "0"]}},
        {"foot_l": {"rotation": ["math.cos(query.modified_distance_moved * 40 + 90) * 12 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["math.cos(query.modified_distance_moved * 40 + 270) * 12 * query.modified_move_speed", "0", "0"]}},
        {"pelvis": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 20)) * 1.4 * query.modified_move_speed", "0"]}},
        {"torso": {"rotation": ["math.cos(query.modified_distance_moved * 40) * 4 * query.modified_move_speed", "0", "math.cos(query.modified_distance_moved * 20) * 5 * query.modified_move_speed"]}},
        {"arm_l_up": {"rotation": ["math.cos(query.modified_distance_moved * 40) * 12 * query.modified_move_speed", "0", "0"]}},
        {"arm_r_up": {"rotation": ["math.cos(query.modified_distance_moved * 40 + 180) * 8 * query.modified_move_speed", "0", "0"]}},
        {"neck": {"rotation": ["math.cos(query.modified_distance_moved * 40) * 3 * query.modified_move_speed", "0", "0"]}},
    )),
    "idle": anim(merge(
        sway("neck", amp=5, rate=32, axis=0),
        sway("torso", amp=2, rate=28, axis=0),
        {"head": {"rotation": ["0", "math.sin(query.life_time * 22) * 8", "0"]}},
        {"arm_r_up": {"rotation": ["math.sin(query.life_time * 30 + 1.0) * 3", "0", "0"]}},
        {"rifle": {"rotation": ["math.sin(query.life_time * 30 + 1.0) * 2", "0", "0"]}},
        {"head": {"rotation": ["math.sin(query.life_time * 55) * 1.5", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"arm_r_up": {"rotation": ["math.sin(variable.attack_time * 180) * -78", "0", "0"]}},
        {"arm_l_up": {"rotation": ["math.sin(variable.attack_time * 180) * -62", "0", "0"]}},
        {"arm_r_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -12", "0", "0"]}},
        {"arm_l_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -20", "0", "0"]}},
        {"rifle": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.5"]}},
        {"torso": {"rotation": ["math.sin(variable.attack_time * 180) * -6", "0", "0"]}},
        {"neck": {"rotation": ["math.sin(variable.attack_time * 180) * -8", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "battle_droid",
    "name": "Battle Droid",
    "egg": ("#c8b184", "#6a5236"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.0, 3.2, 1.2],
    "bones": bones,
    "skins": {"default": tan, "tan": tan, "brown": brown, "dark": dark, "gun": gun, "eye": eye, "stripe": stripe},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 22, "speed": 0.28, "damage": 4, "box": [0.7, 2.0],
        "ranged": True, "range": 18, "projectile": "minecraft:arrow",
        "family": ["droid", "trooper"],
        "spawn": {"biomes": ["overworld"], "weight": 8, "herd": [3, 5]},
        "loot": [("minecraft:iron_ingot", 1, 2), ("minecraft:copper_ingot", 1, 3), ("minecraft:redstone", 0, 2)],
        "sound": ("skeleton", [0.75, 0.9]),
        "xp": 6,
    },
}
