"""Jackalope - a hopping rabbit with a stag's antlers.  Shy, skittish, drops rabbit hide."""
from eggsb_kit import *

FUR, BELLY, ANTLER = "#a87a4c", "#f4e8d4", "#e8d8b0"

def antler(p):
    return shade(mix(ANTLER, "#b8a070", noise3(*p.p, 131, 1.0) * 0.8), 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 3))

def extra(p, c):
    if p.bone == "head" and p.face == "front" and p.fw >= 4 and p.y == 1 and p.x in (1, p.fw - 2): return None
    if p.bone in ("body",) and abs(p.p[0]) < 1.1 and p.p[2] < -3.5: return BELLY   # white blaze on chest

fur = coat(FUR, dark="#7d5632", light="#c89a66", under=BELLY, seed=131, patch=2, extra=extra)

def ear(p):
    if p.face == "front" and 0 < p.x < p.fw - 1: return "#e8a8a8"
    return fur(p)

bones = quad(5, 5, 9, 4, 2, (4, 4, 5), 6, head_dz=0, skin="fur", foot_h=0, leg_ld=2)
by(bones, "head")["pivot"] = [0, 8, -4.5]
for nm in ("bl", "br"):
    b = by(bones, f"leg_{nm}"); x = b["pivot"][0]
    b["pivot"] = [x, 5, 3]
    b["cubes"] = [C([x - 1.5, 1, 1], [3, 4, 5], "fur"), C([x - 1, 0, -3], [2, 1, 6], "fur")]
add(bones, "head",
    C([-1, 6.5, -8.6], [2, 2, 1], "fur"), C([-0.5, 7.6, -9.2], [1, 1, 1], "nose"), eyes(1.0, 8.0, -7.5, "eye", 1),
    pair(C([0.8, 10, -3.5], [1, 6, 2], "ear", rot=[-8, 0, 8], pivot=[1.3, 10, -3])),
    pair(C([1.6, 10, -5], [1, 4, 1], "antler", rot=[0, 0, -18], pivot=[1.6, 10, -5])),
    pair(C([2.6, 12.6, -5], [1, 3, 1], "antler", rot=[0, 0, -42], pivot=[1.6, 10, -5])),
    pair(C([2.4, 11.2, -5], [1, 1, 3], "antler", rot=[0, -20, -18], pivot=[1.6, 10, -5])),
    pair(C([2.0, 6.5, -6], [1, 2, 2], "fur")))
bones.append(bone("tail", "body", [0, 7, 4.5], [C([-1.5, 4.5, 4.5], [3, 3, 3], "puff")]))

hop = lambda a: f"math.abs(math.sin(query.modified_distance_moved * 40)) * {a}"
anims = {
    "walk": anim(merge(
        {"leg_bl": {"rotation": ["math.sin(query.modified_distance_moved * 40 + 1.2) * 50 * query.modified_move_speed * 2", "0", "0"]},
         "leg_br": {"rotation": ["math.sin(query.modified_distance_moved * 40 + 1.2) * 50 * query.modified_move_speed * 2", "0", "0"]},
         "leg_fl": {"rotation": ["math.sin(query.modified_distance_moved * 40) * -40 * query.modified_move_speed * 2", "0", "0"]},
         "leg_fr": {"rotation": ["math.sin(query.modified_distance_moved * 40) * -40 * query.modified_move_speed * 2", "0", "0"]},
         "body": {"position": ["0", hop(2.5), "0"], "rotation": ["math.sin(query.modified_distance_moved * 40) * -10", "0", "0"]},
         "head": {"rotation": ["math.sin(query.modified_distance_moved * 40) * 8", "0", "0"]}},
        sway("tail", 6, 120, 0))),
    "idle": anim(merge(bob("body", 0.2, 70), sway("tail", 8, 45, 2),
                       {"head": {"rotation": ["math.sin(query.life_time * 70) * 4", "math.sin(query.life_time * 30) * 14", "0"]}},
                       {"leg_bl": {"rotation": ["0", "0", "0"]}})),
}

SPEC = with_visible({
    "id": "jackalope", "name": "Jackalope", "egg": ("#a87a4c", "#e8d8b0"), "glow": False, "scale": 1.0,
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "ear": ear, "antler": antler, "nose": solid("#e08a8a", 0.1, 4), "puff": solid("#f8f0e0", 0.2, 5),
              "eye": eye("#8a3a2a")},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "passive", "health": 8, "speed": 0.36, "box": [0.5, 0.6], "family": ["jackalope", "rabbit"],
        "spawn": {"biomes": ["plains", "savanna", "meadow"], "weight": 8, "herd": [1, 3]},
        "loot": [("minecraft:rabbit_hide", 0, 2), ("minecraft:rabbit", 0, 1), ("minecraft:rabbit_foot", 0, 1)],
        "sound": ("fox", [1.5, 1.8]),
    },
})
