"""Spiral Ammonite - a coiled-shell shellfish that has decided to walk on land. Cute, slow, harmless."""
import math
from lib import *
from specs.eggsa_kit import *

body_c = [cube([-3, 1, -6], [6, 4, 10], "flesh"), cube([-4, 4, -4], [8, 3, 5], "flesh")]
bones = [bone("body", None, [0, 3, 0], body_c)]
sh = []
for rot in (0, 45):
    sh.append(cube([-4, 3, -3], [8, 12, 12], "shell", rot=[rot, 0, 0], pivot=[0, 9, 3]) if rot else cube([-4, 3, -3], [8, 12, 12], "shell"))
sh.append(cube([-3, 5, -6], [6, 5, 3], "shell_lip"))
bones.append(bone("shell", "body", [0, 9, 3], sh))
hd = []
pair(hd, cube([2, 4, -8], [2, 3, 2], "eyestalk"))
pair(hd, cube([2.5, 5, -9], [2, 2, 1], "eye_dark"))
bones.append(bone("head", "body", [0, 4, -6], hd))
for i in range(6):
    x = -5 + i * 2
    bones.append(bone(f"tent{i}", "body", [x + 1, 2, -6], [cube([x + 0.5, 0, -10], [1, 2, 5], "tent")]))
order = [f"tent{i}" for i in range(6)]
an = {"walk": anim(merge(hex_walk(order, 20, 60), {"shell": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 60) * 4 * query.modified_move_speed"]}})),
      "idle": anim(merge(sway("shell", 3, 40, 2), *[sway(f"tent{i}", 10, 55, 0, i * 0.9) for i in range(6)],
                         {"head": {"rotation": ["math.sin(query.life_time * 70) * 5", "math.sin(query.life_time * 45) * 10", "0"]}}))}


def spiral(p):
    if p.face in ("east", "west"):
        cx, cy = p.fw / 2, p.fh / 2
        dx, dy = p.x + .5 - cx, p.y + .5 - cy
        r = math.hypot(dx, dy) / (p.fw / 2)
        th = math.atan2(dy, dx) / (2 * math.pi)
        v = (r * 2.6 - th * 1.0 * 1.0) % 1.0
        base = mix("#f0d9a8", "#b8703a", 0.15 + 0.85 * (v > 0.6))
        c = shade(base, 0.9 + 0.2 * (1 - r) + 0.1 * hash01(p.x, p.y, p.fw))
        if r < 0.15: c = "#7a4622"
        return c
    ring = int(p.p[1]) % 3
    return mix("#b8703a", "#f0d9a8", 0.4 + 0.3 * (ring == 0)) if p.fw > 2 else "#b8703a"

skins = {"default": pelt("#e0b48a", "#c48f66", seed=241), "flesh": pelt("#e8a58a", "#cc8266", seed=241, spots=("#f6d0b8", 2.0, 0.65)), "shell": spiral,
         "shell_lip": pelt("#f0d9a8", "#d0b07a", seed=242), "eyestalk": pelt("#e8a58a", "#cc8266", seed=243), "eye_dark": eye_dark,
         "tent": pelt("#e8a58a", "#f3b7a0", seed=244, stripes=("#cc8266", 3.0, 0.5, "z"))}
SPEC = finish("ammonite", "Spiral Ammonite", ("#f0d9a8", "#b8703a"), bones, skins, an, STD_PLAY, {
    "role": "passive", "health": 8, "speed": 0.12, "box": [0.6, 0.8], "family": ["ammonite"],
    "loot": [("minecraft:nautilus_shell", 0, 1), ("minecraft:clay_ball", 0, 2)], "sound": ("turtle", [1.4, 1.7]),
    "spawn": {"biomes": ["beach", "swamp", "river"], "weight": 8, "herd": [1, 3]}})
