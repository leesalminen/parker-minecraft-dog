"""Garden Gnome - tiny, friendly wanderer with a floppy red hat and a long white beard."""
from eggsb_kit import *

SKIN, RED, BLUE, BEARD, BROWN = "#f0b892", "#d43a3a", "#3f6fc4", "#f6f6f2", "#5a3a22"

def hat(p):
    c = coat(RED, dark="#a82424", light="#f05a4a", seed=71, patch=2.5)(p)
    if p.bone == "head" and p.p[1] < 14 and p.face in ("front", "east", "west", "back"): return shade(c, 0.9)
    return c

def tunic(p):
    c = coat(BLUE, dark="#2c4d94", light="#5a8ae0", seed=73, patch=2.5)(p)
    if p.p[1] < 6 and p.p[1] > 5 and p.face != "top" and p.bone == "body":   # belt
        return "#e8c04a" if abs(p.p[0]) < 1 and p.face == "front" else "#3a2818"
    return c

def beard(p):
    return shade(mix(BEARD, "#d8d8d4", noise3(*p.p, 75, 1.4)), 0.92 + 0.16 * hash01(p.x, p.y, p.fw, 7))

def skin(p):
    c = coat(SKIN, dark="#d99a76", light="#ffd0b0", seed=77, patch=2)(p)
    if p.face == "front" and p.bone == "head" and p.y == p.fh - 2 and p.fw >= 6 and p.x in (1, p.fw - 2): return "#f28a8a"   # rosy cheeks
    return c

def mushroom(p):
    if p.face == "top": return "#e04040" if hash01(p.x, p.y, 9, 2) > 0.6 else "#ffe8e8"
    return "#f2ead8"

bones = biped(6, 5, 4, 4, 2, 2, 5, 2, 2, (6, 5, 5), skin="tunic", head_skin="skin", leg_skin="boots", arm_skin="tunic",
              leg_x=1.5, foot_h=1, foot_skin="boots2", hand_h=1, hand_skin="skin")
add(bones, "head",
    C([-4, 12.6, -4], [8, 1, 8], "hat"), C([-3, 13.6, -3], [6, 3, 6], "hat"), C([-2, 16.6, -2], [4, 3, 4], "hat"),
    C([-1, 19.6, -1], [2, 3, 2], "hat", rot=[0, 0, 12], pivot=[0, 19.6, 0]),
    C([-0.5, 22.4, -0.5], [1, 2, 1], "hat", rot=[0, 0, 30], pivot=[0, 19.6, 0]),
    C([-1, 10.5, -4.5], [2, 2, 2], "skin"),
    C([-3, 5.5, -3.5], [6, 4, 1], "beard"), C([-2.5, 9.4, -3.5], [5, 1, 1], "beard"), C([-2, 3.5, -3.6], [4, 2, 1], "beard"),
    C([-1.5, 1.8, -3.7], [3, 2, 1], "beard"),
    eyes(1.0, 11.0, -2.5, "eye", 1), pair(C([3, 10.5, -0.5], [1, 2, 2], "skin")))
add(bones, "arm_r", C([-5.5, 2.2, -3], [2, 2, 2], "mush"), C([-5.5, 0.5, -2.5], [1, 2, 1], "beard"))
add(bones, "body", C([-3, 9, 1.5], [6, 1, 1], "tunic"), C([-2, 1, 2], [4, 4, 1], "hat"))   # hood-tail cape scrap

SPEC = with_visible({
    "id": "gnome", "name": "Garden Gnome", "egg": ("#d43a3a", "#f6f6f2"), "glow": False, "scale": 0.75,
    "bones": bones,
    "skins": {"default": tunic, "tunic": tunic, "skin": skin, "hat": hat, "beard": beard, "boots": solid(BROWN, 0.2, 4),
              "boots2": solid("#3a2412", 0.2, 5), "eye": eye("#2a2a3a"), "mush": mushroom},
    "anims": biped_anims(walk_amp=42, arm_amp=30, freq=60),
    "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "passive", "health": 10, "speed": 0.28, "box": [0.45, 1.15], "family": ["gnome"],
        "spawn": {"biomes": ["forest", "taiga", "flower_forest"], "weight": 5, "herd": [1, 3]},
        "loot": [("minecraft:red_mushroom", 0, 2), ("minecraft:emerald", 0, 1), ("minecraft:string", 0, 1)],
        "sound": ("villager", [1.5, 1.7]),
    },
})
