"""Bog Troll - huge, hunched brute with a knobbly club and mossy shoulders."""
from eggsb_kit import *

HIDE, HIDE_D, MOSS, CLOTH, WOOD = "#7d8f6a", "#55654a", "#4c7a34", "#6b4a2c", "#6b4522"

def wart(p, c):
    x, y, z = p.p
    if hash01(int(x * 0.7), int(y * 0.7), int(z * 0.7), 81) > 0.93: return "#a3b58a"
    if noise3(x, y, z, 83, 1.6) > 0.82: return "#5b6b4a"

hide = coat(HIDE, dark=HIDE_D, light="#9ab086", seed=79, patch=3, extra=wart)

def moss(p):
    return shade(mix("#3c6a2a", "#6a9a48", noise3(*p.p, 85, 1.2)), 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 3))

def cloth(p):
    c = coat(CLOTH, dark="#4a3018", seed=87)(p)
    return shade(c, 0.9) if (p.x + p.y) % 4 == 0 else c

def club(p):
    x, y, z = p.p
    c = coat(WOOD, dark="#4a2f14", light="#8a5c30", seed=89, patch=2)(p)
    if p.bone == "arm_r" and p.p[1] > 12 and hash01(p.x, p.y, p.fw, 9) > 0.86: return "#c8c8c0"   # nails
    return c

def tusk(p): return shade("#eee6cc", 0.9 + 0.2 * hash01(p.x, p.y, 1, 2))

def mouth(p):
    c = hide(p)
    if p.face == "front" and p.y >= p.fh - 2 and 1 <= p.x <= p.fw - 2: return "#3a2a24"
    return c

bones = biped(10, 12, 7, 10, 5, 5, 16, 4, 5, (7, 6, 7), skin="hide", head_skin="face", leg_x=3, foot_h=2, foot_skin="claw",
              head_dy=-2, head_dz=-3, hand_h=5, hand_skin="hide")
add(bones, "body", C([-4, 11, -6.2], [8, 6, 3], "hide"), C([-5, 9, -4.2], [10, 5, 1], "cloth"),
    C([-5, 9, 3.2], [10, 5, 1], "cloth"), C([-5, 21, 0.5], [10, 4, 4], "hide"),          # hunched shoulder mass
    pair(C([5, 22, -3], [4, 2, 6], "moss")), C([-3, 25, 1], [6, 2, 3], "moss"))
add(bones, "head", C([-3.5, 24, -9.2], [7, 1, 2], "hide"), eyes(1.0, 22.6, -6.5, "eye", 2),
    pair(C([1.5, 20.5, -9.8], [1, 3, 1], "tusk")), C([-1.5, 21.5, -10.5], [3, 3, 3], "hide"),
    pair(C([3.5, 22.5, -4.5], [2, 3, 2], "hide", rot=[0, 0, -15], pivot=[3.5, 23, -4])), C([-3, 25.6, -5.5], [6, 1, 4], "moss"))
add(bones, "arm_r", C([-9, 0, -8.5], [3, 16, 3], "club"), C([-10, 12, -9.5], [5, 6, 5], "club"))
by(bones, "arm_r")["cubes"].append(C([-8, 3, -6], [1, 1, 2], "club"))

SPEC = with_visible({
    "id": "troll", "name": "Bog Troll", "egg": ("#7d8f6a", "#6b4522"), "glow": False, "scale": 1.25,
    "bones": bones,
    "skins": {"default": hide, "hide": hide, "face": mouth, "moss": moss, "cloth": cloth, "club": club, "tusk": tusk,
              "claw": solid("#2a2a22", 0.2, 6), "eye": eye("#f0d040", pupil="#201800")},
    "anims": biped_anims(walk_amp=28, arm_amp=22, freq=32, body_bob=0.5,
                         extra_idle={"body": {"rotation": ["math.sin(query.life_time * 45) * 1.5", "0", "0"]}}),
    "play": PLAY_WALK_IDLE + ["attack"],
    "behavior": {
        "role": "hostile", "health": 60, "speed": 0.24, "damage": 9, "box": [1.2, 2.2], "knockback_resist": 0.6,
        "family": ["troll"], "xp": 20, "reach": 1.2,
        "spawn": {"biomes": ["swamp", "taiga", "forest"], "weight": 4, "herd": [1, 1]},
        "loot": [("minecraft:bone", 1, 3), ("minecraft:slime_ball", 0, 3), ("minecraft:iron_ingot", 0, 1), ("minecraft:stick", 1, 4)],
        "sound": ("ravager", [0.7, 0.85]),
    },
})
SPEC["anims"]["attack"] = anim(merge({"body": {"rotation": ["math.sin(variable.attack_time * 180) * 22", "0", "0"]},
                                       "head": {"rotation": ["math.sin(variable.attack_time * 180) * 14", "0", "0"]}}), loop=False)
