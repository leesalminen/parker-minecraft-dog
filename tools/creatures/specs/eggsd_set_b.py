"""eggsd set B: space dog, rocket pup, giant beetle (mount), giant ant, mantis."""
from specs.eggsd_kit import *

WALK = {"walk": "query.modified_move_speed > 0.02"}


def insect_legs(names_sides, hip_y, upper_len, out0, knee_h, drop, skin, thick=1):
    """names_sides: list of (name, side(+1/-1), z). Stepped insect legs (no cube rotation needed)."""
    bones = []
    for name, s, z in names_sides:
        if s > 0:
            up = C([out0, hip_y, z], [upper_len, thick, thick], skin)
            lo = C([out0 + upper_len - thick, hip_y - drop, z], [thick, drop + thick, thick], skin)
            piv = [out0, hip_y, z]
        else:
            up = C([-out0 - upper_len, hip_y, z], [upper_len, thick, thick], skin)
            lo = C([-out0 - upper_len, hip_y - drop, z], [thick, drop + thick, thick], skin)
            piv = [-out0, hip_y, z]
        bones.append(B(name, "body", piv, [up, lo]))
    return bones


# ================================================================== SPACE DOG (companion)
def spacedog():
    fur = spotted("#f3ecdc", "#c99a5a", 9, 1.3, 0.70, "#dcd2bc")
    fur_b = belly(fur, "#fffaf0", 5.0, 2.0, 0.8)
    def vest(p):
        c = metal("#f0781e", "#a04a0c", 40, False)(p)
        if p.face in ("front", "back", "east", "west") and p.y in (p.fh // 2, p.fh // 2 + 1): return "#f4f4f0"
        if p.face == "top" and p.x == p.fw // 2: return "#f4f4f0"
        return c
    bones = [
        B("body", None, [0, 8, 0], [C([-3, 6, -6], [6, 6, 11], "furb"), C([-3, 6, -4], [6, 6, 6], "vest", inflate=0.4),
                                  C([-1.5, 9.5, -2], [3, 1, 3], "badge", inflate=0.4)]),
        B("head", "body", [0, 10, -6], [
            C([-3, 8, -11], [6, 6, 5], "fur"), C([-2, 8, -14], [4, 3, 3], "snoutc"), C([-1, 10, -14.6], [2, 1, 1], "nose"),
            C([-1, 7, -13], [2, 1, 2], "tongue"),
            C([-2.5, 11, -11.6], [2, 2, 1], "eye"), C([0.5, 11, -11.6], [2, 2, 1], "eye"),
            C([-4, 9, -10], [1, 4, 3], "ear"), C([3, 9, -10], [1, 4, 3], "ear"),
            C([-3, 13, -11], [6, 1, 5], "band", inflate=0.3)]),
        B("antenna", "head", [2, 14, -9], [C([1.5, 14, -9.5], [1, 3, 1], "band"), C([1, 17, -10], [2, 2, 2], "bulb")]),
        leg("leg_fl", "body", 1, 6, -6, 2, 6, 2, "fur", foot=(3, 1, 3), foot_skin="pad"),
        leg("leg_fr", "body", -3, 6, -6, 2, 6, 2, "fur", foot=(3, 1, 3), foot_skin="pad"),
        leg("leg_bl", "body", 1, 6, 3, 2, 6, 3, "fur", foot=(3, 1, 4), foot_skin="pad"),
        leg("leg_br", "body", -3, 6, 3, 2, 6, 3, "fur", foot=(3, 1, 4), foot_skin="pad"),
        B("tail", "body", [0, 10, 5], [C([-1, 10, 5], [2, 2, 3], "fur"), C([-1, 11, 7], [2, 4, 2], "fur")]),
    ]
    skins = {"default": fur, "fur": fur, "furb": fur_b, "vest": vest, "badge": lit("#5cf0ff"),
             "snoutc": organic("#fff6e6", "#eadfc8", 4, 2), "nose": flat("#1c1c22"), "tongue": flat("#f08aa0"),
             "eye": eyes("#ffffff", "#2a1a10", "#000000"), "ear": organic("#8a5a2c", "#5c3a18", 5),
             "band": metal("#33394a", "#181c28", 41, False), "bulb": lit("#ff5a7a"), "pad": flat("#3a3038")}
    anims = {
        "walk": anim(merge(quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", 40, 50),
                           wave("tail", 22, 240, 2), wave("antenna", 8, 150, 0), bob("body", 0.35, 130))),
        "idle": anim(merge(bob("body", 0.25, 60), wave("tail", 26, 140, 2), wave("antenna", 12, 90, 0),
                           {"head": {"rotation": ["math.sin(query.life_time * 35) * 3", "math.sin(query.life_time * 19) * 10", "0"]}})),
    }
    return make("ed_space_dog", "Space Dog", ("#f3ecdc", "#f0781e"), bones, skins, anims, [WALK, "idle"],
                {"role": "companion", "health": 18, "speed": 0.34, "damage": 4, "box": [0.6, 1.0], "family": ["space_pet"],
                 "tame_items": ["minecraft:bone", "minecraft:cooked_beef"], "sound": "wolf",
                 "spawn": {"biomes": ["plains", "forest"], "weight": 5, "herd": [1, 2]},
                 "loot": [("minecraft:bone", 0, 2)]},
                scale=1.2, glow=True)


# ================================================================== ROCKET PUP (companion)
def rocketpup():
    fur = spotted("#f7f4ee", "#2a2a32", 13, 1.5, 0.74, "#e6e2d8")
    def rocket(p):
        y = p.p[1]
        c = metal("#f4f4f0", "#a0a4ac", 50, False)(p)
        if 8 <= y < 9.6 or 11 <= y < 12: return metal("#e0342c", "#8a1a14", 51, False)(p)
        return c
    def flame(p):
        y = p.p[1]
        return glow(mix("#ff4a10", "#ffe45a", max(0, min(1, (y - 2) / 3))))
    bones = [
        B("body", None, [0, 6, 0], [C([-3, 4, -3], [6, 5, 7], "furb")]),
        B("head", "body", [0, 9, -3], [
            C([-4, 8, -9], [8, 7, 7], "fur"), C([-2, 8, -11], [4, 3, 2], "snoutc"), C([-1, 10, -11.6], [2, 1, 1], "nose"),
            C([-3.5, 10, -9.6], [2, 3, 1], "eye"), C([1.5, 10, -9.6], [2, 3, 1], "eye"),
            C([-5, 9, -8], [1, 5, 3], "ear"), C([4, 9, -8], [1, 5, 3], "ear"),
            C([-4, 13, -9.4], [8, 2, 1], "strap", inflate=0.1),
            C([-3.5, 13, -10.4], [3, 2, 1], "lens"), C([0.5, 13, -10.4], [3, 2, 1], "lens")]),
        B("pack", "body", [0, 6, 3], [C([-1.5, 6, 2], [3, 7, 3], "rocket"), C([-1, 13, 2.5], [2, 2, 2], "cone"),
                                   C([-2.5, 6, 3], [1, 3, 1], "cone"), C([1.5, 6, 3], [1, 3, 1], "cone"),
                                   C([-1, 5, 2.5], [2, 1, 2], "nozzle")]),
        B("flame", "pack", [0, 5, 3.5], [C([-1, 2, 2.5], [2, 3, 2], "flame"), C([-0.5, 0.5, 3], [1, 2, 1], "flame")]),
        leg("leg_fl", "body", 1, 4, -3, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="pad"),
        leg("leg_fr", "body", -3, 4, -3, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="pad"),
        leg("leg_bl", "body", 1.5, 4, 1.5, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="pad"),
        leg("leg_br", "body", -3.5, 4, 1.5, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="pad"),
        B("tail", "body", [2.5, 7, 4], [C([2, 7, 4], [1, 1, 3], "fur"), C([2, 8, 6], [1, 3, 1], "fur")]),
    ]
    skins = {"default": fur, "fur": fur, "furb": belly(fur, "#ffffff", 5.5, 1.5, 0.7), "snoutc": flat("#fff8ee"),
             "nose": flat("#18181e"), "eye": eyes("#ffffff", "#2a1a10", "#000000"),
             "ear": organic("#26262c", "#16161a", 5), "strap": flat("#8a5a2c"), "lens": lit("#6cf0ff"),
             "rocket": rocket, "cone": metal("#e0342c", "#8a1a14", 52, False), "nozzle": metal("#555a66", "#22252c", 53, False),
             "flame": flame, "pad": flat("#3a3038")}
    flick = "math.sin(query.life_time * 900) * 0.6"
    anims = {
        "walk": anim(merge(quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", 45, 60), wave("tail", 25, 260, 2),
                           bob("body", 0.4, 160), {"flame": {"position": ["0", flick, "0"]}})),
        "idle": anim(merge(bob("body", 0.25, 60), wave("tail", 30, 150, 2), {"flame": {"position": ["0", flick, "0"]}},
                           {"head": {"rotation": ["math.sin(query.life_time * 35) * 4", "math.sin(query.life_time * 19) * 12",
                                                  "math.sin(query.life_time * 27) * 4"]}})),
    }
    return make("ed_rocket_pup", "Rocket Pup", ("#f7f4ee", "#e0342c"), bones, skins, anims, [WALK, "idle"],
                {"role": "companion", "health": 14, "speed": 0.36, "damage": 3, "box": [0.55, 0.9], "family": ["space_pet"],
                 "tame_items": ["minecraft:bone", "minecraft:cooked_chicken"], "sound": ("wolf", [1.3, 1.5]),
                 "spawn": {"biomes": ["plains", "savanna"], "weight": 4, "herd": [1, 2]},
                 "loot": [("minecraft:gunpowder", 0, 2), ("minecraft:bone", 0, 1)]},
                scale=1.15, glow=True)


# ================================================================== GIANT BEETLE (mount)
def beetle():
    shell = chitin("#1c7a5e", "#48e0aa", 6, 2, 8.0)
    dark = chitin("#134a3a", "#1f7a5e", 7)
    horn = organic("#5a3a1c", "#2c1c0c", 8, 2, 0.08)
    legs = [("leg_lf", 1, -5), ("leg_rf", -1, -5), ("leg_rm", -1, 0), ("leg_lm", 1, 0), ("leg_lr", 1, 5), ("leg_rr", -1, 5)]
    bones = [
        B("body", None, [0, 8, 0], [C([-5, 5, -7], [10, 6, 5], "dark"), C([-4, 4, -2], [8, 2, 14], "dark")]),
        B("elytra_l", "body", [3, 11, -3], [C([0, 6, -3], [6, 6, 15], "shell", inflate=0.0)]),
        B("elytra_r", "body", [-3, 11, -3], [C([-6, 6, -3], [6, 6, 15], "shell", inflate=0.0)]),
        B("head", "body", [0, 8, -8], [
            C([-3, 6, -12], [6, 4, 5], "dark"), C([-4, 8, -11], [1, 2, 2], "eye"), C([3, 8, -11], [1, 2, 2], "eye"),
            C([-3, 6, -14], [1, 2, 2], "horn"), C([2, 6, -14], [1, 2, 2], "horn"),
            C([-1, 9, -11], [2, 3, 2], "horn"), C([-1, 11, -16], [2, 2, 6], "horn"), C([-1, 12, -19], [2, 2, 3], "horn"),
            C([-1, 10, -16], [2, 1, 2], "horn")]),
        B("ant_l", "head", [1, 9, -12], [C([1, 9, -12.5], [1, 1, 3], "horn"), C([1, 9, -15.5], [1, 2, 1], "horn")]),
        B("ant_r", "head", [-1, 9, -12], [C([-2, 9, -12.5], [1, 1, 3], "horn"), C([-2, 9, -15.5], [1, 2, 1], "horn")]),
    ] + insect_legs(legs, 6, 4, 5, 0, 6, "dark", 2)
    skins = {"default": dark, "shell": shell, "dark": dark, "horn": horn, "eye": eyes("#111111", "#e8ffe0", "#050505")}
    walk_l = hex_walk([n for n, _, _ in legs], 28, 40)
    anims = {
        "walk": anim(merge(walk_l, bob("body", 0.4, 160), wave("ant_l", 12, 120, 1), wave("ant_r", -12, 120, 1))),
        "idle": anim(merge(bob("body", 0.3, 50), wave("ant_l", 14, 80, 1), wave("ant_r", -14, 80, 1, 1.0),
                           wave("elytra_l", 2.5, 90, 2), wave("elytra_r", -2.5, 90, 2),
                           {"head": {"rotation": ["math.sin(query.life_time * 30) * 4", "0", "0"]}})),
    }
    return make("ed_giant_beetle", "Giant Rhino Beetle", ("#1c7a5e", "#48e0aa"), bones, skins, anims, [WALK, "idle"],
                {"role": "mount", "health": 44, "speed": 0.24, "damage": 5, "box": [1.6, 1.3], "family": ["insect"],
                 "ride": {"seats": [[0, 1.05, 0.1]], "jump": 0.5}, "knockback_resist": 0.4, "sound": ("silverfish", [0.55, 0.7]),
                 "spawn": {"biomes": ["jungle", "forest"], "weight": 3, "herd": [1, 1]},
                 "loot": [("minecraft:slime_ball", 1, 2), ("minecraft:emerald", 0, 1)]},
                scale=1.5, glow=False)


# ================================================================== GIANT ANT
def ant():
    body = chitin("#a83a1f", "#e06a36", 11)
    gaster = stripes("#8a2c16", "#3a0e0a", 4.0, 1.2, 2, 12)
    dark = chitin("#5a1a0c", "#8a2c16", 13)
    zs = [-8, -6, -4]
    legs = []
    for i, z in enumerate(zs):
        legs.append((f"leg_l{i}", 1, z)); legs.append((f"leg_r{i}", -1, z))
    order = ["leg_l0", "leg_r1", "leg_l2", "leg_r0", "leg_l1", "leg_r2"]
    bones = [
        B("body", None, [0, 8, -6], [C([-2.5, 7, -9], [5, 5, 5], "body"), C([-1, 8, -4], [2, 2, 3], "dark"),
                                   C([-1, 10, -4], [2, 2, 2], "dark")]),
        B("gaster", "body", [0, 9, -1], [C([-4, 6, -1], [8, 7, 11], "gaster"), C([-3, 7, 10], [6, 5, 2], "gaster")]),
        B("head", "body", [0, 10, -9], [
            C([-3, 7, -14], [6, 5, 5], "body"), C([-4, 9, -13], [1, 2, 2], "eye"), C([3, 9, -13], [1, 2, 2], "eye"),
            C([-2, 7, -16], [1, 1, 2], "mand"), C([1, 7, -16], [1, 1, 2], "mand"),
            C([-1, 7, -17], [1, 1, 1], "mand"), C([0, 7, -17], [1, 1, 1], "mand")]),
        B("ant_l", "head", [1.5, 12, -13], [C([1, 12, -13], [1, 3, 1], "dark"), C([1, 14, -16], [1, 1, 3], "dark")]),
        B("ant_r", "head", [-1.5, 12, -13], [C([-2, 12, -13], [1, 3, 1], "dark"), C([-2, 14, -16], [1, 1, 3], "dark")]),
    ] + insect_legs(legs, 8, 3, 2, 0, 8, "dark", 1)
    skins = {"default": body, "body": body, "gaster": gaster, "dark": dark, "mand": flat("#e8d8b0"),
             "eye": eyes("#111111", "#f0e0c0", "#050505")}
    anims = {
        "walk": anim(merge(hex_walk(order, 34, 45), bob("body", 0.35, 170), wave("ant_l", 14, 140, 1), wave("ant_r", -14, 140, 1),
                           wave("gaster", 4, 90, 1))),
        "idle": anim(merge(bob("body", 0.2, 60), wave("ant_l", 16, 70, 1), wave("ant_r", -16, 70, 1, 1),
                           wave("ant_l", 8, 50, 0), wave("gaster", 3, 40, 0),
                           {"head": {"rotation": ["0", "math.sin(query.life_time * 24) * 14", "0"]}})),
    }
    return make("ed_giant_ant", "Giant Ant", ("#a83a1f", "#3a0e0a"), bones, skins, anims, [WALK, "idle"],
                {"role": "hostile", "health": 16, "speed": 0.32, "damage": 3, "box": [0.9, 0.9], "family": ["insect"],
                 "sound": ("silverfish", [0.8, 1.0]),
                 "spawn": {"biomes": ["forest", "jungle", "plains"], "weight": 8, "herd": [2, 4]},
                 "loot": [("minecraft:sugar", 0, 2), ("minecraft:spider_eye", 0, 1)], "xp": 3},
                scale=1.4)


# ================================================================== MANTIS
def mantis():
    leaf = chitin("#5fae3c", "#a4e05a", 14)
    lead = chitin("#3c7a26", "#5fae3c", 15)
    wingp = organic("#8fd05a", "#5fa03a", 16, 2.5, 0.10)
    eye = organic("#d9b53a", "#7a5f14", 17, 1.5, 0.12)
    spike = flat("#efe8c8")
    arm_l = B("arm_l", "body", [3, 23, -1], [
        C([2, 22, -9], [2, 2, 8], "lead"), C([2, 13, -10], [2, 10, 2], "leaf"),
        C([4, 20, -10], [1, 1, 2], "spike"), C([4, 17, -10], [1, 1, 2], "spike"), C([4, 14, -10], [1, 1, 2], "spike"),
        C([2.5, 11, -10], [1, 3, 1], "spike")])
    arm_r = B("arm_r", "body", [-3, 23, -1], [mir(c) for c in arm_l["cubes"]])
    legs = [("leg_ml", 1, -1), ("leg_mr", -1, -1), ("leg_rl", 1, 3), ("leg_rr", -1, 3)]
    bones = [
        B("body", None, [0, 14, 0], [C([-2, 12, -2], [4, 13, 4], "leaf"), C([-2.5, 11, 1], [5, 4, 12], "leaf"),
                                   C([-3, 15, 2], [6, 1, 11], "wing"), C([-2, 16, 3], [4, 1, 9], "wing")]),
        B("head", "body", [0, 25, -1], [
            C([-3, 25, -3.5], [6, 4, 4], "leaf"), C([-2, 24, -3.5], [4, 1, 3], "leaf"),
            C([-5, 26, -3], [2, 3, 3], "eye"), C([3, 26, -3], [2, 3, 3], "eye"),
            C([-1, 24, -4.5], [2, 1, 1], "lead"), C([-1.5, 28, -3], [1, 4, 1], "lead"), C([0.5, 28, -3], [1, 4, 1], "lead")]),
        arm_l, arm_r,
    ] + insect_legs(legs, 13, 3, 2, 0, 13, "lead", 1)
    skins = {"default": leaf, "leaf": leaf, "lead": lead, "wing": wingp, "eye": eye, "spike": spike}
    anims = {
        "walk": anim(merge(quad_walk("leg_ml", "leg_mr", "leg_rl", "leg_rr", 32, 50),
                           swing({"arm_l": 0, "arm_r": 180}, 12, 0, 50), bob("body", 0.4, 100))),
        "idle": anim(merge(bob("body", 0.3, 45), wave("arm_l", 7, 55, 0), wave("arm_r", 7, 55, 0, 3.14),
                           {"head": {"rotation": ["math.sin(query.life_time * 30) * 3", "math.sin(query.life_time * 21) * 24",
                                                  "math.sin(query.life_time * 17) * 6"]}})),
        "attack": anim(merge({"arm_l": {"rotation": ["math.sin(variable.attack_time * 180) * -70", "0", "0"]},
                              "arm_r": {"rotation": ["math.sin(variable.attack_time * 180) * -70", "0", "0"]}}), loop=False),
    }
    return make("ed_mantis", "Leaf Mantis", ("#5fae3c", "#d9b53a"), bones, skins, anims, [WALK, "idle", "attack"],
                {"role": "hostile", "health": 22, "speed": 0.3, "damage": 5, "box": [0.8, 2.1], "family": ["insect"],
                 "reach": 1.2, "sound": ("spider", [1.3, 1.5]),
                 "spawn": {"biomes": ["jungle", "forest"], "weight": 5, "herd": [1, 1]},
                 "loot": [("minecraft:spider_eye", 0, 1), ("minecraft:string", 1, 2)], "xp": 6},
                scale=1.3)


SPECS = [spacedog(), rocketpup(), beetle(), ant(), mantis()]
