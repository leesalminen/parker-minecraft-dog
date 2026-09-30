"""Pocket Compy - tiny tameable Compsognathus with huge eyes."""
from lib import *
from specs.eggsa_kit import *

bones = biped(5, 5, 9, 6, 2, 2, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=4, hip_z=1, toes=0)
body = get(bones, "body")
body["cubes"].append(cube([-0.5, 11, -3], [1, 1, 8], "stripe"))
bones.append(bone("neck", "body", [0, 10, -4], [cube([-1.5, 9, -7], [3, 5, 3], "hide", rot=[-10, 0, 0], pivot=[0, 9, -5])]))
hc = [cube([-3, 12, -13], [6, 5, 7], "hide"), cube([-2, 12, -15], [4, 3, 2], "hide"), cube([-2, 11, -14], [4, 1, 3], "belly")]
pair(hc, cube([1, 14, -13.5], [2, 2, 1], "eye"))
pair(hc, cube([1.5, 17, -10], [1, 2, 1], "stripe"))
bones.append(bone("head", "neck", [0, 13, -8], hc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    bones.append(bone(nm, "body", [sx * 2.5, 10, -3], [cube([sx * 2.5 - (0.5 if sx > 0 else 0.5), 7, -4], [1, 4, 1], "hide")]))
tail(bones, "body", 8, 5, 5, 3, 3, 4, taper=0.85, skin="hide", tip_skin="stripe")
hide = pelt("#9fd8b0", "#7cbf94", belly="#f4ecc8", belly_y=8, seed=141, patch=2.0, spots=("#5aa07a", 1.6, 0.66))
skins = {"default": hide, "hide": hide, "leg": pelt("#7cbf94", "#5fa279", seed=142), "stripe": pelt("#ffb35a", "#f28a3a", seed=143),
         "belly": flat("#f4ecc8"), "eye": eye_dark, "claw": claw_paint("#3a3028")}
an = biped_anims(tail_bones=["tail0", "tail1", "tail2", "tail3", "tail4"], amp=40, freq=70, arms=["arm_l", "arm_r"], neck="neck", bob_amp=0.3)
SPEC = finish("compsognathus", "Pocket Compy", ("#9fd8b0", "#ffb35a"), bones, skins, an, STD_PLAY, {
    "role": "companion", "health": 10, "speed": 0.34, "box": [0.4, 0.7], "family": ["compy"],
    "tame_items": ["minecraft:cod", "minecraft:salmon", "minecraft:chicken"],
    "loot": [("minecraft:feather", 0, 1)], "sound": ("parrot", [1.7, 2.0]),
    "spawn": {"biomes": ["jungle", "forest", "swamp"], "weight": 10, "herd": [2, 4]}})
