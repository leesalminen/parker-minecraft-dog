"""Pebble Trilobite - tiny six-legged shell crawler (about a third of a block)."""
from lib import *
from specs.eggsa_kit import *

body_c = [cube([-4, 2, -6], [8, 4, 4], "cephalon"), cube([-3, 5, -5], [6, 2, 2], "glabella")]
seg = [(8, 0), (8, 2), (7, 4), (6, 6), (5, 8), (4, 10)]
for i, (w, z) in enumerate(seg):
    body_c.append(cube([-w / 2, 2, -2 + z], [w, 3, 2], "seg"))
    body_c.append(cube([-w / 2 + 1, 5, -2 + z], [w - 2, 1, 2], "seg_hi"))
body_c.append(cube([-2, 2, 10], [4, 3, 3], "pyg"))
bones = [bone("body", None, [0, 3, 0], body_c)]
hd = []
pair(hd, cube([2, 6, -6], [1, 2, 2], "eye"))
bones.append(bone("head", "body", [0, 5, -5], hd))
pair(bones[-1]["cubes"], cube([1, 4, -8], [1, 1, 3], "antenna"))
legs = []
for side, sx in (("l", 1), ("r", -1)):
    for i in range(3):
        z = -3 + i * 4
        nm = f"leg_{side}{i}"
        bones.append(bone(nm, "body", [sx * 4, 2, z], [cube([sx * 4 - (1 if sx < 0 else 0) + (0 if sx < 0 else 0) + (0.0), 0, z - 0.5], [1, 2, 1], "leg"),
                                                        cube([sx * 5 - (1 if sx < 0 else 0), 0, z - 0.5], [1, 1, 1], "leg")]))
order = ["leg_l0", "leg_r0", "leg_r1", "leg_l1", "leg_l2", "leg_r2"]
an = {"walk": anim(merge(hex_walk(order, 30, 90), {"body": {"rotation": ["0", f"math.sin(query.modified_distance_moved * 90) * 4 * query.modified_move_speed", "0"]}})),
      "idle": anim(merge(sway("head", 5, 50, 1), sway("antenna" if False else "head", 3, 90, 0)))}
sh = shell("#6d6a7a", "#3b3a48", 2)
skins = {"default": sh, "cephalon": pelt("#7b7889", "#5a5768", seed=131, cells=1.5), "glabella": plates("#9a96ab", 0.7),
         "seg": pelt("#6d6a7a", "#4d4a5b", seed=132, stripes=("#3b3a48", 2.5, 0.4, "z")), "seg_hi": plates("#8a8699", 0.7),
         "pyg": pelt("#5a5768", "#43404f", seed=133), "eye": eye_color("#e8d468"), "antenna": solid("#3b3a48"), "leg": solid("#4a4657")}
SPEC = finish("trilobite", "Pebble Trilobite", ("#6d6a7a", "#e8d468"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 4, "speed": 0.16, "box": [0.4, 0.3], "family": ["trilobite"],
    "loot": [("minecraft:flint", 0, 1), ("minecraft:clay_ball", 0, 2)], "sound": ("silverfish", [1.6, 1.9]),
    "spawn": {"biomes": ["swamp", "beach", "river"], "weight": 12, "herd": [3, 6]}})
