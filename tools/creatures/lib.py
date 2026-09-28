"""Creature framework: one Python spec -> geometry, texture, client entity, behavior entity,
animations, spawn rules, loot, sounds, lang.  See tools/creatures/README.md for the spec format."""
import json, math, random, struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BP = ROOT / "packs" / "GalaxyForge_BP"
RP = ROOT / "packs" / "GalaxyForge_RP"
NS = "gx"
GLOW = True          # glow texels get alpha 253 + entity_emissive_alpha material
GLOW_ALPHA = 253


# ---------------------------------------------------------------- colour helpers
def rgb(c):
    if isinstance(c, str):
        c = c.lstrip("#")
        return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)
    return tuple(c) + (255,) * (4 - len(c))

def shade(c, f):
    c = rgb(c); return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3],)

def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)

def glow(c):
    """Mark a colour as emissive (only effective when GLOW is on)."""
    c = rgb(c)
    return c[:3] + ((GLOW_ALPHA if GLOW else 255),)

def hash01(*v):
    h = 2166136261
    for x in v:
        h = ((h ^ (int(x * 1000) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return (h % 10007) / 10007.0

def noise3(x, y, z, seed=0, scale=1.0):
    """Cheap value noise 0..1, smooth-ish; continuous across cubes because it uses model-space coords."""
    x, y, z = x / scale, y / scale, z / scale
    xi, yi, zi = math.floor(x), math.floor(y), math.floor(z)
    fx, fy, fz = x - xi, y - yi, z - zi
    def s(t): return t * t * (3 - 2 * t)
    out = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (s(fx) if dx else 1 - s(fx)) * (s(fy) if dy else 1 - s(fy)) * (s(fz) if dz else 1 - s(fz))
                out += w * hash01(xi + dx, yi + dy, zi + dz, seed)
    return out


# ---------------------------------------------------------------- painting
class P:
    """Passed to skin painters. face in top/bottom/front/back/east/west (front = -Z, the way the creature looks).
    x,y = texel inside the face (0,0 = top-left as seen looking at the face). fw,fh = face size in texels.
    w,h,d = cube size. p = model-space centre of the texel (continuous across cubes: use it for stripes/noise)."""
    __slots__ = ("face", "x", "y", "fw", "fh", "w", "h", "d", "p", "rng", "cube", "bone")

def face_point(cube, face, s, t):
    (X0, Y0, Z0), (w, h, d) = cube["o"], cube["s"]
    X1, Y1, Z1 = X0 + w, Y0 + h, Z0 + d
    return {"front": (X1 - s, Y1 - t, Z0), "east": (X1, Y1 - t, Z1 - s), "west": (X0, Y1 - t, Z0 + s),
            "back": (X0 + s, Y1 - t, Z1), "top": (X1 - s, Y1, Z1 - t), "bottom": (X1 - s, Y0, Z0 + t)}[face]

def face_rects(cube):
    u, v = cube["uv"]; w, h, d = cube["s"]
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "east": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "west": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def pack_uvs(bones):
    cubes = [(b, c) for b in bones for c in b.get("cubes", [])]
    for _, c in cubes:
        assert all(isinstance(x, int) for x in c["s"]), f"cube sizes must be ints: {c}"
    cubes.sort(key=lambda bc: -(bc[1]["s"][2] + bc[1]["s"][1]))
    for size in (64, 128, 256, 512, 1024):
        x = y = rowh = 0; ok = True
        for _, c in cubes:
            w, h, d = c["s"]; cw, ch = 2 * (d + w), d + h
            if x + cw > size: x, y, rowh = 0, y + rowh, 0
            if cw > size or y + ch > size: ok = False; break
            c["uv"] = [x, y]; x += cw; rowh = max(rowh, ch)
        if ok: return size
    raise RuntimeError("texture too large")


def make_texture(spec, bones, size):
    px = [(0, 0, 0, 0)] * (size * size)
    skins = spec["skins"]; default = skins.get("default")
    for b in bones:
        for ci, c in enumerate(b.get("cubes", [])):
            fn = skins.get(c.get("skin", b["name"])) or skins.get(b["name"]) or default
            assert fn, f"no skin for {b['name']} (cube skin={c.get('skin')})"
            rng = random.Random(hash((spec["id"], b["name"], ci, tuple(c["o"]))) & 0xFFFFFFF)
            for face, (fx, fy, fw, fh) in face_rects(c).items():
                for y in range(fh):
                    for x in range(fw):
                        p = P(); p.face, p.x, p.y, p.fw, p.fh = face, x, y, fw, fh
                        p.w, p.h, p.d = c["s"]; p.cube, p.bone, p.rng = c, b["name"], rng
                        p.p = face_point(c, face, x + .5, y + .5)
                        col = fn(p)
                        if col is not None: px[(fy + y) * size + fx + x] = rgb(col)
    return px


def write_png(path, px, w, h):
    raw = b"".join(b"\x00" + b"".join(bytes(px[y * w + x]) for x in range(w)) for y in range(h))
    def chunk(tag, data):
        c = tag + data; return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- animation helpers (return {bone: {...}} dicts)
def swing(phases, amp=40.0, axis=0, freq=38.17, speed_scale=True):
    """Walk-cycle swing. phases: {bone: 0 or 180}. Rotation about `axis` (0=x)."""
    out = {}
    for bone, ph in phases.items():
        e = f"math.cos(query.modified_distance_moved * {freq} + {ph}) * {amp} * query.modified_move_speed"
        r = ["0", "0", "0"]; r[axis] = e
        out[bone] = {"rotation": r}
    return out

def quad_walk(fl, fr, bl, br, amp=40.0, freq=38.17):
    return swing({fl: 0, br: 0, fr: 180, bl: 180}, amp, 0, freq)

def biped_walk(l, r, amp=40.0, freq=38.17):
    return swing({l: 0, r: 180}, amp, 0, freq)

def hex_walk(legs, amp=25.0, freq=38.17):
    """legs: list of bone names in alternating-tripod order (0,2,4 vs 1,3,5)."""
    out = {}
    for i, name in enumerate(legs):
        ph = 0 if i % 2 == 0 else 180
        out[name] = {"rotation": ["0", f"math.cos(query.modified_distance_moved * {freq} + {ph}) * {amp} * query.modified_move_speed", "0"]}
    return out

def sway(bone, amp=8, rate=60, axis=1, off=0):
    r = ["0", "0", "0"]; r[axis] = f"math.sin(query.life_time * {rate} + {off}) * {amp}"
    return {bone: {"rotation": r}}

def bob(bone, amp=0.5, rate=90):
    return {bone: {"position": ["0", f"math.sin(query.life_time * {rate}) * {amp}", "0"]}}

def flap(bones_signs, amp=35, rate=300):
    """bones_signs: {wing_bone: +1/-1}. Rotates about Z."""
    return {b: {"rotation": ["0", "0", f"math.sin(query.life_time * {rate}) * {amp} * {s}"]} for b, s in bones_signs.items()}

def merge(*parts):
    out = {}
    for p in parts:
        for b, v in p.items(): out.setdefault(b, {}).update(v)
    return out

def anim(bones, loop=True, length=None):
    a = {"loop": loop, "bones": bones}
    if length: a["animation_length"] = length
    return a


# ---------------------------------------------------------------- behavior generation
SOUNDS = {
    "zombie": ("mob.zombie.say", "mob.zombie.hurt", "mob.zombie.death", "mob.zombie.step"),
    "golem": ("mob.irongolem.walk", "mob.irongolem.hit", "mob.irongolem.death", "mob.irongolem.walk"),
    "ravager": ("mob.ravager.ambient", "mob.ravager.hurt", "mob.ravager.death", "mob.ravager.step"),
    "wolf": ("mob.wolf.panting", "mob.wolf.hurt", "mob.wolf.death", "mob.wolf.step"),
    "cat": ("mob.cat.meow", "mob.cat.hitt", "mob.cat.hitt", "mob.cat.step"),
    "horse": ("mob.horse.idle", "mob.horse.hit", "mob.horse.death", "mob.horse.gallop"),
    "polarbear": ("mob.polarbear.idle", "mob.polarbear.hurt", "mob.polarbear.death", "mob.polarbear.step"),
    "spider": ("mob.spider.say", "mob.spider.say", "mob.spider.death", "mob.spider.step"),
    "phantom": ("mob.phantom.idle", "mob.phantom.hurt", "mob.phantom.death", "mob.phantom.flap"),
    "dragon": ("mob.enderdragon.growl", "mob.enderdragon.hit", "mob.enderdragon.death", "mob.enderdragon.flap"),
    "skeleton": ("mob.skeleton.say", "mob.skeleton.hurt", "mob.skeleton.death", "mob.skeleton.step"),
    "parrot": ("mob.parrot.idle", "mob.parrot.hurt", "mob.parrot.death", "mob.parrot.step"),
    "villager": ("mob.villager.idle", "mob.villager.hit", "mob.villager.death", "mob.villager.idle"),
    "bat": ("mob.bat.idle", "mob.bat.hurt", "mob.bat.death", "mob.bat.takeoff"),
    "vex": ("mob.vex.ambient", "mob.vex.hurt", "mob.vex.death", "mob.vex.ambient"),
    "iron": ("mob.irongolem.walk", "mob.irongolem.hit", "mob.irongolem.death", "mob.irongolem.walk"),
    "silverfish": ("mob.silverfish.say", "mob.silverfish.hit", "mob.silverfish.kill", "mob.silverfish.step"),
    "fox": ("mob.fox.ambient", "mob.fox.hurt", "mob.fox.death", "mob.fox.step"),
    "turtle": ("mob.turtle.ambient", "mob.turtle.hurt", "mob.turtle.death", "mob.turtle.step"),
}
DEFAULT_TARGETS = [{"filters": {"test": "is_family", "subject": "other", "value": "player"}, "max_dist": 32}]


def build_behavior(spec):
    b = spec["behavior"]; role = b.get("role", "hostile"); ident = f"{NS}:{spec['id']}"
    hp = b.get("health", 20); w, h = b.get("box", [0.8, 1.8])
    fam = [ident.replace(":", "_"), "gx_creature"] + b.get("family", [])
    fam += {"hostile": ["monster"], "boss": ["monster"], "neutral": ["mob"], "passive": ["mob"],
            "companion": ["mob"], "mount": ["mob"]}[role]
    c = {
        "minecraft:type_family": {"family": fam},
        "minecraft:health": {"value": hp, "max": hp},
        "minecraft:collision_box": {"width": w, "height": h},
        "minecraft:movement": {"value": b.get("speed", 0.25)},
        "minecraft:physics": {},
        "minecraft:pushable": {"is_pushable": True, "is_pushable_by_piston": True},
        "minecraft:nameable": {},
        "minecraft:breathable": {"total_supply": 15, "suffocate_time": 0},
        "minecraft:leashable": {},
        "minecraft:knockback_resistance": {"value": b.get("knockback_resist", 0.0)},
        "minecraft:follow_range": {"value": 32, "max": 64},
    }
    if b.get("fire_immune"): c["minecraft:fire_immune"] = {}
    if b.get("no_water_damage") is False: pass
    fly, hover = b.get("fly"), b.get("hover")
    if fly:
        c.update({"minecraft:navigation.fly": {"can_path_over_water": True, "can_pass_doors": True},
                  "minecraft:movement.fly": {} if False else {}, "minecraft:can_fly": {},
                  "minecraft:flying_speed": {"value": b.get("fly_speed", 0.15)}, "minecraft:jump.static": {}})
        c.pop("minecraft:movement.fly")
        c["minecraft:movement.basic"] = {}
    elif hover:
        c.update({"minecraft:navigation.hover": {"can_path_over_water": True, "can_pass_doors": True},
                  "minecraft:movement.hover": {}, "minecraft:can_fly": {}, "minecraft:flying_speed": {"value": b.get("fly_speed", 0.12)}})
    else:
        c.update({"minecraft:movement.basic": {}, "minecraft:jump.static": {},
                  "minecraft:behavior.float": {"priority": 0}})
        nav = {"can_path_over_water": True, "can_pass_doors": True, "avoid_damage_blocks": True}
        if b.get("climb"):
            c["minecraft:navigation.climb"] = nav; c["minecraft:can_climb"] = {}
        else:
            c["minecraft:navigation.walk"] = dict(nav, can_break_doors=bool(b.get("break_doors")))
    if b.get("step_height"): c["minecraft:jump.static"] = {"jump_power": b["step_height"]}

    stroll = {"priority": 8, "speed_multiplier": 0.8}
    hostile = role in ("hostile", "boss")
    if hostile or role in ("neutral", "mount"):
        c["minecraft:attack"] = {"damage": b.get("damage", 3)}
        c["minecraft:behavior.melee_attack"] = {"priority": 3, "speed_multiplier": 1.1, "track_target": True,
                                                "reach_multiplier": b.get("reach", 1.0)}
        c["minecraft:behavior.hurt_by_target"] = {"priority": 1}
    if b.get("ranged"):
        c["minecraft:shooter"] = {"def": b.get("projectile", "minecraft:arrow")}
        c["minecraft:behavior.ranged_attack"] = {"priority": 3, "attack_interval_min": 1.0, "attack_interval_max": 2.5,
                                                 "attack_radius": b.get("range", 16)}
        c.pop("minecraft:behavior.melee_attack", None)
        if "minecraft:attack" not in c: c["minecraft:attack"] = {"damage": b.get("damage", 3)}
        c.setdefault("minecraft:behavior.hurt_by_target", {"priority": 1})
    if hostile:
        c["minecraft:behavior.nearest_attackable_target"] = {
            "priority": 2, "must_see": not b.get("see_through_walls"), "reselect_targets": True,
            "entity_types": b.get("targets", DEFAULT_TARGETS)}
        c["minecraft:experience_reward"] = {"on_death": b.get("xp", 5)}
    if role == "mount" or b.get("ride"):
        r = b.get("ride", {"seats": [[0, h, 0]]})
        seats = [{"position": s, "min_rider_count": 0 if i == 0 else 1 + i - 1, "max_rider_count": 1, "lock_rider_rotation": 0}
                 for i, s in enumerate(r["seats"])]
        seats[0]["min_rider_count"] = 0
        for i, s in enumerate(seats): s["min_rider_count"] = 0 if i == 0 else i; s["max_rider_count"] = len(seats)
        c["minecraft:rideable"] = {"seat_count": len(seats), "family_types": ["player"],
                                   "interact_text": "action.interact.ride.horse", "seats": seats}
        c["minecraft:can_power_jump"] = {} if b.get("power_jump") else None
        if c["minecraft:can_power_jump"] is None: del c["minecraft:can_power_jump"]
        c["minecraft:input_air_controlled" if (fly or hover) else "minecraft:input_ground_controlled"] = {}
        if not (fly or hover): c["minecraft:horse.jump_strength"] = {"value": r.get("jump", 0.6)}
        c["minecraft:is_tamed"] = {}
        stroll["priority"] = 9
    if role == "passive" or role == "neutral" or role == "mount":
        c["minecraft:behavior.panic"] = {"priority": 1, "speed_multiplier": 1.4} if role == "passive" else None
        if c["minecraft:behavior.panic"] is None: del c["minecraft:behavior.panic"]
    if not fly and not hover:
        c["minecraft:behavior.random_stroll"] = stroll
    elif fly:
        c["minecraft:behavior.random_fly"] = {"priority": 8, "xz_dist": 10, "y_dist": 7, "y_offset": 0, "fly_speed": 1.0}
    else:
        c["minecraft:behavior.random_hover"] = {"priority": 8, "xz_dist": 8, "y_dist": 4, "y_offset": -1, "interval": 120, "hover_height": [1, 4]}
    c["minecraft:behavior.look_at_player"] = {"priority": 9, "look_distance": 8}
    c["minecraft:behavior.random_look_around"] = {"priority": 10}
    if b.get("loot"): c["minecraft:loot"] = {"table": f"loot_tables/entities/gx_{spec['id']}.json"}
    if role == "boss":
        c["minecraft:boss"] = {"hud_range": 60, "name": spec["name"], "should_darken_sky": False}
        c["minecraft:persistent"] = {}
    groups, events = {}, {"minecraft:entity_spawned": {}}
    if role == "companion":
        items = b.get("tame_items", ["minecraft:bone"])
        groups["gx:wild"] = {"minecraft:tameable": {"probability": 0.33, "tame_items": items, "tame_event": {"event": "gx:on_tame", "target": "self"}},
                             "minecraft:behavior.tempt": {"priority": 4, "speed_multiplier": 1.1, "items": items, "can_get_scared": False}}
        groups["gx:tame"] = {"minecraft:is_tamed": {}, "minecraft:persistent": {},
                             "minecraft:sittable": {}, "minecraft:behavior.stay_while_sitting": {"priority": 3},
                             "minecraft:behavior.follow_owner": {"priority": 5, "speed_multiplier": 1.15, "start_distance": 8, "stop_distance": 2},
                             "minecraft:health": {"value": int(hp * 1.5), "max": int(hp * 1.5)},
                             "minecraft:healable": {"items": [{"item": i, "heal_amount": 6} for i in items]}}
        events["minecraft:entity_spawned"] = {"add": {"component_groups": ["gx:wild"]}}
        events["gx:on_tame"] = {"remove": {"component_groups": ["gx:wild"]}, "add": {"component_groups": ["gx:tame"]}}
        if b.get("ride"): pass
    if b.get("sit_only_when_tamed") is None: pass
    ent = {"format_version": "1.21.0", "minecraft:entity": {
        "description": {"identifier": ident, "is_spawnable": True, "is_summonable": True, "is_experimental": False},
        "component_groups": groups, "components": c, "events": events}}
    return ent


def build_spawn_rules(spec):
    s = spec["behavior"].get("spawn")
    if not s: return None
    role = spec["behavior"].get("role", "hostile")
    cond = {"minecraft:spawns_on_surface": {}, "minecraft:weight": {"default": s.get("weight", 5)},
            "minecraft:herd": {"min_size": s.get("herd", [1, 1])[0], "max_size": s.get("herd", [1, 1])[1]},
            "minecraft:biome_filter": {"any_of": [{"test": "has_biome_tag", "value": t} for t in s.get("biomes", ["overworld"])]}}
    if role in ("hostile", "boss"):
        cond["minecraft:brightness_filter"] = {"min": 0, "max": 7, "adjust_for_weather": False}
        pop = "monster"
    else:
        cond["minecraft:brightness_filter"] = {"min": 7, "max": 15, "adjust_for_weather": False}
        pop = "animal"
    if s.get("blocks"): cond["minecraft:spawns_on_block_filter"] = s["blocks"]
    return {"format_version": "1.8.0", "minecraft:spawn_rules": {
        "description": {"identifier": f"{NS}:{spec['id']}", "population_control": s.get("population", pop)}, "conditions": [cond]}}


def build_loot(spec):
    d = spec["behavior"].get("loot")
    if not d: return None
    entries = [{"type": "item", "name": it, "weight": 1,
                "functions": [{"function": "set_count", "count": {"min": lo, "max": hi}}]} for it, lo, hi in d]
    return {"pools": [{"rolls": 1, "entries": entries}]}


# ---------------------------------------------------------------- emit
def emit(spec, size_hint=None):
    """Write every file for one creature. Returns texture size."""
    cid = spec["id"]; ident = f"{NS}:{cid}"; key = f"gx_{cid}"
    bones = json.loads(json.dumps(spec["bones"]))
    names = [b["name"] for b in bones]
    for b in bones:
        assert b.get("parent") in (None, *names[:names.index(b["name"])]), f"{cid}: parent of {b['name']} must precede it"
    size = pack_uvs(bones)
    px = make_texture(spec, bones, size)
    write_png(RP / f"textures/entity/{key}.png", px, size, size)

    out_bones = []
    for b in bones:
        ob = {"name": b["name"], "pivot": b.get("pivot", [0, 0, 0])}
        if b.get("parent"): ob["parent"] = b["parent"]
        if b.get("rotation"): ob["rotation"] = b["rotation"]
        cubes = []
        for c in b.get("cubes", []):
            oc = {"origin": c["o"], "size": c["s"], "uv": c["uv"]}
            for k_in, k_out in (("inflate", "inflate"), ("rot", "rotation"), ("pivot", "pivot")):
                if c.get(k_in) is not None: oc[k_out] = c[k_in]
            cubes.append(oc)
        if cubes: ob["cubes"] = cubes
        out_bones.append(ob)
    vb = spec.get("visible", [4, 4, 1.5])
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{"description": {
        "identifier": f"geometry.{key}", "texture_width": size, "texture_height": size,
        "visible_bounds_width": vb[0], "visible_bounds_height": vb[1], "visible_bounds_offset": [0, vb[2], 0]},
        "bones": out_bones}]}
    dump(RP / f"models/entity/{key}.geo.json", geo)

    anims = spec.get("anims", {})
    dump(RP / f"animations/{key}.animation.json", {"format_version": "1.8.0", "animations": {f"animation.{key}.{n}": a for n, a in anims.items()}})
    amap = {n: f"animation.{key}.{n}" for n in anims}
    play = list(spec.get("play", []))
    if spec.get("look", True) and "head" in names:
        amap["look"] = "animation.common.look_at_target"; play.insert(0, "look")
    materials = {"default": "entity_emissive_alpha" if (GLOW and spec.get("glow")) else "entity_alphatest"}
    dump(RP / f"entity/{key}.entity.json", {"format_version": "1.10.0", "minecraft:client_entity": {"description": {
        "identifier": ident, "materials": materials, "textures": {"default": f"textures/entity/{key}"},
        "geometry": {"default": f"geometry.{key}"}, "animations": amap,
        "scripts": {"scale": str(spec.get("scale", 1.0)), "animate": play},
        "render_controllers": [f"controller.render.{key}"],
        "spawn_egg": {"base_color": spec["egg"][0], "overlay_color": spec["egg"][1]}}}})
    dump(RP / f"render_controllers/{key}.render_controllers.json", {"format_version": "1.10.0", "render_controllers": {
        f"controller.render.{key}": {"geometry": "Geometry.default", "materials": [{"*": "Material.default"}], "textures": ["Texture.default"]}}})
    dump(BP / f"entities/{key}.json", build_behavior(spec))
    sr = build_spawn_rules(spec)
    if sr: dump(BP / f"spawn_rules/{key}.json", sr)
    lt = build_loot(spec)
    if lt: dump(BP / f"loot_tables/entities/{key}.json", lt)
    return size


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def sounds_and_lang(specs):
    ents = {}
    for s in specs:
        snd = s["behavior"].get("sound")
        if not snd: continue
        name, pitch = (snd if isinstance(snd, tuple) else (snd, [1.0, 1.0]))
        amb, hurt, death, step = SOUNDS[name]
        ents[f"{NS}:{s['id']}"] = {"volume": 0.9, "pitch": pitch, "events": {
            "ambient": amb, "hurt": hurt, "death": death, "step": {"sound": step, "volume": 0.3, "pitch": pitch[0]}}}
    dump(RP / "sounds.json", {"entity_sounds": {"entities": ents}})


# ---------------------------------------------------------------- shared registries (extras add to these)
LANG = {}          # full lang key -> value
ITEM_TEX = {}      # icon name -> texture path (no extension)
def lang(key, value): LANG[key] = value
