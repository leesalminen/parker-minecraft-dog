"""Meadow Fairy - thumb-sized flutterer (0.4 blocks) with dragonfly wings and a glowing star wand."""
from eggsb_kit import *

SKIN, HAIR, DRESS, DRESS2 = "#ffe0cc", "#ff8fd0", "#b78cff", "#ff9ee0"

skin = coat(SKIN, dark="#f0c0aa", light="#fff0e6", seed=151, patch=2)

def face(p):
    c = skin(p)
    if p.face == "front" and p.fh >= 5 and p.y == 4 and p.x in (0, p.fw - 1) and p.fw >= 6: return "#ff9fa8"
    if p.face == "front" and p.y == 5 and 2 <= p.x <= p.fw - 3: return "#e0707a"
    return c

def hair(p):
    return shade(mix(HAIR, "#ffc0e8", noise3(*p.p, 153, 1.5)), 0.88 + 0.24 * hash01(p.x, p.y, p.fw, 1))

def dress(p):
    t = min(1.0, max(0.0, (p.p[1] - 3) / 8.0))
    c = mix(DRESS2, DRESS, t)
    return shade(c, 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 2))

def wingfn(p):
    x, y, z = p.p
    t = noise3(x * 0.7, y, z * 0.7, 155, 2.5)
    c = mix("#a8f0ff", "#ffb8f4", t)
    edge = p.x in (0, p.fw - 1) or p.y in (0, p.fh - 1)
    return glow(shade(c, 1.0 if edge else 0.82))

def star(p): return glow("#fff27a")
def stick(p): return "#e8c88a"

bones = biped(4, 5, 3, 4, 1, 1, 4, 1, 1, (6, 6, 6), skin="dress", head_skin="face", leg_skin="skin", arm_skin="skin",
              leg_x=1.0, arm_dx=0, shoulder_drop=1, hand_h=0)
add(bones, "body", C([-3, 4, -2.5], [6, 2, 5], "dress"), C([-4, 3, -3], [8, 1, 6], "dress"))
add(bones, "head",
    C([-3.5, 12.5, -3.5], [7, 2, 7], "hair"), C([-3.5, 9, 2], [7, 4, 2], "hair"), C([-1.5, 14.5, 0], [3, 3, 3], "hair"),
    pair(C([3, 10, -2], [1, 3, 2], "hair")),
    eyes(1.0, 10.0, -3, "eye", 2),
    pair(C([3, 9.5, -0.5], [1, 3, 1], "hair", rot=[0, 0, -20], pivot=[3, 9.5, 0])))
add(bones, "arm_r", C([-3.4, 3.5, -4], [1, 1, 4], "stick"), C([-3.9, 3, -5], [2, 2, 1], "star"), C([-3.4, 2.4, -5.2], [1, 3, 1], "star"))
wl = bone("wing_l", "body", [1, 8.5, 1.5], [
    C([1, 8.5, 1.5], [7, 1, 5], "wing"), C([2, 8.5, 6.5], [5, 1, 3], "wing"), C([1, 7.5, 1.5], [5, 1, 1], "wing")])
wr = bone("wing_r", "body", [-1, 8.5, 1.5], [mirror(c) for c in wl["cubes"]])
wl["rotation"] = [0, -12, -38]; wr["rotation"] = [0, 12, 38]
bones += [wl, wr]

anims = biped_anims(walk_amp=25, freq=80, body_bob=0.2)
anims["flap"] = anim(merge(
    {"wing_l": {"rotation": ["0", "-12", "-38 + math.sin(query.life_time * 1500) * 30"]},
     "wing_r": {"rotation": ["0", "12", "38 - math.sin(query.life_time * 1500) * 30"]}},
    bob("body", 0.6, 160), sway("arm_r", 15, 90, 0)))
anims["idle"]["bones"].update({"wing_l": {"rotation": ["0", "-12", "-38 + math.sin(query.life_time * 500) * 10"]},
                               "wing_r": {"rotation": ["0", "12", "38 - math.sin(query.life_time * 500) * 10"]}})
anims["walk"]["bones"].update({"wing_l": {"rotation": ["0", "-12", "-38 + math.sin(query.life_time * 500) * 10"]},
                               "wing_r": {"rotation": ["0", "12", "38 - math.sin(query.life_time * 500) * 10"]}})

SPEC = with_visible({
    "id": "fairy", "name": "Meadow Fairy", "egg": ("#ff8fd0", "#a8f0ff"), "glow": True, "scale": 0.45,
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "face": face, "hair": hair, "dress": dress, "wing": wingfn, "star": star, "stick": stick,
              "eye": eye("#5a8aff")},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "companion", "health": 6, "speed": 0.2, "fly": True, "fly_speed": 0.25, "box": [0.3, 0.45], "family": ["fairy"],
        "tame_items": ["minecraft:sugar", "minecraft:honey_bottle"],
        "spawn": {"biomes": ["flower_forest", "meadow", "forest"], "weight": 6, "herd": [1, 3]},
        "loot": [("minecraft:glowstone_dust", 0, 2), ("minecraft:sugar", 0, 2)],
        "sound": ("vex", [1.9, 2.0]),
    },
}, margin=0.8)
