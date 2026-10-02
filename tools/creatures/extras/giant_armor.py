"""Galaxy Forge giant armor: the Armor Forge (a big crafting table block) plus 12 four-piece armor sets.

Each set also has a matching signature weapon (do_weapons) crafted at the same Forge.

Wearing a full set makes the player physically bigger and stronger (scripts/giants.js): `minecraft:scale` via
a `player.json` override, potion-style buffs, a sprint ram that smashes mobs, a landing stomp and a per-set perk.
Armor recipes only work at the Armor Forge (`gx_armor_forge` crafting tag).  Reuses the armor plumbing from
military_pack.  Emits BP items/recipes/blocks/entities/player.json, RP attachables/textures/geometry and
BP scripts/generated/giants.js.
"""
import json
from pathlib import Path
import lib
from lib import BP, RP, dump, lang, write_png, noise3, hash01, rgb, shade, mix
from extras import military_pack as mp

HERE = Path(__file__).resolve().parent
FORGE_TAG = "gx_armor_forge"
PREFIX = "giant_"

# id, name, size multiplier, material, core (extra ingredient in every recipe), protection h/c/l/b, durability x,
# buffs (effect -> amplifier, 0 = level I), ram damage, stomp damage, perk, palette dark/mid/light, accent, style
SETS = [
    dict(id="ogre", name="Ogre Hide", scale=1.4, mat="minecraft:leather", core=None, prot=(2, 5, 4, 2), dur=1.0,
         fx={"strength": 0, "speed": 0}, ram=8, stomp=0, perk=None,
         pal=("#4a3322", "#7a5636", "#a37a4c"), accent="#d8c9a3", style="hide"),
    dict(id="copper", name="Copper Colossus", scale=1.6, mat="minecraft:copper_ingot", core=None, prot=(2, 6, 5, 2),
         dur=1.2, fx={"strength": 0, "speed": 0, "resistance": 0}, ram=10, stomp=0, perk=None,
         pal=("#8a4a2a", "#c2733f", "#e89a62"), accent="#3fa58a", style="copper"),
    dict(id="iron", name="Iron Giant", scale=1.8, mat="minecraft:iron_ingot", core=None, prot=(3, 7, 5, 3),
         dur=1.6, fx={"strength": 1, "speed": 0, "resistance": 0}, ram=12, stomp=0, perk=None,
         pal=("#6a6e75", "#a4a9b0", "#d2d6da"), accent="#e8ecef", style="plate"),
    dict(id="gold", name="Gold Goliath", scale=1.8, mat="minecraft:gold_ingot", core=None, prot=(3, 5, 4, 3),
         dur=0.9, fx={"strength": 1, "speed": 2, "haste": 1}, ram=12, stomp=0, perk=None,
         pal=("#a9741a", "#e0a82e", "#fbe27a"), accent="#fff6b8", style="gold"),
    dict(id="frost", name="Frost Giant", scale=2.0, mat="minecraft:blue_ice", core=None, prot=(3, 7, 6, 3), dur=1.7,
         fx={"strength": 1, "speed": 1, "resistance": 1}, ram=14, stomp=0, perk="frost",
         pal=("#5a8fc4", "#9fd3f2", "#e8f8ff"), accent="#ffffff", style="frost"),
    dict(id="magma", name="Magma Titan", scale=2.2, mat="minecraft:blaze_rod", core="minecraft:magma_cream",
         prot=(3, 8, 6, 3), dur=1.9, fx={"strength": 2, "speed": 1, "resistance": 1, "fire_resistance": 0},
         ram=16, stomp=0, perk="fire",
         pal=("#1c1414", "#3a2a26", "#5a423a"), accent="#ff7a1a", style="magma"),
    dict(id="storm", name="Storm Giant", scale=2.4, mat="minecraft:lapis_lazuli", core="minecraft:lightning_rod",
         prot=(3, 8, 6, 3), dur=1.9, fx={"strength": 2, "speed": 2, "resistance": 1}, ram=16, stomp=0,
         perk="lightning", pal=("#1e2a4a", "#34508a", "#5f86c9"), accent="#ffe83a", style="storm"),
    dict(id="ender", name="Ender Colossus", scale=2.4, mat="minecraft:ender_pearl", core="minecraft:ender_eye",
         prot=(3, 7, 6, 3), dur=2.0, fx={"strength": 2, "speed": 2, "jump_boost": 2, "slow_falling": 0},
         ram=16, stomp=0, perk="launch", pal=("#120a1c", "#2a1a42", "#46306a"), accent="#e65cff", style="ender"),
    dict(id="emerald", name="Emerald Behemoth", scale=2.2, mat="minecraft:emerald", core=None, prot=(3, 8, 6, 3),
         dur=1.8, fx={"strength": 2, "speed": 1, "resistance": 1, "regeneration": 0}, ram=15, stomp=0, perk=None,
         pal=("#0d7a3a", "#17c15a", "#7af0a4"), accent="#d6ffe6", style="plate"),
    dict(id="diamond", name="Diamond Behemoth", scale=2.8, mat="minecraft:diamond", core=None, prot=(3, 8, 6, 3),
         dur=3.0, fx={"strength": 3, "speed": 1, "resistance": 2, "health_boost": 2}, ram=20, stomp=14, perk=None,
         pal=("#1a9aa6", "#3fd6dd", "#b4fbff"), accent="#ffffff", style="plate"),
    dict(id="netherite", name="Netherite Juggernaut", scale=3.2, mat="minecraft:netherite_scrap",
         core="minecraft:netherite_ingot", prot=(3, 8, 6, 3), dur=4.0,
         fx={"strength": 3, "speed": 1, "resistance": 3, "fire_resistance": 0, "health_boost": 4},
         ram=26, stomp=20, perk=None, pal=("#2a2528", "#4a4146", "#6e6268"), accent="#d9a441", style="plate"),
    dict(id="kaiju", name="Cosmic Kaiju", scale=4.0, mat="minecraft:amethyst_shard", core="minecraft:nether_star",
         prot=(4, 9, 7, 4), dur=5.0,
         fx={"strength": 5, "speed": 2, "resistance": 3, "fire_resistance": 0, "regeneration": 1,
             "health_boost": 9, "jump_boost": 2}, ram=40, stomp=30, perk=None,
         pal=("#0a0614", "#1c1230", "#33224f"), accent="#38f0ff", style="kaiju"),
]

# recipe patterns: the vanilla shape, with the gap filled by the set's core ingredient when it has one
PATTERNS = {"helmet": (["XXX", "X X"], ["XXX", "XCX"]), "chestplate": (["X X", "XXX", "XXX"], ["XCX", "XXX", "XXX"]),
            "leggings": (["XXX", "X X", "X X"], ["XXX", "XCX", "X X"]), "boots": (["X X", "X X"], ["XCX", "X X"])}


# ---------------------------------------------------------------- armor painting
def px(s, x, y, seed):
    d, m, l = s["pal"]
    acc, st = s["accent"], s["style"]
    n = noise3(x, y, 0, seed, 3.0)
    c = mix(d, l, 0.15 + 0.7 * n)
    if st == "hide":
        c = shade(c, 0.93 + 0.14 * hash01(x, y, seed))
        if x % 8 == 0 or y % 8 == 0:
            c = shade(c, 0.7) if (x + y) % 3 else rgb(acc)
    elif st == "copper":
        c = shade(c, 0.95 + 0.1 * hash01(x, y, seed))
        if noise3(x, y, 0, seed + 3, 2.5) > 0.66:
            c = mix(c, acc, 0.75)
    elif st in ("plate", "gold"):
        c = shade(mix(d, m, 0.5 + 0.5 * n), 0.96 + 0.08 * hash01(x, y, seed))
        if x % 8 == 0 or y % 8 == 0:
            c = shade(c, 0.74)
        elif x % 8 == 1 or y % 8 == 1:
            c = shade(c, 1.18)
        if x % 8 == 3 and y % 8 == 3:
            c = rgb(acc)                                                # rivet
        if st == "gold" and (x + y) % 9 < 2:
            c = mix(c, acc, 0.45)
    elif st == "frost":
        c = mix(m, l, n)
        if hash01(x // 2, y // 2, seed) > 0.72:
            c = mix(c, acc, 0.7)
        if (x + 2 * y) % 11 == 0:
            c = shade(c, 0.8)
    elif st == "magma":
        c = shade(mix(d, m, n), 0.9 + 0.2 * hash01(x, y, seed))
        if abs(noise3(x, y, 0, seed + 5, 2.2) - 0.5) < 0.06:
            c = rgb(acc)                                                # glowing crack
        elif abs(noise3(x, y, 0, seed + 5, 2.2) - 0.5) < 0.1:
            c = mix(c, "#c2410c", 0.6)
    elif st == "storm":
        c = shade(mix(d, m, n), 0.92 + 0.16 * hash01(x, y, seed))
        k = y // 3
        if (x + k * (-2 if k % 2 else 2)) % 12 == 0:
            c = rgb(acc)                                                # lightning zig-zag
    elif st == "ender":
        c = mix(d, m, n)
        h = hash01(x, y, seed)
        if h > 0.965:
            c = rgb("#5ff3ff")
        elif h > 0.92:
            c = rgb(acc)
    elif st == "kaiju":
        c = mix(d, m, n)
        v = abs(noise3(x, y, 0, seed + 9, 2.6) - 0.5)
        if v < 0.05:
            c = rgb(acc)                                                # energy vein
        elif hash01(x, y, seed) > 0.97:
            c = rgb("#ff4fd8")
    return c


def paint_tex(path, mask, s, seed):
    pix = [(0, 0, 0, 0)] * (64 * 32)
    for y, row in enumerate(mask):
        bits = int(row, 16)
        for x in range(64):
            if (bits >> x) & 1:
                pix[y * 64 + x] = px(s, x, y, seed)
    write_png(path, pix, 64, 32)


def icon(piece, s, seed):
    def paint(path):
        ic = mp.Icon()
        for y, row in enumerate(mp.ARMOR_ICON_MASKS[piece]):
            for x, ch in enumerate(row):
                if ch == "#":
                    ic.set(x, y, px(s, x * 2, y * 2, seed))
        if piece == "helmet":
            ic.rect(4, 5, 11, 6, shade(s["accent"], 0.9))              # visor
        elif piece == "chestplate":
            ic.rect(7, 4, 8, 11, s["accent"])                            # chest stripe
        elif piece == "boots":
            ic.rect(1, 12, 5, 12, s["accent"]); ic.rect(10, 12, 14, 12, s["accent"])
        ic.save(path)
    return paint


def seed_of(s):
    return 400 + SETS.index(s) * 11


def do_armor():
    mp.TEX_ARMOR.mkdir(parents=True, exist_ok=True)
    for s in SETS:
        seed = seed_of(s)
        key_set = f"{PREFIX}{s['id']}"
        paint_tex(mp.TEX_ARMOR / f"{key_set}_1.png", mp.MASK1, s, seed)
        paint_tex(mp.TEX_ARMOR / f"{key_set}_2.png", mp.MASK2, s, seed + 5)
        for i, (piece, pdisp, group, slot, ench, _prot, geom, baby_geom, setup, dur, texidx) in enumerate(mp.PIECES):
            ident = f"gx:{key_set}_{piece}"
            key = f"gx_{key_set}_{piece}"
            mp.write_icon(key, icon(piece, s, seed))
            mp.write_item(ident, key, {
                "minecraft:icon": key, "minecraft:max_stack_size": 1,
                "minecraft:enchantable": {"slot": ench, "value": 12},
                "minecraft:wearable": {"slot": slot, "protection": s["prot"][i]},
                "minecraft:durability": {"damage_chance": {"min": 60, "max": 100},
                                         "max_durability": round(dur * s["dur"])},
                "minecraft:repairable": {"repair_items": [
                    {"items": [s["mat"]], "repair_amount": "q.max_durability * 0.25"}]},
                "minecraft:tags": {"tags": ["minecraft:is_armor", "minecraft:trimmable_armors"]},
            }, group=group)
            lang(f"item.{ident}", f"{s['name']} {pdisp}")
            tex = f"textures/models/armor/{key_set}_{texidx}"
            dump(mp.ATTACH / f"{key_set}_{piece}.json", {"format_version": "1.8.0", "minecraft:attachable": {
                "description": {
                    "identifier": ident,
                    "materials": {"default": "armor", "enchanted": "armor_enchanted"},
                    "textures": {"default": tex, "enchanted": "textures/misc/enchanted_actor_glint", "baby": tex},
                    "geometry": {"default": geom, "baby": baby_geom},
                    "scripts": {"parent_setup": setup, "pre_animation": [
                        "v.use_baby_geo = q.is_baby && c.owning_entity->v.use_dedicated_baby_armor;"]},
                    "render_controllers": ["controller.render.armor.v2"]}}})
            plain, cored = PATTERNS[piece]
            key_map = {"X": {"item": s["mat"]}}
            if s["core"]:
                key_map["C"] = {"item": s["core"]}
            dump(mp.RECIPES / f"{key_set}_{piece}.json", {"format_version": "1.20.10", "minecraft:recipe_shaped": {
                "description": {"identifier": ident}, "tags": [FORGE_TAG],
                "pattern": cored if s["core"] else plain, "key": key_map,
                "result": {"item": ident, "count": 1}}})


# ---------------------------------------------------------------- matching weapons
# set id -> (kind, display name, attack damage in HP, weapon perk used when the set has no perk of its own)
WEAPONS = {
    "ogre":      ("club",   "Ogre Club",           7,  "bash"),
    "copper":    ("maul",   "Copper Maul",         8,  "sunder"),
    "iron":      ("sword",  "Iron Greatsword",     9,  None),
    "gold":      ("axe",    "Gilded Battleaxe",    9,  None),
    "frost":     ("sword",  "Glacier Greatsword",  11, None),
    "magma":     ("cleaver", "Magma Cleaver",      12, None),
    "storm":     ("spear",  "Stormspear",          12, None),
    "ender":     ("axe",    "Void Reaver",         12, None),
    "emerald":   ("spear",  "Emerald Halberd",     11, "cleave"),
    "diamond":   ("sword",  "Diamond Claymore",    14, "cleave"),
    "netherite": ("maul",   "Juggernaut Maul",     18, "wither"),
    "kaiju":     ("cleaver", "Kaiju Cleaver",      28, "cleave"),
}
WEAPON_RECIPE = {"plain": ["XXX", "XXX", " S "], "cored": ["XCX", "XXX", " S "]}
HANDLE_COL = "#5a3b1f"


def weapon_cells(kind):
    """16x16 role grid for one weapon shape: {(x, y): 'blade' | 'handle' | 'accent'}."""
    g = {}

    def line(role, x0, y0, x1, y1, w=0):
        n = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for i in range(n + 1):
            cx = round(x0 + (x1 - x0) * i / n)
            cy = round(y0 + (y1 - y0) * i / n)
            for dy in range(-w, w + 1):
                for dx in range(-w, w + 1):
                    if 0 <= cx + dx < 16 and 0 <= cy + dy < 16:
                        g[(cx + dx, cy + dy)] = role

    if kind == "sword":
        line("handle", 1, 14, 4, 11); line("accent", 3, 9, 7, 13)          # grip + crossguard
        line("blade", 6, 10, 13, 3, 1); g[(14, 2)] = g[(15, 1)] = g[(14, 1)] = "blade"
    elif kind == "cleaver":
        line("handle", 1, 14, 4, 11); line("accent", 3, 9, 7, 13)
        line("blade", 7, 9, 12, 4, 2); line("blade", 13, 3, 14, 2, 1)
    elif kind == "axe":
        line("handle", 2, 14, 11, 5)
        for y in range(16):
            for x in range(16):
                if (x - 11.5) ** 2 + (y - 4.5) ** 2 <= 11 and x + y >= 10:
                    g[(x, y)] = "blade"
        line("accent", 9, 7, 13, 3)
    elif kind == "maul":
        line("handle", 2, 14, 10, 6)
        line("blade", 8, 4, 14, 10, 1)                                      # slab head across the shaft
        for c in ((8, 4), (14, 10), (7, 3), (15, 11)):
            g[c] = "accent"
    elif kind == "club":
        line("handle", 1, 14, 5, 10)
        line("blade", 5, 10, 8, 7, 1); line("blade", 8, 7, 12, 3, 2)
        for c in ((10, 5), (12, 6), (9, 3), (13, 2)):
            g[c] = "accent"                                                 # studs
    elif kind == "spear":
        line("handle", 1, 14, 11, 4)
        line("accent", 9, 6, 11, 8)
        line("blade", 11, 4, 14, 1, 1); g[(15, 0)] = "blade"
    return g


def weapon_icon(kind, s, seed):
    def paint(path):
        g = weapon_cells(kind)
        ic = mp.Icon()
        for (x, y), role in g.items():
            if role == "blade":
                c = px(s, x * 2, y * 2, seed)
                edge = any((x + dx, y + dy) not in g for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                c = shade(c, 0.62 if edge else 1.0 + 0.1 * (x - y < 0))
            elif role == "handle":
                c = shade(HANDLE_COL, 0.9 + 0.2 * hash01(x, y, seed))
            else:
                c = shade(s["accent"], 0.95)
            ic.set(x, y, c)
        ic.save(path)
    return paint


def do_weapons():
    out = {}
    for s in SETS:
        kind, wname, dmg, wperk = WEAPONS[s["id"]]
        seed = seed_of(s) + 7
        ident = f"gx:{PREFIX}{s['id']}_{kind}"
        key = f"gx_{PREFIX}{s['id']}_{kind}"
        mp.write_icon(key, weapon_icon(kind, s, seed))
        mp.write_item(ident, key, {
            "minecraft:icon": key, "minecraft:max_stack_size": 1, "minecraft:hand_equipped": True,
            "minecraft:damage": dmg,
            "minecraft:durability": {"max_durability": round(400 * s["dur"])},
            "minecraft:enchantable": {"slot": "sword", "value": 14},
            "minecraft:repairable": {"repair_items": [
                {"items": [s["mat"]], "repair_amount": "q.max_durability * 0.25"}]},
            "minecraft:tags": {"tags": ["minecraft:is_sword"]},
            **({"minecraft:glint": True} if s["id"] in ("storm", "ender", "kaiju") else {}),
        }, group="minecraft:itemGroup.name.sword")
        lang(f"item.{ident}", wname)
        key_map = {"X": {"item": s["mat"]}, "S": {"item": "minecraft:stick"}}
        if s["core"]:
            key_map["C"] = {"item": s["core"]}
        dump(mp.RECIPES / f"{PREFIX}{s['id']}_{kind}.json", {"format_version": "1.20.10", "minecraft:recipe_shaped": {
            "description": {"identifier": ident}, "tags": [FORGE_TAG],
            "pattern": WEAPON_RECIPE["cored" if s["core"] else "plain"], "key": key_map,
            "result": {"item": ident, "count": 1}}})
        out[ident] = {"set": s["id"], "perk": s["perk"] or wperk}
    return out


# ---------------------------------------------------------------- the Armor Forge block
FORGE = "gx:armor_forge"
FORGE_TEX = {
    "iron": lambda x, y: shade(mix("#2b2e33", "#4a4f57", noise3(x, y, 0, 21, 3.0)), 0.92 + 0.16 * hash01(x, y, 21))
    if not ((x in (1, 14)) and (y in (1, 14))) else rgb("#9aa0a8"),
    "wood": lambda x, y: shade(mix("#4a2f1a", "#6b4426", noise3(x, 0, 0, 22, 2.0)),
                               0.78 if y % 5 == 0 else 0.94 + 0.12 * hash01(x, y, 22)),
    "ember": lambda x, y: (rgb("#1a1412") if (x % 4 == 0 or y % 4 == 0) else
                           mix("#c2410c", "#ffb02e", noise3(x, y, 0, 23, 2.0))),
    "gold": lambda x, y: shade(mix("#b9831f", "#f7d24a", noise3(x, y, 0, 24, 2.5)), 0.94 + 0.12 * hash01(x, y, 24)),
}
# boxes: (material, x0, y0, z0, x1, y1, z1) in pixels, front = south (+z); a dict material is per-face
FORGE_BOXES = [
    ("iron", 0, 0, 0, 3, 8, 3), ("iron", 13, 0, 0, 16, 8, 3), ("iron", 0, 0, 13, 3, 8, 16), ("iron", 13, 0, 13, 16, 8, 16),
    ({"s": "ember", "*": "iron"}, 3, 1, 3, 13, 8, 15),                    # furnace body with a glowing mouth
    ("gold", 3, 0.5, 3, 13, 1, 15),                                        # brass base trim
    ({"u": "wood", "d": "iron", "*": "wood"}, 0, 8, 0, 16, 11, 16),       # table top
    ("gold", 0, 10.5, 0, 16, 11, 0.5), ("gold", 0, 10.5, 15.5, 16, 11, 16),
    ("iron", 2, 11, 4, 9, 12, 12), ("iron", 3.5, 12, 6, 7.5, 14, 10), ("iron", 1, 14, 3, 11, 16, 13),   # anvil
    ("gold", 12, 11, 7, 15, 15, 11), ("iron", 12.5, 15, 8, 14.5, 16, 10),  # armor stand torso + helm
]
_FACES = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}


def _fmat(m, f):
    return (m.get(f) or m.get("*")) if isinstance(m, dict) else m


def _uv(f, b):
    _, x0, y0, z0, x1, y1, z1 = b
    if f in "ns":
        return [x0, 16 - y1], [x1 - x0, y1 - y0]
    if f in "ew":
        return [z0, 16 - y1], [z1 - z0, y1 - y0]
    return [x0, z0], [x1 - x0, z1 - z0]


def forge_geometry():
    cubes = []
    for b in FORGE_BOXES:
        uv = {}
        for f, name in _FACES.items():
            o, sz = _uv(f, b)
            uv[name] = {"uv": o, "uv_size": sz, "material_instance": _fmat(b[0], f)}
        cubes.append({"origin": [b[1] - 8, b[2], b[3] - 8], "size": [b[4] - b[1], b[5] - b[2], b[6] - b[3]], "uv": uv})
    return {"format_version": "1.21.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.gx_armor_forge", "texture_width": 16, "texture_height": 16,
                        "visible_bounds_width": 2, "visible_bounds_height": 2, "visible_bounds_offset": [0, 0.5, 0]},
        "bones": [{"name": "body", "pivot": [0, 0, 0], "cubes": cubes}]}]}


def do_forge():
    for m, fn in FORGE_TEX.items():
        write_png(RP / f"textures/blocks/gx_forge/{m}.png",
                  [rgb(fn(x, y)) for y in range(16) for x in range(16)], 16, 16)
    path = RP / "textures/terrain_texture.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.setdefault("resource_pack_name", "GalaxyForge")
    data.setdefault("texture_name", "atlas.terrain")
    data.setdefault("padding", 8)
    data.setdefault("num_mip_levels", 4)
    td = {k: v for k, v in data.get("texture_data", {}).items() if not k.startswith("gx_forge_")}
    for m in FORGE_TEX:
        td[f"gx_forge_{m}"] = {"textures": f"textures/blocks/gx_forge/{m}"}
    data["texture_data"] = dict(sorted(td.items()))
    dump(path, data)
    dump(RP / "models/blocks/gx_armor_forge.geo.json", forge_geometry())
    inst = {"*": {"texture": "gx_forge_iron", "render_method": "opaque"}}
    for m in FORGE_TEX:
        inst[m] = {"texture": f"gx_forge_{m}", "render_method": "opaque", "ambient_occlusion": False,
                   "face_dimming": True}
    full = {"origin": [-8, 0, -8], "size": [16, 16, 16]}
    dump(BP / "blocks/gx_armor_forge.json", {"format_version": "1.21.0", "minecraft:block": {
        "description": {"identifier": FORGE, "menu_category": {"category": "construction"},
                        "traits": {"minecraft:placement_direction": {"enabled_states": ["minecraft:cardinal_direction"]}}},
        "components": {
            "minecraft:geometry": "geometry.gx_armor_forge", "minecraft:material_instances": inst,
            "minecraft:collision_box": full, "minecraft:selection_box": full,
            "minecraft:crafting_table": {"grid_size": 3, "crafting_tags": [FORGE_TAG], "custom_description": "Armor Forge"},
            "minecraft:light_emission": 10, "minecraft:map_color": "#4a4f57",
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 3.0},
            "minecraft:destructible_by_explosion": {"explosion_resistance": 30}},
        "permutations": [{"condition": f"query.block_state('minecraft:cardinal_direction') == '{d}'",
                          "components": {"minecraft:transformation": {"rotation": [0, deg, 0]}}}
                         for d, deg in (("south", 180), ("west", 90), ("east", 270))]}})
    lang(f"tile.{FORGE}.name", "Armor Forge")
    # the forge itself is made at a normal crafting table: 5 iron, a crafting table, 3 stone
    dump(BP / "recipes/gx_armor_forge.json", {"format_version": "1.20.10", "minecraft:recipe_shaped": {
        "description": {"identifier": "gx:armor_forge_recipe"}, "tags": ["crafting_table"],
        "pattern": ["III", "ICI", "SSS"],
        "key": {"I": {"item": "minecraft:iron_ingot"}, "C": {"item": "minecraft:crafting_table"},
                "S": {"item": "minecraft:stone"}},
        "result": {"item": FORGE, "count": 1}}})


# ---------------------------------------------------------------- player size override + script data
def scale_id(scale):
    return f"gx:size_{round(scale * 10)}"


def do_player():
    scales = sorted({s["scale"] for s in SETS})
    p = json.loads((HERE / "player_base.json").read_text())
    ent = p["minecraft:entity"]
    groups = {scale_id(sc): {"minecraft:scale": {"value": sc},
                             "minecraft:collision_box": {"width": round(0.6 * sc, 2), "height": round(1.8 * sc, 2)}}
              for sc in scales}
    ent["component_groups"].update(groups)
    ent["events"]["gx:size_reset"] = {"remove": {"component_groups": list(groups)}}
    for g in groups:
        ent["events"][g] = {"remove": {"component_groups": [o for o in groups if o != g]},
                            "add": {"component_groups": [g]}}
    dump(BP / "entities/player.json", p)


def do_script_data(weapons):
    out = {}
    for s in SETS:
        out[s["id"]] = {"name": s["name"], "scale": s["scale"], "event": scale_id(s["scale"]), "fx": s["fx"],
                        "ram": s["ram"], "stomp": s["stomp"], "perk": s["perk"]}
    path = BP / "scripts/generated/giants.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("// GENERATED by tools/creatures/extras/giant_armor.py - do not edit by hand.\n"
                    "// Regenerate with: python3 tools/creatures/build_all.py\n\n"
                    f"export const GIANT_PREFIX = \"gx:{PREFIX}\";\n"
                    f"export const GIANTS = {json.dumps(out, indent=2)};\n"
                    f"export const GIANT_WEAPONS = {json.dumps(weapons, indent=2)};\n")


def run():
    do_armor()
    do_forge()
    do_player()
    weapons = do_weapons()
    do_script_data(weapons)
    print(f"  giant armor: {len(SETS)} sets, {len(SETS) * 4} pieces, {len(weapons)} weapons, armor forge")
