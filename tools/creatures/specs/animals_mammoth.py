"""Ember Mammoth - huge rideable woolly mammoth with howdah.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

DARK   = "#43301f"
MID    = "#63442a"
LIGHT  = "#8a6440"
BELLY  = "#a98a68"
STRAND = "#2f2216"
TUSK   = "#efe6cf"
TUSKD  = "#c9b894"
NOSE   = "#2a1e14"
EYE    = "#ffb347"
PUPIL  = "#2a0f00"
EMBLEM = "#ff7a1a"
HOOF   = "#3a2b1c"
WOOD   = "#6d4c2c"
CLOTH  = "#b6462c"


def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def fur(p):
    x, y, z = p.p
    # vertical shaggy strands (high frequency in y) + broad patches
    strand = noise3(x * 0.9, y * 2.6, z * 0.9, 17, 1.0)
    patch = noise3(x * 0.5, y * 0.5, z * 0.5, 29, 6.0)
    c = mix(MID, LIGHT, 0.25 + 0.7 * patch)
    c = shade(c, 0.72 + 0.55 * strand)
    if y < 34:
        t = min(1.0, (34 - y) / 16.0)
        c = mix(c, BELLY, 0.65 * t)
    if y > 46:
        c = shade(c, 0.86)
    if hash01(int(x * 0.5), int(y * 0.5), int(z * 0.5), 43) > 0.93:
        c = shade(c, 0.72)
    return c


def skirt(p):
    """Hanging fur fringe - darker tips."""
    x, y, z = p.p
    c = fur(p)
    t = min(1.0, max(0.0, (18 - y) / 6.0))
    return mix(c, STRAND, 0.55 * t)


def tusk(p):
    x, y, z = p.p
    n = noise3(x, y, z, 61, 2.0)
    c = mix(TUSKD, TUSK, 0.4 + 0.6 * n)
    # ring bands along the tusk
    band = math.sin(y * 1.15 + z * 0.5)
    if band > 0.6:
        c = shade(c, 0.92)
    return c


def ember_eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 1.0 and abs(p.y + 0.5 - p.fh / 2) < 1.0:
            return glow(PUPIL)
        return glow(EYE)
    return glow(shade(EYE, 0.7))


def wood(p):
    x, y, z = p.p
    n = noise3(x * 0.6, y * 0.3, z * 0.6, 71, 3.0)
    c = mix(shade(WOOD, 0.8), WOOD, n)
    # plank lines
    if abs((z % 8)) < 0.6 or abs((x % 8)) < 0.6:
        c = shade(c, 0.72)
    return c


def cloth(p):
    x, y, z = p.p
    n = noise3(x, y, z, 83, 1.6)
    c = shade(CLOTH, 0.85 + 0.3 * n)
    if abs((z % 6)) < 0.7:
        c = shade(c, 0.7)
    return c


def horn(p):
    return shade("#4a4038", 0.85 + 0.3 * grain(p, 1.5, 91))


def hoof(p):
    return shade(HOOF, 0.9 + 0.2 * grain(p, 1.2, 95))


def mouth(p):
    return "#7a3b3b"


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "fur")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- body
body_cubes = [
    {"o": [-15, 22, -20], "s": [30, 30, 40], "skin": "fur"},
    {"o": [-12, 22, -14], "s": [24, 12, 30], "skin": "fur"},       # belly
    {"o": [-14, 40, -18], "s": [28, 14, 14], "skin": "fur"},       # shoulder hump
    {"o": [-13, 30, 8], "s": [26, 20, 14], "skin": "fur"},         # rump slope
]
# back ridge bumps
for zz in (-14, -4, 6, 15):
    body_cubes.append({"o": [-3, 54, zz], "s": [6, 3, 6], "skin": "fur"})
# hanging fur skirts along both flanks
for zz in range(-18, 18, 5):
    sym(body_cubes, {"o": [13, 12, zz], "s": [4, 14, 4], "skin": "skirt", "inflate": 0.3,
                     "rot": [0, 0, -6], "pivot": [13, 26, zz]})
for zz in range(-16, 17, 4):
    sym(body_cubes, {"o": [10, 10, zz], "s": [3, 12, 3], "skin": "skirt", "inflate": 0.3})

# howdah platform + railing
body_cubes += [
    {"o": [-9, 52, -6], "s": [18, 3, 20], "skin": "wood"},
    {"o": [-8, 55, -5], "s": [16, 1, 18], "skin": "cloth"},
]
for px, pz in ((-9, -6), (7, -6), (-9, 12), (7, 12)):
    body_cubes.append({"o": [px, 55, pz], "s": [2, 4, 2], "skin": "wood"})

head_cubes = [
    {"o": [-10, 40, -36], "s": [20, 16, 16], "skin": "fur"},
    {"o": [-9, 50, -35], "s": [18, 6, 11], "skin": "fur"},         # forehead dome
    {"o": [-6, 38, -38], "s": [12, 4, 12], "skin": "fur"},         # jaw base
]
sym(head_cubes, {"o": [4, 50, -37], "s": [3, 3, 3], "skin": "eye"})
sym(head_cubes, {"o": [1, 44, -37], "s": [3, 6, 4], "skin": "fur"})   # cheek
sym(head_cubes, {"o": [8, 42, -35], "s": [3, 4, 4], "skin": "horn"})  # tusk root bump

jaw_cubes = [
    {"o": [-6, 36, -39], "s": [12, 4, 11], "skin": "fur"},
    {"o": [-5, 39.2, -38.4], "s": [10, 1, 10], "skin": "mouth"},
]
sym(jaw_cubes, {"o": [2, 33, -38], "s": [2, 3, 2], "skin": "horn"})

# big flappy ears
ear_cubes = [{"o": [9, 42, -33], "s": [7, 17, 13], "skin": "fur", "rot": [0, 0, -10], "pivot": [10, 52, -24]}]
ear_in_cubes = [{"o": [10, 44, -31], "s": [3, 13, 9], "skin": "skirt", "rot": [0, 0, -10], "pivot": [10, 52, -24]}]

# curved tusks (arc of blocks)
tusk_cubes = [
    {"o": [6, 36, -42], "s": [4, 5, 10], "skin": "tusk"},
    {"o": [6, 32, -50], "s": [4, 5, 9], "skin": "tusk"},
    {"o": [6, 31, -58], "s": [3, 5, 8], "skin": "tusk"},
    {"o": [6, 34, -65], "s": [3, 4, 7], "skin": "tusk"},
    {"o": [6, 40, -70], "s": [3, 3, 6], "skin": "tusk"},
]

# trunk chain
trunk0 = [{"o": [-4, 30, -40], "s": [8, 14, 8], "skin": "fur"}]
trunk1 = [{"o": [-3.5, 18, -40], "s": [7, 12, 7], "skin": "fur"}]
trunk2 = [{"o": [-3, 8, -40], "s": [6, 10, 6], "skin": "fur"}]
trunk3 = [{"o": [-2.5, 2, -40], "s": [5, 6, 5], "skin": "fur"}]
trunk4 = [{"o": [-2, 0, -43], "s": [4, 3, 4], "skin": "skirt"}]
trunk5 = [{"o": [-1.5, 1, -46], "s": [3, 2, 3], "skin": "skirt"}]

tail_cubes = [{"o": [-2.5, 40, 20], "s": [5, 8, 12], "skin": "fur"}]
tail2_cubes = [{"o": [-2, 38, 31], "s": [4, 6, 8], "skin": "skirt", "inflate": 0.3}]

leg_fl = [{"o": [8, 14, -16], "s": [6, 14, 6], "skin": "fur"}]
leg_fr = [{"o": [-14, 14, -16], "s": [6, 14, 6], "skin": "fur"}]
leg_bl = [{"o": [8, 14, 10], "s": [6, 14, 6], "skin": "fur"}]
leg_br = [{"o": [-14, 14, 10], "s": [6, 14, 6], "skin": "fur"}]
shin_fl = [{"o": [8, 0, -15], "s": [6, 14, 6], "skin": "fur"}]
shin_fr = [{"o": [-14, 0, -15], "s": [6, 14, 6], "skin": "fur"}]
shin_bl = [{"o": [8, 0, 11], "s": [6, 14, 6], "skin": "fur"}]
shin_br = [{"o": [-14, 0, 11], "s": [6, 14, 6], "skin": "fur"}]
paw_fl = [{"o": [7, 0, -17], "s": [8, 4, 11], "skin": "fur"}]
paw_fr = [{"o": [-15, 0, -17], "s": [8, 4, 11], "skin": "fur"}]
paw_bl = [{"o": [7, 0, 9], "s": [8, 4, 11], "skin": "fur"}]
paw_br = [{"o": [-15, 0, 9], "s": [8, 4, 11], "skin": "fur"}]
for paw, px, pz in ((paw_fl, 7, -17), (paw_fr, -15, -17), (paw_bl, 7, 9), (paw_br, -15, 9)):
    for i in range(3):
        paw.append({"o": [px + 0.5 + i * 2.5, 0, pz - 1.5], "s": [2, 3, 2], "skin": "hoof"})
    paw.append({"o": [px + 0.5, 0, pz - 2.5], "s": [2, 1, 2], "skin": "hoof"})
    paw.append({"o": [px + 5.5, 0, pz - 2.5], "s": [2, 1, 2], "skin": "hoof"})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 30, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 46, -22], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 40, -30], "cubes": jaw_cubes},
    {"name": "ear_l", "parent": "head", "pivot": [10, 52, -24], "cubes": ear_cubes},
    {"name": "ear_l_in", "parent": "ear_l", "pivot": [10, 52, -24], "cubes": ear_in_cubes},
    {"name": "ear_r", "parent": "head", "pivot": [-10, 52, -24],
     "cubes": [{"o": [-16, 42, -33], "s": [7, 17, 13], "skin": "fur", "rot": [0, 0, 10], "pivot": [-10, 52, -24]}]},
    {"name": "ear_r_in", "parent": "ear_r", "pivot": [-10, 52, -24],
     "cubes": [{"o": [-13, 44, -31], "s": [3, 13, 9], "skin": "skirt", "rot": [0, 0, 10], "pivot": [-10, 52, -24]}]},
    {"name": "tusk_l", "parent": "head", "pivot": [8, 42, -34], "cubes": tusk_cubes},
    {"name": "tusk_r", "parent": "head", "pivot": [-8, 42, -34],
     "cubes": [{"o": [-10, 36, -42], "s": [4, 5, 10], "skin": "tusk"},
               {"o": [-10, 32, -50], "s": [4, 5, 9], "skin": "tusk"},
               {"o": [-9, 31, -58], "s": [3, 5, 8], "skin": "tusk"},
               {"o": [-9, 34, -65], "s": [3, 4, 7], "skin": "tusk"},
               {"o": [-9, 40, -70], "s": [3, 3, 6], "skin": "tusk"}]},
    {"name": "trunk0", "parent": "head", "pivot": [0, 42, -36], "cubes": trunk0},
    {"name": "trunk1", "parent": "trunk0", "pivot": [0, 30, -40], "cubes": trunk1},
    {"name": "trunk2", "parent": "trunk1", "pivot": [0, 18, -40], "cubes": trunk2},
    {"name": "trunk3", "parent": "trunk2", "pivot": [0, 8, -40], "cubes": trunk3},
    {"name": "trunk4", "parent": "trunk3", "pivot": [0, 2, -40], "cubes": trunk4},
    {"name": "trunk5", "parent": "trunk4", "pivot": [0, 1, -42], "cubes": trunk5},
    {"name": "tail", "parent": "body", "pivot": [0, 44, 20], "cubes": tail_cubes},
    {"name": "tail2", "parent": "tail", "pivot": [0, 40, 31], "cubes": tail2_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [11, 26, -13], "cubes": leg_fl},
    {"name": "shin_fl", "parent": "leg_fl", "pivot": [11, 14, -13], "cubes": shin_fl},
    {"name": "paw_fl", "parent": "shin_fl", "pivot": [11, 2, -13], "cubes": paw_fl},
    {"name": "leg_fr", "parent": "body", "pivot": [-11, 26, -13], "cubes": leg_fr},
    {"name": "shin_fr", "parent": "leg_fr", "pivot": [-11, 14, -13], "cubes": shin_fr},
    {"name": "paw_fr", "parent": "shin_fr", "pivot": [-11, 2, -13], "cubes": paw_fr},
    {"name": "leg_bl", "parent": "body", "pivot": [11, 26, 13], "cubes": leg_bl},
    {"name": "shin_bl", "parent": "leg_bl", "pivot": [11, 14, 13], "cubes": shin_bl},
    {"name": "paw_bl", "parent": "shin_bl", "pivot": [11, 2, 13], "cubes": paw_bl},
    {"name": "leg_br", "parent": "body", "pivot": [-11, 26, 13], "cubes": leg_br},
    {"name": "shin_br", "parent": "leg_br", "pivot": [-11, 14, 13], "cubes": shin_br},
    {"name": "paw_br", "parent": "shin_br", "pivot": [-11, 2, 13], "cubes": paw_br},
]

anims = {
    "walk": anim(merge(
        quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", amp=22, freq=30),
        swing({"trunk0": 0, "trunk1": 180}, amp=10, axis=1, freq=30),
        swing({"head": 0}, amp=3, axis=0, freq=30),
    )),
    "idle": anim(merge(
        bob("body", amp=0.7, rate=45),
        sway("trunk1", amp=9, rate=38, axis=1),
        sway("trunk2", amp=12, rate=34, axis=1, off=0.8),
        sway("trunk3", amp=15, rate=30, axis=1, off=1.6),
        sway("trunk4", amp=18, rate=27, axis=1, off=2.4),
        sway("trunk5", amp=22, rate=24, axis=1, off=3.2),
        sway("ear_l", amp=7, rate=70, axis=2, off=0.0),
        sway("ear_r", amp=7, rate=70, axis=2, off=0.0),
        sway("tail", amp=7, rate=40, axis=1),
        sway("tail2", amp=10, rate=34, axis=1, off=1.0),
    )),
    "attack": anim(merge(
        {"trunk0": {"rotation": ["math.sin(variable.attack_time * 180) * 55", "0", "0"]}},
        {"trunk1": {"rotation": ["math.sin(variable.attack_time * 180) * 45", "0", "0"]}},
        {"trunk2": {"rotation": ["math.sin(variable.attack_time * 180) * 35", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 14", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "mammoth",
    "name": "Ember Mammoth",
    "egg": ("#6b4a30", "#ffb347"),
    "glow": True,
    "scale": 1.0,
    "visible": [8, 5, 2.5],
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "skirt": skirt, "tusk": tusk, "eye": ember_eye,
              "wood": wood, "cloth": cloth, "horn": horn, "hoof": hoof, "mouth": mouth},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 120, "speed": 0.16, "damage": 9, "box": [2.6, 3.5],
        "knockback_resist": 0.6, "family": ["mammoth"],
        "ride": {"seats": [[0, 3.45, -2], [0, 3.45, 6]], "jump": 0.35},
        "loot": [("minecraft:leather", 2, 4), ("minecraft:bone", 1, 3)],
        "sound": ("ravager", [0.5, 0.6]),
    },
}
