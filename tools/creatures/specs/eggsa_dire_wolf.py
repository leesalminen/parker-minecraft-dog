"""Ashmane Dire Wolf - big tameable wolf with a shaggy mane."""
from lib import *
from specs.eggsa_kit import *

bones = quad(9, 10, 18, 11, 4, 4, skin="fur", leg_skin="fur_d", foot_skin="paw", fz=0.5, bz=0.5)
body = get(bones, "body")
body["cubes"] += [cube([-5, 12, -12], [10, 12, 8], "mane"), cube([-4.5, 21, -9], [9, 3, 14], "saddle"), cube([-3.5, 9, -13], [7, 5, 6], "chest")]
hc = [cube([-4, 17, -17], [8, 8, 8], "fur"), cube([-2.5, 17, -22], [5, 4, 5], "fur"), cube([-2, 20, -22.5], [4, 1.5, 1], "nose"),
      cube([-2, 16, -21], [4, 1, 4], "chest")]
pair(hc, cube([2, 25, -14], [2, 4, 2], "fur_d"))       # ears
pair(hc, cube([-3.9, 25, -13.8], [1, 1, 1], "chest")) if False else None
eyes(hc, 2.2, 21, -17, 2, "eye_c")
pair(hc, cube([1.5, 16, -21], [1, 2, 1], "tooth"))
bones.append(bone("head", "body", [0, 20, -6], hc))
bones.append(bone("jaw", "head", [0, 17, -18], [cube([-1.5, 14.5, -21], [3, 2, 4], "chest")]))
tail(bones, "body", 18, 9, 2, 5, 5, 5, taper=0.9, skin="fur_d", tip_skin="chest")
fur = pelt("#7a7d82", "#5a5d63", seed=101, patch=3.0, fine=0.2)
skins = {"default": fur, "fur": fur, "fur_d": pelt("#55585e", "#3c3f44", seed=102, patch=2.5), "mane": pelt("#8c8f95", "#66696f", seed=103, patch=2.0, fine=0.25),
         "saddle": pelt("#4b4e54", "#33363b", seed=104), "chest": pelt("#d8d6d0", "#b5b3ad", seed=105), "paw": solid("#3a3c40"),
         "nose": flat("#15151a"), "tooth": tooth, "eye_c": eye_color("#f2c040")}
an = quad_anims(tail_bones=["tail0", "tail1"], amp=36, freq=46)
SPEC = finish("dire_wolf", "Ashmane Dire Wolf", ("#7a7d82", "#d8d6d0"), bones, skins, an, STD_PLAY, {
    "role": "companion", "health": 30, "speed": 0.36, "box": [0.9, 1.4], "family": ["dire_wolf"],
    "tame_items": ["minecraft:bone", "minecraft:beef", "minecraft:porkchop"],
    "loot": [("minecraft:bone", 0, 2), ("minecraft:leather", 0, 1)], "sound": ("wolf", [0.7, 0.85]),
    "spawn": {"biomes": ["taiga", "forest", "frozen"], "weight": 6, "herd": [2, 4]}})
