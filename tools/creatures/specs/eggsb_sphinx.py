"""Desert Sphinx - a lion-bodied guardian with a gold-and-lapis nemes headdress and folded wings."""
from eggsb_kit import *

SAND, GOLD, LAPIS, SKINC = "#d9b878", "#f2c94c", "#2c58b8", "#c89060"

fur = coat(SAND, dark="#b8965a", light="#ecd49a", under="#e8d3a0", seed=271, patch=2.5)

def nemes(p):
    y = p.p[1]
    stripe = int(p.p[1] * 0.9 + p.p[2] * 0.0) % 2 == 0
    return shade(GOLD if stripe else LAPIS, 0.92 + 0.16 * hash01(p.x, p.y, p.fw, 3))

def face(p):
    c = coat(SKINC, dark="#a8744c", light="#e0aa78", seed=273, patch=2)(p)
    if p.face == "front" and p.y == p.fh - 2 and 1 < p.x < p.fw - 2: return "#7a4030"     # lips
    return c

def wing(p):
    x, y, z = p.p
    c = mix("#e6d4a0", "#f8f0d0", noise3(x * 0.6, y, z * 1.3, 275, 2.0))
    return shade(c, 0.88 + 0.24 * hash01(p.x, p.y, p.fw, 6)) if int(x) % 2 else shade(c, 0.85)

def gold(p): return shade(GOLD, 0.88 + 0.24 * hash01(p.x, p.y, p.fw, 5))
def claw(p): return "#3a2e20"
def glyph(p): return glow("#5ae0ff") if hash01(p.x, p.y, p.fw, 9) > 0.6 else shade(SAND, 0.8)

bones = quad(10, 9, 16, 4, 4, (7, 7, 7), 18, skin="fur", foot_h=0, leg_ld=4)
# crouching pose: chest raised, paws stretched out front
by(bones, "head")["cubes"] = [C([-3.5, 18, -11], [7, 7, 7], "face"), C([-1, 17.2, -12], [2, 1, 1], "gold"),
                              C([-4.5, 24, -12], [9, 2, 9], "nemes"), C([-4.5, 14, -5], [9, 11, 3], "nemes"),
                              pair(C([3.5, 15, -10.5], [2, 9, 6], "nemes")), C([-1, 25, -12.2], [2, 2, 1], "gold"),
                              eyes(1.0, 21.5, -11, "eye", 2), C([-1.5, 13, -12], [3, 5, 2], "nemes"), C([-1, 11.5, -12.6], [2, 2, 1], "gold")]
by(bones, "head")["pivot"] = [0, 18, -8]
bones[0]["cubes"] += [C([-4, 4, -11], [8, 14, 5], "fur"), C([-6, 4, 4], [12, 8, 8], "fur"), C([-5, 12, -12], [10, 2, 3], "gold")]
for nm, s in (("fl", 1), ("fr", -1)):
    b = by(bones, f"leg_{nm}"); b["pivot"] = [s * 4, 4, -8]
    b["cubes"] = [C([s * 4 - 2, 0, -20], [4, 4, 12], "fur"), C([s * 4 - 2, 0, -21], [1, 1, 1], "claw"), C([s * 4 - 0.5, 0, -21], [1, 1, 1], "claw"), C([s * 4 + 1, 0, -21], [1, 1, 1], "claw")]
for nm, s in (("bl", 1), ("br", -1)):
    b = by(bones, f"leg_{nm}"); b["pivot"] = [s * 5, 4, 6]
    b["cubes"] = [C([s * 5 - 2, 0, 1], [4, 4, 9], "fur")]
bones.append(bone("tail", "body", [0, 8, 8], [C([-1, 4, 10], [2, 2, 6], "fur", rot=[-20, 0, 0], pivot=[0, 6, 10]), C([-1.5, 2, 16], [3, 4, 3], "gold")]))
bones.append(wing_l := bone("wing_l", "body", [4, 13, -2], [C([4, 13, -2], [2, 6, 12], "wing", rot=[0, 0, -8], pivot=[4, 13, -2]),
                                                             C([5, 9, 0], [2, 5, 9], "wing", rot=[0, 0, -8], pivot=[4, 13, -2]), C([6, 12, 8], [2, 4, 4], "wing")]))
bones.append(bone("wing_r", "body", [-4, 13, -2], [mirror(c) for c in wing_l["cubes"]]))

anims = quad_anims(tail="tail", tail_amp=18, walk_amp=25, freq=30)
anims["idle"]["bones"].update({"head": {"rotation": ["math.sin(query.life_time * 40) * 2", "math.sin(query.life_time * 21) * 8", "0"]}})

SPEC = with_visible({
    "id": "sphinx", "name": "Desert Sphinx", "egg": ("#d9b878", "#2c58b8"), "glow": True, "scale": 1.2,
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "face": face, "nemes": nemes, "gold": gold, "wing": wing, "claw": claw, "glyph": glyph,
              "eye": eye("#2c8ae0", pupil="#101830")},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "neutral", "health": 60, "speed": 0.24, "damage": 9, "box": [1.4, 1.9], "knockback_resist": 0.5, "family": ["sphinx"],
        "spawn": {"biomes": ["desert"], "weight": 1, "herd": [1, 1]},
        "loot": [("minecraft:gold_ingot", 1, 3), ("minecraft:lapis_lazuli", 2, 6), ("minecraft:paper", 1, 3), ("minecraft:sand", 0, 3)],
        "sound": ("cat", [0.6, 0.7]),
    },
})
