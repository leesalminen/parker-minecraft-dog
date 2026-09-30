"""Crownhorn Megaloceros - giant Irish-elk mount with enormous palmate antlers."""
from lib import *
from specs.eggsa_kit import *

bones = quad(12, 13, 26, 22, 3, 3, skin="hide", leg_skin="leg", foot_skin="hoof", fz=1, bz=1, inset=0.5, front_lw=3, front_ld=3)
body = get(bones, "body")
body["cubes"] += [cube([-6.5, 24, -13], [13, 4, 10], "mane"), cube([-5, 22, 11], [10, 8, 3], "rump")]
bones.append(bone("neck", "body", [0, 32, -12], [cube([-3.5, 30, -18], [7, 14, 8], "mane", rot=[28, 0, 0], pivot=[0, 32, -12])]))
hc = [cube([-3, 40, -28], [6, 7, 11], "hide"), cube([-2, 39, -33], [4, 5, 6], "muzzle"), cube([-2, 42, -33.5], [4, 2, 1], "nose")]
side_eyes(hc, 3, 44, -24, 2, "eye")
pair(hc, cube([2.5, 46, -19], [3, 4, 2], "ear", rot=[0, 0, -35]))
bones.append(bone("head", "neck", [0, 44, -18], hc))
ac = []
for sx in (1, -1):
    def wx(x, w): return x if sx > 0 else -x - w
    ac.append(cube([wx(2, 3), 47, -22], [3, 4, 3], "antler"))
    ac.append(cube([wx(3, 3), 50, -22], [3, 8, 3], "antler", rot=[0, 0, sx * 22], pivot=[sx * 4.5, 50, -20.5]))
    ac.append(cube([wx(5, 15), 57, -24], [15, 2, 14], "palm"))                # the big palm
    for i in range(5):
        ac.append(cube([wx(17, 4), 59, -24 + i * 3], [4, 2, 2], "antler"))
    ac.append(cube([wx(6, 3), 59, -27], [3, 6, 3], "antler"))
    ac.append(cube([wx(11, 3), 59, -26], [3, 8, 2], "antler"))
bones.append(bone("antlers", "head", [0, 47, -21], ac))
tail(bones, "body", 26, 13, 1, 3, 4, 3, skin="rump")
hide = pelt("#8a5a36", "#6b4224", belly="#e8d8b8", belly_y=25, seed=221, patch=3.0, fine=0.18)
skins = {"default": hide, "hide": hide, "mane": pelt("#5c3a20", "#412815", seed=222, patch=1.8, fine=0.28), "leg": pelt("#6b4224", "#4f2f18", seed=223),
         "hoof": solid("#241a14"), "rump": pelt("#f0e2c4", "#d6c5a2", seed=224), "muzzle": pelt("#c8a67a", "#a8865a", seed=225), "nose": flat("#1a1410"),
         "ear": pelt("#8a5a36", "#d8a890", seed=226), "antler": pelt("#d8c9a0", "#b3a37a", seed=227, stripes=("#8f7c52", 1.5, 0.6, "y")),
         "palm": pelt("#cdbd90", "#a8985e", seed=228, cells=2), "eye": eye_color("#2a1a10")}
an = quad_anims(tail_bones=["tail0"], amp=34, freq=36, legs=("leg_fl", "leg_fr", "leg_bl", "leg_br"), extra_idle=sway("antlers", 2, 50, 2))
SPEC = finish("megaloceros", "Crownhorn Megaloceros", ("#8a5a36", "#d8c9a0"), bones, skins, an, STD_PLAY, {
    "role": "mount", "health": 44, "speed": 0.4, "damage": 7, "box": [1.0, 2.9], "knockback_resist": 0.2, "family": ["megaloceros"],
    "ride": {"seats": [[0, 2.0, 0.0]], "jump": 1.0}, "loot": [("minecraft:leather", 1, 3), ("minecraft:bone", 0, 2)],
    "sound": ("horse", [0.7, 0.9]), "spawn": {"biomes": ["taiga", "forest", "plains"], "weight": 6, "herd": [1, 3]}})
