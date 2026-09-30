"""Colossus Quetzalcoatlus - giant stork-necked pterosaur; big rideable flier."""
from lib import *
from specs.eggsa_kit import *

body_c = [cube([-6, 22, -10], [12, 11, 22], "hide"), cube([-5, 21, -9], [10, 1, 20], "belly"), cube([-4, 33, -6], [8, 2, 14], "hide")]
bones = [bone("body", None, [0, 27, 0], body_c)]
prev = "body"; y = 30; z = -10
for i in range(3):
    nm = f"neck{i}"
    bones.append(bone(nm, prev, [0, y, z], [cube([-2.5, y - 1, z - 8], [5, 6, 9], "hide")]))
    prev = nm; z -= 7; y += 2
hc = [cube([-3.5, y - 1, z - 8], [7, 7, 10], "hide"), cube([-2, y, z - 32], [4, 4, 24], "beak"), cube([-1.5, y - 1, z - 30], [3, 1, 22], "beak_lo"),
      cube([-1.5, y + 6, z - 4], [3, 4, 8], "crest"), cube([-1.5, y + 8, z + 3], [3, 4, 8], "crest")]
side_eyes(hc, 3.5, y + 3, z - 4, 2, "eye")
pair(hc, cube([1.5, y + 2, z - 30], [1, 1, 1], "dark"))
bones.append(bone("head", prev, [0, y + 2, z + 2], hc))
for sx, tag in ((1, "l"), (-1, "r")):
    def wx(x, w): return x if sx > 0 else -x - w
    bones.append(bone(f"wing_{tag}", "body", [sx * 6, 33, -4], [cube([wx(5, 16), 32, -8], [16, 3, 7], "arm"), cube([wx(5, 16), 31.5, -2], [16, 1, 14], "membrane")]))
    bones.append(bone(f"wing_{tag}2", f"wing_{tag}", [sx * 21, 33, -4],
                      [cube([wx(21, 24), 32.5, -9], [24, 2, 3], "arm"), cube([wx(21, 24), 32, -6], [24, 1, 20], "membrane")]))
    bones.append(bone(f"wing_{tag}3", f"wing_{tag}2", [sx * 45, 33, -4],
                      [cube([wx(45, 18), 32.5, -8], [18, 2, 2], "arm"), cube([wx(45, 18), 32, -6], [18, 1, 14], "membrane_tip")]))
    xc = sx * 4
    bones.append(bone(f"leg_{tag}", "body", [xc, 23, 5], [cube([xc - 1.5, 0, 4], [3, 24, 3], "leg"), cube([xc - 2.5, 0, 0], [5, 2, 8], "leg"), cube([xc - 1.5, 0, -2], [1, 2, 2], "claw")]))
    bones.append(bone(f"foreleg_{tag}", "body", [xc, 23, -6], [cube([xc - 1.5, 0, -8], [3, 24, 3], "leg"), cube([xc - 2.5, 0, -10], [5, 2, 6], "leg")]))
tail(bones, "body", 24, 12, 2, 4, 5, 5, taper=0.85, skin="hide")
hide = pelt("#8a8f9a", "#666c78", belly="#e6e0d0", belly_y=23, seed=181, stripes=("#4a4f5c", 0.9, 0.7, "z"))
skins = {"default": hide, "hide": hide, "belly": flat("#e6e0d0"), "beak": pelt("#e6c86a", "#c0a040", seed=182), "beak_lo": flat("#b09030"),
         "crest": pelt("#d2483a", "#a02c22", seed=183), "arm": pelt("#5d6370", "#454a56", seed=184),
         "membrane": pelt("#a8aebb", "#8a90a0", seed=185, stripes=("#666c78", 1.1, 0.6, "x")), "membrane_tip": pelt("#9096a5", "#767c8c", seed=186),
         "leg": solid("#5d6370"), "claw": claw_paint(), "eye": eye_color("#f6c84a"), "dark": flat("#1c2028")}
def fl(s):
    g = 1 if s == "l" else -1
    return {f"wing_{s}": {"rotation": ["0", "0", f"math.sin(query.life_time * 200) * 30 * {g}"]},
            f"wing_{s}2": {"rotation": ["0", "0", f"math.sin(query.life_time * 200 - 40) * 24 * {g}"]},
            f"wing_{s}3": {"rotation": ["0", "0", f"math.sin(query.life_time * 200 - 80) * 18 * {g}"]}}
an = {"idle": anim(merge(fl("l"), fl("r"), bob("body", 0.6, 100), sway("neck1", 4, 40, 0), sway("tail0", 6, 50, 1),
                          {"head": {"rotation": ["math.sin(query.life_time * 60) * 4", "math.sin(query.life_time * 33) * 8", "0"]}})),
      "walk": anim(merge(quad_walk("foreleg_l", "foreleg_r", "leg_l", "leg_r", 20, 30)))}
SPEC = finish("quetzalcoatlus", "Colossus Quetzalcoatlus", ("#8a8f9a", "#d2483a"), bones, skins, an, ["idle", {"walk": "query.modified_move_speed > 0.02"}], {
    "role": "mount", "health": 60, "speed": 0.2, "fly": True, "fly_speed": 0.34, "damage": 8, "box": [1.6, 2.3],
    "ride": {"seats": [[0, 2.15, 0.2]]}, "family": ["pterosaur"], "knockback_resist": 0.3,
    "loot": [("minecraft:feather", 2, 4), ("minecraft:bone", 1, 3)], "sound": ("dragon", [1.4, 1.6]),
    "spawn": {"biomes": ["mesa", "savanna", "mountain"], "weight": 2, "herd": [1, 1]}})
