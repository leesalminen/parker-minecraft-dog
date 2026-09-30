"""Outback Kangaroo - hopping passive marsupial with a joey in the pouch."""
from eggsc_kit import *

leg = 12
q = dict(tw=7, th=10, td=6, leg=leg, lw=3, ld=4, foot=(3, 2, 8), claws=2, lean=16, head=(5, 5, 6), hy_off=-2, hz_frac=0.9,
         snout=(3, 3, 4, 1), ear=dict(w=2, h=6, d=1, rot=8, x=0.6, z=3), eye=1, eye_in=0.5,
         arm=(2, 7, 2, 2, 0), hand=(2, 2, 2), hclaws=2,
         tail=[(5, 5, 8), (4, 4, 8), (3, 3, 6)], tail_y=leg + 1, tail_rot=-48, tail_tip=True)
q["extra_body"] = [cube([-4.5, leg - 4, -1], [9, 8, 6], "fur"),           # haunches
                   cube([-2.5, leg + 1, -3.6], [5, 4, 1], "dark"),        # pouch
                   cube([-1.5, leg + 3.5, -4.2], [3, 3, 1], "fur"),       # joey head
                   cube([-1.5, leg + 6, -4.0], [1, 2, 1], "fur"), cube([0.5, leg + 6, -4.0], [1, 2, 1], "fur"),
                   cube([-1.2, leg + 4.6, -4.5], [1, 1, 1], "eye"), cube([0.2, leg + 4.6, -4.5], [1, 1, 1], "eye")]
cfg = dict(base="#b98559", dark="#8f6038", belly="#efdcbc", belly_y=leg + 5, muzzle="#e8d0ac", nose="#2a1c1c",
           eye="#1a120e", tip="#6e4a2a", inner="#e8b8a0", foot="#7a5230", claw="#3a2a20", seed=51)
SPEC = biped_spec("kangaroo", "Outback Kangaroo", ("#b98559", "#efdcbc"), q, cfg,
                  beh("passive", 16, 0.3, [0.7, 1.8], ["kangaroo"], spawn={"biomes": ["savanna", "mesa"], "weight": 6, "herd": [2, 4]},
                      loot=[("minecraft:leather", 0, 2), ("minecraft:beef", 1, 2)], sound=("fox", [0.7, 0.85])),
                  amp=42, freq=60, hop=True)
