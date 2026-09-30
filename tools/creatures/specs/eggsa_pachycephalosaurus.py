"""Bonkhead Pachycephalosaurus - dome-skulled head-butter."""
from lib import *
from specs.eggsa_kit import *

bones = biped(8, 9, 14, 12, 4, 4, skin="hide", leg_skin="leg", foot_skin="leg", foot_len=7, hip_z=1, toes=3, thigh_h=6)
body = get(bones, "body")
body["cubes"].append(cube([-3.5, 18, -9], [7, 8, 5], "hide"))
bones.append(bone("neck", "body", [0, 21, -8], [cube([-2.5, 19, -12], [5, 8, 5], "hide")]))
hc = [cube([-3.5, 23, -20], [7, 7, 9], "hide"), cube([-2.5, 23, -23], [5, 4, 3], "hide"), cube([-3, 29, -18], [6, 3, 6], "dome"),
      cube([-2, 32, -17], [4, 1, 4], "dome")]
for i, (x, y, z) in enumerate([(-4, 27, -19), (3, 27, -19), (-4, 25, -15), (3, 25, -15), (-4, 27, -15), (3, 27, -15), (-1, 28, -21)]):
    hc.append(cube([x, y, z], [1, 2, 2], "stud"))
side_eyes(hc, 3.5, 26, -18, 2, "eye")
pair(hc, cube([1, 24, -23], [1, 1, 1], "dark"))
bones.append(bone("head", "neck", [0, 25, -12], hc))
for nm, sx in (("arm_l", 1), ("arm_r", -1)):
    bones.append(bone(nm, "body", [sx * 4.5, 24, -6], [cube([sx * 4.5 - 1, 17, -8], [2, 8, 2], "hide"), cube([sx * 4.5 - 0.5, 15, -9], [1, 2, 1], "claw")]))
tail(bones, "body", 15, 7, 5, 6, 6, 6, taper=0.82, skin="hide", tip_skin="hide")
hide = pelt("#a5533a", "#7c3a26", belly="#f0d8a8", belly_y=14, seed=151, stripes=("#5a2418", 1.0, 0.6, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#7c3a26", "#5f2a1a", seed=152), "dome": plates("#f0dcb0", 0.7, "#ffffff"),
         "stud": solid("#f7ecc8"), "claw": claw_paint(), "eye": eye_color("#fff0a0"), "dark": flat("#2a1810")}
an = biped_anims(tail_bones=[f"tail{i}" for i in range(5)], amp=32, freq=48, arms=["arm_l", "arm_r"], neck="neck")
an["attack"] = anim({"head": {"rotation": ["math.sin(variable.attack_time * 180) * 35", "0", "0"]},
                      "neck": {"rotation": ["math.sin(variable.attack_time * 180) * 25", "0", "0"]},
                      "body": {"rotation": ["math.sin(variable.attack_time * 180) * 8", "0", "0"]}}, loop=False)
SPEC = finish("pachycephalosaurus", "Bonkhead Pachycephalosaurus", ("#a5533a", "#f0dcb0"), bones, skins, an, STD_PLAY_ATK, {
    "role": "neutral", "health": 28, "speed": 0.3, "damage": 6, "box": [0.7, 1.7], "family": ["dinosaur"],
    "loot": [("minecraft:bone", 0, 2), ("minecraft:leather", 0, 1)], "sound": ("golem", [1.1, 1.3]),
    "spawn": {"biomes": ["plains", "forest", "mesa"], "weight": 7, "herd": [2, 3]}})
