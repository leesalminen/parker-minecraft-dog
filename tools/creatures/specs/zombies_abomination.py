"""The Abomination - colossal mutated horror with three arms and glowing tumour sacs.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SKIN    = "#6f7a52"
SKIN_D  = "#454d33"
SKIN_L  = "#98a074"
BELLY   = "#c2c4a2"
VEIN    = "#7a3a3a"
GRIME   = "#2e2c1e"
BLOOD   = "#7a1f1f"
BONE    = "#e0d6b0"
BONE_D  = "#a59b76"
TOOTH   = "#e8e2c6"
CLAW    = "#2f2b24"
TUMOR   = "#b7ff3c"
EYE     = "#ffd23f"


def n(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def skin(p):
    x, y, z = p.p
    g = n(p, 2.8, 19)
    patch = n(p, 8.0, 43)
    c = mix(SKIN_D, SKIN_L, 0.18 + 0.82 * patch)
    c = shade(c, 0.78 + 0.44 * g)
    if y < 36:                                        # heavy grime low down
        c = mix(c, GRIME, 0.42 * min(1.0, (36 - y) / 20.0))
    if y > 50:
        c = shade(c, 1.06)
    v = math.sin(x * 0.7 + z * 0.55 + y * 0.22)       # thick veins
    if v > 0.80:
        c = mix(c, VEIN, 0.35 + 0.35 * (v - 0.80) * 5)
    if hash01(int(x * 1.2), int(y * 1.2), int(z * 1.2), 83) > 0.955:
        c = mix(c, BLOOD, 0.6)
    if p.bone == "body" and hash01(int(x * 0.9), int(y * 0.9), int(z * 0.9), 37) > 0.90:
        c = mix(c, "#8a8f6a", 0.5)                    # weeping sores / pustules
    return c


def tumor(p):
    x, y, z = p.p
    t = 0.3 + 0.7 * n(p, 1.5, 91)
    c = mix("#4f7a12", TUMOR, t)
    if math.sin(x * 1.1 + y * 1.3 + z * 0.7) > 0.35:
        c = mix(c, "#e6ffa0", 0.6)
    return glow(c)


def bone(p):
    c = mix(BONE_D, BONE, 0.3 + 0.7 * n(p, 1.6, 71))
    if hash01(int(p.p[0] * 2), int(p.p[1] * 2), int(p.p[2] * 2), 73) > 0.86:
        c = shade(c, 0.78)
    return c


def tooth(p):
    return shade(TOOTH, 0.85 + 0.25 * n(p, 1.0, 81))


def claw(p):
    return shade(CLAW, 0.85 + 0.30 * n(p, 1.0, 91))


def eye(p):
    x, y, z = p.p
    if p.face == "front":
        t = 0.35 + 0.65 * n(p, 1.0, 87)
        return glow(mix("#d98a10", EYE, t))
    return glow(shade(EYE, 0.55))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "skin")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- body (bloated, lopsided)
body_cubes = [
    {"o": [-9, 32, -7], "s": [18, 10, 14], "skin": "skin"},    # pelvis
    {"o": [-12, 42, -9], "s": [24, 14, 18], "skin": "skin"},   # bloated torso
    {"o": [-10, 52, -7], "s": [20, 6, 14], "skin": "skin"},    # chest shelf
    {"o": [-10, 35, -13], "s": [20, 11, 6], "skin": "skin"},   # enormous gut
    {"o": [-11, 46, 9], "s": [22, 10, 8], "skin": "skin"},     # hunched back
    {"o": [-3, 41, -14], "s": [7, 6, 3], "skin": "skin"},      # gut fold
]
sym(body_cubes, {"o": [10, 44, -8], "s": [4, 12, 12], "skin": "skin", "rot": [0, 0, -12], "pivot": [10, 44, -8]})
sym(body_cubes, {"o": [11, 48, 3], "s": [4, 10, 10], "skin": "skin", "rot": [0, 0, -12], "pivot": [11, 48, 3]})
# glowing tumour sacs
body_cubes.append({"o": [-6, 50, 9], "s": [5, 5, 4], "skin": "tumor"})
body_cubes.append({"o": [3, 45, 9], "s": [6, 6, 5], "skin": "tumor"})
body_cubes.append({"o": [-12, 43, -3], "s": [3, 5, 6], "skin": "tumor"})
body_cubes.append({"o": [-2, 55, 8], "s": [4, 4, 4], "skin": "tumor"})
body_cubes.append({"o": [6, 38, -13], "s": [4, 4, 3], "skin": "tumor"})
# ribs bursting through the skin
for zz in (-8, -5, -2):
    sym(body_cubes, {"o": [5, 47, zz], "s": [2, 2, 6], "skin": "bone"})
sym(body_cubes, {"o": [6, 43, -4], "s": [3, 3, 3], "skin": "bone"})
body_cubes.append({"o": [-9, 44, -10], "s": [3, 4, 2], "skin": "bone"})

# ----------------------------------------------------------------- head (lopsided, many eyes)
head_cubes = [
    {"o": [-2, 56, -10], "s": [10, 8, 9], "skin": "skin"},     # skewed skull
    {"o": [-1, 63, -11], "s": [9, 2, 4], "skin": "skin"},      # heavy twisted brow
    {"o": [2, 63, -9], "s": [5, 2, 5], "skin": "skin"},        # bony crown lump
    {"o": [-4, 55, -9], "s": [4, 3, 5], "skin": "bone"},       # exposed cheekbone
]
head_cubes.append({"o": [3, 58, -11], "s": [3, 3, 1], "skin": "eye"})    # big central eye
head_cubes.append({"o": [-1, 61, -11], "s": [2, 2, 1], "skin": "eye"})   # upper eye
head_cubes.append({"o": [6, 56, -11], "s": [1, 1, 1], "skin": "eye"})    # small eye
head_cubes.append({"o": [-2, 57, -11], "s": [1, 1, 1], "skin": "eye"})   # small eye

jaw_cubes = [
    {"o": [-1, 52, -12], "s": [8, 4, 9], "skin": "skin"},      # slung jaw
    {"o": [-1, 54, -12], "s": [8, 1, 8], "skin": "tooth"},     # tooth row
    {"o": [-1, 50, -11], "s": [8, 2, 8], "skin": "skin"},
]
jaw_cubes.append({"o": [0, 49, -12], "s": [2, 4, 2], "skin": "tooth"})   # huge tusks
jaw_cubes.append({"o": [3, 49, -12], "s": [2, 4, 2], "skin": "tooth"})
jaw_cubes.append({"o": [6, 49, -12], "s": [1, 4, 2], "skin": "tooth"})

# ----------------------------------------------------------------- oversized clawed arm (left)
arm_l_cubes = [
    {"o": [10, 38, -4], "s": [9, 17, 9], "skin": "skin"},      # huge upper arm
    {"o": [11, 42, -4], "s": [10, 10, 10], "skin": "skin"},    # bulging bicep
    {"o": [13, 40, 2], "s": [3, 6, 6], "skin": "skin"},        # shoulder growth
]
fore_l_cubes = [
    {"o": [9, 22, -5], "s": [11, 16, 11], "skin": "skin"},
    {"o": [9, 24, -5], "s": [11, 3, 11], "skin": "bone"},      # bone ring
]
claw_l_cubes = [
    {"o": [9, 16, -7], "s": [11, 6, 11], "skin": "skin"},      # massive hand
]
for i in range(4):
    claw_l_cubes.append({"o": [9 + i * 2.6, 10, -9], "s": [2, 6, 2], "skin": "claw",
                         "rot": [0, 0, -10 + i * 7], "pivot": [10 + i * 2.6, 16, -8]})

# ----------------------------------------------------------------- right arm (smaller, second)
arm_r_cubes = [
    {"o": [-16, 40, -3], "s": [6, 14, 6], "skin": "skin"},
    {"o": [-17, 43, -3], "s": [8, 7, 7], "skin": "skin"},
]
fore_r_cubes = [
    {"o": [-16, 26, -4], "s": [6, 14, 6], "skin": "skin"},
    {"o": [-16, 28, -5], "s": [6, 2, 6], "skin": "bone"},
]
hand_r_cubes = [
    {"o": [-17, 20, -5], "s": [8, 6, 8], "skin": "skin"},
]
for i in range(3):
    hand_r_cubes.append({"o": [-16 + i * 2, 15, -6.5], "s": [2, 4, 2], "skin": "claw"})

# ----------------------------------------------------------------- third arm (from the back)
arm_c_cubes = [
    {"o": [-3, 38, 9], "s": [6, 14, 6], "skin": "skin"},
]
fore_c_cubes = [
    {"o": [-3, 24, 10], "s": [6, 14, 6], "skin": "skin"},
    {"o": [-3, 26, 10], "s": [6, 2, 6], "skin": "bone"},
]
hand_c_cubes = [
    {"o": [-4, 18, 10], "s": [8, 6, 8], "skin": "skin"},
]
for i in range(3):
    hand_c_cubes.append({"o": [-3 + i * 2, 13, 9], "s": [2, 4, 2], "skin": "claw"})

# ----------------------------------------------------------------- legs (right leg drags)
thigh_l_cubes = [
    {"o": [2, 20, -4], "s": [8, 14, 9], "skin": "skin"},
    {"o": [2, 22, -5], "s": [8, 5, 1], "skin": "skin"},
]
shin_l_cubes = [
    {"o": [2, 6, -4], "s": [7, 14, 8], "skin": "skin"},
    {"o": [2, 8, -5], "s": [3, 3, 2], "skin": "bone"},         # shin bone bursting
]
foot_l_cubes = [
    {"o": [1, 0, -9], "s": [9, 6, 11], "skin": "skin"},
]
for i in range(3):
    foot_l_cubes.append({"o": [1 + i * 3, 0, -11], "s": [2, 3, 3], "skin": "claw"})

thigh_r_cubes = [
    {"o": [-10, 21, -3], "s": [7, 13, 8], "skin": "skin"},
]
shin_r_cubes = [
    {"o": [-10, 7, -2], "s": [6, 14, 7], "skin": "skin", "rot": [12, 0, 0], "pivot": [-10, 20, -2]},
]
foot_r_cubes = [
    {"o": [-11, 0, -7], "s": [7, 5, 10], "skin": "skin", "rot": [-8, 0, 0], "pivot": [-11, 4, -2]},
]
for i in range(3):
    foot_r_cubes.append({"o": [-11 + i * 2.6, 0, -9], "s": [2, 3, 3], "skin": "claw"})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 44, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [2, 58, -4], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [2, 56, -7], "cubes": jaw_cubes},
    {"name": "arm_l", "parent": "body", "pivot": [14, 55, -2], "rotation": [0, 0, -14], "cubes": arm_l_cubes},
    {"name": "fore_l", "parent": "arm_l", "pivot": [14, 38, -1], "cubes": fore_l_cubes},
    {"name": "claw_l", "parent": "fore_l", "pivot": [14, 22, -1], "cubes": claw_l_cubes},
    {"name": "arm_r", "parent": "body", "pivot": [-14, 54, -2], "rotation": [0, 0, 14], "cubes": arm_r_cubes},
    {"name": "fore_r", "parent": "arm_r", "pivot": [-14, 40, -1], "cubes": fore_r_cubes},
    {"name": "hand_r", "parent": "fore_r", "pivot": [-14, 26, -1], "cubes": hand_r_cubes},
    {"name": "arm_c", "parent": "body", "pivot": [0, 52, 10], "rotation": [26, 0, 0], "cubes": arm_c_cubes},
    {"name": "fore_c", "parent": "arm_c", "pivot": [0, 38, 10], "cubes": fore_c_cubes},
    {"name": "hand_c", "parent": "fore_c", "pivot": [0, 24, 10], "cubes": hand_c_cubes},
    {"name": "thigh_l", "parent": "body", "pivot": [6, 34, 0], "cubes": thigh_l_cubes},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [6, 20, 0], "cubes": shin_l_cubes},
    {"name": "foot_l", "parent": "shin_l", "pivot": [6, 6, -1], "cubes": foot_l_cubes},
    {"name": "thigh_r", "parent": "body", "pivot": [-6, 34, 0], "cubes": thigh_r_cubes},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-6, 21, 0], "cubes": shin_r_cubes},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-6, 7, -1], "cubes": foot_r_cubes},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=24, freq=26),
        swing({"shin_l": 180}, amp=16, freq=26),
        {"shin_r": {"rotation": ["10 + math.cos(query.modified_distance_moved * 26 + 180) * 10 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["-8 - math.cos(query.modified_distance_moved * 26 + 180) * 8 * query.modified_move_speed", "0", "0"]}},
        sway("body", amp=6, rate=26, axis=2),
        bob("body", amp=1.2, rate=52),
        {"arm_l": {"rotation": ["-14 + math.cos(query.modified_distance_moved * 26) * 12 * query.modified_move_speed", "0", "-14"]}},
        {"arm_r": {"rotation": ["-10 + math.cos(query.modified_distance_moved * 26 + 180) * 14 * query.modified_move_speed", "0", "14"]}},
        {"arm_c": {"rotation": ["26 + math.cos(query.modified_distance_moved * 26 + 90) * 8 * query.modified_move_speed", "0", "0"]}},
        swing({"fore_c": 0, "hand_c": 180}, amp=10, axis=0, freq=26),
    )),
    "idle": anim(merge(
        bob("body", amp=1.1, rate=40),
        sway("body", amp=4, rate=24, axis=2),
        sway("head", amp=6, rate=27, axis=2, off=0.6),
        sway("head", amp=4, rate=19, axis=1, off=1.4),
        {"jaw": {"rotation": ["math.sin(query.life_time * 33) * 6", "0", "0"]}},
        {"arm_l": {"rotation": ["-14 + math.sin(query.life_time * 26 + 0.3) * 4", "0", "-14"]}},
        {"arm_r": {"rotation": ["-10 + math.sin(query.life_time * 33 + 1.7) * 6", "0", "14"]}},
        {"arm_c": {"rotation": ["26 + math.sin(query.life_time * 30 + 2.5) * 7", "0", "0"]}},
        {"fore_c": {"rotation": ["math.sin(query.life_time * 35 + 0.9) * 9", "0", "0"]}},
        {"claw_l": {"rotation": ["math.sin(query.life_time * 22) * 4", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "math.sin(variable.attack_time * 180) * 14", "0"]}},
        {"arm_l": {"rotation": ["-14 + math.cos(variable.attack_time * 180) * -70", "0", "-14"]}},
        {"fore_l": {"rotation": ["math.cos(variable.attack_time * 180) * -24", "0", "0"]}},
        {"claw_l": {"rotation": ["math.cos(variable.attack_time * 180) * -18", "0", "0"]}},
        {"arm_c": {"rotation": ["26 + math.sin(variable.attack_time * 180) * 40", "0", "0"]}},
        {"fore_c": {"rotation": ["math.sin(variable.attack_time * 180) * 24", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 18", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 34", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "abomination",
    "name": "The Abomination",
    "egg": ("#454d33", "#b7ff3c"),
    "glow": True,
    "scale": 1.0,
    "visible": [7.0, 6.0, 2.0],
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "tumor": tumor, "bone": bone,
              "tooth": tooth, "claw": claw, "eye": eye},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 200, "speed": 0.18, "damage": 12, "box": [2.4, 4.0],
        "knockback_resist": 0.9, "family": ["undead", "zombie"],
        "loot": [("minecraft:rotten_flesh", 4, 8), ("minecraft:bone", 3, 6),
                 ("minecraft:iron_nugget", 0, 3), ("minecraft:gold_nugget", 0, 1)],
        "sound": ("zombie", [0.5, 0.7]),
        "xp": 40,
        "spawn": {"biomes": ["overworld"], "weight": 1, "herd": [1, 1]},
    },
}
