"""Kitsune - five-tailed spirit fox with glowing blue flame tips and a red ribbon.  Tameable companion."""
from eggsb_kit import *

ORANGE, CREAM, RED = "#e8843a", "#fbf1e0", "#c8283a"

def markings(p, c):
    x, y, z = p.p
    if p.bone == "head" and p.face in ("top", "front") and abs(x) < 0.6 and y > 11: return RED
    if p.bone == "head" and p.face == "front" and p.fh > 3 and p.y >= p.fh - 2 and (p.x < 1 or p.x > p.fw - 2): return CREAM
    if p.bone == "body" and y > 9.5 and abs(abs(x) - 1.7) < 0.55 and int(z) % 3 == 0: return shade(RED, 1.1)

fur = coat(ORANGE, dark="#c9642a", light="#f4a458", under=CREAM, under_y=7.5, seed=111, patch=2.5, extra=markings)

def sock(p): return shade("#2a1e1a", 0.9 + 0.2 * noise3(*p.p, 113, 1.0))

def ear(p):
    if p.face == "front" and 0 < p.x < p.fw - 1 and p.y > 0: return "#f2c0b0"
    return fur(p)

def tailfur(p):
    c = fur(p)
    return mix(c, CREAM, 0.4) if p.face == "bottom" else c

def tip(p): return shade(CREAM, 0.94 + 0.12 * hash01(p.x, p.y, p.fw, 3))
def flame(p): return glow(mix("#5ac8ff", "#e8fbff", 0.15 + 0.6 * noise3(*p.p, 115, 1.0)))

bones = quad(5, 5, 10, 6, 2, (5, 4, 5), 9, head_dz=0, skin="fur", foot_h=3, foot_skin="sock", leg_ld=2)
add(bones, "head",
    C([-1.5, 9.4, -10.5], [3, 2, 3], "fur"), C([-0.5, 10.6, -11.3], [1, 1, 1], "sock"),
    pair(C([1, 13, -5.5], [2, 3, 1], "ear")), pair(C([1.4, 16, -5.3], [1, 2, 1], "ear")),
    eyes(1.0, 11.0, -8, "eye", 1),
    pair(C([2.5, 9, -7], [1, 2, 3], "tailfur")),
    C([-3, 7, -6.5], [6, 3, 2], "ribbon"), C([-1, 5, -7], [2, 2, 1], "gold"))
add(bones, "body", C([-2.5, 5, -6], [5, 1, 5], "tailfur"))
for i, yaw in enumerate((-55, -28, 0, 28, 55)):
    n = f"tail{i}"; rot = [-25 - (i == 2) * 10, yaw, 0]; pv = [0, 8, 5]
    bones.append(bone(n, "body", pv, [
        C([-1.5, 7, 5], [3, 3, 6], "tailfur", rot=rot, pivot=pv), C([-1.5, 7, 11], [3, 3, 3], "tailfur", rot=rot, pivot=pv),
        C([-1.5, 7, 14], [3, 3, 2], "tip", rot=rot, pivot=pv), C([-1, 9, 14.3], [2, 2, 2], "flame", rot=rot, pivot=pv)]))

anims = quad_anims(tail=None, walk_amp=42, freq=55)
for i in range(5):
    for a, amp, rate in (("walk", 10, 80), ("idle", 8, 40)):
        anims[a]["bones"].update(sway(f"tail{i}", amp, rate, 1, off=i * 0.9))
anims["idle"]["bones"].update({"head": {"rotation": ["math.sin(query.life_time * 60) * 4", "math.sin(query.life_time * 33) * 10", "math.sin(query.life_time * 47) * 4"]}})

SPEC = with_visible({
    "id": "kitsune", "name": "Kitsune", "egg": ("#e8843a", "#5ac8ff"), "glow": True, "scale": 1.0,
    "bones": bones,
    "skins": {"default": fur, "fur": fur, "sock": sock, "ear": ear, "tailfur": tailfur, "tip": tip, "flame": flame,
              "ribbon": solid(RED, 0.15, 8), "gold": solid("#f2c94c", 0.1, 9), "eye": eye("#6ad0ff")},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "companion", "health": 16, "speed": 0.36, "box": [0.6, 0.9], "family": ["kitsune", "fox"],
        "tame_items": ["minecraft:chicken", "minecraft:sweet_berries", "minecraft:cooked_chicken"],
        "spawn": {"biomes": ["taiga", "cherry_grove", "forest"], "weight": 3, "herd": [1, 1]},
        "loot": [("minecraft:sweet_berries", 0, 2), ("minecraft:lapis_lazuli", 0, 1)],
        "sound": ("fox", [1.1, 1.3]),
    },
})
