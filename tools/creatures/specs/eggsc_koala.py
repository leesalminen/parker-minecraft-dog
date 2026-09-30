"""Eucalyptus Koala - sleepy, wall-climbing fluffball."""
from eggsc_kit import *

leg = 3
q = dict(bw=7, bh=7, bl=8, leg=leg, lw=3, ld=3, foot=1, claws=3, head=(8, 7, 6), hy=8, hz=-2, snout=(3, 3, 2, 1), nosec=(3, 2), nose_dy=0,
         ear=dict(w=4, h=4, d=1, rot=0, x=2, z=3, inner=True), eyes=(1, 2.6, 0.5, False),
         tail=[(4, 4, 2)], tail_y=leg + 1, bob=0.15)
q["extra_body"] = [cube([-3, leg + 1, -5], [6, 5, 2], "light"), cube([-4, leg + 6, -3], [8, 2, 8], "fur", inflate=0.3)]
q["extra_head"] = [cube([-3.5, 8, -8.3], [7, 3, 1], "light")]
cfg = dict(base="#8f8e98", dark="#6d6c78", belly="#e6e4e4", belly_y=leg + 2, muzzle="#8a8892", nose="#1a1418", eye="#120e10",
           inner="#f4f0ee", foot="#4e4c58", claw="#2a2630", seed=61)
SPEC = quad_spec("koala", "Eucalyptus Koala", ("#8f8e98", "#e6e4e4"), q, cfg,
                 beh("passive", 12, 0.1, [0.6, 0.8], ["koala"], spawn={"biomes": ["forest", "birch_forest"], "weight": 5, "herd": [1, 2]},
                     loot=[("minecraft:stick", 0, 2)], sound=("fox", [1.3, 1.5]), climb=True),
                 amp=22, freq=36)
