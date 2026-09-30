"""Yeti - towering shaggy snow-ape.  Peaceful until hit, then hits very hard."""
from eggsb_kit import *

FUR, FUR_D, SKINC = "#f2f6fb", "#b7c6dc", "#7d95b0"

def shag(p):
    x, y, z = p.p
    n = noise3(x * 0.8, y * 2.2, z * 0.8, 181, 1.0)      # vertical hair streaks
    m = noise3(x, y, z, 183, 4.0)
    c = mix(FUR_D, FUR, 0.35 + 0.65 * n)
    c = mix(c, "#cfe0f4", 0.35 * m)
    if p.face == "bottom": c = shade(c, 0.85)
    if hash01(int(x), int(y * 0.7), int(z), 187) > 0.94: c = shade(c, 0.78)
    return c

def face(p):
    if p.face == "front" and p.y >= 1 and 1 <= p.x <= p.fw - 2:
        c = mix(SKINC, "#5a7592", noise3(*p.p, 189, 1.0))
        if p.y == p.fh - 1 or (p.y == p.fh - 2 and p.x in (2, p.fw - 3)): return "#e8ecf0" if p.x % 2 == 0 else "#2a3448"     # fangs / mouth
        return c
    return shag(p)

def paw(p):
    c = mix(SKINC, "#4a6280", noise3(*p.p, 191, 1.0))
    return shade(c, 0.85 + 0.2 * hash01(p.x, p.y, p.fw, 2))

def claw(p): return "#2a2e38"

bones = biped(12, 12, 8, 8, 5, 6, 17, 5, 5, (8, 7, 7), skin="shag", head_skin="face", leg_skin="shag", arm_skin="shag", head_dy=-2, head_dz=-2.5,
              leg_x=3.5, arm_dx=0.5, hand_h=5, hand_skin="paw", foot_h=3, foot_skin="paw")
add(bones, "head", eyes(1.4, 24.0, -6.0, "eye", 2), C([-3, 25.4, -6.2], [6, 1, 2], "shag"),
    C([-4, 27, -6], [8, 3, 6], "shag"), C([-1.5, 29.5, -5], [3, 2, 4], "shag"),
    pair(C([2, 20, -6.5], [1, 3, 1], "tusk")), pair(C([4, 22, -3], [1, 2, 2], "shag")))
add(bones, "body", C([-7, 20, -4], [3, 4, 8], "shag"), C([4, 20, -4], [3, 4, 8], "shag"),          # shoulder shag
    C([-3, 24, -4], [6, 3, 8], "shag"), *[C([-4 + i * 2.7, 24, 2 + (i % 2)], [2, 5, 2], "shag", rot=[-15, 0, 0], pivot=[-4 + i * 2.7, 24, 2]) for i in range(4)],
    C([-4, 9, -4.2], [8, 10, 1], "shag"))
for n_, sx in (("arm_l", 1), ("arm_r", -1)):
    b = by(bones, n_); x = sx * 8.5
    b["cubes"].append(C([x - 3, 10, -3.5], [6, 4, 7], "shag"))
    for i in range(3): b["cubes"].append(C([x - 2 + i * 1.7, 0, -3.4], [1, 2, 1], "claw"))

anims = biped_anims(walk_amp=26, arm_amp=22, freq=30, body_bob=0.5,
                    extra_idle={"body": {"rotation": ["math.sin(query.life_time * 50) * 1.5 + 3", "0", "0"]}})
anims["idle"]["bones"].update({"arm_l": {"rotation": ["math.sin(query.life_time * 50) * 3", "0", "6"]},
                               "arm_r": {"rotation": ["math.sin(query.life_time * 50 + 3) * 3", "0", "-6"]}})
anims["attack"] = anim({"body": {"rotation": ["math.sin(variable.attack_time * 180) * 18", "0", "0"]},
                        "head": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "0", "0"]}}, loop=False)

SPEC = with_visible({
    "id": "yeti", "name": "Yeti", "egg": ("#f2f6fb", "#7d95b0"), "glow": False, "scale": 1.15,
    "bones": bones,
    "skins": {"default": shag, "shag": shag, "face": face, "paw": paw, "claw": claw, "tusk": lambda p: "#f0ead8",
              "eye": eye("#48a8ff", pupil="#0a1020")},
    "anims": anims, "play": PLAY_WALK_IDLE + ["attack"],
    "behavior": {
        "role": "neutral", "health": 64, "speed": 0.26, "damage": 11, "box": [1.3, 2.3], "knockback_resist": 0.6, "family": ["yeti"],
        "reach": 1.3,
        "spawn": {"biomes": ["frozen", "cold"], "weight": 3, "herd": [1, 1]},
        "loot": [("minecraft:snowball", 2, 6), ("minecraft:white_wool", 1, 3), ("minecraft:ice", 0, 2), ("minecraft:diamond", 0, 1)],
        "sound": ("polarbear", [0.6, 0.75]),
    },
})
