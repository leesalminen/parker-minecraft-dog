"""Wyvern - two-legged wyrm whose forelimbs are its wings, with a long barbed tail.  Flies."""
from eggsb_kit import *

HIDE, HIDE_D, BELLY, MEMB = "#7a3a30", "#4a2020", "#d8b078", "#a04a3a"

hide = scales(HIDE, dark=HIDE_D, light="#a05a44", cell=2.2, seed=261)

def belly(p):
    if p.face == "bottom" or p.p[1] < 13.5 and p.face != "top": return mix(BELLY, "#b89058", 0.5 if int(p.p[2] / 1.5) % 2 else 0.0)
    return hide(p)

def memb(p):
    c = mix(MEMB, "#d08a6a", noise3(*p.p, 263, 2.0))
    return shade(c, 0.88) if p.face in ("top", "bottom") and (p.x % 4 == 0) else c

def horn(p): return shade(mix("#d8d0b8", "#8a8068", (p.p[2] * 0.3) % 1.0), 0.95)
def claw(p): return "#2a2218"
def fang(p): return "#f4eedd"
def barb(p): return shade(mix("#3a2a24", "#6a4a3a", noise3(*p.p, 265, 1.0)), 1.0)

bones = [
    bone("body", None, [0, 16, 0], [C([-4.5, 11, -8], [9, 9, 16], "belly"), C([-3, 20, -6], [6, 2, 12], "hide"),
                                    *[C([-0.5, 21.5, -6 + i * 3], [1, 2, 2], "horn") for i in range(5)]]),
    bone("neck0", "body", [0, 16, -8], [C([-2.5, 15, -12], [5, 6, 5], "hide"), C([-2.5, 19, -11], [5, 4, 5], "hide")]),
    bone("neck1", "neck0", [0, 22, -11], [C([-2, 20, -14], [4, 6, 4], "hide"), C([-2, 25, -15], [4, 5, 4], "hide"),
                                          *[C([-0.5, 24 + i * 2, -10.5 - i * 2.5], [1, 2, 2], "horn") for i in range(3)]]),
    bone("head", "neck1", [0, 29, -15], [
        C([-3, 28, -22], [6, 5, 8], "hide"), C([-2.5, 28.5, -27], [5, 3, 5], "hide"), C([-2.5, 31.6, -26.5], [1, 1, 1], "dark"), C([1.5, 31.6, -26.5], [1, 1, 1], "dark"),
        C([-2, 27.4, -26.5], [1, 1, 1], "fang"), C([1, 27.4, -26.5], [1, 1, 1], "fang"),
        eyes(1.6, 30.2, -22, "eye", 2),
        pair(C([1.5, 32, -19], [2, 2, 5], "horn", rot=[-25, 0, 0], pivot=[2.5, 32, -18])),
        pair(C([2.5, 30, -18], [1, 3, 3], "memb", rot=[0, 0, -30], pivot=[3, 31, -17])),
        C([-1, 33, -20], [2, 1, 5], "horn")]),
    bone("jaw", "head", [0, 28, -22], [C([-2.5, 26.5, -26], [5, 2, 7], "hide"), C([-2, 28.2, -25.5], [1, 1, 1], "fang"), C([1, 28.2, -25.5], [1, 1, 1], "fang"),
                                       C([-2, 28, -24], [4, 1, 5], "mouth")]),
    bone("tail0", "body", [0, 15, 8], [C([-3.5, 12, 8], [7, 7, 8], "hide")]),
    bone("tail1", "tail0", [0, 14, 16], [C([-3, 11.5, 16], [6, 5, 8], "hide")]),
    bone("tail2", "tail1", [0, 13, 24], [C([-2, 11, 24], [4, 4, 8], "hide")]),
    bone("tail3", "tail2", [0, 12.5, 32], [C([-1.5, 10.5, 32], [3, 3, 8], "hide"), C([-3.5, 9.5, 39], [7, 1, 4], "barb"), C([-1, 9, 41], [2, 1, 4], "barb"),
                                          C([-0.5, 13, 39], [1, 3, 3], "barb")]),
]
for nm, sx in (("l", 1), ("r", -1)):
    x = sx * 3.5
    bones.append(bone(f"leg_{nm}", None, [x, 14, 1], [C([x - 2.5, 5, -2], [5, 9, 6], "hide"), C([x - 2, 0, -1], [4, 6, 4], "hide"), C([x - 2, 0, -6], [4, 2, 5], "claw"),
                                                   C([x - 2, 2, -5], [1, 1, 1], "claw"), C([x + 1, 2, -5], [1, 1, 1], "claw")]))
bones.append(bat_wing("wing_l", "body", 1, 4, 19, -5, 26, 15, "hide", "memb"))
bones.append(bat_wing("wing_r", "body", -1, 4, 19, -5, 26, 15, "hide", "memb"))
def fold_wing():
    return fold("wing_l", "wing_r", 40, 3, 60)

anims = {
    "walk": anim(merge(biped_walk("leg_l", "leg_r", 32, 36), sway("tail0", 6, 60, 1), sway("tail1", 9, 60, 1, 0.8), sway("tail2", 12, 60, 1, 1.6),
                       sway("tail3", 14, 60, 1, 2.4), fold_wing(), bob("body", 0.4, 200), {"neck0": {"rotation": ["10", "0", "0"]}})),
    "idle": anim(merge(bob("body", 0.5, 70), sway("tail0", 5, 35, 1), sway("tail1", 8, 35, 1, 1), sway("tail2", 11, 35, 1, 2), sway("tail3", 14, 35, 1, 3),
                       sway("neck0", 4, 40, 1), sway("neck1", 6, 45, 1, 1), fold_wing(),
                       {"head": {"rotation": ["math.sin(query.life_time * 60) * 4", "math.sin(query.life_time * 31) * 10", "0"]},
                        "jaw": {"rotation": ["math.max(0, math.sin(query.life_time * 80)) * 6", "0", "0"]}})),
    "flap": flap_anim("wing_l", "wing_r", amp=42, rate=300, extra=merge(sway("tail1", 10, 90, 0), sway("tail3", 12, 90, 0, 1),
                                                                        {"leg_l": {"rotation": ["25", "0", "0"]}, "leg_r": {"rotation": ["25", "0", "0"]}})),
}

SPEC = with_visible({
    "id": "wyvern", "name": "Wyvern", "egg": ("#7a3a30", "#d8b078"), "glow": False, "scale": 1.25,
    "bones": bones, "look": False,
    "skins": {"default": hide, "hide": hide, "belly": belly, "memb": memb, "horn": horn, "claw": claw, "fang": fang, "barb": barb,
              "dark": solid("#1a1010", 0.2, 3), "mouth": solid("#6a2028", 0.1, 4), "eye": eye("#ffc020", pupil="#201000")},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "hostile", "health": 64, "speed": 0.26, "fly": True, "fly_speed": 0.34, "damage": 9, "box": [1.6, 2.0], "knockback_resist": 0.3,
        "family": ["wyvern", "dragon"], "xp": 25,
        "spawn": {"biomes": ["extreme_hills", "mesa"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:leather", 1, 4), ("minecraft:bone", 1, 4), ("minecraft:phantom_membrane", 0, 2), ("minecraft:feather", 0, 2)],
        "sound": ("dragon", [1.3, 1.5]),
    },
})
