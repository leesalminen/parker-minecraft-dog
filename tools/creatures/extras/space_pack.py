"""Galaxy Space Suit: 4 armor pieces (helmet, chestplate, leggings, boots).  Wearing all four lets you live in
space (top of the overworld sky, see scripts/space.js).  Reuses the armor plumbing from military_pack."""
import lib
from lib import noise3, hash01, mix, shade, rgb, write_png, dump, lang
from extras import military_pack as mp

SET = "space"
DISP = "Galaxy Space Suit"
WHITE, WHITE_D, ORANGE, GOLD = "#eef1f4", "#aab3bb", "#f2762e", "#d9a441"


def suit_px(x, y, seed):
    n = noise3(x, y, 0, seed, 3.0)
    c = mix(WHITE_D, WHITE, 0.55 + 0.45 * n)
    c = shade(c, 0.95 + 0.1 * hash01(x, y, seed))
    if x % 8 == 0 or y % 8 == 0:
        c = shade(c, 0.88)
    if x < 16 and y >= 28:
        c = mix("#6d757d", "#8f979f", n)                                # boots
    elif 40 <= x < 56 and y >= 29:
        c = mix("#6d757d", "#8f979f", n)                                # gloves
    elif 20 <= x < 28 and y in (24, 25):
        c = rgb(ORANGE)                                                 # chest band
    elif 20 <= x < 28 and 20 <= y < 23 and 22 <= x < 26:
        c = rgb("#3b4a5a")                                              # chest control panel
    elif 40 <= x < 56 and y in (18, 19):
        c = rgb(ORANGE)                                                 # arm band
    elif x < 16 and y in (16, 17):
        c = rgb(ORANGE)                                                 # leg band
    if 8 <= x < 16 and 8 <= y < 16:                                     # helmet front: gold visor
        if 9 <= x <= 14 and 9 <= y <= 13:
            c = mix("#7a5a1c", GOLD, noise3(x, y, 0, seed + 4, 1.6))
    return c


def paint_tex(path, mask, seed):
    px = [(0, 0, 0, 0)] * (64 * 32)
    for y, row in enumerate(mask):
        bits = int(row, 16)
        for x in range(64):
            if (bits >> x) & 1:
                px[y * 64 + x] = suit_px(x, y, seed)
    write_png(path, px, 64, 32)


def icon(piece):
    def paint(path):
        ic = mp.Icon()
        for y, row in enumerate(mp.ARMOR_ICON_MASKS[piece]):
            for x, ch in enumerate(row):
                if ch == "#":
                    ic.set(x, y, mix(WHITE_D, WHITE, 0.5 + 0.5 * noise3(x, y, 0, 5, 2.0)))
        if piece == "helmet":
            ic.rect(4, 5, 11, 8, GOLD)
        elif piece == "chestplate":
            ic.rect(4, 8, 11, 9, ORANGE)
        elif piece == "boots":
            ic.rect(1, 12, 5, 13, "#6d757d"); ic.rect(10, 12, 14, 13, "#6d757d")
        ic.save(path)
    return paint


PATTERNS = {"helmet": ["XXX", "XGX"], "chestplate": ["X X", "XXX", "XXX"],
            "leggings": ["XXX", "X X", "X X"], "boots": ["X X", "X X"]}


def run():
    mp.TEX_ARMOR.mkdir(parents=True, exist_ok=True)
    paint_tex(mp.TEX_ARMOR / f"{SET}_1.png", mp.MASK1, 301)
    paint_tex(mp.TEX_ARMOR / f"{SET}_2.png", mp.MASK2, 307)
    for piece, pdisp, group, slot, ench, prot, geom, baby_geom, setup, dur, texidx in mp.PIECES:
        ident = f"gx:{SET}_{piece}"
        key = f"gx_{SET}_{piece}"
        mp.write_icon(key, icon(piece))
        mp.write_item(ident, key, {
            "minecraft:icon": key, "minecraft:max_stack_size": 1,
            "minecraft:enchantable": {"slot": ench, "value": 10},
            "minecraft:wearable": {"slot": slot, "protection": prot},
            "minecraft:durability": {"damage_chance": {"min": 60, "max": 100}, "max_durability": dur * 2},
            "minecraft:repairable": {"repair_items": [{"items": ["minecraft:iron_ingot"], "repair_amount": "q.max_durability * 0.25"}]},
            "minecraft:tags": {"tags": ["minecraft:is_armor", "minecraft:trimmable_armors"]},
        }, group=group)
        lang(f"item.{ident}", f"{DISP} {pdisp}")
        tex = f"textures/models/armor/{SET}_{texidx}"
        dump(mp.ATTACH / f"{SET}_{piece}.json", {"format_version": "1.8.0", "minecraft:attachable": {"description": {
            "identifier": ident, "materials": {"default": "armor", "enchanted": "armor_enchanted"},
            "textures": {"default": tex, "enchanted": "textures/misc/enchanted_actor_glint", "baby": tex},
            "geometry": {"default": geom, "baby": baby_geom},
            "scripts": {"parent_setup": setup, "pre_animation": ["v.use_baby_geo = q.is_baby && c.owning_entity->v.use_dedicated_baby_armor;"]},
            "render_controllers": ["controller.render.armor.v2"]}}})
        mp.shaped(ident, PATTERNS[piece], {"X": "minecraft:iron_ingot", "G": "minecraft:glass"}, 1)
