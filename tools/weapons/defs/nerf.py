"""Family 10: Nerf (foam blasters). Weapons 51-53.

Toy-tier bolts: arcing foam darts that bump mobs back, barely hurt, and stick to walls for a
few seconds.

Def schema (see docs/weapons/archetypes.md):
  id, name, family, tier, archetype, scope, zoom, dot, dps, ammo, heat, palette, shape,
  sound, params, hooks, vfx{six layers}, model, recipe, twist, hud, cooldown?, description?
"""

def _on_hit(push):
    return {"on_hit": [{"knockback": push, "dir": "away"},
                       {"vfx": "gx:star_flash", "size": 0.3, "life": 0.15, "count": 1}],
            "on_tick": []}


WEAPONS = [
    {
        "id": "foam_popper",
        "name": "Foam Popper",
        "description": "Foam dart pistol. Hold to rapid-fire; darts arc, bonk mobs back, and stick to walls.",
        "family": "nerf", "tier": "toy", "archetype": "bolt", "dps": 3,
        "scope": "iron", "zoom": 1.0,
        "dot": {"style": "dot", "color": "#ff7a1a", "range": 24},
        "ammo": {"type": "cell", "mag": 6}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "nerf_popper", "core": "#fff4e0", "glow": "#ff7a1a",
                    "trail": "#ffb070", "accent": "#2f6fd6"},
        "shape": {"projectile": "dart", "muzzle": "pop"},
        "sound": [["random.pop", 0.7, 1.6, 0], ["random.bow", 0.3, 1.9, 0]],
        "params": {"speed": 26, "gravity": 0.5, "lifetime": 80, "rate": 8, "damage": 2,
                   "count": 1, "size": 0.3, "muzzle_size": 0.25, "stick": True},
        "hooks": _on_hit(0.35),
        "vfx": {"idle": "gx:orb_dart", "charge": "gx:swirl", "muzzle": "gx:smoke_trail",
                "body": "gx:orb_dart", "impact": "gx:star_flash", "screen": "marker_hit"},
        "model": {"form": "pistol", "tall": 3, "metal": "#ff7a1a", "grip": "#2f6fd6"},
        "recipe": {"ingredients": ["minecraft:orange_dye", "minecraft:blue_dye",
                                   "minecraft:stick", "minecraft:slime_ball"]},
        "twist": "Foam darts arc like the real thing and stay stuck to walls for a few seconds.",
        "custom": None,
    },
    {
        "id": "foam_longshot",
        "name": "Foam Longshot",
        "description": "Scoped foam rifle. Fast, flat darts that knock mobs back hard.",
        "family": "nerf", "tier": "toy", "archetype": "bolt", "dps": 3.5,
        "scope": "scope4", "zoom": 4.0,
        "dot": {"style": "dot_cross", "color": "#2f6fd6", "range": 48},
        "ammo": {"type": "cell", "mag": 10}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "nerf_longshot", "core": "#f0f6ff", "glow": "#ff7a1a",
                    "trail": "#8fb8ff", "accent": "#ffd23a"},
        "shape": {"projectile": "needle", "muzzle": "crack"},
        "sound": [["random.bow", 0.6, 1.3, 0], ["random.click", 0.4, 1.5, 3]],
        "params": {"speed": 42, "gravity": 0.25, "lifetime": 80, "rate": 16, "damage": 3,
                   "count": 1, "size": 0.3, "muzzle_size": 0.3, "stick": True},
        "hooks": _on_hit(0.7),
        "vfx": {"idle": "gx:orb_needle", "charge": "gx:swirl", "muzzle": "gx:smoke_trail",
                "body": "gx:orb_needle", "impact": "gx:star_flash", "screen": "marker_hit"},
        "model": {"form": "rifle", "len": 22, "thick": 3, "tall": 3, "scope": True,
                  "metal": "#2f6fd6", "grip": "#ff7a1a"},
        "recipe": {"ingredients": ["minecraft:blue_dye", "minecraft:orange_dye",
                                   "minecraft:stick", "minecraft:string", "minecraft:glass_pane"]},
        "twist": "Sneak for the 4x scope; the heavier dart shoves mobs a couple of blocks back.",
        "custom": None,
    },
    {
        "id": "foam_storm",
        "name": "Foam Storm",
        "description": "Six-barrel foam blaster. Every shot sprays a volley of six darts.",
        "family": "nerf", "tier": "toy", "archetype": "bolt", "dps": 3,
        "scope": "holo", "zoom": 1.5,
        "dot": {"style": "dot_ring", "color": "#ffd23a", "range": 20},
        "ammo": {"type": "cell", "mag": 5}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "nerf_storm", "core": "#fffbe0", "glow": "#ffd23a",
                    "trail": "#ff7a1a", "accent": "#2f6fd6"},
        "shape": {"projectile": "droplet", "muzzle": "volley"},
        "sound": [["random.pop", 0.6, 1.4, 0], ["random.pop", 0.5, 1.6, 1],
                  ["random.pop", 0.5, 1.8, 2], ["random.bow", 0.4, 1.5, 0]],
        "params": {"speed": 24, "gravity": 0.5, "lifetime": 70, "rate": 40, "damage": 1,
                   "count": 6, "spread": 7, "size": 0.28, "muzzle_size": 0.45, "stick": True},
        "hooks": _on_hit(0.25),
        "vfx": {"idle": "gx:orb_droplet", "charge": "gx:swirl", "muzzle": "gx:smoke_trail",
                "body": "gx:orb_droplet", "impact": "gx:star_flash", "screen": "marker_hit"},
        "model": {"form": "rack", "tubes": 6, "metal": "#ffd23a", "grip": "#2f6fd6"},
        "recipe": {"ingredients": ["minecraft:yellow_dye", "minecraft:blue_dye",
                                   "minecraft:stick", "minecraft:slime_ball", "minecraft:string"]},
        "twist": "Six darts per pull in a loose spread: hard to miss, and each one bonks.",
        "custom": None,
    },
]
