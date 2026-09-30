"""Waddles the Dodo - round, friendly, slightly silly."""
from lib import *
from specs.eggsa_kit import *

bones = biped(10, 10, 12, 5, 2, 2, skin="feather", leg_skin="leg", foot_skin="leg", foot_len=5, hip_z=0, toes=0, gap=-0.5)
body = get(bones, "body")
body["cubes"] += [cube([-6, 6, -5], [12, 8, 10], "feather"), cube([-4, 5, -4], [8, 1, 8], "belly")]
bones.append(bone("neck", "body", [0, 13, -5], [cube([-3, 12, -8], [6, 7, 5], "feather")]))
hc = [cube([-3.5, 17, -13], [7, 7, 8], "feather"), cube([-2.5, 19, -21], [5, 5, 8], "beak"), cube([-1.5, 17.5, -20], [3, 2, 6], "beak_lo"),
      cube([-2, 16, -20], [4, 1, 5], "beak_lo"), cube([-1.5, 18, -23], [3, 3, 2], "beak_tip", rot=[-25, 0, 0])]
eyes(hc, 2.2, 21, -13, 2, "eye_dark")
for i in range(3):
    hc.append(cube([-1 + (i - 1) * 1.6, 24, -10 + i], [1, 3, 1], "wisp"))
bones.append(bone("head", "neck", [0, 18, -8], hc))
for nm, sx in (("wing_l", 1), ("wing_r", -1)):
    bones.append(bone(nm, "body", [sx * 6, 12, -1], [cube([sx * 6 - (0 if sx > 0 else 1.0) - (0 if sx > 0 else 0), 6, -3], [1, 5, 6], "wing")]))
tail(bones, "body", 9, 5, 1, 6, 6, 3, taper=1, skin="feather")
tf = get(bones, "tail0")
for i, a in enumerate((-30, 0, 30)):
    tf["cubes"].append(cube([-1, 12, 6], [2, 4, 4], "wisp", rot=[-20, a, 0], pivot=[0, 12, 6]))
fe = pelt("#8b8a94", "#6c6b77", belly="#c9c8d2", belly_y=8, seed=201, patch=2.0, fine=0.2)
skins = {"default": fe, "feather": fe, "belly": flat("#c9c8d2"), "wing": pelt("#6c6b77", "#54535e", seed=202),
         "beak": pelt("#d9c96a", "#b7a74a", seed=203), "beak_lo": flat("#c4b459"), "beak_tip": flat("#5e6a4a"),
         "wisp": pelt("#e6e2f0", "#c9c5d6", seed=204), "leg": solid("#d1a24a"), "claw": claw_paint(), "eye_dark": eye_dark}
an = biped_anims(tail_bones=["tail0"], amp=42, freq=60, arms=["wing_l", "wing_r"], neck="neck", bob_amp=0.4,
                 extra_walk={"body": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 60) * 4 * query.modified_move_speed"]}})
SPEC = finish("dodo", "Waddles the Dodo", ("#8b8a94", "#d9c96a"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 8, "speed": 0.2, "box": [0.7, 1.0], "family": ["dodo"],
    "loot": [("minecraft:feather", 1, 3), ("minecraft:egg", 0, 1)], "sound": ("parrot", [0.7, 0.9]),
    "spawn": {"biomes": ["beach", "jungle", "forest"], "weight": 10, "herd": [2, 4]}})
