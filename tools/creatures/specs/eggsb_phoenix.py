"""Phoenix - flame bird.  Fire immune, glowing plumage and a long tail of fire feathers."""
from eggsb_kit import *

def flame(seed, lo="#c81e0a", mid="#ff7a1a", hi="#ffd23a"):
    def fn(p):
        x, y, z = p.p
        t = noise3(x * 1.3, y * 0.9, z * 1.3, seed, 2.0)
        c = mix(lo, mid, min(1, t * 1.6))
        c = mix(c, hi, max(0.0, t - 0.55) * 2.0)
        return glow(c)
    return fn

def tipflame(p):
    y = p.p[1]
    return glow(mix("#ff9a1a", "#fff09a", min(1.0, hash01(p.x, p.y, p.fw, 3) * 0.6 + 0.2)))

def beak(p): return shade("#e8a020", 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 5))
def talon(p): return shade("#5a3a20", 0.9 + 0.2 * hash01(p.x, p.y, p.fw, 6))

bones = [
    bone("body", None, [0, 12, 0], [C([-4, 8, -5], [8, 8, 10], "plume"), C([-3, 7, -4], [6, 2, 8], "flame_hi")]),
    bone("head", "body", [0, 16, -5], [C([-3, 15, -9], [6, 6, 6], "plume"), C([-1.5, 17, -12], [3, 2, 3], "beak"),
                                       C([-1, 16, -11.5], [2, 1, 3], "beak"), C([-1, 21, -8], [2, 3, 3], "flame_hi"),
                                       C([-1, 23, -6], [2, 3, 3], "flame_hi"), C([-0.5, 25, -4], [1, 2, 2], "tip"),
                                       eyes(1.0, 18, -9, "eye", 2)]),
    bone("tail", "body", [0, 12, 5], [C([-2, 7, 5], [4, 3, 7], "plume"),
                                     C([-1, 9, 10], [2, 2, 8], "flame_hi", rot=[-15, 0, 0], pivot=[0, 9, 10]),
                                     C([-4, 3, 8], [2, 3, 12], "flame", rot=[0, -18, 0], pivot=[-3, 5, 8]),
                                     C([2, 3, 8], [2, 3, 12], "flame", rot=[0, 18, 0], pivot=[3, 5, 8]),
                                     C([-1, 1, 10], [2, 2, 16], "flame_hi"),
                                     C([-1, 5, 16], [2, 2, 12], "flame", rot=[15, 0, 0], pivot=[0, 5, 16]),
                                     C([-0.5, 0, 24], [1, 2, 6], "tip")]),
    leg("leg_l", 2, 0, 2, 2, 8, "talon", 0, None, top=9),
    leg("leg_r", -2, 0, 2, 2, 8, "talon", 0, None, top=9),
    wing("wing_l", "body", 1, 4, 16, -2, 15, 7, "plume", "flame", "tip", fingers=4),
    wing("wing_r", "body", -1, 4, 16, -2, 15, 7, "plume", "flame", "tip", fingers=4),
]
for b in bones:
    if b["name"].startswith("leg_"):
        b["cubes"].append(C([b["pivot"][0] - 1.5, 0, -3], [3, 1, 3], "talon"))

anims = {
    "walk": anim(merge(biped_walk("leg_l", "leg_r", 30), sway("tail", 8, 60, 1), bob("body", 0.4, 200))),
    "idle": anim(merge(bob("body", 0.6, 90), sway("tail", 10, 40, 1), sway("head", 8, 50, 1),
                       fold("wing_l", "wing_r", 40, 5, 80))),
    "flap": flap_anim("wing_l", "wing_r", amp=45, rate=340, extra=sway("tail", 8, 80, 0)),
}

SPEC = with_visible({
    "id": "phoenix", "name": "Phoenix", "egg": ("#ff7a1a", "#ffd23a"), "glow": True, "scale": 1.3,
    "bones": bones,
    "skins": {"default": flame(61), "plume": flame(63, "#b81808", "#f0561a", "#ffb02a"), "flame": flame(65),
              "flame_hi": flame(67, "#ff8a1a", "#ffc02a", "#fff0a0"), "tip": tipflame, "beak": beak, "talon": talon,
              "eye": eye("#ffee88", pupil="#301000")},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "companion", "health": 24, "speed": 0.26, "fly": True, "fly_speed": 0.32, "box": [0.8, 1.4],
        "fire_immune": True, "family": ["phoenix"],
        "tame_items": ["minecraft:blaze_powder", "minecraft:magma_cream"],
        "spawn": {"biomes": ["desert", "mesa", "savanna"], "weight": 1, "herd": [1, 1]},
        "loot": [("minecraft:feather", 1, 2), ("minecraft:blaze_powder", 0, 2)],
        "sound": ("parrot", [0.7, 0.9]),
    },
})
