"""Savanna Rhino - armoured neutral charger."""
from eggsc_kit import *

leg, bh, bl = 10, 15, 28
q = dict(bw=15, bh=bh, bl=bl, leg=leg, lw=6, ld=6, foot=3, hoof=False, claws=3, foot_w=1, spread=0.5, head=(9, 10, 11),
         hy=leg + 1, hz=-11, snout=(7, 6, 4, 1), nosec=(5, 2), ear=dict(w=3, h=4, d=1, rot=15, x=2.5, z=5, tip=1),
         eyes=(2, 4.2, 0.65, False), tail=[(1, 1, 3), (1, 9, 1), (2, 3, 2)], tail_y=leg + bh - 3, tail_rot=-80, tail_tip=True,
         bob=0.25)
hy, hz = q["hy"], q["hz"]
fz = hz - 11 - 3
q["extra_head"] = [cube([-2, hy + 7, fz + 1], [4, 3, 5], "horn"), cube([-1.5, hy + 9, fz + 2], [3, 3, 3], "horn"),
                   cube([-1, hy + 11, fz + 3], [2, 3, 2], "horn"),
                   cube([-1.5, hy + 8, hz - 12], [3, 2, 3], "horn")]
q["extra_body"] = [cube([-8, leg + bh - 5, -bl / 2 + 3], [16, 8, 6], "fur", inflate=0.2),
                   cube([-7.5, leg + 3, bl / 2 - 9], [15, 10, 9], "fur", inflate=0.3)]


def fur(p):
    x, y, z = p.p
    c = mix("#7c7874", "#9a948c", noise3(x * 0.5, y * 0.5, z * 0.5, 5, 4.0))
    c = shade(c, 0.9 + 0.2 * noise3(x * 2.2, y * 2.2, z * 2.2, 8, 1.0))
    # armour plate creases
    if abs(math.sin(z * 0.55 + 0.9 * noise3(x, y, z, 2, 3.0))) < 0.07 and p.bone == "body":
        c = shade(c, 0.62)
    if y < leg + 4 and p.bone == "body":
        c = shade(mix(c, "#a8a098", 0.4), 0.95)
    return c


def horn(p):
    x, y, z = p.p
    return shade(mix("#5c5248", "#8a7c68", noise3(x, y, z, 3, 1.5)), 0.85 + 0.3 * (0.5 + 0.5 * math.sin(y * 1.3)))


cfg = dict(base="#87827c", fur=fur, muzzle="#8a847c", nose="#3a3430", eye="#141010", foot="#5c5650", inner="#a08880", tip="#4c4844")
SPEC = quad_spec("rhino", "Savanna Rhino", ("#87827c", "#efe6cf"), q, cfg,
                 beh("neutral", 52, 0.24, [1.6, 1.8], ["rhino"], spawn={"biomes": ["savanna"], "weight": 3, "herd": [1, 2]},
                    loot=[("minecraft:leather", 1, 3), ("minecraft:bone", 1, 2)], sound=("ravager", [0.65, 0.8]), damage=8,
                    knockback_resist=0.5, xp=4),
                 extra_skins={"horn": horn}, amp=22, freq=34)
