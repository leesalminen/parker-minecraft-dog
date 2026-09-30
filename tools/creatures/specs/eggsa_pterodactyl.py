"""Skyglider Pterodactyl - leathery-winged flying mount with a long beak and rear crest."""
from lib import *
from specs.eggsa_kit import *

body_c = [cube([-3.5, 10, -7], [7, 7, 14], "hide"), cube([-3, 9, -6], [6, 1, 12], "belly")]
bones = [bone("body", None, [0, 13, 0], body_c)]
bones.append(bone("neck", "body", [0, 15, -7], [cube([-2, 13, -11], [4, 5, 5], "hide")]))
hc = [cube([-2.5, 13, -17], [5, 5, 7], "hide"), cube([-1.5, 14, -29], [3, 3, 12], "beak"), cube([-1, 13, -28], [2, 1, 10], "beak_lo"),
      cube([-1, 18, -14], [2, 3, 6], "crest"), cube([-1, 19, -9], [2, 3, 6], "crest"), cube([-1, 18, -4], [2, 2, 4], "crest")]
side_eyes(hc, 2.5, 16, -15, 2, "eye")
pair(hc, cube([1, 15, -24], [1, 1, 1], "dark"))
bones.append(bone("head", "neck", [0, 15, -11], hc))
for sx, tag in ((1, "l"), (-1, "r")):
    x0 = 3.5 * sx
    def wx(x, w):   # x origin for a cube starting at |x| with width w on the sx side
        return x if sx > 0 else -x - w
    bones.append(bone(f"wing_{tag}", "body", [x0, 15, -3], [cube([wx(3, 10), 14, -5], [10, 2, 6], "arm"), cube([wx(3, 10), 13.5, -1], [10, 1, 8], "membrane")]))
    bones.append(bone(f"wing_{tag}2", f"wing_{tag}", [sx * 13, 15, -3],
                      [cube([wx(13, 16), 14.5, -6], [16, 2, 2], "arm"), cube([wx(13, 16), 14, -4], [16, 1, 14], "membrane"),
                       cube([wx(29, 3), 14, -6], [3, 1, 3], "arm")]))
    bones.append(bone(f"wing_{tag}3", f"wing_{tag}2", [sx * 29, 15, -3],
                      [cube([wx(29, 10), 14.5, -4], [10, 1, 12], "membrane_tip"), cube([wx(29, 12), 14.5, -6], [12, 1, 2], "arm")]))
    bones.append(bone(f"leg_{tag}", "body", [sx * 2, 11, 3], [cube([sx * 2 - 1, 5, 2], [2, 7, 2], "leg"), cube([sx * 2 - 1.5, 4, 0], [3, 1, 4], "claw")]))
tail(bones, "body", 12, 7, 2, 2, 3, 5, taper=0.9, skin="hide", tip_skin="crest")
hide = pelt("#a86f45", "#84512e", belly="#e8d7ae", belly_y=12, seed=171, stripes=("#5a3a20", 1.1, 0.65, "z"))
skins = {"default": hide, "hide": hide, "belly": flat("#e8d7ae"), "beak": pelt("#e0b455", "#c0923a", seed=172), "beak_lo": flat("#b08630"),
         "crest": pelt("#d04a3a", "#a63226", seed=173), "arm": pelt("#7b4f2e", "#5c3a20", seed=174),
         "membrane": pelt("#d59a5e", "#b57a44", seed=175, stripes=("#8f5a30", 1.6, 0.5, "x")), "membrane_tip": pelt("#c88a50", "#a86e3a", seed=176),
         "leg": solid("#84512e"), "claw": claw_paint(), "eye": eye_color("#f6e35a"), "dark": flat("#2a1a10")}
fl = lambda s, k=1: {f"wing_{s}": {"rotation": ["0", "0", f"math.sin(query.life_time * 260) * {35 * k} * {1 if s == 'l' else -1}"]},
                     f"wing_{s}2": {"rotation": ["0", "0", f"math.sin(query.life_time * 260 - 40) * {25 * k} * {1 if s == 'l' else -1}"]},
                     f"wing_{s}3": {"rotation": ["0", "0", f"math.sin(query.life_time * 260 - 80) * {18 * k} * {1 if s == 'l' else -1}"]}}
an = {"idle": anim(merge(fl("l"), fl("r"), bob("body", 0.6, 130), sway("tail0", 8, 60, 1),
                          {"head": {"rotation": ["math.sin(query.life_time * 70) * 4", "math.sin(query.life_time * 40) * 8", "0"]}})),
      "walk": anim(merge(swing({"leg_l": 0, "leg_r": 180}, 25, 0, 50)))}
SPEC = finish("pterodactyl", "Skyglider Pterodactyl", ("#a86f45", "#d04a3a"), bones, skins, an, ["idle", {"walk": "query.modified_move_speed > 0.02"}], {
    "role": "mount", "health": 24, "speed": 0.25, "fly": True, "fly_speed": 0.3, "damage": 4, "box": [1.0, 0.9],
    "ride": {"seats": [[0, 0.95, 0.1]]}, "family": ["pterosaur"],
    "loot": [("minecraft:feather", 1, 2), ("minecraft:leather", 0, 1)], "sound": ("phantom", [1.2, 1.5]),
    "spawn": {"biomes": ["jungle", "mesa", "savanna"], "weight": 5, "herd": [1, 3]}})
