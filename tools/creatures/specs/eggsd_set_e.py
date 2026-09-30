"""eggsd set E: toaster bot, lawnmower bot, cosmic whale (hover mount), moon frog, sputnik bird."""
from specs.eggsd_kit import *

WALK = {"walk": "query.modified_move_speed > 0.02"}


# ================================================================== TOASTER BOT
def toaster():
    chrome = metal("#d8dde6", "#7a8494", 80, True)
    def chrome_b(p):
        c = chrome(p)
        band = (p.p[1] * 0.9 + p.p[0] * 0.3) % 6
        if band < 1.0: c = shade(c, 1.12)
        return c
    def screen(p):
        if p.face == "front":
            if p.y == 1 and p.x in (1, 4): return glow("#59f0ff")
            if p.y == 3 and 1 <= p.x <= 4: return glow("#59f0ff")
            return "#0c1a24"
        return "#0c1a24"
    def topplate(p):
        if p.face == "top" and p.y in (2, 3) and 1 <= p.x <= p.fw - 2 and p.x != p.fw // 2: return "#101216"
        return chrome(p)
    toast = organic("#d9a04a", "#8a5a1c", 4, 1.5, 0.10)
    def toast_f(p):
        if p.face in ("front", "back") and 0 < p.x < p.fw - 1 and 0 < p.y < p.fh - 1: return "#f0d28a"
        return toast(p)
    arm_l = B("arm_l", "body", [5, 10, 0], [C([5, 6, -0.5], [1, 5, 1], "dark"), C([5, 4.5, -1], [2, 2, 2], "chrome")])
    bones = [
        B("body", None, [0, 8, 0], [C([-5, 4, -3], [10, 8, 6], "chrome"), C([-5, 12, -3], [10, 1, 6], "top"),
                                   C([-3, 6, -3.6], [6, 4, 1], "screen"), C([5, 7, -1], [1, 2, 2], "knob"),
                                   C([-6, 7, -1], [1, 2, 2], "knob"), C([-1, 4, 3], [2, 1, 1], "dark"),
                                   C([-0.5, 3.5, 4], [1, 1, 3], "dark")]),
        B("toast_l", "body", [-1.5, 12, 0], [C([-4, 12, -1], [3, 3, 1], "toast")]),
        B("toast_r", "body", [1.5, 12, 0], [C([1, 12, -1], [3, 3, 1], "toast")]),
        arm_l,
        B("arm_r", "body", [-5, 10, 0], [C([-6, 6, -0.5], [1, 5, 1], "dark"), C([-7, 4.5, -1], [2, 2, 2], "chrome")]),
        leg("leg_l", "body", 1.5, 4, -1, 2, 4, 2, "dark", foot=(3, 1, 4), foot_skin="dark"),
        leg("leg_r", "body", -3.5, 4, -1, 2, 4, 2, "dark", foot=(3, 1, 4), foot_skin="dark"),
    ]
    skins = {"default": chrome_b, "chrome": chrome_b, "top": topplate, "screen": screen, "toast": toast_f,
             "knob": metal("#e0342c", "#8a1a14", 81, False), "dark": metal("#33363e", "#16181c", 82, False)}
    pop_a = "math.max(0, math.sin(query.life_time * 90)) * 3.5"
    pop_b = "math.max(0, math.sin(query.life_time * 90 + 1.6)) * 3.5"
    anims = {
        "walk": anim(merge(biped_walk("leg_l", "leg_r", 42, 42), swing({"arm_l": 180, "arm_r": 0}, 35, 0, 42),
                           {"toast_l": {"position": ["0", pop_a, "0"]}, "toast_r": {"position": ["0", pop_b, "0"]}},
                           {"body": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 42) * 3"]}})),
        "idle": anim(merge({"toast_l": {"position": ["0", pop_a, "0"]}, "toast_r": {"position": ["0", pop_b, "0"]}},
                           bob("body", 0.3, 70), wave("arm_l", 6, 50, 2), wave("arm_r", -6, 50, 2, 1.0),
                           {"body": {"rotation": ["0", "math.sin(query.life_time * 20) * 8", "0"]}})),
    }
    return make("ed_toaster_bot", "Toaster Bot", ("#d8dde6", "#d9a04a"), bones, skins, anims, [WALK, "idle"],
                {"role": "passive", "health": 12, "speed": 0.25, "box": [0.7, 0.9], "family": ["robot"],
                 "sound": ("iron", [1.6, 1.9]),
                 "spawn": {"biomes": ["plains", "forest"], "weight": 5, "herd": [1, 1]},
                 "loot": [("minecraft:bread", 1, 2), ("minecraft:iron_nugget", 1, 3)]},
                scale=1.4, glow=True)


# ================================================================== LAWNMOWER BOT
def mower():
    deck = metal("#3aa84a", "#1c5a26", 90, True)
    engine = metal("#d8dde6", "#6a7484", 91, False)
    def vents(p):
        if p.face == "front" and p.y % 2 == 1 and 1 <= p.x < p.fw - 1: return "#181a20"
        return engine(p)
    dark = metal("#33363e", "#16181c", 92, False)
    def wheel(name, x, y, z, big):
        r = 6 if big else 4
        cy = r // 2
        ox = 6 if x > 0 else -8
        return B(name, "body", [x, cy, z], [C([ox, 0, z - r // 2], [2, r, r], "tire")])
    bones = [
        B("body", None, [0, 5, 0], [
            C([-6, 3, -8], [12, 4, 14], "deck"), C([-4, 7, 2], [8, 5, 6], "vents"), C([-4, 8, 1.5], [8, 1, 1], "dark"),
            C([2, 12, 5], [1, 4, 1], "dark"),
            C([-4, 4, -8.6], [3, 2, 1], "lamp"), C([1, 4, -8.6], [3, 2, 1], "lamp"), C([-4, 6, -8.6], [3, 1, 1], "dark"),
            C([1, 6, -8.6], [3, 1, 1], "dark"), C([-3, 3, -9], [6, 1, 1], "dark"),
            C([-4, 7, 8], [1, 9, 1], "dark"), C([3, 7, 8], [1, 9, 1], "dark"), C([-4, 16, 8], [8, 1, 1], "dark"),
            C([-6, 16, 8], [2, 1, 1], "grip"), C([4, 16, 8], [2, 1, 1], "grip")]),
        B("blade", "body", [0, 2, -3], [C([-5, 1, -4], [10, 1, 2], "blade"), C([-1, 1, -8], [2, 1, 10], "blade")]),
        wheel("wheel_fl", 7, 0, -5, False), wheel("wheel_fr", -7, 0, -5, False),
        wheel("wheel_rl", 7, 0, 5, True), wheel("wheel_rr", -7, 0, 5, True),
    ]
    # tires cubes: fix sizes/origins so the wheels sit on the ground
    skins = {"default": deck, "deck": deck, "vents": vents, "dark": dark, "lamp": lit("#fff2a0"), "tire": metal("#26262c", "#101014", 93, False),
             "blade": metal("#e0e4ea", "#8a92a0", 94, False), "grip": flat("#e0342c")}
    spin = "query.modified_distance_moved * 220"
    wl = {"wheel_fl": {"rotation": [spin, "0", "0"]}, "wheel_fr": {"rotation": [spin, "0", "0"]},
          "wheel_rl": {"rotation": [spin, "0", "0"]}, "wheel_rr": {"rotation": [spin, "0", "0"]}}
    anims = {
        "walk": anim(merge(wl, wave("blade", 360, 600, 1), {"body": {"position": ["0", "math.sin(query.life_time * 900) * 0.25", "0"]}})),
        "idle": anim(merge(wave("blade", 360, 300, 1), {"body": {"position": ["0", "math.sin(query.life_time * 700) * 0.2", "0"]}})),
    }
    return make("ed_mower_bot", "Lawnmower Bot", ("#3aa84a", "#d8dde6"), bones, skins, anims, [WALK, "idle"],
                {"role": "neutral", "health": 26, "speed": 0.3, "damage": 4, "box": [1.0, 1.2], "family": ["robot"],
                 "sound": ("iron", [1.0, 1.2]),
                 "spawn": {"biomes": ["plains", "forest"], "weight": 4, "herd": [1, 1]},
                 "loot": [("minecraft:iron_ingot", 0, 2), ("minecraft:redstone", 1, 2)], "xp": 3},
                scale=1.2, glow=True)


# ================================================================== COSMIC WHALE (hover mount, big)
def whale():
    sk = starry("#2a3a8a", "#1c2666", "#e8f4ff", 12, 0.04)
    skin = belly(sk, "#c8d8ff", 15, 4.0, 0.9)
    def eye_side(p):
        if p.face in ("east", "west"):
            cx, cy = p.fw / 2, p.fh / 2
            dx, dy = abs(p.x + .5 - cx), abs(p.y + .5 - cy)
            if dx < 1.0 and dy < 1.0: return "#05060c"
            return "#ffffff"
        return "#ffffff"
    def mouth(p):
        if p.face == "front" and p.y == p.fh - 1: return "#0c1030"
        return skin(p)
    def fluke(p):
        c = skin(p)
        return glow("#6ad8ff") if (p.face in ("top",) and p.y == 0) else c
    bones = [
        B("body", None, [0, 18, 0], [
            C([-9, 10, -14], [18, 16, 28], "skin"), C([-8, 11, -22], [16, 13, 8], "skin"),
            C([-7, 9, -22], [14, 3, 10], "jaw"), C([-10, 17, -18], [1, 4, 4], "eye"), C([9, 17, -18], [1, 4, 4], "eye"),
            C([-1, 24, -18], [2, 1, 2], "spout"), C([-1, 26, 2], [2, 3, 8], "skin"),
            C([-9.6, 22, -8], [1, 2, 2], "star"), C([8.6, 22, -6], [1, 2, 2], "star")]),
        B("tail0", "body", [0, 16, 14], [C([-6, 11, 14], [12, 12, 8], "skin")]),
        B("tail1", "tail0", [0, 16, 22], [C([-4, 12, 22], [8, 9, 8], "skin")]),
        B("tail2", "tail1", [0, 16, 30], [C([-2, 13, 30], [4, 6, 6], "skin")]),
        B("fluke_l", "tail2", [1, 15, 34], [C([1, 14, 34], [9, 2, 7], "fluke")]),
        B("fluke_r", "tail2", [-1, 15, 34], [C([-10, 14, 34], [9, 2, 7], "fluke")]),
        B("fin_l", "body", [9, 12, -8], [C([9, 11, -9], [9, 2, 6], "skin")]),
        B("fin_r", "body", [-9, 12, -8], [C([-18, 11, -9], [9, 2, 6], "skin")]),
    ]
    skins = {"default": skin, "skin": skin, "jaw": mouth, "eye": eye_side, "spout": lit("#6ad8ff"), "star": lit("#e8f4ff"),
             "fluke": fluke}
    ph = "query.life_time * 40"
    anims = {
        "idle": anim(merge(bob("body", 1.2, 35),
                           {"tail0": {"rotation": [f"math.sin({ph}) * (5 + query.modified_move_speed * 40)", "0", "0"]},
                            "tail1": {"rotation": [f"math.sin({ph} - 0.8) * (8 + query.modified_move_speed * 50)", "0", "0"]},
                            "tail2": {"rotation": [f"math.sin({ph} - 1.6) * (10 + query.modified_move_speed * 60)", "0", "0"]},
                            "fluke_l": {"rotation": [f"math.sin({ph} - 2.4) * 10", "0", "0"]},
                            "fluke_r": {"rotation": [f"math.sin({ph} - 2.4) * 10", "0", "0"]}},
                           wave("fin_l", 14, 40, 2), wave("fin_r", -14, 40, 2))),
    }
    return make("ed_cosmic_whale", "Cosmic Whale", ("#2a3a8a", "#e8f4ff"), bones, skins, anims, ["idle"],
                {"role": "passive", "health": 70, "speed": 0.2, "hover": True, "fly_speed": 0.18, "box": [2.2, 2.2],
                 "family": ["alien"], "knockback_resist": 0.6, "sound": ("dragon", [0.4, 0.5]),
                 "ride": {"seats": [[0, 2.0, -0.6], [0, 2.0, 0.7]]},
                 "spawn": {"biomes": ["overworld"], "weight": 1, "herd": [1, 1]},
                 "loot": [("minecraft:glowstone_dust", 3, 8), ("minecraft:ender_pearl", 0, 1)]},
                scale=1.25, glow=True)


# ================================================================== MOON FROG
def frog():
    skin = organic("#4fc0aa", "#3a8898", 5, 2.5, 0.07)
    def frog_skin(p):
        if N(p, 21, 1.5) > 0.80: return glow(mix("#9affc8", "#e4ffb0", N(p, 22, 1.0)))
        c = skin(p)
        if p.p[1] < 4.5: c = mix(c, "#e8f4d0", 0.7)
        return c
    def throat(p): return mix("#f0b0c8", "#e8f4d0", N(p, 5, 1.5))
    def eyeb(p):
        if p.face == "front":
            if 0 < p.x < p.fw - 1 and 0 < p.y < p.fh - 1:
                return "#0a0a14" if (p.x == 1 and p.y == 1) else "#f4e060"
            return skin(p)
        return skin(p)
    bones = [
        B("body", None, [0, 5, 0], [C([-4, 3, -4], [8, 5, 9], "skin"), C([-3, 8, -2], [6, 1, 5], "skin")]),
        B("head", "body", [0, 6, -4], [
            C([-4, 6, -9], [8, 4, 6], "skin"), C([-4, 10, -8], [3, 3, 3], "eyeb"), C([1, 10, -8], [3, 3, 3], "eyeb"),
            C([-3, 7, -9.5], [6, 1, 1], "mouth"), C([-0.5, 10, -5], [1, 3, 1], "stalk")]),
        B("bulb", "head", [0, 13, -5], [C([-1, 13, -5.5], [2, 2, 2], "bulb")]),
        B("throat", "body", [0, 5, -6], [C([-2, 5, -8], [4, 2, 4], "throat")]),
        B("leg_bl", "body", [5.5, 7, 3], [C([4, 3, 0], [3, 4, 6], "skin"), C([4, 0, -2], [3, 1, 8], "skin")]),
        B("leg_br", "body", [-5.5, 7, 3], [C([-7, 3, 0], [3, 4, 6], "skin"), C([-7, 0, -2], [3, 1, 8], "skin")]),
        leg("leg_fl", "body", 3, 5, -4, 2, 5, 2, "skin", foot=(3, 1, 4), foot_skin="skin"),
        leg("leg_fr", "body", -5, 5, -4, 2, 5, 2, "skin", foot=(3, 1, 4), foot_skin="skin"),
    ]
    skins = {"default": frog_skin, "skin": frog_skin, "eyeb": eyeb, "mouth": flat("#12303a"), "throat": throat,
             "stalk": flat("#2a6a7a"), "bulb": lit("#fff08a")}
    anims = {
        "walk": anim(merge(hop("body", 3.0), quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", 45, 70), wave("bulb", 10, 120, 0))),
        "idle": anim(merge(bob("body", 0.15, 50),
                           {"throat": {"position": ["0", "math.sin(query.life_time * 90) * 0.4", "0"]}},
                           wave("bulb", 14, 60, 0), wave("bulb", 8, 45, 2),
                           {"head": {"rotation": ["math.sin(query.life_time * 20) * 3", "math.sin(query.life_time * 14) * 10", "0"]}})),
    }
    return make("ed_moon_frog", "Moon Frog", ("#4fc0aa", "#9affc8"), bones, skins, anims, [WALK, "idle"],
                {"role": "passive", "health": 8, "speed": 0.26, "box": [0.7, 0.6], "family": ["alien"],
                 "sound": ("turtle", [1.4, 1.7]),
                 "spawn": {"biomes": ["swamp", "jungle"], "weight": 8, "herd": [2, 4]},
                 "loot": [("minecraft:slime_ball", 0, 1), ("minecraft:glowstone_dust", 0, 1)]},
                scale=1.25, glow=True)


# ================================================================== SPUTNIK BIRD (flyer)
def sputnik():
    sph = rounded(metal("#c8d0dc", "#6a7484", 100, True))
    solar = None
    def sol(p):
        if p.face in ("top", "bottom"):
            if p.x % 3 == 0 or p.y % 3 == 0: return "#9aa6bc"
            return mix("#1b2a5a", "#2c4a9a", N(p, 3, 1.5))
        return "#9aa6bc"
    bones = [
        B("body", None, [0, 8, 0], [
            C([-3, 5, -3], [6, 6, 6], "sph"), C([-2, 10, -6], [4, 4, 4], "sph"), C([-1, 10, -8], [2, 1, 2], "beak"),
            C([-1, 9, -7.5], [2, 1, 1], "beak"),
            C([-2, 11, -6.6], [1, 1, 1], "eye"), C([1, 11, -6.6], [1, 1, 1], "eye"),
            C([-2, 3, -1], [1, 3, 1], "beak"), C([1, 3, -1], [1, 3, 1], "beak"),
            C([-2.5, 3, -2], [2, 1, 2], "beak"), C([0.5, 3, -2], [2, 1, 2], "beak"),
            C([-2, 6, 3], [4, 1, 5], "sol")]),
        B("wing_l", "body", [3, 9, 0], [C([3, 9, -3], [9, 1, 6], "sol"), C([3, 9, -4], [3, 1, 1], "sph")]),
        B("wing_r", "body", [-3, 9, 0], [C([-12, 9, -3], [9, 1, 6], "sol"), C([-6, 9, -4], [3, 1, 1], "sph")]),
        B("whip_a", "body", [2, 10, 3], [C([1.5, 10, 3], [1, 1, 9], "whip")]),
        B("whip_b", "body", [-2, 10, 3], [C([-2.5, 10, 3], [1, 1, 9], "whip")]),
        B("whip_c", "body", [2, 8, 3], [C([1.5, 8, 3], [1, 1, 8], "whip")]),
        B("whip_d", "body", [-2, 8, 3], [C([-2.5, 8, 3], [1, 1, 8], "whip")]),
    ]
    skins = {"default": sph, "sph": sph, "whip": flat("#4a5060"), "sol": sol, "beak": flat("#f08a1c"), "eye": lit("#59f0ff")}
    anims = {
        "idle": anim(merge(bob("body", 0.8, 100),
                           {"wing_l": {"rotation": ["0", "0", "math.sin(query.life_time * 420) * -38"]},
                            "wing_r": {"rotation": ["0", "0", "math.sin(query.life_time * 420) * 38"]}},
                           wave("whip_a", 6, 140, 1), wave("whip_b", -6, 140, 1, 1), wave("whip_c", 8, 120, 1, 2), wave("whip_d", -8, 120, 1, 3),
                           {"body": {"rotation": ["math.sin(query.life_time * 60) * 5 + query.modified_move_speed * 60", "0", "0"]}})),
    }
    return make("ed_sputnik_bird", "Sputnik Bird", ("#c8d0dc", "#f08a1c"), bones, skins, anims, ["idle"],
                {"role": "passive", "health": 6, "speed": 0.2, "fly": True, "fly_speed": 0.16, "box": [0.5, 0.6],
                 "family": ["robot"], "sound": ("parrot", [1.3, 1.5]),
                 "spawn": {"biomes": ["overworld"], "weight": 5, "herd": [1, 3]},
                 "loot": [("minecraft:iron_nugget", 1, 2), ("minecraft:copper_ingot", 0, 1)]},
                scale=1.3, glow=True)


SPECS = [toaster(), mower(), whale(), frog(), sputnik()]
