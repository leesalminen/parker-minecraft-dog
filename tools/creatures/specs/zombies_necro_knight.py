"""Necro Knight - undead knight in cracked plate with a greatsword and tattered cape.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

PLATE   = "#5c6672"
PLATE_D = "#3a424c"
PLATE_L = "#7d8792"
RUST    = "#6b4326"
RUST_L  = "#8f5c33"
EDGE    = "#9aa4ae"
BONE    = "#d9d0ac"
BONE_D  = "#9e9674"
CLOTH   = "#3a2f33"
CLOTH_D = "#221b1e"
CLOTH_L = "#54454a"
EYE     = "#5cff6a"
BLADE   = "#aeb8c2"
BLADE_D = "#7d8791"


def n(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def armor(p):
    x, y, z = p.p
    g = n(p, 2.4, 17)
    patch = n(p, 6.0, 37)
    c = mix(PLATE_D, PLATE_L, 0.20 + 0.80 * patch)
    c = shade(c, 0.80 + 0.42 * g)
    if (p.y % 7) < 1 or (p.x % 9) < 1:               # panel seams
        c = shade(c, 0.72)
    if hash01(int(x * 1.7), int(y * 1.7), int(z * 1.7), 43) > 0.90:
        c = mix(c, RUST, 0.55)                        # rust bloom
    if p.face in ("front", "back"):
        cx = abs(p.x + 0.5 - p.fw / 2)
        if cx > p.fw * 0.30 and hash01(0, int(y * 3), 0, 59) > 0.5:
            c = shade(c, 1.10)                        # plate highlights
    return c


def metal(p):
    x, y, z = p.p
    c = mix(PLATE_D, EDGE, 0.3 + 0.7 * n(p, 1.6, 61))
    c = shade(c, 0.85 + 0.28 * n(p, 1.0, 63))
    if hash01(int(x * 2), int(y * 2), int(z * 2), 67) > 0.91:
        c = mix(c, RUST_L, 0.6)
    return c


def blade(p):
    x, y, z = p.p
    c = mix(BLADE_D, BLADE, 0.25 + 0.75 * n(p, 2.0, 71))
    if p.face in ("front", "back") and abs(p.x + 0.5 - p.fw / 2) < 0.9:
        c = shade(c, 1.18)                            # central fuller
    c = shade(c, 0.90 + 0.22 * n(p, 1.0, 73))
    if hash01(int(x * 3), int(y * 3), int(z * 3), 79) > 0.94:
        c = mix(c, RUST, 0.5)                         # blood-rust nicks
    return c


def bone(p):
    c = mix(BONE_D, BONE, 0.3 + 0.7 * n(p, 1.5, 83))
    if hash01(int(p.p[0] * 2), int(p.p[1] * 2), int(p.p[2] * 2), 89) > 0.86:
        c = shade(c, 0.78)
    return c


def tooth(p):
    return shade("#e6e0c6", 0.85 + 0.25 * n(p, 1.0, 91))


def cloth(p):
    x, y, z = p.p
    g = n(p, 2.8, 97)
    c = mix(CLOTH_D, CLOTH_L, 0.25 + 0.75 * g)
    weave = (math.floor(x * 0.6) + math.floor(y * 0.6)) % 2
    c = shade(c, 0.80 if weave else 1.14)
    if y < 16:
        c = mix(c, "#0f0d10", 0.45 * min(1.0, (16 - y) / 12.0))   # dirtier toward the hem
    if hash01(int(x * 1.5), int(y * 1.5), int(z * 1.5), 101) > 0.90:
        c = shade(c, 0.6)                             # tattered tears
    return c


def eye(p):
    if p.face == "front":
        return glow(mix("#1f7a2a", EYE, 0.35 + 0.65 * n(p, 1.2, 103)))
    return glow(shade(EYE, 0.55))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "armor")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- body
body_cubes = [
    {"o": [-5, 16, -4], "s": [10, 5, 8], "skin": "armor"},     # pelvis
    {"o": [-6, 13, -4], "s": [12, 3, 9], "skin": "armor"},     # tasset skirt
    {"o": [-6, 21, -5], "s": [12, 8, 10], "skin": "armor"},    # cuirass
    {"o": [-5, 22, -6], "s": [10, 7, 1], "skin": "armor"},     # breastplate face
    {"o": [-5, 22, 5], "s": [10, 7, 1], "skin": "armor"},      # back plate
    {"o": [-6, 20, -5], "s": [12, 2, 10], "skin": "metal"},    # belt
    {"o": [-1, 19, -6], "s": [2, 4, 1], "skin": "metal"},      # buckle strap
    {"o": [-4, 25, -6], "s": [3, 3, 1], "skin": "armor"},      # cracked chest wound
]
sym(body_cubes, {"o": [3, 21, -6], "s": [2, 4, 1], "skin": "bone"})   # ribs through a crack
sym(body_cubes, {"o": [5, 23, -4], "s": [2, 3, 4], "skin": "armor", "rot": [0, 0, -10], "pivot": [5, 23, -4]})

# ----------------------------------------------------------------- helm / head
head_cubes = [
    {"o": [-4, 27, -5], "s": [8, 5, 8], "skin": "armor"},      # great helm
    {"o": [-4, 31, -3], "s": [8, 1, 6], "skin": "armor"},      # helm cap
    {"o": [-1, 32, -4], "s": [2, 1, 6], "skin": "metal"},      # crest ridge
    {"o": [-4, 27, -6], "s": [8, 1, 1], "skin": "armor"},      # visor brow
    {"o": [-2, 25, -6], "s": [4, 1, 1], "skin": "armor"},      # breathing slits plate
]
sym(head_cubes, {"o": [1, 28, -6], "s": [2, 2, 1], "skin": "eye"})    # glowing eye slit

jaw_cubes = [
    {"o": [-2, 24, -6], "s": [4, 2, 6], "skin": "bone"},       # skeletal jaw
    {"o": [-2, 24, -6], "s": [4, 1, 1], "skin": "tooth"},
]
sym(jaw_cubes, {"o": [1, 23, -6], "s": [1, 2, 1], "skin": "tooth"})   # fangs

horn_l_cubes = [{"o": [2, 32, -3], "s": [2, 3, 2], "skin": "metal", "rot": [0, 0, -22], "pivot": [3, 32, -3]}]
horn_l2_cubes = [{"o": [3, 34, -3], "s": [2, 2, 2], "skin": "metal", "rot": [0, 0, -40], "pivot": [4, 34, -3]}]
horn_r_cubes = [{"o": [-4, 32, -3], "s": [2, 3, 2], "skin": "metal", "rot": [0, 0, 22], "pivot": [-3, 32, -3]}]
horn_r2_cubes = [{"o": [-5, 34, -3], "s": [2, 2, 2], "skin": "metal", "rot": [0, 0, 40], "pivot": [-4, 34, -3]}]

# ----------------------------------------------------------------- cape (hangs from the shoulders, behind)
cape0_cubes = [{"o": [-5, 18, 6], "s": [10, 12, 1], "skin": "cloth"}]
cape1_cubes = [{"o": [-5, 8, 6], "s": [10, 10, 1], "skin": "cloth"}]
cape2_cubes = [
    {"o": [-4, 0, 6], "s": [8, 8, 1], "skin": "cloth"},
    {"o": [-4, 0, 6.9], "s": [3, 4, 1], "skin": "cloth"},      # ragged tail of the cape
]

# ----------------------------------------------------------------- arms
arm_l_cubes = [
    {"o": [6, 26, -4], "s": [6, 5, 7], "skin": "armor"},       # pauldron
    {"o": [7, 25, -2], "s": [1, 4, 4], "skin": "armor", "rot": [0, 0, -20], "pivot": [7, 28, -2]},  # pauldron lip
    {"o": [6, 19, -3], "s": [4, 9, 4], "skin": "armor"},       # upper arm
]
fore_l_cubes = [
    {"o": [6, 12, -3], "s": [4, 7, 4], "skin": "bone"},        # skeletal forearm
    {"o": [5, 16, -4], "s": [6, 3, 6], "skin": "armor"},       # vambrace
]
hand_l_cubes = [
    {"o": [6, 9, -3], "s": [4, 3, 4], "skin": "bone"},         # skeletal hand
]
for i in range(3):
    hand_l_cubes.append({"o": [6 + i, 7, -3.6], "s": [1, 2, 1], "skin": "bone"})   # finger bones
sword_cubes = [
    {"o": [7, 12, -2], "s": [2, 15, 1], "skin": "blade", "rot": [35, 0, 0], "pivot": [8, 12, -2]},   # blade angled forward
    {"o": [6, 10, -2], "s": [6, 2, 1], "skin": "metal"},       # crossguard
    {"o": [7, 9, -2], "s": [2, 3, 1], "skin": "metal"},        # grip
    {"o": [7, 7, -2], "s": [3, 2, 1], "skin": "metal"},        # pommel
]

arm_r_cubes = [
    {"o": [-11, 26, -4], "s": [6, 5, 7], "skin": "armor"},
    {"o": [-12, 25, -2], "s": [1, 4, 4], "skin": "armor", "rot": [0, 0, 20], "pivot": [-7, 28, -2]},
    {"o": [-10, 19, -3], "s": [4, 9, 4], "skin": "armor"},
]
fore_r_cubes = [
    {"o": [-10, 12, -3], "s": [4, 7, 4], "skin": "bone"},
    {"o": [-11, 16, -4], "s": [6, 3, 6], "skin": "armor"},
]
hand_r_cubes = [
    {"o": [-10, 9, -3], "s": [4, 3, 4], "skin": "bone"},
]
for i in range(3):
    hand_r_cubes.append({"o": [-9 - i, 7, -3.6], "s": [1, 2, 1], "skin": "bone"})

# ----------------------------------------------------------------- legs
thigh_l_cubes = [
    {"o": [2, 9, -3], "s": [4, 7, 5], "skin": "armor"},
    {"o": [2, 11, -4], "s": [4, 4, 1], "skin": "armor"},       # thigh plate
]
thigh_r_cubes = [
    {"o": [-6, 9, -3], "s": [4, 7, 5], "skin": "armor"},
    {"o": [-6, 11, -4], "s": [4, 4, 1], "skin": "armor"},
]
shin_l_cubes = [
    {"o": [2, 3, -3], "s": [3, 6, 4], "skin": "armor"},
    {"o": [2, 5, -4], "s": [3, 3, 1], "skin": "armor"},        # greave ridge
]
shin_r_cubes = [
    {"o": [-5, 3, -3], "s": [3, 6, 4], "skin": "armor"},
    {"o": [-5, 5, -4], "s": [3, 3, 1], "skin": "armor"},
]
foot_l_cubes = [
    {"o": [2, 0, -5], "s": [4, 3, 7], "skin": "metal"},
    {"o": [2, 0, -7], "s": [4, 2, 2], "skin": "metal"},        # pointed sabaton toe
]
foot_r_cubes = [
    {"o": [-6, 0, -5], "s": [4, 3, 7], "skin": "metal"},
    {"o": [-6, 0, -7], "s": [4, 2, 2], "skin": "metal"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 21, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 28, -1], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 26, -4], "cubes": jaw_cubes},
    {"name": "horn_l", "parent": "head", "pivot": [3, 32, -3], "cubes": horn_l_cubes},
    {"name": "horn_l2", "parent": "horn_l", "pivot": [4, 34, -3], "cubes": horn_l2_cubes},
    {"name": "horn_r", "parent": "head", "pivot": [-3, 32, -3], "cubes": horn_r_cubes},
    {"name": "horn_r2", "parent": "horn_r", "pivot": [-4, 34, -3], "cubes": horn_r2_cubes},
    {"name": "cape0", "parent": "body", "pivot": [0, 30, 6], "cubes": cape0_cubes},
    {"name": "cape1", "parent": "cape0", "pivot": [0, 18, 6], "cubes": cape1_cubes},
    {"name": "cape2", "parent": "cape1", "pivot": [0, 8, 6], "cubes": cape2_cubes},
    {"name": "arm_l", "parent": "body", "pivot": [8, 28, -1], "rotation": [0, 0, -6], "cubes": arm_l_cubes},
    {"name": "fore_l", "parent": "arm_l", "pivot": [8, 19, -1], "cubes": fore_l_cubes},
    {"name": "hand_l", "parent": "fore_l", "pivot": [8, 12, -1], "cubes": hand_l_cubes},
    {"name": "sword", "parent": "hand_l", "pivot": [8, 9, -2], "cubes": sword_cubes},
    {"name": "arm_r", "parent": "body", "pivot": [-8, 28, -1], "rotation": [0, 0, 6], "cubes": arm_r_cubes},
    {"name": "fore_r", "parent": "arm_r", "pivot": [-8, 19, -1], "cubes": fore_r_cubes},
    {"name": "hand_r", "parent": "fore_r", "pivot": [-8, 12, -1], "cubes": hand_r_cubes},
    {"name": "thigh_l", "parent": "body", "pivot": [4, 16, 0], "cubes": thigh_l_cubes},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [4, 9, 0], "cubes": shin_l_cubes},
    {"name": "foot_l", "parent": "shin_l", "pivot": [4, 3, -1], "cubes": foot_l_cubes},
    {"name": "thigh_r", "parent": "body", "pivot": [-4, 16, 0], "cubes": thigh_r_cubes},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-4, 9, 0], "cubes": shin_r_cubes},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-4, 3, -1], "cubes": foot_r_cubes},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=30, freq=38),
        swing({"shin_l": 180, "shin_r": 0}, amp=16, freq=38),
        swing({"cape0": 0, "cape1": 30, "cape2": 60}, amp=10, axis=0, freq=38),
        {"arm_l": {"rotation": ["math.cos(query.modified_distance_moved * 38 + 180) * 10 * query.modified_move_speed", "0", "-6"]}},
        {"arm_r": {"rotation": ["math.cos(query.modified_distance_moved * 38) * 10 * query.modified_move_speed", "0", "6"]}},
        bob("body", amp=0.4, rate=76),
        sway("body", amp=2, rate=38, axis=2),
    )),
    "idle": anim(merge(
        bob("body", amp=0.4, rate=46),
        sway("cape0", amp=3, rate=30, axis=0),
        sway("cape1", amp=6, rate=26, axis=0, off=0.8),
        sway("cape2", amp=10, rate=22, axis=0, off=1.6),
        {"head": {"rotation": ["math.sin(query.life_time * 21) * 3", "math.sin(query.life_time * 13) * 5", "0"]}},
        {"jaw": {"rotation": ["math.sin(query.life_time * 41) * 4", "0", "0"]}},
        {"arm_l": {"rotation": ["math.sin(query.life_time * 30) * 3", "0", "-6"]}},
        {"sword": {"rotation": ["math.sin(query.life_time * 30 + 1.2) * 3", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["0", "math.sin(variable.attack_time * 180) * 18", "0"]}},
        {"arm_l": {"rotation": ["math.cos(variable.attack_time * 180) * -80", "0", "-6"]}},
        {"fore_l": {"rotation": [f"math.cos(variable.attack_time * 180) * -18", "0", "0"]}},
        {"sword": {"rotation": [f"math.cos(variable.attack_time * 180) * 14", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 8", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]}},
        {"arm_r": {"rotation": [f"math.sin(variable.attack_time * 180) * 30", "0", "6"]}},
    ), loop=False),
}

SPEC = {
    "id": "necro_knight",
    "name": "Necro Knight",
    "egg": ("#3a424c", "#5cff6a"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.0, 2.8, 1.2],
    "bones": bones,
    "skins": {"default": armor, "armor": armor, "metal": metal, "blade": blade,
              "bone": bone, "tooth": tooth, "cloth": cloth, "eye": eye},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 50, "speed": 0.25, "damage": 7, "box": [1.0, 2.2],
        "knockback_resist": 0.35, "family": ["undead", "zombie"],
        "loot": [("minecraft:rotten_flesh", 1, 2), ("minecraft:bone", 1, 3),
                 ("minecraft:iron_nugget", 1, 3), ("minecraft:gold_nugget", 0, 1)],
        "sound": ("zombie", [0.7, 0.85]),
        "xp": 10,
        "spawn": {"biomes": ["overworld"], "weight": 6, "herd": [1, 1]},
    },
}
