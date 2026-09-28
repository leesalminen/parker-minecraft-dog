"""Destroyer Droid - hostile armoured roller (unfurled crouched walker) with twin shoulder cannons.
Model faces -Z, y up, ground y=0. 1 unit = 1/16 block."""
import math
from lib import *

ARMOR  = "#7d8794"
ARMOR_D= "#474f59"
PLATE  = "#9aa3ad"
DARK   = "#242930"
LIGHT  = "#c3ccd6"
TRIM   = "#c2a24a"
RUST   = "#7a4a28"
BLUE   = "#5ec8ff"
RED    = "#ff3b30"
RED_H  = "#ffc0b0"


def panel(v, period=9.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, z, period=9.0, r=0.6):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def paint(p, base, dark, seed):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.6)
    c = mix(dark, base, 0.28 + 0.72 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 5, 1.1))
    if panel(x) or panel(z):
        c = shade(c, 0.74)
    if rivets(x, z):
        c = shade(c, 0.58)
    if hash01(x, y, z, seed + 2) > 0.955:
        c = shade(c, 1.30)
    if hash01(x, y, z, seed + 3) > 0.970:
        c = shade(c, 0.45)
    r = noise3(x, y, z, seed + 9, 1.8)
    if r > 0.84:
        c = mix(c, RUST, (r - 0.84) * 1.6)
    if p.face == "top":
        c = shade(c, 1.12)
    if p.face == "bottom":
        c = shade(c, 0.78)
    return c


def armor(p):
    return paint(p, ARMOR, ARMOR_D, 11)


def plate(p):
    return paint(p, PLATE, "#4a525c", 21)


def dark(p):
    x, y, z = p.p
    c = mix("#15181c", DARK, 0.3 + 0.7 * noise3(x, y, z, 31, 3.2))
    if abs((z % 4.0) - 2.0) < 0.7:
        c = shade(c, 0.65)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 33, 1.2))


def light(p):
    return paint(p, LIGHT, "#7d8794", 41)


def trim(p):
    x, y, z = p.p
    c = mix("#8a6f26", TRIM, 0.3 + 0.7 * noise3(x, y, z, 51, 3.0))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.2))


def blue(p):
    x, y, z = p.p
    return glow(mix("#dff4ff", BLUE, 0.25 + 0.75 * noise3(x, y, z, 61, 2.4)))


def redeye(p):
    x, y, z = p.p
    return glow(mix(RED_H, RED, 0.25 + 0.75 * noise3(x, y, z, 63, 2.2)))


def mir(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "armor")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def mirror(cubes):
    return [mir(c) for c in cubes]


def sym(cubes, c):
    cubes.append(c)
    cubes.append(mir(c))


# ---------------------------------------------------------------- legs (tripod: two front + one rear)
thigh_l = [
    {"o": [4, 6, -4], "s": [5, 6, 8], "skin": "armor"},
    {"o": [4, 9, -4], "s": [5, 2, 8], "skin": "dark"},
    {"o": [8, 7, -2], "s": [2, 4, 4], "skin": "light"},
]
shin_l = [
    {"o": [5, 2, -3], "s": [3, 4, 6], "skin": "armor"},
    {"o": [5, 3, -3], "s": [3, 2, 1], "skin": "dark"},
    {"o": [5, 2, 1], "s": [3, 3, 2], "skin": "light"},
]
foot_l = [
    {"o": [3, 0, -6], "s": [7, 2, 12], "skin": "armor"},
    {"o": [3, 0, -6], "s": [7, 1, 3], "skin": "dark"},
    {"o": [3, 0, 6], "s": [7, 1, 3], "skin": "dark"},
]
thigh_r, shin_r, foot_r = mirror(thigh_l), mirror(shin_l), mirror(foot_l)

thigh_c = [
    {"o": [-3, 6, 3], "s": [6, 6, 6], "skin": "armor"},
    {"o": [-3, 9, 3], "s": [6, 2, 6], "skin": "dark"},
]
shin_c = [
    {"o": [-2, 2, 4], "s": [4, 4, 6], "skin": "armor"},
    {"o": [-2, 3, 4], "s": [4, 2, 1], "skin": "dark"},
]
foot_c = [
    {"o": [-3, 0, 4], "s": [6, 2, 10], "skin": "armor"},
    {"o": [-3, 0, 12], "s": [6, 1, 3], "skin": "dark"},
    {"o": [-3, 0, 4], "s": [6, 2, 1], "skin": "trim"},
]

# ---------------------------------------------------------------- body
body_cubes = [
    {"o": [-7, 9, -6], "s": [14, 10, 12], "skin": "armor"},
    {"o": [-6, 18, -5], "s": [12, 2, 10], "skin": "plate"},
    {"o": [-7.5, 12, -6.5], "s": [15, 4, 13], "skin": "dark"},
    {"o": [-7, 9, -6], "s": [14, 2, 12], "skin": "dark"},
    {"o": [-5, 11, -6.5], "s": [10, 6, 1], "skin": "plate"},
    {"o": [-4, 12, -7.2], "s": [8, 3, 1], "skin": "trim"},
    {"o": [-3, 9, 6], "s": [6, 4, 1], "skin": "dark"},
]
sym(body_cubes, {"o": [7, 13, -5], "s": [2, 4, 4], "skin": "light"})
sym(body_cubes, {"o": [6.5, 14, -6.5], "s": [2, 3, 3], "skin": "blue"})
sym(body_cubes, {"o": [4, 15, 6], "s": [3, 4, 1], "skin": "trim"})

# ---------------------------------------------------------------- sensor head
head_cubes = [
    {"o": [-3, 19, -3], "s": [6, 4, 6], "skin": "armor"},
    {"o": [-2.5, 22, -2.5], "s": [5, 1, 5], "skin": "plate"},
    {"o": [-2, 20.5, -3.6], "s": [4, 2, 1], "skin": "dark"},
    {"o": [-1.5, 21, -4], "s": [3, 1, 1], "skin": "redeye"},
    {"o": [-1, 23, -1], "s": [2, 2, 2], "skin": "dark"},
    {"o": [-0.5, 25, -0.5], "s": [1, 1, 1], "skin": "blue"},
]

# ---------------------------------------------------------------- twin shoulder cannons
cannon_l = [
    {"o": [5, 17, -6], "s": [4, 5, 7], "skin": "armor"},
    {"o": [5, 17, -6], "s": [4, 1, 7], "skin": "trim"},
    {"o": [5, 19, -14], "s": [3, 3, 8], "skin": "dark"},
    {"o": [4.5, 19, -16], "s": [4, 3, 2], "skin": "blue"},
    {"o": [5, 20, -7], "s": [3, 3, 4], "skin": "light"},
]
cannon_r = mirror(cannon_l)

# ---------------------------------------------------------------- wheel-plate hoop (rolls when moving)
HOOP_C = (0.0, 14.0, 8.0)
HR = 10.0
hoop_cubes = []
N = 12
for i in range(N):
    th = math.radians(i * (360.0 / N))
    cy = HOOP_C[1] + HR * math.cos(th)
    cz = HOOP_C[2] + HR * math.sin(th)
    hoop_cubes.append({"o": [-1, cy - 2, cz - 2.5], "s": [2, 4, 5], "skin": "armor",
                       "rot": [i * (360.0 / N), 0, 0], "pivot": [0, cy, cz]})
for i in range(4):
    th = math.radians(i * 90.0 + 45.0)
    cy = HOOP_C[1] + (HR * 0.5) * math.cos(th)
    cz = HOOP_C[2] + (HR * 0.5) * math.sin(th)
    hoop_cubes.append({"o": [-0.5, cy - 4.5, cz - 0.5], "s": [1, 9, 1], "skin": "light",
                       "rot": [i * 90.0 + 45.0, 0, 0], "pivot": [0, cy, cz]})
hoop_cubes += [
    {"o": [-1.5, 12.5, 6.5], "s": [3, 3, 3], "skin": "dark"},
    {"o": [-0.5, 13.5, 7.5], "s": [1, 1, 1], "skin": "blue"},
]
for i in range(4):
    th = math.radians(i * 90.0)
    cy = HOOP_C[1] + (HR + 1.0) * math.cos(th)
    cz = HOOP_C[2] + (HR + 1.0) * math.sin(th)
    hoop_cubes.append({"o": [-1, cy - 1, cz - 1], "s": [2, 2, 2], "skin": "blue",
                       "rot": [i * 90.0, 0, 0], "pivot": [0, cy, cz]})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 12, 0], "cubes": body_cubes},
    {"name": "head", "parent": "body", "pivot": [0, 19, 0], "cubes": head_cubes},
    {"name": "cannon_l", "parent": "body", "pivot": [6, 19, 0], "cubes": cannon_l},
    {"name": "cannon_r", "parent": "body", "pivot": [-6, 19, 0], "cubes": cannon_r},
    {"name": "hoop", "parent": "body", "pivot": [0, 14, 8], "cubes": hoop_cubes},
    {"name": "thigh_l", "parent": "body", "pivot": [6, 12, 0], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [6, 6, 0], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [6, 2, 0], "cubes": foot_l},
    {"name": "thigh_r", "parent": "body", "pivot": [-6, 12, 0], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-6, 6, 0], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-6, 2, 0], "cubes": foot_r},
    {"name": "thigh_c", "parent": "body", "pivot": [0, 12, 6], "cubes": thigh_c},
    {"name": "shin_c", "parent": "thigh_c", "pivot": [0, 6, 6], "cubes": shin_c},
    {"name": "foot_c", "parent": "shin_c", "pivot": [0, 2, 6], "cubes": foot_c},
]

anims = {
    "walk": anim(merge(
        hex_walk(["thigh_l", "thigh_c", "thigh_r"], amp=22, freq=34),
        {"shin_l": {"rotation": ["math.cos(query.modified_distance_moved * 34 + 180) * 14 * query.modified_move_speed", "0", "0"]}},
        {"shin_r": {"rotation": ["math.cos(query.modified_distance_moved * 34) * 14 * query.modified_move_speed", "0", "0"]}},
        {"shin_c": {"rotation": ["math.cos(query.modified_distance_moved * 34 + 90) * 12 * query.modified_move_speed", "0", "0"]}},
        {"foot_l": {"rotation": ["math.cos(query.modified_distance_moved * 34 + 90) * 8 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["math.cos(query.modified_distance_moved * 34 + 270) * 8 * query.modified_move_speed", "0", "0"]}},
        {"body": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 17)) * 1.2 * query.modified_move_speed", "0"]}},
        {"body": {"rotation": ["math.cos(query.modified_distance_moved * 34) * 3 * query.modified_move_speed", "0", "math.cos(query.modified_distance_moved * 17) * 4 * query.modified_move_speed"]}},
        {"hoop": {"rotation": ["query.modified_distance_moved * 7", "0", "0"]}},
        {"cannon_l": {"rotation": ["math.cos(query.modified_distance_moved * 34) * 4 * query.modified_move_speed", "0", "0"]}},
        {"cannon_r": {"rotation": ["math.cos(query.modified_distance_moved * 34 + 180) * 4 * query.modified_move_speed", "0", "0"]}},
    )),
    "idle": anim(merge(
        bob("body", amp=0.9, rate=36),
        sway("body", amp=2.0, rate=28, axis=0),
        {"head": {"rotation": ["math.sin(query.life_time * 24) * 4", "math.sin(query.life_time * 20) * 16", "0"]}},
        {"hoop": {"rotation": ["math.sin(query.life_time * 18) * 3", "0", "0"]}},
        {"cannon_l": {"rotation": ["math.sin(query.life_time * 26 + 1.0) * 3", "0", "0"]}},
        {"cannon_r": {"rotation": ["math.sin(query.life_time * 26 + 2.4) * 3", "0", "0"]}},
        {"thigh_l": {"rotation": ["math.sin(query.life_time * 26) * 2", "0", "0"]}},
        {"thigh_r": {"rotation": ["math.sin(query.life_time * 26 + 3.0) * 2", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"cannon_l": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.5"]}},
        {"cannon_r": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.5"]}},
        {"cannon_l": {"rotation": ["math.sin(variable.attack_time * 180) * -6", "0", "0"]}},
        {"cannon_r": {"rotation": ["math.sin(variable.attack_time * 180) * -6", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -8", "0", "0"]}},
        {"body": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 1.5"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * -6", "0", "0"]}},
        {"hoop": {"rotation": ["math.sin(variable.attack_time * 180) * -8", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "destroyer_droid",
    "name": "Destroyer Droid",
    "egg": ("#7d8794", "#5ec8ff"),
    "glow": True,
    "scale": 1.0,
    "visible": [3.6, 3.4, 1.3],
    "bones": bones,
    "skins": {"default": armor, "armor": armor, "plate": plate, "dark": dark, "light": light,
              "trim": trim, "blue": blue, "redeye": redeye},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "hostile",
        "health": 70, "speed": 0.24, "damage": 5, "box": [1.2, 1.4],
        "knockback_resist": 0.5,
        "ranged": True, "range": 20, "projectile": "minecraft:arrow",
        "family": ["droid", "destroyer"],
        "loot": [("minecraft:iron_ingot", 2, 4), ("minecraft:redstone", 1, 4),
                 ("minecraft:copper_ingot", 1, 3), ("minecraft:gold_nugget", 0, 3)],
        "sound": ("golem", [0.75, 0.95]),
        "xp": 20,
    },
}
