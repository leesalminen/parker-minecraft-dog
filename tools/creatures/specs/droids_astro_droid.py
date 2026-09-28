"""Astro Droid - small tameable astromech companion.  Model faces -Z, y up, ground y=0. 1 unit = 1/16 block."""
import math
from lib import *

BLUE    = "#2f63c8"
BLUE_D  = "#173a80"
SILVER  = "#c9ced6"
SILVER_D= "#828a95"
DARK    = "#333a44"
EYE     = "#7fd8ff"
HOLO    = "#a8ecff"
WHITE   = "#eef2f6"


def panel(v, period=12.0, w=0.6):
    d = v % period
    return d < w or d > period - w


def rivets(x, z, period=12.0, r=0.7):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def paint(p, base, dark, seed, blue_band=None):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 4.0)
    c = mix(dark, base, 0.30 + 0.70 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 5, 1.1))
    if blue_band and blue_band[0] < y < blue_band[1]:
        c = mix(c, BLUE, 0.75)
    if panel(x) or panel(z):
        c = shade(c, 0.74)
    if rivets(x, z):
        c = shade(c, 0.60)
    if hash01(x, y, z, seed + 2) > 0.960:
        c = shade(c, 1.26)
    if hash01(x, y, z, seed + 3) > 0.976:
        c = shade(c, 0.45)
    if p.face == "top":
        c = shade(c, 1.14)
    if p.face == "bottom":
        c = shade(c, 0.78)
    return c


def metal(p):
    return paint(p, SILVER, SILVER_D, 11)


def blue(p):
    x, y, z = p.p
    c = mix(BLUE_D, BLUE, 0.35 + 0.65 * noise3(x, y, z, 23, 3.2))
    c = shade(c, 0.92 + 0.16 * noise3(x, y, z, 29, 1.0))
    if panel(y, 9.0):
        c = shade(c, 0.80)
    if hash01(x, y, z, 33) > 0.965:
        c = shade(c, 1.30)
    if hash01(x, y, z, 37) > 0.975:
        c = shade(c, 0.55)
    if p.face == "top":
        c = shade(c, 1.12)
    if p.face == "bottom":
        c = shade(c, 0.80)
    return c


def dark(p):
    x, y, z = p.p
    c = mix("#1d222a", DARK, 0.3 + 0.7 * noise3(x, y, z, 41, 3.0))
    if abs((y % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.55)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 43, 1.2))


def eye(p):
    x, y, z = p.p
    return glow(mix("#cdf4ff", EYE, 0.35 + 0.65 * noise3(x, y, z, 51, 2.2)))


def holo(p):
    x, y, z = p.p
    return glow(mix("#dffaff", HOLO, 0.3 + 0.7 * noise3(x, y, z, 53, 2.6)))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "metal")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ---------------------------------------------------------------- legs
leg_l = [
    {"o": [4, 0, -5], "s": [4, 2, 10], "skin": "metal"},
    {"o": [4, 0, -5], "s": [4, 2, 3], "skin": "blue"},
    {"o": [4, 2, -2], "s": [2, 5, 4], "skin": "metal"},
    {"o": [4, 7, -3], "s": [4, 2, 6], "skin": "dark"},
    {"o": [5, 3, -1], "s": [2, 3, 2], "skin": "blue"},
]
leg_r = []
for c in leg_l:
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c["skin"]}
    leg_r.append(m)

leg_c = [
    {"o": [-1.5, 0, -1.5], "s": [3, 7, 3], "skin": "metal"},
    {"o": [-2, 0, -3], "s": [4, 2, 6], "skin": "dark"},
    {"o": [-1, 1, -3], "s": [2, 1, 1], "skin": "blue"},
]

# ---------------------------------------------------------------- body
body_cubes = [
    {"o": [-5, 7, -5], "s": [10, 7, 10], "skin": "metal"},
    {"o": [-4, 6, -4], "s": [8, 2, 8], "skin": "dark"},
    {"o": [-5, 13, -5], "s": [10, 1, 10], "skin": "blue"},
    {"o": [-3, 8, -6], "s": [6, 5, 2], "skin": "blue"},
    {"o": [-2, 9.5, -7], "s": [4, 2, 1], "skin": "dark"},
    {"o": [-1.5, 10, -7.6], "s": [3, 1, 1], "skin": "holo"},
    {"o": [-4, 7, 5], "s": [8, 3, 1], "skin": "dark"},
    {"o": [-3.5, 8, 5.4], "s": [2, 2, 1], "skin": "metal"},
    {"o": [1.5, 8, 5.4], "s": [2, 2, 1], "skin": "metal"},
    {"o": [3, 8, -5], "s": [2, 2, 2], "skin": "dark"},
]
sym(body_cubes, {"o": [-5, 8, -5], "s": [2, 2, 2], "skin": "dark"})
sym(body_cubes, {"o": [5, 9, -1], "s": [2, 4, 2], "skin": "blue", "rot": [0, 0, -12], "pivot": [6, 13, -1]})
sym(body_cubes, {"o": [-5, 10, -4], "s": [2, 3, 8], "skin": "dark"})
sym(body_cubes, {"o": [3, 6.2, 2], "s": [2, 1, 6], "skin": "dark"})

# ---------------------------------------------------------------- dome head
head_cubes = [
    {"o": [-4, 14, -4], "s": [8, 2, 8], "skin": "metal"},
    {"o": [-3, 16, -3], "s": [6, 1, 6], "skin": "blue"},
    {"o": [-2, 17, -2], "s": [4, 1, 4], "skin": "metal"},
    {"o": [-1, 18, -1], "s": [2, 1, 2], "skin": "blue"},
    {"o": [-2, 15.5, -4.5], "s": [4, 3, 1], "skin": "dark"},
    {"o": [3.5, 15, -1], "s": [1, 2, 4], "skin": "metal"},
]
sym(head_cubes, {"o": [-4, 15, 2], "s": [2, 3, 2], "skin": "dark"})

eye_cubes = [
    {"o": [-1.5, 15.7, -5], "s": [3, 2, 1], "skin": "eye"},
]

holo_cubes = [
    {"o": [-1, 19, -1], "s": [2, 1, 2], "skin": "holo"},
    {"o": [-0.5, 19.6, -0.5], "s": [1, 1, 1], "skin": "dark"},
    {"o": [-2, 19, -2], "s": [4, 1, 1], "skin": "metal"},
]

# ---------------------------------------------------------------- utility arm
arm_up = [
    {"o": [5, 9, -4], "s": [2, 4, 2], "skin": "metal"},
    {"o": [5, 12, -4], "s": [2, 2, 3], "skin": "dark"},
]
arm_fore = [
    {"o": [5, 5, -4], "s": [2, 4, 2], "skin": "metal"},
    {"o": [5, 4, -5], "s": [2, 2, 2], "skin": "blue"},
    {"o": [5, 3, -6], "s": [2, 2, 2], "skin": "holo"},
]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 7, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 14, 0], "cubes": head_cubes},
    {"name": "eye", "parent": "head", "pivot": [0, 16, -4], "cubes": eye_cubes},
    {"name": "holo", "parent": "head", "pivot": [0, 19, 0], "cubes": holo_cubes},
    {"name": "arm_up", "parent": "body", "pivot": [6, 13, -4], "cubes": arm_up},
    {"name": "arm_fore", "parent": "arm_up", "pivot": [6, 9, -4], "cubes": arm_fore},
    {"name": "leg_c", "parent": "body", "pivot": [0, 7, 0], "cubes": leg_c},
    {"name": "leg_l", "parent": "body", "pivot": [6, 9, 0], "cubes": leg_l},
    {"name": "leg_r", "parent": "body", "pivot": [-6, 9, 0], "cubes": leg_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("leg_l", "leg_r", amp=24, freq=45),
        {"leg_c": {"rotation": ["math.cos(query.modified_distance_moved * 45 + 90) * 18 * query.modified_move_speed", "0", "0"]}},
        {"body": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 22) * 7 * query.modified_move_speed"]}},
        {"arm_up": {"rotation": ["math.cos(query.modified_distance_moved * 45 + 180) * 8 * query.modified_move_speed", "0", "0"]}},
        {"holo": {"rotation": ["0", "math.sin(query.life_time * 90) * 25", "0"]}},
    )),
    "idle": anim(merge(
        bob("body", amp=0.6, rate=45),
        sway("arm_up", amp=4, rate=40, axis=0),
        {"arm_fore": {"rotation": ["math.sin(query.life_time * 40 + 1.2) * 3", "0", "0"]}},
        {"holo": {"rotation": ["0", "math.sin(query.life_time * 55) * 30", "0"]}},
        {"eye": {"position": ["0", "0", "math.sin(query.life_time * 80) * 0.15"]}},
        {"leg_c": {"rotation": ["-10", "0", "0"]}},
        {"body": {"rotation": ["math.sin(query.life_time * 40) * 1.5", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"arm_up": {"rotation": ["math.sin(variable.attack_time * 180) * -70", "0", "0"]}},
        {"arm_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -45", "0", "0"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 12", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * 5", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "astro_droid",
    "name": "Astro Droid",
    "egg": ("#2f63c8", "#c9ced6"),
    "glow": True,
    "scale": 1.0,
    "visible": [1.6, 1.7, 0.6],
    "bones": bones,
    "skins": {"default": metal, "metal": metal, "blue": blue, "dark": dark, "eye": eye, "holo": holo},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "companion",
        "health": 20, "speed": 0.30, "box": [0.6, 1.2],
        "tame_items": ["minecraft:redstone"],
        "family": ["droid", "astromech"],
        "sound": ("vex", [1.35, 1.6]),
        "xp": 3,
    },
}
