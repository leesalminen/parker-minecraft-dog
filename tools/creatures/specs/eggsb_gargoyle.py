"""Stone Gargoyle - crouching winged sentinel carved from gargoyle-grey stone with smouldering red eyes."""
from eggsb_kit import *

STONE = "#8a8e96"

def crack(p, c):
    x, y, z = p.p
    n = noise3(x * 0.55, y * 0.55, z * 0.55, 173, 1.0)
    if abs(n - 0.5) < 0.02: return shade(c, 0.5)
    if p.face == "top" and noise3(x, y, z, 175, 2.5) > 0.66: return mix(c, "#5f8a4a", 0.7)    # moss on horizontal surfaces

stone = coat(STONE, dark="#666a74", light="#aeb2ba", seed=171, patch=2.2, extra=crack)

def horn(p): return shade(mix("#4a4e58", "#6a6e78", noise3(*p.p, 177, 1.0)), 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 1))
def wingm(p):
    c = stone(p)
    return shade(c, 0.8) if (p.face in ("top", "bottom")) else c
def eyefn(p): return glow("#ff3a2a")
def fang(p): return "#e8e4d8"

def face(p):
    c = stone(p)
    if p.face == "front" and p.fw >= 6 and p.y == p.fh - 1 and p.x in (1, 2, p.fw - 3, p.fw - 2): return "#e8e4d8"
    return c

bones = biped(8, 8, 5, 7, 3, 4, 9, 3, 3, (7, 6, 6), skin="stone", head_skin="face", head_dy=-1, head_dz=-1.5, hand_h=2, hand_skin="horn",
              foot_h=2, foot_skin="horn", leg_x=2.2)
add(bones, "head",
    eyes(0.8, 13.6, -4.5, "eye", 2), C([-1.5, 11.8, -6.5], [3, 2, 2], "stone"),
    pair(C([2, 20, -1.5], [2, 3, 2], "horn", rot=[-15, 0, -15], pivot=[2.5, 19, -1])),
    pair(C([3.5, 22, -1.5], [2, 3, 2], "horn", rot=[-15, 0, -40], pivot=[2.5, 19, -1])),
    pair(C([3.5, 15, -2], [2, 3, 2], "stone", rot=[0, 0, -25], pivot=[3.5, 16, -1])),
    C([-3.5, 19, -6.5], [7, 1, 2], "horn"))
add(bones, "body", C([-4, 14, -2.5], [8, 2, 5], "stone"), C([-2, 10, -3], [4, 3, 1], "horn"),
    *[C([-0.5, 8 + i * 2.6, 2.5], [1, 2, 2], "horn") for i in range(4)])
bones.append(bone("tail", "body", [0, 8, 2.5], [C([-1, 6, 2.5], [2, 2, 6], "stone"), C([-1, 5, 8], [2, 2, 4], "stone"), C([-2, 3.5, 12], [4, 4, 1], "horn"),
                                              C([-1, 4.5, 11.5], [2, 2, 1], "horn")]))
bones.append(bat_wing("wing_l", "body", 1, 4, 14, 2, 14, 10, "horn", "wingm"))
bones.append(bat_wing("wing_r", "body", -1, 4, 14, 2, 14, 10, "horn", "wingm"))
bones[-2]["rotation"] = [0, -6, 0]; bones[-1]["rotation"] = [0, 6, 0]

anims = biped_anims(walk_amp=30, arm_amp=28, freq=34, body_bob=0.4,
                    extra_idle=merge(sway("tail", 6, 40, 1)))
for a in ("idle", "walk"):
    anims[a]["bones"].update(fold("wing_l", "wing_r", 55 if a == "idle" else 40, 3, 60))
anims["attack"] = anim(merge({"body": {"rotation": ["math.sin(variable.attack_time * 180) * 24", "0", "0"]},
                              "head": {"rotation": ["math.sin(variable.attack_time * 180) * 14", "0", "0"]}}), loop=False)

SPEC = with_visible({
    "id": "gargoyle", "name": "Stone Gargoyle", "egg": ("#8a8e96", "#ff3a2a"), "glow": True, "scale": 1.15,
    "bones": bones,
    "skins": {"default": stone, "stone": stone, "face": face, "horn": horn, "wingm": wingm, "eye": eyefn},
    "anims": anims, "play": PLAY_WALK_IDLE + ["attack"],
    "behavior": {
        "role": "hostile", "health": 44, "speed": 0.26, "damage": 7, "box": [1.0, 1.9], "knockback_resist": 0.5, "family": ["gargoyle"],
        "xp": 15,
        "spawn": {"biomes": ["extreme_hills", "mesa", "taiga"], "weight": 4, "herd": [1, 1]},
        "loot": [("minecraft:cobblestone", 1, 4), ("minecraft:flint", 0, 2), ("minecraft:iron_nugget", 0, 3), ("minecraft:redstone", 0, 2)],
        "sound": ("golem", [0.9, 1.0]),
    },
})
