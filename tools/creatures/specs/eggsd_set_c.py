"""eggsd set C: firefly, butterfly swarm, scorpion, centipede, jellyfloat."""
from specs.eggsd_kit import *
from specs.eggsd_set_b import insect_legs

WALK = {"walk": "query.modified_move_speed > 0.02"}


# ================================================================== FIREFLY (tiny flyer, glowing)
def firefly():
    dark = chitin("#2b2118", "#4a3826", 3)
    red = flat("#d83a2a")
    bones = [
        B("body", None, [0, 5, 0], [
            C([-1, 4, -1], [2, 2, 3], "dark"), C([-1.5, 6, -2], [3, 1, 3], "red"),
            C([-1.5, 3, 2], [3, 3, 4], "abd"), C([-1, 6, 1], [2, 1, 5], "elytra"),
            C([-1, 4, -3], [2, 2, 2], "dark"), C([-1.5, 4.5, -3.4], [1, 1, 1], "eye"), C([0.5, 4.5, -3.4], [1, 1, 1], "eye"),
            C([-1.5, 1, -1], [1, 2, 1], "dark"), C([0.5, 1, -1], [1, 2, 1], "dark"),
            C([-1.5, 1, 1], [1, 2, 1], "dark"), C([0.5, 1, 1], [1, 2, 1], "dark")]),
        B("wing_l", "body", [1, 6.5, 0], [C([1, 6.5, -1], [5, 1, 4], "wing")]),
        B("wing_r", "body", [-1, 6.5, 0], [C([-6, 6.5, -1], [5, 1, 4], "wing")]),
        B("ant_l", "body", [0.5, 6, -3], [C([0.5, 6, -5], [1, 1, 3], "dark")]),
        B("ant_r", "body", [-0.5, 6, -3], [C([-1.5, 6, -5], [1, 1, 3], "dark")]),
    ]
    def abd(p):
        n = N(p, 4, 1.5)
        return glow(mix("#c8ff3a", "#f4ff9a", 0.3 + 0.6 * n))
    skins = {"default": dark, "dark": dark, "red": red, "abd": abd, "elytra": organic("#3a2c1c", "#241a10", 5),
             "eye": flat("#ffe89a"), "wing": organic("#dfe8f4", "#b6c8e0", 6, 1.5, 0.05)}
    anims = {
        "idle": anim(merge(bob("body", 1.0, 90),
                           {"wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 1100) * -50"]},
                            "wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 1100) * 50"]}},
                           wave("ant_l", 10, 100, 1), wave("ant_r", -10, 100, 1),
                           {"body": {"rotation": ["math.sin(query.life_time * 60) * 6", "0", "math.sin(query.life_time * 47) * 6"]}})),
    }
    return make("ed_firefly", "Glow Firefly", ("#c8ff3a", "#2b2118"), bones, skins, anims, ["idle"],
                {"role": "passive", "health": 3, "speed": 0.2, "fly": True, "fly_speed": 0.06, "box": [0.3, 0.3],
                 "family": ["insect"], "sound": ("bat", [2.0, 2.0]),
                 "spawn": {"biomes": ["forest", "swamp", "jungle"], "weight": 14, "herd": [3, 6]},
                 "loot": [("minecraft:glowstone_dust", 0, 1)]},
                scale=1.6, glow=True)


# ================================================================== BUTTERFLY SWARM
def butterflies():
    PAL = [("#ff9a1c", "#ffd23a", "#2a1408"), ("#3a8cff", "#8ac8ff", "#0c1a3a"), ("#ff5aa8", "#ffb0d6", "#3a0c24"),
           ("#ffe23a", "#fff4a0", "#3a2c08"), ("#4ae0b0", "#b0ffe8", "#08302a")]
    POS = [(0, 11, 0), (7, 15, -5), (-7, 8, -3), (5, 6, 6), (-5, 14, 7)]

    def wing_skin(i, cx):
        a, b, edge = PAL[i]
        def f(p):
            ax = abs(p.p[0] - cx)
            c = mix(a, b, min(1.0, ax / 6.5) * 0.7)
            if p.face in ("top", "bottom"):
                z = p.p[2]
                if ax > 5.4 or ax < 0.9: c = edge
                elif abs(p.fh - 1 - p.y - p.fh / 2) > 1.4 or p.y in (0, p.fh - 1): c = mix(c, edge, 0.7)
                if 4.2 < ax < 5.4 and hash01(z * 2, i, 1) > 0.45 and p.y in (1, 2): c = "#ffffff"
                if p.face == "bottom": c = shade(c, 0.9)
                return c
            return edge
        return f
    bones = [B("swarm", None, [0, 11, 0])]
    skins = {"default": flat("#221810")}
    anim_idle = {"swarm": {"rotation": ["0", "query.life_time * 40", "0"], "position": ["0", "math.sin(query.life_time * 80) * 1.0", "0"]}}
    for i, (x, y, z) in enumerate(POS):
        bones.append(B(f"b{i}", "swarm", [x, y, z], [C([x - 0.5, y - 0.5, z - 1.5], [1, 1, 3], "bod"),
                                                      C([x - 0.5, y - 0.5, z - 2.5], [1, 1, 1], "bod")]))
        bones.append(B(f"wl{i}", f"b{i}", [x + 0.5, y, z], [C([x + 0.5, y, z - 2], [6, 1, 5], f"wingl{i}")]))
        bones.append(B(f"wr{i}", f"b{i}", [x - 0.5, y, z], [C([x - 6.5, y, z - 2], [6, 1, 5], f"wingr{i}")]))
        skins[f"wingl{i}"] = wing_skin(i, x + 0.5)
        skins[f"wingr{i}"] = wing_skin(i, x - 0.5)
        r = 340 + 37 * i
        anim_idle[f"wl{i}"] = {"rotation": ["0", "0", f"math.sin(query.life_time * {r} + {i}) * -45"]}
        anim_idle[f"wr{i}"] = {"rotation": ["0", "0", f"math.sin(query.life_time * {r} + {i}) * 45"]}
        anim_idle[f"b{i}"] = {"position": ["0", f"math.sin(query.life_time * {70 + 9 * i} + {i}) * 1.5", "0"]}
    skins["bod"] = flat("#2a1c10")
    return make("ed_butterfly_swarm", "Butterfly Swarm", ("#ff9a1c", "#3a8cff"), bones, skins, {"idle": anim(anim_idle)}, ["idle"],
                {"role": "passive", "health": 6, "speed": 0.2, "fly": True, "fly_speed": 0.08, "box": [0.8, 1.0],
                 "family": ["insect"], "sound": ("parrot", [1.9, 2.0]),
                 "spawn": {"biomes": ["plains", "forest", "jungle"], "weight": 10, "herd": [1, 2]},
                 "loot": [("minecraft:sugar", 0, 1), ("minecraft:bone_meal", 1, 2)]},
                scale=1.0, glow=False)


# ================================================================== STAR SCORPION
def scorpion():
    shell = chitin("#3a2a6a", "#7a58c8", 4, 1, 5.0)
    claw = chitin("#d8641c", "#ffa04a", 5)
    legs = [(f"leg_{s}{i}", d, z) for i, z in enumerate([-4, -2, 0, 2]) for s, d in (("l", 1), ("r", -1))]
    order = ["leg_l0", "leg_r0", "leg_r1", "leg_l1", "leg_l2", "leg_r2", "leg_r3", "leg_l3"]
    claw_l = [C([3, 5, -9], [2, 2, 4], "shell"), C([4, 5, -13], [2, 2, 4], "claw"), C([3, 5, -16], [4, 2, 3], "claw"),
              C([5, 5, -19], [2, 2, 3], "claw"), C([3, 5, -19], [1, 2, 3], "claw")]
    bones = [
        B("body", None, [0, 6, 0], [C([-4, 4, -6], [8, 4, 10], "shell"), C([-3, 5, -9], [6, 3, 3], "shell"),
                                  C([-2, 7, -7], [1, 1, 1], "eye"), C([1, 7, -7], [1, 1, 1], "eye"),
                                  C([-3, 8, -5], [1, 1, 1], "eye"), C([2, 8, -5], [1, 1, 1], "eye"),
                                  C([-2, 8, -2], [4, 1, 6], "shell")]),
        B("claw_l", "body", [3, 6, -7], claw_l),
        B("claw_r", "body", [-3, 6, -7], [mir(c) for c in claw_l]),
        B("tail0", "body", [0, 6, 5], [C([-1.5, 5, 4], [3, 3, 4], "shell")]),
        B("tail1", "tail0", [0, 6, 7], [C([-1.5, 8, 6], [3, 4, 3], "shell")]),
        B("tail2", "tail1", [0, 12, 6], [C([-1.5, 12, 3], [3, 3, 4], "shell")]),
        B("tail3", "tail2", [0, 13, 3], [C([-1.5, 12, -1], [3, 3, 4], "claw"), C([-0.5, 9, -1], [1, 3, 1], "sting")]),
    ] + insect_legs(legs, 5, 3, 4, 0, 5, "shell", 1)
    skins = {"default": shell, "shell": shell, "claw": claw, "eye": lit("#ff4aff"), "sting": lit("#ff4aff")}
    anims = {
        "walk": anim(merge(hex_walk(order, 30, 50), bob("body", 0.3, 170), wave("tail1", 6, 100, 0),
                           wave("tail2", 8, 100, 0, 1), wave("tail3", 8, 100, 0, 2),
                           wave("claw_l", 10, 90, 1), wave("claw_r", -10, 90, 1, 2))),
        "idle": anim(merge(wave("tail0", 3, 50, 0), wave("tail1", 8, 45, 0, 1), wave("tail2", 10, 45, 0, 2), wave("tail3", 14, 45, 0, 3),
                           wave("claw_l", 8, 40, 1), wave("claw_r", -8, 40, 1, 1.5), bob("body", 0.2, 60))),
        "attack": anim(merge({"tail1": {"rotation": ["math.sin(variable.attack_time * 180) * 50", "0", "0"]},
                              "tail3": {"rotation": ["math.sin(variable.attack_time * 180) * 40", "0", "0"]}}), loop=False),
    }
    return make("ed_star_scorpion", "Star Scorpion", ("#3a2a6a", "#ff4aff"), bones, skins, anims, [WALK, "idle", "attack"],
                {"role": "hostile", "health": 20, "speed": 0.28, "damage": 4, "box": [1.2, 0.9], "family": ["insect"],
                 "sound": ("spider", [0.7, 0.9]),
                 "spawn": {"biomes": ["desert", "mesa"], "weight": 8, "herd": [1, 2]},
                 "loot": [("minecraft:spider_eye", 0, 2), ("minecraft:amethyst_shard", 0, 1)], "xp": 5},
                scale=1.4, glow=True)


# ================================================================== MOON CENTIPEDE
def centipede():
    plate = stripes("#c9601c", "#5a2408", 5.0, 1.0, 2, 4)
    N_SEG = 8
    bones = [
        B("head", None, [0, 3, 0], [
            C([-3, 1, -4], [6, 5, 5], "headp"), C([-2.5, 4, -4.5], [1, 1, 1], "eye"),
            C([1.5, 4, -4.5], [1, 1, 1], "eye"),
            C([-2, 1, -5], [1, 3, 1], "fang"), C([1, 1, -5], [1, 3, 1], "fang")]),
        B("ant_l", "head", [1.5, 5, -3], [C([1, 5, -8], [1, 1, 5], "leg")]),
        B("ant_r", "head", [-1.5, 5, -3], [C([-2, 5, -8], [1, 1, 5], "leg")]),
    ]
    prev = "head"
    for k in range(N_SEG):
        z = 1 + 5 * k
        cubes = [C([-3, 1, z], [6, 4, 5], "plate"), C([-1, 5, z + 1], [2, 1, 3], "ridge"),
                 C([3, 2, z + 1], [3, 1, 1], "leg"), C([5, 0, z + 1], [1, 3, 1], "leg"),
                 C([-6, 2, z + 1], [3, 1, 1], "leg"), C([-6, 0, z + 1], [1, 3, 1], "leg"),
                 C([3, 2, z + 3], [3, 1, 1], "leg"), C([5, 0, z + 3], [1, 3, 1], "leg"),
                 C([-6, 2, z + 3], [3, 1, 1], "leg"), C([-6, 0, z + 3], [1, 3, 1], "leg")]
        if k == N_SEG - 1:
            cubes += [C([-2, 2, z + 5], [1, 1, 3], "leg"), C([1, 2, z + 5], [1, 1, 3], "leg")]
        bones.append(B(f"s{k}", prev, [0, 3, z], cubes))
        prev = f"s{k}"
    skins = {"default": plate, "plate": plate, "headp": chitin("#8a3a10", "#c9601c", 8), "ridge": flat("#f0d060"),
             "leg": flat("#e8c040", 0.1), "eye": lit("#ff3030"), "fang": lit("#7cff4a")}
    walk, idle = {}, {}
    for k in range(N_SEG):
        walk[f"s{k}"] = {"rotation": ["0", f"math.sin(query.modified_distance_moved * 55 - {k * 0.9}) * 90 * query.modified_move_speed", "0"]}
        idle[f"s{k}"] = {"rotation": ["0", f"math.sin(query.life_time * 55 - {k * 0.8}) * 5", "0"]}
    anims = {"walk": anim(merge(walk, wave("ant_l", 14, 140, 1), wave("ant_r", -14, 140, 1))),
             "idle": anim(merge(idle, wave("ant_l", 18, 70, 1), wave("ant_r", -18, 70, 1, 1.5)))}
    # put the whole thing so the head faces -Z and the tail trails toward +Z (already the case)
    return make("ed_moon_centipede", "Moon Centipede", ("#c9601c", "#5a2408"), bones, skins, anims, [WALK, "idle"],
                {"role": "hostile", "health": 18, "speed": 0.3, "damage": 3, "box": [0.7, 0.5], "family": ["insect"],
                 "sound": ("silverfish", [0.9, 1.1]),
                 "spawn": {"biomes": ["jungle", "swamp", "taiga"], "weight": 6, "herd": [1, 1]},
                 "loot": [("minecraft:fermented_spider_eye", 0, 1), ("minecraft:string", 1, 2)], "xp": 4},
                scale=1.3, glow=True)


# ================================================================== JELLYFLOAT (hover, friendly)
def jelly():
    def bell(p):
        n = N(p, 5, 2.5)
        c = mix("#ff8ad8", "#ffd0f4", 0.25 + 0.6 * n)
        if hash01(p.p[0] * 2, p.p[1] * 2, p.p[2] * 2, 8) > 0.86: return glow("#e8fff4")
        if p.face == "bottom": return glow("#ff5ac8")
        if p.face == "top": c = shade(c, 1.1)
        return c
    def tent(p):
        t = max(0.0, min(1.0, (14 - p.p[1]) / 14.0))
        c = mix("#ff8ad8", "#5ae8ff", t)
        return glow(shade(c, 0.85 + 0.3 * hash01(p.p[0], p.p[1], p.p[2], 3))) if t > 0.55 else c
    def arm(p): return shade(mix("#ffb0e8", "#ff8ad8", N(p, 3, 1.5)), 0.95)
    bones = [B("bell", None, [0, 14, 0], [
        C([-6, 14, -6], [12, 2, 12], "bell"), C([-5, 16, -5], [10, 3, 10], "bell"), C([-3, 19, -3], [6, 2, 6], "bell"),
        C([-3, 16, -5.6], [2, 2, 1], "eye"), C([1, 16, -5.6], [2, 2, 1], "eye"), C([-1, 15, -6.6], [2, 1, 1], "mouth"),
        C([-4.5, 15, -6.6], [1, 1, 1], "blush"), C([3.5, 15, -6.6], [1, 1, 1], "blush")])]
    for i, (x, z) in enumerate([(4, 4), (-5, 4), (4, -4), (-5, -4)]):
        bones.append(B(f"t{i}", "bell", [x, 14, z], [C([x, 7, z], [1, 7, 1], "tent")]))
        bones.append(B(f"t{i}b", f"t{i}", [x, 7, z], [C([x, 0, z], [1, 7, 1], "tent")]))
    for i, (x, z) in enumerate([(-1, 0), (1, -2), (-3, -2)]):
        bones.append(B(f"o{i}", "bell", [x + 1, 14, z + 1], [C([x, 9, z], [3, 5, 3], "arm")]))
        bones.append(B(f"o{i}b", f"o{i}", [x + 1, 9, z + 1], [C([x + 0.5, 4, z + 0.5], [2, 5, 2], "arm")]))
    skins = {"default": bell, "bell": bell, "tent": tent, "arm": arm, "eye": flat("#301040"), "mouth": flat("#a02070"),
             "blush": lit("#ff9ab8")}
    idle = merge(bob("bell", 1.2, 55))
    walk = {}
    for i in range(4):
        idle.update(wave(f"t{i}", 8, 55, 0, i)); idle.update(wave(f"t{i}", 6, 45, 2, i))
        idle.update(wave(f"t{i}b", 14, 65, 0, i + 1))
    for i in range(3):
        idle.update(wave(f"o{i}", 6, 50, 0, i * 2)); idle.update(wave(f"o{i}b", 10, 60, 2, i))
    idle["bell"]["rotation"] = ["math.sin(query.life_time * 55) * 3 + query.modified_move_speed * 20", "0", "0"]
    anims = {"idle": anim(idle)}
    return make("ed_jellyfloat", "Jellyfloat", ("#ff8ad8", "#5ae8ff"), bones, skins, anims, ["idle"],
                {"role": "passive", "health": 8, "speed": 0.2, "hover": True, "fly_speed": 0.1, "box": [0.9, 1.4],
                 "family": ["alien"], "sound": ("vex", [1.9, 2.0]),
                 "spawn": {"biomes": ["overworld"], "weight": 5, "herd": [1, 3]},
                 "loot": [("minecraft:glowstone_dust", 1, 2), ("minecraft:slime_ball", 0, 1)]},
                scale=1.3, glow=True)


SPECS = [firefly(), butterflies(), scorpion(), centipede(), jelly()]
