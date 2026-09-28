"""Star Fennec - small tameable fox companion with huge ears.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SAND   = "#e8c88a"
SAND_D = "#c9a163"
BACK   = "#c08f4e"
CREAM  = "#f8efd8"
DARK   = "#4a3520"
EARIN  = "#e0a3a8"
NOSE   = "#2b2018"
EYE    = "#3aa0d8"
PUPIL  = "#12100c"


def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def fur(p):
    x, y, z = p.p
    fine = noise3(x * 2.2, y * 2.2, z * 1.2, 23, 1.0)
    patch = noise3(x * 0.8, y * 0.8, z * 0.8, 41, 4.0)
    c = mix(SAND_D, SAND, 0.3 + 0.7 * patch)
    c = shade(c, 0.85 + 0.30 * fine)
    if y < 7:
        t = min(1.0, (7 - y) / 4.0)
        c = mix(c, CREAM, 0.75 * t)
    if y > 9:
        c = mix(c, BACK, 0.35)
    # faint pale banding on the flank
    if p.bone in ("body", "tail0", "tail1"):
        s = math.sin(z * 0.9)
        if s > 0.6:
            c = mix(c, CREAM, 0.25)
    return c


def chest(p):
    return mix(fur(p), CREAM, 0.6 + 0.3 * grain(p, 1.4, 51))


def ear_in(p):
    return mix("#f0c8cc", EARIN, 0.5 + 0.5 * grain(p, 1.5, 61))


def ear_tip(p):
    return mix(DARK, "#6a5238", 0.4 + 0.5 * grain(p, 1.5, 63))


def nose(p):
    return shade(NOSE, 0.9 + 0.2 * grain(p, 1.0, 71))


def eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 0.95 and abs(p.y + 0.5 - p.fh / 2) < 0.95:
            return PUPIL
        return EYE
    return shade(EYE, 0.6)


def paw(p):
    return shade(DARK, 0.9 + 0.25 * grain(p, 1.2, 81))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "fur")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


body_cubes = [
    {"o": [-3.5, 3, -6], "s": [7, 7, 12], "skin": "fur"},
    {"o": [-3, 3, -7], "s": [6, 6, 5], "skin": "fur"},
    {"o": [-3.5, 3, 5], "s": [7, 7, 5], "skin": "fur"},
]
sym(body_cubes, {"o": [3, 4, -3], "s": [2, 5, 6], "skin": "fur", "rot": [0, 0, -10], "pivot": [3, 8, -3]})
sym(body_cubes, {"o": [3, 3, 5], "s": [2, 5, 5], "skin": "fur", "rot": [0, 0, 8], "pivot": [3, 7, 5]})
sym(body_cubes, {"o": [3, 8, -1], "s": [2, 3, 5], "skin": "fur", "rot": [0, 0, -12], "pivot": [3, 9, -1]})
sym(body_cubes, {"o": [3, 7, 6], "s": [2, 3, 4], "skin": "fur", "rot": [0, 0, 10], "pivot": [3, 8, 6]})
body_cubes.append({"o": [-2, 2, 0], "s": [4, 3, 6], "skin": "chest", "inflate": 0.2})

neck_cubes = [
    {"o": [-2.5, 6, -9], "s": [5, 6, 5], "skin": "fur"},
    {"o": [-2, 5, -9], "s": [4, 6, 4], "skin": "chest", "inflate": 0.25},
    {"o": [-3, 5, -8], "s": [6, 4, 4], "skin": "chest", "inflate": 0.25},
]

head_cubes = [
    {"o": [-3, 8, -14], "s": [6, 6, 7], "skin": "fur"},
    {"o": [-3, 13, -14], "s": [6, 1, 5], "skin": "fur"},
    {"o": [-1.5, 8.5, -16], "s": [3, 3, 4], "skin": "fur"},
    {"o": [-1, 10.5, -17], "s": [2, 1, 1], "skin": "nose"},
]
sym(head_cubes, {"o": [1.5, 10, -14], "s": [2, 2, 2], "skin": "eye"})
sym(head_cubes, {"o": [3, 8, -13], "s": [2, 3, 5], "skin": "chest"})

ear_cubes = [{"o": [1.5, 13, -13], "s": [4, 7, 3], "skin": "fur", "rot": [0, 0, -14], "pivot": [3, 13, -11]}]
ear_in_cubes = [{"o": [2, 14, -13], "s": [2, 5, 2], "skin": "ear_in", "rot": [0, 0, -14], "pivot": [3, 13, -11]}]
ear_mid_cubes = [{"o": [1.5, 17, -13], "s": [3, 3, 3], "skin": "fur", "rot": [0, 0, -14], "pivot": [3, 13, -11]}]
ear_tip_cubes = [{"o": [1.5, 19, -13], "s": [3, 2, 3], "skin": "ear_tip", "rot": [0, 0, -14], "pivot": [3, 13, -11]}]

tail0_cubes = [{"o": [-2.5, 4, 6], "s": [5, 6, 8], "skin": "fur", "inflate": 0.3}]
tail1_cubes = [{"o": [-2, 3, 13], "s": [4, 6, 9], "skin": "fur", "inflate": 0.3},
               {"o": [-3, 6, 16], "s": [6, 3, 6], "skin": "fur", "inflate": 0.25}]
tail2_cubes = [{"o": [-1.5, 2, 21], "s": [3, 5, 7], "skin": "fur", "inflate": 0.25}]
tail3_cubes = [{"o": [-1, 1, 27], "s": [2, 3, 5], "skin": "ear_tip", "inflate": 0.2}]

leg_fl = [{"o": [1.5, 0, -5], "s": [2, 5, 3], "skin": "fur"}]
leg_fr = [{"o": [-3.5, 0, -5], "s": [2, 5, 3], "skin": "fur"}]
leg_bl = [{"o": [1.5, 0, 3], "s": [2, 5, 3], "skin": "fur"}]
leg_br = [{"o": [-3.5, 0, 3], "s": [2, 5, 3], "skin": "fur"}]
paw_fl = [{"o": [1, 0, -6.5], "s": [3, 2, 4], "skin": "paw"}]
paw_fr = [{"o": [-4, 0, -6.5], "s": [3, 2, 4], "skin": "paw"}]
paw_bl = [{"o": [1, 0, 1.5], "s": [3, 2, 4], "skin": "paw"}]
paw_br = [{"o": [-4, 0, 1.5], "s": [3, 2, 4], "skin": "paw"}]
for pc, px, pz in ((paw_fl, 1, -6.5), (paw_fr, -4, -6.5), (paw_bl, 1, 1.5), (paw_br, -4, 1.5)):
    for i in range(3):
        pc.append({"o": [px + 0.4 + i * 0.9, 0, pz - 1.2], "s": [1, 2, 1], "skin": "paw"})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 7, 0], "cubes": body_cubes},
    {"name": "neck", "parent": "body", "pivot": [0, 9, -5], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 11, -8], "cubes": head_cubes},
    {"name": "ear_l", "parent": "head", "pivot": [3, 13, -11], "cubes": ear_cubes},
    {"name": "ear_l_in", "parent": "ear_l", "pivot": [3, 13, -11], "cubes": ear_in_cubes},
    {"name": "ear_l_mid", "parent": "ear_l", "pivot": [3, 13, -11], "cubes": ear_mid_cubes},
    {"name": "ear_l_tip", "parent": "ear_l", "pivot": [3, 13, -11], "cubes": ear_tip_cubes},
    {"name": "ear_r", "parent": "head", "pivot": [-3, 13, -11],
     "cubes": [{"o": [-5.5, 13, -13], "s": [4, 7, 3], "skin": "fur", "rot": [0, 0, 14], "pivot": [-3, 13, -11]}]},
    {"name": "ear_r_in", "parent": "ear_r", "pivot": [-3, 13, -11],
     "cubes": [{"o": [-4, 14, -13], "s": [2, 5, 2], "skin": "ear_in", "rot": [0, 0, 14], "pivot": [-3, 13, -11]}]},
    {"name": "ear_r_mid", "parent": "ear_r", "pivot": [-3, 13, -11],
     "cubes": [{"o": [-4.5, 17, -13], "s": [3, 3, 3], "skin": "fur", "rot": [0, 0, 14], "pivot": [-3, 13, -11]}]},
    {"name": "ear_r_tip", "parent": "ear_r", "pivot": [-3, 13, -11],
     "cubes": [{"o": [-4.5, 19, -13], "s": [3, 2, 3], "skin": "ear_tip", "rot": [0, 0, 14], "pivot": [-3, 13, -11]}]},
    {"name": "tail0", "parent": "body", "pivot": [0, 6, 6], "cubes": tail0_cubes},
    {"name": "tail1", "parent": "tail0", "pivot": [0, 6, 13], "cubes": tail1_cubes},
    {"name": "tail2", "parent": "tail1", "pivot": [0, 5, 21], "cubes": tail2_cubes},
    {"name": "tail3", "parent": "tail2", "pivot": [0, 4, 27], "cubes": tail3_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [2.5, 5, -4], "cubes": leg_fl},
    {"name": "paw_fl", "parent": "leg_fl", "pivot": [2.5, 1, -4], "cubes": paw_fl},
    {"name": "leg_fr", "parent": "body", "pivot": [-2.5, 5, -4], "cubes": leg_fr},
    {"name": "paw_fr", "parent": "leg_fr", "pivot": [-2.5, 1, -4], "cubes": paw_fr},
    {"name": "leg_bl", "parent": "body", "pivot": [2.5, 5, 4], "cubes": leg_bl},
    {"name": "paw_bl", "parent": "leg_bl", "pivot": [2.5, 1, 4], "cubes": paw_bl},
    {"name": "leg_br", "parent": "body", "pivot": [-2.5, 5, 4], "cubes": leg_br},
    {"name": "paw_br", "parent": "leg_br", "pivot": [-2.5, 1, 4], "cubes": paw_br},
]

anims = {
    "walk": anim(merge(
        quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", amp=32, freq=54),
        swing({"tail0": 0, "tail1": 180, "tail2": 0}, amp=9, axis=1, freq=54),
        swing({"neck": 0}, amp=4, axis=0, freq=54),
        bob("body", amp=0.4, rate=140),
    )),
    "idle": anim(merge(
        bob("body", amp=0.3, rate=80),
        sway("tail0", amp=6, rate=40, axis=1),
        sway("tail1", amp=9, rate=34, axis=1, off=0.8),
        sway("tail2", amp=13, rate=29, axis=1, off=1.6),
        sway("tail3", amp=16, rate=25, axis=1, off=2.4),
        {"head": {"rotation": ["math.sin(query.life_time * 55) * 3", "math.sin(query.life_time * 27) * 20", "0"]}},
        sway("ear_l", amp=8, rate=150, axis=2, off=0.0),
        sway("ear_r", amp=8, rate=150, axis=2, off=0.0),
        {"neck": {"rotation": ["math.sin(query.life_time * 60) * 2", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 26", "0", "0"]}},
        {"neck": {"rotation": ["math.sin(variable.attack_time * 180) * 16", "0", "0"]}},
        {"leg_fl": {"rotation": ["math.sin(variable.attack_time * 180) * -20", "0", "0"]}},
        {"leg_fr": {"rotation": ["math.sin(variable.attack_time * 180) * -20", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "fennec",
    "name": "Star Fennec",
    "egg": ("#e8c88a", "#4a3520"),
    "glow": False,
    "scale": 1.0,
    "visible": [3.5, 2, 1.0],
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "chest": chest, "ear_in": ear_in, "ear_tip": ear_tip,
              "nose": nose, "eye": eye, "paw": paw},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "companion",
        "health": 12, "speed": 0.38, "box": [0.6, 1.0], "family": ["fennec"],
        "tame_items": ["minecraft:sweet_berries"],
        "loot": [("minecraft:sweet_berries", 0, 1)],
        "sound": ("fox", [1.15, 1.3]),
    },
}
