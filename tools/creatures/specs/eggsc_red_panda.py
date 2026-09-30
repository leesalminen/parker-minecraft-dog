"""Bamboo Red Panda - tameable, ringed-tail forest buddy."""
from eggsc_kit import *

leg = 4
q = dict(bw=6, bh=6, bl=12, leg=leg, lw=2, ld=2, foot=1, foot_w=1, foot_l=1, head=(7, 5, 5), hy=leg + 3, hz=-5,
         snout=(3, 2, 2, 1), nosec=(2, 1), ear=dict(w=3, h=3, d=1, rot=0, x=1, z=3, inner=True), eyes=(1, 2.2, 0.5, False),
         tail=[(5, 5, 4), (5, 5, 4), (4, 4, 3)], tail_y=leg + 2, tail_rot=-6, tail_tip=True, bob=0.2)
q["extra_head"] = [cube([-3.5, leg + 3, -9.2], [7, 2, 1], "fur", inflate=0)]
q["extra_head"] = []


def rings(p):
    if p.bone.startswith("tail"):
        return 0.85 if math.sin(p.p[2] * 1.15) > 0.3 else 0.0
    if p.bone.startswith("leg"):
        return 1.0
    return 0.0


base = fur_painter("#b8562a", "#8e3c1c", "#3a2222", belly_y=leg + 3, pattern=rings, patt="#6e2e16", seed=83)


def face(p, c):
    if p.bone == "head":
        if p.face == "front":
            fw, fh = p.fw, p.fh
            if p.y >= 2 and (p.x <= 1 or p.x >= fw - 2):
                c = "#f6efe2"
            if p.y == 2 and (p.x == 2 or p.x == fw - 3):
                c = "#f6efe2"
            if p.y >= 3 and p.x in (2, fw - 3):
                c = "#6e2e16"
        elif p.face == "top":
            c = mix(c, "#d88a54", 0.5)
    return c


fur = with_face(base, face)
cfg = dict(base="#b8562a", fur=fur, muzzle="#f6efe2", nose="#1a1210", eye="#140e0c", inner="#f6efe2", tip="#3a2222",
           foot="#2a1a1a")
SPEC = quad_spec("red_panda", "Bamboo Red Panda", ("#b8562a", "#f6efe2"), q, cfg,
                 beh("companion", 14, 0.28, [0.55, 0.7], ["red_panda"], spawn={"biomes": ["forest", "taiga"], "weight": 3, "herd": [1, 2]},
                     loot=[("minecraft:bamboo", 0, 2)], sound=("fox", [1.3, 1.5]), tame_items=["minecraft:bamboo", "minecraft:apple"]),
                 amp=32, freq=54)
