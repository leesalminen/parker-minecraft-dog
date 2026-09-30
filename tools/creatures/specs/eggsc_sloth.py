"""Canopy Sloth - very slow, permanently smiling."""
from eggsc_kit import *

leg = 8
q = dict(bw=7, bh=7, bl=12, leg=leg, lw=2, ld=2, foot=1, claws=3, foot_w=2, foot_l=3, head=(6, 6, 5), hy=leg + 3, hz=-5,
         ear=dict(w=2, h=1, d=1, rot=0, x=0.5, z=2, inner=False), eyes=None, tail=[(2, 2, 2)], tail_y=leg + 2, bob=0.15)
q["extra_body"] = [cube([-4, leg - 1, -4], [8, 3, 10], "fur", inflate=0.2), cube([-4, leg + 5, -5], [8, 3, 12], "fur", inflate=0.4)]
hy = q["hy"]


def mossy(p):
    x, y, z = p.p
    f1, f2, h = voronoi(x, y, z, 5.0, 91)
    return 0.55 if f1 < 0.45 and h > 0.5 else 0.0


base = fur_painter("#8d7a5c", "#5e4e38", "#a8946e", belly_y=leg + 2, pattern=mossy, patt="#77894e", fine=0.2, seed=71)


def face(p, c):
    if p.bone == "head" and p.face == "front":
        fw, fh = p.fw, p.fh
        c = mix(c, "#e6d8b6", 0.9)
        # dark eye bands
        if 1 <= p.y <= 3 and (p.x <= 1 or p.x >= fw - 2) and fh >= 5:
            c = "#2a2016"
        if p.y == 2 and (p.x == 1 or p.x == fw - 2):
            c = "#f6f2e6"
        if p.y == fh - 2 and fw // 2 - 1 <= p.x <= fw // 2:
            c = "#2a1c14"
        if p.y == fh - 3 and 1 < p.x < fw - 2 and (p.x in (2, fw - 3)):
            c = "#4a3a28"
    return c


fur = with_face(base, face)
cfg = dict(base="#8d7a5c", fur=fur, belly="#a8946e", muzzle="#e6d8b6", nose="#2a1c14", foot="#3e3226", claw="#e8e0c8", inner="#a8946e")
SPEC = quad_spec("sloth", "Canopy Sloth", ("#8d7a5c", "#77894e"), q, cfg,
                 beh("passive", 14, 0.06, [0.7, 1.0], ["sloth"], spawn={"biomes": ["jungle"], "weight": 6, "herd": [1, 2]},
                     loot=[("minecraft:vine", 0, 2)], sound=("fox", [0.9, 1.05])),
                 amp=14, freq=26)
