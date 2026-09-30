"""Savanna Zebra - fast striped mount."""
from eggsc_kit import *

leg, bh, bl = 14, 10, 20
q = dict(bw=9, bh=bh, bl=bl, leg=leg, lw=3, ld=3, foot=2, hoof=True, foot_w=1, foot_l=0, head=(5, 6, 8), hy=leg + bh + 5, hz=-6,
         neck=(5, 12, 6, leg + bh - 4, -10), neck_rot=[28, 0, 0], eyes=(1, 0, 0.6, True), eye_z=2,
         ear=dict(w=2, h=4, d=1, rot=0, x=1.2, z=3, inner=True, tip=1),
         tail=[(2, 2, 2), (3, 9, 2)], tail_y=leg + bh - 3, tail_rot=-75, tail_tip=True, snout=(4, 5, 3, 1), nosec=(3, 2))
q["extra_neck"] = [cube([-1, leg + bh - 2, -6], [2, 13, 2], "mane")]


def stripes(p):
    x, y, z = p.p
    if p.bone.startswith("leg"):
        return 1.0 if math.sin(y * 1.8) > 0.05 else 0.0
    if p.bone in ("neck", "head"):
        return 1.0 if math.sin(y * 1.6 + x * 0.3) > 0.1 else 0.0
    if p.face in ("front", "back"):
        return 1.0 if math.sin(x * 1.5) > 0.0 else 0.0
    w = math.sin(z * 1.45 + 0.5 * noise3(x, y, z, 4, 3.0) * 3 + y * 0.15)
    return 1.0 if w > 0.0 else 0.0


def fur(p):
    x, y, z = p.p
    base = mix("#e9e6dc", "#fbfaf4", noise3(x, y, z, 3, 3.0))
    if stripes(p) > 0:
        base = shade("#26232a", 0.9 + 0.3 * noise3(x * 2, y * 2, z * 2, 6, 1.0))
    if y < leg + 1 and not p.bone.startswith("leg") and stripes(p) == 0:
        base = mix(base, "#efe9d8", 0.4)
    return base


cfg = dict(base="#f0eee4", fur=fur, muzzle="#6a5a52", nose="#1a1616", eye="#140e0c", mane="#26232a", foot="#2a2622",
           inner="#d8b0a8", tip="#26232a")
SPEC = quad_spec("zebra", "Savanna Zebra", ("#f0eee4", "#26232a"), q, cfg,
                 beh("mount", 22, 0.3, [1.0, 1.7], ["zebra"], spawn={"biomes": ["savanna"], "weight": 8, "herd": [3, 6]},
                    loot=[("minecraft:leather", 0, 2)], sound=("horse", [1.0, 1.15]), damage=3,
                    ride={"seats": [[0, 1.45, 0]], "jump": 0.8}),
                 amp=34, freq=44)
