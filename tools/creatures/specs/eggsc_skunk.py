"""Stripe Skunk - fluffy tail, zero stink."""
from eggsc_kit import *

leg = 3
q = dict(bw=5, bh=5, bl=10, leg=leg, lw=2, ld=2, foot=1, foot_w=1, foot_l=1, head=(4, 4, 5), hy=leg + 2, hz=-3,
         snout=(2, 2, 2, 1), nosec=(1, 1), ear=dict(w=2, h=2, d=1, rot=0, x=0.8, z=2, inner=False),
         eyes=(1, 1.4, 0.55, False), tail=[(4, 5, 5), (5, 6, 5), (4, 5, 4)], tail_y=leg + 1, tail_rot=72, bob=0.15)


def stripe(p):
    x, y, z = p.p
    if p.bone == "head":
        return 1.0 if abs(x) < 0.6 and p.face in ("top", "front") and (p.face == "top" or p.y < 2) else 0.0
    if p.bone.startswith("tail"):
        return 1.0 if abs(x) < 1.8 else 0.0
    if p.bone == "body":
        return 1.0 if 0.6 < abs(x) < 2.0 and p.face in ("top", "back", "front") else 0.0
    return 0.0


base = fur_painter("#2a2630", "#1c1a20", "#3a3640", belly_y=leg + 2, pattern=stripe, patt="#f4f2ee", fine=0.1, seed=103)
cfg = dict(base="#2a2630", fur=base, muzzle="#3a3640", nose="#f0c8c8", eye="#0a0808", foot="#1c1a20", inner="#3a3640", tip="#f0eee8")
SPEC = quad_spec("skunk", "Stripe Skunk", ("#2a2630", "#f4f2ee"), q, cfg,
                 beh("passive", 8, 0.24, [0.5, 0.5], ["skunk"], spawn={"biomes": ["forest", "plains", "taiga"], "weight": 4, "herd": [1, 1]},
                     loot=[("minecraft:string", 0, 1)], sound=("fox", [1.4, 1.6])),
                 amp=30, freq=56)
