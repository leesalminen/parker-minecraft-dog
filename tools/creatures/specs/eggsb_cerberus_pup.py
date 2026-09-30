"""Cerberus Pup - three-headed hellhound puppy with a smouldering tail.  Fire immune, tameable with bones."""
from eggsb_kit import *

FUR, EMBER = "#3a2a2a", "#ff7a1a"

def cracks(p, c):
    x, y, z = p.p
    if p.bone == "body" and p.face in ("east", "west", "top") and abs(math.sin(z * 1.2 + y * 0.5)) > 0.94: return glow(EMBER)
    if hash01(int(x), int(y), int(z), 121) > 0.985: return glow("#ffb02a")

fur = coat(FUR, dark="#241818", light="#5a4040", under="#6a4a3a", seed=121, patch=2.5, extra=cracks)

def snout(p):
    c = coat("#6a4a3a", dark="#4a3028", seed=123)(p)
    if p.face == "front" and p.y == 0 and 0 < p.x < p.fw - 1: return "#141010"
    return c

def eyes_ember(p): return glow("#ff6a1a")
def tongue(p): return "#e85a6a"
def collar(p):
    return "#bcbcc4" if (p.x + p.y) % 2 == 0 else "#7c7c88"
def tailflame(p): return glow(mix("#ff5a10", "#ffd23a", noise3(*p.p, 125, 1.0)))

bones = quad(6, 6, 10, 5, 3, (5, 5, 5), 8, head_dz=0, skin="fur", foot_h=1, foot_skin="claw", leg_ld=3)

def head_bone(name, x, yaw, roll):
    cx = x
    return bone(name, "body", [cx, 9, -5], [
        C([cx - 2.5, 8, -10], [5, 5, 5], "fur", rot=[0, yaw, roll], pivot=[cx, 9, -5]),
        C([cx - 1.5, 8, -13], [3, 2, 3], "snout", rot=[0, yaw, roll], pivot=[cx, 9, -5]),
        C([cx - 1, 7, -12.5], [2, 1, 1], "tongue", rot=[0, yaw, roll], pivot=[cx, 9, -5]),
        C([cx + 1.0, 10.6, -10.4], [1, 1, 1], "eyem", rot=[0, yaw, roll], pivot=[cx, 9, -5]),
        C([cx - 2.0, 10.6, -10.4], [1, 1, 1], "eyem", rot=[0, yaw, roll], pivot=[cx, 9, -5]),
        C([cx + 2, 12, -8.5], [2, 3, 2], "ear", rot=[0, yaw, roll - 25], pivot=[cx, 9, -5]),
        C([cx - 4, 12, -8.5], [2, 3, 2], "ear", rot=[0, yaw, roll + 25], pivot=[cx, 9, -5])])

# centre head goes through quad()'s head bone so it follows look-at
by(bones, "head")["cubes"] = [
    C([-2.5, 8, -10], [5, 5, 5], "fur"), C([-1.5, 8, -13], [3, 2, 3], "snout"), C([-1, 7, -12.5], [2, 1, 1], "tongue"),
    C([1.0, 10.6, -10.4], [1, 1, 1], "eyem"), C([-2.0, 10.6, -10.4], [1, 1, 1], "eyem"),
    C([2, 12, -8.5], [2, 3, 2], "ear", rot=[0, 0, -25], pivot=[2, 12, -8.5]), C([-4, 12, -8.5], [2, 3, 2], "ear", rot=[0, 0, 25], pivot=[-2, 12, -8.5]),
    C([-3, 6, -8], [6, 2, 4], "collar")]
bones.insert(2, head_bone("head_l", 5, 18, -8)); bones.insert(3, head_bone("head_r", -5, -18, 8))
add(bones, "body", C([-2.5, 11, -4], [5, 2, 2], "collar"))
bones.append(bone("tail", "body", [0, 10, 5], [C([-1, 8, 5], [2, 2, 4], "fur", rot=[-30, 0, 0], pivot=[0, 9, 5]),
                                             C([-1.5, 10, 8.5], [3, 3, 3], "flame", rot=[-30, 0, 0], pivot=[0, 9, 5]),
                                             C([-0.5, 12.5, 9], [1, 3, 2], "flame", rot=[-30, 0, 0], pivot=[0, 9, 5])]))

anims = quad_anims(tail="tail", tail_amp=25, walk_amp=45, freq=50)
anims["idle"]["bones"].update({"head_l": {"rotation": ["math.sin(query.life_time * 55) * 5", "math.sin(query.life_time * 40) * 10", "0"]},
                               "head_r": {"rotation": ["math.sin(query.life_time * 61) * 5", "-math.sin(query.life_time * 37) * 10", "0"]}})
anims["walk"]["bones"].update({"head_l": {"rotation": ["math.sin(query.modified_distance_moved * 50) * 6", "0", "0"]},
                               "head_r": {"rotation": ["math.sin(query.modified_distance_moved * 50 + 3) * 6", "0", "0"]}})

SPEC = with_visible({
    "id": "cerberus_pup", "name": "Cerberus Pup", "egg": ("#3a2a2a", "#ff7a1a"), "glow": True, "scale": 1.0,
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "snout": snout, "tongue": tongue, "eyem": eyes_ember, "ear": solid("#241818", 0.2, 5),
              "collar": collar, "claw": solid("#141010", 0.2, 7), "flame": tailflame},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "companion", "health": 24, "speed": 0.32, "box": [0.8, 0.85], "fire_immune": True, "family": ["cerberus", "dog"],
        "tame_items": ["minecraft:bone", "minecraft:cooked_beef", "minecraft:cooked_porkchop"],
        "spawn": {"biomes": ["desert", "mesa", "extreme_hills"], "weight": 2, "herd": [1, 2]},
        "loot": [("minecraft:bone", 1, 3), ("minecraft:blaze_powder", 0, 1), ("minecraft:coal", 0, 2)],
        "sound": ("wolf", [0.8, 1.0]),
    },
})
