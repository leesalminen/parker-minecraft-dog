"""Dune Meerkat - tiny upright sentry."""
from eggsc_kit import *

leg = 4
q = dict(tw=4, th=7, td=3, leg=leg, lw=2, ld=2, foot=(2, 1, 3), head=(4, 4, 4), hy_off=-1, hz_frac=0.9,
         snout=(2, 2, 2, 1), ear=dict(w=1, h=1, d=1, x=1.5, z=2, inner=False), eye=1, eye_in=0.4,
         arm=(1, 4, 1, 1, 0), tail=[(1, 1, 5), (1, 1, 5)], tail_y=1, tail_rot=-30, tail_tip=True)


def bands(p):
    if p.bone == "body" and p.face in ("back", "east", "west", "top"):
        return 0.9 if math.sin(p.p[1] * 2.1 + 0.4) > 0.4 else 0.0
    return 0.0


base = fur_painter("#c9a674", "#a88350", "#eadcbc", belly_y=leg + 6, pattern=bands, patt="#6a4a2a", seed=101)


def face(p, c):
    if p.bone == "head":
        if p.face == "front" and 1 <= p.y <= 2 and (p.x <= 0 or p.x >= p.fw - 1 or p.x == 1 or p.x == p.fw - 2):
            c = "#2a1e16"
        if p.face in ("east", "west") and p.y == 1:
            c = "#2a1e16"
        if p.face == "top":
            c = mix(c, "#e8d6b0", 0.5)
    if p.bone == "body" and p.face == "front" and p.y > 2:
        c = mix(c, "#f0e4c8", 0.6)
    return c


fur = with_face(base, face)
cfg = dict(base="#c9a674", fur=fur, muzzle="#e8d6b0", nose="#1a120e", eye="#120c0a", foot="#5a4028", inner="#a88350", tip="#3a2a1a", claw="#3a2a1a")
SPEC = biped_spec("meerkat", "Dune Meerkat", ("#c9a674", "#3a2a1a"), q, cfg,
                  beh("passive", 8, 0.3, [0.4, 0.9], ["meerkat"], spawn={"biomes": ["desert", "savanna"], "weight": 6, "herd": [3, 6]},
                      loot=[("minecraft:sand", 0, 1)], sound=("fox", [1.6, 1.8])),
                  amp=36, freq=64)
