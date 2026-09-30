"""Savanna Giraffe - tall rideable mount."""
from eggsc_kit import *

leg, bh, bl = 20, 13, 20
q = dict(bw=12, bh=bh, bl=bl, leg=leg, lw=4, ld=4, foot=3, hoof=True, foot_w=1, foot_l=1, spread=0.5,
         head=(5, 5, 8), hy=leg + bh + 22 - 2, hz=-4, neck=(5, 26, 5, leg + bh - 4, -9),
         ear=dict(w=3, h=2, d=1, rot=-30, x=2.5, z=4, inner=False, tip=1),
         eyes=(2, 0, 0.55, True), eye_z=2,
         tail=[(1, 1, 3), (1, 1, 6), (3, 3, 3)], tail_y=leg + bh - 3, tail_rot=-75, tail_tip=True, head_swing=2)
q["extra_neck"] = [cube([-1, leg + bh - 2, -5.5], [2, 26, 2], "mane")]
hy = q["hy"]
q["extra_head"] = [cube([-1.5, hy - 1, -12.4], [3, 3, 1], "nose"), cube([-2, hy + 5, -10], [1, 3, 1], "horn"),
                   cube([1, hy + 5, -10], [1, 3, 1], "horn"), cube([-2.5, hy + 8, -10.5], [2, 2, 2], "tip"),
                   cube([0.5, hy + 8, -10.5], [2, 2, 2], "tip")]
q["snout"] = (4, 4, 3, 1)
q["nosec"] = False


def patches(p):
    return patch_pat(scale=6.5, line=0.2, seed=13)(p)


def fur(p):
    x, y, z = p.p
    f1, f2, h = voronoi(x, y, z, 6.0, 13)
    if f2 - f1 < 0.16:
        c = "#f0dca8"
    else:
        c = mix("#b5722c", "#7a4620", h * 0.8)
    c = shade(c, 0.9 + 0.2 * noise3(x * 2, y * 2, z * 2, 3, 1.0))
    if p.bone.startswith("leg") and y < 8 or (p.bone.startswith("leg") and abs(p.p[1]) < 14):
        c = mix(c, "#f0dca8", 0.55)
    if y < 20 and not p.bone.startswith("leg"):
        c = mix(c, "#f0dca8", 0.4)
    return c


cfg = dict(base="#b5722c", fur=fur, muzzle="#e8cfa0", nose="#3a2a24", eye="#1a1210", mane="#5a3418", foot="#2a2622",
           inner="#e8b090", horn="#a67c48", tip="#2a1e18")
SPEC = quad_spec("giraffe", "Savanna Giraffe", ("#e2b25a", "#7a4620"), q, cfg,
                 beh("mount", 34, 0.24, [1.3, 3.8], ["giraffe"], spawn={"biomes": ["savanna"], "weight": 5, "herd": [2, 4]},
                    loot=[("minecraft:leather", 1, 2), ("minecraft:hay_block", 0, 1)], sound=("horse", [0.7, 0.85]), damage=3,
                    ride={"seats": [[0, 2.05, 0]], "jump": 0.45}),
                 amp=24, freq=40)
