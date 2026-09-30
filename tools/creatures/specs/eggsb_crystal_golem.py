"""Crystal Golem - slender amethyst-stone sentinel bristling with glowing shards."""
from eggsb_kit import *

ROCK, ROCK_D = "#4a3a6a", "#2a2040"

def cracked(p, c):
    x, y, z = p.p
    if abs(noise3(x * 0.6, y * 0.6, z * 0.6, 201, 1.0) - 0.5) < 0.03: return glow("#c060ff")

rock = coat(ROCK, dark=ROCK_D, light="#6a58a0", seed=201, patch=2.2, extra=cracked)

def shard(seed):
    def fn(p):
        x, y, z = p.p
        t = noise3(x * 0.5, y * 0.8, z * 0.5, seed, 2.0)
        c = mix("#b060ff", "#60e8ff", t)
        return glow(shade(c, 0.85 + 0.3 * hash01(p.x, p.y, p.fw, seed)))
    return fn

def core(p): return glow(mix("#ff60d8", "#ffd0f8", noise3(*p.p, 209, 1.0)))
def eyefn(p): return glow("#80f8ff")

bones = biped(8, 10, 6, 9, 3, 3, 13, 3, 3, (5, 5, 5), skin="rock", leg_x=2.4, head_dy=0, foot_h=2, foot_skin="rockd", hand_h=3, hand_skin="shard",
              arm_dx=0.5, shoulder_drop=2)
add(bones, "head", eyes(0.8, 21.0, -2.5, "eye", 1), C([-1, 19.6, -3], [2, 1, 1], "rockd"),
    C([-1, 24, -1], [2, 5, 2], "shard", rot=[0, 0, 0]), C([-3, 24, -1], [2, 3, 2], "shard2", rot=[0, 0, 22], pivot=[-2, 24, 0]),
    C([1, 24, -1], [2, 3, 2], "shard2", rot=[0, 0, -22], pivot=[2, 24, 0]), C([-1, 24, 1.5], [2, 3, 2], "shard", rot=[25, 0, 0], pivot=[0, 24, 2]))
add(bones, "body",
    C([-2.5, 13, -3.6], [5, 5, 1], "core"), C([-3, 12, -3.4], [6, 1, 1], "rockd"), C([-3, 18, -3.4], [6, 1, 1], "rockd"),
    C([-4, 18, -3], [8, 2, 6], "rockd"),
    *[C([x, 19, 2], [2, 6, 2], "shard", rot=[-25 + k * 5, 0, s], pivot=[x + 1, 19, 3]) for k, (x, s) in enumerate(((-3, 10), (-0.5, 0), (2, -10)))],
    C([-2, 9, 3.4], [4, 6, 1], "rockd"))
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    x = sx * 5.5
    add(bones, n_, C([x - 1.5, 16, -1.5], [3, 3, 3], "rockd"))
    add(bones, n_, C([x - 1 + sx * 1.2, 19, -1], [2, 5, 2], "shard2", rot=[0, 0, sx * -25], pivot=[x, 18, 0]))
    add(bones, n_, C([x - 1, 2, -2.5], [2, 3, 1], "shard", rot=[-20, 0, 0], pivot=[x, 4, -1.5]))

anims = biped_anims(walk_amp=24, arm_amp=18, freq=32, body_bob=0.3)
anims["idle"]["bones"].update({"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 25) * 10", "0"]}})

SPEC = with_visible({
    "id": "crystal_golem", "name": "Crystal Golem", "egg": ("#4a3a6a", "#60e8ff"), "glow": True, "scale": 1.15,
    "bones": bones,
    "skins": {"default": rock, "rock": rock, "rockd": solid("#2a2040", 0.25, 5), "shard": shard(203), "shard2": shard(205),
              "core": core, "eye": eyefn},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "neutral", "health": 70, "speed": 0.22, "damage": 8, "box": [0.9, 2.1], "knockback_resist": 0.8, "family": ["golem"],
        "spawn": {"biomes": ["extreme_hills", "mesa"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:amethyst_shard", 2, 6), ("minecraft:lapis_lazuli", 0, 3), ("minecraft:diamond", 0, 1)],
        "sound": ("golem", [1.2, 1.4]),
    },
})
