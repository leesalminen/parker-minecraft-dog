"""Minotaur - hulking bull-headed axeman with a golden nose ring."""
from eggsb_kit import *

FUR, FUR_D, SKINC = "#5a3a26", "#33201a", "#8a5c40"

def hair(p):
    x, y, z = p.p
    n = noise3(x * 1.5, y * 2.0, z * 1.5, 251, 1.0)
    c = mix(FUR_D, FUR, 0.25 + 0.75 * n)
    return shade(c, 0.9 + 0.2 * hash01(int(x), int(y), int(z), 3))

def hide(p):
    c = coat(SKINC, dark="#5a3a28", light="#a8785a", seed=253, patch=2.5)(p)
    if p.bone == "body" and p.face == "front" and p.p[1] > 15 and abs(p.p[0]) < 4 and noise3(*p.p, 255, 1.2) > 0.45: return hair(p)   # chest fur
    return c

def face(p):
    c = hair(p)
    if p.face == "front" and p.fw >= 6 and 2 <= p.y <= p.fh - 1 and 2 <= p.x <= p.fw - 3: return mix("#c8a888", "#8a6a54", noise3(*p.p, 257, 1.0))
    return c

def horn(p): return shade(mix("#eee2c0", "#b8a878", (p.p[1] * 0.35) % 1.0), 0.95)
def gold(p): return shade("#f2c94c", 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 5))
def leather(p): return shade("#3a2a1c", 0.85 + 0.3 * noise3(*p.p, 259, 1.0))
def hoof(p): return shade("#1c1612", 0.9 + 0.2 * noise3(*p.p, 261, 1.0))
def steel(p): return mix("#b8bcc4", "#6a6e78", noise3(*p.p, 263, 0.9))
def wood(p): return shade("#6a4a2a", 0.9 + 0.2 * noise3(*p.p, 265, 1.0))

bones = biped(12, 13, 7, 11, 5, 5, 17, 5, 5, (8, 8, 8), skin="hide", head_skin="face", leg_skin="hair", arm_skin="hide", leg_x=3.3,
              head_dy=-1, head_dz=-1.5, hand_h=5, hand_skin="leather", foot_h=4, foot_skin="hoof", shoulder_drop=1)
add(bones, "head",
    C([-2.5, 23.2, -8.5], [5, 4, 3], "snout"), C([-1.5, 25.0, -9.2], [1, 1, 1], "dark"), C([0.5, 25.0, -9.2], [1, 1, 1], "dark"),
    C([-1, 22.4, -9.5], [2, 1, 1], "gold"), C([-1.5, 21.4, -9.6], [1, 1, 1], "gold"), C([0.5, 21.4, -9.6], [1, 1, 1], "gold"), C([-1, 20.6, -9.6], [2, 1, 1], "gold"),
    eyes(1.0, 27.2, -5.5, "eye", 2),
    pair(C([4, 31, -4], [2, 3, 2], "horn", rot=[0, 0, -30], pivot=[3.5, 30, -3])),
    pair(C([5.5, 33.5, -4], [2, 3, 2], "horn", rot=[0, 0, -60], pivot=[3.5, 30, -3])),
    pair(C([7, 35.5, -4], [1, 3, 2], "horn", rot=[0, 0, -90], pivot=[3.5, 30, -3])),
    pair(C([4, 27, -3], [3, 2, 2], "hair", rot=[0, 0, 20], pivot=[4, 28, -2])))
add(bones, "body", C([-6, 11, -3.5], [12, 4, 7], "leather"), C([-3, 19, -4], [1, 5, 1], "leather"), C([2, 19, -4], [1, 5, 1], "leather"),
    C([-6.4, 12, -3], [13, 2, 6], "leather"), C([-3, 13, -4], [6, 4, 1], "leather"), C([-2, 12, -4.2], [4, 3, 1], "gold"))
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    add(bones, n_, C([sx * 8.5 - 3, 6, -3], [6, 3, 6], "leather"))
    add(bones, n_, C([sx * 8.5 - 3, 17, -3], [6, 3, 6], "gold"))
# double-headed axe in the right hand
add(bones, "arm_r", C([-9.5, 0, -8.5], [2, 26, 2], "wood"), C([-14.5, 17, -9], [5, 8, 1], "steel"), C([-9.5 + 2, 17, -9], [5, 8, 1], "steel"),
    C([-11, 19, -9.5], [3, 4, 2], "steel"))

anims = biped_anims(walk_amp=28, arm_amp=20, freq=30, body_bob=0.5,
                    extra_idle={"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 24) * 9", "0"]}})
anims["attack"] = anim(merge({"body": {"rotation": ["math.sin(variable.attack_time * 180) * 24", "0", "0"]},
                              "head": {"rotation": ["math.sin(variable.attack_time * 180) * 16", "0", "0"]}}), loop=False)

SPEC = with_visible({
    "id": "minotaur", "name": "Minotaur", "egg": ("#5a3a26", "#f2c94c"), "glow": False, "scale": 1.2,
    "bones": bones,
    "skins": {"default": hide, "hide": hide, "hair": hair, "face": face, "snout": lambda p: mix("#d8b898", "#a88870", noise3(*p.p, 267, 1.0)),
              "horn": horn, "gold": gold, "leather": leather, "hoof": hoof, "steel": steel, "wood": wood, "dark": solid("#2a1a14", 0.2, 5),
              "eye": eye("#e83a2a", pupil="#200808")},
    "anims": anims, "play": PLAY_WALK_IDLE + ["attack"],
    "behavior": {
        "role": "hostile", "health": 72, "speed": 0.27, "damage": 11, "box": [1.2, 2.5], "knockback_resist": 0.5, "family": ["minotaur"],
        "xp": 25, "reach": 1.3,
        "spawn": {"biomes": ["mesa", "savanna", "extreme_hills"], "weight": 3, "herd": [1, 1]},
        "loot": [("minecraft:leather", 2, 5), ("minecraft:beef", 1, 4), ("minecraft:gold_nugget", 1, 5), ("minecraft:iron_ingot", 0, 2)],
        "sound": ("ravager", [0.7, 0.85]),
    },
})
