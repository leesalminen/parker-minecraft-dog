"""Scout Walker - rideable bipedal chicken-walker recon mech.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

HULL  = "#93a096"
DARK  = "#4c564f"
PLATE = "#7d877f"
GUN   = "#6a727a"
JOINT = "#1b2024"
PIST  = "#b9c2c6"
GLASS = "#7fe6ff"
AMBER = "#ffab3d"
RUST  = "#6d4527"
BADGE = "#e8e4d8"
RED   = "#b0392e"


# ----------------------------------------------------------------- painters
def panel(v, period=10.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, z, period=10.0, r=0.6):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def metal(p, base=HULL, dark=DARK, seed=11):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.2)
    c = mix(dark, base, 0.28 + 0.72 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 7, 1.1))
    if panel(x) or panel(y):
        c = shade(c, 0.58)
    if rivets(x, y, z):
        c = shade(c, 0.62)
    if p.face == "top":
        c = shade(c, 1.14)
    if p.face == "bottom":
        c = shade(c, 0.80)
    if hash01(x, y, z, seed + 3) > 0.955:
        c = shade(c, 1.30)
    if hash01(x, y, z, seed + 4) > 0.972:
        c = shade(c, 0.52)
    r = noise3(x, y, z, seed + 9, 1.6)
    if r > 0.80:
        c = mix(c, RUST, (r - 0.80) * 1.4)
    return c


def plate(p):
    return metal(p, PLATE, "#2c3531", 21)


def gun(p):
    return metal(p, GUN, "#20262a", 31)


def piston(p):
    x, y, z = p.p
    c = mix("#8f9aa0", PIST, 0.4 + 0.6 * noise3(x, y, z, 51, 2.4))
    if abs((y % 3.0) - 1.5) < 0.7:
        c = shade(c, 0.55)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def joint(p):
    x, y, z = p.p
    return shade(mix(JOINT, "#31383d", noise3(x, y, z, 61, 2.0)), 0.85 + 0.3 * noise3(x, y, z, 63, 1.0))


def glass(p):
    x, y, z = p.p
    c = mix("#16465e", GLASS, 0.35 + 0.65 * noise3(x, y, z, 71, 2.2))
    if abs((x % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.6)
    return glow(c)


def glowamber(p):
    x, y, z = p.p
    return glow(mix("#ff7a1f", "#ffe0a0", 0.4 + 0.6 * noise3(x, y, z, 81, 1.4)))


def hazard(p):
    x, y, z = p.p
    s = math.sin((x + z) * 1.35)
    c = "#d8b24a" if s > 0 else "#20242a"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def badge(p):
    x, y, z = p.p
    c = BADGE
    if y < 28.4 or y > 32.6 or z < -5.6 or z > 1.6:
        c = "#20242a"
    elif y > 30.4 and abs(z + 2.0) < 1.1:
        c = RED
    return shade(c, 0.93 + 0.14 * noise3(x, y, z, 99, 1.0))


def claw(p):
    x, y, z = p.p
    return shade(mix("#2a2f33", "#6b747a", noise3(x, y, z, 111, 1.6)), 0.9 + 0.2 * noise3(x, y, z, 113, 1.0))


def sym(cubes, c):
    """Append cube c and its explicit X mirror (framework forbids the 'mirror' flag)."""
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "hull")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- hull / body
body_cubes = [
    {"o": [-6, 24, -9], "s": [12, 12, 16], "skin": "hull"},
    {"o": [-5, 22, -8], "s": [10, 3, 14], "skin": "plate"},
    {"o": [-6, 28, -14], "s": [12, 8, 6], "skin": "plate", "rot": [-22, 0, 0], "pivot": [0, 32, -9]},
    {"o": [-5, 25, 6], "s": [10, 11, 6], "skin": "hull"},
    {"o": [-2, 36, -2], "s": [4, 2, 7], "skin": "plate"},
    {"o": [-4, 36, 4], "s": [2, 6, 2], "skin": "glow_vent"},
    {"o": [2, 36, 4], "s": [2, 6, 2], "skin": "glow_vent"},
    {"o": [-4.5, 42, 3.5], "s": [3, 2, 3], "skin": "joint"},
    {"o": [1.5, 42, 3.5], "s": [3, 2, 3], "skin": "joint"},
    {"o": [-1, 38, 7], "s": [2, 2, 3], "skin": "joint"},
]
sym(body_cubes, {"o": [6, 25, -8], "s": [2, 9, 11], "skin": "plate", "rot": [0, 0, -9], "pivot": [6, 30, -8]})
sym(body_cubes, {"o": [4, 23, -1], "s": [4, 4, 7], "skin": "joint"})
sym(body_cubes, {"o": [6.1, 28, -3], "s": [1, 5, 5], "skin": "badge"})
sym(body_cubes, {"o": [-4.6, 27, 11], "s": [3, 4, 1], "skin": "glow_vent"})
sym(body_cubes, {"o": [4.5, 32, 0], "s": [2, 2, 2], "skin": "hazard"})

# ----------------------------------------------------------------- neck collar
neck_cubes = [
    {"o": [-2, 36, -5], "s": [4, 7, 6], "skin": "joint"},
    {"o": [-3, 36, -5], "s": [6, 2, 6], "skin": "plate"},
]

# ----------------------------------------------------------------- cockpit head
head_cubes = [
    {"o": [-5, 40, -19], "s": [10, 9, 11], "skin": "hull", "rot": [-12, 0, 0], "pivot": [0, 44, -6]},
    {"o": [-3.5, 44, -20], "s": [7, 5, 1], "skin": "glass", "rot": [-12, 0, 0], "pivot": [0, 44, -6]},
    {"o": [-4, 39, -20], "s": [8, 3, 7], "skin": "joint", "rot": [-12, 0, 0], "pivot": [0, 44, -6]},
    {"o": [-1.5, 50, -11], "s": [3, 3, 4], "skin": "joint"},
    {"o": [-1, 50, -12.5], "s": [2, 2, 1], "skin": "glow_amber"},
]
# cockpit rim (open roof so the pilot is visible)
sym(head_cubes, {"o": [3, 48, -18], "s": [2, 3, 10], "skin": "plate", "rot": [-12, 0, 0], "pivot": [0, 44, -6]})
head_cubes.append({"o": [-3, 48, -10], "s": [6, 3, 4], "skin": "plate", "rot": [-12, 0, 0], "pivot": [0, 44, -6]})
head_cubes.append({"o": [-2, 47, -12], "s": [4, 2, 4], "skin": "joint", "rot": [-12, 0, 0], "pivot": [0, 44, -6]})
sym(head_cubes, {"o": [3, 42, -18], "s": [3, 5, 9], "skin": "plate", "rot": [-12, 0, 0], "pivot": [0, 44, -6]})
sym(head_cubes, {"o": [-1, 47, -12], "s": [1, 2, 1], "skin": "hazard"})

antenna_cubes = [
    {"o": [2, 51, -14], "s": [1, 5, 1], "skin": "piston"},
    {"o": [2, 56, -14], "s": [1, 1, 1], "skin": "glow_amber"},
]

# ----------------------------------------------------------------- chin cannons
cannon_l = [
    {"o": [2, 40, -29], "s": [3, 3, 10], "skin": "gun"},
    {"o": [2.5, 40.5, -36], "s": [2, 2, 7], "skin": "piston"},
    {"o": [2, 40, -38], "s": [3, 3, 2], "skin": "joint"},
    {"o": [2, 39, -28], "s": [3, 2, 5], "skin": "hazard"},
]
cannon_r = [
    {"o": [-5, 40, -29], "s": [3, 3, 10], "skin": "gun"},
    {"o": [-4.5, 40.5, -36], "s": [2, 2, 7], "skin": "piston"},
    {"o": [-5, 40, -38], "s": [3, 3, 2], "skin": "joint"},
    {"o": [-5, 39, -28], "s": [3, 2, 5], "skin": "hazard"},
]

# ----------------------------------------------------------------- legs (reverse-jointed, 3 segments)
thigh_l = [
    {"o": [3, 9, -3], "s": [4, 15, 6], "skin": "hull", "rot": [-14, 0, 0], "pivot": [5, 24, 1]},
    {"o": [6.5, 11, -3], "s": [2, 11, 6], "skin": "plate", "rot": [-14, 0, 0], "pivot": [5, 24, 1]},
    {"o": [3, 7, -6], "s": [4, 5, 5], "skin": "joint", "rot": [-14, 0, 0], "pivot": [5, 24, 1]},
    {"o": [3.5, 13, -5], "s": [3, 9, 3], "skin": "piston", "rot": [-14, 0, 0], "pivot": [5, 24, 1]},
]
thigh_r = [
    {"o": [-7, 9, -3], "s": [4, 15, 6], "skin": "hull", "rot": [-14, 0, 0], "pivot": [-5, 24, 1]},
    {"o": [-8.5, 11, -3], "s": [2, 11, 6], "skin": "plate", "rot": [-14, 0, 0], "pivot": [-5, 24, 1]},
    {"o": [-7, 7, -6], "s": [4, 5, 5], "skin": "joint", "rot": [-14, 0, 0], "pivot": [-5, 24, 1]},
    {"o": [-6.5, 13, -5], "s": [3, 9, 3], "skin": "piston", "rot": [-14, 0, 0], "pivot": [-5, 24, 1]},
]
shin_l = [
    {"o": [3, 0, -1], "s": [4, 11, 6], "skin": "hull", "rot": [16, 0, 0], "pivot": [5, 10, -2]},
    {"o": [6.5, 2, -1], "s": [2, 9, 6], "skin": "plate", "rot": [16, 0, 0], "pivot": [5, 10, -2]},
    {"o": [3, -1, -2], "s": [4, 4, 5], "skin": "joint", "rot": [16, 0, 0], "pivot": [5, 10, -2]},
    {"o": [3.5, 4, -4], "s": [3, 7, 2], "skin": "piston", "rot": [16, 0, 0], "pivot": [5, 10, -2]},
]
shin_r = [
    {"o": [-7, 0, -1], "s": [4, 11, 6], "skin": "hull", "rot": [16, 0, 0], "pivot": [-5, 10, -2]},
    {"o": [-8.5, 2, -1], "s": [2, 9, 6], "skin": "plate", "rot": [16, 0, 0], "pivot": [-5, 10, -2]},
    {"o": [-7, -1, -2], "s": [4, 4, 5], "skin": "joint", "rot": [16, 0, 0], "pivot": [-5, 10, -2]},
    {"o": [-6.5, 4, -4], "s": [3, 7, 2], "skin": "piston", "rot": [16, 0, 0], "pivot": [-5, 10, -2]},
]
foot_l = [
    {"o": [1, 0, -6], "s": [7, 4, 15], "skin": "hull"},
    {"o": [1, 0, -9], "s": [7, 2, 3], "skin": "plate"},
    {"o": [2, 0, 8], "s": [5, 3, 3], "skin": "joint"},
    {"o": [3, 2, 0], "s": [4, 3, 5], "skin": "joint"},
]
foot_r = [
    {"o": [-8, 0, -6], "s": [7, 4, 15], "skin": "hull"},
    {"o": [-8, 0, -9], "s": [7, 2, 3], "skin": "plate"},
    {"o": [-7, 0, 8], "s": [5, 3, 3], "skin": "joint"},
    {"o": [-7, 2, 0], "s": [4, 3, 5], "skin": "joint"},
]
for i in range(3):
    foot_l.append({"o": [1.6 + i * 2.0, 0, -10.2], "s": [1, 1, 2], "skin": "claw"})
    foot_r.append({"o": [-7.4 + i * 2.0, 0, -10.2], "s": [1, 1, 2], "skin": "claw"})

bones = [
    {"name": "body", "parent": None, "pivot": [0, 30, 0], "cubes": body_cubes},
    {"name": "neck", "parent": "body", "pivot": [0, 36, -3], "cubes": neck_cubes},
    {"name": "head", "parent": "neck", "pivot": [0, 40, -6], "cubes": head_cubes},
    {"name": "antenna", "parent": "head", "pivot": [2, 51, -14], "cubes": antenna_cubes},
    {"name": "cannon_l", "parent": "head", "pivot": [3.5, 41, -19], "cubes": cannon_l},
    {"name": "cannon_r", "parent": "head", "pivot": [-3.5, 41, -19], "cubes": cannon_r},
    {"name": "thigh_l", "parent": "body", "pivot": [5, 24, 1], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [5, 10, -2], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [5, 1, 1], "cubes": foot_l},
    {"name": "thigh_r", "parent": "body", "pivot": [-5, 24, 1], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-5, 10, -2], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-5, 1, 1], "cubes": foot_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=24, freq=42),
        {"shin_l": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 180) * 20 * query.modified_move_speed", "0", "0"]}},
        {"shin_r": {"rotation": ["math.cos(query.modified_distance_moved * 42) * 20 * query.modified_move_speed", "0", "0"]}},
        {"foot_l": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 90) * 12 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["math.cos(query.modified_distance_moved * 42 + 270) * 12 * query.modified_move_speed", "0", "0"]}},
        {"body": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 21)) * 0.9 * query.modified_move_speed", "0"]}},
        {"body": {"rotation": ["0", "0", "math.cos(query.modified_distance_moved * 21) * 3 * query.modified_move_speed"]}},
        {"neck": {"rotation": ["math.cos(query.modified_distance_moved * 42) * 2 * query.modified_move_speed", "0", "0"]}},
    )),
    "idle": anim(merge(
        bob("body", amp=0.55, rate=60),
        sway("head", amp=3.5, rate=42, axis=0),
        sway("antenna", amp=12, rate=110, axis=2, off=0.6),
        {"neck": {"rotation": ["math.sin(query.life_time * 50) * 1.5", "0", "0"]}},
        {"cannon_l": {"rotation": ["math.sin(query.life_time * 70) * 1.5", "0", "0"]}},
        {"cannon_r": {"rotation": ["math.sin(query.life_time * 70 + 1.3) * 1.5", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"cannon_l": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.2"]}},
        {"cannon_r": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.2"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 7", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * 4", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * -18"]}},
    ), loop=False),
}

SPEC = {
    "id": "walker",
    "name": "Scout Walker",
    "egg": ("#5b6a63", "#d8b24a"),
    "glow": True,
    "scale": 1.0,
    "visible": [4.0, 4.5, 1.8],
    "bones": bones,
    "skins": {"default": metal, "hull": metal, "plate": plate, "gun": gun, "piston": piston,
              "joint": joint, "glass": glass, "glow_amber": glowamber, "glow_vent": glowamber,
              "hazard": hazard, "badge": badge, "claw": claw},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 90, "speed": 0.32, "damage": 6, "box": [1.4, 3.0],
        "knockback_resist": 0.4, "family": ["mech"],
        "ride": {"seats": [[0, 2.6, -0.8]], "jump": 0.7},
        "loot": [("minecraft:iron_ingot", 2, 4), ("minecraft:redstone", 1, 3), ("minecraft:copper_ingot", 1, 2)],
        "sound": ("golem", [0.6, 0.8]),
        "xp": 8,
    },
}
