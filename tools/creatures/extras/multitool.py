"""Galaxy Forge multi-tool: four tiers of a 5-in-1 tool (pickaxe, shovel, axe, sword, bow).

Reuses the item framework in extras/military_pack.py; build_all.py imports this module and calls run().
"""
from lib import lang, shade
from extras.military_pack import Icon, write_item, write_icon, shapeless

NS = "gx"

# id, display name, tier tag, head colour, durability, dig speed, attack damage, enchantability, repair material
TIERS = [
    ("wood",      "Wooden Multi-Tool",    "minecraft:wooden_tier",    "#9a7440", 59,   2, 5, 15, "minecraft:oak_planks"),
    ("iron",      "Iron Multi-Tool",      "minecraft:iron_tier",      "#d8d8d8", 250,  6, 7, 14, "minecraft:iron_ingot"),
    ("diamond",   "Diamond Multi-Tool",   "minecraft:diamond_tier",   "#4fd8d0", 1561, 8, 8, 10, "minecraft:diamond"),
    ("netherite", "Netherite Multi-Tool", "minecraft:netherite_tier", "#6a5a62", 2031, 9, 9, 15, "minecraft:netherite_ingot"),
]

# The five tools this item replaces; it is crafted by merging their vanilla forms with a bow.
MERGE = {
    "wood": ["minecraft:wooden_pickaxe", "minecraft:wooden_shovel", "minecraft:wooden_axe", "minecraft:wooden_sword"],
    "iron": ["minecraft:iron_pickaxe", "minecraft:iron_shovel", "minecraft:iron_axe", "minecraft:iron_sword"],
    "diamond": ["minecraft:diamond_pickaxe", "minecraft:diamond_shovel", "minecraft:diamond_axe", "minecraft:diamond_sword"],
    "netherite": ["minecraft:netherite_pickaxe", "minecraft:netherite_shovel", "minecraft:netherite_axe", "minecraft:netherite_sword"],
}

# Vanilla blocks carry one of these tags per tool family; mining all four makes the item a pickaxe,
# shovel, axe and sword at once. Tier is enforced by the item's "<material>_tier" tag.
DIG_TAGS = ["minecraft:is_pickaxe_item_destructible", "minecraft:is_shovel_item_destructible",
            "minecraft:is_axe_item_destructible", "minecraft:is_sword_item_destructible"]

TOOL_TAGS = ["minecraft:is_tool", "minecraft:is_pickaxe", "minecraft:is_shovel",
             "minecraft:is_axe", "minecraft:is_sword"]

HANDLE = "#7a5a34"


def multitool_icon(head, handle=HANDLE):
    """16x16: one shaft carrying a pickaxe spike, an axe blade, and a bow."""
    def paint(path):
        ic = Icon()
        dark = shade(head, 0.7)
        ic.line(4, 14, 9, 6, 0, handle)           # shaft
        ic.line(5, 14, 10, 6, 0, shade(handle, 0.85))
        ic.line(2, 5, 11, 4, 0, head)             # pickaxe bar
        ic.set(1, 5, dark)                        # spike tip
        ic.rect(9, 3, 11, 7, head)                # axe blade
        ic.set(12, 5, dark)
        ic.line(13, 5, 13, 10, 0, "#efe6c8")      # bow string
        ic.set(13, 5, handle)                     # bow limb
        ic.set(14, 6, handle)
        ic.set(14, 9, handle)
        ic.set(13, 10, handle)
        ic.save(path)
    return paint


def run():
    for tier, disp, tier_tag, head, dur, speed, dmg, ench, mat in TIERS:
        ident = f"{NS}:multitool_{tier}"
        key = f"gx_multitool_{tier}"
        write_icon(key, multitool_icon(head))
        write_item(ident, key, {
            "minecraft:icon": key,
            "minecraft:max_stack_size": 1,
            "minecraft:hand_equipped": True,
            "minecraft:damage": dmg,
            "minecraft:durability": {"max_durability": dur},
            "minecraft:enchantable": {"slot": "pickaxe", "value": ench},
            "minecraft:repairable": {"repair_items": [
                {"items": [mat], "repair_amount": "q.max_durability * 0.25"}]},
            "minecraft:tags": {"tags": TOOL_TAGS + [tier_tag]},
            "minecraft:digger": {
                "use_efficiency": True,
                "destroy_speeds": [{"block": {"tags": f"q.any_tag('{t}')"}, "speed": speed}
                                   for t in DIG_TAGS],
            },
            "minecraft:shooter": {
                "ammunition": [{"item": "minecraft:arrow", "use_offhand": True,
                                "search_inventory": True, "use_in_creative": True}],
                "max_draw_duration": 1.0,
                "scale_power_by_draw_duration": True,
                "charge_on_draw": False,
            },
            "minecraft:use_modifiers": {"movement_modifier": 0.35},
        }, group="minecraft:itemGroup.name.pickaxe")
        lang(f"item.{ident}", disp)
        shapeless(ident, MERGE[tier] + ["minecraft:bow"])
