"""Pegasus - winged steed, flies and can be ridden.  Storm-grey coat, dark blue mane, broad feathered wings."""
from eggsb_kit import *

GREY, MANE, WING, WING2 = "#c9d3e2", "#2c3a63", "#eef3fb", "#a9b9d6"

def feather(p):
    x, y, z = p.p
    c = mix(WING2, WING, 0.35 + 0.65 * noise3(x * 0.5, y, z * 1.4, 21, 2.0))
    if abs(math.sin(x * 1.3)) > 0.93: c = shade(c, 0.86)   # feather quills
    return shade(c, 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 4))

def mane(p):
    return shade(mix(MANE, "#5a72b8", noise3(*p.p, 13, 1.6)), 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 9))

def hoof(p):
    return shade("#3b4257", 0.9 + 0.2 * noise3(*p.p, 19, 1))

coat_fn = coat(GREY, dark="#9eabc4", light="#e6ecf6", under="#e2e8f3", under_y=14, seed=31, patch=3.5)

bones = quad(10, 10, 20, 14, 3, (6, 7, 8), 22, head_dz=-1, skin="coat", foot_h=2, foot_skin="hoof", neck=(6, 12, 38))
add(bones, "head", C([-2.5, 22.5, -19], [5, 4, 4], "muzzle"), side_eyes(3, 25.5, -14.5),
    pair(C([1.5, 29, -8], [2, 4, 2], "coat")), pair(C([1.9, 29.6, -7.6], [1, 2, 1], "ear_in")),
    C([-1, 28, -10], [2, 3, 4], "mane"), C([-1, 22, -6], [2, 12, 3], "mane", rot=[38, 0, 0], pivot=[0, 21, -8]),
    C([-1, 23, -4], [2, 3, 3], "mane"))
bones.append(bone("tail", "body", [0, 22, 10], [
    C([-1.5, 12, 10], [3, 12, 3], "mane"), C([-2, 5, 11], [2, 8, 2], "mane"), C([0, 4, 11], [2, 9, 2], "mane")]))
bones.append(wing("wing_l", "body", 1, 4, 24, -3, 20, 8, "coat", "feather", "feather", fingers=4))
bones.append(wing("wing_r", "body", -1, 4, 24, -3, 20, 8, "coat", "feather", "feather", fingers=4))
add(bones, "wing_l", C([12, 23.5, 12], [8, 1, 4], "feather")); add(bones, "wing_r", mirror(C([12, 23.5, 12], [8, 1, 4], "feather")))

anims = quad_anims(tail="tail", tail_amp=12)
anims["flap"] = flap_anim("wing_l", "wing_r", amp=38, rate=320,
                          extra=merge(sway("tail", 6, 60, 1), {"leg_fl": {"rotation": ["-20", "0", "0"]}, "leg_fr": {"rotation": ["-20", "0", "0"]},
                                                              "leg_bl": {"rotation": ["15", "0", "0"]}, "leg_br": {"rotation": ["15", "0", "0"]}}))
anims["idle"]["bones"].update(fold("wing_l", "wing_r", 62))
anims["walk"]["bones"].update(fold("wing_l", "wing_r", 62))

SPEC = with_visible({
    "id": "pegasus", "name": "Pegasus", "egg": ("#c9d3e2", "#2c3a63"), "glow": False, "scale": 1.0,
    "bones": bones,
    "skins": {"default": coat_fn, "coat": coat_fn, "muzzle": face_detail(coat("#b7a9b8", seed=4)),
              "hoof": hoof, "mane": mane, "feather": feather, "eye": eye("#4a70d0"),
              "ear_in": lambda p: "#e8b8c8" if p.face == "front" else shade(GREY, 0.95)},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "companion", "health": 30, "speed": 0.3, "fly": True, "fly_speed": 0.4, "box": [1.2, 1.9],
        "family": ["pegasus", "horse"], "ride": {"seats": [[0, 1.5, 0.1]]},
        "tame_items": ["minecraft:golden_apple", "minecraft:golden_carrot", "minecraft:wheat"],
        "spawn": {"biomes": ["extreme_hills", "meadow", "savanna"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:feather", 1, 3), ("minecraft:leather", 0, 1)],
        "sound": ("horse", [0.9, 1.1]),
    },
})
