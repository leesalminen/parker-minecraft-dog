"""Griffin - eagle head, wings and talons on a lion's body.  Flies; can be ridden."""
from eggsb_kit import *

FUR, FUR_D, FEA, FEA_D, WHITE, BEAK, TALON = "#c8964a", "#8f6428", "#7a4a26", "#4b2c16", "#f4ecd8", "#f2b632", "#3a2f22"

def fur(p):
    return coat(FUR, dark=FUR_D, light="#e6bb70", under="#efd9a5", seed=41, patch=3)(p)

def plum(p):
    x, y, z = p.p
    c = mix(FEA_D, FEA, 0.3 + 0.7 * noise3(x * 0.7, y * 0.7, z * 1.3, 43, 2.0))
    if abs(math.sin(z * 1.1 + x * 0.3)) > 0.9: c = shade(c, 0.8)
    return shade(c, 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 6))

def head_f(p):
    y = p.p[1]
    c = mix(WHITE, "#d9cfb6", noise3(*p.p, 47, 1.5))
    return shade(c, 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 8))

def beak(p):
    c = mix(BEAK, "#b98416", noise3(*p.p, 49, 1.2)) if p.face != "bottom" else shade(BEAK, 0.7)
    if p.face == "front" and p.fw >= 2 and p.y == 0 and p.x in (0, p.fw - 1): return "#3a2a08"
    return c

def talon(p):
    return shade(TALON, 0.9 + 0.3 * noise3(*p.p, 51, 1))

bones = quad(9, 9, 18, 10, 4, (6, 6, 6), 17, head_dz=-1, skin="fur", foot_h=0, neck=(6, 6, 20), head_skin="head")
# eagle forelegs: feathered with big talons
for nm, s in (("fl", 1), ("fr", -1)):
    b = by(bones, f"leg_{nm}")
    x = s * 3.5
    b["cubes"] = [C([x - 2, 3, -9], [4, 7, 4], "plum"), C([x - 2, 0, -10], [4, 2, 5], "talon"),
                  C([x - 2, 0, -12], [1, 2, 2], "talon"), C([x - 0.5, 0, -12], [1, 2, 2], "talon"), C([x + 1, 0, -12], [1, 2, 2], "talon")]
for nm in ("bl", "br"):   # lion hind paws
    b = by(bones, f"leg_{nm}")
    x = b["pivot"][0]
    b["cubes"] = [C([x - 2, 0, 5], [4, 10, 4], "fur"), C([x - 2, 0, 3], [4, 2, 2], "talon")]
add(bones, "head",
    C([-1.5, 17.5, -17.5], [3, 3, 4], "beak"), C([-1, 16.5, -17.9], [2, 1, 3], "beak"), C([-1, 20.5, -18], [2, 1, 2], "beak"),
    eyes(1.5, 20.5, -14.5, "eye", 1),
    C([-3.5, 22, -12], [7, 2, 4], "plum"), C([-2, 24, -10], [4, 2, 3], "plum"),
    C([-4, 13, -10], [8, 5, 4], "plum", rot=[10, 0, 0], pivot=[0, 14, -8]))
bones.append(bone("tail", "body", [0, 16, 9], [C([-1, 13, 9], [2, 3, 9], "fur", rot=[-20, 0, 0], pivot=[0, 16, 9]),
                                              C([-2, 8, 16], [4, 5, 5], "plum")]))
bones.append(wing("wing_l", "body", 1, 4, 19, -3, 22, 8, "fur", "plum", "plum", fingers=4))
bones.append(wing("wing_r", "body", -1, 4, 19, -3, 22, 8, "fur", "plum", "plum", fingers=4))

anims = quad_anims(tail="tail", tail_amp=10)
anims["flap"] = flap_anim("wing_l", "wing_r", amp=40, rate=300)
anims["idle"]["bones"].update(fold("wing_l", "wing_r", 55))
anims["walk"]["bones"].update(fold("wing_l", "wing_r", 55))

SPEC = with_visible({
    "id": "griffin", "name": "Griffin", "egg": ("#7a4a26", "#f2b632"), "glow": False, "scale": 1.1,
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "plum": plum, "head": head_f, "beak": beak, "talon": talon,
              "eye": eye("#f2c020", pupil="#101010")},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "mount", "health": 50, "speed": 0.28, "fly": True, "fly_speed": 0.38, "damage": 6, "box": [1.4, 1.6],
        "knockback_resist": 0.2, "family": ["griffin"], "ride": {"seats": [[0, 1.3, 0.1]]},
        "spawn": {"biomes": ["extreme_hills", "savanna"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:feather", 2, 4), ("minecraft:leather", 0, 2), ("minecraft:beef", 0, 2)],
        "sound": ("phantom", [1.0, 1.2]),
    },
})
