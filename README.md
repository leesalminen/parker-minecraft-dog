# Galaxy Pup + Galaxy Forge

Minecraft Bedrock add-ons. **Galaxy Pup** is a custom tameable dog. **Galaxy Forge** adds
creatures, mechs, tanks and 73 script-driven weapons: sci-fi blasters, nerf blasters and
realistic firearms and launchers with scope zoom, recoil and synthesized gunshots. See
`docs/weapons/` for the weapon engine and roster.

**Install:** download the `.mcaddon` files from the latest
[release](../../releases) and open them with Minecraft. Or build them yourself:
`python3 tools/creatures/build_all.py && python3 tools/build.py`
(needs Python 3 and ffmpeg), which writes them to `dist/`.

**Galaxy Home:** 80+ furniture blocks for a whole house, see `docs/furniture.md` (`python3 tools/furniture/build_furniture.py`).

## Galaxy Pup

A custom Minecraft Bedrock creature (`galaxy:pup`), not a wolf reskin: its own geometry, texture, animations, and behavior.

## What it does

- Spawn egg ("Galaxy Pup Spawn Egg" in the creative inventory), plus rare natural spawns in plains, meadow, and forest biomes.
- Follows a player who is holding a **Galaxy Treat**, and begs (tilts its head) at treats and bones.
- To tame it, feed it a Galaxy Treat or a bone. Each feed has a 34% chance to work. Once tamed, it follows its owner, gets 30 HP, and never despawns.
- To make it sit or stand, interact with it as the owner. Feeding it treats heals it.
- **Galaxy Treat** recipe: bone + sugar makes 2 (shapeless, crafting table).
- Animations: walk cycle, sit, tail wag (faster when tamed), and a head tilt every few seconds.
- Sounds are the vanilla wolf sounds at a higher pitch (1.3–1.6, set in `sounds.json`).
- Size: adult proportions, about 1.5 blocks tall (about 1.7 with the ears), hitbox 0.8 × 1.5. It won't fit through 1-block gaps.

## Layout

```
packs/GalaxyPup_BP/   behavior: entity logic, treat item, recipe, spawn rules
packs/GalaxyPup_RP/   resources: client entity, geometry, animations, textures, sounds
tools/gen_textures.py seeds the starting textures/icons (won't overwrite without --force)
tools/build.py        validates JSON + manifest links, writes dist/GalaxyPup.mcaddon
```

## Editing the model and painting it (Blockbench)

In Blockbench, use File → Open Model and pick `packs/GalaxyPup_RP/models/entity/galaxy_pup.geo.json`. Then drag `textures/entity/galaxy_pup.png` onto the model. Blockbench saves straight back to those two files. After you paint in Blockbench, the PNG is the source of truth, so never run `gen_textures.py --force` again.

The texture uses box UV (64×64). The pup faces **-Z**. Keep the bone names `head`, `body`, `tail`, and `leg0` through `leg3`, because the animations target them by name. `leg0` and `leg1` are the front legs. Leg pivots sit at the top of each leg (y = 11), so you can change leg length without touching the animations, but the sit pose in `galaxy_pup.animation.json` (body -35°, back legs -90°) assumes roughly the current proportions.

## Build

```
python3 tools/build.py      # -> dist/GalaxyPup.mcaddon
```

Before you change a pack and ship it again, raise `version` in **both** manifests. Otherwise Realms and consoles keep the copy they already downloaded.

## Getting it onto the PS5

The PlayStation can't import packs. The world has to bring them along.

1. On the Windows PC, double-click `GalaxyPup.mcaddon`. Minecraft imports both packs.
2. Create a world. Under Behavior Packs, turn on Galaxy Pup (the resource pack switches on with it).
3. **To test on the PS5:** host the world on the PC and join it from the PS5 as an Xbox-account friend. The packs download to the console when it joins. No Realm is needed.
4. **So it's playable when the PC is off:** upload the world to a Realm from the PC (Realm settings → Replace World). Then open the Realm on the PS5.

To iterate faster on the PC: copy the two pack folders into `development_behavior_packs` and `development_resource_packs`. Minecraft re-reads them every time you load a world, so you don't have to re-import. Where these folders live depends on the version:
- Newer (GDK) versions: `%APPDATA%\Minecraft Bedrock\Users\Shared\games\com.mojang\`
- Older (UWP) versions: `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\`
