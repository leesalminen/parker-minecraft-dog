"""Sailfin Dimetrodon - sprawling, sail-backed reptile predator (older than the dinosaurs)."""
from lib import *
from specs.eggsa_kit import *

bones = quad(12, 8, 22, 4, 4, 4, skin="hide", leg_skin="leg", foot_skin="leg", toes=3, fz=1, bz=1, inset=-3.5, front_lw=4, front_ld=4)
for nm in ("leg_fl", "leg_fr", "leg_bl", "leg_br"):
    b = get(bones, nm)
    b["cubes"].append(cube([b["cubes"][0]["o"][0] + (1 if "l" in nm[-1] else -1) * 0, 3, b["cubes"][0]["o"][2]], [4, 5, 4], "leg"))
body = get(bones, "body")
sail = [4, 8, 12, 16, 17, 16, 14, 11, 7]
for i, h in enumerate(sail):
    z = -10 + i * 2.4
    body["cubes"].append(cube([-0.5, 12, z], [1, h + 4, 1], "spine"))
    body["cubes"].append(cube([-0.5, 12, z + 1], [1, max(2, h + 1), 2], "sail"))
bones.append(bone("neck", "body", [0, 8, -11], [cube([-3.5, 5, -14], [7, 6, 5], "hide")]))
hc = [cube([-4, 4, -25], [8, 7, 11], "hide"), cube([-3, 5, -28], [6, 5, 4], "hide"), cube([-3, 11, -24], [6, 1, 8], "ridge")]
side_eyes(hc, 4, 8, -22, 2, "eye")
for z in (-27, -24, -21):
    pair(hc, cube([2.5, 3, z], [1, 2, 1], "tooth"))
pair(hc, cube([1, 8, -28.5], [1, 1, 1], "dark"))
bones.append(bone("head", "neck", [0, 8, -14], hc))
bones.append(bone("jaw", "head", [0, 5, -14], [cube([-3, 3, -26], [6, 2, 12], "belly")] + [cube([1.5, 5, -25 + i * 3], [1, 2, 1], "tooth") for i in range(3)] +
                 [cube([-2.5, 5, -25 + i * 3], [1, 2, 1], "tooth") for i in range(3)]))
tail(bones, "body", 3, 11, 6, 6, 5, 7, taper=0.82, skin="hide", tip_skin="hide")
hide = pelt("#b8763a", "#8f5626", belly="#e8d8a0", belly_y=5, seed=251, stripes=("#4a2c12", 1.1, 0.55, "z"))
skins = {"default": hide, "hide": hide, "leg": pelt("#8f5626", "#6b3f1a", seed=252), "spine": solid("#f0e4c0"),
         "sail": pelt("#d8483a", "#a82e26", seed=253, stripes=("#f0a04a", 1.6, 0.5, "y")), "ridge": solid("#5c3a1a"), "tooth": tooth,
         "belly": flat("#e8d8a0"), "claw": claw_paint(), "eye": eye_color("#e8b830"), "dark": flat("#1a120a")}
an = quad_anims(tail_bones=[f"tail{i}" for i in range(6)], amp=28, freq=40, bob_amp=0.2)
an["attack"] = bite_anim("jaw", "head", "neck", 32)
SPEC = finish("dimetrodon", "Sailfin Dimetrodon", ("#b8763a", "#d8483a"), bones, skins, an, STD_PLAY_ATK, {
    "role": "neutral", "health": 30, "speed": 0.22, "damage": 6, "box": [1.2, 1.1], "family": ["dimetrodon"],
    "loot": [("minecraft:bone", 1, 2), ("minecraft:leather", 0, 1)], "sound": ("spider", [0.6, 0.8]),
    "spawn": {"biomes": ["desert", "mesa", "savanna", "swamp"], "weight": 6, "herd": [1, 2]}})
