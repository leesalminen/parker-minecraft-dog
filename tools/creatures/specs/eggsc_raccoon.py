"""Bandit Raccoon - tameable masked scavenger with a ringed tail."""
from eggsc_kit import *

leg = 4
q = dict(bw=7, bh=6, bl=12, leg=leg, lw=2, ld=2, foot=1, foot_w=1, foot_l=1, claws=3, head=(7, 5, 5), hy=leg + 3, hz=-5,
         snout=(3, 2, 3, 1), nosec=(2, 1), ear=dict(w=2, h=3, d=1, rot=0, x=1.2, z=3, inner=True),
         eyes=(1, 2.3, 0.5, False), tail=[(4, 4, 3), (4, 4, 3), (4, 4, 3), (4, 4, 3)], tail_y=leg + 2, tail_rot=4,
         tail_tip=True, bob=0.2)


def rings(p):
    if p.bone.startswith("tail"):
        return 0.95 if math.sin(p.p[2] * 1.7) > 0.05 else 0.0
    if p.bone.startswith("leg"):
        return 0.7
    return 0.0


base = fur_painter("#9a9694", "#6c6866", "#c8c4c0", belly_y=leg + 3, pattern=rings, patt="#2c292a", seed=93)


def face(p, c):
    if p.bone == "head" and p.face == "front":
        fw, fh = p.fw, p.fh
        c = mix(c, "#d8d4d0", 0.5)
        if 1 <= p.y <= 3:
            c = "#26232a"
        if p.y == 0 and abs(p.x - fw / 2 + 0.5) < 1:
            c = "#26232a"
        if p.y == 2 and (p.x == 2 or p.x == fw - 3):
            c = "#1a1a1a"
    if p.bone == "head" and p.face in ("east", "west") and 1 <= p.y <= 3:
        c = "#26232a"
    return c


fur = with_face(base, face)
cfg = dict(base="#9a9694", fur=fur, muzzle="#e8e4dc", nose="#141012", eye="#f0e8d0", inner="#3a3438", tip="#26232a", foot="#2c292a", claw="#c8c0b0")
SPEC = quad_spec("raccoon", "Bandit Raccoon", ("#9a9694", "#26232a"), q, cfg,
                 beh("companion", 14, 0.28, [0.6, 0.65], ["raccoon"], spawn={"biomes": ["forest", "swamp"], "weight": 5, "herd": [1, 2]},
                     loot=[("minecraft:string", 0, 1)], sound=("fox", [1.15, 1.3]), tame_items=["minecraft:cooked_chicken", "minecraft:sweet_berries"]),
                 amp=32, freq=52)
