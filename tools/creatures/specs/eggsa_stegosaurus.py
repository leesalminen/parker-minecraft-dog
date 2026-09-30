"""Plated Stegosaurus - big, calm, plates along the back and a spiked tail."""
from lib import *
from specs.eggsa_kit import *

bones = quad(16, 14, 30, 8, 5, 5, skin="hide", leg_skin="leg", foot_skin="leg", toes=3, toe_skin="claw", fz=1.5, bz=1.5)
body = get(bones, "body")
body["cubes"].append(cube([-7.5, 22, 4], [15, 3, 12], "hide"))            # raised rump
body["cubes"].append(cube([-8, 8, 4], [16, 17, 12], "hide"))
# back plates: alternating pairs, biggest over the hips
for i, (z, h) in enumerate(zip(range(-12, 15, 4), [5, 7, 9, 11, 11, 9, 6])):
    top = 22 if z < 4 else 25
    zz = z + (1 if i % 2 else 0)
    body["cubes"].append(cube([-1, top - 1, zz], [2, h + 1, 5], "plate"))
    body["cubes"].append(cube([-1, top + h, zz + 1], [2, 2, 3], "plate_tip"))

bones.append(bone("neck", "body", [0, 14, -14], [cube([-3.5, 11, -21], [7, 9, 9], "hide")]))
hc = [cube([-3, 8, -28], [6, 6, 8], "hide"), cube([-2, 8, -33], [4, 4, 5], "beak"),
      cube([-2.5, 7, -27], [5, 1, 6], "belly")]
side_eyes(hc, 3, 11, -25, 2, "eye")
pair(hc, cube([1, 12, -32], [1, 1, 1], "dark"))
bones.append(bone("head", "neck", [0, 13, -21], hc))

last = tail(bones, "body", 11, 15, 4, 9, 9, 8, taper=0.78, rise=1.0, skin="hide", tip_skin="hide")
for nm, dz in (("tail2", 1), ("tail3", 1)):
    b = get(bones, nm); c = b["cubes"][0]
    x0, y0, z0 = c["o"]; w, h, d = c["s"]
    sp = cube([w / 2 - 0.5 + 0.5, y0 + h - 1, z0 + dz], [1, 7, 2], "spike", rot=[0, 0, 40], pivot=[w / 2, y0 + h, z0 + dz])
    pair(b["cubes"], sp)
    sp2 = cube([-0.5, y0 + h - 1, z0 + dz + 3], [1, 6, 2], "spike", rot=[-35, 0, 0], pivot=[0, y0 + h, z0 + dz + 3])
    b["cubes"].append(sp2)

hide = pelt("#6f8a4e", "#55703c", belly="#c9c48f", belly_y=11, seed=3, stripes=("#3f5a2c", 0.9, 0.55, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#5c7642", "#485f33", seed=8),
         "plate": plates("#d9832b", 0.7, "#f3b25a"), "plate_tip": plates("#e9a04a", 0.75),
         "spike": solid("#efe6c9", 0.08), "beak": pelt("#9a8a5a", "#7c6d43", seed=4), "belly": flat("#c9c48f"),
         "claw": claw_paint(), "eye": eye_color("#f3d34a"), "dark": flat("#26301c")}
anims = quad_anims(tail_bones=["tail0", "tail1", "tail2", "tail3"], amp=22, freq=34, neck="neck")
anims["attack"] = anim({"tail0": {"rotation": ["0", "math.sin(variable.attack_time * 180) * 40", "0"]},
                         "tail1": {"rotation": ["0", "math.sin(variable.attack_time * 180) * 40", "0"]}}, loop=False)
SPEC = finish("stegosaurus", "Plated Stegosaurus", ("#6f8a4e", "#d9832b"), bones, skins, anims, STD_PLAY_ATK, {
    "role": "neutral", "health": 60, "speed": 0.2, "damage": 7, "box": [1.3, 1.9], "knockback_resist": 0.4,
    "family": ["dinosaur"], "loot": [("minecraft:leather", 1, 3), ("minecraft:bone", 1, 3)],
    "sound": ("ravager", [0.7, 0.9]), "xp": 5, "spawn": {"biomes": ["plains", "savanna"], "weight": 6, "herd": [1, 2]}})
