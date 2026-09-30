"""Galaxy Cruiser - cheerful 4-seat open-top car for small drivers.  Model faces -Z, y up, ground y=0.
Movement is native input_ground_controlled; smooth slope climbing is done by scripts/vehicles.js."""
import math
from lib import *
from specs.vehicles_common import *

BLUE, BLUE_D = "#2f8fe0", "#1b55a0"
RED = "#e0402f"
YEL = "#ffe27a"

body = paint(BLUE, BLUE_D, 3, 12.0)
trim = paint("#e9eef1", "#a9b3ba", 5, 10.0)
under = paint("#3a4048", "#20242a", 8, 8.0)
red = paint(RED, "#96271b", 13, 10.0)

# --------------------------------------------------------------------- body tub
tub = [
    {"o": [-10, 4, -22], "s": [20, 3, 44], "skin": "under"},           # floor pan
    {"o": [-9, 7, -22], "s": [18, 6, 15], "skin": "body"},             # hood block
    {"o": [-8, 13, -21], "s": [16, 1, 13], "skin": "body"},            # hood top
    {"o": [-6, 14, -18], "s": [12, 1, 6], "skin": "trim"},             # hood scoop
    {"o": [-10, 8, -7], "s": [2, 7, 25], "skin": "body"},              # left cabin wall
    {"o": [8, 8, -7], "s": [2, 7, 25], "skin": "body"},                # right cabin wall
    {"o": [-8, 7, -7], "s": [16, 1, 18], "skin": "under"},             # cabin floor
    {"o": [-9, 7, 11], "s": [18, 7, 11], "skin": "body"},              # trunk
    {"o": [-8, 14, 12], "s": [16, 1, 9], "skin": "body"},              # trunk lid
    {"o": [-10.5, 11, -7], "s": [1, 1, 25], "skin": "trim"},           # side stripe (left)
    {"o": [9.5, 11, -7], "s": [1, 1, 25], "skin": "trim"},             # side stripe (right)
    {"o": [-2, 14, -21], "s": [4, 1, 3], "skin": "trim"},              # racing stripe (hood)
    {"o": [-8, 12, -8], "s": [16, 3, 2], "skin": "body"},              # dash
    {"o": [-11, 5, -24], "s": [22, 3, 3], "skin": "chrome"},           # front bumper
    {"o": [-11, 5, 21], "s": [22, 3, 3], "skin": "chrome"},            # rear bumper
    {"o": [-5, 8, -23], "s": [10, 5, 1], "skin": "dark"},              # grille
    {"o": [-3, 9, -24], "s": [6, 3, 1], "skin": "chrome"},
    {"o": [-3, 8, 22], "s": [6, 3, 1], "skin": "plate"},               # licence plate
]
sym(tub, {"o": [5.5, 9, -23], "s": [3, 3, 1], "skin": "headlamp"})
sym(tub, {"o": [5.5, 9, 22], "s": [3, 3, 1], "skin": "taillamp"})

# wheel arches (fenders) over each wheel
fenders = []
for x in (10, -15):
    fenders.append({"o": [x, 12, -21], "s": [5, 2, 14], "skin": "body"})
    fenders.append({"o": [x, 12, 7], "s": [5, 2, 14], "skin": "body"})

# --------------------------------------------------------------------- seats
seats = []
for x in (-8, 3):
    seats.append({"o": [x, 8, -5], "s": [5, 4, 5], "skin": "fabric"})     # front cushion
    seats.append({"o": [x, 12, -1], "s": [5, 7, 2], "skin": "fabric"})    # front back
    seats.append({"o": [x, 8, 6], "s": [5, 4, 5], "skin": "fabric"})      # rear cushion
    seats.append({"o": [x, 12, 10], "s": [5, 6, 2], "skin": "fabric"})    # rear back
seats.append({"o": [-1, 8, -5], "s": [2, 4, 16], "skin": "under"})      # centre console

# --------------------------------------------------------------------- windshield + roll bar
shield = [
    {"o": [-9, 14, -8], "s": [1, 8, 1], "skin": "chrome", "rot": [-18, 0, 0], "pivot": [0, 14, -8]},
    {"o": [8, 14, -8], "s": [1, 8, 1], "skin": "chrome", "rot": [-18, 0, 0], "pivot": [0, 14, -8]},
    {"o": [-8, 14, -8], "s": [16, 8, 1], "skin": "glass", "rot": [-18, 0, 0], "pivot": [0, 14, -8]},
    {"o": [-9, 21.5, -5.5], "s": [18, 1, 1], "skin": "chrome"},
]
rollbar = [
    {"o": [-8, 14, 12], "s": [1, 8, 1], "skin": "chrome"},
    {"o": [7, 14, 12], "s": [1, 8, 1], "skin": "chrome"},
    {"o": [-8, 21, 12], "s": [16, 1, 1], "skin": "chrome"},
    {"o": [-6, 17, 12], "s": [12, 1, 1], "skin": "chrome"},
]
# steering wheel in front of the left front seat: square rim + column
steer = [
    {"o": [-8, 18, -10], "s": [6, 1, 1], "skin": "under", "rot": [-25, 0, 0], "pivot": [-5, 15, -10]},
    {"o": [-8, 12, -10], "s": [6, 1, 1], "skin": "under", "rot": [-25, 0, 0], "pivot": [-5, 15, -10]},
    {"o": [-8, 13, -10], "s": [1, 5, 1], "skin": "under", "rot": [-25, 0, 0], "pivot": [-5, 15, -10]},
    {"o": [-3, 13, -10], "s": [1, 5, 1], "skin": "under", "rot": [-25, 0, 0], "pivot": [-5, 15, -10]},
    {"o": [-5.5, 15, -10], "s": [2, 2, 2], "skin": "chrome", "rot": [-25, 0, 0], "pivot": [-5, 15, -10]},
    {"o": [-5.5, 11, -9], "s": [1, 4, 1], "skin": "under"},
]
mirrors = []
sym(mirrors, {"o": [10, 17, -8], "s": [2, 1, 1], "skin": "chrome"})
sym(mirrors, {"o": [11, 15, -9], "s": [2, 3, 1], "skin": "body"})
spoiler = [
    {"o": [-9, 19, 19], "s": [18, 1, 4], "skin": "red"},
    {"o": [-8, 14, 19.5], "s": [1, 5, 1], "skin": "under"},
    {"o": [7, 14, 19.5], "s": [1, 5, 1], "skin": "under"},
]
exhaust = [
    {"o": [4, 5, 24], "s": [3, 3, 3], "skin": "chrome"},
    {"o": [4.5, 5.5, 27], "s": [2, 2, 1], "skin": "dark"},
]
antenna = [
    {"o": [-8, 15, 16], "s": [1, 9, 1], "skin": "under"},
    {"o": [-8, 24, 16], "s": [1, 1, 1], "skin": "taillamp"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 8, 0], "cubes": tub + fenders},
    {"name": "seats", "parent": "body", "pivot": [0, 8, 0], "cubes": seats},
    {"name": "shield", "parent": "body", "pivot": [0, 14, -8], "cubes": shield},
    {"name": "rollbar", "parent": "body", "pivot": [0, 14, 12], "cubes": rollbar},
    {"name": "steer", "parent": "body", "pivot": [-5, 15, -10], "cubes": steer},
    {"name": "mirrors", "parent": "body", "pivot": [0, 17, -8], "cubes": mirrors},
    {"name": "spoiler", "parent": "body", "pivot": [0, 17, 21], "cubes": spoiler},
    {"name": "exhaust", "parent": "body", "pivot": [5, 6, 24], "cubes": exhaust},
    {"name": "antenna", "parent": "body", "pivot": [-8, 15, 16], "cubes": antenna},
]
WHEELS = []
for name, x, z in (("wheel_fl", 13, -14), ("wheel_fr", -13, -14), ("wheel_rl", 13, 14), ("wheel_rr", -13, 14)):
    WHEELS.append(name)
    xo = x - 2
    bones.append({"name": name, "parent": "body", "pivot": [x, 6, z], "cubes": [
        {"o": [xo, 0, z - 6], "s": [4, 12, 12], "skin": "tire"},
        {"o": [xo + (2 if x > 0 else -1), 3, z - 3], "s": [1, 6, 6], "skin": "chrome"},
    ]})


def spin(names, rate=170):
    return {n: {"rotation": [f"query.modified_distance_moved * {rate}", "0", "0"]} for n in names}


anims = {
    "move": anim(merge(
        spin(WHEELS),
        {"body": {"position": ["0", "math.sin(query.life_time * 240) * 0.18", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 150) * 0.8", "0", "math.sin(query.life_time * 120) * 0.6"]}},
        {"antenna": {"rotation": ["math.sin(query.life_time * 330) * 6", "0", "math.sin(query.life_time * 290) * 8"]}},
        {"steer": {"rotation": ["0", "0", "math.sin(query.life_time * 60) * 14"]}},
        {"exhaust": {"position": ["0", "math.sin(query.life_time * 500) * 0.15", "0"]}},
    )),
    "idle": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 200) * 0.06", "0"]}},
        {"antenna": {"rotation": ["math.sin(query.life_time * 90) * 3", "0", "math.sin(query.life_time * 70) * 4"]}},
    )),
}

SPEC = {
    "id": "car",
    "name": "Galaxy Cruiser Car",
    "egg": ("#2f8fe0", "#ffe27a"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.6, 2.0, 0.7],
    "bones": bones,
    "skins": {"default": body, "body": body, "trim": trim, "under": under, "red": red, "chrome": chrome,
              "tire": tire("#c9d2d8"), "glass": glass(), "fabric": fabric(), "dark": dark_metal,
              "headlamp": lamp(YEL), "taillamp": lamp("#ff4a3a"), "plate": plate_fn()},
    "anims": anims,
    "play": [{"move": "query.modified_move_speed > 0.02"}, "idle"],
    "behavior": {
        "role": "mount",
        "health": 60, "speed": 0.2, "damage": 0, "box": [1.9, 1.4],
        "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle"],
        # front L/R, rear L/R.  Y is the seat surface minus ~0.2 (matches the buggy).
        "ride": {"seats": [[-0.34, 0.55, -0.15], [0.34, 0.55, -0.15], [-0.34, 0.55, 0.53], [0.34, 0.55, 0.53]], "jump": 0.0},
        "sound": ("golem", [0.7, 0.9]),
        "xp": 0,
    },
}
