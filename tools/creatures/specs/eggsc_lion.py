"""Savanna Lion - neutral big cat with a shaggy mane."""
from eggsc_kit import *

q = dict(bw=10, bh=11, bl=20, leg=11, lw=4, ld=4, foot=2, foot_w=1, claws=3, head=(8, 8, 7), hy=19, hz=-7,
         snout=(4, 3, 3, 2), ear=dict(w=3, h=3, d=1, rot=0, x=2.5),
         tail=[(2, 2, 7), (2, 2, 7), (3, 3, 3)], tail_y=18, tail_rot=-18, tail_tip=True)
q["extra_head"] = [cube([-6.5, 16.5, -9.5], [13, 13, 5], "mane"), cube([-7.5, 18, -9], [15, 9, 4], "mane"),
                   cube([-4.5, 14.5, -10], [9, 15, 4], "mane"), cube([-5, 12, -9], [10, 4, 4], "mane")]
q["extra_body"] = [cube([-5.5, 18, -12], [11, 7, 6], "mane", inflate=0.2)]
cfg = dict(base="#c9974f", dark="#8a5a2a", belly="#e9cf9c", belly_y=14, muzzle="#eedcb0", nose="#5a3030",
           eye="#7a5010", mane="#6e3f18", tip="#3a2410", inner="#a06a50", foot="#a67b3c", seed=41)


def mane(p):
    x, y, z = p.p
    c = mix("#55300f", "#8c5a24", noise3(x * 2, y * 0.8, z * 2, 5, 1.2))
    return shade(c, 0.8 + 0.4 * noise3(x * 3, y * 3, z * 3, 8, 1.0))


SPEC = quad_spec("lion", "Savanna Lion", ("#d6a45a", "#6e3f18"), q, cfg,
                 beh("neutral", 26, 0.3, [0.9, 1.5], ["lion"], spawn={"biomes": ["savanna"], "weight": 3, "herd": [1, 3]},
                    loot=[("minecraft:beef", 1, 3), ("minecraft:bone", 0, 1)], sound=("polarbear", [0.7, 0.85]), damage=5, xp=3),
                 extra_skins={"mane": mane}, amp=30, freq=45)
