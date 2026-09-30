"""eggsd set A: UFO drone, grey alien, tentacle blob, slime-cube robot, space cat.  Model faces -Z, y up, ground y=0."""
from specs.eggsd_kit import *

WALK = {"walk": "query.modified_move_speed > 0.02"}


# ================================================================== UFO DRONE (hover, tiny)
def ufo():
    def dome(p):
        n = N(p, 4, 2.0)
        c = mix("#36b8c8", "#a8f4ff", 0.3 + 0.6 * n)
        if p.face == "top": c = shade(c, 1.15)
        return c
    def rim_lights(p): return lit("#ffd84a" if hash01(p.p[0], p.p[2], 1) > 0.5 else "#ff5a8a")(p)
    bones = [
        B("body", None, [0, 5, 0], [
            C([-4, 3, -4], [8, 1, 8], "hull_d"),
            C([-7, 4, -7], [14, 2, 14], "hull", inflate=0.0),
            C([-4, 6, -4], [8, 1, 8], "hull_d"),
            C([-2, 2, -2], [4, 1, 4], "beam"),
            C([-4, 1, -4], [1, 2, 1], "hull_d"), C([3, 1, -4], [1, 2, 1], "hull_d"),
            C([-4, 1, 3], [1, 2, 1], "hull_d"), C([3, 1, 3], [1, 2, 1], "hull_d"),
        ]),
        B("dome", "body", [0, 7, 0], [C([-3, 7, -3], [6, 4, 6], "dome"), C([-2, 11, -2], [4, 1, 4], "dome")]),
        B("eye", "dome", [0, 9, -3], [C([-1.5, 8, -3.6], [3, 3, 1], "eye")]),
        B("ring", "body", [0, 5, 0], [
            C([-1, 4.5, -7.6], [2, 1, 1], "rim"), C([-1, 4.5, 6.6], [2, 1, 1], "rim"),
            C([6.6, 4.5, -1], [1, 1, 2], "rim"), C([-7.6, 4.5, -1], [1, 1, 2], "rim"),
            C([4.6, 4.5, -5.6], [1, 1, 1], "rim"), C([-5.6, 4.5, -5.6], [1, 1, 1], "rim"),
            C([4.6, 4.5, 4.6], [1, 1, 1], "rim"), C([-5.6, 4.5, 4.6], [1, 1, 1], "rim")]),
        B("antenna", "body", [0, 7, 3], [C([-0.5, 7, 2.5], [1, 4, 1], "hull_d"), C([-1, 11, 2], [2, 2, 2], "beam")]),
    ]
    skins = {"default": metal("#aab6c4"), "hull": metal("#8d9bab", split=1), "hull_d": metal("#5b6674"),
             "dome": dome, "beam": lit("#7dffb0"), "rim": rim_lights,
             "eye": eyes("#ffffff", "#ff3b3b", "#ffe6e6", True)}
    anims = {
        "idle": anim(merge(bob("body", 0.9, 110), wave("ring", 360, 250, 1, 0),
                           {"body": {"rotation": ["math.sin(query.life_time * 70) * 4 + query.modified_move_speed * 60", "0",
                                                  "math.sin(query.life_time * 55) * 5"]}},
                           wave("antenna", 10, 160, 2))),
    }
    return make("ed_ufo_drone", "Mini UFO Drone", ("#8d9bab", "#7dffb0"), bones, skins, anims, ["idle"],
                {"role": "passive", "health": 6, "speed": 0.3, "hover": True, "fly_speed": 0.14, "box": [0.7, 0.6],
                 "family": ["alien"], "sound": ("vex", [1.7, 2.0]),
                 "spawn": {"biomes": ["overworld"], "weight": 4, "herd": [1, 2]},
                 "loot": [("minecraft:iron_nugget", 1, 3), ("minecraft:glowstone_dust", 0, 2)]},
                scale=1.2, glow=True)


# ================================================================== GREY ALIEN
def grey():
    def suit(p):
        c = metal("#41507f", "#252e50", 12)(p)
        if p.face == "front" and p.fw >= 4:
            if p.x == p.fw // 2: return glow("#59f0ff")
            if p.x in (p.fw - 2, ) and p.y in (2, 3): return glow("#a4ff59")
        return c
    def big_eye(p):
        if p.face == "front":
            if p.fw >= 3 and abs(p.x + .5 - p.fw / 2) < 0.6 and abs(p.y + .5 - p.fh / 2) < 0.6: return "#5c6a8a"
            return "#050608"
        return "#07080b"
    skin = organic("#9fb1a9", "#88998f", 8, 4.0, 0.05)
    bones = [
        B("body", None, [0, 8, 0], [C([-3, 8, -2], [6, 8, 4], "suit"), C([-3, 8, -2], [6, 1, 4], "belt", inflate=0.2)]),
        B("head", "body", [0, 16, 0], [
            C([-2, 16, -2], [4, 2, 4], "skin"),
            C([-5, 18, -4.5], [10, 7, 9], "skin"),
            C([-4, 25, -4], [8, 2, 8], "skin"),
            C([-3, 17, -4], [6, 2, 2], "skin"),
            C([1, 20, -5.2], [3, 3, 1], "eye"), C([-4, 20, -5.2], [3, 3, 1], "eye"),
            C([3, 19, -5.2], [2, 2, 1], "eye"), C([-5, 19, -5.2], [2, 2, 1], "eye"),
            C([-1.5, 18.2, -4.9], [3, 1, 1], "mouth"),
            C([-1, 19.3, -4.9], [1, 1, 1], "mouth"), C([0, 19.3, -4.9], [1, 1, 1], "mouth")]),
        B("arm_l", "body", [4, 15, 0], [C([3.5, 6, -0.5], [1, 10, 1], "skin"), C([3, 5, -1], [2, 2, 2], "skin"),
                                          C([3, 3.5, -1], [1, 2, 1], "skin"), C([4, 3.5, -1], [1, 2, 1], "skin")]),
        B("arm_r", "body", [-4, 15, 0], [C([-4.5, 6, -0.5], [1, 10, 1], "skin"), C([-5, 5, -1], [2, 2, 2], "skin"),
                                           C([-5, 3.5, -1], [1, 2, 1], "skin"), C([-4, 3.5, -1], [1, 2, 1], "skin")]),
        leg("leg_l", "body", 0.5, 8, -1, 2, 8, 2, "legsuit", foot=(3, 1, 4), foot_skin="belt"),
        leg("leg_r", "body", -2.5, 8, -1, 2, 8, 2, "legsuit", foot=(3, 1, 4), foot_skin="belt"),
    ]
    skins = {"default": skin, "skin": skin, "suit": suit, "legsuit": metal("#34406c", "#212a4a", 14),
             "belt": metal("#c6ccd6", None, 15), "eye": big_eye, "mouth": flat("#4a5850")}
    anims = {
        "walk": anim(merge(biped_walk("leg_l", "leg_r", 38), swing({"arm_l": 180, "arm_r": 0}, 28), bob("body", 0.3, 160))),
        "idle": anim(merge(bob("body", 0.3, 70),
                           {"head": {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 23) * 14",
                                                  "math.sin(query.life_time * 31) * 8"]}},
                           wave("arm_l", 6, 50, 2), wave("arm_r", -6, 50, 2, 1.0))),
    }
    return make("ed_grey_alien", "Little Grey Alien", ("#9fb1a9", "#41507f"), bones, skins, anims, [WALK, "idle"],
                {"role": "passive", "health": 14, "speed": 0.26, "box": [0.6, 1.5], "family": ["alien"],
                 "sound": ("villager", [1.4, 1.6]),
                 "spawn": {"biomes": ["plains", "desert"], "weight": 3, "herd": [1, 2]},
                 "loot": [("minecraft:glowstone_dust", 1, 3), ("minecraft:ender_pearl", 0, 1)]},
                scale=0.85, glow=True)


# ================================================================== TENTACLE BLOB
def blob():
    gel = rounded(organic("#8a52d6", "#5d33a6", 3, 3.5, 0.06, top=1.15))
    def tent(p):
        c = organic("#7a45c4", "#552d99", 5, 3, 0.06)(p)
        if p.face in ("front", "back", "east", "west") and p.x % 2 == 0 and p.y % 2 == 1 and p.fw >= 2: return "#f3b6e8"
        return c
    def slit(p):
        if p.face == "front":
            dx = abs(p.x + .5 - p.fw / 2)
            if dx < 0.8: return "#0b0614"
            if dx < 2.2: return glow("#b6ff4a")
            return "#f4f0ff"
        return "#d8d0f0"
    bones = [B("body", None, [0, 6, 0], [
        C([-6, 6, -6], [12, 3, 12], "gel"), C([-7, 9, -7], [14, 6, 14], "gel"),
        C([-5, 15, -5], [10, 3, 10], "gel"), C([-3, 18, -3], [6, 1, 6], "gel"),
        C([-3, 10, -8], [6, 5, 1], "eye"),
        C([-4, 16, -6], [2, 2, 1], "eye2"), C([2, 16, -6], [2, 2, 1], "eye2"),
        C([-2, 8, -7.5], [4, 1, 1], "mouth")])]
    ring = [(0, 5.5), (60, 5.5), (120, 5.5), (180, 5.5), (240, 5.5), (300, 5.5)]
    tnames = []
    for i, (a, r) in enumerate(ring):
        x, z = round(r * math.cos(math.radians(a)) * 1.0, 1), round(r * math.sin(math.radians(a)) * 1.0, 1)
        bones.append(B(f"t{i}", "body", [x, 6, z], [C([x - 1.5, 2, z - 1.5], [3, 4, 3], "tent")]))
        bones.append(B(f"t{i}b", f"t{i}", [x, 2, z], [C([x - 1, 0, z - 1], [2, 2, 2], "tent")]))
        tnames.append(f"t{i}")
    bones.append(B("arm_l", "body", [6, 12, -3], [C([6, 11, -8], [2, 2, 6], "tent")]))
    bones.append(B("arm_l2", "arm_l", [7, 12, -8], [C([6.5, 11.5, -12], [1, 1, 4], "tent")]))
    bones.append(B("arm_r", "body", [-6, 12, -3], [C([-8, 11, -8], [2, 2, 6], "tent")]))
    bones.append(B("arm_r2", "arm_r", [-7, 12, -8], [C([-7.5, 11.5, -12], [1, 1, 4], "tent")]))
    skins = {"default": gel, "gel": gel, "tent": tent, "eye": slit, "eye2": eyes("#ffffff", "#b6ff4a", "#0b0614", True),
             "mouth": flat("#3a1466")}
    walk = {}
    for i in range(6):
        ph = 0 if i % 2 == 0 else 180
        walk.update(swing({f"t{i}": ph}, 22, 0, 40))
    idle = merge(bob("body", 0.6, 60), wave("arm_l", 25, 80, 1), wave("arm_r", 25, 80, 1, 2.0),
                 wave("arm_l2", 30, 110, 1, 1), wave("arm_r2", 30, 110, 1, 3))
    for i in range(6):
        idle.update(wave(f"t{i}", 10, 60, 0, i))
        idle.update(wave(f"t{i}b", 18, 90, 0, i + 1))
    anims = {"walk": anim(merge(walk, bob("body", 0.8, 150), wave("arm_l", 30, 110, 1), wave("arm_r", 30, 110, 1, 2.0))),
             "idle": anim(idle)}
    return make("ed_tentacle_blob", "Tentacle Blob", ("#8a52d6", "#b6ff4a"), bones, skins, anims, [WALK, "idle"],
                {"role": "neutral", "health": 26, "speed": 0.2, "damage": 3, "box": [1.0, 1.3], "family": ["alien"],
                 "sound": ("silverfish", [0.5, 0.7]),
                 "spawn": {"biomes": ["swamp"], "weight": 6, "herd": [1, 2]},
                 "loot": [("minecraft:slime_ball", 1, 3)], "xp": 4},
                scale=1.3, glow=True)


# ================================================================== SLIME-CUBE ROBOT
def cubebot():
    frame = metal("#9aa7b6", "#4b5563", 20)
    def shell(p):
        if p.face == "bottom": return frame(p)
        b = 2
        if b <= p.x < p.fw - b and b <= p.y < p.fh - b: return None
        return frame(p)
    def core(p):
        n = N(p, 6, 2.0)
        c = mix("#3fd06a", "#a5ff7a", 0.25 + 0.7 * n)
        if hash01(p.p[0], p.p[1], p.p[2], 3) > 0.93: c = "#e6ffd0"
        return c
    bones = [
        B("body", None, [0, 9, 0], [C([-6, 3, -6], [12, 12, 12], "shell"), C([-4, 5, -4], [8, 8, 8], "core"),
                                  C([-3, 8, -4.6], [2, 3, 1], "eye"), C([1, 8, -4.6], [2, 3, 1], "eye"),
                                  C([-1, 6, -4.6], [2, 1, 1], "eye")]),
        B("gear", "body", [0, 13.5, 0], [C([-2, 13, -2], [4, 1, 4], "gear"), C([-3, 13, -1], [6, 1, 2], "gear"),
                                        C([-1, 13, -3], [2, 1, 6], "gear")]),
        B("feet", None, [0, 3, 0], [C([-5, 0, -5], [3, 3, 3], "foot"), C([2, 0, -5], [3, 3, 3], "foot"),
                                   C([-5, 0, 2], [3, 3, 3], "foot"), C([2, 0, 2], [3, 3, 3], "foot")]),
    ]
    skins = {"default": frame, "shell": shell, "core": core, "eye": flat("#0b3a1c"), "gear": lit("#ffd34a"),
             "foot": metal("#6b7686", "#333b46", 22)}
    anims = {
        "walk": anim(merge(hop("body", 2.0), hop("gear", 2.0), wave("gear", 200, 300, 1),
                           {"body": {"rotation": ["0", "0", "math.sin(query.modified_distance_moved * 60) * 6"]}})),
        "idle": anim(merge(bob("body", 0.5, 80), bob("gear", 0.5, 80), wave("gear", 90, 120, 1),
                           wave("body", 5, 40, 1))),
    }
    return make("ed_cube_bot", "Slime-Cube Bot", ("#9aa7b6", "#3fd06a"), bones, skins, anims, [WALK, "idle"],
                {"role": "neutral", "health": 20, "speed": 0.22, "damage": 2, "box": [0.9, 1.0], "family": ["robot"],
                 "sound": ("iron", [1.5, 1.8]),
                 "spawn": {"biomes": ["overworld"], "weight": 6, "herd": [1, 1]},
                 "loot": [("minecraft:slime_ball", 1, 2), ("minecraft:iron_nugget", 1, 3)]},
                scale=1.0, glow=True)


# ================================================================== SPACE CAT (companion)
def spacecat():
    fur = starry("#43307d", "#2c2058", "#fff2a0", 7, 0.05)
    fur_l = belly(fur, "#c9b8f0", 5.5, 2.0, 0.8)
    paw = organic("#f1eaff", "#d5c8f0", 3, 2.0, 0.04)
    bones = [
        B("body", None, [0, 6, 0], [C([-2.5, 4, -4], [5, 5, 9], "furb"), C([-2.5, 5, -3], [5, 1, 1], "collar", inflate=0.3)]),
        B("head", "body", [0, 7, -4.5], [
            C([-3, 6, -9], [6, 5, 5], "fur"), C([-1.5, 6, -10], [3, 2, 1], "muzzle"), C([-0.5, 7.4, -10.6], [1, 1, 1], "nose"),
            C([-3, 8, -9.5], [3, 2, 1], "eye"), C([0, 8, -9.5], [3, 2, 1], "eye"),
            C([-3, 11, -8], [2, 2, 2], "fur"), C([1, 11, -8], [2, 2, 2], "fur"),
            C([-2.5, 11, -8.5], [1, 1, 1], "ear_in"), C([1.5, 11, -8.5], [1, 1, 1], "ear_in"),
            C([-3, 4.5, -8.4], [6, 2, 3], "collar"), C([-1, 3, -8.8], [2, 2, 1], "tag")]),
        leg("leg_fl", "body", 0.5, 4, -4, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="paw"),
        leg("leg_fr", "body", -2.5, 4, -4, 2, 4, 2, "fur", foot=(2, 1, 3), foot_skin="paw"),
        leg("leg_bl", "body", 0.5, 4, 3, 2, 4, 3, "fur", foot=(2, 1, 4), foot_skin="paw"),
        leg("leg_br", "body", -2.5, 4, 3, 2, 4, 3, "fur", foot=(2, 1, 4), foot_skin="paw"),
        B("tail0", "body", [0, 7, 5], [C([-1, 6, 5], [2, 2, 3], "fur")]),
        B("tail1", "tail0", [0, 7, 8], [C([-1, 6, 8], [2, 4, 2], "fur")]),
        B("tail2", "tail1", [0, 10, 8], [C([-1, 10, 8], [2, 2, 2], "tail_tip")]),
    ]
    skins = {"default": fur, "fur": fur, "furb": fur_l, "paw": paw, "muzzle": paw, "nose": flat("#e88aa8"),
             "eye": slit_eyes("#ffe14a"), "ear_in": flat("#f0a8c8"),
             "collar": metal("#d24a6a", "#7a2036", 30, False), "tag": lit("#5cf0ff"), "tail_tip": lit("#7cf0ff")}
    anims = {
        "walk": anim(merge(quad_walk("leg_fl", "leg_fr", "leg_bl", "leg_br", 42, 55),
                           wave("tail0", 8, 80, 1), wave("tail1", 12, 80, 1, 1), bob("body", 0.3, 150))),
        "idle": anim(merge(bob("body", 0.2, 60), wave("tail0", 10, 40, 1), wave("tail1", 18, 40, 1, 1.0),
                           wave("tail2", 22, 40, 1, 2.0),
                           {"head": {"rotation": ["math.sin(query.life_time * 30) * 3", "math.sin(query.life_time * 21) * 12",
                                                  "math.sin(query.life_time * 17) * 5"]}})),
    }
    return make("ed_space_cat", "Space Cat", ("#43307d", "#fff2a0"), bones, skins, anims, [WALK, "idle"],
                {"role": "companion", "health": 12, "speed": 0.34, "box": [0.5, 0.7], "family": ["space_pet"],
                 "tame_items": ["minecraft:cod", "minecraft:salmon"], "sound": "cat",
                 "spawn": {"biomes": ["plains", "forest"], "weight": 5, "herd": [1, 2]},
                 "loot": [("minecraft:string", 0, 2), ("minecraft:glowstone_dust", 0, 1)]},
                scale=1.15, glow=True)


SPECS = [ufo(), grey(), blob(), cubebot(), spacecat()]
