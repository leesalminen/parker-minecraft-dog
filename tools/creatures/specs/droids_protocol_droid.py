"""Protocol Droid - passive gold butler droid.  Model faces -Z, y up, ground y=0. 1 unit = 1/16 block."""
import math
from lib import *

GOLD   = "#e2b53f"
GOLD_D = "#b98c26"
DULL   = "#8a7434"
DARK   = "#4c3d16"
STEEL  = "#8f9298"
EYE    = "#ffcf4d"
RED    = "#c8402c"


def panel(v, period=10.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, period=10.0, r=0.6):
    dx = min(x % period, period - x % period)
    dy = min(y % period, period - y % period)
    return dx < r and dy < r


def paint(p, base, dark, seed, dull=None):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.8)
    c = mix(dark, base, 0.30 + 0.70 * n)
    c = shade(c, 0.90 + 0.22 * noise3(x, y, z, seed + 5, 1.1))
    if dull is not None:
        d = noise3(x, y, z, seed + 13, 5.5)
        if d > 0.62:
            c = mix(c, dull, min(1.0, (d - 0.62) * 2.4))
    if panel(x) or panel(y):
        c = shade(c, 0.78)
    if rivets(x, y):
        c = shade(c, 0.62)
    if hash01(x, y, z, seed + 2) > 0.958:
        c = shade(c, 1.28)
    if hash01(x, y, z, seed + 3) > 0.975:
        c = shade(c, 0.55)
    if p.face == "top":
        c = shade(c, 1.15)
    if p.face == "bottom":
        c = shade(c, 0.78)
    return c


def gold(p):
    return paint(p, GOLD, GOLD_D, 11, DULL)


def dull(p):
    return paint(p, DULL, "#5e4f22", 17, "#6b5c28")


def dark(p):
    x, y, z = p.p
    c = mix("#241d08", DARK, 0.3 + 0.7 * noise3(x, y, z, 31, 3.0))
    if abs((y % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 33, 1.2))


def steel(p):
    return paint(p, STEEL, "#55585e", 41)


def eye(p):
    x, y, z = p.p
    return glow(mix("#fff2c0", EYE, 0.3 + 0.7 * noise3(x, y, z, 51, 2.2)))


def red(p):
    x, y, z = p.p
    return glow(mix("#ff8a70", RED, 0.3 + 0.7 * noise3(x, y, z, 55, 2.6)))


def mir(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "gold")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def mirror(cubes):
    return [mir(c) for c in cubes]


def sym(cubes, c):
    cubes.append(c)
    cubes.append(mir(c))


# ---------------------------------------------------------------- legs
foot_l = [
    {"o": [1.5, 0, -4], "s": [4, 2, 9], "skin": "gold"},
    {"o": [1.5, 0, -4], "s": [4, 2, 3], "skin": "dull"},
    {"o": [1.5, 0, 5], "s": [4, 2, 2], "skin": "dark"},
]
shin_l = [
    {"o": [2, 2, -2], "s": [3, 7, 4], "skin": "gold"},
    {"o": [2, 5, -2.5], "s": [3, 2, 1], "skin": "dull"},
    {"o": [2, 8, -2.5], "s": [3, 2, 1], "skin": "dark"},
]
thigh_l = [
    {"o": [2, 9, -2], "s": [3, 6, 4], "skin": "gold", "rot": [0, 0, 7], "pivot": [3.5, 15, 0]},
    {"o": [2, 12, -2.5], "s": [3, 2, 1], "skin": "dull"},
    {"o": [4.5, 10, -1.5], "s": [1, 4, 3], "skin": "dark"},
]
foot_r, shin_r, thigh_r = mirror(foot_l), mirror(shin_l), mirror(thigh_l)

# ---------------------------------------------------------------- pelvis
pelvis_cubes = [
    {"o": [-4, 14, -3], "s": [8, 5, 6], "skin": "gold"},
    {"o": [-3.5, 14, -3.5], "s": [7, 2, 1], "skin": "dull"},
    {"o": [-3, 18, -3], "s": [6, 1, 6], "skin": "dark"},
]
sym(pelvis_cubes, {"o": [3, 15, -2.5], "s": [1, 3, 5], "skin": "dark"})

# ---------------------------------------------------------------- torso
torso_cubes = [
    {"o": [-3.5, 18, -2.5], "s": [7, 8, 5], "skin": "gold"},
    {"o": [-3, 19, -4], "s": [6, 5, 2], "skin": "gold"},
    {"o": [-2.5, 20, -4.6], "s": [5, 3, 1], "skin": "dull"},
    {"o": [-1.5, 21, -5.1], "s": [1, 1, 1], "skin": "red"},
    {"o": [-1.5, 20, -5.1], "s": [1, 1, 1], "skin": "eye"},
    {"o": [-3, 25, -2.5], "s": [6, 1, 5], "skin": "dark"},
    {"o": [-2.5, 22, 2.5], "s": [5, 4, 2], "skin": "dull"},
    {"o": [-3, 18.5, -2.5], "s": [6, 1, 5], "skin": "dull"},
]
sym(torso_cubes, {"o": [3, 22, -2], "s": [2, 4, 4], "skin": "gold", "rot": [0, 0, -12], "pivot": [4, 26, -2]})
sym(torso_cubes, {"o": [-3, 19, -4.5], "s": [2, 5, 1], "skin": "dull"})
# exposed back cabling
for i in range(3):
    sym(torso_cubes, {"o": [-2 + i * 1.4, 19, 4.6], "s": [1, 7, 1], "skin": "dark"})

# ---------------------------------------------------------------- neck + head
neck_cubes = [
    {"o": [-1, 26, -1], "s": [2, 3, 2], "skin": "steel"},
    {"o": [-1.5, 27, -1.5], "s": [3, 1, 3], "skin": "dark"},
]
head_cubes = [
    {"o": [-2.5, 27, -2], "s": [5, 6, 5], "skin": "gold"},
    {"o": [-2, 29, -2.5], "s": [4, 3, 1], "skin": "dull"},
    {"o": [-2.5, 32.5, -2], "s": [5, 1, 5], "skin": "dull"},
    {"o": [-1.5, 27.5, -2.4], "s": [3, 1, 1], "skin": "dark"},
    {"o": [-2.5, 30, 3], "s": [5, 3, 1], "skin": "dark"},
]
sym(head_cubes, {"o": [-2.3, 29.4, -2.6], "s": [3, 3, 1], "skin": "dark"})
sym(head_cubes, {"o": [0.3, 30.2, -3], "s": [2, 2, 1], "skin": "eye"})
sym(head_cubes, {"o": [3, 28, -1], "s": [1, 4, 3], "skin": "dark"})

# ---------------------------------------------------------------- arms
arm_l_up = [
    {"o": [4, 18, -1], "s": [3, 7, 3], "skin": "gold"},
    {"o": [4, 24, -1], "s": [3, 2, 4], "skin": "dull"},
    {"o": [4, 19, -1.5], "s": [3, 1, 1], "skin": "dark"},
]
arm_l_fore = [
    {"o": [4, 11, -1], "s": [3, 7, 3], "skin": "gold"},
    {"o": [4, 15, -1.5], "s": [3, 2, 1], "skin": "dull"},
    {"o": [6, 12, -1], "s": [1, 3, 2], "skin": "dark"},
]
arm_l_hand = [
    {"o": [4, 9, -2], "s": [3, 3, 4], "skin": "steel"},
    {"o": [4, 9.5, -3], "s": [3, 2, 1], "skin": "dark"},
]
arm_r_up, arm_r_fore, arm_r_hand = mirror(arm_l_up), mirror(arm_l_fore), mirror(arm_l_hand)

bones = [
    {"name": "pelvis", "parent": None, "pivot": [0, 15, 0], "cubes": pelvis_cubes},
    {"name": "torso", "parent": "pelvis", "pivot": [0, 18, 0], "cubes": torso_cubes},
    {"name": "neck", "parent": "torso", "pivot": [0, 26, 0], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 27, 0], "cubes": head_cubes},
    {"name": "arm_l_up", "parent": "torso", "pivot": [5.5, 25, 0], "cubes": arm_l_up},
    {"name": "arm_l_fore", "parent": "arm_l_up", "pivot": [5.5, 18, 0], "cubes": arm_l_fore},
    {"name": "arm_l_hand", "parent": "arm_l_fore", "pivot": [5.5, 11, 0], "cubes": arm_l_hand},
    {"name": "arm_r_up", "parent": "torso", "pivot": [-5.5, 25, 0], "cubes": arm_r_up},
    {"name": "arm_r_fore", "parent": "arm_r_up", "pivot": [-5.5, 18, 0], "cubes": arm_r_fore},
    {"name": "arm_r_hand", "parent": "arm_r_fore", "pivot": [-5.5, 11, 0], "cubes": arm_r_hand},
    {"name": "thigh_l", "parent": "pelvis", "pivot": [3.5, 15, 0], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [3.5, 9, 0], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [3.5, 2, 0], "cubes": foot_l},
    {"name": "thigh_r", "parent": "pelvis", "pivot": [-3.5, 15, 0], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-3.5, 9, 0], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-3.5, 2, 0], "cubes": foot_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=20, freq=42),
        {"shin_l": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 180) * 12 * query.modified_move_speed", "0", "0"]}},
        {"shin_r": {"rotation": ["math.cos(query.modified_distance_moved * 42) * 12 * query.modified_move_speed", "0", "0"]}},
        {"foot_l": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 90) * 6 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 270) * 6 * query.modified_move_speed", "0", "0"]}},
        {"pelvis": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 21)) * 1.0 * query.modified_move_speed", "0"]}},
        {"torso": {"rotation": ["math.cos(query.modified_distance_moved * 42) * 2 * query.modified_move_speed", "0", "math.cos(query.modified_distance_moved * 21) * 3 * query.modified_move_speed"]}},
        {"arm_l_up": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 180) * 8 * query.modified_move_speed", "0", "0"]}},
        {"arm_r_up": {"rotation": ["math.cos(query.modified_distance_moved * 42) * 8 * query.modified_move_speed", "0", "0"]}},
    )),
    "idle": anim(merge(
        bob("pelvis", amp=0.5, rate=38),
        sway("neck", amp=3.5, rate=30, axis=0),
        sway("torso", amp=1.4, rate=26, axis=0),
        {"arm_l_up": {"rotation": ["-6", "0", "0"]}},
        {"arm_r_up": {"rotation": ["-6", "0", "0"]}},
        {"arm_l_fore": {"rotation": ["-14", "0", "math.sin(query.life_time * 55) * 9"]}},
        {"arm_r_fore": {"rotation": ["-14", "0", "math.sin(query.life_time * 55 + 180) * -9"]}},
        {"arm_l_hand": {"rotation": ["0", "math.sin(query.life_time * 55) * 14", "0"]}},
        {"arm_r_hand": {"rotation": ["0", "math.sin(query.life_time * 55 + 180) * -14", "0"]}},
        {"head": {"rotation": ["math.sin(query.life_time * 33) * 2", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"arm_l_up": {"rotation": ["math.sin(variable.attack_time * 180) * -55", "0", "0"]}},
        {"arm_r_up": {"rotation": ["math.sin(variable.attack_time * 180) * -55", "0", "0"]}},
        {"arm_l_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -35", "0", "0"]}},
        {"arm_r_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -35", "0", "0"]}},
        {"torso": {"rotation": ["math.sin(variable.attack_time * 180) * 10", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * -8", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "protocol_droid",
    "name": "Protocol Droid",
    "egg": ("#e2b53f", "#8a7434"),
    "glow": True,
    "scale": 1.0,
    "visible": [2.6, 3.0, 1.0],
    "bones": bones,
    "skins": {"default": gold, "gold": gold, "dull": dull, "dark": dark, "steel": steel, "eye": eye, "red": red},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "passive",
        "health": 20, "speed": 0.22, "box": [0.6, 1.9],
        "family": ["droid", "protocol"],
        "spawn": {"biomes": ["plains"], "weight": 1, "herd": [1, 1]},
        "loot": [("minecraft:gold_nugget", 1, 4), ("minecraft:redstone", 0, 2)],
        "sound": ("villager", [0.65, 0.8]),
        "xp": 5,
    },
}
