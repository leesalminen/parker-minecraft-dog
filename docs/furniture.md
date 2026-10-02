# Galaxy Home furniture

84 placeable furniture blocks (`gx:furn_<id>`) with custom geometry, in the creative inventory under Construction > **Galaxy Home**. Creative-only (no recipes).

## How it works

- Piece definitions: `tools/furniture/pieces.py` (boxes in pixel coordinates, front = south face). Materials/textures: `tools/furniture/materials.py` (procedural 32x32 tiles).
- Generator: `python3 tools/furniture/build_furniture.py` (`--check` validates, `--preview out.png` renders a front-view contact sheet). It also runs from `python3 tools/creatures/build_all.py` through `tools/creatures/extras/furniture.py`, which is what adds names to `en_US.lang`.
- Output: `BP/blocks/gx_furn_*.json`, `RP/models/blocks/gx_furn_*.geo.json`, `RP/textures/blocks/gx_furn/*.png`, and `gx_furn_*` keys merged into `RP/textures/terrain_texture.json` (other keys preserved).
- Blocks use format_version 1.21.0, `minecraft:geometry`, per-face `material_instances` (opaque, alpha_test for leaves/fire, blend for glass/water), `minecraft:placement_direction` (cardinal_direction) with one permutation per facing that rotates the model and its collision/selection boxes. Fronts face the player.
- Collision: one box per piece (union of the listed boxes); rugs, mats, paintings, curtains, chandelier and wall pieces are walk-through. Lamps, fireplace, fire pit, chandelier etc. emit light.
- Multi-block layouts: sofas chain (`sofa_left` + `sofa_mid` + `sofa_right`), beds pair head + foot pieces side by side, counters/islands line up.
- Not implemented: sitting on chairs/sofas (no seat entity; the pinned @minecraft/server 1.11 has no stable block-interact event), recipes, block sounds.

## Pieces

**Living Room** (21): Sofa (`sofa`), Sofa Middle Seat (`sofa_mid`), Sofa Left End (`sofa_left`), Sofa Right End (`sofa_right`), Leather Sofa (`sofa_leather`), Cream Sofa (`sofa_cream`), Armchair (`armchair`), Coffee Table (`coffee_table`), Side Table (`side_table`), Table Lamp (`table_lamp`), TV Stand (`tv_stand`), Television (`tv`), TV on Stand (`tv_unit`), Bookshelf (`bookshelf`), Floor Lamp (`floor_lamp`), Red Rug (`rug`), Blue Rug (`rug_blue`), Fireplace (`fireplace`), Curtains (`curtain`), Painting (`painting`), Houseplant (`houseplant`)

**Kitchen** (11): Kitchen Counter (`kitchen_counter`), Kitchen Sink (`kitchen_sink`), Stove (`stove`), Refrigerator (`fridge`), Kitchen Island (`kitchen_island`), Upper Cabinet (`upper_cabinet`), Kitchen Table (`kitchen_table`), Bar Stool (`kitchen_stool`), Microwave (`microwave`), Range Hood (`range_hood`), Fruit Bowl (`fruit_bowl`)

**Dining Room** (5): Dining Table (`dining_table`), Dining Chair (`dining_chair`), China Cabinet (`china_cabinet`), Chandelier (`chandelier`), Sideboard (`sideboard`)

**Master Bedroom** (8): Double Bed (Head) (`double_bed`), Double Bed (Foot) (`double_bed_foot`), Nightstand (`nightstand`), Dresser (`dresser`), Wardrobe (`wardrobe`), Vanity with Mirror (`vanity_mirror`), Vanity Stool (`vanity_stool`), Ottoman (`ottoman`)

**Kids Room** (6): Bunk Bed (`bunk_bed`), Toy Chest (`toy_chest`), Kids Desk (`kids_desk`), Play Mat (`play_mat`), Teddy Bear (`teddy_bear`), Toy Blocks (`toy_blocks`)

**Bathroom** (8): Toilet (`toilet`), Bathroom Sink Vanity (`bathroom_sink`), Bathtub (`bathtub`), Shower Stall (`shower`), Towel Rack (`towel_rack`), Laundry Hamper (`laundry_hamper`), Bath Mat (`bath_mat`), Bathroom Mirror (`bathroom_mirror`)

**Home Office** (8): Desk (`desk`), Office Chair (`office_chair`), Filing Cabinet (`filing_cabinet`), Desk Lamp (`desk_lamp`), Laptop (`laptop`), Printer (`printer`), Gaming PC Tower (`gaming_pc`), Gaming Desk Setup (`gaming_desk`)

**Laundry** (3): Washing Machine (`washer`), Dryer (`dryer`), Ironing Board (`ironing_board`)

**Entry** (6): Console Table (`console_table`), Coat Rack (`coat_rack`), Shoe Rack (`shoe_rack`), Umbrella Stand (`umbrella_stand`), Entry Bench (`entry_bench`), Floor Mirror (`floor_mirror`)

**Patio** (8): BBQ Grill (`bbq_grill`), Patio Chair (`patio_chair`), Planter Box (`planter`), Patio Table (`patio_table`), Patio Umbrella (`patio_umbrella`), Garden Bench (`garden_bench`), Fire Pit (`fire_pit`), Mailbox (`mailbox`)
