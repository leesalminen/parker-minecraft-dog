"""Mossback Giant Sloth - upright, shaggy, sleepy; long arms with big claws."""
from lib import *
from specs.eggsa_kit import *

bones = biped(16, 20, 14, 12, 6, 6, skin="fur", leg_skin="fur_d", foot_skin="fur_d", foot_len=8, hip_z=2, toes=3, gap=-1)
body = get(bones, "body")
body["cubes"] += [cube([-7, 31, -7], [14, 5, 10], "fur"), cube([-6, 12, 6], [12, 10, 4], "moss")]
for i in range(6):                      # shaggy moss tufts down the back
    body["cubes"].append(cube([-6 + (i % 3) * 4.5, 14 + (i // 3) * 10, 8], [3, 6, 3], "moss"))
bones.append(bone("neck", "body", [0, 33, -7], [cube([-3, 31, -11], [6, 6, 6], "fur_d")]))
hc = [cube([-3.5, 30, -18], [7, 8, 8], "face"), cube([-2.5, 30, -22], [5, 5, 5], "face"), cube([-2, 32, -23], [4, 2, 1], "nose"),
      cube([-4, 36, -16], [8, 3, 6], "fur")]
pair(hc, cube([1.5, 34, -18], [2, 2, 1], "patch"))
pair(hc, cube([2, 34, -18.5], [1, 1, 1], "eye_dark"))
bones.append(bone("head", "neck", [0, 33, -12], hc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    xc = sx * 10
    cs = [cube([xc - 2.5, 14, -4], [5, 20, 6], "fur_d"), cube([xc - 3, 24, -5], [6, 8, 8], "fur")]
    for i in range(3):
        cs.append(cube([xc - 2 + i * 1.7, 4, -3.5], [1, 11, 2], "claw", rot=[-12, 0, 0], pivot=[xc, 14, -3]))
    bones.append(bone(nm, "body", [xc, 33, -1], cs))
tail(bones, "body", 12, 8, 1, 6, 6, 4, skin="fur_d")
fur = pelt("#7a6448", "#584730", seed=121, patch=2.0, fine=0.26, spots=("#5f7a45", 3.5, 0.6))
skins = {"default": fur, "fur": fur, "fur_d": pelt("#63503a", "#463826", seed=122, patch=2.0, fine=0.26),
         "moss": pelt("#6e8c4a", "#4a6a32", seed=123, patch=1.5, fine=0.3), "face": pelt("#a08862", "#80694a", seed=124),
         "nose": flat("#241a14"), "patch": pelt("#3c2e22", "#2a1f16", seed=125), "eye_dark": eye_dark, "claw": solid("#e2d8b8", 0.1)}
an = biped_anims(tail_bones=["tail0"], amp=22, freq=30, arms=["arm_l", "arm_r"], bob_amp=0.3,
                 extra_idle=merge(sway("arm_l", 8, 40, 0), sway("arm_r", 8, 40, 0, 1.5)))
SPEC = finish("giant_sloth", "Mossback Giant Sloth", ("#7a6448", "#6e8c4a"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 50, "speed": 0.14, "box": [1.3, 2.4], "knockback_resist": 0.3, "family": ["sloth"],
    "loot": [("minecraft:leather", 1, 3), ("minecraft:moss_block", 0, 2)], "sound": ("polarbear", [0.5, 0.65]),
    "spawn": {"biomes": ["jungle", "forest", "swamp"], "weight": 6, "herd": [1, 2]}})
