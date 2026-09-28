"""Titan Mech - enormous heavy assault boss mech with reactor core.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#7f8792"
DARK   = "#484d55"
PLATE  = "#6d747e"
GUN    = "#60666d"
JOINT  = "#171b20"
PIST   = "#c2ccd2"
CORE   = "#ffb43c"
CORE_H = "#fff0c0"
VISOR  = "#ff5a3c"
RUST   = "#6d4527"
HAZ    = "#d8b24a"
RED    = "#a8322c"
BADGE  = "#e8e4d8"


def panel(v, period=10.0, w=0.55):
    d = v % period
    return d < w or d > period - w


def rivets(x, y, z, period=10.0, r=0.6):
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    return dx < r and dz < r


def metal(p, base=STEEL, dark=DARK, seed=11):
    x, y, z = p.p
    n = noise3(x, y, z, seed, 3.6)
    c = mix(dark, base, 0.26 + 0.74 * n)
    c = shade(c, 0.90 + 0.20 * noise3(x, y, z, seed + 7, 1.1))
    if panel(x) or panel(y):
        c = shade(c, 0.72)
    if rivets(x, y, z):
        c = shade(c, 0.62)
    if p.face == "top":
        c = shade(c, 1.16)
    if p.face == "bottom":
        c = shade(c, 0.80)
    if hash01(x, y, z, seed + 3) > 0.952:
        c = shade(c, 1.32)
    if hash01(x, y, z, seed + 4) > 0.970:
        c = shade(c, 0.5)
    r = noise3(x, y, z, seed + 9, 1.8)
    if r > 0.80:
        c = mix(c, RUST, (r - 0.80) * 1.4)
    return c


def plate(p):
    return metal(p, PLATE, "#20252b", 21)


def gun(p):
    return metal(p, GUN, "#191d22", 31)


def piston(p):
    x, y, z = p.p
    c = mix("#8f9aa0", PIST, 0.35 + 0.65 * noise3(x, y, z, 51, 2.6))
    if abs((y % 4.0) - 2.0) < 0.8:
        c = shade(c, 0.5)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def joint(p):
    x, y, z = p.p
    return shade(mix(JOINT, "#2c333a", noise3(x, y, z, 61, 2.2)), 0.85 + 0.3 * noise3(x, y, z, 63, 1.0))


def core(p):
    x, y, z = p.p
    c = mix(CORE, CORE_H, 0.3 + 0.7 * noise3(x, y, z, 71, 2.6))
    d = math.hypot(x - 0.0, y - 68.0)
    if d < 2.2:
        c = shade(c, 1.15)
    return glow(c)


def ventglow(p):
    x, y, z = p.p
    return glow(mix("#ff7a1f", "#ffe0a0", 0.35 + 0.65 * noise3(x, y, z, 81, 1.5)))


def visor(p):
    x, y, z = p.p
    c = mix("#7a1a10", VISOR, 0.3 + 0.7 * noise3(x, y, z, 83, 2.0))
    if abs((x % 3.0) - 1.5) < 0.6:
        c = shade(c, 0.55)
    return glow(c)


def hazard(p):
    x, y, z = p.p
    s = math.sin((x + z) * 1.4)
    c = HAZ if s > 0 else "#1b1f24"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def badge(p):
    x, y, z = p.p
    c = BADGE
    if y < 62.4 or y > 67.6 or z < -3.6 or z > 1.6:
        c = "#1b1f24"
    elif y > 64.6 and abs(z + 1.0) < 1.2:
        c = RED
    return shade(c, 0.93 + 0.14 * noise3(x, y, z, 99, 1.0))


def sym(cubes, c):
    cubes.append(c)
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "steel")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    cubes.append(m)


# ----------------------------------------------------------------- pelvis
pelvis_cubes = [
    {"o": [-10, 42, -9], "s": [20, 12, 18], "skin": "steel"},
    {"o": [-9, 40, -8], "s": [18, 3, 16], "skin": "plate"},
    {"o": [-8, 54, -6], "s": [16, 3, 12], "skin": "plate"},
]
sym(pelvis_cubes, {"o": [9, 43, -8], "s": [3, 10, 14], "skin": "plate", "rot": [0, 0, -8], "pivot": [9, 48, -8]})
sym(pelvis_cubes, {"o": [7, 41, -1], "s": [5, 5, 9], "skin": "joint"})
sym(pelvis_cubes, {"o": [-5.5, 46, 10], "s": [5, 5, 1], "skin": "vent_glow"})

# ----------------------------------------------------------------- torso
torso_cubes = [
    {"o": [-11, 54, -10], "s": [22, 30, 20], "skin": "steel"},
    {"o": [-10, 52, -9], "s": [20, 4, 18], "skin": "plate"},
    {"o": [-11, 56, -13], "s": [22, 14, 5], "skin": "plate", "rot": [-14, 0, 0], "pivot": [0, 70, -10]},
    {"o": [-9, 78, -9], "s": [18, 6, 18], "skin": "plate"},
    {"o": [-3, 84, -4], "s": [6, 3, 10], "skin": "joint"},
]
sym(torso_cubes, {"o": [11, 58, -8], "s": [3, 22, 15], "skin": "plate", "rot": [0, 0, -6], "pivot": [11, 70, -8]})
sym(torso_cubes, {"o": [-7.5, 58, 11], "s": [5, 16, 1], "skin": "vent_glow"})
sym(torso_cubes, {"o": [7, 62, -11], "s": [4, 8, 2], "skin": "hazard"})
sym(torso_cubes, {"o": [12.1, 62, -3], "s": [1, 6, 6], "skin": "badge"})
sym(torso_cubes, {"o": [4, 76, -11], "s": [3, 3, 2], "skin": "joint"})

# ----------------------------------------------------------------- reactor core
core_cubes = [
    {"o": [-4, 62, -12], "s": [8, 8, 3], "skin": "core"},
    {"o": [-5, 61, -11], "s": [10, 10, 2], "skin": "joint"},
]
sym(core_cubes, {"o": [5, 63, -11], "s": [2, 6, 1], "skin": "piston"})

# ----------------------------------------------------------------- head
head_cubes = [
    {"o": [-5, 84, -9], "s": [10, 10, 12], "skin": "steel"},
    {"o": [-5, 92, -8], "s": [10, 3, 10], "skin": "plate"},
    {"o": [-4, 88, -10], "s": [8, 4, 1], "skin": "visor"},
    {"o": [-4, 85, -10], "s": [8, 2, 2], "skin": "joint"},
    {"o": [-1, 94, -4], "s": [2, 4, 8], "skin": "plate"},
]
sym(head_cubes, {"o": [3, 86, -9], "s": [3, 5, 7], "skin": "plate"})
sym(head_cubes, {"o": [3, 93, -6], "s": [1, 6, 1], "skin": "piston"})

# ----------------------------------------------------------------- shoulder missile pods
pod_l = [
    {"o": [12, 68, -8], "s": [10, 12, 16], "skin": "steel"},
    {"o": [12, 78, -7], "s": [10, 4, 14], "skin": "plate"},
    {"o": [13, 66, -9], "s": [8, 4, 3], "skin": "hazard"},
]
pod_r = [
    {"o": [-22, 68, -8], "s": [10, 12, 16], "skin": "steel"},
    {"o": [-22, 78, -7], "s": [10, 4, 14], "skin": "plate"},
    {"o": [-21, 66, -9], "s": [8, 4, 3], "skin": "hazard"},
]
# missile tubes (front face) - four per pod
for i in range(4):
    pod_l.append({"o": [13.5 + (i % 2) * 3, 71 + (i // 2) * 4, -9.5], "s": [2, 2, 2], "skin": "joint"})
    pod_r.append({"o": [-21.5 + (i % 2) * 3, 71 + (i // 2) * 4, -9.5], "s": [2, 2, 2], "skin": "joint"})

# ----------------------------------------------------------------- arms
arm_l_up = [
    {"o": [12, 54, -3], "s": [8, 18, 8], "skin": "steel"},
    {"o": [10, 68, -5], "s": [12, 6, 11], "skin": "plate"},
    {"o": [11, 56, -5], "s": [10, 4, 12], "skin": "plate"},
]
arm_l_fore = [
    {"o": [10, 40, -8], "s": [11, 14, 12], "skin": "steel"},
    {"o": [13, 42, -20], "s": [5, 5, 14], "skin": "gun"},
    {"o": [12.5, 41.5, -22], "s": [6, 6, 3], "skin": "joint"},
    {"o": [9, 44, -2], "s": [6, 7, 6], "skin": "joint"},
    {"o": [12, 41, -14], "s": [6, 2, 6], "skin": "hazard"},
]
arm_r_up = [
    {"o": [-20, 54, -3], "s": [8, 18, 8], "skin": "steel"},
    {"o": [-22, 68, -5], "s": [12, 6, 11], "skin": "plate"},
    {"o": [-21, 56, -5], "s": [10, 4, 12], "skin": "plate"},
]
arm_r_fore = [
    {"o": [-22, 40, -6], "s": [12, 14, 12], "skin": "steel"},
    {"o": [-23, 30, -8], "s": [14, 12, 16], "skin": "steel"},
    {"o": [-24, 31, -9], "s": [4, 4, 4], "skin": "joint"},
    {"o": [-15, 31, -9], "s": [4, 4, 4], "skin": "joint"},
    {"o": [-23, 30, -9], "s": [14, 2, 18], "skin": "plate"},
    {"o": [-21, 40, 4], "s": [10, 5, 4], "skin": "joint"},
]

# ----------------------------------------------------------------- exhaust stacks
exhaust_l = [
    {"o": [6, 84, 7], "s": [3, 14, 3], "skin": "steel"},
    {"o": [6, 96, 7], "s": [3, 3, 3], "skin": "plate"},
    {"o": [6.5, 97, 7.5], "s": [2, 2, 2], "skin": "vent_glow"},
]
exhaust_r = [
    {"o": [-9, 84, 7], "s": [3, 14, 3], "skin": "steel"},
    {"o": [-9, 96, 7], "s": [3, 3, 3], "skin": "plate"},
    {"o": [-8.5, 97, 7.5], "s": [2, 2, 2], "skin": "vent_glow"},
]

# ----------------------------------------------------------------- legs
thigh_l = [
    {"o": [4, 24, -3], "s": [10, 20, 10], "skin": "steel"},
    {"o": [3, 26, -6], "s": [12, 7, 6], "skin": "plate"},
    {"o": [12, 27, -4], "s": [3, 15, 3], "skin": "piston"},
    {"o": [3, 24, -6], "s": [12, 4, 12], "skin": "plate"},
]
thigh_r = [
    {"o": [-14, 24, -3], "s": [10, 20, 10], "skin": "steel"},
    {"o": [-15, 26, -6], "s": [12, 7, 6], "skin": "plate"},
    {"o": [-15, 27, -4], "s": [3, 15, 3], "skin": "piston"},
    {"o": [-15, 24, -6], "s": [12, 4, 12], "skin": "plate"},
]
shin_l = [
    {"o": [4, 8, -2], "s": [10, 16, 9], "skin": "steel"},
    {"o": [3, 10, -5], "s": [12, 6, 5], "skin": "plate"},
    {"o": [12, 10, -3], "s": [3, 12, 3], "skin": "piston"},
    {"o": [4, 8, -6], "s": [10, 3, 14], "skin": "plate"},
]
shin_r = [
    {"o": [-14, 8, -2], "s": [10, 16, 9], "skin": "steel"},
    {"o": [-15, 10, -5], "s": [12, 6, 5], "skin": "plate"},
    {"o": [-15, 10, -3], "s": [3, 12, 3], "skin": "piston"},
    {"o": [-14, 8, -6], "s": [10, 3, 14], "skin": "plate"},
]
foot_l = [
    {"o": [1, 0, -9], "s": [16, 8, 20], "skin": "steel"},
    {"o": [1, 0, -12], "s": [16, 4, 3], "skin": "plate"},
    {"o": [3, 0, 11], "s": [12, 5, 4], "skin": "joint"},
    {"o": [6, 6, 0], "s": [6, 3, 8], "skin": "joint"},
]
foot_r = [
    {"o": [-17, 0, -9], "s": [16, 8, 20], "skin": "steel"},
    {"o": [-17, 0, -12], "s": [16, 4, 3], "skin": "plate"},
    {"o": [-15, 0, 11], "s": [12, 5, 4], "skin": "joint"},
    {"o": [-12, 6, 0], "s": [6, 3, 8], "skin": "joint"},
]
for i in range(4):
    foot_l.append({"o": [2 + i * 3.6, 0, -13.4], "s": [2, 2, 3], "skin": "joint"})
    foot_r.append({"o": [-16 + i * 3.6, 0, -13.4], "s": [2, 2, 3], "skin": "joint"})

bones = [
    {"name": "pelvis", "parent": None, "pivot": [0, 48, 0], "cubes": pelvis_cubes},
    {"name": "torso", "parent": "pelvis", "pivot": [0, 56, 0], "cubes": torso_cubes},
    {"name": "core", "parent": "torso", "pivot": [0, 68, -10], "cubes": core_cubes},
    {"name": "head", "parent": "torso", "pivot": [0, 84, -4], "cubes": head_cubes},
    {"name": "pod_l", "parent": "torso", "pivot": [14, 74, 0], "cubes": pod_l},
    {"name": "pod_r", "parent": "torso", "pivot": [-14, 74, 0], "cubes": pod_r},
    {"name": "arm_l_up", "parent": "torso", "pivot": [14, 72, 0], "cubes": arm_l_up},
    {"name": "arm_l_fore", "parent": "arm_l_up", "pivot": [14, 54, 0], "cubes": arm_l_fore},
    {"name": "arm_r_up", "parent": "torso", "pivot": [-14, 72, 0], "cubes": arm_r_up},
    {"name": "arm_r_fore", "parent": "arm_r_up", "pivot": [-14, 54, 0], "cubes": arm_r_fore},
    {"name": "exhaust_l", "parent": "torso", "pivot": [7, 84, 8], "cubes": exhaust_l},
    {"name": "exhaust_r", "parent": "torso", "pivot": [-8, 84, 8], "cubes": exhaust_r},
    {"name": "thigh_l", "parent": "pelvis", "pivot": [9, 44, 0], "cubes": thigh_l},
    {"name": "shin_l", "parent": "thigh_l", "pivot": [9, 24, 0], "cubes": shin_l},
    {"name": "foot_l", "parent": "shin_l", "pivot": [9, 8, 0], "cubes": foot_l},
    {"name": "thigh_r", "parent": "pelvis", "pivot": [-9, 44, 0], "cubes": thigh_r},
    {"name": "shin_r", "parent": "thigh_r", "pivot": [-9, 24, 0], "cubes": shin_r},
    {"name": "foot_r", "parent": "shin_r", "pivot": [-9, 8, 0], "cubes": foot_r},
]

anims = {
    "walk": anim(merge(
        biped_walk("thigh_l", "thigh_r", amp=16, freq=30),
        {"shin_l": {"rotation": ["math.cos(query.modified_distance_moved * 30 + 180) * 16 * query.modified_move_speed", "0", "0"]}},
        {"shin_r": {"rotation": ["math.cos(query.modified_distance_moved * 30) * 16 * query.modified_move_speed", "0", "0"]}},
        {"foot_l": {"rotation": ["math.cos(query.modified_distance_moved * 30 + 90) * 8 * query.modified_move_speed", "0", "0"]}},
        {"foot_r": {"rotation": ["math.cos(query.modified_distance_moved * 30 + 270) * 8 * query.modified_move_speed", "0", "0"]}},
        {"pelvis": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 15)) * 1.6 * query.modified_move_speed", "0"]}},
        {"torso": {"rotation": ["math.cos(query.modified_distance_moved * 30) * 3 * query.modified_move_speed", "0", "math.cos(query.modified_distance_moved * 15) * 4 * query.modified_move_speed"]}},
        {"arm_l_up": {"rotation": ["math.cos(query.modified_distance_moved * 30) * 10 * query.modified_move_speed", "0", "0"]}},
        {"arm_r_up": {"rotation": ["math.cos(query.modified_distance_moved * 30 + 180) * 10 * query.modified_move_speed", "0", "0"]}},
        {"head": {"rotation": ["math.cos(query.modified_distance_moved * 30) * 2 * query.modified_move_speed", "0", "0"]}},
    )),
    "idle": anim(merge(
        bob("pelvis", amp=0.7, rate=40),
        sway("torso", amp=1.6, rate=35, axis=0),
        sway("head", amp=4.0, rate=30, axis=1),
        {"core": {"position": ["0", "math.sin(query.life_time * 110) * 0.4", "0"]}},
        {"core": {"rotation": ["0", "math.sin(query.life_time * 55) * 4", "0"]}},
        sway("exhaust_l", amp=1.5, rate=70, axis=2),
        sway("exhaust_r", amp=1.5, rate=70, axis=2, off=1.4),
        {"pod_l": {"rotation": ["math.sin(query.life_time * 40) * 2", "0", "0"]}},
        {"pod_r": {"rotation": ["math.sin(query.life_time * 40 + 2.0) * 2", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"arm_r_up": {"rotation": ["math.sin(variable.attack_time * 180) * -40", "0", "0"]}},
        {"arm_r_fore": {"rotation": ["math.sin(variable.attack_time * 180) * -55", "0", "0"]}},
        {"arm_l_up": {"rotation": ["math.sin(variable.attack_time * 180) * 20", "0", "0"]}},
        {"torso": {"rotation": ["math.sin(variable.attack_time * 180) * 14", "0", "0"]}},
        {"pelvis": {"rotation": ["math.sin(variable.attack_time * 180) * 6", "0", "0"]}},
        {"core": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 1.5"]}},
        {"head": {"rotation": ["math.sin(variable.attack_time * 180) * 6", "0", "0"]}},
    ), loop=False),
}

SPEC = {
    "id": "titan",
    "name": "Titan Mech",
    "egg": ("#3a4048", "#ffb43c"),
    "glow": True,
    "scale": 1.0,
    "visible": [6.0, 7.0, 3.5],
    "bones": bones,
    "skins": {"default": metal, "steel": metal, "plate": plate, "gun": gun, "piston": piston,
              "joint": joint, "core": core, "vent_glow": ventglow, "visor": visor,
              "hazard": hazard, "badge": badge},
    "anims": anims,
    "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "boss",
        "health": 500, "speed": 0.22, "damage": 14, "box": [3.0, 6.0],
        "knockback_resist": 1.0, "fire_immune": True, "boss": True, "family": ["mech"],
        "reach": 1.6,
        "loot": [("minecraft:iron_block", 3, 6), ("minecraft:redstone_block", 2, 4),
                 ("minecraft:netherite_scrap", 1, 2), ("minecraft:copper_ingot", 4, 8)],
        "sound": ("golem", [0.4, 0.55]),
        "xp": 120,
    },
}
