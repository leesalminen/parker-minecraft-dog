"""eggsd set D: crystal golem, lava crab, cyber bunny, moon rover (mount), vacuum bot."""
from specs.eggsd_kit import *
from specs.eggsd_set_b import insect_legs

WALK = {"walk": "query.modified_move_speed > 0.02"}


# ================================================================== CRYSTAL GOLEM (big)
def golem():
    def rock(p):
        c = organic("#5a5070", "#2e2842", 3, 2.5, 0.10)(p)
        n = N(p, 21, 1.4)
        if abs(n - 0.5) < 0.035: c = shade(c, 0.5)
        if hash01(p.p[0] * 2, p.p[1] * 2, p.p[2] * 2, 9) > 0.985: return glow("#c48aff")
        return c
    def crystal(hi, lo):
        def f(p):
            t = min(1.0, max(0.0, N(p, 4, 2.0) * 0.6 + (p.p[1] % 12) / 30.0))
            c = mix(lo, hi, t)
            if p.face == "top": c = mix(c, "#ffffff", 0.35)
            return glow(c)
        return f
    def core(p):
        if p.x in (0, p.fw - 1) or p.y in (0, p.fh - 1): return "#3a2a5a"
        return glow(mix("#d8a0ff", "#ffffff", 0.5 * N(p, 3, 1.2)))
    def cr(o, s, skin="crystal", rot=None):
        d = C(o, s, skin)
        if rot:
            d["rot"] = rot; d["pivot"] = [o[0] + s[0] / 2, o[1], o[2] + s[2] / 2]
        return d
    arm_l = B("arm_l", "body", [11, 27, 0], [
        C([9, 12, -3], [5, 15, 5], "rock"), C([8, 6, -4], [7, 7, 7], "rock"),
        cr([9, 13, -5], [2, 4, 2], "crystal2", [-25, 0, 0]), cr([12, 13, 2], [2, 5, 2], "crystal", [20, 0, 15]),
        cr([9, 27, -1], [3, 5, 3], "crystal", [0, 0, -20])])
    arm_r = B("arm_r", "body", [-11, 27, 0], [mir(c) for c in arm_l["cubes"]])
    bones = [
        B("body", None, [0, 12, 0], [
            C([-8, 10, -5], [16, 10, 10], "rock"), C([-9, 20, -6], [18, 8, 12], "rock"),
            C([-3, 15, -5.7], [6, 6, 1], "core"),
            cr([-6, 27, 2], [3, 9, 3], "crystal", [15, 0, 8]), cr([2, 27, 3], [3, 11, 3], "crystal2", [10, 0, -10]),
            cr([-1, 27, 4], [4, 8, 4], "crystal", [20, 0, 0]), cr([-9, 26, -3], [3, 6, 3], "crystal2", [0, 0, 25]),
            cr([6, 26, -3], [3, 6, 3], "crystal", [0, 0, -25]), cr([-4, 12, 5], [3, 6, 3], "crystal", [30, 0, 0])]),
        B("head", "body", [0, 28, -1], [
            C([-4, 28, -5], [8, 7, 8], "rock"), C([-3, 27, -4], [6, 2, 6], "rock"),
            C([-3, 31, -5.6], [2, 2, 1], "eye"), C([1, 31, -5.6], [2, 2, 1], "eye"),
            cr([-1, 35, -2], [2, 6, 2], "crystal2", [0, 0, 0]), cr([-3, 35, -1], [2, 4, 2], "crystal", [0, 0, 15]),
            cr([1, 35, -1], [2, 4, 2], "crystal", [0, 0, -15])]),
        arm_l, arm_r,
        leg("leg_l", "body", 1, 10, -3, 6, 10, 6, "rock", foot=(7, 2, 8), foot_skin="rock"),
        leg("leg_r", "body", -7, 10, -3, 6, 10, 6, "rock", foot=(7, 2, 8), foot_skin="rock"),
    ]
    skins = {"default": rock, "rock": rock, "crystal": crystal("#e0b0ff", "#8a3ad8"), "crystal2": crystal("#a0f4ff", "#2a8ad8"),
             "core": core, "eye": lit("#ff9aff")}
    anims = {
        "walk": anim(merge(biped_walk("leg_l", "leg_r", 26, 30), swing({"arm_l": 180, "arm_r": 0}, 20, 0, 30), bob("body", 0.6, 100))),
        "idle": anim(merge(bob("body", 0.3, 40), wave("arm_l", 4, 35, 2), wave("arm_r", -4, 35, 2, 1.0),
                           {"head": {"rotation": ["math.sin(query.life_time * 25) * 3", "math.sin(query.life_time * 17) * 12", "0"]}})),
        "attack": anim(merge({"arm_l": {"rotation": ["math.sin(variable.attack_time * 180) * -100", "0", "0"]},
                              "arm_r": {"rotation": ["math.sin(variable.attack_time * 180) * -100", "0", "0"]}}), loop=False),
    }
    return make("ed_crystal_golem", "Crystal Golem", ("#5a5070", "#c48aff"), bones, skins, anims, [WALK, "idle", "attack"],
                {"role": "neutral", "health": 90, "speed": 0.2, "damage": 10, "box": [1.9, 3.3], "family": ["golem"],
                 "knockback_resist": 0.9, "sound": "golem",
                 "spawn": {"biomes": ["extreme_hills"], "weight": 2, "herd": [1, 1]},
                 "loot": [("minecraft:amethyst_shard", 2, 5), ("minecraft:emerald", 0, 2)], "xp": 15},
                scale=1.5, glow=True)


# ================================================================== LAVA CRAB
def crab():
    def shell(p):
        c = organic("#3c2a2a", "#1e1414", 3, 2.5, 0.10)(p)
        n = N(p, 12, 1.8)
        if abs(n - 0.5) < 0.05 or abs(n - 0.75) < 0.03: return glow(mix("#ff5a10", "#ffc030", N(p, 4, 1.0)))
        if p.face == "top": c = shade(c, 1.1)
        return c
    claw = organic("#c8401a", "#7a2010", 5, 2.0, 0.10)
    def claw_f(p):
        c = claw(p)
        if p.face in ("front",) and p.y >= p.fh - 1: return glow("#ffb030")
        return c
    legs = [(f"leg_{s}{i}", d, z) for i, z in enumerate([-3, 0, 3]) for s, d in (("l", 1), ("r", -1))]
    order = ["leg_l0", "leg_r0", "leg_r1", "leg_l1", "leg_l2", "leg_r2"]
    claw_l = [C([7, 5, -8], [3, 2, 5], "claw"), C([6, 4, -15], [6, 5, 7], "claw2"), C([6, 4, -18], [2, 4, 3], "claw2"),
              C([10, 4, -18], [2, 4, 3], "claw2")]
    bones = [
        B("body", None, [0, 5, 0], [C([-7, 3, -5], [14, 5, 10], "shell"), C([-6, 8, -4], [12, 2, 8], "shell"),
                                  C([-5, 5, 5], [10, 2, 1], "claw")]),
        B("eye_l", "body", [3, 10, -4], [C([2.5, 10, -4.5], [1, 3, 1], "claw"), C([2, 13, -5], [2, 2, 2], "eye")]),
        B("eye_r", "body", [-3, 10, -4], [C([-3.5, 10, -4.5], [1, 3, 1], "claw"), C([-4, 13, -5], [2, 2, 2], "eye")]),
        B("claw_l", "body", [7, 6, -6], claw_l),
        B("claw_r", "body", [-7, 6, -6], [mir(c) for c in claw_l]),
    ] + insect_legs(legs, 5, 3, 7, 0, 5, "claw", 2)
    skins = {"default": shell, "shell": shell, "claw": claw, "claw2": claw_f, "eye": eyes("#ffe090", "#ffe090", "#200800", True)}
    anims = {
        "walk": anim(merge(hex_walk(order, 26, 60), bob("body", 0.3, 200), wave("claw_l", 10, 100, 1), wave("claw_r", -10, 100, 1, 1),
                           wave("eye_l", 6, 90, 0), wave("eye_r", 6, 90, 0, 1))),
        "idle": anim(merge(bob("body", 0.2, 50), wave("claw_l", 12, 45, 1), wave("claw_r", -12, 45, 1, 2),
                           wave("claw_l", 5, 60, 0), wave("eye_l", 12, 80, 0), wave("eye_r", 12, 80, 0, 2))),
        "attack": anim(merge({"claw_l": {"rotation": ["math.sin(variable.attack_time * 180) * -50", "0", "0"]},
                              "claw_r": {"rotation": ["math.sin(variable.attack_time * 180) * -50", "0", "0"]}}), loop=False),
    }
    return make("ed_lava_crab", "Lava Crab", ("#3c2a2a", "#ff7a1a"), bones, skins, anims, [WALK, "idle", "attack"],
                {"role": "neutral", "health": 26, "speed": 0.25, "damage": 5, "box": [1.3, 0.9], "family": ["crustacean"],
                 "fire_immune": True, "knockback_resist": 0.3, "sound": ("turtle", [0.8, 1.0]),
                 "spawn": {"biomes": ["desert", "mesa", "beach"], "weight": 6, "herd": [1, 2]},
                 "loot": [("minecraft:magma_cream", 1, 2), ("minecraft:coal", 0, 2)], "xp": 4},
                scale=1.3, glow=True)


# ================================================================== CYBER BUNNY (companion)
def bunny():
    fur = organic("#f6f2ff", "#d8d0ee", 5, 2.5, 0.06)
    fur_b = belly(fur, "#ffffff", 4.5, 2, 0.8)
    plate = metal("#b8c4d4", "#5a6678", 61, True)
    ear_out = fur
    bones = [
        B("body", None, [0, 5, 0], [C([-3, 3, -3], [6, 5, 6], "furb"), C([-4, 3, 1], [8, 6, 5], "furb"),
                                  C([-4.4, 5, 1.5], [1, 3, 3], "plate"), C([3.4, 5, 1.5], [1, 3, 3], "plate"),
                                  C([-1.5, 5, 6], [3, 3, 2], "tail"), C([-0.5, 6.5, 8], [1, 1, 1], "glowdot")]),
        B("head", "body", [0, 7, -3], [
            C([-3, 6, -8], [6, 5, 5], "fur"), C([-4, 6, -7], [8, 3, 3], "fur"), C([-1, 8, -8.6], [2, 1, 1], "nose"),
            C([-3, 9, -8.5], [2, 2, 1], "visor"), C([1, 9, -8.5], [2, 2, 1], "visor"),
            C([-1, 7, -8.5], [2, 1, 1], "mouth")]),
        B("ear_l", "head", [2, 11, -5], [C([1, 11, -6], [2, 8, 1], "fur"), C([1.5, 12, -6.6], [1, 6, 1], "earglow"),
                                         C([1, 19, -6], [2, 1, 1], "plate")]),
        B("ear_r", "head", [-2, 11, -5], [C([-3, 11, -6], [2, 8, 1], "fur"), C([-2.5, 12, -6.6], [1, 6, 1], "earglow"),
                                          C([-3, 19, -6], [2, 1, 1], "plate")]),
        leg("leg_fl", "body", 1, 4, -3, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="fur"),
        leg("leg_fr", "body", -3, 4, -3, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="fur"),
        leg("leg_bl", "body", 2, 3, 1, 2, 3, 5, "fur", foot=(2, 1, 7), foot_skin="plate"),
        leg("leg_br", "body", -4, 3, 1, 2, 3, 5, "fur", foot=(2, 1, 7), foot_skin="plate"),
    ]
    skins = {"default": fur, "fur": fur, "furb": fur_b, "plate": plate, "nose": flat("#f08aa8"), "mouth": flat("#c86a88"),
             "visor": lit("#4af0ff"), "earglow": lit("#ff7ad8"), "tail": organic("#ffffff", "#e6e0f4", 8, 1.5, 0.05),
             "glowdot": lit("#4af0ff")}
    anims = {
        "walk": anim(merge(hop("body", 2.2), hop("head", 0.0), quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", 35, 60),
                           wave("ear_l", 8, 130, 2), wave("ear_r", -8, 130, 2))),
        "idle": anim(merge(bob("body", 0.15, 60), wave("ear_l", 8, 40, 2), wave("ear_r", -8, 40, 2, 2.0),
                           {"head": {"rotation": ["math.sin(query.life_time * 40) * 4", "math.sin(query.life_time * 20) * 12", "0"]}})),
    }
    return make("ed_cyber_bunny", "Cyber Bunny", ("#f6f2ff", "#4af0ff"), bones, skins, anims, [WALK, "idle"],
                {"role": "companion", "health": 10, "speed": 0.32, "box": [0.5, 0.8], "family": ["space_pet"],
                 "tame_items": ["minecraft:carrot", "minecraft:golden_carrot"], "sound": ("parrot", [1.5, 1.7]),
                 "spawn": {"biomes": ["plains", "forest", "taiga"], "weight": 6, "herd": [1, 3]},
                 "loot": [("minecraft:rabbit_foot", 0, 1), ("minecraft:redstone", 0, 2)]},
                scale=1.2, glow=True)


# ================================================================== MOON ROVER (mount)
def rover():
    def foil(p):
        n = N(p, 6, 1.1)
        c = mix("#b8892e", "#f4d878", n)
        c = shade(c, 0.85 + 0.35 * hash01(p.p[0] * 2, p.p[1] * 2, p.p[2] * 2, 4))
        if p.face == "top": c = shade(c, 1.1)
        if (p.x == 0 or p.y == 0) and p.fw >= 4: c = shade(c, 0.7)
        return c
    def solar(p):
        if p.face in ("top", "bottom"):
            if p.x % 3 == 0 or p.y % 3 == 0 or p.x == p.fw - 1 or p.y == p.fh - 1: return "#9aa6bc"
            return shade(mix("#1b2a5a", "#2c4a9a", N(p, 3, 1.5)), 1.0)
        return "#9aa6bc"
    def tread(p):
        if p.face in ("top", "bottom") and (p.x + p.y) % 2 == 0: return "#1c1c20"
        return "#2c2c32"
    hub = metal("#c8d0dc", "#5a6270", 62, False)
    def wheel(name, x, z):
        w = 2
        ox = x - 1 if x > 0 else x - 1
        return B(name, "body", [x, 4, z], [C([ox, 1, z - 2], [w, 6, 4], "tread"), C([ox, 2, z - 3], [w, 4, 6], "tread"),
                                           C([ox + (1 if x > 0 else 0), 3, z - 1], [1, 2, 2], "hub") if False else C([x + (0.5 if x > 0 else -1.5), 3, z - 1], [1, 2, 2], "hub")])
    wheels = [wheel(f"wheel_{s}{i}", 8 if s == "l" else -8, z) for i, z in enumerate([-8, 0, 8]) for s in ("l", "r")]
    bones = [
        B("body", None, [0, 6, 0], [
            C([-7, 5, -10], [14, 4, 20], "foil"), C([-6, 9, -4], [12, 1, 12], "deck"), C([-5, 5, -12], [10, 3, 2], "dark"),
            C([-4, 6, -12.6], [2, 2, 1], "lamp"), C([2, 6, -12.6], [2, 2, 1], "lamp"),
            C([-1, 10, -9], [2, 8, 2], "dark"), C([5, 10, 7], [1, 5, 1], "dark"), C([3, 15, 5], [5, 1, 5], "dish"),
            C([5, 16, 6], [1, 2, 1], "dark"),
            C([7, 9, -4], [6, 1, 10], "solar"), C([-13, 9, -4], [6, 1, 10], "solar"),
            C([-6, 10, 5], [12, 3, 4], "foil"), C([-6, 5, 8], [12, 1, 2], "dark")]),
        B("cam", "body", [0, 18, -8], [C([-3, 18, -10], [6, 4, 4], "dark"), C([-2, 19, -10.6], [4, 2, 1], "lens"),
                                      C([-4, 19, -9], [1, 2, 2], "hub"), C([3, 19, -9], [1, 2, 2], "hub")]),
    ] + wheels
    skins = {"default": foil, "foil": foil, "deck": metal("#c0c8d4", "#606878", 63), "dark": metal("#4a505c", "#222630", 64),
             "lamp": lit("#fff2a0"), "dish": metal("#f0f2f6", "#a0a8b8", 65, False), "solar": solar, "lens": lit("#5ac8ff"),
             "tread": tread, "hub": hub}
    spin = "query.modified_distance_moved * 200"
    ws = {n["name"]: {"rotation": [spin, "0", "0"]} for n in wheels}
    anims = {
        "walk": anim(merge(ws, wave("cam", 25, 70, 1), bob("body", 0.2, 200))),
        "idle": anim(merge(wave("cam", 35, 40, 1), wave("cam", 4, 60, 0))),
    }
    return make("ed_moon_rover", "Moon Rover Bot", ("#f4d878", "#4a505c"), bones, skins, anims, [WALK, "idle"],
                {"role": "mount", "health": 40, "speed": 0.28, "damage": 3, "box": [1.6, 1.1], "family": ["robot"],
                 "ride": {"seats": [[0, 0.9, 0.1]], "jump": 0.45}, "sound": ("iron", [1.2, 1.4]),
                 "spawn": {"biomes": ["desert", "mesa", "extreme_hills"], "weight": 3, "herd": [1, 1]},
                 "loot": [("minecraft:iron_ingot", 1, 3), ("minecraft:redstone", 1, 3), ("minecraft:gold_nugget", 0, 3)]},
                scale=1.4, glow=True)


# ================================================================== VACUUM BOT
def vacuum():
    body = metal("#dfe4ea", "#7a8494", 70, True)
    dark = metal("#3a3e48", "#181a20", 71, False)
    bones = [
        B("body", None, [0, 3, 0], [
            C([-7, 1, -5], [14, 4, 10], "body"), C([-5, 1, -7], [10, 4, 14], "body"),
            C([-5, 5, -5], [10, 1, 10], "top"), C([-4, 2, -8], [8, 2, 1], "bump"),
            C([-3, 3, -8], [2, 2, 1], "eye"), C([1, 3, -8], [2, 2, 1], "eye"), C([-1, 2, -8.6], [2, 1, 1], "mouth"),
            C([-7, 0, -1], [1, 1, 2], "dark"), C([6, 0, -1], [1, 1, 2], "dark")]),
        B("lidar", "body", [0, 6, 1], [C([-2, 6, -1], [4, 2, 4], "dark"), C([-1, 8, 0], [2, 1, 2], "led")]),
        B("brush_l", "body", [5, 1, -6], [C([3, 0, -6.5], [4, 1, 1], "bristle"), C([4.5, 0, -8], [1, 1, 4], "bristle")]),
        B("brush_r", "body", [-5, 1, -6], [C([-7, 0, -6.5], [4, 1, 1], "bristle"), C([-5.5, 0, -8], [1, 1, 4], "bristle")]),
    ]
    def top(p):
        c = body(p)
        if p.face == "top" and p.x in (1, p.fw - 2) and p.y in (1, p.fh - 2): return glow("#4aff8a")
        return c
    skins = {"default": body, "body": body, "top": top, "dark": dark, "bump": dark, "eye": lit("#4aff8a"), "mouth": lit("#4aff8a"),
             "led": lit("#ff4a4a"), "bristle": flat("#e8c040")}
    anims = {
        "walk": anim(merge(wave("lidar", 360, 400, 1), wave("brush_l", 360, 500, 1), wave("brush_r", -360, 500, 1),
                           {"body": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 80) * 3"]}})),
        "idle": anim(merge(wave("lidar", 360, 150, 1), wave("brush_l", 200, 120, 1), wave("brush_r", -200, 120, 1),
                           bob("body", 0.15, 60))),
    }
    return make("ed_vacuum_bot", "Vacuum Bot", ("#dfe4ea", "#4aff8a"), bones, skins, anims, [WALK, "idle"],
                {"role": "passive", "health": 12, "speed": 0.24, "box": [0.9, 0.5], "family": ["robot"],
                 "sound": ("iron", [1.8, 2.0]),
                 "spawn": {"biomes": ["plains", "desert"], "weight": 6, "herd": [1, 2]},
                 "loot": [("minecraft:iron_nugget", 1, 3), ("minecraft:redstone", 0, 2)]},
                scale=1.3, glow=True)


SPECS = [golem(), crab(), bunny(), rover(), vacuum()]
