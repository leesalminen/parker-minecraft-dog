"""Armoured biped trooper kit shared by the storm-trooper and clone-trooper specs.  Not a spec itself.
Model faces -Z, y up, ground y=0, 32 units (2 blocks) tall."""
import math
from lib import *


def armor(base, dark, seed, grime=0.0, accent=None):
    def fn(p):
        x, y, z = p.p
        c = mix(dark, base, 0.62 + 0.38 * noise3(x, y, z, seed, 5.0))
        c = shade(c, 0.95 + 0.1 * noise3(x, y, z, seed + 3, 1.3))
        if (x % 7.0) < 0.5 or (y % 7.0) < 0.5 or (z % 7.0) < 0.5:
            c = shade(c, 0.86)
        if p.face == "top":
            c = shade(c, 1.06)
        elif p.face == "bottom":
            c = shade(c, 0.8)
        if grime:
            g = noise3(x, y, z, seed + 11, 3.0) * 0.6 + (1 - min(1.0, y / 32.0)) * 0.5
            if g > 0.85 - grime * 0.35:
                c = mix(c, "#8a7a5a", min(0.7, grime))
        if hash01(x, y, z, seed + 7) > 0.975:
            c = shade(c, 0.78)
        return c
    return fn


def under(base="#1b1d20"):
    def fn(p):
        x, y, z = p.p
        return shade(mix(base, "#3a3f46", noise3(x, y, z, 91, 1.4)), 0.92 + 0.16 * noise3(x, y, z, 93, 0.7))
    return fn


def colour(base, dark=None, seed=101):
    dark = dark or shade(base, 0.6)
    def fn(p):
        x, y, z = p.p
        c = mix(dark, base, 0.5 + 0.5 * noise3(x, y, z, seed, 3.0))
        return shade(c, 0.93 + 0.14 * noise3(x, y, z, seed + 1, 1.0))
    return fn


def gunmetal(p):
    x, y, z = p.p
    c = mix("#1c1f23", "#4b525a", noise3(x, y, z, 111, 2.4))
    if (z % 6.0) < 0.6:
        c = shade(c, 0.7)
    return shade(c, 0.92 + 0.16 * noise3(x, y, z, 113, 0.9))


def lens(tint="#0b0d10"):
    def fn(p):
        x, y, z = p.p
        c = mix(tint, "#2a3038", noise3(x, y, z, 121, 1.2))
        return shade(c, 1.25) if hash01(p.x, p.y, 7) > 0.9 else c
    return fn


def helmet(style, base, dark, seed, accent=None, grime=0.0):
    body = armor(base, dark, seed, grime)
    blk = "#0d0f12"

    def fn(p):
        c = body(p)
        if p.face == "top" and accent and style in ("clone", "heavy", "commander"):
            if 3 <= p.x <= 4:
                return colour(accent)(p)
        if p.face in ("east", "west"):
            if 2 <= p.x <= 5 and 3 <= p.y <= 5:
                return shade(dark, 0.45)                          # ear plate
            if accent and style != "storm" and p.y == 2:
                return colour(accent)(p)
        if p.face == "front":
            x, y = p.x, p.y
            if style == "storm":
                if (y in (2, 3) and x in (1, 2, 5, 6)) or (y == 4 and x in (2, 5)):
                    return blk                                     # eye lenses
                if y == 5 and x in (3, 4):
                    return shade(dark, 0.5)                        # nose
                if y == 5 and x in (1, 6):
                    return blk                                     # cheek tears
                if y >= 6 and 2 <= x <= 5 and x != 3:
                    return blk if (x + y) % 2 == 0 or y == 7 else shade(dark, 0.6)   # mouth grille
                if y == 1:
                    return shade(dark, 0.7)
            elif style in ("clone", "heavy", "commander"):
                if (y in (2, 3) and 1 <= x <= 6):
                    return blk                                     # T visor bar
                if 4 <= y <= 6 and x in (3, 4):
                    return blk                                     # T visor stem
                if y == 1 and accent:
                    return colour(accent)(p)
                if y >= 5 and x in (1, 6):
                    return shade(dark, 0.6)
            elif style == "scout":
                if 2 <= y <= 4:
                    return blk if (x not in (3, 4) or y != 3) else shade(dark, 0.5)
                if y >= 6 and 3 <= x <= 4:
                    return blk
        return c
    return fn


def mir(c):
    m = {"o": [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]], "s": list(c["s"]), "skin": c.get("skin", "armor")}
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    if "inflate" in c:
        m["inflate"] = c["inflate"]
    return m


def build(cfg):
    """cfg: id,name,egg,style,base,dark,under,accent,grime,pauldron(side,colour)|None,kama colour|None,
    backpack,fin,rangefinder,scale,behavior"""
    st = cfg["style"]; acc = cfg.get("accent")
    a, ac = "armor", "accent"

    # legs (left, mirrored)
    foot = [{"o": [1, 0, -5], "s": [4, 2, 8], "skin": "armor"}]
    shin = [{"o": [1, 2, -2.5], "s": [4, 5, 5], "skin": "armor"}, {"o": [1.5, 6.5, -3], "s": [3, 2, 1], "skin": "under"}]
    thigh = [{"o": [0.5, 7, -2.5], "s": [4, 5, 5], "skin": "armor"}, {"o": [1, 7, -2.5], "s": [3, 1, 5], "skin": "under"}]
    # pelvis / torso
    pelvis = [{"o": [-4, 12, -2.5], "s": [8, 3, 5], "skin": "under"},
              {"o": [-4.5, 12, -3], "s": [9, 2, 6], "skin": "armor"},
              {"o": [-1.5, 11, -3.5], "s": [3, 3, 1], "skin": "armor"}]
    if cfg.get("kama"):
        pelvis.append({"o": [-4, 6, -3.5], "s": [8, 7, 1], "skin": "kama"})
        pelvis.append({"o": [-4, 6, 2.5], "s": [8, 6, 1], "skin": "kama"})
    torso = [{"o": [-4.5, 15, -2.5], "s": [9, 4, 5], "skin": "under"},               # abdomen
             {"o": [-4, 15, -3], "s": [8, 1, 6], "skin": "armor"}, {"o": [-4, 17, -3], "s": [8, 1, 6], "skin": "armor"},
             {"o": [-5, 19, -3], "s": [10, 6, 6], "skin": "armor"},                   # chest
             {"o": [-3, 20, -3.4], "s": [6, 3, 1], "skin": "armor"},
             {"o": [-1, 21, -3.8], "s": [2, 2, 1], "skin": "under"},
             {"o": [-4, 24, -2.5], "s": [8, 1, 5], "skin": "under"},
             {"o": [-4, 19, 3], "s": [8, 5, 2], "skin": "armor"}]                     # back plate
    if cfg.get("backpack"):
        torso.append({"o": [-3, 16, 5], "s": [6, 8, 3], "skin": "under"})
        torso.append({"o": [-2.5, 24, 5.5], "s": [5, 2, 2], "skin": "armor"})
    if cfg.get("pack_canteen"):
        torso.append({"o": [2, 15, 4.5], "s": [3, 5, 3], "skin": "under"})
    if acc:
        torso.append({"o": [-2, 21.5, -3.5], "s": [4, 1, 1], "skin": "accent"})
    neck = [{"o": [-1.5, 24, -1.5], "s": [3, 1, 3], "skin": "under"}]
    head = [{"o": [-4, 25, -4], "s": [8, 8, 8], "skin": "helmet"},
            {"o": [-4.2, 25.5, -4.2], "s": [1, 3, 4], "skin": "dark"} if False else {"o": [-4.5, 26, -1], "s": [1, 3, 3], "skin": "armor"},
            {"o": [3.5, 26, -1], "s": [1, 3, 3], "skin": "armor"},
            {"o": [-3, 24.5, -4.5], "s": [6, 2, 1], "skin": "armor"}]                # jaw
    if st in ("clone", "heavy", "commander"):
        head.append({"o": [-4, 30.5, -4.6], "s": [8, 1, 1], "skin": "armor"})
    if cfg.get("fin"):
        head.append({"o": [-0.5, 33, -3], "s": [1, 2, 7], "skin": "accent"})
    if cfg.get("rangefinder"):
        head.append({"o": [2.5, 32, -2], "s": [2, 4, 2], "skin": "under"})
    if st == "scout":
        head.append({"o": [-4.5, 25, -4.5], "s": [9, 9, 9], "skin": "helmet", "inflate": 0} if False else {"o": [-3, 33, -3], "s": [6, 1, 6], "skin": "armor"})

    # arms (left, mirrored)
    def arm_up(side_pauld):
        c = [{"o": [4.5, 18, -1.5], "s": [3, 5, 3], "skin": "armor"}]
        if side_pauld:
            col = side_pauld
            c.append({"o": [4, 23, -2.5], "s": [5, 3, 5], "skin": col})
            c.append({"o": [5.5, 21, -2.5], "s": [3, 3, 5], "skin": col})
        else:
            c.append({"o": [4, 23, -2.5], "s": [4, 2, 5], "skin": "armor"})
        return c
    pl = cfg.get("pauldron")          # (side "l"/"r"/"both", skin name)
    up_l = arm_up(pl[1] if pl and pl[0] in ("l", "both") else None)
    up_r_src = arm_up(pl[1] if pl and pl[0] in ("r", "both") else None)
    up_r = [mir(c) for c in up_r_src]
    lo_l = [{"o": [4.5, 13, -1.5], "s": [3, 5, 3], "skin": "under"}, {"o": [4, 14, -2], "s": [4, 4, 4], "skin": "armor"},
            {"o": [4.5, 10.5, -1.5], "s": [3, 3, 3], "skin": "under"}]
    if acc:
        lo_l.append({"o": [3.8, 16, -2.2], "s": [4, 1, 4], "skin": "accent"})
    lo_r = [mir(c) for c in lo_l]

    # blaster rifle, drawn around the right hand (-6, 11.5, 0) with the barrel along -Z
    hx, hy = -3.0, 13.0
    rifle = [{"o": [hx - 1, hy - 1, -5], "s": [2, 3, 12], "skin": "gun"},
             {"o": [hx - 0.5, hy, -16], "s": [1, 1, 11], "skin": "gun"},
             {"o": [hx - 1.5, hy - 1.5, -8], "s": [3, 4, 5], "skin": "gun"},
             {"o": [hx - 0.5, hy + 2, -12], "s": [1, 1, 6], "skin": "gun"},
             {"o": [hx - 1, hy - 5, -3], "s": [2, 4, 3], "skin": "gun"},
             {"o": [hx - 1, hy - 2, 5], "s": [2, 4, 5], "skin": "under"}]

    bones = [
        {"name": "pelvis", "parent": None, "pivot": [0, 12, 0], "cubes": pelvis},
        {"name": "torso", "parent": "pelvis", "pivot": [0, 15, 0], "cubes": torso},
        {"name": "neck", "parent": "torso", "pivot": [0, 24, 0], "cubes": neck},
        {"name": "head", "parent": "neck", "pivot": [0, 25, 0], "cubes": head},
        {"name": "arm_l_up", "parent": "torso", "pivot": [6, 23, 0], "rotation": [-42, 0, 26], "cubes": up_l},
        {"name": "arm_l_lo", "parent": "arm_l_up", "pivot": [6, 18, 0], "rotation": [-40, 0, 14], "cubes": lo_l},
        {"name": "arm_r_up", "parent": "torso", "pivot": [-6, 23, 0], "rotation": [-38, 0, -10], "cubes": up_r},
        {"name": "arm_r_lo", "parent": "arm_r_up", "pivot": [-6, 18, 0], "rotation": [-40, 0, -14], "cubes": lo_r},
        {"name": "rifle", "parent": "arm_r_lo", "pivot": [hx, hy, 0], "rotation": [75, 0, 0], "cubes": rifle},
        {"name": "thigh_l", "parent": "pelvis", "pivot": [2.5, 12, 0], "cubes": thigh},
        {"name": "shin_l", "parent": "thigh_l", "pivot": [2.5, 7, 0], "cubes": shin},
        {"name": "foot_l", "parent": "shin_l", "pivot": [2.5, 2, 0], "cubes": foot},
        {"name": "thigh_r", "parent": "pelvis", "pivot": [-2.5, 12, 0], "cubes": [mir(c) for c in thigh]},
        {"name": "shin_r", "parent": "thigh_r", "pivot": [-2.5, 7, 0], "cubes": [mir(c) for c in shin]},
        {"name": "foot_r", "parent": "shin_r", "pivot": [-2.5, 2, 0], "cubes": [mir(c) for c in foot]},
    ]

    W = "query.modified_distance_moved * 40"
    S = "query.modified_move_speed"
    anims = {
        "walk": anim(merge(
            biped_walk("thigh_l", "thigh_r", amp=38, freq=40),
            {"shin_l": {"rotation": [f"math.max(0, math.cos({W} + 180)) * 30 * {S}", "0", "0"]}},
            {"shin_r": {"rotation": [f"math.max(0, math.cos({W})) * 30 * {S}", "0", "0"]}},
            {"pelvis": {"position": ["0", f"math.abs(math.sin({W} / 2)) * 0.9 * {S}", "0"]}},
            {"torso": {"rotation": ["0", f"math.cos({W}) * 5 * {S}", "0"]}},
        )),
        "idle": anim(merge(
            sway("torso", amp=1.5, rate=28, axis=0),
            {"head": {"rotation": ["math.sin(query.life_time * 40) * 2", "math.sin(query.life_time * 22) * 14", "0"]}},
        )),
        "attack": anim(merge(
            {"arm_r_up": {"rotation": ["math.sin(variable.attack_time * 180) * -20", "0", "0"]}},
            {"rifle": {"position": ["0", "0", "math.sin(variable.attack_time * 180) * 2"]}},
            {"torso": {"rotation": ["math.sin(variable.attack_time * 180) * -3", "0", "0"]}},
        ), loop=False),
    }

    skins = {"default": armor(cfg["base"], cfg["dark"], 141, cfg.get("grime", 0), acc),
             "armor": armor(cfg["base"], cfg["dark"], 141, cfg.get("grime", 0), acc),
             "under": under(cfg["under"]), "gun": gunmetal, "dark": colour(shade(cfg["dark"], 0.5)),
             "helmet": helmet(st, cfg["base"], cfg["dark"], 141, acc, cfg.get("grime", 0))}
    if acc:
        skins["accent"] = colour(acc)
    if cfg.get("kama"):
        skins["kama"] = colour(cfg["kama"])
    if pl:
        skins[pl[1]] = colour(pl[2]) if len(pl) > 2 else colour(acc)
    b = dict(cfg["behavior"])
    return {"id": cfg["id"], "name": cfg["name"], "egg": cfg["egg"], "glow": False, "scale": cfg.get("scale", 1.0),
            "visible": [2.0, 2.6, 1.0], "bones": bones, "skins": skins, "anims": anims,
            "play": [{"walk": "query.modified_move_speed > 0.02"}, "idle", "attack"], "behavior": b}
