# Giant armor

12 armor sets (48 pieces) crafted at the **Armor Forge**, a big crafting table. Wear all four pieces of one set and you grow, get buffs, and can run through mobs to smash them.

## Crafting

- **Armor Forge** (Construction tab): iron ingot x5, crafting table, stone x3 (`III / ICI / SSS`) at a normal crafting table.
- Armor recipes only work at the Armor Forge (3x3 grid, `gx_armor_forge` tag). Vanilla shapes: helmet 5, chestplate 8, leggings 7, boots 4 of the material; sets with a core ingredient use it in the gap of every piece.

## What a full set does

Size, buffs (refreshed every 0.5 s, removed when you take the set off), **sprint ram** (sprint into mobs: damage + knockback + perk), **stomp** (landing from a jump/fall; sets with stomp damage), and a **melee perk** (frost slows, magma ignites, storm strikes lightning, ender launches). Players, villagers, tamed pets and ridden mobs are never hit.

| Set | Size | Materials | Buffs | Ram | Stomp | Perk |
|---|---|---|---|---|---|---|
| Ogre Hide | 1.4x | leather | strength 1, speed 1 | 8 | - | - |
| Copper Colossus | 1.6x | copper_ingot | strength 1, speed 1, resistance 1 | 10 | - | - |
| Iron Giant | 1.8x | iron_ingot | strength 2, speed 1, resistance 1 | 12 | - | - |
| Gold Goliath | 1.8x | gold_ingot | strength 2, speed 3, haste 2 | 12 | - | - |
| Frost Giant | 2.0x | blue_ice | strength 2, speed 2, resistance 2 | 14 | - | frost |
| Magma Titan | 2.2x | blaze_rod + magma_cream | strength 3, speed 2, resistance 2, fire_resistance 1 | 16 | - | fire |
| Storm Giant | 2.4x | lapis_lazuli + lightning_rod | strength 3, speed 3, resistance 2 | 16 | - | lightning |
| Ender Colossus | 2.4x | ender_pearl + ender_eye | strength 3, speed 3, jump_boost 3, slow_falling 1 | 16 | - | launch |
| Emerald Behemoth | 2.2x | emerald | strength 3, speed 2, resistance 2, regeneration 1 | 15 | - | - |
| Diamond Behemoth | 2.8x | diamond | strength 4, speed 2, resistance 3, health_boost 3 | 20 | 14 | - |
| Netherite Juggernaut | 3.2x | netherite_scrap + netherite_ingot | strength 4, speed 2, resistance 4, fire_resistance 1, health_boost 5 | 26 | 20 | - |
| Cosmic Kaiju | 4.0x | amethyst_shard + nether_star | strength 6, speed 3, resistance 4, fire_resistance 1, regeneration 2, health_boost 10, jump_boost 3 | 40 | 30 | - |

## How it works

- Generator: `tools/creatures/extras/giant_armor.py` (runs from `build_all.py`). Edit `SETS` to retune; everything regenerates.
- Size: `entities/player.json` is a **full override of the vanilla player** (`tools/creatures/extras/player_base.json`, format 1.21.0, sulfur-cube knockback rules removed). `gx:size_*` events add a `minecraft:scale` + `minecraft:collision_box` component group. Only one behavior pack can override the player, so this conflicts with any other pack that does.
- Behavior: `scripts/giants.js` with data from `scripts/generated/giants.js`.
- Ram damage values are HP (20 = a full player bar).

## Matching weapons

One signature weapon per set (crafted at the Armor Forge: 6 of the set material + 1 stick, the core ingredient replaces the top-middle slot). Held as a 2D icon like the lightsabers, `minecraft:is_sword`, repaired with the set material. Hitting with it applies the set's perk (frost / fire / lightning / launch) even without the armor; sets with no perk get **bash** (big knockback), **sunder** (weakness), **cleave** (6 dmg to mobs within 3 blocks of the target) or **wither**.

| Set | Weapon | Damage | Perk |
|---|---|---|---|
| Ogre Hide | Ogre Club | 7 | bash |
| Copper Colossus | Copper Maul | 8 | sunder |
| Iron Giant | Iron Greatsword | 9 | - |
| Gold Goliath | Gilded Battleaxe | 9 | - |
| Frost Giant | Glacier Greatsword | 11 | frost |
| Magma Titan | Magma Cleaver | 12 | fire |
| Storm Giant | Stormspear | 12 | lightning |
| Ender Colossus | Void Reaver | 12 | launch |
| Emerald Behemoth | Emerald Halberd | 11 | cleave |
| Diamond Behemoth | Diamond Claymore | 14 | cleave |
| Netherite Juggernaut | Juggernaut Maul | 18 | wither |
| Cosmic Kaiju | Kaiju Cleaver | 28 | cleave |

Edit `WEAPONS` in `giant_armor.py` to retune.
