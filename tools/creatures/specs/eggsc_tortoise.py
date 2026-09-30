"""Giant Tortoise - slow, sturdy, very rideable."""
from eggsc_kit import *

leg = 5
q = dict(bw=16, bh=6, bl=22, leg=leg, lw=6, ld=6, foot=1, foot_w=1, foot_l=2, claws=3, spread=0.5, head=(5, 5, 7), hy=leg + 1, hz=-11,
         ear=None, eyes=(1, 1.9, 0.6, False), tail=[(2, 2, 3)], tail_y=leg + 1, tail_rot=-10, bob=0.1)
top = leg + 6
q["extra_body"] = [cube([-9, top - 3, -12.5], [18, 4, 25], "shell"), cube([-8, top + 1, -11], [16, 3, 22], "shell"),
                   cube([-6, top + 4, -8], [12, 3, 16], "shell"), cube([-3, top + 7, -4], [6, 2, 8], "shell"),
                   cube([-8, top - 4, -12], [16, 2, 24], "rim")]


def shell(p):
    x, y, z = p.p
    f1, f2, h = voronoi(x, y * 1.2, z, 6.5, 121)
    edge = f2 - f1
    if edge < 0.14:
        return shade("#3a2e1c", 0.9 + 0.2 * noise3(x * 2, y * 2, z * 2, 3, 1.0))
    c = mix("#6c7a3a", "#8a7a3e", h)
    # growth rings
    c = shade(c, 0.9 + 0.12 * math.sin(f1 * 14 + h * 6))
    return shade(c, 0.92 + 0.16 * noise3(x * 3, y * 3, z * 3, 5, 1.0))


def hide(p):
    x, y, z = p.p
    c = mix("#8a8a56", "#a09a62", noise3(x * 1.2, y * 1.2, z * 1.2, 7, 1.5))
    f1, f2, h = voronoi(x, y, z, 2.0, 55)
    if f2 - f1 < 0.2:
        c = shade(c, 0.72)
    return c


cfg = dict(base="#8f8c58", fur=hide, muzzle="#a09a62", nose="#3a3628", eye="#120e08", foot="#6c6a3e", tip="#6c6a3e", claw="#d8d0b0")
SPEC = quad_spec("tortoise", "Giant Tortoise", ("#6c7a3a", "#d8d0b0"), q, cfg,
                 beh("mount", 44, 0.1, [1.5, 1.1], ["tortoise"], spawn={"biomes": ["desert", "savanna"], "weight": 3, "herd": [1, 2]},
                     loot=[("minecraft:scute", 0, 1), ("minecraft:seagrass", 0, 2)], sound=("turtle", [0.7, 0.85]), damage=2,
                     knockback_resist=0.7, ride={"seats": [[0, 1.05, 0]], "jump": 0.3}),
                 extra_skins={"shell": shell, "rim": flat("#3a2e1c", 0.15)}, amp=16, freq=26, attack=False)
