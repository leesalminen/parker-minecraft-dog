"""Moss Golem - squat, ancient garden guardian overgrown with moss and wildflowers.  Tameable pet."""
from eggsb_kit import *

STONE, MOSS = "#8d8f84", "#4f8a34"

def growth(p, c):
    x, y, z = p.p
    m = noise3(x, y * 0.8, z, 211, 3.0) + (0.25 if p.face == "top" else 0) + (y / 120)
    if m > 0.72: return mix(c, mix("#3e7a2a", "#7ab648", noise3(*p.p, 213, 0.8)), 0.9)
    if hash01(int(x), int(y), int(z), 215) > 0.985: return "#d6e8b0"

rock = coat(STONE, dark="#6a6c62", light="#b0b2a4", seed=211, patch=2.5, extra=growth)

def leaf(p): return shade(mix("#3e8a2a", "#86c850", noise3(*p.p, 217, 0.9)), 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 4))
def flower(col): return lambda p: col if p.face == "top" or p.fh < 2 else shade(col, 0.8)
def wood(p): return shade(mix("#6a4a2a", "#8a6a3a", noise3(*p.p, 219, 1.0)), 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 3))
def eyef(p): return "#f4e8a0" if p.face == "front" else "#3a3a30"

bones = biped(14, 10, 9, 5, 5, 5, 12, 5, 5, (7, 6, 7), skin="rock", leg_x=3.6, head_dy=-1, head_dz=-1, hand_h=4, hand_skin="rock2",
              arm_dx=0, shoulder_drop=2, foot_h=1, foot_skin="rock2")
add(bones, "head", eyes(1.0, 11.4, -4.5, "eye", 1), C([-2, 9.6, -4.5], [4, 1, 1], "rock2"),
    C([-3, 15, -3], [6, 3, 6], "leaf"), C([-1, 17.5, -1], [3, 2, 3], "leaf"), C([0, 19, 1], [1, 2, 1], "pink"),
    C([-2, 17.4, -2], [1, 2, 1], "yellow"))
add(bones, "body",
    C([-4, 15, -3], [8, 3, 6], "rock"), C([-6, 14, -2], [4, 3, 5], "leaf"), C([3, 14, -3], [4, 3, 5], "leaf"),
    C([-5, 17, 0], [1, 2, 1], "yellow"), C([4, 17, -1], [1, 2, 1], "pink"), C([2, 18, 1], [1, 2, 1], "white"),
    C([-3, 14.5, 3.2], [1, 5, 1], "leaf"), C([0, 12, 4.4], [1, 6, 1], "leaf"), C([2, 13, 4.4], [2, 1, 1], "leaf"),
    C([-3, 9, -4.6], [6, 4, 1], "rock2"))     # worn chest plate
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    add(bones, n_, C([sx * 7.5 - 2.5, 12, -2.5], [5, 2, 5], "leaf"), C([sx * 7.5 - 0.5, 14, 0], [1, 2, 1], "white" if sx > 0 else "yellow"))

anims = biped_anims(walk_amp=22, arm_amp=16, freq=28, body_bob=0.4,
                    extra_idle={"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 22) * 14", "0"]}})

SPEC = with_visible({
    "id": "moss_golem", "name": "Moss Golem", "egg": ("#8d8f84", "#4f8a34"), "glow": False, "scale": 1.2,
    "bones": bones,
    "skins": {"default": rock, "rock": rock, "rock2": solid("#77796e", 0.25, 6), "leaf": leaf, "yellow": flower("#f6d838"),
              "pink": flower("#f078b8"), "white": flower("#f8f8f0"), "eye": eyef},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "companion", "health": 70, "speed": 0.2, "box": [1.3, 1.5], "knockback_resist": 0.7, "family": ["golem"],
        "tame_items": ["minecraft:moss_block", "minecraft:vine", "minecraft:poppy", "minecraft:dandelion"],
        "spawn": {"biomes": ["forest", "swamp", "jungle", "flower_forest"], "weight": 3, "herd": [1, 1]},
        "loot": [("minecraft:moss_block", 1, 3), ("minecraft:vine", 0, 3), ("minecraft:poppy", 0, 2), ("minecraft:cobblestone", 0, 3)],
        "sound": ("golem", [0.75, 0.9]),
    },
})
