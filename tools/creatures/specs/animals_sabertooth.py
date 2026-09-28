"""Glacier Sabertooth - big rideable snow-cat mount.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SNOW   = "#eef6ff"
ICE    = "#c3d6e8"
DEEP   = "#7f9cba"
STRIPE = "#3d6288"
BELLY  = "#f8fcff"
NOSE   = "#22303e"
EYE    = "#ffd23f"
PUPIL  = "#0e1620"
TOOTH  = "#f3efe4"
CLAW   = "#2c3038"
TUFT   = "#f6fbff"
TONGUE = "#c76a78"


# ----------------------------------------------------------------- painters
def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def fur(p):
    x, y, z = p.p
    g = grain(p, 2.2, 11)
    patch = grain(p, 5.5, 23)
    c = mix(DEEP, SNOW, 0.35 + 0.65 * patch)
    c = shade(c, 0.85 + 0.30 * g)
    if y < 12:
        t = min(1.0, (12 - y) / 7.0)
        c = mix(c, BELLY, 0.7 * t)
    if y > 18:
        c = shade(c, 0.90)
    if p.bone in ("body", "neck") and y < 19.5:
        s = math.sin(z * 0.70 + x * 0.06)
        if s > 0.5:
            c = mix(c, STRIPE, 0.60 * min(1.0, (s - 0.5) * 3))
    if p.bone == "body" and -9 < z < -3 and 12 < y < 17 and abs((y - 14.5) - 0.55 * (z + 6)) < 0.8:
        c = mix(c, "#e2b9b9", 0.45)
    if hash01(int(x * 0.7), int(y * 0.7), int(z * 0.7), 91) > 0.972:
        c = shade(c, 0.78)
    return c


def ruff(p):
    return mix(fur(p), "#ffffff", 0.20 + 0.40 * grain(p, 1.6, 41))


def tailtip(p):
    return mix(fur(p), "#2f3742", 0.55 + 0.35 * grain(p, 2.0, 55))


def ear_in(p):
    return mix(fur(p), "#d8a7b0", 0.6)


def tuft(p):
    return mix(fur(p), TUFT, 0.55 + 0.30 * grain(p, 1.4, 47))


def tooth(p):
    return shade(TOOTH, 0.88 + 0.16 * grain(p, 1.2, 61))


def claw(p):
    return shade(CLAW, 0.9 + 0.2 * grain(p, 1.0, 71))


def eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 0.95 and abs(p.y + 0.5 - p.fh / 2) < 0.95:
            return PUPIL
        return EYE
    return shade(EYE, 0.55)


def nose(p):
    return shade(NOSE, 0.9 + 0.2 * grain(p, 1.0, 81))


def mouth(p):
    return TONGUE


def pads(p):
    return shade("#3b3238", 0.9 + 0.2 * grain(p, 1.0, 91))


# ----------------------------------------------------------------- cubes
def sym(cubes, c):
    """Append cube c and its explicit X mirror (framework forbids the 'mirror' flag)."""
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "fur")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


body_cubes = []
# torso + bulk
body_cubes.append({"o": [-7, 9, -13], "s": [14, 11, 26], "skin": "fur"})
body_cubes.append({"o": [-8, 8, -14], "s": [16, 12, 10], "skin": "fur"})
body_cubes.append({"o": [-8, 8, 4], "s": [16, 12, 10], "skin": "fur"})
# spine ridge plates
for zz in (-9, -2, 5):
    body_cubes.append({"o": [-2, 20, zz], "s": [4, 2, 5], "skin": "fur"})
# shoulder muscle plates (tilted)
sym(body_cubes, {"o": [5, 12, -10], "s": [4, 6, 7], "skin": "fur", "rot": [0, 0, -14], "pivot": [5, 12, -10]})
# haunch plates
sym(body_cubes, {"o": [6, 11, 5], "s": [4, 6, 7], "skin": "fur", "rot": [0, 0, 10], "pivot": [6, 11, 5]})

neck_cubes = [
    {"o": [-4, 13, -21], "s": [8, 9, 9], "skin": "fur"},
    {"o": [-6, 11, -21], "s": [12, 10, 4], "skin": "ruff", "inflate": 0.35},
]
sym(neck_cubes, {"o": [5, 11, -20], "s": [3, 10, 5], "skin": "ruff", "inflate": 0.35})

head_cubes = [
    {"o": [-4, 14, -31], "s": [9, 9, 12], "skin": "fur"},
    {"o": [-4, 22, -31], "s": [8, 2, 7], "skin": "fur"},
    {"o": [-3, 14, -36], "s": [5, 6, 7], "skin": "fur"},
    {"o": [-1.5, 18, -37], "s": [3, 2, 2], "skin": "nose"},
]
sym(head_cubes, {"o": [1.5, 19, -33], "s": [3, 3, 3], "skin": "eye"})
sym(head_cubes, {"o": [3, 21, -31], "s": [2, 4, 6], "skin": "fur", "rot": [0, 0, -18], "pivot": [3, 21, -31]})
# cheek tufts
sym(head_cubes, {"o": [3, 15, -34], "s": [2, 3, 6], "skin": "tuft"})

jaw_cubes = [
    {"o": [-2.5, 11, -35], "s": [5, 3, 8], "skin": "fur"},
    {"o": [-2, 13.2, -34.4], "s": [4, 1, 7], "skin": "mouth"},
]
sym(jaw_cubes, {"o": [1.5, 9, -34], "s": [1, 3, 1], "skin": "tooth"})

# huge curved sabers, three segments each
fang_cubes = [{"o": [1.5, 10, -34], "s": [2, 6, 2], "skin": "tooth", "rot": [-8, 0, 0], "pivot": [2.5, 14, -34]}]
fang2_cubes = [{"o": [1.5, 7, -33], "s": [2, 5, 2], "skin": "tooth", "rot": [-14, 0, 0], "pivot": [2.5, 10, -34]}]
fang3_cubes = [{"o": [1.5, 5, -31], "s": [2, 3, 2], "skin": "tooth", "rot": [-24, 0, 0], "pivot": [2.5, 7, -33]}]

ear_cubes = [{"o": [2, 22, -27], "s": [3, 3, 3], "skin": "fur", "rot": [0, 0, -16], "pivot": [2, 22, -27]}]
tuft_cubes = [{"o": [2, 24, -26.5], "s": [2, 3, 2], "skin": "tuft", "rot": [0, 0, -24], "pivot": [2, 24, -27]}]

tail0_cubes = [{"o": [-2.5, 14, 12], "s": [5, 6, 10], "skin": "fur"}]
tail1_cubes = [{"o": [-2, 13, 21], "s": [4, 5, 9], "skin": "fur"}]
tail2_cubes = [{"o": [-1.5, 11, 29], "s": [3, 4, 9], "skin": "fur"}]
tail3_cubes = [{"o": [-1, 9, 37], "s": [2, 3, 8], "skin": "tailtip"}]

leg_fl_cubes = [{"o": [2.5, 3, -11], "s": [4, 10, 6], "skin": "fur"}]
leg_fr_cubes = [{"o": [-6.5, 3, -11], "s": [4, 10, 6], "skin": "fur"}]
leg_bl_cubes = [{"o": [2.5, 3, 6], "s": [4, 10, 6], "skin": "fur"}]
leg_br_cubes = [{"o": [-6.5, 3, 6], "s": [4, 10, 6], "skin": "fur"}]
shin_fl = [{"o": [2.5, 0, -10], "s": [3, 4, 4], "skin": "fur"}]
shin_fr = [{"o": [-5.5, 0, -10], "s": [3, 4, 4], "skin": "fur"}]
shin_bl = [{"o": [2.5, 0, 7], "s": [3, 4, 4], "skin": "fur"}]
shin_br = [{"o": [-5.5, 0, 7], "s": [3, 4, 4], "skin": "fur"}]

paw_fl = [{"o": [2, 0, -13], "s": [5, 3, 7], "skin": "fur"}]
paw_fr = [{"o": [-7, 0, -13], "s": [5, 3, 7], "skin": "fur"}]
paw_bl = [{"o": [2, 0, 6], "s": [5, 3, 7], "skin": "fur"}]
paw_br = [{"o": [-7, 0, 6], "s": [5, 3, 7], "skin": "fur"}]
# toes + claws on each paw (front edge of paw)
for px, pz in ((2, -13), (-7, -13), (2, 6), (-7, 6)):
    for i in range(3):
        tx = px + 0.4 + i * 1.5
        cubes = {(-13): paw_fl, (6): paw_bl}.get(pz) if px > 0 else ({(-13): paw_fr, (6): paw_br}.get(pz))
        cubes.append({"o": [tx, 0, pz - 1.2], "s": [1, 2, 1], "skin": "pads"})
        cubes.append({"o": [tx, 0, pz - 2.0], "s": [1, 1, 1], "skin": "claw"})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 13, 0], "cubes": body_cubes},
    {"name": "neck", "parent": "body", "pivot": [0, 16, -13], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 19, -20], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 14, -27], "cubes": jaw_cubes},
    {"name": "fang_l", "parent": "head", "pivot": [2.5, 14, -34], "cubes": fang_cubes},
    {"name": "fang_l2", "parent": "fang_l", "pivot": [2.5, 10, -34], "cubes": fang2_cubes},
    {"name": "fang_l3", "parent": "fang_l2", "pivot": [2.5, 7, -33], "cubes": fang3_cubes},
    {"name": "fang_r", "parent": "head", "pivot": [-2.5, 14, -34],
     "cubes": [{"o": [-3.5, 10, -34], "s": [2, 6, 2], "skin": "tooth", "rot": [-8, 0, 0], "pivot": [-2.5, 14, -34]}]},
    {"name": "fang_r2", "parent": "fang_r", "pivot": [-2.5, 10, -34],
     "cubes": [{"o": [-3.5, 7, -33], "s": [2, 5, 2], "skin": "tooth", "rot": [-14, 0, 0], "pivot": [-2.5, 10, -34]}]},
    {"name": "fang_r3", "parent": "fang_r2", "pivot": [-2.5, 7, -33],
     "cubes": [{"o": [-3.5, 5, -31], "s": [2, 3, 2], "skin": "tooth", "rot": [-24, 0, 0], "pivot": [-2.5, 7, -33]}]},
    {"name": "ear_l", "parent": "head", "pivot": [3.5, 23, -24], "cubes": ear_cubes},
    {"name": "tuft_l", "parent": "ear_l", "pivot": [3, 25, -27], "cubes": tuft_cubes},
    {"name": "ear_r", "parent": "head", "pivot": [-3.5, 23, -24],
     "cubes": [{"o": [-5, 22, -27], "s": [3, 3, 3], "skin": "fur", "rot": [0, 0, 16], "pivot": [-2, 22, -27]}]},
    {"name": "tuft_r", "parent": "ear_r", "pivot": [-3, 25, -27],
     "cubes": [{"o": [-4, 24, -26.5], "s": [2, 3, 2], "skin": "tuft", "rot": [0, 0, 24], "pivot": [-2, 24, -27]}]},
    {"name": "tail0", "parent": "body", "pivot": [0, 15, 13], "cubes": tail0_cubes},
    {"name": "tail1", "parent": "tail0", "pivot": [0, 16, 21], "cubes": tail1_cubes},
    {"name": "tail2", "parent": "tail1", "pivot": [0, 14, 29], "cubes": tail2_cubes},
    {"name": "tail3", "parent": "tail2", "pivot": [0, 12, 37], "cubes": tail3_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [4.5, 12, -9], "cubes": leg_fl_cubes},
    {"name": "shin_fl", "parent": "leg_fl", "pivot": [4.5, 3, -9], "cubes": shin_fl},
    {"name": "paw_fl", "parent": "shin_fl", "pivot": [4.5, 1, -9], "cubes": paw_fl},
    {"name": "leg_fr", "parent": "body", "pivot": [-4.5, 12, -9], "cubes": leg_fr_cubes},
    {"name": "shin_fr", "parent": "leg_fr", "pivot": [-4.5, 3, -9], "cubes": shin_fr},
    {"name": "paw_fr", "parent": "shin_fr", "pivot": [-4.5, 1, -9], "cubes": paw_fr},
    {"name": "leg_bl", "parent": "body", "pivot": [4.5, 12, 8], "cubes": leg_bl_cubes},
    {"name": "shin_bl", "parent": "leg_bl", "pivot": [4.5, 3, 8], "cubes": shin_bl},
    {"name": "paw_bl", "parent": "shin_bl", "pivot": [4.5, 1, 8], "cubes": paw_bl},
    {"name": "leg_br", "parent": "body", "pivot": [-4.5, 12, 8], "cubes": leg_br_cubes},
    {"name": "shin_br", "parent": "leg_br", "pivot": [-4.5, 3, 8], "cubes": shin_br},
    {"name": "paw_br", "parent": "shin_br", "pivot": [-4.5, 1, 8], "cubes": paw_br},
]

anims = {
    "walk": anim(merge(
        quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", amp=30, freq=42),
        swing({"tail1": 0, "tail2": 180}, amp=7, axis=1, freq=42),
        swing({"neck": 0, "head": 180}, amp=4, axis=0, freq=42),
    )),
    "idle": anim(merge(
        bob("body", amp=0.45, rate=70),
        sway("tail1", amp=5, rate=45, axis=1),
        sway("tail2", amp=9, rate=38, axis=1, off=1.0),
        sway("tail3", amp=13, rate=31, axis=1, off=2.1),
        sway("ear_l", amp=6, rate=140, axis=2, off=0.4),
        sway("ear_r", amp=6, rate=140, axis=2, off=2.4),
        {"jaw": {"rotation": ["math.sin(query.life_time * 55) * 3", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 24", "0", "0"]}},
        {"neck": {"rotation": ["math.sin(variable.attack_time * 180) * 14", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 38", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "sabertooth",
    "name": "Glacier Sabertooth",
    "egg": ("#d9e6f2", "#3a5a7a"),
    "glow": False,
    "scale": 1.0,
    "visible": [5.5, 2.5, 1.25],
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "ruff": ruff, "tailtip": tailtip, "tuft": tuft,
              "ear_in": ear_in, "tooth": tooth, "claw": claw, "eye": eye, "nose": nose,
              "mouth": mouth, "pads": pads},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 40, "speed": 0.34, "damage": 7, "box": [1.2, 1.4],
        "knockback_resist": 0.25, "family": ["cat"],
        "ride": {"seats": [[0, 1.25, 0.2]], "jump": 0.8},
        "loot": [("minecraft:leather", 1, 3), ("minecraft:bone", 0, 2)],
        "sound": ("polarbear", [0.8, 0.9]),
        "spawn": {"biomes": ["frozen"], "weight": 2, "herd": [1, 2]},
    },
}
