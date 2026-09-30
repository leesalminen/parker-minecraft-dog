"""Burrow Badger - low, grumpy digger with a striped face."""
from eggsc_kit import *

leg = 3
q = dict(bw=8, bh=6, bl=14, leg=leg, lw=3, ld=3, foot=1, foot_w=1, foot_l=2, claws=3, head=(5, 4, 7), hy=leg + 2, hz=-5,
         snout=(3, 2, 3, 1), nosec=(2, 1), ear=dict(w=2, h=2, d=1, rot=0, x=1.0, z=3, inner=False),
         eyes=(1, 1.7, 0.6, False), tail=[(3, 3, 3)], tail_y=leg + 2, tail_rot=-10, bob=0.15)


def grizzle(p):
    return 0.0


base = fur_painter("#7a7a80", "#55555c", "#26262a", belly_y=leg + 3, fine=0.22, seed=107)


def face(p, c):
    if p.bone == "head":
        x = p.p[0]
        if p.face in ("top", "front"):
            if abs(x) < 0.9:
                return "#efeeea"
            if abs(x) < 1.9:
                return "#1e1e22"
            if p.face == "front" and p.y >= 2:
                return "#dcdad4"
        if p.face in ("east", "west") and p.y >= 1:
            return mix(c, "#1e1e22", 0.7) if p.x > 2 else c
    if p.bone.startswith("leg"):
        return mix(c, "#26262a", 0.7)
    return c


fur = with_face(base, face)
cfg = dict(base="#7a7a80", fur=fur, muzzle="#dcdad4", nose="#101012", eye="#0a0808", foot="#26262a", inner="#26262a", claw="#d8d4c8")
SPEC = quad_spec("badger", "Burrow Badger", ("#7a7a80", "#efeeea"), q, cfg,
                 beh("neutral", 16, 0.25, [0.7, 0.55], ["badger"], spawn={"biomes": ["forest", "taiga", "plains"], "weight": 3, "herd": [1, 2]},
                     loot=[("minecraft:leather", 0, 1), ("minecraft:bone", 0, 1)], sound=("polarbear", [1.4, 1.6]), damage=4),
                 amp=28, freq=52)
