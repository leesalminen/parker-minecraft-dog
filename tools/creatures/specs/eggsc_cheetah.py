"""Plains Cheetah - spotted sprinter."""
from eggsc_kit import *

leg = 12
q = dict(bw=7, bh=8, bl=20, leg=leg, lw=3, ld=3, foot=2, foot_w=1, foot_l=1, claws=3, head=(5, 5, 6), hy=leg + 5, hz=-8,
         snout=(3, 2, 2, 1), nosec=(2, 1), ear=dict(w=2, h=2, d=1, rot=0, x=1.5, z=3, inner=True),
         eyes=(1, 1.7, 0.6, False), tail=[(2, 2, 7), (2, 2, 7), (3, 3, 5)], tail_y=leg + 5, tail_rot=-12, tail_tip=True)
q["extra_body"] = [cube([-3, leg + 6, -8.5], [6, 4, 4], "fur", inflate=0.2)]
spots = spot_pat(scale=3.0, r=0.33, seed=113, ymin=leg + 2)


def pat(p):
    if p.bone.startswith("leg"):
        return spots(p) if p.p[1] > 4 else 0.0
    return spots(p)


base = fur_painter("#d9ad5e", "#b88a3e", "#f4ead0", belly_y=leg + 3, pattern=pat, patt="#2a1e14", seed=113)


def face(p, c):
    if p.bone == "head" and p.face == "front":
        if p.x in (0, 1) and p.y >= 2 and p.y < p.fh - 1 and False:
            return c
        if p.x == 1 and p.y >= 2 or p.x == p.fw - 2 and p.y >= 2:
            return "#26190f"
    return c


fur = with_face(base, face)
cfg = dict(base="#d9ad5e", fur=fur, muzzle="#f4ead0", nose="#241814", eye="#8a6a14", inner="#3a2a1a", tip="#2a1e14", foot="#b8863a")
SPEC = quad_spec("cheetah", "Plains Cheetah", ("#d9ad5e", "#2a1e14"), q, cfg,
                 beh("neutral", 18, 0.44, [0.7, 1.3], ["cheetah"], spawn={"biomes": ["savanna", "plains"], "weight": 3, "herd": [1, 2]},
                     loot=[("minecraft:beef", 1, 2)], sound=("cat", [0.6, 0.75]), damage=3, xp=3),
                 amp=38, freq=42)
