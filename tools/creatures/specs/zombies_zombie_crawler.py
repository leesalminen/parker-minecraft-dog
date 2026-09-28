"""Grave Crawler - small fast four-limbed undead scuttler with exposed spine.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SKIN    = "#7d8a6a"
SKIN_D  = "#4d573c"
SKIN_L  = "#9aa684"
BELLY   = "#b9c0a0"
VEIN    = "#6a4040"
GRIME   = "#33321f"
BLOOD   = "#6e2020"
BONE    = "#ded4b2"
BONE_D  = "#a49a78"
TOOTH   = "#e2dcc0"
EYE     = "#8dff5a"
CLAW    = "#3a352c"


def n(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def skin(p):
    x, y, z = p.p
    g = n(p, 2.0, 13)
    patch = n(p, 5.0, 29)
    c = mix(SKIN_D, SKIN_L, 0.20 + 0.80 * patch)
    c = shade(c, 0.80 + 0.40 * g)
    if y < 5:                                       # pale belly / grime low down
        c = mix(c, BELLY, 0.45 * min(1.0, (5 - y) / 3.0))
        c = mix(c, GRIME, 0.30)
    v = math.sin(x * 1.1 + z * 0.8 + y * 0.4)
    if v > 0.80:
        c = mix(c, VEIN, 0.35 + 0.30 * (v - 0.80) * 5)
    if hash01(int(x * 1.6), int(y * 1.6), int(z * 1.6), 83) > 0.955:
        c = mix(c, BLOOD, 0.6)
    if p.bone == "body" and hash01(int(x), 0, int(z), 41) > 0.90:
        c = shade(c, 0.82)                          # mottled sores
    return c


def bone(p):
    c = mix(BONE_D, BONE, 0.3 + 0.7 * n(p, 1.4, 71))
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
        t = 0.4 + 0.6 * n(p, 1.0, 87)
        return glow(mix("#6fbf1e", EYE, t))
    return glow(shade(EYE, 0.5))


def sym(cubes, c):
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
    {"o": [-5, 3, -6], "s": [10, 5, 13], "skin": "skin"},      # torso
    {"o": [-4, 2, -5], "s": [8, 2, 11], "skin": "skin"},       # sagging belly
    {"o": [-3, 5, -5], "s": [6, 3, 12], "skin": "skin"},       # back mass
]
sym(body_cubes, {"o": [4, 3, 4], "s": [3, 4, 5], "skin": "skin", "rot": [0, 0, -14], "pivot": [4, 3, 4]})
sym(body_cubes, {"o": [4, 3, -5], "s": [3, 4, 5], "skin": "skin", "rot": [0, 0, -14], "pivot": [4, 3, -5]})
# exposed spine ridge
for zz in (-4, -2, 0, 2, 4):
    body_cubes.append({"o": [-1, 7, zz], "s": [2, 2, 2], "skin": "bone"})
body_cubes.append({"o": [-1, 7, 6], "s": [2, 2, 2], "skin": "bone"})
# burst ribs through the flanks
for zz in (-3, 0, 3):
    sym(body_cubes, {"o": [4, 4, zz], "s": [2, 2, 2], "skin": "bone"})
# tumour growth on the back
body_cubes.append({"o": [1, 7, 1], "s": [3, 2, 3], "skin": "skin"})

# ----------------------------------------------------------------- neck / head
neck_cubes = [{"o": [-3, 4, -9], "s": [6, 5, 5], "skin": "skin"}]

head_cubes = [
    {"o": [-3, 4, -14], "s": [6, 5, 6], "skin": "skin"},       # skull
    {"o": [-2, 4, -19], "s": [4, 4, 6], "skin": "skin"},       # elongated snout
    {"o": [-2, 8, -18], "s": [4, 1, 4], "skin": "bone"},       # skull ridge
]
sym(head_cubes, {"o": [1, 7, -14], "s": [2, 2, 3], "skin": "skin", "rot": [-14, 0, 0], "pivot": [1, 7, -14]})
sym(head_cubes, {"o": [1, 6, -15], "s": [2, 2, 1], "skin": "eye"})      # main glowing eyes
sym(head_cubes, {"o": [2, 8, -13], "s": [1, 1, 1], "skin": "eye"})      # secondary eye dots
sym(head_cubes, {"o": [1, 4, -20], "s": [1, 3, 1], "skin": "tooth"})    # upper fangs

jaw_cubes = [
    {"o": [-2, 2, -19], "s": [4, 2, 7], "skin": "skin"},       # long lower jaw
    {"o": [-2, 4, -19], "s": [4, 1, 6], "skin": "tooth"},      # tooth row
]
sym(jaw_cubes, {"o": [1, 1, -20], "s": [1, 2, 1], "skin": "tooth"})
sym(jaw_cubes, {"o": [1, 2, -15], "s": [1, 1, 4], "skin": "bone"})   # jaw bone spur

# ----------------------------------------------------------------- legs (four splayed scuttling limbs)
def make_leg(side, fz):
    """side +1/-1, fz = z of the limb root."""
    s = side
    def M(o, sz, skin, **kw):
        c = {"o": [o[0] * s if s > 0 else -o[0] - sz[0], o[1], o[2]], "s": list(sz), "skin": skin}
        c.update(kw); return c
    femur = [M([4, 2, fz - 2], [4, 5, 5], "skin")]
    shin = [M([4, 0, fz - 2], [4, 3, 4], "skin")]
    foot = [M([3, 0, fz - 3], [6, 2, 6], "skin")]
    for i in range(3):
        foot.append(M([3 + i * 2, 0, fz - 5], [1, 1, 2], "claw"))
    return femur, shin, foot

leg_fl_cubes, shin_fl_cubes, foot_fl_cubes = make_leg(1, -4)
leg_fr_cubes, shin_fr_cubes, foot_fr_cubes = make_leg(-1, -4)
leg_bl_cubes, shin_bl_cubes, foot_bl_cubes = make_leg(1, 4)
leg_br_cubes, shin_br_cubes, foot_br_cubes = make_leg(-1, 4)

bones = [
    {"name": "body", "parent": None, "pivot": [0, 6, 0], "cubes": body_cubes},
    {"name": "neck", "parent": "body", "pivot": [0, 7, -6], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 7, -9], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 6, -13], "cubes": jaw_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [6, 6, -4], "cubes": leg_fl_cubes},
    {"name": "shin_fl", "parent": "leg_fl", "pivot": [6, 2, -4], "cubes": shin_fl_cubes},
    {"name": "foot_fl", "parent": "shin_fl", "pivot": [6, 1, -4], "cubes": foot_fl_cubes},
    {"name": "leg_fr", "parent": "body", "pivot": [-6, 6, -4], "cubes": leg_fr_cubes},
    {"name": "shin_fr", "parent": "leg_fr", "pivot": [-6, 2, -4], "cubes": shin_fr_cubes},
    {"name": "foot_fr", "parent": "shin_fr", "pivot": [-6, 1, -4], "cubes": foot_fr_cubes},
    {"name": "leg_bl", "parent": "body", "pivot": [6, 6, 4], "cubes": leg_bl_cubes},
    {"name": "shin_bl", "parent": "leg_bl", "pivot": [6, 2, 4], "cubes": shin_bl_cubes},
    {"name": "foot_bl", "parent": "shin_bl", "pivot": [6, 1, 4], "cubes": foot_bl_cubes},
    {"name": "leg_br", "parent": "body", "pivot": [-6, 6, 4], "cubes": leg_br_cubes},
    {"name": "shin_br", "parent": "leg_br", "pivot": [-6, 2, 4], "cubes": shin_br_cubes},
    {"name": "foot_br", "parent": "shin_br", "pivot": [-6, 1, 4], "cubes": foot_br_cubes},
]

anims = {
    "walk": anim(merge(
        quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", amp=52, freq=52),
        swing({"shin_fl": 0, "shin_fr": 180, "shin_bl": 180, "shin_br": 0}, amp=30, freq=52),
        swing({"foot_fl": 0, "foot_fr": 180, "foot_bl": 180, "foot_br": 0}, amp=18, freq=52),
        bob("body", amp=0.7, rate=104),
        sway("body", amp=4, rate=52, axis=2),
        swing({"neck": 0, "head": 180}, amp=6, axis=0, freq=52),
        swing({"jaw": 0}, amp=9, axis=0, freq=52),
    )),
    "idle": anim(merge(
        bob("body", amp=0.35, rate=96),
        sway("body", amp=3, rate=36, axis=1),
        sway("head", amp=5, rate=44, axis=1, off=0.7),
        {"jaw": {"rotation": ["math.sin(query.life_time * 60) * 7", "0", "0"]}},
        {"neck": {"rotation": ["math.sin(query.life_time * 38) * 3", "0", "0"]}},
        sway("leg_fl", amp=3, rate=70, axis=0),
        sway("leg_br", amp=3, rate=70, axis=0, off=1.1),
    )),
    "attack": anim(merge(
        {"neck": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 26", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 45", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * 10", "0", "0"]}},
        {"leg_fl": {"rotation": ["math.sin(variable.attack_time * 180) * -14", "0", "0"]}},
        {"leg_fr": {"rotation": ["math.sin(variable.attack_time * 180) * -14", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "zombie_crawler",
    "name": "Grave Crawler",
    "egg": ("#7d8a6a", "#8dff5a"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.0, 1.6, 0.5],
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "bone": bone, "tooth": tooth,
              "claw": claw, "eye": eye},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 14, "speed": 0.38, "damage": 3, "box": [0.9, 0.6],
        "knockback_resist": 0.0, "family": ["undead", "zombie"],
        "loot": [("minecraft:rotten_flesh", 1, 2), ("minecraft:bone", 0, 1)],
        "sound": ("zombie", [1.3, 1.5]),
        "xp": 5,
        "spawn": {"biomes": ["overworld"], "weight": 10, "herd": [2, 4]},
    },
}
