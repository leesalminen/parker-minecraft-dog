"""Jungle Tiger - striped neutral big cat."""
from eggsc_kit import *

q = dict(bw=10, bh=10, bl=22, leg=10, lw=4, ld=4, foot=2, claws=3, head=(8, 7, 7), hy=15, hz=-9,
         snout=(4, 3, 3, 1), ear=dict(w=3, h=3, d=1, rot=0, x=2.5, tip=1),
         tail=[(2, 2, 7), (2, 2, 7), (2, 2, 6)], tail_y=16, tail_rot=-15, tail_tip=True,
         tail_climb=0)
q["extra_head"] = [cube([-5, 14.5, -13], [1, 3, 3], "light"), cube([4, 14.5, -13], [1, 3, 3], "light"),
                   cube([-4.5, 15.5, -15.6], [9, 1, 1], "light", inflate=0)]
q["extra_head"] = q["extra_head"][:2]
pat = stripe_pat(axis=2, freq=1.25, width=0.35, wobble=1.0, seed=9, ymin=-1)


def stripes(p):
    if p.bone.startswith("leg"):
        return 1.0 if math.sin(p.p[1] * 1.6 + p.p[2] * 0.3) > 0.55 and p.p[1] > 2 else 0.0
    if p.bone in ("head",):
        return 1.0 if abs(math.sin(p.p[0] * 1.7 + 0.6)) > 0.86 and p.p[1] > 17 else 0.0
    return pat(p)


cfg = dict(base="#dc8630", dark="#b8621c", belly="#f6ead2", belly_y=13, muzzle="#f6ead2", nose="#c67a72",
           eye="#c8a030", pattern=stripes, patt="#1e1512", tip="#1e1512", inner="#e8b8a0", foot="#c26f1e", seed=17)
SPEC = quad_spec("tiger", "Jungle Tiger", ("#dc8630", "#1e1512"), q, cfg,
                 beh("neutral", 28, 0.32, [0.9, 1.3], ["tiger"], spawn={"biomes": ["jungle"], "weight": 3, "herd": [1, 2]},
                    loot=[("minecraft:beef", 1, 3), ("minecraft:leather", 0, 1)], sound=("polarbear", [0.75, 0.9]), damage=5, xp=3),
                 amp=32, freq=46)
