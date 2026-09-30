"""Glimmer Archaeopteryx - tiny tameable flier, part lizard, part bird."""
from lib import *
from specs.eggsa_kit import *

bones = [bone("body", None, [0, 6, 0], [cube([-2.5, 4, -4], [5, 5, 8], "feather"), cube([-2, 3, -3], [4, 1, 6], "belly")])]
bones.append(bone("neck", "body", [0, 8, -4], [cube([-1.5, 7, -6], [3, 4, 3], "feather")]))
hc = [cube([-2.5, 8, -11], [5, 5, 6], "feather"), cube([-1.5, 9, -14], [3, 2, 3], "snout"), cube([-1.5, 8, -14], [3, 1, 3], "tooth_row"),
      cube([-1, 13, -8], [2, 2, 3], "crest")]
eyes(hc, 1.6, 10, -11, 2, "eye_dark")
bones.append(bone("head", "neck", [0, 9, -6], hc))
for sx, tag in ((1, "l"), (-1, "r")):
    def wx(x, w): return x if sx > 0 else -x - w
    bones.append(bone(f"wing_{tag}", "body", [sx * 2.5, 8, -1], [cube([wx(2.5, 7), 7.5, -3], [7, 1, 7], "wing"), cube([wx(2.5, 7), 7, -3], [7, 1, 3], "wing_d")]))
    bones.append(bone(f"wing_{tag}2", f"wing_{tag}", [sx * 9.5, 8, -1],
                      [cube([wx(9.5, 8), 7.5, -3], [8, 1, 9], "wing_tip"), cube([wx(17.5, 1), 7, -4], [1, 1, 2], "claw")]))
    bones.append(bone(f"leg_{tag}", "body", [sx * 1.2, 4, 1], [cube([sx * 1.2 - 0.5, 0, 0.5], [1, 5, 1], "leg"), cube([sx * 1.2 - 1, 0, -1.5], [2, 1, 3], "claw")]))
bones.append(bone("tail0", "body", [0, 6, 4], [cube([-1, 5, 4], [2, 2, 8], "feather")]))
bones.append(bone("tail1", "tail0", [0, 6, 12], [cube([-4, 5.5, 12], [8, 1, 8], "wing_tip", rot=[0, 0, 0])]))
skins = {"default": pelt("#2c4c7a", "#1d3557", belly="#d8ecff", belly_y=5, seed=191, patch=1.6),
         "feather": pelt("#2c4c7a", "#1d3557", belly="#d8ecff", belly_y=5, seed=191, patch=1.6), "belly": flat("#d8ecff"),
         "wing": pelt("#3b6aa8", "#2c4c7a", seed=192, stripes=("#f0a030", 1.4, 0.6, "z")), "wing_d": pelt("#1d3557", "#14263f", seed=193),
         "wing_tip": pelt("#3b6aa8", "#e88a2a", seed=194, stripes=("#f2c14a", 1.8, 0.5, "z")), "snout": pelt("#f2c14a", "#d19a2a", seed=195),
         "tooth_row": tooth, "crest": pelt("#e88a2a", "#c9691a", seed=196), "leg": solid("#c9a24a"), "claw": claw_paint(),
         "eye_dark": eye_dark}
def fl(s):
    g = 1 if s == "l" else -1
    return {f"wing_{s}": {"rotation": ["0", "0", f"math.sin(query.life_time * 420) * 38 * {g}"]},
            f"wing_{s}2": {"rotation": ["0", "0", f"math.sin(query.life_time * 420 - 40) * 30 * {g}"]}}
an = {"idle": anim(merge(fl("l"), fl("r"), bob("body", 0.5, 160), sway("tail1", 6, 90, 0),
                          {"head": {"rotation": ["math.sin(query.life_time * 90) * 5", "math.sin(query.life_time * 55) * 12", "0"]}})),
      "walk": anim(swing({"leg_l": 0, "leg_r": 180}, 35, 0, 60))}
SPEC = finish("archaeopteryx", "Glimmer Archaeopteryx", ("#2c4c7a", "#f2c14a"), bones, skins, an, ["idle", {"walk": "query.modified_move_speed > 0.02"}], {
    "role": "companion", "health": 10, "speed": 0.26, "fly": True, "fly_speed": 0.22, "box": [0.5, 0.5], "family": ["archaeopteryx"],
    "tame_items": ["minecraft:wheat_seeds", "minecraft:beetroot_seeds", "minecraft:melon_seeds"],
    "loot": [("minecraft:feather", 1, 2)], "sound": ("parrot", [1.5, 1.9]),
    "spawn": {"biomes": ["forest", "jungle"], "weight": 8, "herd": [1, 3]}})
