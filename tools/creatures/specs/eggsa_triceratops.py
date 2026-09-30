"""Horn-Brow Triceratops - three-horned frilled rideable herbivore."""
from lib import *
from specs.eggsa_kit import *

bones = quad(16, 15, 26, 9, 5, 5, skin="hide", leg_skin="leg", foot_skin="leg", toes=3, fz=1, bz=1)
body = get(bones, "body")
body["cubes"].append(cube([-6, 20, -14], [12, 6, 8], "hide"))   # shoulder hump
hc = [cube([-4.5, 11, -25], [9, 9, 12], "hide"), cube([-2.5, 10, -29], [5, 5, 5], "beak"),
      cube([-3, 9, -27], [6, 1, 8], "belly")]
pair(hc, cube([4, 12, -26], [1, 3, 3], "cheek"))
# frill: big plate behind the skull with a knobbly rim
hc.append(cube([-9, 13, -15], [18, 15, 3], "frill", rot=[-12, 0, 0], pivot=[0, 14, -14]))
for i in range(6):
    x = -9 + i * 3.2
    hc.append(cube([x, 28.5 - abs(i - 2.5) * 0.6, -15.5], [3, 3, 2], "frill_rim", rot=[-12, 0, 0], pivot=[0, 14, -14]))
side_eyes(hc, 4.5, 15, -22, 2, "eye")
pair(hc, cube([2, 19, -24], [2, 8, 2], "horn", rot=[-32, 0, 0], pivot=[3, 19, -24]))         # brow horns
hc.append(cube([-1, 16, -29], [2, 6, 2], "horn", rot=[-18, 0, 0], pivot=[0, 16, -28]))      # nose horn
bones.append(bone("head", "body", [0, 16, -13], hc))
tail(bones, "body", 13, 13, 3, 7, 7, 7, taper=0.72, skin="hide", tip_skin="hide")

hide = pelt("#7e8fa3", "#5e6f86", belly="#d2cbb0", belly_y=12, seed=21, spots=("#4d5a70", 3.0, 0.62))
skins = {"default": hide, "hide": hide, "leg": pelt("#66788f", "#4d5c70", seed=22), "beak": pelt("#a89466", "#8a774f", seed=4),
         "belly": flat("#d2cbb0"), "cheek": solid("#66788f"),
         "frill": pelt("#c8583a", "#8f3a2a", seed=25, stripes=("#f0b24a", 0.55, 0.5, "x")),
         "frill_rim": plates("#f0d58a", 0.7), "horn": solid("#f2ead2", 0.1),
         "claw": claw_paint(), "eye": eye_color("#e8c14a")}
anims = quad_anims(tail_bones=["tail0", "tail1", "tail2"], amp=28, freq=38, extra_idle=sway("head", 3, 55, 2))
SPEC = finish("triceratops", "Horn-Brow Triceratops", ("#7e8fa3", "#c8583a"), bones, skins, anims, STD_PLAY, {
    "role": "mount", "health": 70, "speed": 0.26, "damage": 8, "box": [1.3, 1.6], "knockback_resist": 0.5,
    "family": ["dinosaur"], "ride": {"seats": [[0, 1.55, 0.1]], "jump": 0.5},
    "loot": [("minecraft:leather", 1, 3), ("minecraft:bone", 1, 3)], "sound": ("ravager", [0.8, 1.0]),
    "spawn": {"biomes": ["plains", "savanna"], "weight": 6, "herd": [1, 3]}})
