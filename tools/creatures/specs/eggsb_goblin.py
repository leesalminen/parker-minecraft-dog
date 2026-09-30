"""Cave Goblin - skinny, big-eared scamp with a rusty dagger.  Sneaky, only fights back when hit."""
from eggsb_kit import *

GREEN, RAG, LEATHER = "#6fae3c", "#7a5a34", "#4a3220"

skin = coat(GREEN, dark="#4f8a2a", light="#8fce58", seed=91, patch=2.5)

def face(p):
    c = skin(p)
    if p.face == "front" and p.y == p.fh - 1 and p.fw >= 6 and 1 < p.x < p.fw - 2:
        return "#e8e0c0" if p.x % 2 == 0 else "#2a3a18"   # jagged teeth
    return c

def rags(p):
    c = coat(RAG, dark="#4a3620", light="#9a7a4c", seed=93, patch=1.8)(p)
    return shade(c, 0.8) if noise3(*p.p, 95, 1.0) > 0.78 else c

def steel(p):
    return mix("#9aa0a4", "#5a4a3a", noise3(*p.p, 97, 1.0) * 0.7)

def ear_fn(p):
    return mix(skin(p), "#e89a9a", 0.4) if p.face in ("front", "back") else skin(p)

bones = biped(5, 6, 3, 6, 2, 2, 7, 2, 2, (6, 5, 5), skin="rags", head_skin="face", leg_skin="skin", arm_skin="skin",
              leg_x=1.5, foot_h=1, foot_skin="leather", arm_dx=0)
add(bones, "head",
    pair(C([3, 13.5, -0.5], [4, 2, 1], "ear", rot=[0, 0, 20], pivot=[3, 14.5, 0])),
    pair(C([6.4, 12.5, -0.5], [2, 1, 1], "ear", rot=[0, 0, 20], pivot=[3, 14.5, 0])),
    C([-1, 12.2, -3.6], [2, 3, 2], "skin"), eyes(1.0, 14.0, -2.5, "eye", 2),
    C([-3, 15.6, -2.5], [6, 1, 5], "skin"), C([-1, 17, -1], [2, 1, 3], "skin"))       # heavy brow + scruff tuft
add(bones, "body", C([-2.5, 6, -2.6], [5, 1, 1], "leather"), C([-3, 4, -2], [6, 2, 4], "rags"))
add(bones, "arm_r", C([-4.5, 2.5, -3.5], [1, 1, 3], "leather"), C([-4.5, 2.5, -9], [1, 1, 6], "steel"), C([-4.5, 1.5, -3.5], [1, 3, 1], "leather"))

SPEC = with_visible({
    "id": "goblin", "name": "Cave Goblin", "egg": ("#6fae3c", "#7a5a34"), "glow": False, "scale": 1.0,
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "face": face, "rags": rags, "leather": solid(LEATHER, 0.2, 8), "steel": steel,
              "ear": ear_fn, "eye": eye("#ffd82a", pupil="#1a1200")},
    "anims": biped_anims(walk_amp=45, arm_amp=38, freq=55, body_bob=0.5),
    "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "neutral", "health": 14, "speed": 0.32, "damage": 3, "box": [0.6, 1.15], "family": ["goblin"],
        "spawn": {"biomes": ["forest", "taiga", "swamp", "jungle"], "weight": 6, "herd": [2, 4]},
        "loot": [("minecraft:emerald", 0, 1), ("minecraft:gold_nugget", 0, 3), ("minecraft:iron_nugget", 0, 2)],
        "sound": ("villager", [0.8, 1.0]),
    },
})
