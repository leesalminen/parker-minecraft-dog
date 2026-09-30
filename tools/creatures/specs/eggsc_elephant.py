"""Savanna Elephant - gentle giant mount with a swinging trunk."""
from eggsc_kit import *

leg, bh, bl = 20, 22, 32
q = dict(bw=20, bh=bh, bl=bl, leg=leg, lw=8, ld=8, foot=3, foot_w=1, foot_l=1, claws=3, spread=0.5, head=(14, 15, 11),
         hy=leg + bh - 16, hz=-14, snout=None, eyes=(2, 5.5, 0.55, False),
         ear=dict(w=10, h=14, d=2, rot=-14, x=6, z=6, sink=14, inner=True),
         tail=[(2, 2, 4), (2, 9, 2), (3, 3, 3)], tail_y=leg + bh - 3, tail_rot=-85, tail_tip=True, bob=0.4, head_swing=2)
hy, hz = q["hy"], q["hz"]
fz = hz - 11
tr = [{"name": "trunk0", "parent": "head", "pivot": [0, hy + 8, fz + 1], "cubes": [cube([-3.5, hy - 6, fz - 3], [7, 15, 5])]},
      {"name": "trunk1", "parent": "trunk0", "pivot": [0, hy - 6, fz + 1], "cubes": [cube([-3, hy - 14, fz - 3], [6, 9, 5])]},
      {"name": "trunk2", "parent": "trunk1", "pivot": [0, hy - 14, fz + 1], "cubes": [cube([-2.5, hy - 21, fz - 3], [5, 8, 5], "trunkend")]},
      {"name": "trunk3", "parent": "trunk2", "pivot": [0, hy - 21, fz], "cubes": [cube([-2, hy - 24, fz - 5], [4, 3, 6], "trunkend")]}]
q["more_bones"] = tr
q["extra_head"] = [cube([4, hy - 1, fz - 5], [2, 2, 7], "horn"), cube([-6, hy - 1, fz - 5], [2, 2, 7], "horn"),
                   cube([4, hy - 2, fz - 9], [2, 2, 4], "horn"), cube([-6, hy - 2, fz - 9], [2, 2, 4], "horn"),
                   cube([-7, hy + 11, hz - 4], [14, 3, 5], "fur", inflate=0.4)]


def fur(p):
    x, y, z = p.p
    n = noise3(x * 0.7, y * 0.5, z * 0.7, 5, 3.0)
    c = mix("#7c7a80", "#9a989e", n)
    fold = noise3(x * 0.4, y * 1.6, z * 0.4, 8, 1.6)
    if fold < 0.33:
        c = shade(c, 0.78)
    c = shade(c, 0.92 + 0.16 * noise3(x * 1.3, y * 1.3, z * 1.3, 9, 1.0))
    if p.bone.startswith("leg") and y < 4:
        c = mix(c, "#b8b2a8", 0.4)
    return c


cfg = dict(base="#8a888e", fur=fur, foot="#c8c0b0", eye="#1a1614", horn="#efe6cf", inner="#c99a98", tip="#4a4850")
SPEC = quad_spec("elephant", "Savanna Elephant", ("#8a888e", "#efe6cf"), q, cfg,
                 beh("mount", 80, 0.18, [2.2, 3.3], ["elephant"], spawn={"biomes": ["savanna"], "weight": 3, "herd": [2, 4]},
                    loot=[("minecraft:leather", 2, 4), ("minecraft:bone", 1, 2)], sound=("ravager", [0.55, 0.7]), damage=8,
                    knockback_resist=0.6, ride={"seats": [[0, 2.65, 0]], "jump": 0.4}),
                 extra_skins={"trunkend": fur}, amp=20, freq=32,
                 extra_idle=merge(sway("trunk0", 5, 45, 0), sway("trunk1", 9, 40, 0, 0.6), sway("trunk2", 13, 36, 0, 1.2),
                                  sway("trunk3", 16, 33, 0, 1.8)))
