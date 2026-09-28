"""Sky Raptor - fast rideable feathered dinosaur.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

TEAL   = "#2f7d6b"
TEAL_D = "#1d5548"
TEAL_L = "#5fb49c"
CREAM  = "#f2e6c8"
STRIPE = "#d9a13c"
CREST  = "#e8703a"
CREST2 = "#f6b93b"
BEAK   = "#3a3630"
EYE    = "#ffd94a"
PUPIL  = "#101820"
CLAW   = "#2a2620"
BLOOD  = "#7a2b2b"


def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def feather(p):
    x, y, z = p.p
    # fine feather grain (elongated along z)
    fine = noise3(x * 1.8, y * 1.8, z * 0.7, 13, 1.0)
    patch = noise3(x * 0.6, y * 0.6, z * 0.5, 27, 5.0)
    c = mix(TEAL_D, TEAL_L, 0.25 + 0.7 * patch)
    c = shade(c, 0.80 + 0.40 * fine)
    if y < 15:
        t = min(1.0, (15 - y) / 6.0)
        c = mix(c, CREAM, 0.7 * t)
    if y > 20:
        c = shade(c, 0.88)
    # tiger stripes down the flanks/back
    if p.bone in ("body", "neck", "tail0", "tail1") and y < 21:
        s = math.sin(z * 0.55 + x * 0.12)
        if s > 0.35:
            c = mix(c, STRIPE, 0.65 * min(1.0, (s - 0.35) * 2.2))
    if hash01(int(x * 0.6), int(y * 0.6), int(z * 0.6), 57) > 0.95:
        c = shade(c, 0.80)
    return c


def plume(p):
    x, y, z = p.p
    c = mix(CREST, CREST2, 0.3 + 0.7 * noise3(x, y, z, 71, 2.0))
    return shade(c, 0.85 + 0.3 * grain(p, 1.2, 73))


def beak(p):
    return shade(BEAK, 0.9 + 0.2 * grain(p, 1.4, 81))


def claw(p):
    return shade(CLAW, 0.88 + 0.24 * grain(p, 1.0, 87))


def eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 0.95 and abs(p.y + 0.5 - p.fh / 2) < 0.95:
            return PUPIL
        return EYE
    return shade(EYE, 0.6)


def tooth(p):
    return shade("#efe7d4", 0.9 + 0.2 * grain(p, 1.0, 91))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "feather")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


body_cubes = [
    {"o": [-5, 10, -11], "s": [10, 12, 22], "skin": "feather"},
    {"o": [-6, 10, -13], "s": [12, 11, 7], "skin": "feather"},
    {"o": [-5, 10, 9], "s": [10, 11, 7], "skin": "feather"},
]
# dorsal feather tufts
for zz in (-8, -3, 2, 7):
    body_cubes.append({"o": [-2, 21, zz], "s": [4, 3, 5], "skin": "plume"})
sym(body_cubes, {"o": [4, 12, -4], "s": [3, 6, 10], "skin": "feather", "rot": [0, 0, -12], "pivot": [4, 18, -4]})

neck_cubes = [
    {"o": [-3, 16, -18], "s": [6, 9, 9], "skin": "feather"},
    {"o": [-3, 16, -16], "s": [6, 4, 6], "skin": "plume"},
]

head_cubes = [
    {"o": [-3.5, 19, -27], "s": [7, 8, 11], "skin": "feather"},
    {"o": [-3, 26, -27], "s": [6, 2, 8], "skin": "feather"},
]
sym(head_cubes, {"o": [1, 23, -28], "s": [2, 1, 2], "skin": "beak"})
sym(head_cubes, {"o": [1.5, 23, -27], "s": [2, 2, 2], "skin": "eye"})

jaw_cubes = [
    {"o": [-3, 17, -27], "s": [6, 3, 9], "skin": "feather"},
    {"o": [-2.5, 19.2, -26.4], "s": [5, 1, 8], "skin": "blood"},
]
sym(jaw_cubes, {"o": [0.5, 18, -26], "s": [1, 2, 1], "skin": "tooth"})
sym(jaw_cubes, {"o": [2.5, 18, -25], "s": [1, 2, 1], "skin": "tooth"})
sym(jaw_cubes, {"o": [0.5, 20, -26], "s": [1, 2, 1], "skin": "tooth"})

# feather crest
crest_cubes = [
    {"o": [0, 27, -24], "s": [2, 5, 3], "skin": "plume", "rot": [-30, 0, 0], "pivot": [1, 27, -22]},
    {"o": [0, 27, -20], "s": [2, 6, 3], "skin": "plume", "rot": [-55, 0, 0], "pivot": [1, 27, -19]},
    {"o": [0, 26, -16], "s": [2, 6, 3], "skin": "plume", "rot": [-80, 0, 0], "pivot": [1, 26, -15]},
]
crest_r = [{"o": [-2, 27, -24], "s": [2, 5, 3], "skin": "plume", "rot": [-30, 0, 0], "pivot": [-1, 27, -22]},
           {"o": [-2, 27, -20], "s": [2, 6, 3], "skin": "plume", "rot": [-55, 0, 0], "pivot": [-1, 27, -19]},
           {"o": [-2, 26, -16], "s": [2, 6, 3], "skin": "plume", "rot": [-80, 0, 0], "pivot": [-1, 26, -15]}]

arm_l_cubes = [{"o": [4, 12, -10], "s": [3, 6, 5], "skin": "feather"},
               {"o": [4, 11, -12], "s": [1, 2, 2], "skin": "claw"},
               {"o": [5, 11, -12], "s": [1, 2, 2], "skin": "claw"},
               {"o": [6, 11, -12], "s": [1, 2, 2], "skin": "claw"}]

tail0 = [{"o": [-2.5, 14, 10], "s": [5, 6, 10], "skin": "feather"}]
tail1 = [{"o": [-2, 13, 19], "s": [4, 5, 10], "skin": "feather"},
         {"o": [-1, 17, 21], "s": [2, 4, 6], "skin": "plume", "rot": [-20, 0, 0], "pivot": [0, 17, 20]}]
tail2 = [{"o": [-1.5, 12, 28], "s": [3, 4, 10], "skin": "feather"}]
tail3 = [{"o": [-1, 11, 37], "s": [3, 3, 10], "skin": "feather"},
         {"o": [-1, 13, 40], "s": [2, 3, 7], "skin": "plume", "rot": [-25, 0, 0], "pivot": [0, 13, 39]}]
tail4 = [{"o": [-0.5, 10, 46], "s": [2, 2, 9], "skin": "plume"}]

thigh_l = [{"o": [2, 6, -2], "s": [3, 9, 6], "skin": "feather"},
           {"o": [2, 11, -3], "s": [3, 4, 6], "skin": "feather"}]
thigh_r = [{"o": [-5, 6, -2], "s": [3, 9, 6], "skin": "feather"},
           {"o": [-5, 11, -3], "s": [3, 4, 6], "skin": "feather"}]
shin_l = [{"o": [2, 0, -1], "s": [3, 7, 4], "skin": "feather"}]
shin_r = [{"o": [-5, 0, -1], "s": [3, 7, 4], "skin": "feather"}]
foot_l = [{"o": [1.5, 0, -5], "s": [4, 3, 10], "skin": "feather"}]
foot_r = [{"o": [-5.5, 0, -5], "s": [4, 3, 10], "skin": "feather"}]
for foot, px, sgn in ((foot_l, 1.5, 1), (foot_r, -5.5, 1)):
    for i in range(3):
        foot.append({"o": [px + 0.5 + i * 1.2, 0, -6.2], "s": [1, 2, 2], "skin": "claw"})
    foot.append({"o": [px + 1.0, 1, -7.2], "s": [1, 3, 3], "skin": "claw", "rot": [35, 0, 0], "pivot": [px + 1.5, 1, -6]})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 15, 0], "cubes": body_cubes},
    {"name": "neck", "parent": "body", "pivot": [0, 19, -10], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 23, -17], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 21, -22], "cubes": jaw_cubes},
    {"name": "crest_l", "parent": "head", "pivot": [0, 27, -22], "cubes": crest_cubes},
    {"name": "crest_r", "parent": "head", "pivot": [0, 27, -22], "cubes": crest_r},
    {"name": "arm_l", "parent": "body", "pivot": [5, 17, -8], "cubes": arm_l_cubes},
    {"name": "arm_r", "parent": "body", "pivot": [-5, 17, -8],
     "cubes": [{"o": [-7, 12, -10], "s": [3, 6, 5], "skin": "feather"},
               {"o": [-5, 11, -12], "s": [1, 2, 2], "skin": "claw"},
               {"o": [-6, 11, -12], "s": [1, 2, 2], "skin": "claw"},
               {"o": [-7, 11, -12], "s": [1, 2, 2], "skin": "claw"}]},
    {"name": "tail0", "parent": "body", "pivot": [0, 17, 11], "cubes": tail0},
    {"name": "tail1", "parent": "tail0", "pivot": [0, 16, 19], "cubes": tail1},
    {"name": "tail2", "parent": "tail1", "pivot": [0, 15, 28], "cubes": tail2},
    {"name": "tail3", "parent": "tail2", "pivot": [0, 14, 37], "cubes": tail3},
    {"name": "tail4", "parent": "tail3", "pivot": [0, 13, 46], "cubes": tail4},
    {"name": "thigh_l", "parent": "body", "pivot": [3.5, 14, 1], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [3.5, 6, 1], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [3.5, 0, 1], "cubes": foot_l},
    {"name": "thigh_r", "parent": "body", "pivot": [-3.5, 14, 1], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-3.5, 6, 1], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-3.5, 0, 1], "cubes": foot_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=34, freq=48),
        swing({"shin_l": 180, "shin_r": 0}, amp=16, axis=0, freq=48),
        swing({"tail1": 0, "tail2": 180, "tail3": 0}, amp=8, axis=1, freq=48),
        swing({"neck": 0}, amp=5, axis=0, freq=48),
        swing({"arm_l": 0, "arm_r": 180}, amp=12, axis=0, freq=48),
    )),
    "idle": anim(merge(
        bob("body", amp=0.5, rate=85),
        sway("tail1", amp=7, rate=42, axis=1),
        sway("tail2", amp=10, rate=36, axis=1, off=0.9),
        sway("tail3", amp=14, rate=30, axis=1, off=1.8),
        sway("tail4", amp=18, rate=26, axis=1, off=2.7),
        {"head": {"rotation": ["math.sin(query.life_time * 90) * 4", "math.sin(query.life_time * 47) * 8", "0"]}},
        sway("crest_l", amp=5, rate=110, axis=0, off=0.3),
        sway("crest_r", amp=5, rate=110, axis=0, off=1.4),
        sway("arm_l", amp=6, rate=75, axis=0),
        sway("arm_r", amp=6, rate=75, axis=0),
    )),
    "attack": anim(merge(
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 30", "0", "0"]}},
        {"neck": {"rotation": ["math.sin(variable.attack_time * 180) * 18", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 42", "0", "0"]}},
        {"thigh_l": {"rotation": ["math.sin(variable.attack_time * 180) * -14", "0", "0"]}},
        {"thigh_r": {"rotation": ["math.sin(variable.attack_time * 180) * -14", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "raptor",
    "name": "Sky Raptor",
    "egg": ("#5fb49c", "#d9a13c"),
    "glow": False,
    "scale": 1.0,
    "visible": [5.5, 3, 1.5],
    "bones": bones,
    "skins": {"default": feather, "feather": feather, "plume": plume, "beak": beak,
              "claw": claw, "eye": eye, "tooth": tooth, "blood": lambda p: BLOOD},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 45, "speed": 0.42, "damage": 8, "box": [1.0, 1.9],
        "knockback_resist": 0.1, "family": ["raptor"],
        "ride": {"seats": [[0, 1.45, -1]], "jump": 1.0},
        "loot": [("minecraft:feather", 1, 3), ("minecraft:bone", 0, 2)],
        "sound": ("phantom", [1.3, 1.5]),
    },
}
