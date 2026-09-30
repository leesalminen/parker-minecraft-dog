"""River Otter - sleek tameable swimmer."""
from eggsc_kit import *

leg = 3
q = dict(bw=5, bh=5, bl=14, leg=leg, lw=2, ld=2, foot=1, foot_w=2, foot_l=2, head=(5, 4, 5), hy=leg + 2, hz=-6,
         snout=(3, 2, 2, 1), nosec=(2, 1), ear=dict(w=2, h=1, d=1, rot=0, x=1.3, z=2, inner=False),
         eyes=(1, 1.8, 0.62, False), tail=[(3, 3, 5), (3, 3, 5), (2, 2, 4)], tail_y=leg + 1, tail_rot=0, bob=0.2)
q["extra_head"] = [cube([-3, leg + 2.5, -10.5], [1, 1, 1], "whisk"), cube([2, leg + 2.5, -10.5], [1, 1, 1], "whisk")]


def fur(p):
    x, y, z = p.p
    c = mix("#5e4130", "#7a5842", noise3(x * 0.6, y * 0.6, z * 0.6, 5, 4.0))
    c = shade(c, 0.88 + 0.24 * noise3(x * 2.2, y * 2.2, z * 1.4, 8, 1.0))
    if p.bone in ("body", "head", "neck") and y < leg + 2.5:
        c = mix(c, "#d8c3a0", 0.8)
    if p.bone == "head" and p.face == "front" and p.y >= p.fh - 2:
        c = mix(c, "#e0d0b0", 0.9)
    return c


cfg = dict(base="#6b4a34", fur=fur, muzzle="#e0d0b0", nose="#181012", eye="#100a08", foot="#4a3020", inner="#6b4a34", tip="#4a3020")
SPEC = quad_spec("otter", "River Otter", ("#6b4a34", "#d8c3a0"), q, cfg,
                 beh("companion", 12, 0.3, [0.5, 0.45], ["otter"], spawn={"biomes": ["river", "swamp", "taiga"], "weight": 6, "herd": [2, 4]},
                     loot=[("minecraft:cod", 0, 1)], sound=("fox", [1.25, 1.4]), tame_items=["minecraft:cod", "minecraft:salmon"]),
                 extra_skins={"whisk": flat("#e8e0d0")}, amp=34, freq=56,
                 extra_idle=merge(sway("body", 4, 60, 1)))
