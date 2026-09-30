"""Fuzzy Mastodon Calf - tameable baby mastodon with floppy ears and a tiny trunk."""
from lib import *
from specs.eggsa_kit import *

bones = quad(11, 10, 14, 6, 4, 4, skin="fur", leg_skin="fur_d", foot_skin="foot", fz=0.5, bz=0.5)
body = get(bones, "body")
for i in range(5):
    body["cubes"].append(cube([-5.5 + i * 2.2, 5.5, -6 + (i % 2) * 8], [2, 3, 5], "fringe"))
body["cubes"].append(cube([-4, 16, -7], [8, 2, 14], "fur_d"))
hc = [cube([-5, 7, -14], [10, 9, 9], "fur"), cube([-4, 15, -13], [8, 3, 7], "fur_d")]
eyes(hc, 3, 11, -14, 2, "eye_dark")
pair(hc, cube([3.5, 6, -13], [2, 6, 2], "tusk", rot=[-12, 0, 0]))
bones.append(bone("head", "body", [0, 13, -8], hc))
pair_e = []
pair(pair_e, cube([5, 6, -11], [1, 8, 6], "ear"))
bones.append(bone("ears", "head", [0, 14, -11], pair_e))
prev = "head"
for i in range(3):
    w = 4 - (i > 1)
    bones.append(bone(f"trunk{i}", prev, [0, 10 - i * 2.5, -16 - i * 0], [cube([-w / 2, 9 - i * 3, -16], [w, 4, 2 + 0], "trunk")]))
    prev = f"trunk{i}"
tail(bones, "body", 9, 7, 2, 2, 5, 2, taper=1.0, skin="fur_d", tip_skin="fringe")
fur = pelt("#8a5a3a", "#6b4128", seed=91, patch=2.5, fine=0.22)
skins = {"default": fur, "fur": fur, "fur_d": pelt("#6b4128", "#523020", seed=92, patch=2.0), "fringe": pelt("#a06e46", "#7d5234", seed=93),
         "foot": solid("#4e3222"), "tusk": solid("#f4ecd0", 0.06), "ear": pelt("#a06a4a", "#c98a7a", seed=94),
         "trunk": pelt("#7d5234", "#5e3c26", seed=95), "eye_dark": eye_dark, "eye": eye_dark}
an = quad_anims(tail_bones=["tail0", "tail1"], amp=30, freq=52, ears=["ears"])
an["idle"]["bones"].update(merge(*[sway(f"trunk{i}", 8, 60, 0, i * 0.8) for i in range(3)]))
an["walk"]["bones"].update(merge(*[swing({f"trunk{i}": 0}, 8, 0, 52) for i in range(3)]))
SPEC = finish("mastodon", "Fuzzy Mastodon Calf", ("#8a5a3a", "#f4ecd0"), bones, skins, an, STD_PLAY, {
    "role": "companion", "health": 24, "speed": 0.3, "box": [0.7, 1.0], "family": ["mastodon"],
    "tame_items": ["minecraft:wheat", "minecraft:apple", "minecraft:sweet_berries"],
    "loot": [("minecraft:leather", 0, 1)], "sound": ("polarbear", [1.5, 1.8]),
    "spawn": {"biomes": ["taiga", "forest", "plains"], "weight": 6, "herd": [2, 3]}})
