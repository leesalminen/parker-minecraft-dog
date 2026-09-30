"""Sailback Spinosaurus - croc-snouted river hunter with a huge dorsal sail."""
from lib import *
from specs.eggsa_kit import *

bones = biped(12, 14, 26, 14, 5, 6, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=10, hip_z=2, toes=3, thigh_h=8)
body = get(bones, "body")
body["cubes"].append(cube([-5, 16, -16], [10, 12, 8], "hide"))
sail_h = [4, 8, 12, 15, 17, 18, 17, 14, 10, 6]
for i, h in enumerate(sail_h):
    z = -12 + i * 2.5
    body["cubes"].append(cube([-1, 28, z], [2, h, 3], "spine"))
    body["cubes"].append(cube([-1, 28, z + 0.5], [2, max(1, h - 5), 3], "sail")) if False else None
for i, h in enumerate(sail_h):
    z = -12 + i * 2.5
    body["cubes"].append(cube([-0.5, 28 + 2, z], [1, h - 2, 3], "sail"))
bones.append(bone("neck", "body", [0, 25, -14], [cube([-3.5, 22, -21], [7, 9, 8], "hide")]))
hc = [cube([-3.5, 22, -28], [7, 7, 9], "hide"), cube([-2.5, 23, -40], [5, 4, 13], "snout"), cube([-3, 27, -40], [6, 2, 3], "snout"), cube([-0.5, 29, -30], [1, 3, 7], "spine")]
side_eyes(hc, 3.5, 26, -27, 2, "eye")
for z in (-39, -36, -33):
    pair(hc, cube([1.5, 21.5, z], [1, 2, 1], "tooth"))
bones.append(bone("head", "neck", [0, 25, -21], hc))
jc = [cube([-2, 21, -39], [4, 2, 12], "belly"), cube([-3, 21, -29], [6, 2, 6], "belly")]
for z in (-38, -35):
    pair(jc, cube([1, 23, z], [1, 2, 1], "tooth"))
bones.append(bone("jaw", "head", [0, 22, -28], jc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    xc = sx * 6.5
    cs = [cube([xc - 1.5, 19, -18], [3, 8, 3], "hide")] + [cube([xc - 1.5 + i * 1.2, 17, -19.5], [1, 3, 2], "claw") for i in range(3)]
    bones.append(bone(nm, "body", [xc, 26, -16], cs))
tail(bones, "body", 16, 13, 6, 4, 11, 7, taper=0.9, skin="hide", tip_skin="sail")
hide = pelt("#3f7f6a", "#2c5e4d", belly="#d9d2a0", belly_y=19, seed=161, stripes=("#1c3f34", 0.7, 0.6, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#2f6a58", "#214d40", seed=162), "spine": solid("#b8452e"),
         "sail": pelt("#e5643c", "#c04a2a", seed=163, stripes=("#f4b04a", 0.8, 0.5, "z")), "snout": pelt("#5a9080", "#3f7264", seed=164),
         "belly": pelt("#d9d2a0", "#b8b078", seed=165), "tooth": tooth, "claw": claw_paint("#1f1a16"), "eye": eye_color("#f0a020")}
an = biped_anims(tail_bones=[f"tail{i}" for i in range(6)], amp=28, freq=38, arms=["arm_l", "arm_r"], neck="neck")
an["attack"] = bite_anim("jaw", "head", "neck", 35)
SPEC = finish("spinosaurus", "Sailback Spinosaurus", ("#3f7f6a", "#e5643c"), bones, skins, an, STD_PLAY_ATK, {
    "role": "hostile", "health": 90, "speed": 0.3, "damage": 11, "box": [1.3, 2.2], "knockback_resist": 0.5, "family": ["dinosaur"],
    "loot": [("minecraft:bone", 2, 5), ("minecraft:cod", 1, 3)], "sound": ("ravager", [0.6, 0.75]), "xp": 20,
    "spawn": {"biomes": ["swamp", "jungle", "river"], "weight": 3, "herd": [1, 1]}})
