"""Meadow Hedgehog - tiny tameable spikeball."""
from eggsc_kit import *

leg = 2
q = dict(bw=6, bh=4, bl=8, leg=leg, lw=2, ld=2, foot=0, head=(4, 4, 4), hy=leg + 1, hz=-3,
         snout=(2, 2, 3, 1), nosec=(1, 1), ear=dict(w=1, h=1, d=1, rot=0, x=1.2, z=2, inner=False),
         eyes=(1, 1.3, 0.62, False), bob=0.1)
sp = [cube([-3.5, leg + 2, -3], [7, 4, 10], "spine")]
for xx in (-3, -0.5, 2):
    for zz, hh in ((-2, 2), (1, 3), (4, 2)):
        sp.append(cube([xx, leg + 6, zz], [2, hh, 2], "spine"))
sp.append(cube([-3.5, leg + 1, 4], [7, 4, 3], "spine"))
q["extra_body"] = sp


def spine(p):
    x, y, z = p.p
    band = math.sin(x * 2.4 + z * 1.3 + y * 1.1)
    c = mix("#4a3a2a", "#c9b48a", 0.5 + 0.5 * band)
    if hash01(int(x * 2), int(z * 2), int(y * 2), 5) > 0.85:
        c = "#e8dcc0"
    return shade(c, 0.85 + 0.3 * noise3(x * 3, y * 3, z * 3, 2, 1.0))


cfg = dict(base="#b89a76", dark="#8c7050", belly="#e2cfae", belly_y=leg + 2, muzzle="#e2cfae", nose="#1a1210", eye="#120c0a",
           foot="#8c7050", inner="#b89a76", seed=97)
SPEC = quad_spec("hedgehog", "Meadow Hedgehog", ("#b89a76", "#4a3a2a"), q, cfg,
                 beh("companion", 8, 0.2, [0.45, 0.4], ["hedgehog"], spawn={"biomes": ["forest", "plains", "taiga"], "weight": 6, "herd": [1, 2]},
                     loot=[("minecraft:stick", 0, 1)], sound=("fox", [1.7, 1.9]), tame_items=["minecraft:sweet_berries", "minecraft:apple"]),
                 extra_skins={"spine": spine}, amp=40, freq=70)
