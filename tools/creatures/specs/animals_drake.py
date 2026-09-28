"""Thunder Drake - flying rideable dragon with glowing lightning-blue veins.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

SCALE_D = "#2b2f52"
SCALE_M = "#3f4676"
SCALE_L = "#5b6699"
BELLY   = "#8f96bd"
VEIN    = "#7fe8ff"
GLOW_HI = "#d6f7ff"
HORN    = "#d8cbb0"
HORN_D  = "#a8997c"
MEMB    = "#4a3f6e"
MEMB_D  = "#332b4f"
CLAW    = "#e8e2d0"
TOOTH   = "#f2eee2"


def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def scales(p):
    x, y, z = p.p
    n = noise3(x * 1.3, y * 1.3, z * 1.3, 13, 1.0)
    patch = noise3(x * 0.5, y * 0.5, z * 0.5, 29, 6.0)
    c = mix(SCALE_D, SCALE_L, 0.25 + 0.7 * patch)
    c = shade(c, 0.85 + 0.30 * n)
    if y < 24:
        t = min(1.0, (24 - y) / 8.0)
        c = mix(c, BELLY, 0.7 * t)
    # scale plates: darker lattice
    if abs((y % 3) - 1.5) < 0.6 and abs((z % 4) - 2) < 0.8:
        c = shade(c, 0.86)
    # glowing lightning veins running along the spine and flanks
    if p.bone in ("body", "neck0", "neck1", "tail0", "tail1", "tail2", "tail3"):
        vein = abs(math.sin(z * 0.45 + x * 0.3))
        if y > 26 and vein > 0.93:
            c = glow(VEIN)
        elif vein > 0.97:
            c = glow(GLOW_HI)
    return c


def membrane(p):
    x, y, z = p.p
    c = mix(MEMB_D, MEMB, 0.3 + 0.7 * noise3(x * 0.4, y, z * 0.4, 37, 5.0))
    # radiating veins across the membrane
    ang = math.atan2(y - 30, x - 36)
    if math.sin(ang * 7.0 + z * 0.2) > 0.55:
        c = mix(c, VEIN, 0.6)
    return shade(c, 0.88 + 0.24 * grain(p, 1.5, 41))


def horn(p):
    x, y, z = p.p
    c = mix(HORN_D, HORN, 0.4 + 0.6 * noise3(x, y, z, 53, 3.0))
    if abs((y % 2) - 1) < 0.4:
        c = shade(c, 0.9)
    return c


def eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 1.05 and abs(p.y + 0.5 - p.fh / 2) < 1.05:
            return glow(GLOW_HI)
        return glow(VEIN)
    return glow(shade(VEIN, 0.8))


def claw(p):
    return shade(CLAW, 0.9 + 0.2 * grain(p, 1.2, 61))


def tooth(p):
    return shade(TOOTH, 0.92 + 0.16 * grain(p, 1.0, 67))


def spike(p):
    x, y, z = p.p
    c = mix(SCALE_M, SCALE_L, 0.4 + 0.6 * grain(p, 1.5, 71))
    if y > 33:
        c = glow(mix(VEIN, GLOW_HI, 0.5))
    return c


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "scales")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


body_cubes = [
    {"o": [-6, 20, -12], "s": [12, 12, 24], "skin": "scales"},
    {"o": [-7, 20, -13], "s": [14, 12, 9], "skin": "scales"},     # chest
    {"o": [-6, 20, 9], "s": [12, 11, 9], "skin": "scales"},       # hips
    {"o": [-4, 20, -10], "s": [8, 8, 22], "skin": "scales"},      # belly
]
# dorsal spine ridge
for zz in range(-10, 11, 4):
    body_cubes.append({"o": [-1, 32, zz], "s": [2, 4, 5], "skin": "spike", "rot": [-10, 0, 0], "pivot": [0, 32, zz]})
sym(body_cubes, {"o": [5, 22, -6], "s": [3, 6, 12], "skin": "scales", "rot": [0, 0, -14], "pivot": [5, 28, -6]})
sym(body_cubes, {"o": [5, 22, 6], "s": [3, 6, 9], "skin": "scales", "rot": [0, 0, 10], "pivot": [5, 27, 6]})

neck0_cubes = [{"o": [-3, 23, -18], "s": [6, 9, 8], "skin": "scales"},
               {"o": [-1, 32, -16], "s": [2, 4, 5], "skin": "spike", "rot": [-20, 0, 0], "pivot": [0, 32, -16]}]
neck1_cubes = [{"o": [-2.5, 25, -25], "s": [5, 8, 8], "skin": "scales"},
               {"o": [-1, 33, -23], "s": [2, 4, 5], "skin": "spike", "rot": [-30, 0, 0], "pivot": [0, 33, -23]}]

head_cubes = [
    {"o": [-4, 26, -34], "s": [8, 8, 10], "skin": "scales"},
    {"o": [-4, 33, -34], "s": [8, 2, 8], "skin": "scales"},
    {"o": [-3, 26, -36], "s": [6, 6, 5], "skin": "scales"},
    {"o": [-2, 30, -37], "s": [4, 2, 2], "skin": "scales"},
]
sym(head_cubes, {"o": [2, 29, -35], "s": [3, 3, 3], "skin": "eye"})
sym(head_cubes, {"o": [3, 26, -33], "s": [2, 4, 7], "skin": "spike", "rot": [0, 0, -20], "pivot": [3, 28, -33]})

jaw_cubes = [
    {"o": [-3, 23, -36], "s": [6, 3, 10], "skin": "scales"},
    {"o": [-2.5, 25.2, -35.4], "s": [5, 1, 9], "skin": "membrane"},
]
for i in range(4):
    sym(jaw_cubes, {"o": [0.4 + i * 1.2, 24, -35], "s": [1, 2, 1], "skin": "tooth"})
sym(jaw_cubes, {"o": [1.5, 27, -35], "s": [1, 2, 1], "skin": "tooth"})

# horns curving back and up from the skull
horn_cubes = [{"o": [2, 33, -35], "s": [3, 4, 8], "skin": "horn"}]
horn2_cubes = [{"o": [2, 37, -27], "s": [2, 3, 7], "skin": "horn"}]
horn3_cubes = [{"o": [2, 40, -20], "s": [2, 2, 5], "skin": "horn"}]

tail0 = [{"o": [-3, 23, 12], "s": [6, 7, 8], "skin": "scales"},
         {"o": [-1, 30, 14], "s": [2, 4, 5], "skin": "spike", "rot": [10, 0, 0], "pivot": [0, 30, 14]}]
tail1 = [{"o": [-2.5, 22, 19], "s": [5, 6, 8], "skin": "scales"},
         {"o": [-1, 28, 21], "s": [2, 4, 5], "skin": "spike", "rot": [16, 0, 0], "pivot": [0, 28, 21]}]
tail2 = [{"o": [-2, 21, 26], "s": [4, 5, 7], "skin": "scales"},
         {"o": [-1, 26, 28], "s": [2, 3, 4], "skin": "spike", "rot": [22, 0, 0], "pivot": [0, 26, 28]}]
tail3 = [{"o": [-1.5, 20, 32], "s": [3, 4, 6], "skin": "scales"}]
fin_cubes = [{"o": [-1, 20, 38], "s": [2, 3, 5], "skin": "membrane"},
             {"o": [-2, 22, 40], "s": [4, 2, 5], "skin": "membrane", "rot": [-25, 0, 0], "pivot": [0, 22, 38]},
             {"o": [-3, 24, 40], "s": [6, 2, 5], "skin": "membrane", "rot": [-50, 0, 0], "pivot": [0, 23, 38]},
             {"o": [-2, 21, 42], "s": [4, 2, 5], "skin": "membrane", "rot": [25, 0, 0], "pivot": [0, 21, 40]}]

leg_fl = [{"o": [3.5, 12, -11], "s": [3, 10, 5], "skin": "scales"}]
leg_fr = [{"o": [-6.5, 12, -11], "s": [3, 10, 5], "skin": "scales"}]
leg_bl = [{"o": [3.5, 12, 7], "s": [3, 10, 5], "skin": "scales"}]
leg_br = [{"o": [-6.5, 12, 7], "s": [3, 10, 5], "skin": "scales"}]
shin_fl = [{"o": [3.5, 4, -10], "s": [3, 8, 4], "skin": "scales"}]
shin_fr = [{"o": [-6.5, 4, -10], "s": [3, 8, 4], "skin": "scales"}]
shin_bl = [{"o": [3.5, 4, 8], "s": [3, 8, 4], "skin": "scales"}]
shin_br = [{"o": [-6.5, 4, 8], "s": [3, 8, 4], "skin": "scales"}]
paw_fl = [{"o": [3, 0, -13], "s": [4, 4, 9], "skin": "scales"}]
paw_fr = [{"o": [-7, 0, -13], "s": [4, 4, 9], "skin": "scales"}]
paw_bl = [{"o": [3, 0, 6], "s": [4, 4, 9], "skin": "scales"}]
paw_br = [{"o": [-7, 0, 6], "s": [4, 4, 9], "skin": "scales"}]
for paw, px, pz in ((paw_fl, 3, -13), (paw_fr, -7, -13), (paw_bl, 3, 6), (paw_br, -7, 6)):
    for i in range(3):
        paw.append({"o": [px + 0.4 + i * 1.3, 0, pz - 1.4], "s": [1, 2, 2], "skin": "claw"})

wing_l_up = [{"o": [6, 27, -10], "s": [16, 5, 10], "skin": "scales"},
             {"o": [6, 30, -8], "s": [16, 2, 6], "skin": "membrane"}]
wing_l_f = [{"o": [22, 27, -8], "s": [14, 5, 8], "skin": "scales"},
            {"o": [22, 29, -7], "s": [14, 2, 6], "skin": "membrane"}]
wing_l_h = [{"o": [36, 28, -12], "s": [10, 3, 3], "skin": "scales"},
            {"o": [36, 28, -5], "s": [10, 3, 3], "skin": "scales"},
            {"o": [36, 28, 2], "s": [10, 3, 3], "skin": "scales"},
            {"o": [36, 29, -12], "s": [10, 1, 14], "skin": "membrane"},
            {"o": [46, 29, -9], "s": [12, 1, 9], "skin": "membrane"},
            {"o": [46, 28, -9], "s": [12, 2, 3], "skin": "scales"}]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 26, 0], "cubes": body_cubes},
    {"name": "neck0", "parent": "body", "pivot": [0, 27, -11], "cubes": neck0_cubes},
    {"name": "neck1", "parent": "neck0", "pivot": [0, 28, -17], "cubes": neck1_cubes},
    {"name": "head", "parent": "neck1", "pivot": [0, 29, -24], "cubes": head_cubes},
    {"name": "jaw", "parent": "head", "pivot": [0, 26, -30], "cubes": jaw_cubes},
    {"name": "horn_l", "parent": "head", "pivot": [3, 35, -32], "cubes": horn_cubes},
    {"name": "horn_l2", "parent": "horn_l", "pivot": [3, 37, -27], "cubes": horn2_cubes},
    {"name": "horn_l3", "parent": "horn_l2", "pivot": [3, 40, -20], "cubes": horn3_cubes},
    {"name": "horn_r", "parent": "head", "pivot": [-3, 35, -32],
     "cubes": [{"o": [-5, 33, -35], "s": [3, 4, 8], "skin": "horn"}]},
    {"name": "horn_r2", "parent": "horn_r", "pivot": [-3, 37, -27],
     "cubes": [{"o": [-4, 37, -27], "s": [2, 3, 7], "skin": "horn"}]},
    {"name": "horn_r3", "parent": "horn_r2", "pivot": [-3, 40, -20],
     "cubes": [{"o": [-4, 40, -20], "s": [2, 2, 5], "skin": "horn"}]},
    {"name": "tail0", "parent": "body", "pivot": [0, 25, 12], "cubes": tail0},
    {"name": "tail1", "parent": "tail0", "pivot": [0, 24, 19], "cubes": tail1},
    {"name": "tail2", "parent": "tail1", "pivot": [0, 23, 26], "cubes": tail2},
    {"name": "tail3", "parent": "tail2", "pivot": [0, 22, 32], "cubes": tail3},
    {"name": "fin", "parent": "tail3", "pivot": [0, 21, 37], "cubes": fin_cubes},
    {"name": "leg_fl", "parent": "body", "pivot": [5, 22, -8], "cubes": leg_fl},
    {"name": "shin_fl", "parent": "leg_fl", "pivot": [5, 12, -8], "cubes": shin_fl},
    {"name": "paw_fl", "parent": "shin_fl", "pivot": [5, 2, -8], "cubes": paw_fl},
    {"name": "leg_fr", "parent": "body", "pivot": [-5, 22, -8], "cubes": leg_fr},
    {"name": "shin_fr", "parent": "leg_fr", "pivot": [-5, 12, -8], "cubes": shin_fr},
    {"name": "paw_fr", "parent": "shin_fr", "pivot": [-5, 2, -8], "cubes": paw_fr},
    {"name": "leg_bl", "parent": "body", "pivot": [5, 22, 8], "cubes": leg_bl},
    {"name": "shin_bl", "parent": "leg_bl", "pivot": [5, 12, 8], "cubes": shin_bl},
    {"name": "paw_bl", "parent": "shin_bl", "pivot": [5, 2, 8], "cubes": paw_bl},
    {"name": "leg_br", "parent": "body", "pivot": [-5, 22, 8], "cubes": leg_br},
    {"name": "shin_br", "parent": "leg_br", "pivot": [-5, 12, 8], "cubes": shin_br},
    {"name": "paw_br", "parent": "shin_br", "pivot": [-5, 2, 8], "cubes": paw_br},
    {"name": "wing_l", "parent": "body", "pivot": [6, 30, -6], "cubes": wing_l_up},
    {"name": "wing_l_f", "parent": "wing_l", "pivot": [22, 30, -5], "cubes": wing_l_f},
    {"name": "wing_l_h", "parent": "wing_l_f", "pivot": [36, 30, -4], "cubes": wing_l_h},
    {"name": "wing_r", "parent": "body", "pivot": [-6, 30, -6],
     "cubes": [{"o": [-22, 27, -10], "s": [16, 5, 10], "skin": "scales"},
               {"o": [-22, 30, -8], "s": [16, 2, 6], "skin": "membrane"}]},
    {"name": "wing_r_f", "parent": "wing_r", "pivot": [-22, 30, -5],
     "cubes": [{"o": [-36, 27, -8], "s": [14, 5, 8], "skin": "scales"},
               {"o": [-36, 29, -7], "s": [14, 2, 6], "skin": "membrane"}]},
    {"name": "wing_r_h", "parent": "wing_r_f", "pivot": [-36, 30, -4],
     "cubes": [{"o": [-46, 28, -12], "s": [10, 3, 3], "skin": "scales"},
               {"o": [-46, 28, -5], "s": [10, 3, 3], "skin": "scales"},
               {"o": [-46, 28, 2], "s": [10, 3, 3], "skin": "scales"},
               {"o": [-46, 29, -12], "s": [10, 1, 14], "skin": "membrane"},
               {"o": [-58, 29, -9], "s": [12, 1, 9], "skin": "membrane"},
               {"o": [-58, 28, -9], "s": [12, 2, 3], "skin": "scales"}]},
]

_wing_flap = {
    "wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 200) * 40"]},
    "wing_l_f": {"rotation": ["0", "0", "math.sin(query.life_time * 200 - 40) * 28"]},
    "wing_l_h": {"rotation": ["0", "0", "math.sin(query.life_time * 200 - 80) * 20"]},
    "wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 200) * -40"]},
    "wing_r_f": {"rotation": ["0", "0", "math.sin(query.life_time * 200 - 40) * -28"]},
    "wing_r_h": {"rotation": ["0", "0", "math.sin(query.life_time * 200 - 80) * -20"]},
}
_walk_flap = {
    "wing_l": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26) * 36 * query.modified_move_speed"]},
    "wing_l_f": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26 - 40) * 24 * query.modified_move_speed"]},
    "wing_l_h": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26 - 80) * 16 * query.modified_move_speed"]},
    "wing_r": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26) * -36 * query.modified_move_speed"]},
    "wing_r_f": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26 - 40) * -24 * query.modified_move_speed"]},
    "wing_r_h": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 26 - 80) * -16 * query.modified_move_speed"]},
}

anims = {
    "flap": anim(_wing_flap),
    "walk": anim(merge(
        _walk_flap,
        swing({"leg_fl": 0, "leg_fr": 180, "leg_bl": 180, "leg_br": 0}, amp=18, axis=0, freq=40),
        swing({"tail1": 0, "tail2": 180, "tail3": 0}, amp=7, axis=1, freq=40),
        bob("body", amp=0.6, rate=160),
    )),
    "idle": anim(merge(
        bob("body", amp=0.5, rate=55),
        sway("tail0", amp=6, rate=40, axis=1),
        sway("tail1", amp=8, rate=34, axis=1, off=0.9),
        sway("tail2", amp=11, rate=29, axis=1, off=1.8),
        sway("tail3", amp=14, rate=25, axis=1, off=2.7),
        sway("fin", amp=17, rate=22, axis=1, off=3.6),
        {"neck0": {"rotation": ["math.sin(query.life_time * 60) * 3", "0", "0"]}},
        {"neck1": {"rotation": ["math.sin(query.life_time * 60 + 30) * 3", "0", "0"]}},
        {"head": {"rotation": ["math.sin(query.life_time * 60 + 60) * 4", "math.sin(query.life_time * 31) * 10", "0"]}},
        {"wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 90) * 10 + 6"]},
         "wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 90) * -10 - 6"]}},
    )),
    "attack": anim(merge(
        {"neck0": {"rotation": ["math.sin(variable.attack_time * 180) * 16", "0", "0"]}},
        {"neck1": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 28", "0", "0"]}},
        {"jaw": {"rotation": ["math.sin(variable.attack_time * 180) * 45", "0", "0"]}},
        {"wing_l": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 34 + 8"]},
         "wing_r": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * -34 - 8"]}},
    ), loop=False),
}

SPEC = {
    "id": "drake",
    "name": "Thunder Drake",
    "egg": ("#3f4676", "#7fe8ff"),
    "glow": True,
    "scale": 1.0,
    "visible": [8, 4, 2.0],
    "bones": bones,
    "skins": {"default": scales, "scales": scales, "membrane": membrane, "horn": horn,
              "eye": eye, "claw": claw, "tooth": tooth, "spike": spike},
    "anims": anims,
    "play": [{"flap": "query.modified_move_speed < 0.02"}, {"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 80, "speed": 0.3, "fly": True, "fly_speed": 0.35,
        "damage": 10, "box": [1.6, 2.6], "knockback_resist": 0.3, "family": ["dragon"],
        "ride": {"seats": [[0, 2.1, -2]]},
        "loot": [("minecraft:feather", 1, 3), ("minecraft:bone", 0, 2)],
        "sound": ("dragon", [1.2, 1.4]),
    },
}
