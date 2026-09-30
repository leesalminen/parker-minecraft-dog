"""Taiga Moose - towering antlered mount."""
from eggsc_kit import *

leg, bh, bl = 19, 15, 24
q = dict(bw=14, bh=bh, bl=bl, leg=leg, lw=5, ld=5, foot=2, hoof=True, foot_w=1, foot_l=0, spread=0.5, head=(7, 8, 13),
         hy=leg + bh + 1, hz=-6, neck=(6, 12, 7, leg + bh - 6, -12), neck_rot=[22, 0, 0],
         snout=(5, 5, 3, 1), nosec=(4, 2), eyes=(1, 0, 0.62, True), eye_z=4,
         ear=dict(w=2, h=4, d=1, rot=-40, x=2.6, z=4, inner=True), tail=[(2, 3, 3)], tail_y=leg + bh - 5, tail_rot=-40, bob=0.3)
hy, hz = q["hy"], q["hz"]
ex = []
for sgn in (1, -1):
    def M(c):
        return c if sgn > 0 else mirror(c)
    ex.append(M(cube([2.5, hy + 7, hz - 4], [4, 2, 2], "horn")))
    ex.append(M(cube([5.5, hy + 7, hz - 6], [10, 2, 10], "horn")))
    for i in range(4):
        ex.append(M(cube([6 + i * 3, hy + 7, hz - 9 - (1 if i in (1, 2) else 0) - 2], [1, 1, 3], "horn")))
    ex.append(M(cube([9, hy + 8, hz - 4], [2, 3, 1], "horn")))
ex.append(cube([-1, hy - 4, hz - 8], [2, 5, 2], "dark"))
q["extra_head"] = ex
q["extra_body"] = [cube([-5, leg + bh, -bl / 2 + 2], [10, 4, 9], "fur")]


def fur(p):
    x, y, z = p.p
    c = mix("#4a3222", "#5e422d", noise3(x * 0.6, y * 0.4, z * 0.6, 5, 3.0))
    c = shade(c, 0.9 + 0.2 * noise3(x * 1.8, y * 1.8, z * 1.8, 7, 1.0))
    if p.bone.startswith("leg"):
        c = mix(c, "#a89476", 0.55 * min(1.0, max(0.0, (16 - y) / 12 + 0.3)))
    if p.bone == "body" and y < leg + 3:
        c = mix(c, "#7a6248", 0.5)
    return c


cfg = dict(base="#4a3222", fur=fur, muzzle="#2e2018", nose="#181210", eye="#120e0c", horn="#b8a06e", inner="#8a6a52",
           foot="#1e1814", dark="#2a1c14")
SPEC = quad_spec("moose", "Taiga Moose", ("#4a3222", "#b8a06e"), q, cfg,
                 beh("mount", 42, 0.22, [1.4, 2.5], ["moose"], spawn={"biomes": ["taiga"], "weight": 4, "herd": [1, 2]},
                     loot=[("minecraft:leather", 1, 3), ("minecraft:beef", 1, 3)], sound=("horse", [0.65, 0.8]), damage=6,
                     knockback_resist=0.3, ride={"seats": [[0, 2.1, 0]], "jump": 0.5}),
                 amp=24, freq=38)
