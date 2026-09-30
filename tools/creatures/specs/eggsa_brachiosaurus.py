"""Skytower Brachiosaurus - gentle giant with a tall neck; carries two riders."""
from lib import *
from specs.eggsa_kit import *

bones = quad(22, 18, 36, 24, 8, 8, skin="hide", leg_skin="leg", foot_skin="leg", toes=4, fz=1, bz=1)
body = get(bones, "body")
body["cubes"].append(cube([-7, 42, -14], [14, 3, 20], "back"))
prev = "body"; y = 36; z = -14
for i in range(4):
    w = 8 - i; h = 14
    nm = f"neck{i}"
    bones.append(bone(nm, prev, [0, y, z], [cube([-w / 2, y, z - 3], [w, h + 2, 8 - i], "hide")]))
    prev = nm; y += h; z -= 3
hc = [cube([-3, y - 1, z - 8], [6, 6, 9], "hide"), cube([-2, y - 1, z - 11], [4, 4, 4], "hide"), cube([-1.5, y + 5, z - 6], [3, 1, 4], "nostril")]
side_eyes(hc, 3, y + 2, z - 5, 2, "eye")
pair(hc, cube([1, y + 3, z - 11], [1, 1, 1], "dark"))
bones.append(bone("head", prev, [0, y + 2, z - 3], hc))
tail(bones, "body", 30, 18, 6, 12, 12, 8, taper=0.8, skin="hide", fall=0.8)
hide = pelt("#7d9aa8", "#5f7d8c", belly="#d8e0d4", belly_y=26, seed=51, patch=8.0, spots=("#5a7482", 4.0, 0.66))
skins = {"default": hide, "hide": hide, "leg": pelt("#6a8492", "#506a78", seed=52), "back": pelt("#4f6a58", "#3a5241", seed=53),
         "claw": claw_paint(), "eye": eye_color("#e7d26a"), "dark": flat("#1d2a30"), "nostril": flat("#2b3b44")}
an = quad_anims(tail_bones=[f"tail{i}" for i in range(6)], amp=18, freq=27, bob_amp=0.3)
an["idle"]["bones"].update(merge(*[sway(f"neck{i}", 3, 40, 0, i * 0.6) for i in range(4)]))
SPEC = finish("brachiosaurus", "Skytower Brachiosaurus", ("#7d9aa8", "#4f6a58"), bones, skins, an, STD_PLAY, {
    "role": "mount", "health": 110, "speed": 0.2, "damage": 10, "box": [2.6, 3.0], "knockback_resist": 0.9,
    "family": ["dinosaur"], "ride": {"seats": [[0, 2.85, -0.4], [0, 2.85, 0.6]], "jump": 0.3},
    "loot": [("minecraft:leather", 2, 5), ("minecraft:bone", 2, 5)], "sound": ("horse", [0.4, 0.5]),
    "spawn": {"biomes": ["jungle", "savanna"], "weight": 3, "herd": [1, 2]}})
