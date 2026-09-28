"""Family 8: Sonic, Missile, Drone (kinetic / support, white-green-blue). Weapons 42-45.

Def schema (see docs/weapons/archetypes.md):
  id, name, family, tier, archetype, scope, zoom, dot, dps, ammo, heat, palette, shape,
  sound, params, hooks, vfx{six layers}, model, recipe, twist, hud, cooldown?, description?

Deviations (see docs/weapons/DEVIATIONS.md):
  * sonic_cannon — the spec's "hits arrive delayed by distance" is dropped: the cone
    archetype damages every mob in the cone on the release tick.  The expanding arc
    particles give the wave its visual speed, but there is no per-distance hit delay.
  * seeker_rack — the spec's "lock + rangefinder" is expressed as `scope: lock`; the
    engine's rangefinder readout is bound to the scope4/scope8/rangefinder scopes
    (engine/scope.js), so a lock reticle cannot also show the distance.
"""

WEAPONS = [
    {
        "id": "sonic_cannon",
        "name": "Sonic Cannon",
        "description": "Charge a 45-degree shockwave that stuns mobs and shatters glass.",
        "family": "support", "tier": "rare", "archetype": "cone", "dps": 14,
        "scope": "iron", "zoom": 1.0,
        "dot": {"style": "dot", "color": "#6fe0d0", "range": 20},
        "ammo": {"type": "heat"}, "heat": None, "hud": {"kind": "charge"},
        "palette": {"name": "support_sonic", "core": "#f4fffb", "glow": "#6fe0d0",
                    "trail": "#1f7a6e", "accent": "#bff2e8"},
        "shape": {"projectile": "plume", "muzzle": "horn"},
        "sound": [["beacon.activate", 0.7, 0.8, 0], ["random.explode", 0.6, 1.5, 1]],
        "params": {"range": 15, "angle": 45, "dps": 10, "charge": True, "hold_ticks": 20,
                   "charge_mult": 0.5, "knockback": 1.4, "heat_rate": 0,
                   "particle_size": 0.6, "muzzle_size": 0.8,
                   "grief": {"radius": 5, "from": ["minecraft:glass", "minecraft:glass_pane"],
                             "to": "minecraft:air", "cap": 12}},
        "hooks": {"on_hit": [{"status": "slowness", "ticks": 30, "amp": 4},
                             {"stun": 30},
                             {"vfx": "gx:ring_wave", "size": 1.2, "life": 0.4}],
                  "on_tick": []},
        "vfx": {"idle": "gx:swirl", "charge": "gx:swirl", "muzzle": "gx:orb_plume",
                "body": "gx:ring_wave", "impact": "gx:shock_disc", "screen": "vignette_whiteout"},
        "model": {"form": "cannon", "len": 14, "metal": "#5a6a70"},
        "recipe": {"ingredients": ["gx:energy_cell", "minecraft:iron_ingot",
                                   "minecraft:amethyst_shard", "minecraft:echo_shard"]},
        "twist": "Charge and release: concentric arcs ripple out, stun mobs 1.5 s and shove "
                 "them back, and shatter glass in the cone (mobGriefing, cap 12).",
        "custom": None,
    },
    {
        "id": "seeker_rack",
        "name": "Seeker Missile Rack",
        "description": "Lock up to four targets, then ripple-fire four homing missiles.",
        "family": "support", "tier": "epic", "archetype": "lob", "dps": 22,
        "scope": "lock", "zoom": 4.0,
        "dot": {"style": "dot_cross", "color": "#ff5a4a", "range": 60},
        "ammo": {"type": "cell", "mag": 4}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "support_seeker", "core": "#fff4e6", "glow": "#8fd0ff",
                    "trail": "#5a6a78", "accent": "#ffb066"},
        "shape": {"projectile": "dart", "muzzle": "rack"},
        "sound": [["crossbow.shoot", 0.8, 1.2, 0], ["mob.ghast.shoot", 0.6, 1.4, 2]],
        "params": {"speed": 20, "gravity": 0.08, "aoe": 2, "damage": 8, "homing": 6,
                   "homing_turn": 0.4, "lifetime": 60, "rate": 20, "count": 1, "spread": 0,
                   "size": 0.45, "muzzle_size": 0.6, "max_locks": 4, "lock_ticks": 12,
                   "fire_gap": 4, "arc_ticks": 10, "arc_lift": 0.5},
        "hooks": {"on_hit": [{"vfx": "gx:smoke_trail", "size": 0.5, "life": 0.5, "count": 3}],
                  "on_tick": []},
        "vfx": {"idle": "gx:smoke_trail", "charge": "gx:swirl", "muzzle": "gx:muzzle_flash",
                "body": "gx:orb_dart", "impact": "gx:star_flash", "screen": "scope_lock"},
        "model": {"form": "rack", "tubes": 4, "metal": "#4a5a66"},
        "recipe": {"ingredients": ["gx:energy_cell", "minecraft:iron_ingot",
                                   "minecraft:gunpowder", "minecraft:copper_ingot"]},
        "twist": "Hold aim to bank a lock every 0.6 s (up to four), then release to "
                 "ripple-fire that many missiles that arc up, dive, and detonate on a wall "
                 "instead of dudding.",
        "custom": "seeker_rack",
    },
    {
        "id": "drone_launcher",
        "name": "Combat Drone Launcher",
        "description": "Launches a hovering drone that orbits you and lasers hostiles.",
        "family": "support", "tier": "epic", "archetype": "deploy", "dps": 22,
        "scope": "holo", "zoom": 1.5,
        "dot": {"style": "dot", "color": "#5ab4ff", "range": 12},
        "ammo": {"type": "cell", "mag": 2}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "support_drone", "core": "#eaf6ff", "glow": "#5ab4ff",
                    "trail": "#1f4a7a", "accent": "#a8d8ff"},
        "shape": {"projectile": "disc", "muzzle": "tube"},
        "sound": [["beacon.activate", 0.6, 1.4, 0], ["mob.irongolem.hit", 0.4, 1.6, 2]],
        "params": {"entity": "gx:combat_drone", "hover": True, "cap": 2, "duration": 20,
                   "dps": 6, "range": 12, "interval": 10, "rate": 30, "place_range": 8},
        "hooks": {"on_hit": [], "on_tick": []},
        "vfx": {"idle": "gx:field_glow", "charge": "gx:swirl", "muzzle": "gx:orb_disc",
                "body": "gx:beam_bar", "impact": "gx:spark_burst", "screen": "marker_hit"},
        "model": {"form": "launcher", "len": 14, "metal": "#3f5a72"},
        "recipe": {"ingredients": ["gx:energy_cell", "minecraft:iron_ingot",
                                   "minecraft:redstone", "minecraft:amethyst_shard"]},
        "twist": "The drone orbits you for 20 s, shoots hostiles within 12 blocks (max two "
                 "up), docks at the end of its timer and refunds a cell if it survived; "
                 "the aim dot orders it to focus a mob.",
        "custom": None,
    },
    {
        "id": "sentinel_kit",
        "name": "Sentinel Turret Kit",
        "description": "Unfolds a 30 s auto-turret; synced turrets deal bonus damage.",
        "family": "support", "tier": "epic", "archetype": "deploy", "dps": 22,
        "scope": "iron", "zoom": 1.0,
        "dot": {"style": "dot", "color": "#6aff9a", "range": 16},
        "ammo": {"type": "cell", "mag": 2}, "heat": None, "hud": {"kind": "ammo"},
        "palette": {"name": "support_sentinel", "core": "#eaffef", "glow": "#6aff9a",
                    "trail": "#1f6a3a", "accent": "#aaffc8"},
        "shape": {"projectile": "hex", "muzzle": "case"},
        "sound": [["beacon.activate", 0.6, 1.1, 0], ["mob.irongolem.hit", 0.5, 1.3, 2]],
        "params": {"entity": "gx:sentinel_turret", "cap": 2, "duration": 30, "dps": 8,
                   "range": 16, "place_range": 6, "interval": 10, "rate": 30,
                   "sync_range": 16, "sync_mult": 0.25},
        "hooks": {"on_hit": [], "on_tick": []},
        "vfx": {"idle": "gx:field_glow", "charge": "gx:swirl", "muzzle": "gx:orb_hex",
                "body": "gx:beam_bar", "impact": "gx:spark_burst", "screen": "marker_hit"},
        "model": {"form": "kit", "metal": "#4a6a52"},
        "recipe": {"ingredients": ["gx:energy_cell", "minecraft:iron_ingot",
                                   "minecraft:redstone", "minecraft:emerald"]},
        "twist": "A turret that shares its 16-block line of sight with another of yours "
                 "deals +25% damage while both stand; never targets pups, tamed mobs or "
                 "players.",
        "custom": "sentinel_kit",
    },
]
