"""Sand Golem - pot-bellied desert guardian with floating hands, a carved headdress and glowing gold eyes."""
from eggsb_kit import *

SAND, SAND_D, GOLD, TEAL = "#dcc07a", "#b89a54", "#f2c94c", "#2fa8a0"

def strata(p, c):
    x, y, z = p.p
    band = math.sin(y * 1.1 + noise3(x, y, z, 233, 3.0) * 4)
    if band > 0.75: return shade(c, 0.86)
    if p.bone == "body" and p.face == "front" and abs(p.x + 0.5 - p.fw / 2) < 1 and p.y in (2, 3, 5): return shade(c, 0.55)   # carved glyphs

sand = coat(SAND, dark=SAND_D, light="#f0dca0", seed=231, patch=2, extra=strata)

def band(p):
    return TEAL if (int(p.p[1]) + int(p.p[0] + p.p[2])) % 3 else GOLD
def headdress(p):
    s = int(p.p[1] * 1.0) % 2
    return GOLD if s == 0 else TEAL
def eyefn(p): return glow("#ffe060")
def rune(p): return glow("#ffd040") if hash01(p.x, p.y, p.fw, 5) > 0.35 else shade(SAND_D, 0.6)

bones = biped(12, 10, 9, 5, 8, 6, 10, 4, 4, (8, 7, 7), skin="sand", leg_x=4, head_dy=-1, arm_dx=2, hand_h=4, hand_skin="sand",
              foot_h=1, foot_skin="sand", shoulder_drop=2)
add(bones, "head", eyes(1.4, 16.6, -3.5, "eye", 2), C([-1, 14.6, -4.5], [2, 3, 1], "sand"),
    C([-5, 19.4, -4], [10, 2, 8], "headdress"), pair(C([4, 12, -3], [2, 8, 6], "headdress")), C([-4, 12, 3.5], [8, 8, 2], "headdress"),
    C([-1, 18, -4.5], [2, 2, 1], "gold"))
add(bones, "body", C([-6, 13, -4.5], [12, 2, 9], "band"), C([-2.5, 9, -4.7], [5, 3, 1], "rune"), C([-7, 6, -5], [14, 3, 10], "sand"))
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    add(bones, n_, C([sx * 8 - 2.5, 14.5, -2.5], [5, 2, 5], "band"))

anims = biped_anims(walk_amp=28, arm_amp=12, freq=42, body_bob=0.4,
                    extra_idle=merge(sway("arm_l", 6, 60, 0), sway("arm_r", 6, 60, 0, 2),
                                     {"head": {"rotation": ["math.sin(query.life_time * 50) * 2", "math.sin(query.life_time * 27) * 12", "0"]}}))

SPEC = with_visible({
    "id": "sand_golem", "name": "Sand Golem", "egg": ("#dcc07a", "#2fa8a0"), "glow": True, "scale": 1.05,
    "bones": bones,
    "skins": {"default": sand, "sand": sand, "band": band, "headdress": headdress, "gold": solid(GOLD, 0.15, 5), "rune": rune, "eye": eyefn},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "neutral", "health": 50, "speed": 0.24, "damage": 6, "box": [1.3, 1.9], "knockback_resist": 0.5, "family": ["golem"],
        "spawn": {"biomes": ["desert"], "weight": 5, "herd": [1, 2]},
        "loot": [("minecraft:sand", 2, 6), ("minecraft:gold_nugget", 0, 4), ("minecraft:clay_ball", 0, 3), ("minecraft:sandstone", 0, 2)],
        "sound": ("golem", [1.0, 1.1]),
    },
})
