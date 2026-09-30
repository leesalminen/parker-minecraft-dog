"""Baby Dragon - chubby, big-eyed hatchling with stubby wings.  Tameable with raw fish or meat."""
from eggsb_kit import *

TEAL, CREAM, HORN, MEMB = "#3fb0a0", "#f8e7b8", "#f4d68a", "#b878d8"

def belly(p, c):
    if p.face == "bottom" or (p.bone == "body" and p.face == "front"): return None
    if p.bone in ("body", "head", "tail0", "tail1") and p.face != "top" and p.p[1] < 6.3 + (1.5 if p.bone == "head" else 0): return None

hide = scales(TEAL, dark="#2a8a80", light="#63d0bc", cell=1.8, under=CREAM, seed=141)

def belly_plates(p):
    if p.face == "bottom": return mix(CREAM, "#e8cf94", 0.5 if p.y % 2 else 0.0)
    return hide(p)

def spine(p): return mix("#f0a040", "#ffd070", hash01(p.x, p.y, p.fw, 1))
def horn(p): return shade(HORN, 0.85 + 0.25 * hash01(p.x, p.y, p.fw, 2))
def memb(p):
    c = mix("#b878d8", "#e6a0f0", noise3(*p.p, 143, 1.5))
    return shade(c, 0.85) if (p.x % 3 == 0 and p.face in ("top", "bottom")) else c
def snout(p):
    c = hide(p)
    if p.face == "front" and p.y == 0 and p.x in (1, p.fw - 2): return "#1a3a38"
    return c

bones = quad(7, 6, 9, 4, 3, (8, 7, 7), 6, head_dz=0, skin="hide", foot_h=1, foot_skin="claw", leg_ld=3)
by(bones, "head")["pivot"] = [0, 8, -4.5]
bones[0]["cubes"][0]["skin"] = "belly"
add(bones, "head",
    C([-2, 6.5, -12.5], [4, 3, 3], "snout"), eyes(1.0, 9.5, -9.5, "eye", 3),
    pair(C([2.5, 13, -8], [1, 3, 1], "horn", rot=[-25, 0, -10], pivot=[3, 13, -7])),
    pair(C([3.5, 9, -6], [1, 3, 2], "wingfin", rot=[0, 0, 0])),
    C([-1, 13.5, -10], [2, 1, 3], "spine"), C([-1, 13.5, -6.5], [2, 1, 2], "spine"))
for i in range(4):
    add(bones, "body", C([-0.5, 10, -3 + i * 2.5], [1, 2, 1], "spine"))
bones.append(bone("tail0", "body", [0, 7, 4.5], [C([-2, 5, 4.5], [4, 4, 5], "hide")]))
bones.append(bone("tail1", "tail0", [0, 6.5, 9.5], [C([-1.5, 5, 9.5], [3, 3, 5], "hide"), C([-0.5, 8, 10], [1, 2, 2], "spine")]))
bones.append(bone("tail2", "tail1", [0, 6.5, 14.5], [C([-1, 5.5, 14.5], [2, 2, 5], "hide"), C([-1, 4.5, 19.5], [2, 4, 1], "spine")]))
bones.append(wing("wing_l", "body", 1, 3, 10, -1, 8, 6, "hide", "memb", None, fingers=2))
bones.append(wing("wing_r", "body", -1, 3, 10, -1, 8, 6, "hide", "memb", None, fingers=2))

anims = quad_anims(tail=None, walk_amp=40, freq=50)
for a in ("walk", "idle"):
    anims[a]["bones"].update(merge(sway("tail0", 10, 60, 1), sway("tail1", 14, 60, 1, 0.8), sway("tail2", 18, 60, 1, 1.6),
                                   fold("wing_l", "wing_r", 30, 14, 200)))
anims["idle"]["bones"].update({"head": {"rotation": ["math.sin(query.life_time * 50) * 5", "math.sin(query.life_time * 29) * 10", "math.sin(query.life_time * 41) * 4"]}})

SPEC = with_visible({
    "id": "baby_dragon", "name": "Baby Dragon", "egg": ("#3fb0a0", "#f0a040"), "glow": False, "scale": 1.0,
    "bones": bones,
    "skins": {"default": hide, "hide": hide, "belly": belly_plates, "snout": snout, "spine": spine, "horn": horn, "memb": memb,
              "wingfin": lambda p: shade(TEAL, 0.9), "claw": solid("#f4e8c8", 0.15, 5), "eye": eye("#ffb020", pupil="#1a1008")},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "companion", "health": 20, "speed": 0.3, "box": [0.7, 0.85], "family": ["dragon"],
        "tame_items": ["minecraft:cod", "minecraft:salmon", "minecraft:beef"],
        "spawn": {"biomes": ["extreme_hills", "taiga"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:gunpowder", 0, 1), ("minecraft:string", 0, 2)],
        "sound": ("dragon", [1.9, 2.0]),
    },
})
