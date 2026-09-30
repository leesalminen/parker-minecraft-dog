"""Riverbank Capybara - chill kid-sized mount, tangerine included."""
from eggsc_kit import *

leg = 5
q = dict(bw=12, bh=10, bl=20, leg=leg, lw=3, ld=3, foot=1, claws=3, spread=0.5, head=(8, 8, 9), hy=8, hz=-8,
         snout=(6, 6, 2, 1), nosec=(6, 2), ear=dict(w=2, h=2, d=1, rot=0, x=1.5, z=3, inner=False),
         eyes=(2, 3, 0.7, False), tail=[(2, 2, 1)], tail_y=leg + 5, bob=0.2)
q["extra_head"] = [cube([-2, 16, -11], [4, 2, 4], "orange"), cube([-0.5, 18, -9.5], [1, 1, 1], "leaf")]
q["extra_body"] = [cube([-5.5, leg + 8, -8], [11, 3, 16], "fur", inflate=0.1)]


def orange(p):
    return shade("#f28a1c", 0.9 + 0.25 * noise3(p.p[0] * 3, p.p[1] * 3, p.p[2] * 3, 5, 1.0))


cfg = dict(base="#9c6a3e", dark="#7a5030", belly="#c89a62", belly_y=leg + 4, muzzle="#7a5030", nose="#3a261a", eye="#140e0c",
           foot="#5a3c24", seed=81)
SPEC = quad_spec("capybara", "Riverbank Capybara", ("#9c6a3e", "#f28a1c"), q, cfg,
                 beh("mount", 22, 0.2, [1.0, 1.1], ["capybara"], spawn={"biomes": ["swamp", "jungle", "mangrove_swamp"], "weight": 6, "herd": [3, 5]},
                     loot=[("minecraft:leather", 0, 1)], sound=("fox", [0.75, 0.85]), damage=1,
                     ride={"seats": [[0, 0.95, 0]], "jump": 0.4}),
                 extra_skins={"orange": orange, "leaf": flat("#4c8a2c")}, amp=22, freq=40)
