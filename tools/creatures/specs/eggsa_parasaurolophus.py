"""Trumpet Parasaurolophus - gentle duckbill with a long swept-back crest."""
from lib import *
from specs.eggsa_kit import *

bones = quad(11, 12, 22, 12, 4, 4, skin="hide", leg_skin="leg", foot_skin="leg", toes=3, fz=1, bz=1, front_lw=3, front_ld=3)
body = get(bones, "body")
for z in range(-8, 10, 4):
    body["cubes"].append(cube([-1, 24, z], [2, 2, 3], "ridge"))
bones.append(bone("neck", "body", [0, 20, -10], [cube([-3, 19, -16], [6, 11, 8], "hide", rot=[12, 0, 0], pivot=[0, 20, -11])]))
hc = [cube([-3.5, 27, -25], [7, 6, 9], "hide"), cube([-3, 27, -30], [6, 4, 6], "bill"), cube([-3, 26, -29], [6, 1, 6], "bill_lo")]
side_eyes(hc, 3.5, 30, -22, 2, "eye")
pair(hc, cube([1, 29, -30], [1, 1, 1], "dark"))
crest = [cube([-1.5, 32, -21], [3, 4, 5], "crest", rot=[-20, 0, 0]), cube([-1.5, 33, -17], [3, 3, 7], "crest", rot=[-10, 0, 0]),
         cube([-1.5, 33, -11], [3, 3, 7], "crest", rot=[12, 0, 0]), cube([-1.5, 31, -5], [3, 3, 6], "crest", rot=[30, 0, 0]),
         cube([-1.5, 28, -1], [3, 3, 5], "crest", rot=[45, 0, 0])]
bones.append(bone("head", "neck", [0, 28, -18], hc))
bones.append(bone("crest", "head", [0, 32, -20], crest))
tail(bones, "body", 14, 11, 4, 6, 7, 8, taper=0.8, skin="hide", tip_skin="ridge")
hide = pelt("#4d9b8a", "#347565", belly="#e6dfb4", belly_y=15, seed=71, stripes=("#1f5a4e", 0.9, 0.6, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#3c8071", "#2b6055", seed=72), "ridge": solid("#e08a3a"),
         "bill": pelt("#d9c27a", "#b59f58", seed=73), "bill_lo": flat("#c1aa64"),
         "crest": pelt("#e5683a", "#b44a26", seed=74, stripes=("#f6c65a", 0.8, 0.55, "z")),
         "claw": claw_paint(), "eye": eye_color("#f0d060"), "dark": flat("#2a3a30")}
an = quad_anims(tail_bones=["tail0", "tail1", "tail2", "tail3"], amp=26, freq=44, extra_idle=sway("crest", 3, 60, 0))
SPEC = finish("parasaurolophus", "Trumpet Parasaurolophus", ("#4d9b8a", "#e5683a"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 30, "speed": 0.28, "box": [0.9, 2.0], "family": ["dinosaur"],
    "loot": [("minecraft:leather", 0, 2), ("minecraft:bone", 0, 2)], "sound": ("horse", [1.3, 1.5]),
    "spawn": {"biomes": ["plains", "forest", "jungle"], "weight": 10, "herd": [3, 5]}})
