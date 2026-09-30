"""King Tyrannosaurus - huge biting predator with tiny arms."""
from lib import *
from specs.eggsa_kit import *

bones = biped(16, 18, 26, 20, 7, 8, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=14, thigh_h=12, hip_z=3, toes=3)
body = get(bones, "body")
body["cubes"].append(cube([-7, 22, -21], [14, 15, 8], "hide"))
for z in range(-14, 12, 6):
    body["cubes"].append(cube([-1.5, 36, z], [3, 2, 4], "ridge"))
bones.append(bone("neck", "body", [0, 34, -16], [cube([-4.5, 30, -24], [9, 11, 10], "hide")]))
hc = [cube([-5, 31, -40], [10, 10, 17], "hide"), cube([-4, 41, -38], [8, 1, 8], "ridge")]
pair(hc, cube([2, 41, -30], [3, 2, 5], "brow"))
side_eyes(hc, 5, 37, -31, 2, "eye")
pair(hc, cube([2, 38, -41], [1, 1, 1], "dark"))
for z in (-38, -34, -30):
    pair(hc, cube([3.5, 28.5, z], [1, 3, 1], "tooth"))
bones.append(bone("head", "neck", [0, 35, -24], hc))
jc = [cube([-4, 28, -39], [8, 3, 15], "jaw")]
for z in (-38, -34, -30):
    pair(jc, cube([2.5, 31, z], [1, 2, 1], "tooth"))
jc.append(cube([-3, 31, -38], [6, 1, 12], "mouth"))
bones.append(bone("jaw", "head", [0, 30, -24], jc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    xc = sx * 6.5
    bones.append(bone(nm, "body", [xc, 32, -13], [cube([xc - 1.5, 24, -16], [3, 9, 3], "hide")] +
                 [cube([xc - 1.5 + i * 1.5, 22, -17], [1, 3, 1], "claw") for i in range(2)]))
tail(bones, "body", 24, 12, 6, 11, 12, 8, taper=0.8, skin="hide", fall=-0.2)
hide = pelt("#6a5a3a", "#54462c", belly="#cdb98a", belly_y=27, seed=41, stripes=("#3a2f1e", 0.8, 0.6, "z"), top=("#3f3323", 0.4), top_y=32)
skins = {"default": hide, "hide": hide, "leg": pelt("#5a4b30", "#463a25", seed=42), "ridge": solid("#3a3020"), "brow": plates("#4a3d28", 0.7),
         "tooth": tooth, "mouth": flat("#8a2f35"), "jaw": pelt("#8a7a54", "#6a5c3c", seed=44), "claw": claw_paint("#1e1a16"),
         "eye": eye_color("#f0c020"), "dark": flat("#1c150e")}
anims = biped_anims(tail_bones=[f"tail{i}" for i in range(6)], amp=30, freq=36, arms=["arm_l", "arm_r"], neck="neck")
anims["attack"] = bite_anim("jaw", "head", "neck", 40)
SPEC = finish("tyrannosaurus", "King Tyrannosaurus", ("#6a5a3a", "#8a2f35"), bones, skins, anims, STD_PLAY_ATK, {
    "role": "hostile", "health": 120, "speed": 0.32, "damage": 14, "box": [1.5, 2.6], "knockback_resist": 0.7,
    "family": ["dinosaur"], "reach": 1.3, "loot": [("minecraft:bone", 2, 6), ("minecraft:leather", 1, 4)],
    "sound": ("ravager", [0.55, 0.7]), "xp": 30, "spawn": {"biomes": ["plains", "forest", "jungle"], "weight": 2, "herd": [1, 1]}})
