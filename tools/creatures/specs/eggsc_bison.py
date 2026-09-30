"""Prairie Bison - shaggy-shouldered herd mount."""
from eggsc_kit import *

leg, bh, bl = 9, 14, 22
q = dict(bw=14, bh=bh, bl=bl, leg=leg, lw=5, ld=5, foot=2, hoof=True, foot_w=1, foot_l=0, spread=0.5, head=(9, 9, 8),
         hy=leg - 1, hz=-9, snout=(6, 5, 3, 2), nosec=(4, 2), ear=dict(w=2, h=3, d=1, rot=40, x=3.6, z=3, inner=False),
         eyes=(2, 3.4, 0.62, False), tail=[(2, 2, 4), (3, 3, 3)], tail_y=leg + bh - 5, tail_rot=-60, tail_tip=True, bob=0.25)
hy, hz = q["hy"], q["hz"]
q["extra_head"] = [cube([-2.5, hy + 8, hz - 7], [5, 3, 5], "mane"),
                   cube([4.5, hy + 6, hz - 6], [3, 2, 2], "horn"), cube([7, hy + 7, hz - 6], [2, 4, 2], "horn"),
                   cube([-7.5, hy + 6, hz - 6], [3, 2, 2], "horn"), cube([-9, hy + 7, hz - 6], [2, 4, 2], "horn"),
                   cube([-2.5, hy - 5, hz - 10], [5, 6, 3], "mane")]
q["extra_body"] = [cube([-7, leg + bh - 2, -bl / 2 - 1], [14, 5, 13], "mane"),
                   cube([-7.5, leg + 1, -bl / 2 - 1.5], [15, 10, 8], "mane"),
                   cube([-6, leg - 3, -bl / 2 + 2], [12, 4, 6], "mane")]


def fur(p):
    x, y, z = p.p
    c = mix("#6c4c32", "#7c5a3c", noise3(x * 0.5, y * 0.5, z * 0.5, 5, 4.0))
    c = shade(c, 0.9 + 0.2 * noise3(x * 2, y * 2, z * 2, 8, 1.0))
    if z > 1:
        c = mix(c, "#8a6a48", min(1.0, (z - 1) / 14) * 0.4)
    if p.bone.startswith("leg"):
        c = shade(c, 0.8)
    return c


def mane(p):
    x, y, z = p.p
    c = mix("#33231a", "#4a3324", noise3(x * 2.5, y * 0.6, z * 2.5, 4, 1.2))
    return shade(c, 0.8 + 0.4 * noise3(x * 4, y * 1.5, z * 4, 6, 1.0))


cfg = dict(base="#6c4c32", fur=fur, muzzle="#2e2018", nose="#1a1210", eye="#120c0a", horn="#2a2622", mane="#33231a",
           foot="#1a1614", inner="#3a2a20", tip="#33231a")
SPEC = quad_spec("bison", "Prairie Bison", ("#6c4c32", "#33231a"), q, cfg,
                 beh("mount", 46, 0.2, [1.5, 1.7], ["bison"], spawn={"biomes": ["plains"], "weight": 6, "herd": [3, 6]},
                     loot=[("minecraft:leather", 1, 3), ("minecraft:beef", 1, 3)], sound=("ravager", [0.85, 1.0]), damage=6,
                     knockback_resist=0.5, ride={"seats": [[0, 1.65, 0.2]], "jump": 0.4}),
                 extra_skins={"mane": mane}, amp=22, freq=36)
