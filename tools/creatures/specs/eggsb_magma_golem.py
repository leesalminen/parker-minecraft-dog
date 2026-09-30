"""Magma Golem - a hulking obsidian brute, cracked open along every seam with molten rock.  Fire immune."""
from eggsb_kit import *

def lava_rock(seed=221, thr=0.04):
    def fn(p):
        x, y, z = p.p
        n = noise3(x * 0.5, y * 0.5, z * 0.5, seed, 1.0)
        m = noise3(x * 0.5 + 9, y * 0.5, z * 0.5, seed + 3, 1.0)
        if abs(n - 0.5) < thr or abs(m - 0.5) < thr * 0.6:
            return glow(mix("#ff5a10", "#ffd23a", noise3(*p.p, seed + 5, 0.9)))
        c = coat("#2c2830", dark="#18141c", light="#4a4450", seed=seed, patch=2)(p)
        return c
    return fn

def magma(p): return glow(mix("#ff4a08", "#ffc02a", noise3(*p.p, 227, 1.0)))
def horn(p): return shade(mix("#1a1618", "#3a3234", noise3(*p.p, 229, 1.0)), 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 3))
def eyefn(p): return glow("#fff0a0")
def mouth(p):
    if p.face == "front" and p.y >= p.fh - 2 and 1 <= p.x <= p.fw - 2: return glow("#ff8a1a")
    return lava_rock(223)(p)

bones = biped(12, 11, 8, 9, 5, 5, 15, 5, 5, (7, 6, 7), skin="lava", head_skin="face", leg_x=3.3, head_dy=-1, head_dz=-1.5, hand_h=6,
              hand_skin="magma", arm_dx=0.5, shoulder_drop=1, foot_h=2, foot_skin="magma")
add(bones, "head", eyes(0.9, 19.0, -5.0, "eye", 2), C([-3.5, 20, -5.5], [7, 1, 2], "horn"),
    pair(C([2.5, 24, -2], [2, 4, 2], "horn", rot=[-10, 0, -20], pivot=[3, 23, -1])),
    pair(C([5, 27, -2], [2, 3, 2], "horn", rot=[-10, 0, -45], pivot=[3, 23, -1])),
    C([-2, 22, -5], [4, 1, 1], "horn"))
add(bones, "body", C([-4, 12, -4.6], [8, 5, 1], "magma"), C([-5, 16, -4.2], [10, 3, 2], "horn"),
    pair(C([5.5, 19, -3], [4, 3, 6], "horn", rot=[0, 0, -12], pivot=[5.5, 19, 0])),
    *[C([-1 + (i % 2) * 2, 12 + i * 2.5, 4], [2, 2, 2], "horn") for i in range(4)],
    C([-4, 10, 3.6], [8, 6, 1], "magma"))
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    add(bones, n_, C([sx * 8.5 - 3, 15, -3], [6, 2, 6], "horn"))

anims = biped_anims(walk_amp=26, arm_amp=20, freq=30, body_bob=0.5,
                    extra_idle={"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 20) * 9", "0"]}})
anims["attack"] = anim(merge({"body": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]},
                              "head": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "0", "0"]}}), loop=False)

SPEC = with_visible({
    "id": "magma_golem", "name": "Magma Golem", "egg": ("#2c2830", "#ff5a10"), "glow": True, "scale": 1.3,
    "bones": bones,
    "skins": {"default": lava_rock(), "lava": lava_rock(), "face": mouth, "magma": magma, "horn": horn, "eye": eyefn},
    "anims": anims, "play": PLAY_WALK_IDLE + ["attack"],
    "behavior": {
        "role": "hostile", "health": 80, "speed": 0.22, "damage": 12, "box": [1.4, 2.6], "knockback_resist": 0.8, "fire_immune": True,
        "family": ["golem", "magma"], "xp": 25, "reach": 1.2,
        "spawn": {"biomes": ["mesa", "desert"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:magma_cream", 1, 3), ("minecraft:obsidian", 0, 2), ("minecraft:coal", 1, 4), ("minecraft:blaze_powder", 0, 2)],
        "sound": ("golem", [0.6, 0.75]),
    },
})
