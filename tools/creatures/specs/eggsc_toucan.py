"""Rainforest Toucan - all beak, all attitude."""
from eggsc_kit import *

BLACK = "#1c1a22"


def plume(p):
    x, y, z = p.p
    return shade(BLACK, 0.85 + 0.5 * noise3(x * 2, y * 2, z * 2, 3, 1.4))


def bib(p):
    x, y, z = p.p
    return shade("#f6f0da", 0.92 + 0.14 * noise3(x * 3, y * 3, z * 3, 5, 1.0))


def bill(p):
    x, y, z = p.p
    if z < -17.4:
        c = "#1c1a22"
    elif z < -14.5:
        c = mix("#f28a1c", "#e05a12", (-14.5 - z) / 3.0)
    else:
        c = mix("#f6d020", "#f2a018", (z + 14.5) / -3.0 if z < -12 else 0.0)
    if y > 9.3:
        c = mix(c, "#fff0a0", 0.35)
    return shade(c, 0.94 + 0.12 * noise3(x * 3, y * 3, z * 3, 8, 1.0))


def ring_eye(p):
    if p.fw > 1 and (p.face == "front") and 0 < p.x < p.fw - 1 and 0 < p.y < p.fh - 1:
        return "#101010"
    return "#3aa8e0"


def leg(p):
    return shade("#e8901c", 0.9 + 0.2 * noise3(p.p[0] * 3, p.p[1] * 3, p.p[2] * 3, 3, 1.0))


def tailunder(p):
    return "#d8281c"


L = 4
bones = [
    {"name": "body", "parent": None, "pivot": [0, L + 3, 0],
     "cubes": [cube([-2.5, L, -3], [5, 6, 8], "plume"), cube([-2, L + 0.5, -4.3], [4, 5, 2], "bib"),
               cube([-1.5, L + 3, 5], [3, 2, 6], "plume"), cube([-1.5, L + 2, 8], [3, 1, 3], "tailunder")]},
    {"name": "head", "parent": "body", "pivot": [0, L + 8, -3],
     "cubes": [cube([-2.5, L + 5, -8], [5, 5, 5], "plume"), cube([-2, L + 5, -8.6], [4, 2, 1], "bib"),
               cube([1.2, L + 7, -8.4], [2, 2, 1], "ring_eye"), cube([-3.2, L + 7, -8.4], [2, 2, 1], "ring_eye")]},
    {"name": "bill", "parent": "head", "pivot": [0, L + 8, -8],
     "cubes": [cube([-1.5, L + 6, -13], [3, 3, 5], "bill"), cube([-1.5, L + 5.6, -16], [3, 3, 3], "bill"), cube([-1, L + 5.2, -18.5], [2, 2, 3], "bill")]},
    {"name": "wing_l", "parent": "body", "pivot": [2.5, L + 5, -2], "cubes": [cube([2.5, L + 0.5, -2.5], [1, 5, 7], "plume")]},
    {"name": "wing_r", "parent": "body", "pivot": [-2.5, L + 5, -2], "cubes": [cube([-3.5, L + 0.5, -2.5], [1, 5, 7], "plume")]},
]
for nm, sx in (("leg_l", 1), ("leg_r", -1)):
    x0 = 1.2 * sx - 0.5
    bones.append({"name": nm, "parent": None, "pivot": [x0 + 0.5, L + 1, 0],
                  "cubes": [cube([x0, 1, -0.5], [1, L, 1], "leg"), cube([x0 - 1, 0, -2.5], [3, 1, 3], "leg")]})
anims = {
    "walk": anim(merge(biped_walk("leg_l", "leg_r", amp=45, freq=70),
                       {"body": {"position": ["0", "math.abs(math.sin(query.modified_distance_moved * 70)) * 1.5 * query.modified_move_speed * 3", "0"]}},
                       swing({"head": 0}, amp=5, axis=0, freq=70))),
    "idle": anim(merge(bob("body", 0.15, 80),
                       {"head": {"rotation": ["math.sin(query.life_time * 50) * 5", "math.sin(query.life_time * 26) * 22", "math.sin(query.life_time * 19) * 6"]}},
                       sway("wing_l", 3, 100, 2), sway("wing_r", 3, 100, 2, 3.1))),
}
SPEC = {"id": "toucan", "name": "Rainforest Toucan", "egg": ("#1c1a22", "#f28a1c"), "glow": False, "scale": 1.0,
        "visible": auto_visible(bones), "bones": bones,
        "skins": {"default": plume, "plume": plume, "bib": bib, "bill": bill, "leg": leg, "ring_eye": ring_eye, "tailunder": tailunder},
        "anims": anims, "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle"],
        "behavior": beh("passive", 6, 0.25, [0.4, 0.7], ["toucan"],
                        spawn={"biomes": ["jungle"], "weight": 8, "herd": [2, 4]},
                        loot=[("minecraft:feather", 0, 2)], sound=("parrot", [0.85, 1.0]))}
