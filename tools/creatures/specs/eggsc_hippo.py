"""River Hippo - huge-mouthed neutral bruiser."""
from eggsc_kit import *

leg, bh, bl = 6, 15, 28
q = dict(bw=18, bh=bh, bl=bl, leg=leg, lw=6, ld=6, foot=0, spread=0.5, head=(13, 11, 9), hy=leg + 1, hz=-11,
         snout=(12, 8, 7, 2), nosec=(9, 2), ear=dict(w=3, h=2, d=1, rot=20, x=3.5, z=3, inner=False),
         eyes=(3, 0, 0, False), tail=[(2, 2, 4)], tail_y=leg + bh - 4, tail_rot=-30, bob=0.25)
hy, hz = q["hy"], q["hz"]
# eyes and nostrils on top bumps, tusk row
q["eyes"] = None
q["extra_head"] = [cube([-6, hy + 9, hz - 8], [3, 3, 3], "fur"), cube([3, hy + 9, hz - 8], [3, 3, 3], "fur"),
                   cube([-5.5, hy + 12, hz - 7.5], [2, 1, 2], "eye"), cube([3.5, hy + 12, hz - 7.5], [2, 1, 2], "eye"),
                   cube([-2.5, hy + 8, hz - 15.5], [1, 1, 1], "nose"), cube([1.5, hy + 8, hz - 15.5], [1, 1, 1], "nose"),
                   cube([-5, hy + 1, hz - 15.5], [2, 2, 1], "horn"), cube([3, hy + 1, hz - 15.5], [2, 2, 1], "horn"),
                   cube([-1, hy + 1, hz - 15.5], [2, 2, 1], "horn")]
q["extra_body"] = [cube([-9, leg + 5, -8], [18, 4, 14], "fur", inflate=0.4)]


def fur(p):
    x, y, z = p.p
    c = mix("#736a80", "#8a7f92", noise3(x * 0.6, y * 0.6, z * 0.6, 5, 4.0))
    c = shade(c, 0.92 + 0.16 * noise3(x * 2.4, y * 2.4, z * 2.4, 8, 1.0))
    if y < leg + 5 and not p.bone == "head":
        c = mix(c, "#b48a90", 0.5)
    if p.bone in ("head",) and y < 9:
        c = mix(c, "#b48a90", 0.4)
    if p.bone in ("body",) and y > leg + bh - 1:
        c = shade(c, 0.92)
    return c


cfg = dict(base="#7c7286", fur=fur, muzzle="#a8909a", nose="#3a2c32", eye="#1a1214", foot="#5a5060", horn="#efe6cf")
SPEC = quad_spec("hippo", "River Hippo", ("#7c7286", "#c99aa6"), q, cfg,
                 beh("neutral", 50, 0.2, [1.6, 1.4], ["hippo"], spawn={"biomes": ["swamp", "mangrove_swamp", "river"], "weight": 4, "herd": [1, 3]},
                    loot=[("minecraft:leather", 1, 3), ("minecraft:porkchop", 1, 2)], sound=("ravager", [0.7, 0.85]), damage=7,
                    knockback_resist=0.4, xp=4),
                 amp=18, freq=34)
