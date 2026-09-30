"""Will-o'-Wisp - a shy glowing ghost-flame that drifts over swamps and trails cold blue fire."""
from eggsb_kit import *

def cold(seed, lo="#3ad0b0", hi="#c8fff0"):
    def fn(p):
        t = noise3(*p.p, seed, 1.6)
        return glow(mix(lo, hi, 0.25 + 0.7 * t))
    return fn

def halo(p):
    return glow(mix("#2a90c8", "#7af0ff", noise3(*p.p, 163, 1.3)))

def face_eye(p):
    return "#0a2a30"

bones = [
    bone("body", None, [0, 10, 0], [
        C([-3, 8, -3], [6, 6, 6], "core"), C([-4, 10, -1], [8, 2, 2], "halo"), C([-1, 10, -4], [2, 2, 8], "halo"), C([-1, 7, -1], [2, 8, 2], "halo")]),
    bone("head", "body", [0, 11, 0], [eyes(1.6, 9.6, -3, "dark", 2), C([-1, 8.2, -3.5], [2, 1, 1], "dark")]),
    bone("flame", "body", [0, 14, 0], [
        C([-1.5, 14, -1.5], [3, 3, 3], "core"), C([-1, 17, -1], [2, 3, 2], "tail"), C([-0.5, 20, -0.5], [1, 2, 1], "tail"),
        C([-2.5, 12, -0.5], [1, 3, 1], "tail", rot=[0, 0, 25], pivot=[-2, 14, 0]), C([1.5, 12, -0.5], [1, 3, 1], "tail", rot=[0, 0, -25], pivot=[2, 14, 0])]),
    bone("wisp0", "body", [0, 11, 0], [C([4, 10.5, -0.5], [1, 1, 1], "core")]),
    bone("wisp1", "body", [0, 11, 0], [C([-5, 10.5, -0.5], [1, 1, 1], "halo")]),
    bone("wisp2", "body", [0, 11, 0], [C([-0.5, 15, 4], [1, 1, 1], "core")]),
    bone("trail0", "body", [0, 9, 3], [C([-2, 6, 3], [4, 4, 4], "tail")]),
    bone("trail1", "trail0", [0, 8, 7], [C([-1.5, 5, 7], [3, 3, 4], "tail")]),
    bone("trail2", "trail1", [0, 7, 11], [C([-1, 4, 11], [2, 2, 4], "tail")]),
    bone("trail3", "trail2", [0, 6, 15], [C([-0.5, 3, 15], [1, 1, 3], "halo")]),
]

def orbit(bone_name, r_rate, phase, ry=4):
    return {bone_name: {"position": [f"math.sin(query.life_time * {r_rate} + {phase}) * 3", f"math.sin(query.life_time * {r_rate * 1.7} + {phase}) * 2",
                                     f"math.cos(query.life_time * {r_rate} + {phase}) * 3"]}}

def motes():
    return merge(orbit("wisp0", 120, 0), orbit("wisp1", 100, 2.1), orbit("wisp2", 140, 4.2))

common = merge(motes(), sway("trail0", 12, 90, 1), sway("trail1", 16, 90, 1, 0.8), sway("trail2", 20, 90, 1, 1.6), sway("trail3", 24, 90, 1, 2.4),
               sway("flame", 8, 130, 2), bob("body", 1.4, 110))
anims = {"idle": anim(merge(common, {"head": {"rotation": ["math.sin(query.life_time * 60) * 4", "math.sin(query.life_time * 43) * 12", "0"]}})),
         "walk": anim(merge(common, {"body": {"rotation": ["18", "0", "0"]}}))}

SPEC = with_visible({
    "id": "wisp", "name": "Will-o'-Wisp", "egg": ("#3ad0b0", "#c8fff0"), "glow": True, "scale": 1.0,
    "bones": bones,
    "skins": {"default": cold(161), "core": cold(161, "#3ae8c0", "#e8fff8"), "halo": halo, "tail": cold(165, "#1aa088", "#6af0d0"),
              "dark": face_eye},
    "anims": anims, "play": PLAY_WALK_IDLE,
    "behavior": {
        "role": "passive", "health": 6, "speed": 0.18, "hover": True, "fly_speed": 0.14, "box": [0.5, 0.75], "family": ["wisp", "spirit"],
        "spawn": {"biomes": ["swamp", "forest"], "weight": 5, "herd": [1, 2]},
        "loot": [("minecraft:glowstone_dust", 1, 3), ("minecraft:glow_ink_sac", 0, 1)],
        "sound": ("vex", [1.4, 1.6]),
    },
})
