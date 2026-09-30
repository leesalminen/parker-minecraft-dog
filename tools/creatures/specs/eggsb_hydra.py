"""Marsh Hydra - three-necked swamp serpent-beast.  Big, slow, and very bitey."""
from eggsb_kit import *

GREEN, DARK, BELLY, FRILL = "#4f8a4a", "#2c5a34", "#e2d68a", "#e8842a"

hide = scales(GREEN, dark=DARK, light="#78b05c", cell=2.0, under=BELLY, seed=241)

def belly(p):
    if p.face in ("bottom",) or p.p[1] < 6: return mix(BELLY, "#cbbd70", 0.5 if int(p.p[2]) % 2 else 0.0)
    return hide(p)

def frill(p): return shade(mix(FRILL, "#ffc060", noise3(*p.p, 243, 1.0)), 0.85 + 0.3 * hash01(p.x, p.y, p.fw, 3))
def fang(p): return "#f4eedd"
def mouth(p): return "#7a2a30"
def claw(p): return "#2a2418"

def headfn(p):
    c = hide(p)
    if p.face == "front" and p.y >= 1 and p.fw >= 4 and p.x in (0, p.fw - 1): return "#e8e0c0"
    return c

def head_parts(x, hy, hz):
    """A snake-ish head: skull + long snout, fangs, horn frills, slit eyes; pivot for jaw bone at mouth."""
    upper = [C([x - 2.5, hy, hz - 4], [5, 4, 6], "head"), C([x - 2, hy + 0.5, hz - 9], [4, 3, 5], "head"),
             C([x - 1.5, hy + 1, hz - 9.5], [1, 1, 1], "fang"), C([x + 0.5, hy + 1, hz - 9.5], [1, 1, 1], "fang"),
             C([x - 1, hy + 3.4, hz - 8.5], [2, 1, 1], "dark"),
             *eyes_at(x, hy + 2.6, hz - 4.6),
             C([x - 1, hy + 4, hz - 3], [2, 2, 5], "frill"), C([x - 3.5, hy + 3, hz - 1], [1, 3, 3], "frill", rot=[0, 0, 25], pivot=[x - 3, hy + 3, hz - 1]),
             C([x + 2.5, hy + 3, hz - 1], [1, 3, 3], "frill", rot=[0, 0, -25], pivot=[x + 3, hy + 3, hz - 1])]
    lower = [C([x - 2, hy - 1.2, hz - 8], [4, 1, 7], "head"), C([x - 1.5, hy - 0.4, hz - 8], [1, 1, 1], "fang"), C([x + 0.5, hy - 0.4, hz - 8], [1, 1, 1], "fang"),
             C([x - 1.5, hy - 0.3, hz - 7], [3, 1, 5], "mouth")]
    return upper, lower

def eyes_at(x, y, z):
    return [C([x + 2.0, y, z], [1, 2, 2], "eye"), C([x - 3.0, y, z], [1, 2, 2], "eye")]

bones = [bone("body", None, [0, 10, 0], [C([-6, 5, -8], [12, 8, 16], "belly"), C([-5, 12, -6], [10, 2, 12], "hide")]),
         bone("tail0", "body", [0, 9, 8], [C([-4, 5, 8], [8, 7, 8], "hide")]),
         bone("tail1", "tail0", [0, 8, 16], [C([-3, 4.5, 16], [6, 5, 8], "hide")]),
         bone("tail2", "tail1", [0, 7, 24], [C([-2, 4, 24], [4, 4, 8], "hide"), C([-0.5, 8, 26], [1, 3, 4], "frill")])]
for i, (x, hh, yaw, ph) in enumerate(((0, 19, 0, 0), (-6, 14, 1, 1.4), (6, 14, -1, 2.8))):
    # stair-step neck rising from shoulder
    nc = []
    steps = 4 if i == 0 else 3
    for s in range(steps):
        nc.append(C([x - 2.5 + yaw * s * 1.2 * -1, 11 + s * 3.4, -8 - s * 1.5], [5, 5, 5], "hide"))
        nc.append(C([x - 0.5 + yaw * s * 1.2 * -1, 15 + s * 3.4, -7.5 - s * 1.5], [1, 2, 3], "frill"))
    bones.append(bone(f"neck{i}", "body", [x, 12, -7], nc))
    top = 11 + steps * 3.4 + 2
    hx = x + yaw * steps * -1.2
    up, lo = head_parts(hx, top, -8 - steps * 1.5 + 4)
    bones.append(bone(f"head{i}", f"neck{i}", [hx, top + 1, -8 - steps * 1.5], up))
    bones.append(bone(f"jaw{i}", f"head{i}", [hx, top, -8 - steps * 1.5 - 1], lo))
for nm, sx, sz in (("fl", 1, -5), ("fr", -1, -5), ("bl", 1, 5), ("br", -1, 5)):
    bones.append(bone(f"leg_{nm}", "body", [sx * 5.5, 6, sz], [C([sx * 5.5 - 2.5, 0, sz - 2.5], [5, 6, 5], "hide"), C([sx * 5.5 - 2.5, 0, sz - 4.5], [1, 2, 2], "claw"),
                                                              C([sx * 5.5 - 0.5, 0, sz - 4.5], [1, 2, 2], "claw"), C([sx * 5.5 + 1.5, 0, sz - 4.5], [1, 2, 2], "claw")]))

anims = quad_anims(tail="tail0", tail_amp=8, walk_amp=28, freq=30, head_bob=False)
for a in ("walk", "idle"):
    for i, ph in enumerate((0, 1.4, 2.8)):
        anims[a]["bones"].update(sway(f"neck{i}", 9, 45, 1, ph))
        anims[a]["bones"].update({f"head{i}": {"rotation": [f"math.sin(query.life_time * 55 + {ph}) * 6", f"math.sin(query.life_time * 37 + {ph}) * 12", "0"]},
                                  f"jaw{i}": {"rotation": [f"math.max(0, math.sin(query.life_time * 90 + {ph * 2})) * 12", "0", "0"]}})
    anims[a]["bones"].update(sway("tail1", 10, 50, 1, 1))
    anims[a]["bones"].update(sway("tail2", 14, 50, 1, 2))

SPEC = with_visible({
    "id": "hydra", "name": "Marsh Hydra", "egg": ("#4f8a4a", "#e8842a"), "glow": False, "scale": 1.15,
    "bones": bones, "look": False,
    "skins": {"default": hide, "hide": hide, "belly": belly, "head": headfn, "frill": frill, "fang": fang, "mouth": mouth, "dark": solid("#1a2a1a", 0.2, 3),
              "claw": claw, "eye": lambda p: "#ffd830" if p.face in ("east", "west", "front") and p.y == 0 else "#1a1a10"},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "hostile", "health": 100, "speed": 0.2, "damage": 10, "box": [2.0, 2.3], "knockback_resist": 0.7, "family": ["hydra"],
        "xp": 30, "reach": 1.4,
        "spawn": {"biomes": ["swamp", "jungle"], "weight": 2, "herd": [1, 1]},
        "loot": [("minecraft:slime_ball", 1, 4), ("minecraft:bone", 2, 5), ("minecraft:spider_eye", 0, 2), ("minecraft:emerald", 0, 2)],
        "sound": ("ravager", [0.8, 0.95]),
    },
})
