"""Domeshell Glyptodon - a walking hill of armour with a tiny friendly face."""
from lib import *
from specs.eggsa_kit import *

bones = quad(16, 8, 22, 6, 5, 5, skin="under", leg_skin="leg", foot_skin="leg", toes=3, fz=1.5, bz=1.5)
body = get(bones, "body")
body["cubes"] += [cube([-11, 11, -13], [22, 8, 26], "shell"), cube([-9, 19, -11], [18, 4, 22], "shell"),
                  cube([-6, 23, -8], [12, 2, 16], "shell_hi"), cube([-10, 9, -12], [20, 3, 24], "rim")]
for z in range(-10, 12, 5):
    pair(body["cubes"], cube([10.5, 12, z], [2, 3, 3], "rim"))
hc = [cube([-3.5, 7, -19], [7, 7, 7], "skin"), cube([-2.5, 7, -22], [5, 4, 3], "skin"), cube([-2.5, 13, -18], [5, 1, 5], "shell_hi")]
eyes(hc, 2, 10, -19, 2, "eye")
pair(hc, cube([1, 12, -18], [2, 2, 1], "skin"))
bones.append(bone("head", "body", [0, 10, -12], hc))
tail(bones, "body", 8, 12, 4, 8, 7, 6, taper=0.85, skin="shell", tip_skin="club")
t = get(bones, "tail3")
t["cubes"].append(cube([-5, 5, 19 + 6], [10, 8, 8], "club"))
for z in (0, 4):
    pair(t["cubes"], cube([4, 8, 25 + z], [2, 2, 2], "rim"))
shellp = shell("#8a6d4a", "#4e3d28", 4)
skins = {"default": pelt("#b59a72", "#8f7752", seed=81), "shell": shellp, "shell_hi": shell("#a58455", "#5d4a30", 3),
         "rim": plates("#c7ad7c", 0.62), "under": pelt("#b59a72", "#8f7752", seed=81), "skin": pelt("#c4a87c", "#9a8158", seed=82),
         "leg": pelt("#9a8158", "#7a6440", seed=83), "club": shell("#6b5a40", "#2e2618", 3),
         "claw": claw_paint(), "eye": eye_dark}
an = quad_anims(tail_bones=["tail0", "tail1", "tail2", "tail3"], amp=22, freq=36)
SPEC = finish("glyptodon", "Domeshell Glyptodon", ("#8a6d4a", "#c7ad7c"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 40, "speed": 0.15, "box": [1.5, 1.7], "knockback_resist": 0.6, "family": ["glyptodon"],
    "loot": [("minecraft:leather", 1, 2), ("minecraft:scute", 0, 2)], "sound": ("turtle", [0.6, 0.8]),
    "spawn": {"biomes": ["plains", "savanna", "mesa"], "weight": 8, "herd": [1, 2]}})
