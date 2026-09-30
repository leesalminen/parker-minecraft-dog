"""Thunderbeak Terror Bird - tall flightless predator, fast rideable."""
from lib import *
from specs.eggsa_kit import *

bones = biped(9, 12, 14, 17, 3, 3, skin="feather", leg_skin="leg", foot_skin="leg", foot_len=7, hip_z=1, toes=3, gap=-0.5)
body = get(bones, "body")
body["cubes"].append(cube([-5, 19, -9], [10, 9, 6], "feather"))
for i in range(3):
    body["cubes"].append(cube([-1.5, 28, -4 + i * 4], [3, 2, 4], "plume"))
bones.append(bone("neck", "body", [0, 27, -8], [cube([-2, 26, -10], [4, 10, 4], "feather", rot=[-8, 0, 0], pivot=[0, 26, -8]),
                                                cube([-2.5, 26, -10], [5, 4, 4], "collar")]))
hc = [cube([-3, 34, -17], [6, 7, 9], "feather"), cube([-2, 36, -24], [4, 5, 7], "beak"), cube([-1.5, 33, -23], [3, 4, 2], "beak", rot=[20, 0, 0]),
      cube([-1.5, 34.5, -22], [3, 1.5, 6], "beak_lo")]
eyes(hc, 2, 38, -17, 2, "eye_c")
for i in range(3):
    hc.append(cube([-1, 41, -15 + i * 2], [2, 3 + (i % 2), 2], "plume"))
bones.append(bone("head", "neck", [0, 35, -12], hc))
for nm, sx in (("wing_l", 1), ("wing_r", -1)):
    xc = sx * 5
    bones.append(bone(nm, "body", [xc, 26, -4], [cube([xc - 1 + (sx > 0), 17, -6], [2, 10, 8], "wing")]))
tail(bones, "body", 20, 7, 3, 6, 5, 5, taper=0.9, skin="feather")
for i, a in enumerate((-40, -14, 14, 40)):
    get(bones, "tail2")["cubes"].append(cube([-1, 21, 12], [2, 2, 8], "plume", rot=[0, a, 0], pivot=[0, 21, 12]))
fe = pelt("#5a4a8a", "#3f3268", belly="#d8cfe8", belly_y=19, seed=111, patch=2.5, fine=0.2, stripes=("#2b2148", 1.3, 0.6, "y"))
skins = {"default": fe, "feather": fe, "wing": pelt("#3f3268", "#2b2148", seed=112), "plume": pelt("#d8503a", "#f0a030", seed=113, patch=1.5),
         "collar": pelt("#eeeaf2", "#cfc8dc", seed=114), "beak": pelt("#e8c04a", "#b8902a", seed=115), "beak_lo": flat("#a8801e"),
         "leg": pelt("#c8a05a", "#a07c3c", seed=116, cells=1.5), "claw": claw_paint("#221c18"), "eye_c": eye_color("#f24a2a")}
an = biped_anims(tail_bones=["tail0", "tail1", "tail2"], amp=38, freq=54, arms=["wing_l", "wing_r"], neck="neck")
SPEC = finish("terror_bird", "Thunderbeak Terror Bird", ("#5a4a8a", "#e8c04a"), bones, skins, an, STD_PLAY, {
    "role": "mount", "health": 40, "speed": 0.42, "damage": 7, "box": [0.9, 2.5], "family": ["terror_bird"],
    "ride": {"seats": [[0, 1.85, 0.0]], "jump": 0.9}, "loot": [("minecraft:feather", 1, 4), ("minecraft:bone", 0, 2)],
    "sound": ("parrot", [0.6, 0.75]), "spawn": {"biomes": ["plains", "savanna"], "weight": 5, "herd": [1, 2]}})
