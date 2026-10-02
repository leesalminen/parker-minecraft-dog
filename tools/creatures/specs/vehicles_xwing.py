"""Four-wing starfighter (X-wing style): pointed nose, open-frame bubble canopy, astromech behind the pilot,
four engine nacelles, S-foils that spread when someone climbs in, four wingtip laser cannons.
Model faces -Z, y up, ground y=0.  Flight + guns live in scripts/vehicles.js (family 'starfighter')."""
import math
from lib import *
from specs.vehicles_common import *

hull = paint("#d5dade", "#8a949c", 71, 11.0)
red = paint("#c9352b", "#7d1d17", 73, 9.0)
dark = paint("#2d3339", "#15181c", 75, 8.0)
grey = paint("#7b838b", "#3a4046", 77, 9.0)
engine = paint("#8d959c", "#3b4147", 79, 7.0)
ion = lamp("#ff9a4a")
lens = lamp("#ff4a3a")
blue = paint("#3a6fb8", "#1d3b66", 81, 8.0)

# ---------------------------------------------------------------- fuselage
fuse = loft([(-124, 1, 43, 47), (-104, 3, 41, 48), (-84, 5, 38, 50), (-60, 7, 35, 52), (-34, 9, 33, 53)], "hull", dz=4)
fuse += [
    {"o": [-1, 43, -126], "s": [2, 4, 3], "skin": "dark"},                    # nose tip
    {"o": [-9, 32, -34], "s": [18, 6, 50], "skin": "grey"},                   # cockpit floor / tub bottom
    {"o": [-11, 36, -34], "s": [2, 18, 50], "skin": "hull"},                  # cockpit walls (hip height)
    {"o": [9, 36, -34], "s": [2, 18, 50], "skin": "hull"},
    {"o": [-9, 48, -36], "s": [18, 6, 4], "skin": "grey"},                    # instrument hood
    {"o": [-9, 38, 14], "s": [18, 16, 3], "skin": "hull"},                    # rear bulkhead
    {"o": [-7, 44, -33], "s": [14, 3, 2], "skin": "dark"},                    # panel
    {"o": [-8, 45, -40], "s": [16, 1, 5], "skin": "red"},                     # red stripe on nose
    {"o": [-6, 45, -66], "s": [12, 1, 4], "skin": "red"},
    {"o": [-4, 47, -92], "s": [8, 1, 3], "skin": "red"},
]
fuse += loft([(17, 10, 32, 56), (44, 10, 32, 56), (64, 9, 34, 52), (74, 7, 36, 48)], "hull", dz=4)
fuse += [{"o": [-11, 32, 17], "s": [1, 24, 30], "skin": "red"}, {"o": [10, 32, 17], "s": [1, 24, 30], "skin": "red"}]
fuse += seat_set(0, 38, -2, w=14, d=12, back_h=12, skin="fabric", head=False)

# canopy: sparse frame so nothing sits near the pilot's eyes
canopy = [
    {"o": [-9, 53, -33], "s": [18, 27, 1], "skin": "glass", "rot": [24, 0, 0], "pivot": [0, 53, -33]},   # windscreen
    {"o": [-10, 53, -33], "s": [2, 27, 2], "skin": "dark", "rot": [24, 0, 0], "pivot": [0, 53, -33]},    # A-pillars
    {"o": [8, 53, -33], "s": [2, 27, 2], "skin": "dark", "rot": [24, 0, 0], "pivot": [0, 53, -33]},
    {"o": [-10, 54, -30], "s": [1, 24, 44], "skin": "glass"},                                            # side panes
    {"o": [9, 54, -30], "s": [1, 24, 44], "skin": "glass"},
    {"o": [-10, 78, -22], "s": [20, 1, 34], "skin": "glass"},                                            # roof
    {"o": [-11, 77, -22], "s": [2, 2, 36], "skin": "dark"},                                              # roof rails
    {"o": [9, 77, -22], "s": [2, 2, 36], "skin": "dark"},
    {"o": [-11, 54, 12], "s": [2, 24, 3], "skin": "dark"},                                               # rear posts
    {"o": [9, 54, 12], "s": [2, 24, 3], "skin": "dark"},
    {"o": [-10, 77, 12], "s": [20, 2, 3], "skin": "dark"},
    {"o": [-10, 77, -24], "s": [20, 2, 2], "skin": "dark"},
]

# astromech
r2 = [
    {"o": [-5, 54, 19], "s": [10, 10, 10], "skin": "hull"},
    {"o": [-4, 64, 20], "s": [8, 4, 8], "skin": "hull"},
    {"o": [-3, 68, 21], "s": [6, 2, 6], "skin": "blue"},
    {"o": [-1, 66, 19], "s": [2, 2, 1], "skin": "lens"},
    {"o": [-2, 68, 26], "s": [4, 3, 1], "skin": "blue"},
]

# ---------------------------------------------------------------- engines (four nacelles) + gear
eng = []
for sx in (1, -1):
    for cy in (59, 29):
        cx = 17 * sx
        eng += cyl_z(cx, cy, 24, 84, 22, "engine")
        eng += cyl_z(cx, cy, 20, 4, 16, "dark")                                # intake
        eng += cyl_z(cx, cy, 108, 2, 14, "dark")
        eng.append({"o": [cx - 5, cy - 5, 110], "s": [10, 10, 1], "skin": "ion"})   # exhaust glow
        eng.append({"o": [cx - 11, cy - 1, 60], "s": [22, 2, 3], "skin": "red"})   # band
gear = [
    {"o": [-1, 4, -70], "s": [2, 29, 2], "skin": "grey"},
    {"o": [-4, 0, -74], "s": [8, 4, 10], "skin": "dark"},
    {"o": [-15, 4, 34], "s": [2, 16, 2], "skin": "grey"}, {"o": [13, 4, 34], "s": [2, 16, 2], "skin": "grey"},
    {"o": [-19, 0, 30], "s": [8, 4, 10], "skin": "dark"}, {"o": [11, 0, 30], "s": [8, 4, 10], "skin": "dark"},
]

# ---------------------------------------------------------------- S-foils (bone-local, pivot at root, extends +x for sign=+1)
def wing(sign, y0):
    def X(x, w):
        return x if sign > 0 else -x - w
    return [
        {"o": [X(14, 52), y0 - 1, 8], "s": [52, 3, 44], "skin": "hull"},
        {"o": [X(66, 26), y0 - 1, 16], "s": [26, 3, 30], "skin": "hull"},
        {"o": [X(14, 52), y0 + 2, 8], "s": [52, 1, 5], "skin": "grey"},
        {"o": [X(66, 24), y0 + 2, 46], "s": [24, 1, 6], "skin": "red"},
        {"o": [X(84, 12), y0 - 3, 14], "s": [12, 7, 26], "skin": "grey"},          # cannon housing
        {"o": [X(91, 2), y0 - 1, -56], "s": [2, 2, 8], "skin": "lens"},               # muzzle glow (front tip)
    ] + cyl_z(88 * sign, y0 + 0.0, -50, 66, 4, "dark") + [
        {"o": [X(80, 4), y0 - 2, 20], "s": [4, 4, 30], "skin": "dark"},
    ]

BIND = 4
wing_defs = [("wing_ul", 1, 58, -1), ("wing_ll", 1, 32, 1), ("wing_ur", -1, 58, 1), ("wing_lr", -1, 32, -1)]
bones = [
    {"name": "body", "parent": None, "pivot": [0, 44, 0], "cubes": fuse + canopy + gear + eng},
    {"name": "r2", "parent": "body", "pivot": [0, 60, 24], "cubes": r2},
]
for name, sign, y0, up in wing_defs:
    # +x wing: negative z-rotation raises the tip; -x wing: positive
    rz = BIND * up * (1 if sign > 0 else -1)
    bones.append({"name": name, "parent": "body", "pivot": [14 * sign, y0, 30], "rotation": [0, 0, rz], "cubes": wing(sign, y0)})

OPEN = 11
def wanim(name, sign, up):
    k = up * (1 if sign > 0 else -1)
    return {name: {"rotation": ["0", "0", f"variable.open * {OPEN * k}"]}}

anims = {
    "wings": anim(merge(*[wanim(n, s, u) for n, s, y, u in wing_defs])),
    "fly": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 140) * 0.3", "0"]}},
        {"r2": {"rotation": ["0", "math.sin(query.life_time * 120) * 25", "0"]}},
    )),
    "idle": anim(merge({"r2": {"rotation": ["0", "math.sin(query.life_time * 30) * 10", "0"]}})),
}

SPEC = {
    "id": "x_wing",
    "name": "X-Wing Starfighter",
    "egg": ("#d5dade", "#c9352b"),
    "glow": True,
    "scale": 1.0,
    "visible": [12.0, 6.0, 2.6],
    "bones": bones,
    "skins": {"default": hull, "hull": hull, "red": red, "dark": dark, "grey": grey, "engine": engine, "ion": ion,
              "lens": lens, "blue": blue, "glass": glass("#9fe4ff"), "fabric": fabric("#3b3f47", "#555b66")},
    "pre_animation": ["variable.open = math.lerp(variable.open, query.has_rider ? 1 : 0, 0.06);"],
    "anims": anims,
    "play": ["wings", {"fly": "query.has_rider"}, {"idle": "!query.has_rider"}],
    "behavior": {
        "role": "mount",
        "health": 100, "speed": 0.45, "damage": 0, "box": [3.0, 2.4],
        "hover": True, "fly_speed": 0.75, "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle", "starfighter"],
        "ride": {"seats": [[0, 2.4, -0.15]]},
        "sound": ("phantom", [0.7, 0.9]),
        "xp": 0,
    },
}
