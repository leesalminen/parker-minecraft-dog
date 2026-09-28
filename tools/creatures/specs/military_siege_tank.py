"""Siege Breaker - heavy assault tank: dual barrels, missile pod, dozer blade, extra plating.
Model faces -Z, y up, ground y=0."""
import math
from lib import *

STEEL  = "#6f767e"
DARK   = "#33383e"
PLATE  = "#848c93"
STRUCT = "#42484f"
TRACK  = "#1f2226"
HAZ    = "#d8b24a"
OLIVE  = "#55603e"
ERA    = "#3c4249"
LIGHT  = "#fff0c4"
OPTIC  = "#8fd8ff"
VENT   = "#ff8a2a"
HOT    = "#ffe0a0"
WAR    = "#ff3b1e"


def armor(p, base=STEEL, dark=DARK, seed=11, period=18.0, edge=1.2):
    x, y, z = p.p
    c = mix(base, dark, 0.18 + 0.55 * noise3(x, y, z, seed, 3.2))
    if (x % period) < edge or (y % period) < edge or (z % period) < edge:
        c = shade(c, 0.62)
    dx = min(x % period, period - x % period)
    dz = min(z % period, period - z % period)
    if dx < 1.0 and dz < 1.0:
        c = shade(c, 0.78)
    h = hash01(x, y, z, seed)
    if h > 0.93:
        c = shade(c, 0.72)
    elif h < 0.05:
        c = mix(c, "#6f5c44", 0.5)
    return shade(c, 0.92 + 0.18 * noise3(x, y, z, seed + 3, 1.0))


def steel(p):  return armor(p, STEEL, DARK, 11)
def plate(p):  return armor(p, PLATE, "#1c2127", 21, 14.0)
def struct(p): return armor(p, STRUCT, "#171b20", 31, 10.0)


def era(p):
    x, y, z = p.p
    c = mix(ERA, "#2a2f35", 0.25 + 0.6 * noise3(x, y, z, 33, 2.4))
    if abs((x % 4.0) - 2.0) < 0.8 or abs((y % 4.0) - 2.0) < 0.8:
        c = shade(c, 0.65)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 35, 1.0))


def gun(p):
    x, y, z = p.p
    c = mix("#4e545b", "#1d2126", 0.25 + 0.6 * noise3(x, y, z, 41, 2.5))
    if abs((z % 8.0) - 4.0) < 0.7:
        c = shade(c, 0.66)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 43, 1.0))


def track(p):
    x, y, z = p.p
    c = mix(TRACK, "#353b42", 0.3 + 0.6 * noise3(x, y, z, 51, 2.2))
    if math.sin(z * 1.15) > 0.2:
        c = shade(c, 0.7)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 53, 1.0))


def wheel(p):
    x, y, z = p.p
    if p.face in ("east", "west"):
        dx, dy = p.x - p.fw / 2.0, p.y - p.fh / 2.0
        r = math.hypot(dx, dy)
        a = math.atan2(dy, dx)
        if r > 5.6:
            c = mix("#171a1e", "#2f343a", 0.3 + 0.5 * noise3(x, y, z, 7, 2.0))
            if (r * 2.4) % 2.0 < 0.6:
                c = shade(c, 0.66)
        else:
            c = mix("#646a72", "#282c31", 0.3 + 0.4 * noise3(x, y, z, 9, 2.0))
            k = ((a + math.pi) / (math.pi / 2.0)) % 1.0
            if k < 0.2 or k > 0.8:
                c = shade(c, 0.55)
            if r < 1.6:
                c = shade(c, 0.45)
    else:
        c = mix("#15181c", "#262a30", 0.3 + 0.6 * noise3(x, y, z, 11, 2.0))
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 13, 1.0))


def skirt(p):
    x, y, z = p.p
    if 11.0 <= y <= 14.5:
        c = HAZ if math.sin(z * 1.2) > 0 else "#141619"
    else:
        c = armor(p, PLATE, "#20252b", 61, 16.0)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 63, 1.0))


def stowage(p):
    x, y, z = p.p
    c = mix(OLIVE, "#333b26", 0.3 + 0.6 * noise3(x, y, z, 71, 3.0))
    if abs((x % 6.0) - 3.0) < 0.6:
        c = shade(c, 0.6)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 73, 1.0))


def hazard(p):
    x, y, z = p.p
    c = HAZ if math.sin(x * 0.5 + z * 1.2) > 0 else "#141619"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 91, 1.0))


def badge(p):
    x, y, z = p.p
    c = mix("#46503a", "#252c1e", 0.3 + 0.5 * noise3(x, y, z, 81, 2.0))
    if abs(z + 4.0) < 1.8 and 38.5 <= y <= 43.5:
        c = "#e6e2d4"
    elif abs(z + 1.2) < 1.0 and 38.5 <= y <= 43.5:
        c = "#c03028"
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 83, 1.0))


def missile(p):
    x, y, z = p.p
    c = mix("#3d4636", "#20261c", 0.3 + 0.6 * noise3(x, y, z, 97, 3.0))
    if abs((y % 5.0) - 2.5) < 0.6:
        c = shade(c, 0.7)
    return shade(c, 0.9 + 0.2 * noise3(x, y, z, 99, 1.0))


def warhead(p):
    x, y, z = p.p
    return glow(mix(WAR, HOT, 0.2 + 0.7 * noise3(x, y, z, 101, 1.6)))


def light(p): return glow(LIGHT)


def optic(p):
    x, y, z = p.p
    return glow(mix("#1f6f9c", OPTIC, 0.4 + 0.6 * noise3(x, y, z, 87, 2.0)))


def vent(p):
    x, y, z = p.p
    return glow(mix(VENT, HOT, 0.3 + 0.7 * noise3(x, y, z, 89, 1.4)))


def exhaust(p):
    x, y, z = p.p
    return glow(shade(mix(VENT, HOT, 0.25 + 0.7 * noise3(x, y, z, 93, 1.6)),
                      0.85 + 0.3 * noise3(x, y, z, 95, 1.0)))


def mc(c):
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
    {"o": [-12, 14, -34], "s": [24, 20, 66], "skin": "steel"},
    {"o": [-11, 11, -30], "s": [22, 6, 60], "skin": "struct"},
    {"o": [-12, 34, -30], "s": [24, 4, 20], "skin": "plate"},
    {"o": [-12, 34, 12], "s": [24, 4, 20], "skin": "plate"},
    {"o": [-9, 38, 14], "s": [18, 1, 14], "skin": "vent"},
    {"o": [-12, 14, 32], "s": [24, 20, 3], "skin": "struct"},
    {"o": [-12, 14, -36], "s": [24, 20, 2], "skin": "struct"},
    {"o": [-11, 30, -32], "s": [22, 2, 62], "skin": "steel"},
    {"o": [-5, 38, -4], "s": [10, 1, 12], "skin": "struct"},
    {"o": [-7, 38, 6], "s": [7, 4, 9], "skin": "stowage"},
    {"o": [1, 38, 18], "s": [9, 4, 8], "skin": "stowage"},
]
sym(body_cubes, {"o": [12, 18, -26], "s": [2, 16, 52], "skin": "plate"})
sym(body_cubes, {"o": [-12, 15, -34], "s": [1, 1, 66], "skin": "hazard"})
sym(body_cubes, {"o": [12, 20, -18], "s": [2, 4, 5], "skin": "era"})
sym(body_cubes, {"o": [12, 25, -8], "s": [2, 4, 5], "skin": "era"})
sym(body_cubes, {"o": [-12, 36, -26], "s": [3, 1, 8], "skin": "vent"})
sym(body_cubes, {"o": [-11, 30, -6], "s": [1, 3, 8], "skin": "stowage"})

# ----------------------------------------------------------------- sloped glacis
glacis_cubes = [
    {"o": [-12, 12, -42], "s": [24, 20, 4], "skin": "steel", "rot": [-34, 0, 0], "pivot": [0, 22, -40]},
    {"o": [-11, 13, -41], "s": [22, 18, 3], "skin": "plate", "rot": [-34, 0, 0], "pivot": [0, 22, -40]},
    {"o": [-12, 30, -38], "s": [24, 4, 8], "skin": "struct", "rot": [-34, 0, 0], "pivot": [0, 22, -40]},
]
for i in range(3):
    sym(glacis_cubes, {"o": [2 + i * 4, 20, -43], "s": [3, 4, 3], "skin": "era",
                       "rot": [-34, 0, 0], "pivot": [0, 22, -40]})

# ----------------------------------------------------------------- dozer blade
dozer_cubes = [
    {"o": [-16, 2, -52], "s": [32, 22, 3], "skin": "plate", "rot": [-28, 0, 0], "pivot": [0, 13, -50.5]},
    {"o": [-16, 20, -50], "s": [32, 4, 8], "skin": "steel", "rot": [-28, 0, 0], "pivot": [0, 13, -50.5]},
    {"o": [-9, 14, -44], "s": [4, 4, 14], "skin": "struct"},
    {"o": [-12, 16, -46], "s": [2, 3, 10], "skin": "struct"},
]
sym(dozer_cubes, {"o": [6, 14, -44], "s": [4, 4, 14], "skin": "struct"})
sym(dozer_cubes, {"o": [-14, 2, -56], "s": [2, 4, 3], "skin": "era"})
sym(dozer_cubes, {"o": [-8, 2, -57], "s": [2, 4, 3], "skin": "era"})

# ----------------------------------------------------------------- skirts
skirt_l = [
    {"o": [27, 14, -30], "s": [2, 20, 60], "skin": "skirt"},
    {"o": [27, 11, -30], "s": [2, 3, 60], "skin": "hazard"},
    {"o": [27, 34, -30], "s": [2, 2, 60], "skin": "plate"},
]
skirt_r = [mc(c) for c in skirt_l]

# ----------------------------------------------------------------- tracks
track_l = [
    {"o": [12, 14, -34], "s": [15, 3, 66], "skin": "track"},
    {"o": [12, 0, -34], "s": [15, 3, 66], "skin": "track"},
    {"o": [12, 3, -36], "s": [15, 14, 4], "skin": "track"},
    {"o": [12, 3, 30], "s": [15, 14, 4], "skin": "track"},
    {"o": [13, 4, -35], "s": [13, 8, 4], "skin": "struct"},
    {"o": [12, 3, -34], "s": [2, 14, 66], "skin": "struct"},
]
track_r = [mc(c) for c in track_l]

# ----------------------------------------------------------------- exhausts + antenna + lights
exhaust_l = [
    {"o": [8, 38, 26], "s": [4, 10, 4], "skin": "struct"},
    {"o": [7.5, 48, 25.5], "s": [5, 2, 5], "skin": "exhaust"},
    {"o": [7, 40, 25], "s": [6, 8, 6], "skin": "steel"},
]
exhaust_r = [mc(c) for c in exhaust_l]
antenna_cubes = [
    {"o": [10, 38, 29], "s": [2, 3, 2], "skin": "struct"},
    {"o": [10.5, 41, 29.5], "s": [1, 9, 1], "skin": "struct"},
    {"o": [10.5, 50, 29.5], "s": [1, 1, 1], "skin": "optic"},
]
light_l = [
    {"o": [8, 24, -35], "s": [5, 5, 2], "skin": "struct"},
    {"o": [8.5, 24.5, -36], "s": [4, 4, 1], "skin": "light"},
]
light_r = [mc(c) for c in light_l]

# ----------------------------------------------------------------- turret
turret_cubes = [
    {"o": [-10, 34, -14], "s": [20, 10, 26], "skin": "steel"},
    {"o": [-9, 44, -12], "s": [18, 3, 22], "skin": "plate"},
    {"o": [-9, 34, 12], "s": [18, 9, 12], "skin": "struct"},
    {"o": [-9, 43, 13], "s": [18, 1, 10], "skin": "struct"},
    {"o": [-6, 35, -17], "s": [12, 9, 4], "skin": "struct"},
    {"o": [-6, 35, -18], "s": [12, 9, 1], "skin": "struct"},
    {"o": [-4, 34, -5], "s": [8, 1, 10], "skin": "struct"},
    {"o": [-4, 45, -8], "s": [3, 3, 3], "skin": "struct"},
    {"o": [-3.5, 46, -8.5], "s": [2, 1, 2], "skin": "optic"},
    {"o": [-7, 44, 18], "s": [5, 3, 4], "skin": "stowage"},
]
sym(turret_cubes, {"o": [10, 36, -10], "s": [2, 8, 20], "skin": "plate"})
sym(turret_cubes, {"o": [10, 38, -4], "s": [2, 5, 10], "skin": "badge"})
sym(turret_cubes, {"o": [8, 36, -15], "s": [3, 3, 3], "skin": "era"})
sym(turret_cubes, {"o": [8, 39, -15], "s": [3, 3, 3], "skin": "era"})
sym(turret_cubes, {"o": [9, 40, -13], "s": [2, 2, 5], "skin": "struct"})
sym(turret_cubes, {"o": [9.5, 41, -12], "s": [1, 1, 1], "skin": "hazard"})

# ----------------------------------------------------------------- missile pod
missile_cubes = [
    {"o": [-6, 40, 10], "s": [12, 8, 14], "skin": "struct"},
    {"o": [-5, 47, 11], "s": [10, 2, 12], "skin": "plate"},
    {"o": [-6, 40, 8], "s": [12, 8, 2], "skin": "steel", "rot": [-20, 0, 0], "pivot": [0, 44, 9]},
]
for i in range(3):
    for j in range(2):
        tx = -4.5 + i * 3.4
        tz = 13.0 + j * 5.5
        missile_cubes.append({"o": [tx, 45, tz], "s": [2, 3, 4], "skin": "missile"})
        missile_cubes.append({"o": [tx, 47.5, tz], "s": [2, 1, 4], "skin": "warhead"})

cupola_cubes = [
    {"o": [1, 47, -2], "s": [8, 3, 9], "skin": "steel"},
    {"o": [0.5, 50, -2.5], "s": [9, 1, 10], "skin": "plate"},
    {"o": [1, 49, -3], "s": [8, 1, 1], "skin": "optic"},
    {"o": [2, 48, -7], "s": [2, 2, 5], "skin": "struct"},
    {"o": [2.5, 49, -12], "s": [1, 1, 5], "skin": "gun"},
]
hatch_cubes = [
    {"o": [1.5, 50, -2], "s": [7, 1, 9], "skin": "plate"},
    {"o": [1, 50, -3], "s": [1, 1, 2], "skin": "struct"},
]
barrel_l_cubes = [
    {"o": [-5.5, 38, -52], "s": [3, 4, 36], "skin": "gun"},
    {"o": [-6, 37.5, -44], "s": [4, 5, 12], "skin": "plate"},
    {"o": [-6, 37, -58], "s": [5, 6, 8], "skin": "gun"},
    {"o": [-4.5, 39, -57], "s": [1, 2, 1], "skin": "struct"},
]
barrel_r_cubes = [mc(c) for c in barrel_l_cubes]

WHEEL_Z = [-28, -17, -6, 5, 16, 27]

bones = [
    {"name": "body", "parent": None, "pivot": [0, 24, 0], "cubes": body_cubes},
    {"name": "glacis", "parent": "body", "pivot": [0, 20, -38], "cubes": glacis_cubes},
    {"name": "dozer", "parent": "body", "pivot": [0, 16, -40], "cubes": dozer_cubes},
    {"name": "skirt_l", "parent": "body", "pivot": [27, 24, 0], "cubes": skirt_l},
    {"name": "skirt_r", "parent": "body", "pivot": [-27, 24, 0], "cubes": skirt_r},
    {"name": "track_l", "parent": "body", "pivot": [19.5, 8, 0], "cubes": track_l},
    {"name": "track_r", "parent": "body", "pivot": [-19.5, 8, 0], "cubes": track_r},
    {"name": "exhaust_l", "parent": "body", "pivot": [10, 38, 27.5], "cubes": exhaust_l},
    {"name": "exhaust_r", "parent": "body", "pivot": [-10, 38, 27.5], "cubes": exhaust_r},
    {"name": "antenna", "parent": "body", "pivot": [10.5, 38, 29.5], "cubes": antenna_cubes},
    {"name": "light_l", "parent": "body", "pivot": [10, 26, -35], "cubes": light_l},
    {"name": "light_r", "parent": "body", "pivot": [-10, 26, -35], "cubes": light_r},
    {"name": "turret", "parent": "body", "pivot": [0, 40, -4], "cubes": turret_cubes},
    {"name": "missile_pod", "parent": "turret", "pivot": [0, 46, 17], "cubes": missile_cubes},
    {"name": "cupola", "parent": "turret", "pivot": [5, 47, 2], "cubes": cupola_cubes},
    {"name": "hatch", "parent": "turret", "pivot": [5, 50, 2], "cubes": hatch_cubes},
    {"name": "barrel_l", "parent": "turret", "pivot": [-4, 40, -14], "cubes": barrel_l_cubes},
    {"name": "barrel_r", "parent": "turret", "pivot": [4, 40, -14], "cubes": barrel_r_cubes},
]
for side, x in (("l", 19.5), ("r", -19.5)):
    for i, z in enumerate(WHEEL_Z):
        bones.append({"name": f"wheel_{side}{i}", "parent": "body", "pivot": [x, 8, z], "cubes": [
            {"o": [x - 3.5, 1, z - 7], "s": [7, 14, 14], "skin": "wheel"},
            {"o": [x - 5, 4, z - 3], "s": [10, 8, 8], "skin": "struct"},
        ]})

WHEELS = [b["name"] for b in bones if b["name"].startswith("wheel_")]


def spin(names, rate=180):
    return {n: {"rotation": [f"query.modified_distance_moved * {rate}", "0", "0"]} for n in names}


anims = {
    "move": anim(merge(
        spin(WHEELS),
        {"body": {"position": ["0", "math.sin(query.life_time * 150) * 0.24", "0"]}},
        {"body": {"rotation": ["math.cos(query.modified_distance_moved * 20) * 1.4 * query.modified_move_speed",
                               "0", "math.sin(query.modified_distance_moved * 20) * 2.2 * query.modified_move_speed"]}},
        {"turret": {"rotation": ["math.cos(query.modified_distance_moved * 20) * 1.0 * query.modified_move_speed",
                                 "0", "0"]}},
        {"dozer": {"rotation": ["math.sin(query.life_time * 150) * 1.2", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 130) * 10"]}},
        {"exhaust_l": {"position": ["0", "math.sin(query.life_time * 210) * 0.18", "0"]}},
        {"exhaust_r": {"position": ["0", "math.sin(query.life_time * 210 + 0.7) * 0.18", "0"]}},
        {"skirt_l": {"rotation": ["math.sin(query.life_time * 150) * 1.4", "0", "0"]}},
        {"skirt_r": {"rotation": ["math.sin(query.life_time * 150 + 0.6) * 1.4", "0", "0"]}},
    )),
    "idle": anim(merge(
        {"turret": {"rotation": ["0", "math.sin(query.life_time * 24) * 18", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(query.life_time * 60) * 7"]}},
        {"exhaust_l": {"position": ["0", "math.sin(query.life_time * 80) * 0.12", "0"]}},
        {"exhaust_r": {"position": ["0", "math.sin(query.life_time * 80 + 0.9) * 0.12", "0"]}},
        {"body": {"position": ["0", "math.sin(query.life_time * 100) * 0.08", "0"]}},
        {"missile_pod": {"rotation": ["math.sin(query.life_time * 40) * 2", "0", "0"]}},
        {"cupola": {"rotation": ["math.sin(query.life_time * 38) * 3", "0", "0"]}},
        {"hatch": {"rotation": ["math.sin(query.life_time * 34 + 1.0) * 4", "0", "0"]}},
    )),
    "attack": anim(merge(
        {"barrel_l": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 3.0"]}},
        {"barrel_r": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 3.0"]}},
        {"turret": {"rotation": ["math.sin(variable.attack_time * 180) * -4", "0", "0"]}},
        {"body": {"rotation": ["math.sin(variable.attack_time * 180) * -2.5", "0", "0"]}},
        {"missile_pod": {"rotation": ["math.sin(variable.attack_time * 180) * 4", "0", "0"]}},
        {"antenna": {"rotation": ["0", "0", "math.sin(variable.attack_time * 180) * 16"]}},
    ), loop=False),
}

SPEC = {
    "id": "military_siege_tank",
    "name": "Siege Breaker",
    "egg": ("#42484f", "#ff3b1e"),
    "glow": True,
    "scale": 1.0,
    "visible": [6.4, 3.8, 1.6],
    "bones": bones,
    "skins": {"default": steel, "steel": steel, "plate": plate, "struct": struct, "era": era, "gun": gun,
              "track": track, "wheel": wheel, "skirt": skirt, "stowage": stowage, "hazard": hazard,
              "badge": badge, "missile": missile, "warhead": warhead, "light": light, "optic": optic,
              "vent": vent, "exhaust": exhaust},
    "anims": anims,
    "play": [{"move": "query.modified_move_speed > 0.02"}, "idle", "attack"],
    "behavior": {
        "role": "mount",
        "health": 220, "speed": 0.18, "damage": 12, "box": [3.2, 3.2],
        "knockback_resist": 0.9, "fire_immune": True, "family": ["mech", "vehicle"],
        "ride": {"seats": [[-0.5, 2.4, -1.4], [0.35, 3.05, 0.15]], "jump": 0.25},
        "loot": [("minecraft:iron_ingot", 5, 9), ("minecraft:copper_ingot", 3, 7), ("minecraft:gunpowder", 1, 3)],
        "sound": ("golem", [0.4, 0.55]),
        "xp": 30,
    },
}
