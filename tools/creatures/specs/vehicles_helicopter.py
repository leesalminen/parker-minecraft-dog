"""Galaxy Rescue Copter - friendly two-seat bubble helicopter (seats side by side).
Model faces -Z, y up, ground y=0.  Flight behaviour lives in scripts/vehicles.js."""
import math
from lib import *
from specs.vehicles_common import *

RED = "#e04232"

white = paint("#f2f4f5", "#b7c0c6", 51, 12.0)
red = paint(RED, "#8f2a20", 53, 10.0)
teal = paint("#2fb5c4", "#1a6f7c", 55, 10.0)
under = paint("#454b53", "#22262c", 57, 8.0)
blade = paint("#25282d", "#111316", 59, 6.0)

# --------------------------------------------------------------------- cabin
cabin = [
    {"o": [-12, 6, -22], "s": [24, 3, 32], "skin": "under"},             # floor
    {"o": [-10, 6, -26], "s": [20, 4, 5], "skin": "white"},              # chin
    {"o": [-9, 9, -26], "s": [18, 4, 4], "skin": "white"},               # nose lower
    {"o": [-12, 9, -22], "s": [24, 3, 32], "skin": "white"},             # lower door band
    {"o": [-12, 12, -22], "s": [24, 1, 32], "skin": "red"},              # stripe
    {"o": [-12, 9, 10], "s": [24, 26, 6], "skin": "white"},              # back wall
    {"o": [-9, 35, 0], "s": [18, 5, 16], "skin": "white"},               # engine housing
    {"o": [-10, 34, 2], "s": [20, 1, 14], "skin": "red"},                # housing skirt
    {"o": [-7, 40, 3], "s": [14, 2, 12], "skin": "under"},               # housing top
    {"o": [-12, 33, -22], "s": [24, 2, 32], "skin": "white"},            # roof
    {"o": [-6, 35, -18], "s": [12, 1, 8], "skin": "red"},                # roof panel
    {"o": [-11, 9, -16], "s": [22, 5, 2], "skin": "under"},              # dash
    {"o": [-4, 12, -17], "s": [8, 2, 1], "skin": "lamp_b"},              # dash screen glow
]
sym(cabin, {"o": [12, 13, -20], "s": [1, 20, 2], "skin": "white"})       # front pillar
sym(cabin, {"o": [12, 13, 6], "s": [1, 20, 4], "skin": "white"})         # rear pillar
sym(cabin, {"o": [12, 13, -8], "s": [1, 20, 2], "skin": "white"})        # door pillar
sym(cabin, {"o": [12, 13, -6], "s": [1, 2, 12], "skin": "teal"})         # sill trim (upper)
sym(cabin, {"o": [-2, 9, -30], "s": [4, 4, 4], "skin": "lamp_w"})        # unused placeholder (removed below)
cabin = [c for c in cabin if c.get("skin") != "lamp_w"]
cabin += [
    {"o": [-3, 8, -27], "s": [6, 3, 1], "skin": "lamp_w"},               # searchlight
]

# see-through windows (frame + sheen only)
windows = [
    {"o": [-11, 14, -21], "s": [22, 19, 1], "skin": "glass", "rot": [-12, 0, 0], "pivot": [0, 14, -21]},   # windscreen
    {"o": [12.5, 14, -20], "s": [1, 19, 24], "skin": "glass"},                                          # side R
    {"o": [-13.5, 14, -20], "s": [1, 19, 24], "skin": "glass"},                                         # side L
    {"o": [-11, 14, 8], "s": [22, 19, 1], "skin": "glass"},                                             # rear window
]

# --------------------------------------------------------------------- seats
seats = []
for x in (-10, 2):
    seats.append({"o": [x, 9, -6], "s": [8, 3, 7], "skin": "fabric"})
    seats.append({"o": [x, 12, 1], "s": [8, 11, 2], "skin": "fabric"})
    seats.append({"o": [x, 23, 1], "s": [8, 3, 2], "skin": "under"})
seats.append({"o": [-1, 9, -6], "s": [2, 6, 9], "skin": "under"})        # centre console / collective
seats.append({"o": [-1.5, 15, -12], "s": [3, 1, 3], "skin": "chrome"})

# --------------------------------------------------------------------- tail boom
boom = [
    {"o": [-3, 22, 16], "s": [6, 6, 8], "skin": "white"},
    {"o": [-2.5, 23, 24], "s": [5, 5, 18], "skin": "white"},
    {"o": [-2.6, 25.5, 16], "s": [5, 1, 26], "skin": "red"},             # boom stripe
    {"o": [-1, 26, 38], "s": [2, 14, 6], "skin": "red"},                 # fin
    {"o": [-8, 24, 36], "s": [16, 1, 5], "skin": "white"},               # stabiliser
    {"o": [-1.5, 39.5, 38.5], "s": [3, 1, 3], "skin": "lamp_r"},         # tail beacon
]

# --------------------------------------------------------------------- skids
skids = []
sym(skids, {"o": [9, 0, -24], "s": [3, 2, 36], "skin": "under"})
sym(skids, {"o": [9, 0, -26], "s": [3, 2, 2], "skin": "under", "rot": [-30, 0, 0], "pivot": [0, 1, -24]})
for z in (-14, 0):
    sym(skids, {"o": [10, 2, z], "s": [2, 5, 2], "skin": "under"})
    sym(skids, {"o": [7, 6, z], "s": [3, 1, 2], "skin": "under"})

# --------------------------------------------------------------------- main rotor (Y spin) and tail rotor (X spin)
main_rotor = [
    {"o": [-1.5, 42, 4.5], "s": [3, 1, 3], "skin": "chrome"},           # mast top
    {"o": [-3, 43, 3], "s": [6, 2, 6], "skin": "under"},                # hub
    {"o": [-30, 43, 3.5], "s": [27, 1, 5], "skin": "blade"},
    {"o": [3, 43, 3.5], "s": [27, 1, 5], "skin": "blade"},
    {"o": [-2.5, 43, -27], "s": [5, 1, 30], "skin": "blade"},
    {"o": [-2.5, 43, 9], "s": [5, 1, 30], "skin": "blade"},
    {"o": [-30, 43, 3.5], "s": [3, 1, 5], "skin": "red"},
    {"o": [27, 43, 3.5], "s": [3, 1, 5], "skin": "red"},
    {"o": [-2.5, 43, -27], "s": [5, 1, 3], "skin": "red"},
    {"o": [-2.5, 43, 36], "s": [5, 1, 3], "skin": "red"},
]
mast = [{"o": [-1.5, 40, 4.5], "s": [3, 3, 3], "skin": "chrome"}]
tail_rotor = [
    {"o": [2.5, 31, 39.5], "s": [2, 2, 2], "skin": "chrome"},
    {"o": [3, 25.5, 40], "s": [1, 12, 2], "skin": "blade"},
    {"o": [3, 31, 34.5], "s": [1, 2, 12], "skin": "blade"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 20, 0], "cubes": cabin},
    {"name": "windows", "parent": "body", "pivot": [0, 14, -21], "cubes": windows},
    {"name": "seats", "parent": "body", "pivot": [0, 12, 0], "cubes": seats},
    {"name": "boom", "parent": "body", "pivot": [0, 25, 20], "cubes": boom},
    {"name": "skids", "parent": "body", "pivot": [0, 4, -8], "cubes": skids},
    {"name": "mast", "parent": "body", "pivot": [0, 40, 6], "cubes": mast},
    {"name": "rotor", "parent": "mast", "pivot": [0, 43.5, 6], "cubes": main_rotor},
    {"name": "tail_rotor", "parent": "boom", "pivot": [3, 32, 40.5], "cubes": tail_rotor},
]

anims = {
    "fly": anim(merge(
        {"rotor": {"rotation": ["0", "query.life_time * 3200", "0"]}},
        {"tail_rotor": {"rotation": ["query.life_time * 3600", "0", "0"]}},
        {"body": {"position": ["0", "math.sin(query.life_time * 210) * 0.25", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 130) * 0.9", "0", "math.sin(query.life_time * 100) * 0.7"]}},
        {"boom": {"rotation": ["math.sin(query.life_time * 330) * 0.6", "0", "0"]}},
    )),
    "idle": anim(merge(
        {"rotor": {"rotation": ["0", "query.life_time * 60", "0"]}},
        {"tail_rotor": {"rotation": ["query.life_time * 90", "0", "0"]}},
    )),
}

SPEC = {
    "id": "helicopter",
    "name": "Galaxy Rescue Copter",
    "egg": ("#f2f4f5", "#e04232"),
    "glow": True,
    "scale": 1.0,
    "visible": [6.4, 3.4, 1.4],
    "bones": bones,
    "skins": {"default": white, "white": white, "red": red, "teal": teal, "under": under, "chrome": chrome,
              "glass": glass("#9fe6ff"), "fabric": fabric("#26444d", "#356472"), "blade": blade,
              "lamp_r": lamp("#ff3b3b"), "lamp_w": lamp("#fff3c0"), "lamp_b": lamp("#5fd0ff")},
    "anims": anims,
    "play": [{"fly": "query.has_rider"}, {"idle": "!query.has_rider"}],
    "behavior": {
        "role": "mount",
        "health": 60, "speed": 0.25, "damage": 0, "box": [1.7, 2.2],
        "hover": True, "fly_speed": 0.3, "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle"],
        "ride": {"seats": [[-0.38, 0.53, -0.16], [0.38, 0.53, -0.16]]},
        "sound": ("iron", [0.5, 0.6]),
        "xp": 0,
    },
}
