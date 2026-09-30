"""Centaur - chestnut horse body with a human archer's torso.  Keeps to itself, shoots back when provoked."""
from eggsb_kit import *

COAT, MANE, SKINC = "#8a4a26", "#2a1a12", "#d8a078"

coat_fn = coat(COAT, dark="#623418", light="#a86a3a", under="#a87a4c", seed=281, patch=3)
skin = coat(SKINC, dark="#b8825c", light="#f0bc94", seed=283, patch=2)

def face(p):
    c = skin(p)
    if p.face == "front" and p.y == p.fh - 1 and 1 < p.x < p.fw - 2: return "#9a5a4a"
    return c

def hair(p): return shade(mix(MANE, "#5a3a24", noise3(*p.p, 285, 1.5)), 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 3))
def hoof(p): return shade("#1c1612", 0.9 + 0.2 * noise3(*p.p, 287, 1.0))
def leather(p): return shade("#5a3a20", 0.85 + 0.3 * noise3(*p.p, 289, 1.0))
def wood(p): return shade("#7a5228", 0.9 + 0.2 * noise3(*p.p, 291, 1.0))
def string(p): return "#e8e0d0"
def feather(p): return "#e8e4d8" if p.y % 2 else "#c84a3a"
def tunic(p): return shade(mix("#3a6a4a", "#2c5a3a", noise3(*p.p, 293, 1.5)), 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 1))

bones = quad(9, 9, 18, 13, 3, (5, 6, 5), 30, skin="coat", foot_h=2, foot_skin="hoof", leg_ld=3)
bones.remove(by(bones, "head"))
bones.append(bone("torso", "body", [0, 22, -6], [C([-4, 22, -9], [8, 10, 5], "skin"), C([-4, 22, -9.5], [8, 3, 6], "leather"),
                                                C([-4.2, 27, -9.4], [8, 5, 1], "tunic"), C([-2, 22.5, -3.4], [4, 8, 2], "leather"),
                                                C([-1.5, 30, -3.4], [1, 5, 1], "feather"), C([0.5, 30, -3.4], [1, 4, 1], "feather"), C([-0.5, 31, -3.4], [1, 5, 1], "feather")]))
bones.append(bone("head", "torso", [0, 32, -6.5], [C([-2.5, 32, -9], [5, 6, 5], "face"), C([-2.5, 37.4, -9.2], [5, 1, 5], "hair"), C([-3, 35, -8.8], [6, 3, 6], "hair"),
                                                 C([-2.5, 32, -4.2], [5, 6, 2], "hair"), C([-1, 26, -3.8], [2, 6, 2], "hair"),
                                                 eyes(0.8, 34.4, -9, "eye", 1), C([-0.5, 33.2, -9.6], [1, 1, 1], "skin"),
                                                 pair(C([2.5, 33.5, -7], [1, 2, 1], "skin"))]))
for nm, s in (("l", 1), ("r", -1)):
    bones.append(bone(f"arm_{nm}", "torso", [s * 5.5, 31, -6.5], [C([s * 5.5 - 1.5, 22, -8.5], [3, 10, 3], "skin"), C([s * 5.5 - 1.5, 30, -8.5], [3, 2, 3], "leather")]))
add(bones, "arm_l", C([6.6, 22, -14], [1, 13, 1], "wood"), C([6.6, 34, -14.2], [1, 2, 3], "wood", rot=[-20, 0, 0], pivot=[7, 34, -13]),
    C([6.7, 22, -14.6], [1, 1, 1], "wood"), C([7.1, 23, -14.2], [1, 11, 1], "string"))
bones.append(bone("tail", "body", [0, 20, 9], [C([-1.5, 8, 9], [3, 14, 3], "hair"), C([-2, 3, 10], [2, 6, 2], "hair"), C([0, 4, 10], [2, 5, 2], "hair")]))
add(bones, "body", C([-1, 22, -5.5], [2, 3, 6], "hair"))     # mane blends into the back

anims = quad_anims(tail="tail", tail_amp=12, walk_amp=36, freq=34, head_bob=False)
anims["idle"]["bones"].update(merge({"head": {"rotation": ["math.sin(query.life_time * 60) * 3", "math.sin(query.life_time * 31) * 10", "0"]}},
                                    sway("arm_r", 4, 55, 0)))
anims["walk"]["bones"].update(swing({"arm_r": 0}, amp=10, axis=0, freq=34))

SPEC = with_visible({
    "id": "centaur", "name": "Centaur", "egg": ("#8a4a26", "#d8a078"), "glow": False, "scale": 1.05,
    "bones": bones,
    "skins": {"default": coat_fn, "coat": coat_fn, "skin": skin, "face": face, "hair": hair, "hoof": hoof, "leather": leather, "wood": wood,
              "string": string, "feather": feather, "tunic": tunic, "eye": eye("#3a2a10")},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "neutral", "health": 40, "speed": 0.32, "damage": 4, "box": [1.2, 2.4], "family": ["centaur"],
        "ranged": True, "range": 18, "projectile": "minecraft:arrow",
        "spawn": {"biomes": ["plains", "savanna", "forest"], "weight": 3, "herd": [1, 2]},
        "loot": [("minecraft:arrow", 1, 4), ("minecraft:leather", 0, 2), ("minecraft:stick", 1, 3), ("minecraft:feather", 0, 2)],
        "sound": ("horse", [0.8, 0.95]),
    },
})
