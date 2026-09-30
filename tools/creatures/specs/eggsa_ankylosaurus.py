"""Clubtail Ankylosaurus - low armoured tank with a wrecking-ball tail."""
from lib import *
from specs.eggsa_kit import *

bones = quad(20, 9, 26, 5, 5, 5, skin="hide", leg_skin="leg", foot_skin="leg", toes=3, fz=1, bz=1)
body = get(bones, "body")
for x in (-6.5, -1.5, 3.5):                      # armour plate rows
    for z in range(-12, 12, 6):
        body["cubes"].append(cube([x, 14, z], [3, 2, 5], "armor"))
        body["cubes"].append(cube([x + 0.5, 16, z + 1], [2, 1, 3], "armor_hi"))
for z in range(-11, 12, 5):                      # side spikes
    pair(body["cubes"], cube([10, 9, z], [3, 3, 2], "spike", rot=[0, 0, 25], pivot=[10, 10, z + 1]))
hc = [cube([-5, 6, -20], [10, 6, 9], "hide"), cube([-4, 7, -23], [8, 4, 4], "beak"), cube([-4, 12, -19], [8, 2, 6], "armor")]
pair(hc, cube([4, 7, -17], [3, 3, 3], "spike", rot=[0, 35, 0]))
side_eyes(hc, 5, 9, -18, 2, "eye")
bones.append(bone("head", "body", [0, 8, -12], hc))
tail(bones, "body", 6, 13, 4, 8, 6, 7, taper=0.86, skin="hide")
t = get(bones, "tail3")
t["cubes"].append(cube([-6, 4, 27], [12, 9, 8], "club"))
pair(t["cubes"], cube([5, 8, 29], [3, 3, 4], "spike"))
hide = pelt("#8a7a56", "#6d5f42", belly="#cdbf94", belly_y=7, seed=31)
skins = {"default": hide, "hide": hide, "leg": pelt("#6d5f42", "#54492f", seed=33), "armor": plates("#7b6a48", 0.65, "#9a8760"),
         "armor_hi": plates("#a08c62", 0.7), "spike": solid("#e5dcc0"), "club": shell("#6c604a", "#3a3428", 3),
         "beak": pelt("#a29060", "#847548", seed=4), "claw": claw_paint(), "eye": eye_color("#d86a2a")}
anims = quad_anims(tail_bones=["tail0", "tail1", "tail2", "tail3"], amp=20, freq=32)
anims["attack"] = anim({f"tail{i}": {"rotation": ["0", f"math.sin(variable.attack_time * 180) * {35 - i * 4}", "0"]} for i in range(4)}, loop=False)
SPEC = finish("ankylosaurus", "Clubtail Ankylosaurus", ("#8a7a56", "#e5dcc0"), bones, skins, anims, STD_PLAY_ATK, {
    "role": "neutral", "health": 55, "speed": 0.18, "damage": 9, "box": [1.4, 1.1], "knockback_resist": 0.8,
    "family": ["dinosaur"], "loot": [("minecraft:bone", 1, 3), ("minecraft:iron_nugget", 0, 3)],
    "sound": ("golem", [0.6, 0.8]), "spawn": {"biomes": ["mesa", "desert", "savanna"], "weight": 5, "herd": [1, 1]}})
