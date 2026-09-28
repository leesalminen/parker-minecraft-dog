"""Family 11: Military (realistic firearms and launchers). Weapons 54-73.

Real-world proportions and behaviour: high-detail models (hd_models.py), synthesised
gunshots (sounds.py), real FOV zoom on scoped weapons, camera-shake recoil, ejected brass,
bullet spread, burst / bolt / pump / full-auto cadences (fire_mode keeps each weapon's own
rate instead of the global rapid-fire clamp), i-frame-aware damage, and explosive
launchers that leave craters when mobGriefing is on.

dps below is the honest sustained number: damage * pellets * burst * 20 / rate.
"""

PAL = {"core": "#fff3c4", "glow": "#ffae42", "trail": "#8e8e8e", "accent": "#c9a24a"}

BULLET_VFX = {"idle": "gx:smoke_trail", "charge": "gx:swirl", "muzzle": "gx:muzzle_flash",
              "body": "gx:orb_needle", "impact": "gx:debris_burst", "screen": "marker_hit"}
ROCKET_VFX = {"idle": "gx:smoke_trail", "charge": "gx:swirl", "muzzle": "gx:muzzle_flash",
              "body": "gx:orb_plume", "impact": "gx:ring_wave", "screen": "marker_hit",
              "trail": "gx:smoke_trail"}


def hit(knock=0.0):
    fx = [{"vfx": "gx:spark_burst", "size": 0.25, "life": 0.25, "count": 3, "speed": 1.2}]
    if knock:
        fx.insert(0, {"knockback": knock, "dir": "away"})
    return {"on_hit": fx, "on_tick": []}


def weapon(wid, name, desc, tier, arch, dps, mode, scope, zoom, proj, muzzle, sound, params,
           model, ingredients, twist, knock=0.0, move=0.9, vfx=None):
    return {
        "id": wid, "name": name, "description": desc,
        "family": "military", "tier": tier, "archetype": arch, "dps": dps,
        "fire_mode": mode, "scope": scope, "zoom": zoom,
        "dot": {"style": "dot", "color": "#ff2a1a", "range": params.get("range", 64), "show": False},
        "ammo": {"type": "mag", "mag": params.pop("mag", 30)}, "heat": None, "hud": {"kind": "mode"},
        "palette": dict(PAL, name=f"mil_{wid}"),
        "shape": {"projectile": proj, "muzzle": muzzle},
        "sound": sound, "params": params, "hooks": hit(knock),
        "vfx": vfx or BULLET_VFX, "model": model, "move_mod": move,
        "recipe": {"ingredients": ingredients}, "twist": twist, "custom": None,
    }


def shot(kind, extra=None):
    """Report + brass (+ an optional mechanical cycle [(sound, delay)])."""
    s = [[f"gx.gun.{kind}", 1.0, 1.0, 0], ["gx.gun.brass", 0.35, 1.0, 5]]
    for snd, delay in extra or []:
        s.append([f"gx.gun.{snd}", 0.8, 1.0, delay])
    return s


def bullet(damage, rate, rng, spread, recoil, **kw):
    p = {"damage": damage, "rate": rate, "range": rng, "spread": spread, "recoil": recoil,
         "shell": True, "tracer_every": 1, "tracer_size": 0.07, "tracer_life": 0.06,
         "muzzle_size": 0.35, "impact_size": 0.25, "falloff": 0.8, "smoke": True}
    p.update(kw)
    return p


IRON, WOOD, STEEL = "minecraft:iron_ingot", "minecraft:oak_planks", "minecraft:iron_block"
POWDER, FLINT, STRING = "minecraft:gunpowder", "minecraft:flint", "minecraft:string"
GLASS, COPPER, TNT = "minecraft:glass_pane", "minecraft:copper_ingot", "minecraft:tnt"
DARK = "minecraft:dark_oak_planks"

WEAPONS = [
    # ---------------------------------------------------------------- sidearms
    weapon("m9_pistol", "M9 Service Pistol",
           "9mm semi-automatic sidearm. Hold to fire as fast as the slide cycles.",
           "rare", "hitscan", 16, "semi", "iron", 1.0, "9mm", "compact",
           shot("pistol"), bullet(4, 5, 50, 1.2, 0.05, mag=15, headshot_mult=1.5),
           {"form": "pistol"}, [IRON, IRON, POWDER, "minecraft:black_dye"],
           "Light recoil and fast follow-ups; headshots deal 1.5x.", move=1.0),
    weapon("magnum_44", ".44 Magnum Revolver",
           "Six-shot stainless revolver. Slow, loud, and hits like a truck.",
           "epic", "hitscan", 20, "semi", "iron", 1.0, "44mag", "revolver_gap",
           shot("magnum"), bullet(14, 14, 60, 0.6, 0.18, mag=6, headshot_mult=2.0, shell=False),
           {"form": "revolver", "barrel": 16}, [IRON, IRON, POWDER, POWDER, "minecraft:bone"],
           "Heavy kick and knockback; headshots deal double.", knock=0.5, move=1.0),

    # ---------------------------------------------------------------- SMGs
    weapon("mp5_smg", "MP5 Submachine Gun",
           "Roller-delayed 9mm SMG. Smooth, accurate full auto.",
           "epic", "hitscan", 25, "auto", "iron", 1.0, "9mm_para", "tri_lug",
           shot("smg"), bullet(2.5, 2, 45, 1.8, 0.04, mag=30, tracer_every=3),
           {"form": "smg"}, [IRON, IRON, POWDER, POWDER, "minecraft:black_dye"],
           "600 rpm with very little climb; best hip-fire in the family.", move=1.0),
    weapon("thompson_m1928", "Thompson M1928",
           "The Chicago typewriter: .45 ACP, 50-round drum, walnut furniture.",
           "mythic", "hitscan", 30, "auto", "iron", 1.0, "45acp", "cutts",
           shot("smg"), bullet(3, 2, 40, 2.6, 0.06, mag=50, tracer_every=3),
           {"form": "tommy"}, [IRON, IRON, WOOD, WOOD, POWDER, POWDER],
           "Big drum, heavy hitter, wide spray: get close.", move=0.95),

    # ---------------------------------------------------------------- rifles
    weapon("m4a1_carbine", "M4A1 Carbine",
           "5.56mm carbine with quad rail and holographic sight. Full auto.",
           "mythic", "hitscan", 27, "auto", "holo", 1.5, "556", "birdcage",
           shot("rifle"), bullet(4, 3, 80, 1.4, 0.06, mag=30, tracer_every=4),
           {"form": "ar15", "handguard": 11, "barrel": 5, "optic": "holo", "stock": "m4"},
           [IRON, IRON, IRON, POWDER, POWDER, GLASS],
           "Sneak to aim through the holo sight (1.5x zoom, tighter spread)."),
    weapon("ak47", "AK-47",
           "7.62x39 assault rifle. Wood furniture, banana mag, hard-hitting full auto.",
           "mythic", "hitscan", 33, "auto", "iron", 1.0, "762x39", "slant_brake",
           shot("rifle_heavy"), bullet(5, 3, 70, 2.2, 0.09, mag=30, tracer_every=4),
           {"form": "ak"}, [IRON, IRON, IRON, WOOD, WOOD, POWDER, POWDER],
           "More punch and more climb than the M4; aim to tighten it up."),
    weapon("scar_h", "SCAR-H Battle Rifle",
           "7.62 NATO battle rifle in flat dark earth with a red-dot optic.",
           "mythic", "hitscan", 35, "auto", "dot", 2.0, "762nato", "scar_hider",
           shot("rifle_heavy"), bullet(7, 4, 90, 1.2, 0.1, mag=20, tracer_every=3, pierce=1),
           {"form": "scar", "colors": {"tan": "#b09670"}},
           [IRON, IRON, IRON, POWDER, POWDER, GLASS, "minecraft:sand"],
           "Full-power rounds punch through one mob into the next."),
    weapon("m16a4", "M16A4 Burst Rifle",
           "Full-length 5.56 rifle with ACOG. Three-round burst per pull.",
           "mythic", "hitscan", 30, "burst", "scope4", 4.0, "556_m855", "a2_hider",
           shot("rifle"), bullet(5, 10, 100, 0.6, 0.06, mag=30, burst=3, burst_gap=2),
           {"form": "ar15", "handguard": 16, "barrel": 9, "optic": "acog", "stock": "a2",
            "hg_style": "ribbed"},
           [IRON, IRON, IRON, POWDER, POWDER, GLASS, GLASS],
           "Each pull fires a tight three-round burst; the ACOG zooms when you sneak."),
    weapon("m14_ebr", "M14 EBR",
           "Designated marksman rifle: 7.62 semi-auto in a chassis with a 4x scope and bipod.",
           "mythic", "hitscan", 30, "semi", "scope4", 4.0, "762_match", "dmr_brake",
           shot("rifle_heavy"), bullet(9, 6, 140, 0.3, 0.12, mag=20, headshot_mult=1.75, pierce=1),
           {"form": "dmr"}, [IRON, IRON, IRON, POWDER, POWDER, GLASS, "minecraft:black_dye"],
           "Pinpoint semi-auto at long range; headshots deal 1.75x."),

    # ---------------------------------------------------------------- snipers
    weapon("m24_sws", "M24 Sniper Rifle",
           "Bolt-action .308 sniper system with a long 10x scope and bipod.",
           "epic", "hitscan", 19, "bolt", "scope8", 8.0, "308_win", "sniper_crown",
           shot("sniper", [("bolt", 10)]),
           bullet(28, 30, 220, 0.05, 0.3, mag=5, headshot_mult=2.0, pierce=1, falloff=1.0,
                  tracer_size=0.09, tracer_life=0.12),
           {"form": "bolt_sniper", "stock_skin": "od", "barrel": 24, "scope": "long", "bipod": True},
           [STEEL, POWDER, POWDER, GLASS, GLASS, "minecraft:green_dye"],
           "Sneak for the zoomed scope; the bolt cycles between shots. Headshots deal double."),
    weapon("barrett_m82", "Barrett M82 .50 Cal",
           "Anti-materiel rifle. .50 BMG punches through a whole line of mobs.",
           "mythic", "hitscan", 36, "semi", "scope8", 8.0, "50bmg", "double_brake",
           shot("fifty"),
           bullet(36, 20, 260, 0.1, 0.55, mag=10, headshot_mult=1.5, pierce=4, falloff=1.0,
                  tracer_size=0.12, tracer_life=0.16, muzzle_size=0.7, impact_size=0.5),
           {"form": "anti_materiel"}, [STEEL, STEEL, POWDER, POWDER, POWDER, GLASS, GLASS],
           "Pierces four targets and throws them back. Massive kick.", knock=1.2, move=0.75),
    weapon("mosin_nagant", "Mosin-Nagant",
           "Classic bolt-action 7.62x54R with a wooden stock and a short PU scope.",
           "rare", "hitscan", 16, "bolt", "scope4", 3.5, "762x54r", "hooded_post",
           shot("sniper", [("bolt", 9)]),
           bullet(21, 26, 180, 0.15, 0.25, mag=5, headshot_mult=2.0, falloff=1.0,
                  tracer_size=0.08, tracer_life=0.1),
           {"form": "bolt_sniper", "stock_skin": "wood", "barrel": 18, "scope": "short",
            "bands": True},
           [IRON, IRON, WOOD, WOOD, POWDER, GLASS],
           "Old-school bolt gun: slow, precise, double damage on headshots."),

    # ---------------------------------------------------------------- shotguns
    weapon("remington_870", "Remington 870",
           "12-gauge pump shotgun. Eight buckshot pellets per shell.",
           "mythic", "hitscan", 30, "pump", "iron", 1.0, "12ga_buck", "bead",
           shot("shotgun", [("pump", 7)]),
           bullet(3, 16, 28, 5.5, 0.22, mag=6, pellets=8, falloff=0.5, shell=False,
                  tracer_every=0, impact_size=0.2),
           {"form": "pump_shotgun"}, [IRON, IRON, WOOD, WOOD, POWDER, POWDER, FLINT],
           "Devastating up close, falls off fast past 14 blocks. Knocks mobs back.",
           knock=0.4),
    weapon("aa12", "AA-12 Auto Shotgun",
           "Fully automatic 12-gauge fed from a 20-round drum.",
           "mythic", "hitscan", 30, "auto", "iron", 1.0, "12ga_auto", "aa12_muzzle",
           shot("shotgun"),
           bullet(1.5, 6, 24, 6.5, 0.14, mag=20, pellets=6, falloff=0.5, tracer_every=0,
                  impact_size=0.18),
           {"form": "auto_shotgun"}, [IRON, IRON, IRON, POWDER, POWDER, FLINT, FLINT],
           "Hold the trigger and it keeps spraying buckshot.", knock=0.2, move=0.85),

    # ---------------------------------------------------------------- machine guns
    weapon("m249_saw", "M249 SAW",
           "Belt-fed 5.56 light machine gun with bipod and 200-round pouch.",
           "mythic", "hitscan", 30, "auto", "iron", 1.0, "556_linked", "saw_hider",
           shot("rifle"), bullet(3, 2, 90, 2.4, 0.07, mag=200, tracer_every=4),
           {"form": "lmg"}, [IRON, IRON, IRON, IRON, POWDER, POWDER, "minecraft:leather"],
           "Sustained fire with every fourth round a tracer; sneak to steady it.", move=0.75),
    weapon("m134_minigun", "M134 Minigun",
           "Six-barrel rotary gun. Spins up, then fires 20 rounds a second.",
           "mythic", "hitscan", 30, "auto", "iron", 1.0, "762_belt", "rotary",
           [["gx.gun.minigun", 0.8, 1.0, 0]],
           bullet(1.5, 1, 80, 3.0, 0.05, mag=1500, tracer_every=3, spinup=14, shell=True,
                  smoke=False),
           {"form": "minigun"}, [STEEL, STEEL, POWDER, POWDER, POWDER, "minecraft:redstone"],
           "Barrels spin up for 0.7 s before the first round, then it never stops.", move=0.6),

    # ---------------------------------------------------------------- launchers
    weapon("m20_bazooka", "M20 Super Bazooka",
           "3.5-inch rocket launcher. Unguided rocket, big blast, blows a crater.",
           "rare", "bolt", 12, "single", "iron", 1.0, "rocket_he", "bazooka_bell",
           [["gx.gun.rocket", 1.0, 1.0, 0]],
           {"damage": 24, "rate": 40, "speed": 42, "gravity": 0.04, "lifetime": 100, "aoe": 4,
            "aoe_mult": 1.0, "size": 0.5, "muzzle_size": 0.9, "recoil": 0.5, "blast": 2,
            "smoke": True, "mag": 1},
           {"form": "rocket_tube", "dia": 6, "length": 56, "tube_skin": "od"},
           [STEEL, TNT, TNT, POWDER, "minecraft:green_dye"],
           "Rockets fly flat, trail smoke, and explode on contact (craters need mobGriefing).",
           move=0.8, vfx=ROCKET_VFX),
    weapon("fgm148_javelin", "FGM-148 Javelin",
           "Guided anti-tank missile. Locks onto the nearest mob and chases it.",
           "rare", "bolt", 12, "single", "thermal", 2.0, "missile_heat", "soft_launch",
           [["gx.gun.launcher", 0.8, 0.8, 0], ["gx.gun.rocket", 1.0, 0.9, 4]],
           {"damage": 30, "rate": 50, "speed": 30, "gravity": 0, "lifetime": 160, "aoe": 4.5,
            "aoe_mult": 1.0, "size": 0.55, "muzzle_size": 0.6, "recoil": 0.3, "blast": 2,
            "homing": 28, "homing_turn": 0.18, "mag": 1},
           {"form": "javelin"}, [STEEL, TNT, TNT, "minecraft:redstone", "minecraft:compass",
                                 GLASS],
           "Fire-and-forget: the missile homes onto mobs up to 28 blocks from it.",
           move=0.75, vfx=ROCKET_VFX),
    weapon("m79_launcher", "M79 Grenade Launcher",
           "40mm break-action 'thumper'. Lobs high-explosive grenades in an arc.",
           "epic", "lob", 20, "single", "iron", 1.0, "40mm_he", "thumper",
           [["gx.gun.launcher", 1.0, 1.0, 0]],
           {"damage": 16, "rate": 16, "speed": 26, "gravity": 0.9, "lifetime": 120, "aoe": 3.5,
            "size": 0.4, "muzzle_size": 0.5, "recoil": 0.25, "blast": 1, "mag": 1},
           {"form": "grenade_launcher"}, [IRON, IRON, WOOD, TNT, POWDER],
           "Aim above the target: grenades arc and burst on impact.",
           vfx={"idle": "gx:smoke_trail", "charge": "gx:swirl", "muzzle": "gx:muzzle_flash",
                "body": "gx:orb_glob", "impact": "gx:ring_wave", "screen": "marker_hit",
                "trail": "gx:smoke_trail"}),
    weapon("carl_gustaf", "Carl Gustaf Recoilless Cannon",
           "84mm recoilless cannon. The heaviest shell here and the biggest crater.",
           "rare", "bolt", 12, "single", "scope4", 3.0, "84mm_heat", "venturi",
           [["gx.gun.fifty", 1.0, 0.7, 0], ["gx.gun.rocket", 0.6, 0.8, 1]],
           {"damage": 30, "rate": 50, "speed": 55, "gravity": 0.05, "lifetime": 100, "aoe": 5,
            "aoe_mult": 1.0, "size": 0.6, "muzzle_size": 1.1, "recoil": 0.7, "blast": 3,
            "smoke": True, "mag": 1},
           {"form": "rocket_tube", "dia": 7, "length": 50, "tube_skin": "gunmetal",
            "gustaf": True},
           [STEEL, STEEL, TNT, TNT, TNT, GLASS],
           "Back-blast smoke, a 5-block blast radius, and a 3-block crater.",
           move=0.7, vfx=ROCKET_VFX),
]
