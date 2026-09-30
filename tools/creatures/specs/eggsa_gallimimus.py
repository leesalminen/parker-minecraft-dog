"""Dashstrider Gallimimus - lanky ostrich-dino, the fast saddle mount."""
from lib import *
from specs.eggsa_kit import *

bones = biped(8, 9, 14, 18, 3, 4, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=8, hip_z=1, toes=3, thigh_h=9, gap=-0.5)
body = get(bones, "body")
body["cubes"].append(cube([-3, 27, -8], [6, 2, 12], "back"))
prev = "body"
segs = [(-6, 25, 5, 8), (-10, 31, 4, 8), (-13, 37, 4, 7)]
for i, (z, y, w, h) in enumerate(segs):
    nm = f"neck{i}"
    bones.append(bone(nm, prev, [0, y - 1, z + 3], [cube([-w / 2, y, z - 3], [w, h, 5], "neck")]))
    prev = nm
hc = [cube([-2.5, 42, -22], [5, 5, 8], "hide"), cube([-1.5, 42, -27], [3, 3, 5], "beak"), cube([-1.5, 41, -26], [3, 1, 4], "beak_lo")]
side_eyes(hc, 2.5, 45, -19, 2, "eye")
pair(hc, cube([1, 44, -27], [1, 1, 1], "dark"))
bones.append(bone("head", prev, [0, 43, -17], hc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    bones.append(bone(nm, "body", [sx * 4, 25, -6], [cube([sx * 4 - 0.5, 19, -8], [1, 7, 2], "hide"), cube([sx * 4 - 0.5, 18, -9], [1, 2, 1], "claw")]))
tail(bones, "body", 22, 6, 5, 4, 4, 6, taper=0.9, skin="hide", tip_skin="stripe", rise=0.3)
hide = pelt("#c9a870", "#a5854e", belly="#f2e6c4", belly_y=21, seed=211, stripes=("#6e4f2a", 1.3, 0.65, "z"))
skins = {"default": hide, "hide": hide, "back": pelt("#7a5a34", "#5c4222", seed=212), "neck": pelt("#e8a09a", "#c98078", seed=213),
         "leg": pelt("#a5854e", "#846838", seed=214), "beak": pelt("#e8c46a", "#c49a3a", seed=215), "beak_lo": flat("#b48a2e"),
         "stripe": solid("#6e4f2a"), "claw": claw_paint(), "eye": eye_color("#e8f0a0"), "dark": flat("#3a2a18")}
an = biped_anims(tail_bones=[f"tail{i}" for i in range(5)], amp=44, freq=56, arms=["arm_l", "arm_r"], neck="neck0", bob_amp=0.4)
an["walk"]["bones"].update(swing({"neck1": 0, "neck2": 180}, 6, 0, 56))
SPEC = finish("gallimimus", "Dashstrider Gallimimus", ("#c9a870", "#e8a09a"), bones, skins, an, STD_PLAY, {
    "role": "mount", "health": 28, "speed": 0.46, "damage": 3, "box": [0.8, 2.3], "family": ["dinosaur"],
    "ride": {"seats": [[0, 1.75, 0.1]], "jump": 0.8}, "loot": [("minecraft:feather", 1, 3), ("minecraft:chicken", 0, 2)],
    "sound": ("horse", [1.4, 1.6]), "spawn": {"biomes": ["plains", "savanna"], "weight": 8, "herd": [3, 5]}})
