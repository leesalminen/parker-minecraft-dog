"""Zombie Brute - hulking ~2.6-block undead bruiser with chained fists.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SKIN    = "#5b6b46"
SKIN_D  = "#3b4529"
SKIN_L  = "#828f5e"
VEIN    = "#6a3a3a"
GRIME   = "#28271d"
BLOOD   = "#6e2020"
CLOTH   = "#4a4235"
CLOTH_D = "#2c271d"
RUST    = "#6b4326"
RUST_L  = "#93613a"
METAL   = "#46464a"
BONE    = "#d6cda9"
BONE_D  = "#9c9474"
GASH    = "#a4d84a"
EYE     = "#cde26a"
TOOTH   = "#cfc7a6"


# ----------------------------------------------------------------- painters
def n(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def skin(p):
    x, y, z = p.p
    g = n(p, 2.6, 11)
    patch = n(p, 7.0, 23)
    c = mix(SKIN_D, SKIN_L, 0.20 + 0.80 * patch)
    c = shade(c, 0.78 + 0.44 * g)
    if y < 26:                                   # grime toward the ground
        c = mix(c, GRIME, 0.40 * min(1.0, (26 - y) / 14.0))
    if y > 33:                                   # lighter shoulder tops
        c = shade(c, 1.06)
    v = math.sin(x * 0.85 + z * 0.65 + y * 0.28)  # veins, continuous across cubes
    if v > 0.84:
        c = mix(c, VEIN, 0.30 + 0.35 * (v - 0.84) * 6)
    if hash01(int(x * 1.4), int(y * 1.4), int(z * 1.4), 91) > 0.962:
        c = mix(c, BLOOD, 0.55)                   # blood speckle
    if p.bone in ("body", "head") and 20 < y < 36:  # long stitched scar down the chest
        if abs(x + 0.6 * (z + 5) - 1.0) < 0.7 and hash01(0, int(y * 2.0), 0, 77) > 0.4:
            c = mix(c, "#8f6060", 0.55)
    if p.bone in ("thigh_l", "thigh_r", "shin_l", "shin_r") and y < 14:
        c = mix(c, CLOTH_D, 0.25)                 # dirt on the legs
    return c


def cloth(p):
    x, y, z = p.p
    g = n(p, 3.0, 41)
    c = mix(CLOTH_D, CLOTH, 0.30 + 0.70 * g)
    weave = (math.floor(x * 0.6) + math.floor(y * 0.6)) % 2
    c = shade(c, 0.80 if weave else 1.14)
    if hash01(int(x), int(y), int(z), 53) > 0.93:
        c = shade(c, 0.66)                        # torn hole
    return c


def metal(p):
    x, y, z = p.p
    r = n(p, 2.2, 61)
    c = mix(METAL, RUST, 0.30 + 0.60 * r)
    c = shade(c, 0.82 + 0.32 * n(p, 1.3, 63))
    if p.face in ("front", "back", "east", "west") and (p.y % 6) < 1:
        c = shade(c, 0.70)                        # panel seam
    if hash01(int(x * 2.0), int(y * 2.0), int(z * 2.0), 67) > 0.90:
        c = mix(c, RUST_L, 0.7)                   # flaking rust
    return c


def bone(p):
    c = mix(BONE_D, BONE, 0.3 + 0.7 * n(p, 1.6, 71))
    if hash01(int(p.p[0] * 2), int(p.p[1] * 2), int(p.p[2] * 2), 73) > 0.88:
        c = shade(c, 0.80)
    return c


def tooth(p):
    return shade(TOOTH, 0.85 + 0.25 * n(p, 1.2, 81))


def gash(p):
    x, y, z = p.p
    t = 0.35 + 0.65 * n(p, 1.6, 87)
    c = mix("#6f8a1e", GASH, t)
    if math.sin(x * 1.3 + y * 1.1) > 0.55:
        c = mix(c, "#e7ff9a", 0.6)
    return glow(c)


def eye(p):
    if p.face == "front" and abs(p.x + 0.5 - p.fw / 2) < 0.8 and abs(p.y + 0.5 - p.fh / 2) < 0.8:
        return glow("#e9ffb0")
    return glow(shade(EYE, 0.6))


# ----------------------------------------------------------------- cubes
def sym(cubes, c):
    """Append cube c plus its explicit X mirror (framework forbids the 'mirror' flag)."""
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "skin")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- body
body_cubes = [
    {"o": [-7, 19, -4], "s": [14, 7, 9], "skin": "cloth"},     # pelvis / torn pants top
    {"o": [-9, 26, -5], "s": [18, 8, 12], "skin": "skin"},     # torso
    {"o": [-13, 31, -5], "s": [26, 6, 12], "skin": "skin"},    # massive shoulder girdle
    {"o": [-9, 33, 4], "s": [18, 5, 7], "skin": "skin"},       # back hump
    {"o": [-7, 21, -8], "s": [14, 7, 5], "skin": "skin"},      # gut
    {"o": [-2, 34, -3], "s": [4, 5, 5], "skin": "skin"},       # thick neck stump
    {"o": [-3, 24, -8.4], "s": [6, 3, 1], "skin": "gash"},     # belly gash (glow)
]
# burst ribs poking through the chest
for rx in (-6, -2, 2):
    body_cubes.append({"o": [rx, 27, -8.6], "s": [2, 2, 1], "skin": "bone"})
body_cubes.append({"o": [-6, 26, -8.6], "s": [2, 4, 1], "skin": "bone"})
# stitched wound on the back
body_cubes.append({"o": [-4, 32, 10.6], "s": [8, 2, 1], "skin": "gash"})
# shoulder muscle knots
sym(body_cubes, {"o": [9, 29, -7], "s": [4, 6, 6], "skin": "skin", "rot": [0, 0, -16], "pivot": [9, 29, -7]})

# ----------------------------------------------------------------- head (tiny, perched on the shoulder girdle)
head_cubes = [
    {"o": [-3, 36, -5], "s": [6, 6, 7], "skin": "skin"},
    {"o": [-3, 40, -6], "s": [6, 2, 2], "skin": "skin"},        # heavy brow
    {"o": [-2, 42, -4], "s": [4, 1, 4], "skin": "skin"},        # bald scalp scar
    {"o": [-1, 34, -3], "s": [2, 3, 4], "skin": "bone"},        # exposed vertebra
]
sym(head_cubes, {"o": [1, 38, -6], "s": [2, 2, 1], "skin": "eye"})

jaw_cubes = [
    {"o": [-2, 33, -6], "s": [4, 3, 5], "skin": "skin"},
    {"o": [-2, 33, -7], "s": [4, 1, 1], "skin": "tooth"},       # teeth row
    {"o": [-2, 31, -7.2], "s": [4, 1, 1], "skin": "skin"},
]
sym(jaw_cubes, {"o": [1, 30, -7], "s": [1, 3, 1], "skin": "tooth"})   # dangling tusks

# ----------------------------------------------------------------- spiked shoulder pad (left only)
pad_l_cubes = [
    {"o": [8, 37, -6], "s": [9, 4, 12], "skin": "metal"},
    {"o": [17, 38, -2], "s": [2, 4, 8], "skin": "metal"},       # side skirt
]
pad_l_cubes.append({"o": [10, 41, -4], "s": [2, 3, 2], "skin": "metal", "rot": [0, 0, -12], "pivot": [11, 41, -4]})
pad_l_cubes.append({"o": [14, 41, -1], "s": [2, 3, 2], "skin": "metal", "rot": [0, 0, -12], "pivot": [15, 41, -1]})
pad_l_cubes.append({"o": [12, 41, 3], "s": [2, 3, 2], "skin": "metal", "rot": [0, 0, -12], "pivot": [13, 41, 3]})
pad_r_cubes = [
    {"o": [-13, 37, -6], "s": [5, 4, 12], "skin": "metal"},
]

# ----------------------------------------------------------------- arms
arm_l_cubes = [
    {"o": [12, 21, -3], "s": [6, 14, 6], "skin": "skin"},       # upper arm
    {"o": [11, 23, -3], "s": [8, 8, 7], "skin": "skin"},        # bicep bulge
]
arm_r_cubes = [
    {"o": [-18, 21, -3], "s": [6, 14, 6], "skin": "skin"},
    {"o": [-19, 23, -3], "s": [8, 8, 7], "skin": "skin"},
]
fore_l_cubes = [
    {"o": [11, 10, -4], "s": [7, 12, 7], "skin": "skin"},
    {"o": [10, 12, -5], "s": [9, 3, 9], "skin": "metal"},       # rusty manacle band
    {"o": [10, 15, -5], "s": [9, 2, 9], "skin": "metal"},
]
fore_r_cubes = [
    {"o": [-18, 10, -4], "s": [7, 12, 7], "skin": "skin"},
    {"o": [-19, 12, -5], "s": [9, 3, 9], "skin": "metal"},
    {"o": [-19, 15, -5], "s": [9, 2, 9], "skin": "metal"},
]
fist_l_cubes = [
    {"o": [9, 2, -6], "s": [11, 8, 11], "skin": "skin"},        # oversized fist
    {"o": [9, 4, -6], "s": [11, 1, 11], "skin": "metal"},       # chain wrap
    {"o": [9, 8, -6], "s": [11, 1, 11], "skin": "metal"},
]
for i in range(3):
    fist_l_cubes.append({"o": [10 + i * 3, 2, -7], "s": [2, 2, 1], "skin": "bone"})   # knuckle spikes
fist_r_cubes = [
    {"o": [-20, 2, -6], "s": [11, 8, 11], "skin": "skin"},
    {"o": [-20, 4, -6], "s": [11, 1, 11], "skin": "metal"},
    {"o": [-20, 8, -6], "s": [11, 1, 11], "skin": "metal"},
]
for i in range(3):
    fist_r_cubes.append({"o": [-12 - i * 3, 2, -7], "s": [2, 2, 1], "skin": "bone"})

chain_l_cubes = [
    {"o": [9, 0, -8], "s": [2, 2, 2], "skin": "metal"},
    {"o": [13, 0, -8], "s": [2, 2, 2], "skin": "metal"},
    {"o": [9, 0, -1], "s": [2, 2, 2], "skin": "metal"},
]
chain_r_cubes = [
    {"o": [-21, 0, -8], "s": [2, 2, 2], "skin": "metal"},
    {"o": [-17, 0, -8], "s": [2, 2, 2], "skin": "metal"},
    {"o": [-21, 0, -1], "s": [2, 2, 2], "skin": "metal"},
]

# ----------------------------------------------------------------- legs
thigh_l_cubes = [
    {"o": [3, 11, -3], "s": [5, 8, 6], "skin": "cloth"},
    {"o": [2, 12, -4], "s": [7, 4, 8], "skin": "cloth"},        # torn pant cuff
]
thigh_r_cubes = [
    {"o": [-8, 11, -3], "s": [5, 8, 6], "skin": "cloth"},
    {"o": [-9, 12, -4], "s": [7, 4, 8], "skin": "cloth"},
]
shin_l_cubes = [
    {"o": [3, 4, -3], "s": [4, 7, 5], "skin": "skin"},
    {"o": [2, 6, -5], "s": [2, 2, 2], "skin": "bone"},          # shin bone poking out
]
shin_r_cubes = [
    {"o": [-7, 4, -3], "s": [4, 7, 5], "skin": "skin"},
    {"o": [-4, 6, -5], "s": [2, 2, 2], "skin": "bone"},
]
foot_l_cubes = [
    {"o": [3, 0, -5], "s": [5, 4, 8], "skin": "skin"},
    {"o": [3, 0, -7], "s": [5, 2, 2], "skin": "bone"},          # splayed toes
]
foot_r_cubes = [
    {"o": [-8, 0, -5], "s": [5, 4, 8], "skin": "skin"},
    {"o": [-8, 0, -7], "s": [5, 2, 2], "skin": "bone"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 30, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 38, -1], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 36, -5], "cubes": jaw_cubes},
    {"name": "pad_l", "parent": "body", "pivot": [12, 39, -1], "cubes": pad_l_cubes},
    {"name": "pad_r", "parent": "body", "pivot": [-11, 39, -1], "cubes": pad_r_cubes},
    {"name": "arm_l", "parent": "body", "pivot": [15, 35, -1], "rotation": [-72, 0, -10], "cubes": arm_l_cubes},
    {"name": "fore_l", "parent": "arm_l", "pivot": [15, 22, -1], "cubes": fore_l_cubes},
    {"name": "fist_l", "parent": "fore_l", "pivot": [15, 10, -1], "cubes": fist_l_cubes},
    {"name": "chain_l", "parent": "fist_l", "pivot": [15, 4, -5], "cubes": chain_l_cubes},
    {"name": "arm_r", "parent": "body", "pivot": [-15, 35, -1], "rotation": [-72, 0, 10], "cubes": arm_r_cubes},
    {"name": "fore_r", "parent": "arm_r", "pivot": [-15, 22, -1], "cubes": fore_r_cubes},
    {"name": "fist_r", "parent": "fore_r", "pivot": [-15, 10, -1], "cubes": fist_r_cubes},
    {"name": "chain_r", "parent": "fist_r", "pivot": [-15, 4, -5], "cubes": chain_r_cubes},
    {"name": "thigh_l", "parent": "body", "pivot": [5.5, 19, 0], "cubes": thigh_l_cubes},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [5.5, 11, 0], "cubes": shin_l_cubes},
    {"name": "foot_l", "parent": "shin_l", "pivot": [5.5, 4, -1], "cubes": foot_l_cubes},
    {"name": "thigh_r", "parent": "body", "pivot": [-5.5, 19, 0], "cubes": thigh_r_cubes},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-5.5, 11, 0], "cubes": shin_r_cubes},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-5.5, 4, -1], "cubes": foot_r_cubes},
]


def arm_swing(bone, ph, base, ztilt):
    e = f"{base} + math.cos(query.modified_distance_moved * 34 + {ph}) * 10 * query.modified_move_speed"
    return {bone: {"rotation": [e, "0", str(ztilt)]}}


anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=32, freq=34),
        swing({"shin_l": 180, "shin_r": 0}, amp=18, freq=34),
        arm_swing("arm_l", 0, -72, -10),
        arm_swing("arm_r", 180, -72, 10),
        bob("body", amp=0.9, rate=68),
        sway("body", amp=3, rate=34, axis=2),
        swing({"chain_l": 0, "chain_r": 180}, amp=8, axis=0, freq=34),
    )),
    "idle": anim(merge(
        bob("body", amp=0.6, rate=52),
        sway("body", amp=2.5, rate=30, axis=2),
        {"arm_l": {"rotation": ["-72 + math.sin(query.life_time * 44 + 0.5) * 5", "0", "-10"]}},
        {"arm_r": {"rotation": ["-72 + math.sin(query.life_time * 44 + 2.2) * 5", "0", "10"]}},
        sway("chain_l", amp=14, rate=90, axis=0),
        sway("chain_r", amp=14, rate=90, axis=0, off=1.3),
        {"jaw": {"rotation": ["math.sin(query.life_time * 47) * 4", "0", "0"]}},
        {"head": {"rotation": ["math.sin(query.life_time * 23) * 3", "0", "math.sin(query.life_time * 17) * 4"]}},
    )),
    "attack": anim(merge(
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * 9", "0", "0"]}},
        {"arm_l": {"rotation": [f"-72 + math.sin(variable.attack_time * 180) * 52", "0", "-10"]}},
        {"arm_r": {"rotation": [f"-72 + math.sin(variable.attack_time * 180) * 52", "0", "10"]}},
        {"fore_l": {"rotation": ["math.sin(variable.attack_time * 180) * 22", "0", "0"]}},
        {"fore_r": {"rotation": ["math.sin(variable.attack_time * 180) * 22", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 26", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "zombie_brute",
    "name": "Zombie Brute",
    "egg": ("#5b6b46", "#6b4326"),
    "glow": True,
    "scale": 1.0,
    "visible": [4.0, 3.6, 1.6],
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "cloth": cloth, "metal": metal,
              "bone": bone, "tooth": tooth, "gash": gash, "eye": eye},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 60, "speed": 0.23, "damage": 8, "box": [1.4, 2.7],
        "knockback_resist": 0.5, "family": ["undead", "zombie"],
        "loot": [("minecraft:rotten_flesh", 2, 4), ("minecraft:bone", 1, 3), ("minecraft:iron_nugget", 0, 2)],
        "sound": ("zombie", [0.6, 0.75]),
        "xp": 12,
        "spawn": {"biomes": ["overworld"], "weight": 8, "herd": [1, 2]},
    },
}
