"""Eggshell Hatchling - baby dino wearing half its egg. The kid-friendly starter companion."""
from lib import *
from specs.eggsa_kit import *

bones = quad(6, 6, 9, 4, 3, 3, skin="hide", leg_skin="leg", foot_skin="leg", fz=0.5, bz=0.5, inset=0)
body = get(bones, "body")
body["cubes"].append(cube([-2.5, 10, -3], [5, 1, 8], "spot"))
hc = [cube([-4.5, 6, -14], [9, 8, 8], "hide"), cube([-3, 6, -17], [6, 4, 3], "hide"), cube([-3, 5, -16], [6, 1, 3], "belly")]
eyes(hc, 2.6, 9, -14, 3, "eye_dark")
pair(hc, cube([3.6, 7, -14], [2, 1, 1], "blush"))
pair(hc, cube([1, 9, -17.5], [1, 1, 1], "dark"))
# eggshell cap with zig-zag edge
hc.append(cube([-5, 12, -15], [10, 4, 10], "shell"))
for i, x in enumerate(range(-5, 5, 2)):
    hc.append(cube([x, 14 + (i % 2) * 0, -15.5], [2, 3 + (i % 2) * 2, 1], "shell"))
    hc.append(cube([x, 14, -5.5], [2, 3 + ((i + 1) % 2) * 2, 1], "shell"))
hc.append(cube([-3, 16, -13], [6, 1, 6], "shell_hi"))
bones.append(bone("head", "body", [0, 8, -8], hc))
tail(bones, "body", 3, 5, 3, 4, 4, 3, taper=0.8, skin="hide")
pair(get(bones, "body")["cubes"], cube([2.5, 7, 0], [1, 4, 1], "spot", rot=[0, 0, 20]))
hide = pelt("#8fd4a8", "#6ab88a", belly="#fff3c4", belly_y=6, seed=261, spots=("#5aa878", 1.5, 0.68))
skins = {"default": hide, "hide": hide, "leg": pelt("#6ab88a", "#4e9a6e", seed=262), "spot": solid("#ffb04a"), "belly": flat("#fff3c4"),
         "shell": pelt("#fbf4e2", "#e8dcc0", seed=263, spots=("#b8a078", 1.2, 0.72)), "shell_hi": flat("#fffaf0"), "eye_dark": eye_dark,
         "blush": flat("#ff9aa8"), "dark": flat("#2a3a30")}
an = quad_anims(tail_bones=["tail0", "tail1", "tail2"], amp=36, freq=62, bob_amp=0.3, extra_idle=sway("head", 3, 90, 2))
SPEC = finish("dino_hatchling", "Eggshell Hatchling", ("#fbf4e2", "#8fd4a8"), bones, skins, an, STD_PLAY, {
    "role": "companion", "health": 12, "speed": 0.3, "box": [0.5, 0.7], "family": ["dinosaur"],
    "tame_items": ["minecraft:egg", "minecraft:wheat_seeds", "minecraft:pumpkin_seeds"],
    "loot": [("minecraft:egg", 0, 1)], "sound": ("parrot", [1.7, 2.0]),
    "spawn": {"biomes": ["forest", "plains", "jungle"], "weight": 10, "herd": [1, 2]}})
