"""Galaxy Forge military item pack: 6 lightsabers, 5 grenades, 2 camo armor sets.

Owns the `extras` item framework.  build_all.py imports this module and calls run().
Uses lib.dump / lib.lang / lib.ITEM_TEX and lib.write_png to emit BP/RP files.
"""
import math
import lib
from lib import BP, RP, dump, lang, write_png, noise3, hash01, rgb, shade

NS = "gx"
ITEMS = BP / "items"
RECIPES = BP / "recipes"
ENTITIES = BP / "entities"
ATTACH = RP / "attachables"
TEX_ITEMS = RP / "textures/items"
TEX_ARMOR = RP / "textures/models/armor"


# ---------------------------------------------------------------- icons
class Icon:
    def __init__(self, w=16, h=16):
        self.w, self.h = w, h
        self.px = [(0, 0, 0, 0)] * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = rgb(c)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, c)

    def disc(self, cx, cy, r, c):
        for y in range(self.h):
            for x in range(self.w):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, c)

    def line(self, x0, y0, x1, y1, w, c):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(steps + 1):
            t = i / steps
            x = round(x0 + (x1 - x0) * t)
            y = round(y0 + (y1 - y0) * t)
            for dy in range(-w, w + 1):
                for dx in range(-w, w + 1):
                    self.set(x + dx, y + dy, c)

    def save(self, path):
        write_png(path, self.px, self.w, self.h)


# ---------------------------------------------------------------- camo palettes
JUNGLE = ["#2f3a22", "#4a5a34", "#6b7a44", "#8a7a52"]
SAND = ["#6f5a3a", "#a08a5c", "#d8c89a", "#8f7c55"]


def camo(x, y, pal, seed):
    t = noise3(x, y, 0, seed, 3.0) * 0.6 + noise3(x, y, 0, seed + 7, 1.2) * 0.4
    idx = 0 if t < 0.34 else 1 if t < 0.55 else 2 if t < 0.74 else 3
    c = rgb(pal[idx])
    if hash01(x, y, seed) > 0.9:
        c = shade(c, 0.72)
    return c


# ---------------------------------------------------------------- armor model texture masks
# Alpha masks of vanilla iron armor textures (64x32): only opaque texels are drawn, so the
# camo keeps the exact vanilla armor silhouette (face opening, arm holes, etc.).
MASK1 = ["000000000000ff00", "000000000000ff00", "000000000000ff00", "000000000000ff00",
         "000000000000ff00", "000000000000ff00", "000000000000ff00", "000000000000ff00",
         "00000000ffffffff", "00000000ffffffff", "00000000ffffffff", "00000000ffff99ff",
         "00000000fff0180f", "00000000ff000000", "000000003c000000", "0000000000000000",
         "0000f00000000f00", "0000f00000000f00", "0000f00000000f00", "0000f00000000f00",
         "00ffffc3fc3f0000", "00fffffffe7f0000", "00ffffffffff0000", "00c03fffffff0000",
         "00c03fffffff0000", "000000ffffff0000", "000000ffffffffff", "000000ffffffffff",
         "000000ffffffffff", "0000007e07e0ffff", "0000000003c0ffff", "000000000000ffff"]
MASK2 = ["0000000000000000"] * 16 + [
         "00000000000000f0", "00000000000000f0", "00000000000000f0", "00000000000000f0",
         "000000000000ffff", "000000000000ffff", "000000000000ffff", "000000000000ffff",
         "000000000000ffff", "000000000000ffff", "000000000000ffff", "000000ffffffffff",
         "000000ffffffffff", "000000ffffff0000", "000000ffffff0000", "000000ffffff0000"]


def paint_armor_texture(path, mask, pal, seed):
    px = [(0, 0, 0, 0)] * (64 * 32)
    for y, row in enumerate(mask):
        bits = int(row, 16)
        for x in range(64):
            if (bits >> x) & 1:
                px[y * 64 + x] = camo(x, y, pal, seed)
    write_png(path, px, 64, 32)


# ---------------------------------------------------------------- emitters
def write_item(ident, icon, components, category="equipment", group=None):
    desc = {"identifier": ident, "menu_category": {"category": category}}
    if group:
        desc["menu_category"]["group"] = group
    dump(ITEMS / (ident.split(":")[1] + ".json"),
         {"format_version": "1.21.0", "minecraft:item": {"description": desc, "components": components}})


def write_icon(key, painter):
    lib.ITEM_TEX[key] = f"textures/items/{key}"
    painter(TEX_ITEMS / f"{key}.png")


def shaped(ident, pattern, key, count=1):
    dump(RECIPES / (ident.split(":")[1] + ".json"), {"format_version": "1.20.10", "minecraft:recipe_shaped": {
        "description": {"identifier": ident}, "tags": ["crafting_table"], "pattern": pattern,
        "key": {k: {"item": v} for k, v in key.items()},
        "result": {"item": ident, "count": count}}})


def shapeless(ident, ingredients, count=1):
    dump(RECIPES / (ident.split(":")[1] + ".json"), {"format_version": "1.20.10", "minecraft:recipe_shapeless": {
        "description": {"identifier": ident}, "tags": ["crafting_table"],
        "ingredients": [{"item": i} for i in ingredients],
        "result": {"item": ident, "count": count}}})


# ---------------------------------------------------------------- lightsabers
SABERS = [
    ("azure",   "Azure Lightsaber",   "#2f7bff", "#bfe0ff", "minecraft:lapis_lazuli", 12),
    ("crimson", "Crimson Lightsaber", "#ff2b2b", "#ffc9c9", "minecraft:redstone", 14),
    ("jade",    "Jade Lightsaber",    "#2bff6a", "#d0ffdc", "minecraft:emerald", 13),
    ("amber",   "Amber Lightsaber",   "#ffb02b", "#ffeec2", "minecraft:gold_ingot", 13),
    ("violet",  "Violet Lightsaber",  "#a02bff", "#e6c9ff", "minecraft:amethyst_shard", 14),
    ("storm",   "Storm Lightsaber",   "#f2f6ff", "#38e6ff", "minecraft:nether_star", 16),
]


def saber_icon(blade, core):
    def paint(path):
        ic = Icon()
        ic.line(4, 12, 13, 3, 2, shade(blade, 0.45))   # outer glow
        ic.line(4, 12, 13, 3, 1, blade)                # blade
        ic.line(4, 12, 13, 3, 0, core)                 # core
        ic.rect(2, 12, 6, 15, "#3a4046")               # emitter / hilt
        ic.rect(3, 13, 5, 14, "#141821")               # grip
        ic.set(3, 15, "#9aa2a9")                       # pommel
        ic.set(2, 12, "#7c848c")
        ic.save(path)
    return paint


def do_sabers():
    for name, disp, blade, core, mat, dmg in SABERS:
        ident = f"{NS}:saber_{name}"
        key = f"gx_saber_{name}"
        write_icon(key, saber_icon(blade, core))
        write_item(ident, key, {
            "minecraft:icon": key,
            "minecraft:max_stack_size": 1,
            "minecraft:damage": dmg,
            "minecraft:durability": {"max_durability": 2031},
            "minecraft:hand_equipped": True,
            "minecraft:enchantable": {"slot": "sword", "value": 16},
            "minecraft:glint": True,
            "minecraft:can_destroy_in_creative": False,
            "minecraft:repairable": {"repair_items": [
                {"items": ["minecraft:iron_ingot"], "repair_amount": "q.max_durability * 0.25"}]},
            "minecraft:tags": {"tags": ["minecraft:is_sword"]},
        }, group="minecraft:itemGroup.name.sword")
        lang(f"item.{ident}", disp)
        shaped(ident, ["  B", " B ", "HI"], {"B": mat, "H": "minecraft:iron_ingot", "I": "minecraft:stick"})


# ---------------------------------------------------------------- grenades
GRENADES = [
    ("frag",      "Frag Grenade",      "#5c6a44", "#d8b24a", "#5a6068"),
    ("smoke",     "Smoke Grenade",     "#7c848c", "#6f7078", "#5a6068"),
    ("flashbang", "Flashbang",         "#d8d2c4", "#ffd24a", "#5a6068"),
    ("incendiary", "Incendiary Grenade", "#a8461e", "#ff7a1f", "#5a6068"),
    ("emp",       "EMP Grenade",       "#2f3a5a", "#8fd8ff", "#5a6068"),
]


def grenade_icon(body, band, accent):
    def paint(path):
        ic = Icon()
        ic.disc(8, 9, 5, body)
        ic.rect(4, 7, 12, 9, band)
        ic.rect(6, 3, 9, 5, accent)
        ic.rect(4, 4, 7, 4, accent)
        ic.set(6, 6, shade(body, 1.3))
        ic.set(7, 6, shade(body, 1.22))
        ic.set(5, 11, shade(body, 0.7))
        ic.save(path)
    return paint


GRENADE_ITEMS = {
    "frag":      ("minecraft:gunpowder", "minecraft:iron_ingot", "minecraft:flint"),
    "smoke":     ("minecraft:gunpowder", "minecraft:sugar", "minecraft:charcoal"),
    "flashbang": ("minecraft:gunpowder", "minecraft:glowstone_dust", "minecraft:sugar"),
    "incendiary": ("minecraft:gunpowder", "minecraft:blaze_powder", "minecraft:coal"),
    "emp":       ("minecraft:gunpowder", "minecraft:redstone", "minecraft:copper_ingot"),
}

PROJ_GEOM = "geometry.gx_grenade_proj"
PROJ_RC = "controller.render.gx_grenade_proj"


def write_proj_assets():
    """Shared geometry + render controller + one client entity/texture per grenade so the
    thrown projectile is actually visible in game."""
    dump(RP / "models/entity/gx_grenade_proj.geo.json", {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": PROJ_GEOM, "texture_width": 16, "texture_height": 16,
                        "visible_bounds_width": 1.0, "visible_bounds_height": 1.0,
                        "visible_bounds_offset": [0, 0, 0]},
        "bones": [{"name": "body", "pivot": [0, 0, 0], "cubes": [
            {"origin": [-2, -2, -2], "size": [4, 4, 4], "uv": [0, 0]}]}]}]})
    dump(RP / "render_controllers/gx_grenade_proj.render_controllers.json", {"format_version": "1.10.0",
         "render_controllers": {PROJ_RC: {"geometry": "Geometry.default",
                                          "materials": [{"*": "Material.default"}],
                                          "textures": ["Texture.default"]}}})
    for name, disp, body, band, accent in GRENADES:
        ident = f"{NS}:grenade_{name}_proj"
        dump(RP / f"entity/gx_grenade_{name}_proj.entity.json", {"format_version": "1.10.0",
             "minecraft:client_entity": {"description": {
                 "identifier": ident,
                 "materials": {"default": "entity_emissive_alpha"},
                 "textures": {"default": f"textures/entity/gx_grenade_{name}_proj"},
                 "geometry": {"default": PROJ_GEOM},
                 "render_controllers": [PROJ_RC]}}})
        write_png(RP / f"textures/entity/gx_grenade_{name}_proj.png",
                  grenade_proj_pixels(body, band), 16, 16)


def grenade_proj_pixels(body, band):
    ic = Icon()
    ic.rect(4, 0, 7, 3, shade(body, 1.2))    # top face
    ic.rect(8, 0, 11, 3, shade(body, 0.65))  # bottom face
    for u in (0, 4, 8, 12):                  # side faces
        for y in range(4):
            for x in range(4):
                if y in (1, 2):
                    ic.set(u + x, 4 + y, lib.glow(band))
                else:
                    c = shade(body, 0.85 + 0.3 * noise3(x, y, u, 5, 2.0))
                    ic.set(u + x, 4 + y, c)
    return ic.px



def projectile_entity(name, commands, dmg=(4, 6), knockback=True, power=1.3, gravity=0.05):
    ident = f"{NS}:grenade_{name}_proj"
    events = {f"{NS}:detonate": {"run_command": {"command": list(commands)}}}
    on_hit = {"impact_damage": {"damage": {"min": dmg[0], "max": dmg[1]}, "knockback": knockback,
                                "catch_fire": False},
              "remove_on_hit": {},
              "definition_event": {"affect_projectile": True,
                                   "event_trigger": {"event": f"{NS}:detonate", "target": "self"}}}
    ent = {"format_version": "1.16.0", "minecraft:entity": {
        "description": {"identifier": ident, "is_spawnable": False, "is_summonable": True,
                        "is_experimental": False, "runtime_identifier": "minecraft:snowball"},
        "components": {
            "minecraft:type_family": {"family": ["projectile", "grenade"]},
            "minecraft:collision_box": {"width": 0.25, "height": 0.25},
            "minecraft:physics": {},
            "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
            "minecraft:conditional_bandwidth_optimization": {},
            "minecraft:projectile": {"power": power, "gravity": gravity, "angle_offset": -5,
                                     "hit_sound": "land.stone", "on_hit": on_hit},
        },
        "events": events}}
    dump(ENTITIES / f"gx_grenade_{name}_proj.json", ent)


def charge_entity(name, power, fire=False, fuse=0):
    ident = f"{NS}:{name}_charge"
    ent = {"format_version": "1.16.0", "minecraft:entity": {
        "description": {"identifier": ident, "is_spawnable": False, "is_summonable": True,
                        "is_experimental": False},
        "components": {
            "minecraft:type_family": {"family": ["grenade"]},
            "minecraft:collision_box": {"width": 0.2, "height": 0.2},
            "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
            "minecraft:conditional_bandwidth_optimization": {},
            "minecraft:explode": {"fuse_lit": True, "fuse_length": fuse, "power": power,
                                  "causes_fire": fire, "breaks_blocks": False,
                                  "fire_affected_by_griefing": False,
                                  "destroy_affected_by_griefing": False},
        },
        "events": {}}}
    dump(ENTITIES / f"gx_{name}_charge.json", ent)


def do_grenades():
    write_proj_assets()
    for name, disp, body, band, accent in GRENADES:
        ident = f"{NS}:grenade_{name}"
        key = f"gx_grenade_{name}"
        write_icon(key, grenade_icon(body, band, accent))
        write_item(ident, key, {
            "minecraft:icon": key,
            "minecraft:max_stack_size": 16,
            "minecraft:throwable": {"do_swing_animation": True, "launch_power_scale": 1.2,
                                    "max_launch_power": 1.2, "min_draw_duration": 0.0,
                                    "max_draw_duration": 0.0, "scale_power_by_draw_duration": False},
            "minecraft:projectile": {"projectile_entity": f"{NS}:grenade_{name}_proj"},
            "minecraft:cooldown": {"category": f"grenade_{name}", "duration": 0.8},
        })
        lang(f"item.{ident}", disp)
        shapeless(ident, list(GRENADE_ITEMS[name]))

    # frag -> live charge entity with a real explosion
    projectile_entity("frag", [f"particle minecraft:huge_explosion_emitter ~~~",
                               "playsound random.explode @a ~~~",
                               f"summon {NS}:frag_charge ~~~"], (5, 8))
    charge_entity("frag", 3.5)
    # incendiary -> fire charge
    projectile_entity("incendiary", [f"particle minecraft:basic_flame_particle ~~~",
                                     "playsound mob.blaze.burn @a ~~~",
                                     f"summon {NS}:fire_charge ~~~"], (3, 5))
    charge_entity("fire", 2.5, fire=True)
    # smoke / flashbang / EMP -> area effects
    projectile_entity("smoke", ["particle minecraft:basic_smoke_particle ~~~",
                                "playsound random.fizz @a ~~~",
                                "effect @a[r=6] blindness 8 0"], (0, 1), knockback=False)
    projectile_entity("flashbang", ["particle minecraft:huge_explosion_emitter ~~~",
                                    "playsound random.explode @a ~~~",
                                    "effect @a[r=8] blindness 6 0",
                                    "effect @a[r=8] nausea 10 0"], (0, 1), knockback=False)
    projectile_entity("emp", ["particle minecraft:electric_spark_particle ~~~",
                              "playsound random.fizz @a ~~~",
                              "effect @e[family=mech,r=10] slowness 8 1",
                              "effect @e[family=mech,r=10] weakness 8 1",
                              "effect @e[family=droid,r=10] slowness 8 1",
                              "effect @e[family=droid,r=10] weakness 8 1"], (2, 3))


# ---------------------------------------------------------------- camo armor
PIECES = [
    ("helmet", "Helmet", "minecraft:itemGroup.name.helmet", "slot.armor.head", "armor_head", 3,
     "geometry.humanoid.armor.helmet", "geometry.humanoid.baby.armor.helmet",
     "v.helmet_layer_visible = false;", 165, 1),
    ("chestplate", "Chestplate", "minecraft:itemGroup.name.chestplate", "slot.armor.chest", "armor_torso", 8,
     "geometry.humanoid.armor.chestplate", "geometry.humanoid.baby.armor.chestplate",
     "v.chest_layer_visible = false;", 240, 1),
    ("leggings", "Leggings", "minecraft:itemGroup.name.leggings", "slot.armor.legs", "armor_legs", 6,
     "geometry.humanoid.armor.leggings", "geometry.humanoid.baby.armor.leggings",
     "v.leg_layer_visible = false;", 225, 2),
    ("boots", "Boots", "minecraft:itemGroup.name.boots", "slot.armor.feet", "armor_feet", 3,
     "geometry.humanoid.armor.boots", "geometry.humanoid.baby.armor.boots",
     "v.boot_layer_visible = false;", 195, 1),
]

ARMOR_ICON_MASKS = {
    "helmet": [
        "................", "................", ".....######.....", "....########....",
        "...##########...", "...##########...", "...##########...", "...##########...",
        "...##########...", "..############..", "..############..", "................",
        "................", "................", "................", "................"],
    "chestplate": [
        "................", "................", "..####....####..", "..####....####..",
        "...##########...", "...##########...", "...##########...", "...##########...",
        "...##########...", "...##########...", "...##########...", "...##########...",
        "...##########...", "................", "................", "................"],
    "leggings": [
        "................", "................", "...##########...", "...##########...",
        "...##########...", "...###....###...", "...###....###...", "...###....###...",
        "...###....###...", "...###....###...", "...###....###...", "...###....###...",
        "...###....###...", "................", "................", "................"],
    "boots": [
        "................", "................", "................", "................",
        "................", "................", "..###.....###...", "..###.....###...",
        "..###.....###...", "..###.....###...", "..####....####..", "..####....####..",
        ".#####...#####..", ".#####...#####..", "................", "................"],
}

SETS = [
    ("jungle_ops", "Jungle Ops", JUNGLE, "minecraft:leather", 101),
    ("sandstorm", "Sandstorm", SAND, "minecraft:iron_ingot", 202),
]

RECIPE_PATTERNS = {
    "helmet": (["XXX", "X X"], 1),
    "chestplate": (["X X", "XXX", "XXX"], 1),
    "leggings": (["XXX", "X X", "X X"], 1),
    "boots": (["X X", "X X"], 1),
}


def armor_icon(piece, pal, seed):
    def paint(path):
        ic = Icon()
        for y, row in enumerate(ARMOR_ICON_MASKS[piece]):
            for x, ch in enumerate(row):
                if ch == "#":
                    ic.set(x, y, camo(x, y, pal, seed))
        ic.save(path)
    return paint


def do_armor():
    for setname, disp, pal, mat, seed in SETS:
        paint_armor_texture(TEX_ARMOR / f"{setname}_1.png", MASK1, pal, seed)
        paint_armor_texture(TEX_ARMOR / f"{setname}_2.png", MASK2, pal, seed + 5)
        for piece, pdisp, group, slot, ench, prot, geom, baby_geom, setup, dur, texidx in PIECES:
            ident = f"{NS}:{setname}_{piece}"
            key = f"gx_{setname}_{piece}"
            write_icon(key, armor_icon(piece, pal, seed))
            write_item(ident, key, {
                "minecraft:icon": key,
                "minecraft:max_stack_size": 1,
                "minecraft:enchantable": {"slot": ench, "value": 10},
                "minecraft:wearable": {"slot": slot, "protection": prot},
                "minecraft:durability": {"damage_chance": {"min": 60, "max": 100},
                                         "max_durability": dur},
                "minecraft:repairable": {"repair_items": [
                    {"items": [mat], "repair_amount": "q.max_durability * 0.25"}]},
                "minecraft:tags": {"tags": ["minecraft:is_armor", "minecraft:trimmable_armors"]},
            }, group=group)
            lang(f"item.{ident}", f"{disp} {pdisp}")
            tex = f"textures/models/armor/{setname}_{texidx}"
            dump(ATTACH / f"{setname}_{piece}.json", {"format_version": "1.8.0", "minecraft:attachable": {
                "description": {
                    "identifier": ident,
                    "materials": {"default": "armor", "enchanted": "armor_enchanted"},
                    "textures": {"default": tex, "enchanted": "textures/misc/enchanted_actor_glint",
                                 "baby": tex},
                    "geometry": {"default": geom, "baby": baby_geom},
                    "scripts": {"parent_setup": setup, "pre_animation": [
                        "v.use_baby_geo = q.is_baby && c.owning_entity->v.use_dedicated_baby_armor;"]},
                    "render_controllers": ["controller.render.armor.v2"]}}})
            pattern, count = RECIPE_PATTERNS[piece]
            shaped(ident, pattern, {"X": mat}, count)


# ---------------------------------------------------------------- entry point
def run():
    do_sabers()
    do_grenades()
    do_armor()
