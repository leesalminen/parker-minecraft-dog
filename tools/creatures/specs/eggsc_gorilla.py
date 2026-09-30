"""Jungle Gorilla - silverback bruiser, neutral until poked."""
from eggsc_kit import *

leg = 9
q = dict(tw=14, th=14, td=9, leg=leg, lw=5, ld=5, foot=(6, 2, 7), lean=14, head=(8, 7, 8), hy_off=-2, hz_frac=0.85,
         snout=(5, 4, 2, 1), ear=dict(w=2, h=2, d=1, x=3.5, z=3, inner=False, rot=0), eye=2, eye_in=0.4, eyef=0.5,
         arm=(5, 20, 5, 1, 0.5), hand=(6, 3, 6), lspread=0.5)
hy = leg + 14 - 2
hz = -4.5 + 8 * 0.85 - 0
q["extra_head"] = [cube([-4.5, hy + 3.5, hz - 9], [9, 2, 2], "dark"), cube([-2, hy + 7, hz - 7], [4, 3, 6], "fur")]
q["extra_body"] = [cube([-7.5, leg + 1, 0.6], [15, 12, 4], "silver"), cube([-4, leg + 5, -5.2], [8, 6, 1], "skin"),
                   cube([-7.5, leg + 11, -3], [15, 3, 7], "fur", inflate=0.3)]


def silver(p):
    x, y, z = p.p
    return shade(mix("#7c7a82", "#a8a6ae", noise3(x, y, z, 3, 2.0)), 0.9 + 0.2 * noise3(x * 2.5, y * 2.5, z * 2.5, 9, 1.0))


cfg = dict(base="#2f2d34", dark="#1e1c22", muzzle="#3c363c", nose="#0c0a0c", eye="#2a1408", foot="#1e1c22", inner="#2f2d34", seed=109)
cfg["fur"] = fur_painter("#2f2d34", "#1e1c22", None, fine=0.2, seed=109)
SPEC = biped_spec("gorilla", "Jungle Gorilla", ("#2f2d34", "#a8a6ae"), q, cfg,
                  beh("neutral", 44, 0.26, [1.2, 2.0], ["gorilla"], spawn={"biomes": ["jungle"], "weight": 3, "herd": [2, 4]},
                      loot=[("minecraft:bone", 1, 2), ("minecraft:leather", 0, 1)], sound=("polarbear", [0.55, 0.7]), damage=7,
                      knockback_resist=0.4, xp=4),
                  extra_skins={"silver": silver, "skin": flat("#231f26", 0.1)}, amp=30, freq=42, arm_amp=26)
