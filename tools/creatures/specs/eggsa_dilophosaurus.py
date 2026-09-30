"""Frillneck Dilophosaurus - twin-crested hunter with a flaring neck frill."""
from lib import *
from specs.eggsa_kit import *

bones = biped(9, 9, 16, 13, 4, 5, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=8, thigh_h=7, hip_z=2, toes=3)
body = get(bones, "body")
for z in range(-6, 8, 4):
    body["cubes"].append(cube([-1, 22, z], [2, 2, 3], "stripe"))
bones.append(bone("neck", "body", [0, 20, -8], [cube([-2.5, 18, -15], [5, 9, 6], "hide")]))
bones.append(bone("frill", "neck", [0, 22, -12], [cube([-7, 16, -13], [14, 11, 1], "frill", rot=[10, 0, 0], pivot=[0, 22, -13])] +
                 [cube([-6 + i * 3, 27, -13], [2, 2, 1], "frill_tip") for i in range(5)]))
hc = [cube([-3, 22, -26], [6, 6, 11], "hide"), cube([-2, 22, -29], [4, 4, 4], "hide")]
pair(hc, cube([1, 28, -24], [1, 5, 6], "crest", rot=[-10, 0, 0]))
side_eyes(hc, 3, 25, -21, 2, "eye")
for z in (-27, -24):
    pair(hc, cube([1.5, 21, z], [1, 2, 1], "tooth"))
bones.append(bone("head", "neck", [0, 23, -15], hc))
bones.append(bone("jaw", "head", [0, 23, -16], [cube([-2, 20, -28], [4, 2, 12], "jaw")]))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    xc = sx * 4.5
    bones.append(bone(nm, "body", [xc, 20, -6], [cube([xc - 1, 15, -8], [2, 6, 2], "hide"), cube([xc - 0.5, 14, -9], [1, 2, 1], "claw")]))
tail(bones, "body", 15, 8, 6, 6, 7, 7, taper=0.8, skin="hide", tip_skin="stripe")
hide = pelt("#e08a2e", "#b8641c", belly="#f3dda0", belly_y=16, seed=61, stripes=("#2b6a5a", 1.1, 0.55, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#b8641c", "#8f4a14", seed=62), "stripe": solid("#2b6a5a"),
         "frill": pelt("#2f8f7a", "#1e6a5a", seed=63, stripes=("#f2c84a", 0.9, 0.5, "x")), "frill_tip": solid("#f2c84a"),
         "crest": plates("#e5523a", 0.7), "jaw": pelt("#f0d29a", "#d4b47a", seed=64), "tooth": tooth,
         "claw": claw_paint(), "eye": eye_color("#e83a2a")}
an = biped_anims(tail_bones=[f"tail{i}" for i in range(6)], amp=32, freq=46, arms=["arm_l", "arm_r"], neck="neck",
                 extra_idle=sway("frill", 6, 100, 0))
an["attack"] = bite_anim("jaw", "head", "neck", 35)
SPEC = finish("dilophosaurus", "Frillneck Dilophosaurus", ("#e08a2e", "#2f8f7a"), bones, skins, an, STD_PLAY_ATK, {
    "role": "hostile", "health": 32, "speed": 0.34, "damage": 5, "box": [0.8, 1.5], "family": ["dinosaur"],
    "loot": [("minecraft:bone", 0, 2), ("minecraft:feather", 0, 2)], "sound": ("phantom", [1.1, 1.3]), "xp": 8,
    "spawn": {"biomes": ["jungle", "swamp"], "weight": 6, "herd": [1, 2]}})
