"""Unicorn - rideable, friendly.  Pearl coat, spiral horn, pastel mane and tail."""
from eggsb_kit import *

WHITE, PINK, LAV, MINT, SKY, GOLD = "#f6f2fa", "#f6c6e0", "#c9b3f0", "#b8ecd8", "#a9d8f8", "#f7dc7a"

def pastel(p):
    t = (p.p[2] * 0.22 + p.p[1] * 0.12 + noise3(*p.p, 5, 2.0))
    stops = [PINK, LAV, SKY, MINT, PINK]
    f = (t % 1.0) * 4; i = int(f)
    return shade(mix(stops[i], stops[i + 1], f - i), 0.95 + 0.1 * hash01(p.x, p.y, p.p[2], 3))

def horn(p):
    band = math.sin((p.p[1] + p.p[0] * 1.3 + p.p[2]) * 1.5) > 0.2
    return mix(GOLD, "#fff3b0", 0.7) if band else shade(GOLD, 0.82)

def hoof(p):
    return mix("#e9c2dc", "#c9a0c8", noise3(*p.p, 9, 1))

def ear_in(p):
    return PINK if p.face == "front" else shade(WHITE, 0.95)

def sparkle(p, c):
    if hash01(p.p[0] * 3, p.p[1] * 3, p.p[2] * 3, 41) > 0.965: return "#ffffff"

coat_fn = coat(WHITE, dark="#dcd3ea", light="#ffffff", under="#efe6f6", under_y=13, seed=11, patch=3, extra=sparkle)

bones = quad(10, 10, 20, 14, 3, (6, 7, 8), 22, head_dz=-1, skin="coat", foot_h=2, foot_skin="hoof", neck=(6, 12, 38),
             leg_ld=3)
add(bones, "head", C([-2.5, 22.5, -19], [5, 4, 4], "muzzle"), side_eyes(3, 25.5, -14.5),
    pair(C([1.5, 29, -8], [2, 4, 2], "coat")), pair(C([1.9, 29.6, -7.6], [1, 2, 1], "ear_in")),
    C([-1, 29, -13], [2, 7, 2], "horn", rot=[-8, 0, 0], pivot=[0, 29, -12]),
    C([-0.5, 35, -13.6], [1, 4, 1], "horn", rot=[-8, 0, 0], pivot=[0, 29, -12]),
    C([-1, 28.4, -12.4], [2, 2, 2], "gold"))
add(bones, "head", C([-1, 28, -10], [2, 3, 4], "mane"), C([-1, 22, -6], [2, 12, 3], "mane", rot=[38, 0, 0], pivot=[0, 21, -8]),
    C([-1, 23, -4], [2, 3, 3], "mane"))
bones.append(bone("tail", "body", [0, 22, 10], [
    C([-1.5, 10, 10], [3, 12, 3], "mane"), C([-2.5, 4, 11], [2, 8, 2], "mane"), C([0.5, 5, 11], [2, 7, 2], "mane"),
    C([-1, 2, 12], [2, 6, 2], "mane")]))

SPEC = with_visible({
    "id": "unicorn", "name": "Unicorn", "egg": ("#f6f2fa", "#c9b3f0"), "glow": False, "scale": 1.0,
    "bones": bones,
    "skins": {"default": coat_fn, "coat": coat_fn, "muzzle": face_detail(coat(PINK, light="#ffd8ec", seed=2)),
              "hoof": hoof, "horn": horn, "mane": pastel, "eye": eye("#b070e0"), "ear_in": ear_in, "gold": solid(GOLD)},
    "anims": quad_anims(tail="tail", tail_amp=14, ears=()),
    "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "companion", "health": 30, "speed": 0.3, "box": [1.2, 1.9], "family": ["unicorn", "horse"],
        "ride": {"seats": [[0, 1.5, 0.1]], "jump": 0.9},
        "tame_items": ["minecraft:apple", "minecraft:golden_carrot", "minecraft:sugar"],
        "spawn": {"biomes": ["plains", "flower_forest", "meadow"], "weight": 3, "herd": [1, 2]},
        "loot": [("minecraft:glowstone_dust", 0, 2), ("minecraft:leather", 0, 1)],
        "sound": ("horse", [1.2, 1.4]),
    },
})
