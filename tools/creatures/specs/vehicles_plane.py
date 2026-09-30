"""Galaxy Sky Pup Plane - friendly two-seat tandem prop plane, low wing, open cockpit.
Model faces -Z, y up, ground y=0.  Flight behaviour lives in scripts/vehicles.js."""
import math
from lib import *
from specs.vehicles_common import *

YEL, YEL_D = "#ffc21f", "#d98a10"
RED = "#dd3b2c"

body = paint(YEL, YEL_D, 21, 12.0)
red = paint(RED, "#8f2419", 23, 10.0)
cream = paint("#f4efe0", "#c9c2ac", 25, 10.0)
under = paint("#4a5058", "#262a30", 27, 8.0)

# --------------------------------------------------------------------- fuselage
fuse = [
    {"o": [-7, 8, -12], "s": [14, 12, 10], "skin": "body"},              # firewall section
    {"o": [-7, 8, -2], "s": [14, 4, 22], "skin": "body"},                # cockpit floor / belly
    {"o": [-7, 12, -2], "s": [2, 6, 22], "skin": "body"},                # cockpit wall L
    {"o": [5, 12, -2], "s": [2, 6, 22], "skin": "body"},                 # cockpit wall R
    {"o": [-5, 12, 18], "s": [10, 8, 2], "skin": "body"},                # rear bulkhead
    {"o": [-6, 9, 20], "s": [12, 10, 8], "skin": "body"},                # rear taper 1
    {"o": [-5, 10, 28], "s": [10, 8, 8], "skin": "body"},                # rear taper 2
    {"o": [-3, 11, 36], "s": [6, 6, 6], "skin": "body"},                 # tail cone
    {"o": [-7, 20, -12], "s": [14, 3, 10], "skin": "body"},              # cowl top
    {"o": [-6, 23, -10], "s": [12, 1, 6], "skin": "cream"},              # cowl hump
    {"o": [-7.5, 9, -20], "s": [15, 12, 9], "skin": "red"},              # engine cowl
    {"o": [-6, 10, -21], "s": [12, 10, 1], "skin": "dark"},              # air intake
    {"o": [-8, 13, -10], "s": [1, 2, 22], "skin": "red"},                # stripe L
    {"o": [7, 13, -10], "s": [1, 2, 22], "skin": "red"},                 # stripe R
    {"o": [-7, 20, 18], "s": [14, 2, 2], "skin": "body"},                # turtle-deck start
    {"o": [-5, 18, 18], "s": [10, 2, 10], "skin": "body"},               # turtle deck
    {"o": [-6, 5, -2], "s": [12, 3, 20], "skin": "under"},               # belly pan
    {"o": [-5, 21, -12], "s": [10, 1, 2], "skin": "cream"},              # windscreen cowl lip
]
# windscreen (angled, see-through with frame)
screen = [
    {"o": [-6, 21, -2], "s": [12, 6, 1], "skin": "glass", "rot": [-30, 0, 0], "pivot": [0, 20, -2]},
    {"o": [-6.5, 20, -2], "s": [13, 1, 1], "skin": "chrome"},
    {"o": [6, 20, -2], "s": [1, 4, 1], "skin": "chrome"},
    {"o": [-7, 20, -2], "s": [1, 4, 1], "skin": "chrome"},
]
# coaming rims
coaming = [
    {"o": [-7, 18, -2], "s": [14, 1, 1], "skin": "cream"},
    {"o": [-7, 18, 17], "s": [14, 1, 1], "skin": "cream"},
    {"o": [-7, 18, -1], "s": [1, 1, 18], "skin": "cream"},
    {"o": [6, 18, -1], "s": [1, 1, 18], "skin": "cream"},
]
# seats + stick
seats = [
    {"o": [-3, 12, 0], "s": [6, 2, 6], "skin": "fabric"},
    {"o": [-3, 14, 5], "s": [6, 6, 1], "skin": "fabric"},
    {"o": [-3, 12, 9], "s": [6, 2, 6], "skin": "fabric"},
    {"o": [-3, 14, 14], "s": [6, 6, 1], "skin": "fabric"},
    {"o": [-0.5, 12, -4], "s": [1, 5, 1], "skin": "under"},               # stick
    {"o": [-1.5, 17, -4], "s": [3, 1, 1], "skin": "chrome"},
    {"o": [-4, 14, -6], "s": [8, 4, 2], "skin": "under"},                 # instrument panel
]

# --------------------------------------------------------------------- wings (dihedral) + ailerons
wing_l = [
    {"o": [7, 7, -8], "s": [28, 2, 16], "skin": "cream", "rot": [0, 0, -5], "pivot": [7, 8, 0]},
    {"o": [7, 7, 0], "s": [28, 2, 5], "skin": "red", "rot": [0, 0, -5], "pivot": [7, 8, 0]},
    {"o": [33, 7, -8], "s": [3, 2, 16], "skin": "red", "rot": [0, 0, -5], "pivot": [7, 8, 0]},
    {"o": [35, 7, -3], "s": [2, 2, 5], "skin": "lamp_r", "rot": [0, 0, -5], "pivot": [7, 8, 0]},
    {"o": [4, 8, -8], "s": [4, 2, 16], "skin": "body"},
]
wing_r = [
    {"o": [-35, 7, -8], "s": [28, 2, 16], "skin": "cream", "rot": [0, 0, 5], "pivot": [-7, 8, 0]},
    {"o": [-35, 7, 0], "s": [28, 2, 5], "skin": "red", "rot": [0, 0, 5], "pivot": [-7, 8, 0]},
    {"o": [-36, 7, -8], "s": [3, 2, 16], "skin": "red", "rot": [0, 0, 5], "pivot": [-7, 8, 0]},
    {"o": [-37, 7, -3], "s": [2, 2, 5], "skin": "lamp_g", "rot": [0, 0, 5], "pivot": [-7, 8, 0]},
    {"o": [-8, 8, -8], "s": [4, 2, 16], "skin": "body"},
]

# --------------------------------------------------------------------- tail
fin = [
    {"o": [-1, 18, 30], "s": [2, 12, 8], "skin": "body"},
    {"o": [-1, 20, 38], "s": [2, 12, 4], "skin": "red"},                 # rudder
]
stab_l = [{"o": [3, 13, 30], "s": [14, 2, 8], "skin": "cream"}, {"o": [3, 13, 38], "s": [14, 2, 4], "skin": "red"}]
stab_r = [{"o": [-17, 13, 30], "s": [14, 2, 8], "skin": "cream"}, {"o": [-17, 13, 38], "s": [14, 2, 4], "skin": "red"}]

# --------------------------------------------------------------------- landing gear
gear = [
    {"o": [-9, 4, -6], "s": [1, 5, 1], "skin": "under", "rot": [0, 0, -18], "pivot": [-6, 8, -6]},
    {"o": [8, 4, -6], "s": [1, 5, 1], "skin": "under", "rot": [0, 0, 18], "pivot": [6, 8, -6]},
    {"o": [-3, 2, -6], "s": [6, 1, 1], "skin": "under"},
    {"o": [-10, 0, -9], "s": [3, 6, 6], "skin": "tire"},
    {"o": [7, 0, -9], "s": [3, 6, 6], "skin": "tire"},
    {"o": [-0.5, 3, 40], "s": [1, 9, 1], "skin": "under"},
    {"o": [-1, 0, 39], "s": [2, 4, 4], "skin": "tire"},
]

# --------------------------------------------------------------------- propeller
prop = [
    {"o": [-2.5, 11.5, -25], "s": [5, 5, 5], "skin": "red"},              # spinner
    {"o": [-1, 12.5, -27], "s": [2, 3, 2], "skin": "chrome"},
    {"o": [-1.5, 1, -23.5], "s": [3, 26, 1], "skin": "blade"},            # blade (vertical, centred on y=14)
    {"o": [-13, 12.5, -23.5], "s": [26, 3, 1], "skin": "blade"},
]
exhaust = [
    {"o": [-8, 10, -16], "s": [1, 2, 6], "skin": "chrome"},
    {"o": [7, 10, -16], "s": [1, 2, 6], "skin": "chrome"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 14, 0], "cubes": fuse + coaming},
    {"name": "screen", "parent": "body", "pivot": [0, 20, -2], "cubes": screen},
    {"name": "seats", "parent": "body", "pivot": [0, 12, 4], "cubes": seats},
    {"name": "wing_l", "parent": "body", "pivot": [7, 8, 0], "cubes": wing_l},
    {"name": "wing_r", "parent": "body", "pivot": [-7, 8, 0], "cubes": wing_r},
    {"name": "fin", "parent": "body", "pivot": [0, 18, 34], "cubes": fin},
    {"name": "stab_l", "parent": "body", "pivot": [3, 14, 34], "cubes": stab_l},
    {"name": "stab_r", "parent": "body", "pivot": [-3, 14, 34], "cubes": stab_r},
    {"name": "gear", "parent": "body", "pivot": [0, 6, -6], "cubes": gear},
    {"name": "exhaust", "parent": "body", "pivot": [0, 11, -16], "cubes": exhaust},
    {"name": "prop", "parent": "body", "pivot": [0, 14, -24], "cubes": prop},
]

anims = {
    # prop spin only while someone is flying; slow idle turn otherwise.
    "fly": anim(merge(
        {"prop": {"rotation": ["0", "0", "query.life_time * 2600"]}},
        {"body": {"position": ["0", "math.sin(query.life_time * 170) * 0.2", "0"]}},
        {"wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 200) * 1.2"]}},
        {"wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 200 + 1.0) * -1.2"]}},
        {"stab_l": {"rotation": ["math.sin(query.life_time * 260) * 2", "0", "0"]}},
        {"stab_r": {"rotation": ["math.sin(query.life_time * 260 + 0.6) * 2", "0", "0"]}},
        {"fin": {"rotation": ["0", "math.sin(query.life_time * 90) * 4", "0"]}},
    )),
    "idle": anim(merge(
        {"prop": {"rotation": ["0", "0", "query.life_time * 40"]}},
        {"fin": {"rotation": ["0", "math.sin(query.life_time * 40) * 2", "0"]}},
    )),
}

SPEC = {
    "id": "plane",
    "name": "Sky Pup Plane",
    "egg": ("#ffc21f", "#dd3b2c"),
    "glow": True,
    "scale": 1.0,
    "visible": [5.2, 2.6, 0.9],
    "bones": bones,
    "skins": {"default": body, "body": body, "red": red, "cream": cream, "under": under, "chrome": chrome,
              "dark": dark_metal, "glass": glass(), "fabric": fabric("#5a2a24", "#7a3a30"),
              "tire": tire("#d8dde0"), "lamp_r": lamp("#ff3b3b"), "lamp_g": lamp("#4dff7a"),
              "blade": paint("#2a2d32", "#14161a", 41, 6.0)},
    "anims": anims,
    "play": [{"fly": "query.has_rider"}, {"idle": "!query.has_rider"}],
    "behavior": {
        "role": "mount",
        "health": 60, "speed": 0.25, "damage": 0, "box": [1.5, 1.4],
        "hover": True, "fly_speed": 0.35, "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle"],
        # tandem: pilot in front, passenger behind
        "ride": {"seats": [[0, 0.62, 0.15], [0, 0.62, 0.7]]},
        "sound": ("phantom", [0.5, 0.7]),
        "xp": 0,
    },
}
