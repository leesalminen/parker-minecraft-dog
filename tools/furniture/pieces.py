"""Furniture piece definitions.  Coordinates are pixels inside one block: x 0..16 (west->east), y 0..16 (up),
z 0..16 (north/back -> south/front).  The FRONT of every piece is the south (+Z) face.

B(mat, x0,y0,z0, x1,y1,z1)  ->  box.  `mat` is a material name, or a dict of per-face overrides:
   keys: "*" default, "side" (n/s/e/w), "front" (=s), "top" (=u), "bottom" (=d), or n/s/e/w/u/d.
   A leading "@" (e.g. "@oven_front") stretches the whole tile over that face instead of projecting it.
PIECES: list of dicts {id, name, room, boxes, col?, sel?, light?, rot?}.  col=False -> walk-through."""

PIECES = []


def B(mat, x0, y0, z0, x1, y1, z1):
    return (mat, x0, y0, z0, x1, y1, z1)


def piece(id, name, room, boxes, col=None, sel=None, light=0, rot=True):
    PIECES.append(dict(id=id, name=name, room=room, boxes=list(boxes), col=col, sel=sel, light=light, rot=rot))


def legs(mat, x0, z0, x1, z1, h, w=2):
    return [B(mat, x, 0, z, x + w, h, z + w) for x in (x0, x1 - w) for z in (z0, z1 - w)]


# ------------------------------------------------------------------ living room
def sofa_boxes(fab, arms, cushion):
    l, r = arms
    xl = 3 if l else 0
    xr = 13 if r else 16
    b = [*legs("dark_wood", 0, 1, 16, 16, 2),
         B(fab, 0, 2, 1, 16, 6, 16),
         B(fab, 0, 6, 0, 16, 16, 4),
         B(cushion, xl, 6, 4, xr, 9, 16),
         B(cushion, xl + 1 if l else 1, 9, 4, xr - 1 if r else 15, 14, 7)]
    if l: b.append(B(fab, 0, 6, 1, 3, 11, 16))
    if r: b.append(B(fab, 13, 6, 1, 16, 11, 16))
    return b

for _id, _name, _fab, _cush, _arms in [
        ("sofa", "Sofa", "fab_blue", "fab_blue", (1, 1)),
        ("sofa_mid", "Sofa Middle Seat", "fab_blue", "fab_blue", (0, 0)),
        ("sofa_left", "Sofa Left End", "fab_blue", "fab_blue", (1, 0)),
        ("sofa_right", "Sofa Right End", "fab_blue", "fab_blue", (0, 1)),
        ("sofa_leather", "Leather Sofa", "leather", "leather", (1, 1)),
        ("sofa_cream", "Cream Sofa", "fab_cream", "fab_cream", (1, 1))]:
    piece(_id, _name, "Living Room", sofa_boxes(_fab, _arms, _cush), col=None)

piece("armchair", "Armchair", "Living Room", [
    *legs("dark_wood", 1, 2, 15, 16, 2),
    B("fab_green", 1, 2, 2, 15, 6, 16),
    B("fab_green", 1, 6, 0, 15, 16, 4),
    B("fab_green", 1, 6, 4, 4, 11, 16), B("fab_green", 12, 6, 4, 15, 11, 16),
    B("fab_cream", 4, 6, 4, 12, 9, 16),
    B("fab_cream", 4, 9, 4, 12, 14, 6)])

piece("coffee_table", "Coffee Table", "Living Room", [
    B("oak", 0, 6, 2, 16, 8, 14),
    *legs("dark_wood", 1, 3, 15, 13, 6),
    B("dark_wood", 2, 2, 4, 14, 3, 12)])

piece("side_table", "Side Table", "Living Room", [
    B("oak", 2, 10, 2, 14, 12, 14),
    *legs("dark_wood", 3, 3, 13, 13, 10),
    B("dark_wood", 3, 4, 3, 13, 5, 13)])

piece("table_lamp", "Table Lamp", "Living Room", [
    B("brass", 5, 0, 5, 11, 2, 11), B("brass", 7, 2, 7, 9, 8, 9),
    B("lampshade", 4, 8, 4, 12, 15, 12)], light=11)

piece("tv_stand", "TV Stand", "Living Room", [
    B("walnut", 0, 0, 3, 16, 10, 16),
    B({"*": "walnut", "s": "@drawers2"}, 0, 0, 15, 16, 10, 16),
    B("dark_wood", 0, 10, 2, 16, 12, 16)])

piece("tv", "Television", "Living Room", [
    B("iron", 5, 0, 6, 11, 1, 10), B("iron", 7, 1, 7, 9, 3, 9),
    B({"*": "iron", "s": "@screen_off"}, 0, 3, 7, 16, 15, 9)])

piece("tv_unit", "TV on Stand", "Living Room", [
    B("walnut", 0, 0, 3, 16, 7, 16),
    B({"*": "walnut", "s": "@drawers2"}, 0, 0, 15, 16, 7, 16),
    B("iron", 6, 7, 8, 10, 8, 12), B("iron", 7, 8, 9, 9, 9, 11),
    B({"*": "iron", "s": "@screen_on"}, 0, 9, 9, 16, 16, 11)])

piece("bookshelf", "Bookshelf", "Living Room", [
    B("walnut", 0, 0, 2, 16, 16, 3),
    B("walnut", 0, 0, 3, 1, 16, 16), B("walnut", 15, 0, 3, 16, 16, 16),
    B("walnut", 1, 0, 3, 15, 1, 16), B("walnut", 1, 5, 3, 15, 6, 16),
    B("walnut", 1, 10, 3, 15, 11, 16), B("walnut", 0, 15, 2, 16, 16, 16),
    *[B({"*": "dark_wood", "s": "@books"}, 1, y, 4, 15, y + 4, 15) for y in (1, 6, 11)]])

piece("floor_lamp", "Floor Lamp", "Living Room", [
    B("iron", 5, 0, 5, 11, 1, 11), B("iron", 7.5, 1, 7.5, 8.5, 11, 8.5),
    B("lampshade", 4, 11, 4, 12, 16, 12)], col=[(5, 0, 5, 11, 16, 11)], light=13)

piece("rug", "Red Rug", "Living Room", [B({"*": "rug_red"}, 0, 0, 0, 16, 1, 16)], col=False)
piece("rug_blue", "Blue Rug", "Living Room", [B({"*": "rug_blue"}, 0, 0, 0, 16, 1, 16)], col=False)

piece("fireplace", "Fireplace", "Living Room", [
    B("brick", 0, 0, 2, 3, 14, 16), B("brick", 13, 0, 2, 16, 14, 16),
    B("brick", 3, 0, 2, 13, 12, 4), B("brick", 2, 12, 2, 14, 14, 16),
    B("stone", 0, 14, 0, 16, 16, 16), B("stone", 0, 0, 12, 16, 1, 16),
    B("stone", 3, 0, 4, 13, 1, 12), B("charcoal", 3, 1, 6, 13, 2, 11),
    B("embers", 4, 1, 7, 12, 2, 10),
    B({"*": "fire"}, 4, 2, 6, 12, 8, 6.5), B({"*": "fire"}, 4, 2, 10.5, 12, 8, 11),
    B({"*": "fire"}, 5, 2, 6, 5.5, 8, 11), B({"*": "fire"}, 10.5, 2, 6, 11, 8, 11)], light=14)

piece("curtain", "Curtains", "Living Room", [
    B("brass", 0, 14, 0, 16, 15, 2),
    B("fab_red", 0, 0, 0, 5, 14, 2), B("fab_red", 11, 0, 0, 16, 14, 2),
    B("fab_cream", 5, 2, 0, 11, 14, 1)], col=[(0, 0, 0, 16, 16, 2)])

piece("painting", "Painting", "Living Room", [
    B({"*": "oak", "s": "@painting"}, 1, 2, 0, 15, 14, 1.5)], col=False)

piece("houseplant", "Houseplant", "Living Room", [
    B("terracotta", 4, 0, 4, 12, 6, 12), B("soil", 5, 6, 5, 11, 7, 11),
    B("leaves", 2, 7, 8, 14, 15, 8.5), B("leaves", 8, 7, 2, 8.5, 15, 14),
    B("leaves", 4, 9, 4, 12, 16, 12)], col=[(4, 0, 4, 12, 12, 12)])

# ------------------------------------------------------------------ kitchen
piece("kitchen_counter", "Kitchen Counter", "Kitchen", [
    B("white_wood", 0, 0, 1, 16, 2, 16),
    B({"*": "white_wood", "s": "@cab_door"}, 0, 2, 1, 16, 14, 16),
    B("marble", 0, 14, 0, 16, 16, 16)])

piece("kitchen_sink", "Kitchen Sink", "Kitchen", [
    B({"*": "white_wood", "s": "@cab_door"}, 0, 0, 1, 16, 13, 16),
    B("marble", 0, 13, 0, 16, 15, 3), B("marble", 0, 13, 13, 16, 15, 16),
    B("marble", 0, 13, 3, 3, 15, 13), B("marble", 13, 13, 3, 16, 15, 13),
    B("steel", 3, 13, 3, 13, 14, 13),
    B("chrome", 7.5, 15, 1, 8.5, 16, 2), B("chrome", 7.5, 15.5, 2, 8.5, 16, 5)])

piece("stove", "Stove", "Kitchen", [
    B({"*": "steel", "s": "@oven_front"}, 0, 0, 1, 16, 14, 16),
    B({"*": "iron", "u": "@stove_top"}, 0, 14, 0, 16, 16, 16),
    B("iron", 3, 15, 0, 5, 16, 1), B("iron", 11, 15, 0, 13, 16, 1)])

piece("fridge", "Refrigerator", "Kitchen", [
    B({"*": "steel", "s": "@fridge_front"}, 1, 0, 1, 15, 16, 15)])

piece("kitchen_island", "Kitchen Island", "Kitchen", [
    B("dark_wood", 0, 0, 0, 16, 2, 16),
    B({"*": "white_wood", "s": "@cab_door"}, 1, 2, 1, 15, 13, 15),
    B("oak", 0, 13, 0, 16, 16, 16)])

piece("upper_cabinet", "Upper Cabinet", "Kitchen", [
    B({"*": "white_wood", "s": "@cab_door"}, 0, 3, 0, 16, 16, 10)])

piece("kitchen_table", "Kitchen Table", "Kitchen", [
    B("white_wood", 1, 11, 1, 15, 13, 15), B("oak", 7, 1, 7, 9, 11, 9),
    B("oak", 4, 0, 4, 12, 1, 12)])

piece("kitchen_stool", "Bar Stool", "Kitchen", [
    B("fab_red", 3, 10, 3, 13, 12, 13), B("chrome", 3, 12, 3, 13, 12.5, 13),
    *legs("chrome", 4, 4, 12, 12, 10, 1), B("chrome", 4, 4, 4, 12, 5, 12)],
    col=[(3, 0, 3, 13, 12, 13)])

piece("microwave", "Microwave", "Kitchen", [
    B({"*": "iron", "s": "@micro_front"}, 1, 0, 3, 15, 9, 14)])

piece("range_hood", "Range Hood", "Kitchen", [
    B("steel", 1, 9, 0, 15, 11, 12), B("steel", 2, 11, 0, 14, 13, 9),
    B("steel", 5, 13, 0, 11, 16, 6)], col=[(1, 9, 0, 15, 16, 12)])

piece("fruit_bowl", "Fruit Bowl", "Kitchen", [
    B("white_wood", 4, 0, 4, 12, 1, 12), B("porcelain", 3, 1, 3, 13, 3, 13),
    B("paint_red", 5, 3, 5, 8, 6, 8), B("paint_yellow", 8, 3, 6, 11, 6, 9),
    B("paint_green", 6, 3, 9, 9, 6, 12)], col=[(3, 0, 3, 13, 6, 13)])

# ------------------------------------------------------------------ dining room
piece("dining_table", "Dining Table", "Dining Room", [
    B("walnut", 0, 12, 1, 16, 14, 15), B("dark_wood", 1, 10, 2, 15, 12, 14),
    *legs("dark_wood", 0, 1, 16, 15, 12, 2)])

piece("dining_chair", "Dining Chair", "Dining Room", [
    B("oak", 3, 7, 3, 13, 8, 13), B("fab_cream", 3, 8, 3, 13, 9, 13),
    *legs("oak", 3, 3, 13, 13, 7, 2),
    B("oak", 3, 9, 3, 5, 16, 5), B("oak", 11, 9, 3, 13, 16, 5),
    B("oak", 5, 11, 3.5, 11, 13, 4.5), B("oak", 5, 14, 3.5, 11, 15.5, 4.5)])

piece("china_cabinet", "China Cabinet", "Dining Room", [
    B("walnut", 0, 0, 2, 16, 6, 16),
    B({"*": "walnut", "s": "@cab_door_dark"}, 0, 0, 15, 16, 6, 16),
    B("walnut", 0, 6, 2, 16, 7, 16),
    B("walnut", 0, 7, 2, 16, 16, 3), B("walnut", 0, 7, 3, 1, 16, 16), B("walnut", 15, 7, 3, 16, 16, 16),
    B("walnut", 0, 15, 2, 16, 16, 16), B("walnut", 1, 11, 3, 15, 11.5, 15),
    B("porcelain", 2, 7, 6, 6, 11, 7), B("porcelain", 7, 7, 6, 11, 11, 7),
    B("porcelain", 11, 7, 6, 14, 10, 9), B("porcelain", 2, 11.5, 6, 6, 14, 7),
    B("paint_blue", 8, 11.5, 6, 12, 13, 10),
    B("glass", 1, 7, 15.5, 15, 15, 16)])

piece("chandelier", "Chandelier", "Dining Room", [
    B("iron", 7.5, 11, 7.5, 8.5, 16, 8.5), B("brass", 3, 9, 3, 13, 10, 4),
    B("brass", 3, 9, 12, 13, 10, 13), B("brass", 3, 9, 4, 4, 10, 12), B("brass", 12, 9, 4, 13, 10, 12),
    B("brass", 7, 9, 7, 9, 11, 9),
    *[B("bulb", x, 10, z, x + 1.5, 12.5, z + 1.5) for x, z in ((3, 3), (11.5, 3), (3, 11.5), (11.5, 11.5), (7.25, 7.25))]],
    col=False, sel=(3, 9, 3, 13, 16, 13), light=15)

piece("sideboard", "Sideboard", "Dining Room", [
    B("walnut", 0, 0, 3, 16, 12, 16), B({"*": "walnut", "s": "@drawers3"}, 0, 0, 15, 16, 12, 16),
    B("marble", 0, 12, 2, 16, 14, 16), B("brass", 3, 14, 6, 5, 15, 8)])

# ------------------------------------------------------------------ master bedroom
piece("double_bed", "Double Bed (Head)", "Master Bedroom", [
    B("walnut", 0, 0, 0, 16, 16, 2), B("walnut", 0, 0, 2, 2, 5, 16), B("walnut", 14, 0, 2, 16, 5, 16),
    B("fab_white", 2, 5, 2, 14, 8, 16), B("quilt_blue", 2, 8, 9, 14, 9, 16),
    B("fab_white", 2, 8, 3, 8, 11, 8), B("fab_white", 8, 8, 3, 14, 11, 8),
    B("quilt_blue", 2, 8, 8, 14, 10, 16)], col=[(0, 0, 0, 16, 10, 16)])

piece("double_bed_foot", "Double Bed (Foot)", "Master Bedroom", [
    B("walnut", 0, 0, 14, 16, 8, 16), B("walnut", 0, 0, 0, 2, 5, 14), B("walnut", 14, 0, 0, 16, 5, 14),
    B("fab_white", 2, 5, 0, 14, 8, 14), B("quilt_blue", 2, 8, 0, 14, 10, 14)],
    col=[(0, 0, 0, 16, 10, 16)])

piece("nightstand", "Nightstand", "Master Bedroom", [
    B("walnut", 2, 0, 2, 14, 12, 14),
    B({"*": "walnut", "s": "@drawers2"}, 2, 0, 13, 14, 12, 14),
    B("dark_wood", 1, 12, 1, 15, 14, 15)])

piece("dresser", "Dresser", "Master Bedroom", [
    B("walnut", 0, 0, 3, 16, 14, 16),
    B({"*": "walnut", "s": "@drawers3"}, 0, 0, 15, 16, 14, 16),
    B("dark_wood", 0, 14, 2, 16, 16, 16)])

piece("wardrobe", "Wardrobe", "Master Bedroom", [
    B("walnut", 0, 0, 2, 16, 16, 16),
    B({"*": "walnut", "s": "@wardrobe_front"}, 0, 0, 15, 16, 16, 16)])

piece("vanity_mirror", "Vanity with Mirror", "Master Bedroom", [
    B("white_wood", 0, 8, 2, 16, 10, 16), *legs("white_wood", 0, 2, 16, 16, 8, 2),
    B({"*": "white_wood", "s": "@drawers2"}, 3, 3, 13, 13, 8, 14),
    B("white_wood", 2, 10, 1, 14, 16, 3),
    B({"*": "white_wood", "s": "@mirror"}, 3, 11, 3, 13, 15, 3.5),
    B("bulb", 1.5, 11, 3, 2.5, 15, 4), B("bulb", 13.5, 11, 3, 14.5, 15, 4)], light=8)

piece("vanity_stool", "Vanity Stool", "Master Bedroom", [
    B("fab_pink", 3, 8, 3, 13, 11, 13), *legs("brass", 4, 4, 12, 12, 8, 1)],
    col=[(3, 0, 3, 13, 11, 13)])

piece("ottoman", "Ottoman", "Master Bedroom", [
    B("fab_gray", 1, 2, 3, 15, 8, 13), B("dark_wood", 1, 0, 3, 3, 2, 5), B("dark_wood", 13, 0, 3, 15, 2, 5),
    B("dark_wood", 1, 0, 11, 3, 2, 13), B("dark_wood", 13, 0, 11, 15, 2, 13)])

# ------------------------------------------------------------------ kids room
piece("bunk_bed", "Bunk Bed", "Kids Room", [
    *[B("birch", x, 0, z, x + 2, 16, z + 2) for x in (0, 14) for z in (0, 14)],
    B("birch", 2, 2, 0, 14, 4, 16), B("fab_yellow", 2, 4, 1, 14, 6, 15),
    B("fab_white", 3, 6, 2, 13, 7.5, 6),
    B("birch", 2, 9, 0, 14, 11, 16), B("quilt_rose", 2, 11, 1, 14, 13, 15),
    B("birch", 2, 13, 0, 14, 15, 1), B("birch", 2, 13, 15, 14, 15, 16),
    *[B("birch", 14, y, 2, 16, y + 1, 14) for y in (1, 4, 7, 10)]],
    col=[(0, 0, 0, 16, 16, 16)])

piece("toy_chest", "Toy Chest", "Kids Room", [
    B("paint_blue", 1, 0, 3, 15, 8, 13), B("paint_yellow", 1, 8, 3, 15, 10, 13),
    B("paint_red", 0, 8, 2, 16, 9, 3), B("brass", 7, 7, 13, 9, 9, 14)])

piece("kids_desk", "Kids Desk", "Kids Room", [
    B("birch", 0, 8, 2, 16, 10, 14), *legs("paint_yellow", 0, 2, 16, 14, 8, 2),
    B({"*": "birch", "s": "@drawers2"}, 8, 3, 3, 15, 8, 4)])

piece("play_mat", "Play Mat", "Kids Room", [B({"*": "play_mat", "u": "@play_mat"}, 0, 0, 0, 16, 1, 16)], col=False)

piece("teddy_bear", "Teddy Bear", "Kids Room", [
    B("fab_brown", 5, 0, 5, 11, 6, 10), B("fab_brown", 5, 6, 5, 11, 12, 10),
    B("fab_brown", 4, 0, 4, 7, 3, 8), B("fab_brown", 9, 0, 4, 12, 3, 8),
    B("fab_brown", 3, 5, 5, 5, 9, 8), B("fab_brown", 11, 5, 5, 13, 9, 8),
    B("fab_brown", 5, 9, 3.5, 11, 15, 9), B("fab_brown", 4, 14, 5, 6, 16, 7), B("fab_brown", 10, 14, 5, 12, 16, 7),
    B("fab_cream", 7, 9, 3, 9, 11, 3.5), B("fab_black", 7.5, 10, 2.8, 8.5, 10.6, 3.5)],
    col=[(3, 0, 3, 13, 16, 10)])

piece("toy_blocks", "Toy Blocks", "Kids Room", [
    B("paint_red", 2, 0, 3, 7, 5, 8), B("paint_blue", 8, 0, 4, 13, 5, 9), B("paint_green", 4, 0, 9, 9, 5, 14),
    B("paint_yellow", 4.5, 5, 4, 7.5, 8, 7)], col=[(2, 0, 3, 13, 8, 14)])

# ------------------------------------------------------------------ bathroom
piece("toilet", "Toilet", "Bathroom", [
    B("porcelain", 5, 0, 5, 11, 4, 13), B("porcelain", 4, 4, 4, 12, 8, 15),
    B("porcelain", 3.5, 8, 3.5, 12.5, 9, 15.5), B("porcelain", 4.5, 8.5, 4, 11.5, 9.5, 15),
    B("porcelain", 3, 8, 0.5, 13, 15, 4), B("porcelain", 2.5, 15, 0.5, 13.5, 16, 4.5),
    B("chrome", 7.5, 15.5, 2, 8.5, 16, 3)], col=[(3, 0, 0.5, 13, 16, 15.5)])

piece("bathroom_sink", "Bathroom Sink Vanity", "Bathroom", [
    B({"*": "white_wood", "s": "@cab_door"}, 1, 0, 3, 15, 12, 16),
    B("marble", 0, 12, 2, 16, 13, 16),
    B("porcelain", 3, 13, 5, 13, 15, 15), B("porcelain", 4, 13, 6, 12, 14, 14),
    B("water", 4, 13.4, 6, 12, 13.5, 14),
    B("chrome", 7.5, 13, 2.5, 8.5, 16, 3.5), B("chrome", 7.5, 15, 3.5, 8.5, 16, 6)])

piece("bathtub", "Bathtub", "Bathroom", [
    B("porcelain", 0, 0, 0, 16, 2, 16), B("porcelain", 0, 2, 0, 16, 9, 2), B("porcelain", 0, 2, 14, 16, 9, 16),
    B("porcelain", 0, 2, 2, 2, 9, 14), B("porcelain", 14, 2, 2, 16, 9, 14),
    B("water", 2, 7, 2, 14, 7.5, 14),
    B("chrome", 7.5, 9, 0, 8.5, 12, 1.5), B("chrome", 7.5, 11, 1.5, 8.5, 12, 4),
    B("chrome", 5, 9, 0.5, 6, 10, 1.5), B("chrome", 10, 9, 0.5, 11, 10, 1.5)],
    col=[(0, 0, 0, 16, 9, 16)])

piece("shower", "Shower Stall", "Bathroom", [
    B("bathtile", 0, 0, 0, 16, 1, 16), B("bathtile", 0, 1, 0, 16, 16, 1), B("bathtile", 0, 1, 1, 1, 16, 16),
    B("glass", 15, 1, 1, 16, 16, 16), B("glass", 1, 1, 15, 15, 16, 16),
    B("chrome", 14.5, 1, 14.5, 15.5, 16, 15.5),
    B("chrome", 7.5, 12, 1, 8.5, 16, 2), B("chrome", 6, 12, 2, 10, 13, 5), B("chrome", 3, 8, 1, 5, 10, 2)],
    col=[(0, 0, 0, 16, 16, 16)])

piece("towel_rack", "Towel Rack", "Bathroom", [
    B("chrome", 1, 10, 1, 15, 11, 2), B("chrome", 1, 6, 1, 15, 7, 2),
    B("chrome", 1, 6, 0, 2, 11, 1), B("chrome", 14, 6, 0, 15, 11, 1),
    B("towel_stripe", 2, 2, 2, 8, 11, 3), B("fab_white", 8.5, 5, 2, 14, 11, 3)],
    col=False, sel=(1, 2, 0, 15, 11, 3))

piece("laundry_hamper", "Laundry Hamper", "Bathroom", [
    B("wicker", 3, 0, 3, 13, 12, 13), B("wicker", 2.5, 12, 2.5, 13.5, 13, 13.5),
    B("fab_white", 4, 13, 4, 12, 14, 12)])

piece("bath_mat", "Bath Mat", "Bathroom", [B("fab_blue", 2, 0, 3, 14, 1, 13)], col=False)

piece("bathroom_mirror", "Bathroom Mirror", "Bathroom", [
    B("chrome", 2, 4, 0, 14, 15, 1), B({"*": "mirror", "s": "@mirror"}, 3, 5, 1, 13, 14, 1.5),
    B("bulb", 3, 14.5, 1, 13, 15.5, 2)], col=False, sel=(2, 4, 0, 14, 15.5, 2), light=6)

# ------------------------------------------------------------------ home office
piece("desk", "Desk", "Home Office", [
    B("walnut", 0, 13, 1, 16, 15, 15), B("dark_wood", 0, 0, 2, 5, 13, 14),
    B({"*": "dark_wood", "s": "@drawers3"}, 0, 0, 13, 5, 13, 14),
    B("dark_wood", 14, 0, 2, 16, 13, 14), B("dark_wood", 5, 7, 13, 14, 12, 14)])

piece("office_chair", "Office Chair", "Home Office", [
    B("iron", 3, 0, 7, 13, 1, 9), B("iron", 7, 0, 3, 9, 1, 13),
    B("iron", 7.25, 1, 7.25, 8.75, 7, 8.75),
    B("fab_black", 3, 7, 3, 13, 10, 13), B("fab_black", 3, 10, 2, 13, 16, 4),
    B("iron", 2, 10, 4, 3, 11, 12), B("iron", 13, 10, 4, 14, 11, 12)],
    col=[(2, 0, 2, 14, 16, 13)])

piece("filing_cabinet", "Filing Cabinet", "Home Office", [
    B({"*": "steel", "s": "@filing_front"}, 2, 0, 2, 14, 16, 14)])

piece("desk_lamp", "Desk Lamp", "Home Office", [
    B("iron", 4, 0, 6, 10, 1, 10), B("iron", 6.5, 1, 7.5, 7.5, 8, 8.5),
    B("iron", 6.5, 7, 7.5, 12, 8, 8.5),
    B("lampshade", 10, 5, 6, 14, 8, 10)], col=[(4, 0, 6, 14, 8, 10)], light=10)

piece("laptop", "Laptop", "Home Office", [
    B("iron", 2, 0, 4, 14, 1, 14), B("iron", 4, 0.9, 6, 12, 1.1, 12),
    B({"*": "iron", "s": "@screen_on"}, 2, 1, 3, 14, 10, 4)], col=[(2, 0, 3, 14, 10, 14)])

piece("gaming_pc", "Gaming PC Tower", "Home Office", [
    B("iron", 4, 0, 3, 5, 1, 4), B("iron", 11, 0, 3, 12, 1, 4), B("iron", 4, 0, 14, 5, 1, 15), B("iron", 11, 0, 14, 12, 1, 15),
    B({"*": "iron", "s": "@pc_front", "top": "rgb_strip"}, 4, 1, 3, 12, 15, 15),
    B({"*": "pc_side"}, 12, 2, 4, 12.4, 14, 14),
    B("rgb_strip", 4, 14.5, 3.5, 12, 15, 4.5), B("iron", 6, 15, 6, 10, 15.4, 12)], light=7)

piece("gaming_desk", "Gaming Desk Setup", "Home Office", [
    B("iron", 0, 7, 1, 16, 8, 15), B("rgb_strip", 0, 6, 14.6, 16, 7, 15),
    B("iron", 0, 0, 1, 1, 7, 15), B("iron", 15, 0, 1, 16, 7, 15),
    B({"*": "iron", "s": "@pc_front", "top": "rgb_strip"}, 1.5, 0, 3, 7.5, 7, 14),
    B("mousepad", 2, 8, 7, 15, 8.2, 14),
    B("iron", 6.5, 8, 3, 9.5, 9, 6), B("iron", 7.3, 9, 4, 8.7, 11, 5),
    B({"*": "iron", "s": "@gaming_screen"}, 0.5, 10, 3, 15.5, 16, 4.2),
    B("rgb_strip", 0.5, 9.6, 3, 15.5, 10, 4.2),
    B({"*": "iron", "s": "@keyboard"}, 3, 8.2, 9.5, 11, 8.8, 13),
    B("iron", 12.5, 8.2, 10.5, 14, 8.9, 12.5), B("rgb_strip", 12.7, 8.9, 10.7, 13.8, 9.1, 11.2)],
    col=[(0, 0, 1, 16, 9, 15), (0.5, 9, 3, 15.5, 16, 4.2)], light=8)

piece("printer", "Printer", "Home Office", [
    B("porcelain", 1, 0, 2, 15, 6, 14), B("fab_white", 3, 6, 5, 13, 7, 12),
    B("iron", 3, 2, 13.5, 13, 3, 14.5), B("paint_green", 12, 4, 13.5, 13.5, 5, 14.5)])

# ------------------------------------------------------------------ laundry
piece("washer", "Washing Machine", "Laundry", [
    B({"*": "porcelain", "s": "@washer_front"}, 1, 0, 1, 15, 16, 15)])

piece("dryer", "Dryer", "Laundry", [
    B({"*": "porcelain", "s": "@dryer_front"}, 1, 0, 1, 15, 16, 15)])

piece("ironing_board", "Ironing Board", "Laundry", [
    B("fab_cream", 1, 11, 4, 15, 12, 12), B("fab_cream", 1, 11, 5, 3, 12, 11),
    B("iron", 3, 10, 5, 4, 11, 6), B("iron", 3, 10, 10, 4, 11, 11),
    B("iron", 3, 0, 4, 4, 10, 5), B("iron", 3, 0, 11, 4, 10, 12),
    B("iron", 11, 0, 4, 12, 10, 5), B("iron", 11, 0, 11, 12, 10, 12),
    B("iron", 3, 0, 4, 12, 1, 5), B("iron", 3, 0, 11, 12, 1, 12),
    B("paint_blue", 9, 12, 6, 14, 14, 10)], col=[(1, 0, 4, 15, 14, 12)])

# ------------------------------------------------------------------ entry / hall
piece("console_table", "Console Table", "Entry", [
    B("walnut", 0, 10, 4, 16, 12, 12), *legs("dark_wood", 0, 4, 16, 12, 10),
    B("dark_wood", 1, 3, 5, 15, 4, 11)])

piece("coat_rack", "Coat Rack", "Entry", [
    B("iron", 4, 0, 4, 12, 1, 12), B("dark_wood", 7.5, 1, 7.5, 8.5, 16, 8.5),
    B("brass", 5, 12, 7.5, 7.5, 13, 8.5), B("brass", 8.5, 12, 7.5, 11, 13, 8.5),
    B("brass", 7.5, 14, 5, 8.5, 15, 7.5), B("brass", 7.5, 14, 8.5, 8.5, 15, 11),
    B("fab_red", 9.5, 4, 6, 12, 12, 10), B("fab_navy", 4, 5, 6, 6.5, 12, 10)],
    col=[(4, 0, 4, 12, 16, 12)])

piece("shoe_rack", "Shoe Rack", "Entry", [
    B("oak", 1, 0, 3, 15, 1, 13), B("oak", 1, 5, 3, 15, 6, 13), B("oak", 1, 10, 3, 15, 11, 13),
    B("oak", 1, 0, 3, 2, 11, 13), B("oak", 14, 0, 3, 15, 11, 13),
    B("fab_black", 3, 1, 5, 7, 3, 11), B("fab_red", 8, 1, 5, 12, 3, 11),
    B("fab_navy", 3, 6, 5, 7, 8, 11), B("fab_cream", 8, 6, 5, 12, 8, 11),
    B("fab_brown", 4, 11, 5, 8, 13, 11)])

piece("umbrella_stand", "Umbrella Stand", "Entry", [
    B("iron", 4, 0, 4, 12, 9, 12), B("brass", 4, 9, 4, 12, 10, 12),
    B("fab_navy", 5, 9, 5, 7, 15, 7), B("fab_red", 9, 9, 8, 11, 14, 10), B("fab_black", 6, 9, 9, 8, 13, 11)],
    col=[(4, 0, 4, 12, 15, 12)])

piece("entry_bench", "Entry Bench", "Entry", [
    B("oak", 0, 7, 3, 16, 9, 13), B("fab_blue", 0, 9, 3, 16, 10, 13),
    B("oak", 0, 0, 3, 2, 7, 13), B("oak", 14, 0, 3, 16, 7, 13), B("oak", 2, 2, 3, 14, 3, 13)])

piece("floor_mirror", "Floor Mirror", "Entry", [
    B("oak", 3, 0, 2, 13, 16, 3.5), B({"*": "oak", "s": "@mirror"}, 4, 1, 3.5, 12, 15, 4),
    B("oak", 3, 0, 3.5, 4, 16, 5), B("oak", 12, 0, 3.5, 13, 16, 5)],
    col=[(3, 0, 2, 13, 16, 5)])

# ------------------------------------------------------------------ outdoor / patio
piece("bbq_grill", "BBQ Grill", "Patio", [
    *legs("iron", 3, 4, 13, 13, 6, 1),
    B("iron", 2, 6, 2, 14, 11, 14), B("embers", 3, 11, 3, 13, 11.5, 13),
    B("steel", 2, 11.5, 2, 14, 12, 14), B("chrome", 2, 12, 1, 14, 13, 2),
    B("iron", 14, 8, 6, 16, 9, 10), B("brass", 15, 8, 4, 16, 9, 6),
    B("iron", 2, 0.5, 12, 14, 1.5, 13)], col=[(2, 0, 1, 16, 13, 14)], light=6)

piece("patio_chair", "Patio Chair", "Patio", [
    *legs("white_wood", 2, 3, 14, 13, 7, 2),
    B("wicker", 2, 7, 3, 14, 8, 14), B("white_wood", 2, 8, 12, 4, 10, 14),
    B("white_wood", 12, 8, 12, 14, 10, 14),
    B("white_wood", 2, 8, 2, 14, 16, 4), B("fab_cream", 3, 8, 4, 13, 9, 13),
    B("white_wood", 2, 10, 4, 4, 11, 12), B("white_wood", 12, 10, 4, 14, 11, 12)],
    col=[(2, 0, 2, 14, 16, 14)])

piece("planter", "Planter Box", "Patio", [
    B("terracotta", 1, 0, 3, 15, 9, 13), B("soil", 2, 9, 4, 14, 10, 12),
    B("leaves", 2, 10, 4, 14, 14, 4.5), B("leaves", 2, 10, 11.5, 14, 14, 12),
    B("flowers_red", 2, 10, 8, 14, 16, 8.5), B("flowers_yellow", 8, 10, 4, 8.5, 16, 12),
    B("leaves", 4, 10, 4, 12, 13, 12)])

piece("patio_table", "Patio Table", "Patio", [
    B("glass", 0, 11, 0, 16, 12, 16), B("iron", 0, 10, 0, 16, 11, 1), B("iron", 0, 10, 15, 16, 11, 16),
    B("iron", 0, 10, 1, 1, 11, 15), B("iron", 15, 10, 1, 16, 11, 15),
    B("iron", 7, 1, 7, 9, 10, 9), B("iron", 3, 0, 3, 13, 1, 13)])

piece("patio_umbrella", "Patio Umbrella", "Patio", [
    B("concrete", 3, 0, 3, 13, 2, 13), B("iron", 7.5, 2, 7.5, 8.5, 14, 8.5),
    B({"*": "awning"}, 1, 14, 1, 15, 15, 15), B("awning", 4, 15, 4, 12, 16, 12)],
    col=[(3, 0, 3, 13, 16, 13)])

piece("garden_bench", "Garden Bench", "Patio", [
    *[B("oak", 0, 8, z, 16, 9, z + 2.5) for z in (3, 6, 9)],
    B("oak", 0, 9, 2, 16, 10, 4.5), B("oak", 0, 12, 2, 16, 13.5, 4), B("oak", 0, 15, 2, 16, 16, 4),
    B("iron", 1, 0, 3, 3, 8, 12), B("iron", 13, 0, 3, 15, 8, 12), B("iron", 1, 9, 2, 3, 16, 4), B("iron", 13, 9, 2, 15, 16, 4)],
    col=[(0, 0, 2, 16, 16, 12)])

piece("fire_pit", "Fire Pit", "Patio", [
    B("stone", 1, 0, 1, 15, 5, 3), B("stone", 1, 0, 13, 15, 5, 15),
    B("stone", 1, 0, 3, 3, 5, 13), B("stone", 13, 0, 3, 15, 5, 13),
    B("embers", 3, 1, 3, 13, 2, 13), B("charcoal", 4, 2, 4, 12, 3, 12),
    B("fire", 4, 3, 8, 12, 12, 8.5), B("fire", 8, 3, 4, 8.5, 12, 12)], col=[(1, 0, 1, 15, 5, 15)], light=15)

piece("mailbox", "Mailbox", "Patio", [
    B("dark_wood", 7, 0, 7, 9, 9, 9), B("mail_blue", 3, 9, 4, 13, 14, 12), B("mail_blue", 4, 14, 5, 12, 15, 11),
    B("paint_red", 12.5, 12, 5, 13.5, 16, 6)], col=[(3, 0, 4, 13, 15, 12)])
