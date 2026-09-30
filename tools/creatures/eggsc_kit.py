"""Shared kit for the eggsc_* animal specs: painters, quadruped / biped / bird builders.
All units are 1/16 block. Model faces -Z, ground y=0. Cube sizes must be ints; origins may be fractional."""
import math
from lib import *


# ------------------------------------------------------------------ painting helpers
def voronoi(x, y, z, scale, seed=0):
    """Jittered-grid cellular noise -> (F1, F2, cell_id_hash) in units of `scale`."""
    x, y, z = x / scale, y / scale, z / scale
    xi, yi, zi = math.floor(x), math.floor(y), math.floor(z)
    best = [9.0, 9.0, 0.0]
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                cx, cy, cz = xi + dx, yi + dy, zi + dz
                px = cx + hash01(cx, cy, cz, seed + 1)
                py = cy + hash01(cx, cy, cz, seed + 2)
                pz = cz + hash01(cx, cy, cz, seed + 3)
                d = math.sqrt((px - x) ** 2 + (py - y) ** 2 + (pz - z) ** 2)
                if d < best[0]:
                    best[1] = best[0]; best[0] = d; best[2] = hash01(cx, cy, cz, seed + 4)
                elif d < best[1]:
                    best[1] = d
    return best


def fur_painter(base, dark=None, belly=None, belly_y=0.0, belly_soft=3.0, pattern=None, patt=None,
                fine=0.16, patch=0.10, seed=7, top=None, top_y=None):
    """Returns painter fn. pattern(p)->0..1 blends toward `patt` colour."""
    dark = dark or shade(base, 0.7)

    def fn(p):
        x, y, z = p.p
        c = mix(dark, base, 0.55 + 0.45 * noise3(x * 0.5, y * 0.5, z * 0.5, seed, 5.0))
        c = mix(c, base, 0.5)
        c = shade(c, 1 - fine + 2 * fine * noise3(x * 2.0, y * 2.0, z * 1.4, seed + 3, 1.0))
        c = shade(c, 1 - patch + 2 * patch * noise3(x, y, z, seed + 9, 4.0))
        if top is not None and top_y is not None and y > top_y:
            c = mix(c, top, 0.6)
        if pattern is not None:
            a = pattern(p)
            if a > 0:
                c = mix(c, patt, min(1.0, a))
        if belly is not None and not p.bone.startswith("leg") and not p.bone.startswith("arm"):
            t = max(0.0, min(1.0, (belly_y - y) / belly_soft + 0.5))
            if t > 0:
                c = mix(c, belly, t * 0.9)
        return c
    return fn


def flat(color, var=0.12, seed=11, scale=1.4):
    def fn(p):
        return shade(color, 1 - var + 2 * var * noise3(p.p[0], p.p[1], p.p[2], seed, scale))
    return fn


def eye_fn(iris="#1c1410", white=None, glint="#ffffff"):
    def fn(p):
        if p.x == 0 and p.y == 0 and p.fw > 1:
            return glint
        return iris
    return fn


def stripe_pat(axis=2, freq=1.0, width=0.5, wobble=1.5, seed=3, ymin=-999, soft=False):
    def pat(p):
        x, y, z = p.p
        if y < ymin:
            return 0
        v = (x, y, z)[axis]
        s = math.sin(v * freq + wobble * noise3(x, y, z, seed, 3.0) * 3)
        if soft:
            return max(0.0, (s - width) * 3)
        return 1.0 if s > width else 0.0
    return pat


def spot_pat(scale=4.0, r=0.32, seed=5, ymin=-999):
    def pat(p):
        x, y, z = p.p
        if y < ymin:
            return 0
        f1, f2, h = voronoi(x, y, z, scale, seed)
        return 1.0 if (f1 < r and h > 0.15) else 0.0
    return pat


def patch_pat(scale=7.0, line=0.16, seed=5):
    """Giraffe-ish: patches (returns 1) separated by light lines (returns 0)."""
    def pat(p):
        x, y, z = p.p
        f1, f2, h = voronoi(x, y, z, scale, seed)
        return 0.0 if (f2 - f1) < line else 1.0
    return pat


def std_skins(cfg, extra=None):
    """Standard skin dict from colours in cfg: base,dark,belly,muzzle,inner,foot,nose,eye,horn."""
    base = cfg["base"]
    fur = cfg.get("fur") or fur_painter(base, cfg.get("dark"), cfg.get("belly"), cfg.get("belly_y", 0),
                                        pattern=cfg.get("pattern"), patt=cfg.get("patt"),
                                        seed=cfg.get("seed", 7), top=cfg.get("top"), top_y=cfg.get("top_y"))
    sk = {
        "default": fur, "fur": fur,
        "muzzle": flat(cfg.get("muzzle", cfg.get("belly") or shade(base, 1.2)), 0.08, 21),
        "inner": flat(cfg.get("inner", "#e8a0a0"), 0.1, 22),
        "foot": flat(cfg.get("foot", shade(base, 0.55)), 0.12, 23),
        "hoof": flat(cfg.get("foot", "#2a2622"), 0.12, 23),
        "nose": flat(cfg.get("nose", "#1e1616"), 0.1, 24),
        "eye": eye_fn(cfg.get("eye", "#1c1410")),
        "horn": flat(cfg.get("horn", "#d9cfae"), 0.14, 25, 1.2),
        "dark": flat(cfg.get("dark") or shade(base, 0.6), 0.12, 26),
        "light": flat(cfg.get("belly") or shade(base, 1.3), 0.1, 27),
        "tip": flat(cfg.get("tip", shade(base, 0.5)), 0.12, 28),
        "claw": flat(cfg.get("claw", "#e8e2d0"), 0.08, 29),
        "mane": flat(cfg.get("mane", shade(base, 0.7)), 0.2, 30, 1.0),
    }
    if extra:
        sk.update(extra)
    return sk


# ------------------------------------------------------------------ geometry helpers
def mirror(c):
    m = dict(c)
    m["o"] = [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]]
    m["s"] = list(c["s"])
    if "rot" in c:
        m["rot"] = [c["rot"][0], -c["rot"][1], -c["rot"][2]]
        m["pivot"] = [-c["pivot"][0], c["pivot"][1], c["pivot"][2]]
    return m


def pair(cubes, c):
    cubes.append(c); cubes.append(mirror(c))


def mirror_bone(b, newname, newparent=None):
    nb = {"name": newname, "parent": newparent or b["parent"], "pivot": [-b["pivot"][0], b["pivot"][1], b["pivot"][2]],
          "cubes": [mirror(c) for c in b["cubes"]]}
    return nb


def cube(o, s, skin="fur", **kw):
    d = {"o": list(o), "s": [int(v) for v in s], "skin": skin}
    d.update(kw)
    return d


def auto_visible(bones):
    mx = my = 1.0
    for b in bones:
        for c in b.get("cubes", []):
            x0, y0, z0 = c["o"]; w, h, d = c["s"]
            mx = max(mx, abs(x0), abs(x0 + w), abs(z0), abs(z0 + d)); my = max(my, y0 + h, abs(y0))
    ext = mx * 1.35 + 4
    return [round(2 * ext / 16 + 0.6, 2), round(my * 1.3 / 16 + 0.8, 2), round((my * 1.3 / 16 + 0.8) / 2, 2)]


def walk_anims(legs, tail=None, ears=None, amp=30, freq=50, head_swing=3, extra_idle=None, body_bob=0.3,
               neck="head", attack=True, trunk=None):
    fl, fr, bl, br = legs
    walk_parts = [quad_walk(fl, fr, bl, br, amp=amp, freq=freq), bob("body", amp=body_bob, rate=freq * 3)]
    if tail:
        walk_parts.append(swing({t: (0 if i % 2 == 0 else 180) for i, t in enumerate(tail)}, amp=7, axis=1, freq=freq))
    if head_swing:
        walk_parts.append(swing({neck: 0}, amp=head_swing, axis=0, freq=freq))
    idle = [bob("body", amp=body_bob, rate=70),
            {neck: {"rotation": ["math.sin(query.life_time * 40) * 3", "math.sin(query.life_time * 21) * 14", "0"]}}]
    for i, t in enumerate(tail or []):
        idle.append(sway(t, amp=6 + 3 * i, rate=45 - 4 * i, axis=1, off=0.8 * i))
    for e, sgn in (ears or []):
        idle.append({e: {"rotation": ["0", "0", f"math.sin(query.life_time * 120 + {abs(sgn) * 1.7}) * 6 * {sgn}"]}})
    if extra_idle:
        idle.append(extra_idle)
    an = {"walk": anim(merge(*walk_parts)), "idle": anim(merge(*idle))}
    if attack:
        an["attack"] = anim(merge(
            {neck: {"rotation": ["math.sin(variable.attack_time * 180) * 24", "0", "0"]}},
            {fl: {"rotation": ["math.sin(variable.attack_time * 180) * -18", "0", "0"]}},
            {fr: {"rotation": ["math.sin(variable.attack_time * 180) * -18", "0", "0"]}}), loop=False)
    return an


# ------------------------------------------------------------------ quadruped builder
def quad(q):
    """q keys: bw,bh,bl (body), leg, lw, ld, foot (foot cube height), claws, spread (leg x inset)
    head: hw,hh,hd,  hy (bottom y), hz (back z of head cube)
    snout: (sw,sh,sl,drop) ; nosec=(w,h)  ; eyes: (size, xoff, yfrac, side)
    ear: dict(w,h,d,x,z,rot,inner,style) ; neck: (nw,nh,nd,y,z)  (vertical neck)
    tail: list of (w,h,l) ; tail_y ; tail_rot
    extra_body/extra_head/extra_neck: lists of cubes ; more_bones: list of bones appended
    """
    bw, bh, bl, leg = q["bw"], q["bh"], q["bl"], q["leg"]
    lw = q.get("lw", max(2, bw // 4)); ld = q.get("ld", lw)
    foot = q.get("foot", 0); spread = q.get("spread", 0.0)
    top = leg + bh
    body = [cube([-bw / 2, leg, -bl / 2], [bw, bh, bl])]
    if q.get("belly_lip"):
        body.append(cube([-bw / 2 + 1, leg - 1, -bl / 2 + 1], [bw - 2, 2, bl - 2], "light"))
    body += q.get("extra_body", [])
    bones = [{"name": "body", "parent": None, "pivot": [0, leg + bh / 2, 0], "cubes": body}]

    # legs
    lens = q.get("leg_z", (0.0, 0.0))
    for nm, sx, zf in (("leg_fl", 1, 0), ("leg_fr", -1, 0), ("leg_bl", 1, 1), ("leg_br", -1, 1)):
        x0 = (bw / 2 - lw - spread) if sx > 0 else (-bw / 2 + spread)
        z0 = (-bl / 2 + lens[0]) if zf == 0 else (bl / 2 - ld - lens[1])
        cs = [cube([x0, foot, z0], [lw, int(leg - foot), ld])]
        if foot:
            fw = lw + q.get("foot_w", 1)
            fx = x0 - (fw - lw) / 2
            cs.append(cube([fx, 0, z0 - q.get("foot_l", 2)], [fw, foot, ld + q.get("foot_l", 2)], "hoof" if q.get("hoof") else "foot"))
            for i in range(q.get("claws", 0)):
                cw = max(1, int(fw // q["claws"]))
                cs.append(cube([fx + i * fw / q["claws"], 0, z0 - q.get("foot_l", 2) - 1], [cw if cw > 0 else 1, 1, 1], "claw"))
        bones.append({"name": nm, "parent": "body", "pivot": [x0 + lw / 2, leg, z0 + ld / 2], "cubes": cs})

    # neck
    parent = "body"
    hw, hh, hd = q["head"]
    hy = q.get("hy", top - hh + 2); hz = q.get("hz", -bl / 2 + 2)
    if q.get("neck"):
        nw, nh, nd, ny, nz = q["neck"]
        ncubes = [cube([-nw / 2, ny, nz], [nw, nh, nd])] + q.get("extra_neck", [])
        bones.append({"name": "neck", "parent": "body", "pivot": [0, ny, nz + nd / 2], "cubes": ncubes,
                      **({"rotation": q["neck_rot"]} if q.get("neck_rot") else {})})
        parent = "neck"
    head = [cube([-hw / 2, hy, hz - hd], [hw, hh, hd])]
    if q.get("snout"):
        sw, sh, sl, sdrop = q["snout"]
        sz = hz - hd - sl + 1
        head.append(cube([-sw / 2, hy + (hh - sh) / 2 - sdrop, sz], [sw, sh, sl], q.get("snout_skin", "muzzle")))
        ns = q.get("nosec")
        nw2, nh2 = ns if ns else (max(2, sw - 1), max(1, sh // 2))
        if ns is not False:
            head.append(cube([-nw2 / 2, hy + (hh - sh) / 2 - sdrop + sh - nh2 + q.get("nose_dy", 0), sz - 1], [nw2, nh2, 1], "nose"))
    ecfg = q.get("eyes", (2, hw / 2 - 2.5, 0.6, False))
    if ecfg:
        es, ex, eyf, eside = ecfg
        ey = hy + hh * eyf - es / 2
        if eside:
            pair(head, cube([hw / 2 - 0.4, ey, hz - hd + q.get("eye_z", 2)], [1, es, es], "eye"))
        else:
            pair(head, cube([ex - es / 2, ey, hz - hd - 0.4], [es, es, 1], "eye"))
    head += q.get("extra_head", [])
    hp = [0, hy + hh * 0.3, hz - hd * 0.3]
    if q.get("head_pivot"):
        hp = q["head_pivot"]
    bones.append({"name": "head", "parent": parent, "pivot": hp, "cubes": head})

    # ears
    ears = []
    e = q.get("ear")
    if e:
        ew, eh, ed = e["w"], e["h"], e.get("d", 1)
        ex0 = e.get("x", hw / 2 - ew - 0.5)
        ez = hz - e.get("z", 2 + ed) if False else hz - e.get("z", ed + 2)
        ey0 = hy + hh - e.get("sink", 0)
        rz = e.get("rot", 12)
        for side, sgn in (("l", 1), ("r", -1)):
            ox = ex0 if sgn > 0 else -ex0 - ew
            pv = [(ex0 + ew / 2) * sgn, ey0, ez + ed / 2]
            cs = [cube([ox, ey0, ez], [ew, eh, ed], e.get("skin", "fur"), rot=[e.get("rx", 0), 0, -rz * sgn], pivot=pv)]
            if e.get("inner", True) and ew >= 3 and eh >= 3:
                cs.append(cube([ox + 1, ey0 + 1, ez - 0.4], [ew - 2, eh - 1, 1], "inner", rot=[e.get("rx", 0), 0, -rz * sgn], pivot=pv))
            if e.get("tip"):
                cs.append(cube([ox, ey0 + eh - e["tip"], ez], [ew, e["tip"], ed], "tip", rot=[e.get("rx", 0), 0, -rz * sgn], pivot=pv, inflate=0.05))
            bones.append({"name": f"ear_{side}", "parent": "head", "pivot": pv, "cubes": cs})
            ears.append((f"ear_{side}", sgn))

    # tail
    tails = []
    ty = q.get("tail_y", leg + bh * 0.8)
    z = bl / 2 - 1
    prev = "body"
    for i, (tw, th, tl) in enumerate(q.get("tail", [])):
        nm = f"tail{i}"
        pv = [0, ty + th / 2, z]
        cs = [cube([-tw / 2, ty, z], [tw, th, tl], "tip" if (q.get("tail_tip") and i == len(q["tail"]) - 1) else "fur")]
        b = {"name": nm, "parent": prev, "pivot": pv, "cubes": cs}
        if i == 0 and q.get("tail_rot"):
            b["rotation"] = [q["tail_rot"], 0, 0]
        bones.append(b)
        tails.append(nm); prev = nm; z += tl - 1
        ty = ty + (th - th) / 2
    bones += q.get("more_bones", [])
    return bones, ears, tails


def quad_spec(sid, name, egg, q, cfg, behavior, extra_skins=None, amp=28, freq=50, glow=False, extra_idle=None, attack=None,
              scale=1.0):
    bones, ears, tails = quad(q)
    anims = walk_anims(("leg_fl", "leg_fr", "leg_bl", "leg_br"), tails, ears, amp=amp, freq=freq,
                       neck="neck" if q.get("neck") else "head", extra_idle=extra_idle,
                       body_bob=q.get("bob", 0.3), attack=behavior.get("role") in ("neutral", "mount") if attack is None else attack,
                       head_swing=q.get("head_swing", 3))
    play = [{"walk": "query.modified_move_speed > 0.02"}, "idle"] + (["attack"] if "attack" in anims else [])
    return {"id": sid, "name": name, "egg": egg, "glow": glow, "scale": scale, "visible": auto_visible(bones),
            "bones": bones, "skins": std_skins(cfg, extra_skins), "anims": anims, "play": play, "behavior": behavior}


# ------------------------------------------------------------------ upright (biped) builder
def biped(q):
    """Upright mammal. q: tw,th,td (torso), leg (leg length), lw, ld, lean(deg), head=(hw,hh,hd), hy_off, snout,
    arm=(aw,al,ad,ay_off,spread), tail list, ear dict, foot=(fw,fh,fl), extra_body, extra_head."""
    tw, th, td, leg = q["tw"], q["th"], q["td"], q["leg"]
    lw = q.get("lw", max(2, tw // 3)); ld = q.get("ld", lw)
    foot = q.get("foot")
    body = [cube([-tw / 2, leg, -td / 2], [tw, th, td])] + q.get("extra_body", [])
    lean = q.get("lean", 0)
    bones = [{"name": "body", "parent": None, "pivot": [0, leg, 0], **({"rotation": [lean, 0, 0]} if lean else {}), "cubes": body}]
    # legs hang from root (not leaning)
    for nm, sx in (("leg_l", 1), ("leg_r", -1)):
        x0 = (tw / 2 - lw - q.get("lspread", 0)) if sx > 0 else (-tw / 2 + q.get("lspread", 0))
        cs = [cube([x0, foot[1] if foot else 0, -ld / 2], [lw, int(leg - (foot[1] if foot else 0) + q.get("leg_up", 0)), ld])]
        if foot:
            fw, fh, fl = foot
            cs.append(cube([x0 + lw / 2 - fw / 2, 0, -ld / 2 - fl + ld], [fw, fh, fl], "foot"))
            for i in range(q.get("claws", 0)):
                cs.append(cube([x0 + lw / 2 - fw / 2 + i * fw / q["claws"], 0, -ld / 2 + ld - fl - 1], [max(1, int(fw // q["claws"])), 1, 1], "claw"))
        bones.append({"name": nm, "parent": None, "pivot": [x0 + lw / 2, leg, 0], "cubes": cs})
    hw, hh, hd = q["head"]
    hy = leg + th + q.get("hy_off", -1)
    hz = -td / 2 + hd * q.get("hz_frac", 0.7)
    head = [cube([-hw / 2, hy, hz - hd], [hw, hh, hd])]
    if q.get("snout"):
        sw, sh, sl, sdrop = q["snout"]
        sz = hz - hd - sl + 1
        head.append(cube([-sw / 2, hy + (hh - sh) / 2 - sdrop, sz], [sw, sh, sl], "muzzle"))
        head.append(cube([-max(1, sw // 2) / 2 - 0.0, hy + (hh - sh) / 2 - sdrop + sh - 1, sz - 1], [max(1, sw // 2), 1, 1], "nose"))
    es = q.get("eye", 2)
    pair(head, cube([hw / 2 - es - 0.5 - q.get("eye_in", 0), hy + hh * q.get("eyef", 0.55) - es / 2, hz - hd - 0.4], [es, es, 1], "eye"))
    head += q.get("extra_head", [])
    bones.append({"name": "head", "parent": "body", "pivot": [0, hy + 1, hz - hd * 0.3], "cubes": head})
    ears = []
    e = q.get("ear")
    if e:
        ew, eh, ed = e["w"], e["h"], e.get("d", 1)
        ex0 = e.get("x", hw / 2 - ew - 0.5); ez = hz - e.get("z", ed + 2); ey0 = hy + hh - e.get("sink", 0)
        for side, sgn in (("l", 1), ("r", -1)):
            ox = ex0 if sgn > 0 else -ex0 - ew
            pv = [(ex0 + ew / 2) * sgn, ey0, ez + ed / 2]
            cs = [cube([ox, ey0, ez], [ew, eh, ed], "fur", rot=[0, 0, -e.get("rot", 10) * sgn], pivot=pv)]
            if ew >= 3 and eh >= 3:
                cs.append(cube([ox + 1, ey0 + 1, ez - 0.4], [ew - 2, eh - 1, 1], "inner", rot=[0, 0, -e.get("rot", 10) * sgn], pivot=pv))
            bones.append({"name": f"ear_{side}", "parent": "head", "pivot": pv, "cubes": cs})
            ears.append((f"ear_{side}", sgn))
    if q.get("arm"):
        aw, al, ad, ay, asp = q["arm"]
        for nm, sx in (("arm_l", 1), ("arm_r", -1)):
            x0 = (tw / 2 + asp) if sx > 0 else (-tw / 2 - asp - aw)
            top = leg + th - ay
            cs = [cube([x0, top - al, -ad / 2], [aw, int(al), ad])]
            if q.get("hand"):
                hw2, hh2, hl2 = q["hand"]
                cs.append(cube([x0 + aw / 2 - hw2 / 2, top - al - hh2 + 1, -hl2 / 2], [hw2, hh2, hl2], "foot"))
                for i in range(q.get("hclaws", 0)):
                    cs.append(cube([x0 + aw / 2 - hw2 / 2 + i * hw2 / q["hclaws"], top - al - hh2, -hl2 / 2 - 1], [max(1, int(hw2 // q["hclaws"])), 1, 1], "claw"))
            bones.append({"name": nm, "parent": "body", "pivot": [x0 + aw / 2, top, 0], "cubes": cs})
    tails = []
    z = td / 2 - 1; ty = q.get("tail_y", leg + 2); prev = "body"
    for i, (w, h, l) in enumerate(q.get("tail", [])):
        nm = f"tail{i}"
        b = {"name": nm, "parent": prev, "pivot": [0, ty + h / 2, z], "cubes": [cube([-w / 2, ty, z], [w, h, l], "tip" if (q.get("tail_tip") and i == len(q["tail"]) - 1) else "fur")]}
        if i == 0 and q.get("tail_rot"):
            b["rotation"] = [q["tail_rot"], 0, 0]
        bones.append(b); tails.append(nm); prev = nm; z += l - 1
        ty += q.get("tail_climb", 0)
    bones += q.get("more_bones", [])
    return bones, ears, tails


def biped_spec(sid, name, egg, q, cfg, behavior, extra_skins=None, amp=32, freq=50, arm_amp=None, hop=False):
    bones, ears, tails = biped(q)
    names = {b["name"] for b in bones}
    walk = [biped_walk("leg_l", "leg_r", amp=amp, freq=freq), bob("body", amp=0.4, rate=freq * 3)]
    if hop:
        walk = [swing({"leg_l": 0, "leg_r": 0}, amp=amp, axis=0, freq=freq),
                {"body": {"position": ["0", f"math.abs(math.sin(query.modified_distance_moved * {freq})) * 3 * query.modified_move_speed", "0"]}}]
    if "arm_l" in names:
        walk.append(swing({"arm_l": 180, "arm_r": 0}, amp=arm_amp or amp * 0.8, axis=0, freq=freq))
    if tails:
        walk.append(swing({t: (0 if i % 2 == 0 else 180) for i, t in enumerate(tails)}, amp=6, axis=1, freq=freq))
    idle = [bob("body", amp=0.3, rate=70),
            {"head": {"rotation": ["math.sin(query.life_time * 40) * 4", "math.sin(query.life_time * 23) * 16", "0"]}}]
    for i, t in enumerate(tails):
        idle.append(sway(t, amp=5 + 2 * i, rate=45 - 4 * i, axis=1, off=0.8 * i))
    for e, sgn in ears:
        idle.append({e: {"rotation": ["0", "0", f"math.sin(query.life_time * 120) * 6 * {sgn}"]}})
    if "arm_l" in names:
        idle.append(sway("arm_l", amp=4, rate=50, axis=0)); idle.append(sway("arm_r", amp=4, rate=50, axis=0, off=3.1))
    an = {"walk": anim(merge(*walk)), "idle": anim(merge(*idle))}
    if behavior.get("role") in ("neutral", "mount"):
        an["attack"] = anim(merge({"head": {"rotation": ["math.sin(variable.attack_time * 180) * 22", "0", "0"]}},
                                  *([{"arm_l": {"rotation": ["math.sin(variable.attack_time * 180) * -70", "0", "0"]}},
                                     {"arm_r": {"rotation": ["math.sin(variable.attack_time * 180) * -70", "0", "0"]}}] if "arm_l" in names else [])), loop=False)
    play = [{"walk": "query.modified_move_speed > 0.02"}, "idle"] + (["attack"] if "attack" in an else [])
    return {"id": sid, "name": name, "egg": egg, "glow": False, "scale": 1.0, "visible": auto_visible(bones),
            "bones": bones, "skins": std_skins(cfg, extra_skins), "anims": an, "play": play, "behavior": behavior}


def beh(role, hp, speed, box, family, spawn=None, loot=None, sound=("horse", [1, 1]), **kw):
    d = {"role": role, "health": hp, "speed": speed, "box": box, "family": family}
    if spawn:
        d["spawn"] = spawn
    if loot:
        d["loot"] = loot
    d["sound"] = sound
    d.update(kw)
    return d


def with_face(base_fn, over):
    """Wrap a fur painter: over(p, colour) -> colour."""
    return lambda p: over(p, base_fn(p))
