"""Night Owl - small flying tameable companion.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

TAWNY  = "#8a6a44"
TAWNY_D= "#5c452c"
CREAM  = "#e8dcc0"
SPECK  = "#3d2f1e"
DISC   = "#efe4cc"
BEAK   = "#3b342c"
EYE    = "#ffbf47"
PUPIL  = "#241000"
TALON  = "#4a4038"


def grain(p, scale, seed):
    return noise3(p.p[0], p.p[1], p.p[2], seed, scale)


def down(p):
    x, y, z = p.p
    fine = noise3(x * 1.6, y * 1.6, z * 1.6, 19, 1.0)
    patch = noise3(x * 0.7, y * 0.7, z * 0.7, 31, 4.0)
    c = mix(TAWNY_D, TAWNY, 0.25 + 0.7 * patch)
    c = shade(c, 0.82 + 0.36 * fine)
    if y < 7:
        c = mix(c, CREAM, 0.45)
    # dark speckles like an owl's mottling
    if hash01(int(x * 1.4), int(y * 1.4), int(z * 1.4), 67) > 0.80:
        c = mix(c, SPECK, 0.55)
    return c


def disc(p):
    x, y, z = p.p
    c = mix(CREAM, DISC, 0.5 + 0.5 * noise3(x, y, z, 77, 3.0))
    # radial streaks from the face centre
    ang = math.atan2(y - 13.5, x)
    if math.sin(ang * 9.0) > 0.4:
        c = shade(c, 0.88)
    return shade(c, 0.92 + 0.16 * grain(p, 1.5, 79))


def owl_eye(p):
    if p.face == "front":
        if abs(p.x + 0.5 - p.fw / 2) < 1.05 and abs(p.y + 0.5 - p.fh / 2) < 1.05:
            return glow(PUPIL)
        return glow(EYE)
    return glow(shade(EYE, 0.75))


def beak(p):
    return shade(BEAK, 0.9 + 0.2 * grain(p, 1.2, 83))


def talon(p):
    return shade(TALON, 0.9 + 0.2 * grain(p, 1.0, 87))


def tip(p):
    x, y, z = p.p
    c = down(p)
    return mix(c, "#f6efdd", 0.35 + 0.4 * grain(p, 1.4, 91))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "down")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


body_cubes = [
    {"o": [-4.5, 3, -4.5], "s": [9, 8, 9], "skin": "down"},
    {"o": [-3.5, 3, -6], "s": [7, 6, 4], "skin": "down"},        # breast
    {"o": [-4, 4, 3], "s": [8, 7, 4], "skin": "down"},           # back
]
# belly down tufts + back tufts
sym(body_cubes, {"o": [2, 2, -3], "s": [3, 3, 3], "skin": "tip", "inflate": 0.2})
body_cubes.append({"o": [-3, 2, -1], "s": [6, 3, 4], "skin": "tip", "inflate": 0.2})
body_cubes.append({"o": [-3, 10, 1], "s": [6, 3, 5], "skin": "down"})
sym(body_cubes, {"o": [3, 8, 2], "s": [2, 4, 4], "skin": "down", "rot": [0, 0, -12], "pivot": [3, 11, 2]})

head_cubes = [
    {"o": [-5, 10, -5], "s": [10, 7, 10], "skin": "down"},
    {"o": [-4.5, 11, -6], "s": [9, 5, 2], "skin": "disc"},
    {"o": [-4, 16, -5], "s": [8, 2, 6], "skin": "down"},
    {"o": [-3, 17, -3], "s": [6, 2, 5], "skin": "down"},
]
sym(head_cubes, {"o": [1, 12, -7], "s": [3, 3, 3], "skin": "eye"})
sym(head_cubes, {"o": [0.5, 11, -6.5], "s": [4, 5, 2], "skin": "disc"})   # eye ring
sym(head_cubes, {"o": [4, 11, -5], "s": [2, 4, 4], "skin": "down", "rot": [0, 0, -10], "pivot": [5, 13, -5]})

beak_cubes = [{"o": [-1, 11, -8], "s": [2, 3, 3], "skin": "beak"}]

tuft_cubes = [{"o": [3, 16, -4], "s": [2, 4, 3], "skin": "down", "rot": [0, 0, -18], "pivot": [3, 16, -4]}]
tuft_tip = [{"o": [4, 19, -4], "s": [2, 2, 2], "skin": "tip", "rot": [0, 0, -26], "pivot": [4, 19, -4]}]

wing_l_cubes = [{"o": [4, 3, -3], "s": [3, 8, 8], "skin": "down"},
                {"o": [3, 8, -2], "s": [3, 4, 5], "skin": "tip"},
                {"o": [4, 2, 4], "s": [3, 3, 5], "skin": "down", "rot": [-20, 0, 0], "pivot": [4, 4, 4]}]
wing_l2_cubes = [{"o": [6, 1, -2], "s": [2, 5, 7], "skin": "down"},
                 {"o": [6, 0, 3], "s": [2, 3, 6], "skin": "tip"}]

tail_cubes = [
    {"o": [-3, 4, 5], "s": [6, 2, 8], "skin": "down"},
    {"o": [-4, 3, 12], "s": [8, 2, 6], "skin": "tip"},
    {"o": [-3, 2, 17], "s": [6, 2, 5], "skin": "tip"},
    {"o": [-1, 4, 8], "s": [2, 2, 7], "skin": "tip"},
    {"o": [-5, 1, 15], "s": [2, 2, 5], "skin": "tip"},
]

leg_l_cubes = [{"o": [1.5, 0, -1], "s": [2, 4, 3], "skin": "down"},
               {"o": [1, 0, -3], "s": [3, 2, 4], "skin": "talon"}]
leg_r_cubes = [{"o": [-3.5, 0, -1], "s": [2, 4, 3], "skin": "down"},
               {"o": [-4, 0, -3], "s": [3, 2, 4], "skin": "talon"}]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 8, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 11, 0], "cubes": head_cubes},
    {"name": "beak", "parent": "head", "pivot": [0, 12, -6], "cubes": beak_cubes},
    {"name": "tuft_l", "parent": "head", "pivot": [3, 16, -4], "cubes": tuft_cubes},
    {"name": "tuft_lt", "parent": "tuft_l", "pivot": [4, 19, -4], "cubes": tuft_tip},
    {"name": "tuft_r", "parent": "head", "pivot": [-3, 16, -4],
     "cubes": [{"o": [-5, 16, -4], "s": [2, 4, 3], "skin": "down", "rot": [0, 0, 18], "pivot": [-3, 16, -4]}]},
    {"name": "tuft_rt", "parent": "tuft_r", "pivot": [-4, 19, -4],
     "cubes": [{"o": [-6, 19, -4], "s": [2, 2, 2], "skin": "tip", "rot": [0, 0, 26], "pivot": [-4, 19, -4]}]},
    {"name": "wing_l", "parent": "body", "pivot": [4, 10, 0], "cubes": wing_l_cubes},
    {"name": "wing_l2", "parent": "wing_l", "pivot": [6, 4, 1], "cubes": wing_l2_cubes},
    {"name": "wing_r", "parent": "body", "pivot": [-4, 10, 0],
     "cubes": [{"o": [-7, 3, -3], "s": [3, 8, 8], "skin": "down"},
               {"o": [-6, 8, -2], "s": [3, 4, 5], "skin": "tip"},
               {"o": [-7, 2, 4], "s": [3, 3, 5], "skin": "down", "rot": [-20, 0, 0], "pivot": [-4, 4, 4]}]},
    {"name": "wing_r2", "parent": "wing_r", "pivot": [-6, 4, 1],
     "cubes": [{"o": [-8, 1, -2], "s": [2, 5, 7], "skin": "down"},
               {"o": [-8, 0, 3], "s": [2, 3, 6], "skin": "tip"}]},
    {"name": "tail", "parent": "body", "pivot": [0, 6, 5], "cubes": tail_cubes},
    {"name": "leg_l", "parent": "body", "pivot": [2, 3, 0], "cubes": leg_l_cubes},
    {"name": "leg_r", "parent": "body", "pivot": [-2, 3, 0], "cubes": leg_r_cubes},
]

anims = {
    "walk": anim(merge(
        {"wing_l": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 90) * 34 * query.modified_move_speed"]},
         "wing_r": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 90) * -34 * query.modified_move_speed"]},
         "wing_l2": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 90 + 40) * 22 * query.modified_move_speed"]},
         "wing_r2": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 90 + 40) * -22 * query.modified_move_speed"]}},
        swing({"tail": 0}, amp=6, axis=0, freq=90),
        bob("body", amp=0.6, rate=120),
    )),
    "idle": anim(merge(
        bob("body", amp=0.35, rate=60),
        {"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 23) * 22", "0"]}},
        sway("tail", amp=5, rate=35, axis=0),
        sway("tuft_l", amp=6, rate=130, axis=0, off=0.0),
        sway("tuft_r", amp=6, rate=130, axis=0, off=0.0),
        {"wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 120) * 5"]},
         "wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 120) * -5"]}},
    )),
    "attack": anim(merge(
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 32", "0", "0"]}},
        {"beak": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]}},
        {"wing_l": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 30"]},
         "wing_r": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * -30"]}},
    ), loop=False),
}

SPEC = {
    "id": "owl",
    "name": "Night Owl",
    "egg": ("#8a6a44", "#ffbf47"),
    "glow": True,
    "scale": 1.0,
    "visible": [3, 2, 1.0],
    "bones": bones,
    "skins": {"default": down, "down": down, "disc": disc, "eye": owl_eye, "beak": beak,
              "talon": talon, "tip": tip},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "companion",
        "health": 12, "speed": 0.32, "fly": True, "fly_speed": 0.28,
        "box": [0.6, 1.2], "family": ["owl"],
        "tame_items": ["minecraft:wheat_seeds"],
        "loot": [("minecraft:feather", 1, 2)],
        "sound": ("parrot", [0.6, 0.8]),
    },
}
