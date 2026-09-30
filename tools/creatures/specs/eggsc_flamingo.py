"""Lagoon Flamingo - tall pink wader with an S-curved neck."""
from eggsc_kit import *

PINK = "#f07a9a"
PINK_D = "#d4547a"
PINK_L = "#fbb0c4"


def plume(p):
    x, y, z = p.p
    c = mix(PINK_D, PINK_L, noise3(x * 1.4, y * 1.4, z * 1.4, 5, 2.5))
    return shade(c, 0.9 + 0.2 * noise3(x * 3, y * 3, z * 3, 8, 1.0))


def wing(p):
    x, y, z = p.p
    if y < 16.2:
        return shade("#26202a", 0.9 + 0.3 * noise3(x * 3, y * 3, z * 3, 2, 1.0))
    c = plume(p)
    if y < 17.3:
        c = mix(c, "#26202a", 0.5)
    return c


def bill(p):
    z = p.p[2]
    if z < -15.0:
        return "#1e1a1e"
    if z < -13.2:
        return mix("#e8b0a8", "#1e1a1e", 0.55)
    return "#f2d0c6"


def leg(p):
    return shade("#e2688a", 0.9 + 0.25 * noise3(p.p[0] * 4, p.p[1] * 2, p.p[2] * 4, 3, 1.0))


def eye(p):
    return "#141010" if not (p.x == 0 and p.y == 0) else "#ffe680"


L = 14
body = [cube([-3, L, -5], [6, 6, 11], "plume"), cube([-2.5, L + 1, -7], [5, 5, 3], "plume"), cube([-2, L + 2, 5], [4, 3, 4], "wing")]
bones = [
    {"name": "body", "parent": None, "pivot": [0, L + 3, 0], "cubes": body},
    {"name": "neck0", "parent": "body", "pivot": [0, L + 5, -5], "cubes": [cube([-1, L + 5, -6.5], [2, 6, 2], "plume")]},
    {"name": "neck1", "parent": "neck0", "pivot": [0, L + 11, -6], "cubes": [cube([-1, L + 10, -7.5], [2, 6, 2], "plume")]},
    {"name": "neck2", "parent": "neck1", "pivot": [0, L + 16, -6.5], "cubes": [cube([-1, L + 15, -6.5], [2, 5, 2], "plume")]},
    {"name": "head", "parent": "neck2", "pivot": [0, L + 19, -6], "cubes": [
        cube([-1.5, L + 18, -10], [3, 3, 4], "plume"),
        cube([-1, L + 18, -13.5], [2, 2, 4], "bill"), cube([-1, L + 16.2, -14.5], [2, 2, 3], "bill"),
        cube([1.4, L + 19.2, -8.5], [1, 1, 1], "eye"), cube([-2.4, L + 19.2, -8.5], [1, 1, 1], "eye")]},
    {"name": "wing_l", "parent": "body", "pivot": [3, L + 5, -3], "cubes": [cube([3, L + 0.5, -3.5], [1, 6, 9], "wing")]},
    {"name": "wing_r", "parent": "body", "pivot": [-3, L + 5, -3], "cubes": [cube([-4, L + 0.5, -3.5], [1, 6, 9], "wing")]},
]
for nm, sx in (("leg_l", 1), ("leg_r", -1)):
    x0 = 1.5 * sx - 0.5
    bones.append({"name": nm, "parent": None, "pivot": [x0 + 0.5, L + 1, 0],
                  "cubes": [cube([x0, 1, -0.5], [1, L, 1], "leg"), cube([x0 - 1, 0, -3], [3, 1, 4], "leg"), cube([x0 - 0.5, 0, -4], [2, 1, 1], "leg")]})

anims = {
    "walk": anim(merge(biped_walk("leg_l", "leg_r", amp=38, freq=44),
                       swing({"neck0": 0, "neck1": 180, "neck2": 0}, amp=6, axis=0, freq=44), bob("body", 0.4, 120))),
    "idle": anim(merge(bob("body", 0.2, 70),
                       sway("neck0", 4, 40, 0), sway("neck1", 6, 33, 0, 1.0), sway("neck2", 8, 29, 0, 2.0),
                       {"head": {"rotation": ["math.sin(query.life_time * 45) * 4", "math.sin(query.life_time * 24) * 18", "0"]}},
                       sway("wing_l", 4, 90, 2), sway("wing_r", 4, 90, 2, 3.1))),
}
SPEC = {"id": "flamingo", "name": "Lagoon Flamingo", "egg": ("#f07a9a", "#26202a"), "glow": False, "scale": 0.75,
        "visible": auto_visible(bones), "bones": bones,
        "skins": {"default": plume, "plume": plume, "wing": wing, "bill": bill, "leg": leg, "eye": eye},
        "anims": anims, "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle"],
        "behavior": beh("passive", 8, 0.22, [0.6, 2.7], ["flamingo"],
                        spawn={"biomes": ["swamp", "mangrove_swamp", "beach"], "weight": 5, "herd": [3, 6]},
                        loot=[("minecraft:feather", 1, 2)], sound=("parrot", [0.65, 0.8]))}
