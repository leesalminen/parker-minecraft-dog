"""Twin-ion starfighter (TIE-style): hollow spherical cockpit pod, two hexagonal solar panels, chin cannons.
Big open spoke-frame canopy so the pilot sees out over a wide field.  Model faces -Z, y up, ground y=0.
Flight + guns live in scripts/vehicles.js (family 'starfighter')."""
import math
from lib import *
from specs.vehicles_common import *

CY, RP, RH = 52, 26, 50            # pod centre height, pod radius, hex panel circumradius

hull = paint("#8c959d", "#454c54", 61, 10.0)
dark = paint("#2c3238", "#14171b", 63, 8.0)
struts = paint("#59616a", "#2b3036", 65, 7.0)
ion = lamp("#5fc8ff")
lens = lamp("#7fe8ff")

# ---------------------------------------------------------------- pod: hollow shell rear/equator, open spoke dome in front
pod = []
z = -8
while z < RP:
    zc = z + 2
    r = math.sqrt(max(0.0, RP * RP - zc * zc))
    R = int(round(r))
    if R <= 6:
        pod.append({"o": [-max(R, 3), CY - max(R, 3), z], "s": [2 * max(R, 3), 2 * max(R, 3), 4], "skin": "hull"})
    else:
        pod += ring_z(0, CY, z, R, 3, 4, "hull")
    z += 4
pod.append({"o": [-6, CY - 6, RP - 2], "s": [12, 12, 2], "skin": "ion"})              # ion exhaust plate
pod.append({"o": [-9, CY + RP - 1, -6], "s": [18, 2, 14], "skin": "dark"})           # top hatch
pod.append({"o": [-3, CY + RP + 1, -2], "s": [6, 1, 6], "skin": "struts"})
for zz, R in ((-14, 23), (-22, 19), (-30, 13), (-36, 7)):                            # dome frames
    pod += ring_z(0, CY, zz, R, 2, 2, "struts")
for i, (z0, z1, r0, r1) in enumerate(((-8, -14, 25, 23), (-14, -22, 23, 19), (-22, -30, 19, 13), (-30, -36, 13, 7))):
    zm, rm = (z0 + z1) / 2.0, (r0 + r1) / 2.0
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        pod.append({"o": [sx * rm - 1, CY + sy * rm - 1, min(z0, z1)], "s": [2, 2, abs(z1 - z0)], "skin": "struts"})

# equator collars + pylons
pylons = []
for s in (1, -1):
    x0 = 24 if s == 1 else -30
    pylons.append({"o": [x0, CY - 11, -11], "s": [6, 22, 22], "skin": "dark"})
    px = 30 if s == 1 else -46
    pylons.append({"o": [px, CY - 4, -7], "s": [16, 8, 14], "skin": "hull"})
    pylons.append({"o": [px + (2 if s == 1 else 0), CY - 6, -9], "s": [12, 12, 18], "skin": "struts"})

# chin cannons
guns = []
for s in (1, -1):
    gx = 9 * s
    guns.append({"o": [gx - 4, 28, -22], "s": [8, 6, 16], "skin": "dark"})
    guns += cyl_z(gx, 31, -34, 14, 4, "struts")
    guns.append({"o": [gx - 1, 30, -35], "s": [2, 2, 1], "skin": "lens"})

# ---------------------------------------------------------------- hexagonal wing panels
def panel(sign):
    cubes = []
    zc = -RH * 0.866 + 1.5
    while zc < RH * 0.866:
        hh = RH - abs(zc) * (RH / 2.0) / (RH * 0.866)
        h = max(2, int(round(2 * hh)))
        x0 = 46 if sign > 0 else -50
        cubes.append({"o": [x0, CY - h / 2.0, zc - 1.5], "s": [4, h, 3], "skin": "panel"})
        zc += 3
    x0 = 44 if sign > 0 else -52
    cubes.append({"o": [x0, CY - 6, -6], "s": [8, 12, 12], "skin": "dark"})           # hub
    return cubes

bones = [
    {"name": "body", "parent": None, "pivot": [0, CY, 0], "cubes": pod + pylons + guns},
    {"name": "wing_l", "parent": "body", "pivot": [46, CY, 0], "cubes": panel(1)},
    {"name": "wing_r", "parent": "body", "pivot": [-46, CY, 0], "cubes": panel(-1)},
]

anims = {
    "fly": anim(merge(
        {"body": {"position": ["0", "math.sin(query.life_time * 150) * 0.35", "0"]}},
        {"wing_l": {"rotation": ["math.sin(query.life_time * 230) * 0.8", "0", "0"]}},
        {"wing_r": {"rotation": ["math.sin(query.life_time * 230 + 1.3) * 0.8", "0", "0"]}},
    )),
    "idle": anim(merge({"body": {"position": ["0", "math.sin(query.life_time * 40) * 0.1", "0"]}})),
}

SPEC = {
    "id": "tie_fighter",
    "name": "Twin-Ion Fighter",
    "egg": ("#8c959d", "#5fc8ff"),
    "glow": True,
    "scale": 1.0,
    "visible": [9.0, 8.0, 3.2],
    "bones": bones,
    "skins": {"default": hull, "hull": hull, "dark": dark, "struts": struts, "ion": ion, "lens": lens,
              "panel": panel_paint(CY, RH)},
    "anims": anims,
    "play": [{"fly": "query.has_rider"}, {"idle": "!query.has_rider"}],
    "behavior": {
        "role": "mount",
        "health": 80, "speed": 0.4, "damage": 0, "box": [2.0, 3.4],
        "hover": True, "fly_speed": 0.7, "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle", "starfighter"],
        "ride": {"seats": [[0, 2.0, 0.2]]},
        "sound": ("phantom", [1.3, 1.6]),
        "xp": 0,
    },
}
