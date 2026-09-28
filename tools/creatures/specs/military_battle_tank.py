"""Ironclad Battle Tank - rideable tracked MBT with rotating turret.  Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#7c848c"
DARK   = "#3a4046"
PLATE  = "#8f979e"
STRUCT = "#4a5058"
TRACK  = "#24272c"
HAZ    = "#d8b24a"
OLIVE  = "#5c6a44"
LIGHT  = "#fff0c4"
OPTIC  = "#8fd8ff"
VENT   = "#ff8a2a"
HOT    = "#ffe0a0"


def armor(p, base=STEEL, dark=DARK, seed=11, period=16.0, edge=1.0):
    x, y, z = p.p
    c = mix(base, dark, 0.18 + 0.55 * noise3(x, y, z, seed, 3.2))
    if (x % period) < edge or (y % period) < edge or (z % period) < edge:
        c = shade(c, 0.62)
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    if dx < 0.9 and dz < 0.9:
        c = shade(c, 0.8)
    h = hash01(x, y, z, seed)
    if h > 0.93:
        c = shade(c, 0.74)
    elif h < 0.05:
        c = mix(c, "#7a6a52", 0.5)
    return shade(c, 0.92 + 0.18 * noise3(x, y, z, seed + 3, 1.0))


def steel(p):  return armor(p, STEEL, DARK, 11)
def plate(p):  return armor(p, PLATE, "#20252b", 21, 12.0)
def struct(p): return armor(p, STRUCT, "#1b1f24", 31, 9.0)


def gun(p):
    x, y, z = p.p
    c = mix("#565c63", "#22262b", 0.25 + 0.6 * noise3(x, y, z, 41, 2.5))
    if abs((z % 7.0) - 3.5) < 0.6:
        c = shade(c, 0.68)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 43, 1.0))


def track(p):
    x, y, z = p.p
    c = mix(TRACK, "#3a4047", 0.3 + 0.6 * noise3(x, y, z, 51, 2.2))
    if math.sin(z * 1.35) > 0.2:
        c = shade(c, 0.72)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def wheel(p):
    x, y, z = p.p
    if p.face in ("east", "west"):
        dx, dy = p.x - p.fw / 2.0, p.y - p.fh / 2.0
        r = math.hypot(dx, dy)
        a = math.atan2(dy, dx)
        if r > 3.3:
            c = mix("#1b1e22", "#33383e", 0.3 + 0.5 * noise3(x, y, z, 7, 2.0))
            if (r * 3.0) % 2.0 < 0.6:
                c = shade(c, 0.68)
        else:
            c = mix("#6b7078", "#2c3036", 0.3 + 0.4 * noise3(x, y, z, 9, 2.0))
            k = ((a + math.pi) / (math.pi / 2.0)) % 1.0
            if k < 0.2 or k > 0.8:
                c = shade(c, 0.55)
            if r < 1.1:
                c = shade(c, 0.45)
    else:
        c = mix("#181b1f", "#2a2f34", 0.3 + 0.6 * noise3(x, y, z, 11, 2.0))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 13, 1.0))


def skirt(p):
    x, y, z = p.p
    if 10.0 <= y <= 12.5:
        c = HAZ if math.sin(z * 1.5) > 0 else "#16181c"
    else:
        c = armor(p, PLATE, "#262b31", 61, 14.0)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 63, 1.0))


def stowage(p):
    x, y, z = p.p
    c = mix(OLIVE, "#3a442c", 0.3 + 0.6 * noise3(x, y, z, 71, 3.0))
    if abs((x % 5.0) - 2.5) < 0.5:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 73, 1.0))


def hazard(p):
    x, y, z = p.p
    c = HAZ if math.sin(x * 0.6 + z * 1.5) > 0 else "#16181c"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def badge(p):
    x, y, z = p.p
    c = mix("#4f5a3c", "#2c3324", 0.3 + 0.5 * noise3(x, y, z, 81, 2.0))
    if abs(z + 4.0) < 1.6 and 25.5 <= y <= 29.5:
        c = "#e6e2d4"
    elif abs(z + 1.0) < 0.9 and 25.5 <= y <= 29.5:
        c = "#c03028"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 83, 1.0))


def light(p): return glow(LIGHT)


def optic(p):
    x, y, z = p.p
    return glow(mix("#1f6f9c", OPTIC, 0.4 + 0.6 * noise3(x, y, z, 87, 2.0)))


def vent(p):
    x, y, z = p.p
    return glow(mix(VENT, HOT, 0.3 + 0.7 * noise3(x, y, z, 89, 1.4)))


def exhaust(p):
    x, y, z = p.p
    c = mix(VENT, HOT, 0.25 + 0.7 * noise3(x, y, z, 93, 1.6))
    return glow(shade(c, 0.85 + 0.3 * noise3(x, y, z, 95, 1.0)))


def mc(c):
    """Mirror one cube across x=0 (kept as an explicit, independent cube)."""
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c["skin"]}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def sym(cubes, c):
    cubes.append(c)
    cubes.append(mc(c))


# ----------------------------------------------------------------- hull
body_cubes = [
    {"o": [-9, 10, -20], "s": [18, 12, 40], "skin": "steel"},
    {"o": [-8, 8, -18], "s": [16, 4, 36], "skin": "struct"},
    {"o": [-9, 22, -18], "s": [18, 2, 14], "skin": "plate"},
    {"o": [-9, 22, 6], "s": [18, 2, 14], "skin": "plate"},
    {"o": [-7, 24, 8], "s": [14, 1, 9], "skin": "vent"},
    {"o": [-9, 10, 20], "s": [18, 13, 3], "skin": "struct"},
    {"o": [-9, 10, -22], "s": [18, 13, 2], "skin": "struct"},
    {"o": [-8, 20, -19], "s": [16, 2, 38], "skin": "steel"},
    {"o": [-5, 22, 2], "s": [6, 3, 7], "skin": "stowage"},
    {"o": [0, 22, 11], "s": [8, 3, 6], "skin": "stowage"},
    {"o": [-3, 23, -3], "s": [6, 1, 8], "skin": "struct"},
    {"o": [-9, 8, -24], "s": [18, 4, 3], "skin": "struct"},
]
sym(body_cubes, {"o": [9, 12, -19], "s": [1, 10, 38], "skin": "plate"})
sym(body_cubes, {"o": [-8, 22, -18], "s": [3, 1, 6], "skin": "vent"})
sym(body_cubes, {"o": [-9, 11, -20], "s": [1, 1, 40], "skin": "hazard"})
sym(body_cubes, {"o": [-8, 13, 14], "s": [2, 2, 6], "skin": "hazard"})
sym(body_cubes, {"o": [-8, 20, 0], "s": [1, 2, 6], "skin": "stowage"})

# ----------------------------------------------------------------- sloped glacis
glacis_cubes = [
    {"o": [-9, 8, -27], "s": [18, 15, 3], "skin": "steel", "rot": [-32, 0, 0], "pivot": [0, 15.5, -25.5]},
    {"o": [-8, 9, -26], "s": [16, 13, 2], "skin": "plate", "rot": [-32, 0, 0], "pivot": [0, 15.5, -25.5]},
    {"o": [-9, 20, -25], "s": [18, 3, 6], "skin": "struct", "rot": [-32, 0, 0], "pivot": [0, 15.5, -25.5]},
]

# ----------------------------------------------------------------- side skirts
skirt_l = [
    {"o": [19, 12, -20], "s": [1, 12, 40], "skin": "skirt"},
    {"o": [19, 10, -20], "s": [2, 2, 40], "skin": "hazard"},
    {"o": [19, 22, -20], "s": [1, 2, 40], "skin": "plate"},
]
skirt_r = [mc(c) for c in skirt_l]

# ----------------------------------------------------------------- tracks
track_l = [
    {"o": [9, 10, -22], "s": [11, 2, 44], "skin": "track"},
    {"o": [9, 0, -22], "s": [11, 2, 44], "skin": "track"},
    {"o": [9, 2, -24], "s": [11, 10, 3], "skin": "track"},
    {"o": [9, 2, 21], "s": [11, 10, 3], "skin": "track"},
    {"o": [10, 3, -23], "s": [9, 6, 3], "skin": "struct"},
    {"o": [9, 2, -22], "s": [2, 10, 44], "skin": "struct"},
]
track_r = [mc(c) for c in track_l]

# ----------------------------------------------------------------- exhaust + antenna + lights + tow
exhaust_cubes = [
    {"o": [5, 24, 16], "s": [3, 12, 3], "skin": "struct"},
    {"o": [4.5, 36, 15.5], "s": [4, 1, 4], "skin": "exhaust"},
    {"o": [4, 26, 15], "s": [5, 7, 5], "skin": "steel"},
]
antenna_cubes = [
    {"o": [6.5, 24, 15.5], "s": [2, 3, 2], "skin": "struct"},
    {"o": [7, 27, 16], "s": [1, 9, 1], "skin": "struct"},
    {"o": [7, 36, 16], "s": [1, 1, 1], "skin": "optic"},
]
light_l = [
    {"o": [5, 17, -21], "s": [4, 4, 2], "skin": "struct"},
    {"o": [5.5, 17.5, -22], "s": [3, 3, 1], "skin": "light"},
]
light_r = [mc(c) for c in light_l]
tow_cubes = []
sym(tow_cubes, {"o": [-7, 11, -23], "s": [3, 3, 3], "skin": "struct"})
sym(tow_cubes, {"o": [-8, 12, -24], "s": [2, 2, 1], "skin": "struct"})

# ----------------------------------------------------------------- turret
turret_cubes = [
    {"o": [-7, 24, -9], "s": [14, 6, 18], "skin": "steel"},
    {"o": [-6, 30, -8], "s": [12, 2, 16], "skin": "plate"},
    {"o": [-6, 24, 9], "s": [12, 5, 9], "skin": "struct"},
    {"o": [-6, 29, 10], "s": [12, 1, 7], "skin": "struct"},
    {"o": [-4, 25, -11], "s": [8, 5, 3], "skin": "struct"},
    {"o": [-4, 25, -12], "s": [8, 5, 1], "skin": "struct"},
    {"o": [-5, 30, 12], "s": [4, 2, 4], "skin": "stowage"},
    {"o": [-3, 31, 4], "s": [3, 2, 4], "skin": "struct"},
    {"o": [3, 31, -6], "s": [3, 2, 3], "skin": "struct"},
    {"o": [3.5, 32, -6.5], "s": [2, 1, 2], "skin": "optic"},
]
sym(turret_cubes, {"o": [7, 25, -6], "s": [1, 5, 12], "skin": "plate"})
sym(turret_cubes, {"o": [7, 26, -2], "s": [1, 3, 8], "skin": "badge"})
sym(turret_cubes, {"o": [6, 27, -9], "s": [2, 2, 4], "skin": "struct"})
sym(turret_cubes, {"o": [6.5, 28, -8], "s": [1, 1, 1], "skin": "hazard"})

cupola_cubes = [
    {"o": [0, 32, -2], "s": [7, 4, 8], "skin": "steel"},
    {"o": [-0.5, 36, -2.5], "s": [8, 1, 9], "skin": "plate"},
    {"o": [0, 34, -3], "s": [7, 1, 1], "skin": "optic"},
    {"o": [1, 34, -6], "s": [2, 3, 5], "skin": "struct"},
    {"o": [1.5, 35, -11], "s": [1, 1, 5], "skin": "gun"},
]
hatch_cubes = [
    {"o": [0.5, 36, -2], "s": [6, 2, 8], "skin": "plate"},
    {"o": [0, 37, -3], "s": [1, 1, 2], "skin": "struct"},
]
barrel_cubes = [
    {"o": [-2, 26, -46], "s": [4, 4, 36], "skin": "gun"},
    {"o": [-3, 25, -36], "s": [6, 6, 14], "skin": "plate"},
    {"o": [-2.5, 25.5, -12], "s": [5, 5, 4], "skin": "struct"},
]
muzzle_cubes = [
    {"o": [-3, 25, -54], "s": [6, 6, 8], "skin": "gun"},
    {"o": [-1, 27, -55], "s": [2, 2, 1], "skin": "struct"},
]
sym(muzzle_cubes, {"o": [3, 26, -52], "s": [1, 4, 1], "skin": "struct"})

WHEEL_Z = [-18, -9, 0, 9, 18]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 16, 0], "cubes": body_cubes},
    {"name": "glacis", "parent": "body", "pivot": [0, 12, -24], "cubes": glacis_cubes},
    {"name": "skirt_l", "parent": "body", "pivot": [19, 17, 0], "cubes": skirt_l},
    {"name": "skirt_r", "parent": "body", "pivot": [-19, 17, 0], "cubes": skirt_r},
    {"name": "track_l", "parent": "body", "pivot": [14.5, 6, 0], "cubes": track_l},
    {"name": "track_r", "parent": "body", "pivot": [-14.5, 6, 0], "cubes": track_r},
    {"name": "exhaust", "parent": "body", "pivot": [6.5, 24, 17.5], "cubes": exhaust_cubes},
    {"name": "antenna", "parent": "body", "pivot": [7, 24, 16], "cubes": antenna_cubes},
    {"name": "light_l", "parent": "body", "pivot": [7, 19, -21], "cubes": light_l},
    {"name": "light_r", "parent": "body", "pivot": [-7, 19, -21], "cubes": light_r},
    {"name": "tow", "parent": "body", "pivot": [0, 12, -23], "cubes": tow_cubes},
    {"name": "turret", "parent": "body", "pivot": [0, 26, -2], "cubes": turret_cubes},
    {"name": "cupola", "parent": "turret", "pivot": [3.5, 32, 2], "cubes": cupola_cubes},
    {"name": "hatch", "parent": "turret", "pivot": [3.5, 37, 2], "cubes": hatch_cubes},
    {"name": "barrel", "parent": "turret", "pivot": [0, 28, -10], "cubes": barrel_cubes},
    {"name": "muzzle", "parent": "barrel", "pivot": [0, 28, -46], "cubes": muzzle_cubes},
]
for side, x in (("l", 14.5), ("r", -14.5)):
    for i, z in enumerate(WHEEL_Z):
        bones.append({"name": f"wheel_{side}{i}", "parent": "body", "pivot": [x, 6, z], "cubes": [
            {"o": [x - 3, 2, z - 4], "s": [6, 8, 8], "skin": "wheel"},
            {"o": [x - 4, 4, z - 2], "s": [8, 4, 4], "skin": "struct"},
        ]})

WHEELS = [b["name"] for b in bones if b["name"].startswith("wheel_")]


def spin(names, rate=230):
    return {n: {"rotation": [f"query.modified_distance_moved * {rate}", "0", "0"]} for n in names}


anims = {
    "move": anim(merge(
        spin(WHEELS),
        {"body": {"position": ["0", "math.sin(query.life_time * 190) * 0.22", "0"]}},
        {"body": {"rotation": ["math.cos(query.modified_distance_moved * 26) * 1.5 * query.modified_move_speed",
                               "0", "math.sin(query.modified_distance_moved * 26) * 2.5 * query.modified_move_speed"]}},
        {"turret": {"rotation": ["math.cos(query.modified_distance_moved * 26) * 1.2 * query.modified_move_speed",
                                 "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 150) * 9"]}},
        {"exhaust": {"position": ["0", "math.sin(query.life_time * 240) * 0.15", "0"]}},
        {"skirt_l": {"rotation": ["math.sin(query.life_time * 190) * 1.5", "0", "0"]}},
        {"skirt_r": {"rotation": ["math.sin(query.life_time * 190 + 0.6) * 1.5", "0", "0"]}},
    )),
    "idle": anim(merge(
        {"turret": {"rotation": ["0", "math.sin(query.life_time * 30) * 22", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 70) * 6"]}},
        {"exhaust": {"position": ["0", "math.sin(query.life_time * 90) * 0.1", "0"]}},
        {"body": {"position": ["0", "math.sin(query.life_time * 120) * 0.07", "0"]}},
        {"cupola": {"rotation": ["math.sin(query.life_time * 45) * 3", "0", "0"]}},
        {"hatch": {"rotation": ["math.sin(query.life_time * 40 + 1.0) * 4", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"barrel": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2.5"]}},
        {"muzzle": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 1.2"]}},
        {"turret": {"rotation": ["math.sin(variable.attack_time * 180) * -3", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -2", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 14"]}},
    ), loop=False),
}

SPEC = {
    "id": "military_battle_tank",
    "name": "Ironclad Battle Tank",
    "egg": ("#4a5058", "#d8b24a"),
    "glow": True,
    "scale": 1.0,
    "visible": [5.4, 3.2, 1.2],
    "bones": bones,
    "skins": {"default": steel, "steel": steel, "plate": plate, "struct": struct, "gun": gun,
              "track": track, "wheel": wheel, "skirt": skirt, "stowage": stowage, "hazard": hazard,
              "badge": badge, "light": light, "optic": optic, "vent": vent, "exhaust": exhaust},
    "anims": anims,
    "play": [{"move": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 150, "speed": 0.22, "damage": 8, "box": [2.6, 2.2],
        "knockback_resist": 0.8, "fire_immune": True, "family": ["mech", "vehicle"],
        "ride": {"seats": [[-0.4, 1.45, -0.85], [0.35, 2.1, 0.15]], "jump": 0.3},
        "loot": [("minecraft:iron_ingot", 3, 6), ("minecraft:copper_ingot", 2, 5)],
        "sound": ("golem", [0.5, 0.7]),
        "xp": 20,
    },
}
