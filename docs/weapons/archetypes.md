# Galaxy Forge weapon engine — design notes

One engine, ten archetypes, fifty weapons expressed as data + VFX. Nothing here is
per-weapon bespoke code except the ~60-line signature-twist modules in
`packs/GalaxyForge_BP/scripts/archetypes/custom/<id>.js`.

```
tools/weapons/
  archetypes.md   this file
  defs/*.py       one module per family, exports WEAPONS = [dict, ...]   (data only)
  model.py        held-model geometry + emissive texture (reuses tools/creatures/lib.py)
  particles.py    RP/particles/*.json + the shared shape atlas
  glyphs.py       RP/font/glyph_E2.png (scopes, reticles, HUD readouts)
  build_weapons.py emits items, attachables, recipes, particles, lang, generated/weapons.js
  tests/          Node unit tests against a mocked @minecraft/server
packs/GalaxyForge_BP/scripts/
  main.js         one global system.runInterval drives everything
  engine/         state input ray scope hud heat damage vfx sound safety
  archetypes/     hitscan bolt beam charge cone lob chain deploy field tether
  archetypes/custom/<id>.js   signature twists only
  generated/weapons.js        written by build_weapons.py, never hand-edited
```

## Def schema

Every weapon in `defs/<family>.py` is a plain dict with these keys (all required):

| key | meaning |
|---|---|
| `id` | file/id stem, e.g. `pulse_carbine` → `gx:pulse_carbine` |
| `name` | display name (no real streamers) |
| `description` | one-line tooltip, also written to lang |
| `family` | plasma, laser, fire, cryo, lightning, void, bio, support, cosmic, nerf, military |
| `tier` | toy / common / rare / epic / mythic / ultimate |
| `archetype` | hitscan, bolt, beam, charge, cone, lob, chain, deploy, field, tether |
| `dps` | sustained DPS at a comparable range (budget below) |
| `scope` | iron, holo, dot, scope4, scope8, thermal, rangefinder, lock, focus |
| `zoom` | magnification while aiming: real camera FOV, floored at 30° (see DEVIATIONS.md) |
| `dot` | `{style: dot\|dot_ring\|dot_cross, color: "#rrggbb", range: blocks}` |
| `ammo` | `{type: "cell", mag: N}` or `{type: "heat"}`; ammo is unlimited in play (main.js keeps magazines full) |
| `heat` | `None`, or `{max, per_shot, cool, vent}` (`cool` = units/second) |
| `hud` | `{kind: ammo\|heat\|fuel\|charge\|charges\|mode\|none}` (`mode` shows the fire mode / minigun spin-up) |
| `palette` | `{name, core, glow, trail, accent}` — `name` must be unique |
| `shape` | `{projectile, muzzle}` — unique per family (build fails otherwise) |
| `sound` | `[[soundId, volume, pitch, delayTicks], ...]` |
| `params` | archetype-specific (below) |
| `hooks` | `{on_hit: [effects], on_tick: [effects]}` |
| `vfx` | `{idle, charge, muzzle, body, impact, screen}` — all six required |
| `model` | `{form, ...}` geometry recipe for model.py |
| `recipe` | `{ingredients: [...]}` (shapeless) or `{pattern, key}` (shaped) |
| `twist` | the signature twist, one sentence |
| `custom` | `None` or the id of `archetypes/custom/<id>.js` |
| `cooldown` | optional seconds (ultimates use 45-60) |
| `melee` | optional melee damage (default 2) |
| `move_mod` | optional movement modifier while holding (default 0.9) |
| `fire_mode` | optional: semi / auto / burst / bolt / pump / single. Weapons with a fire mode keep their own `rate` instead of the rapid-fire clamp |

Realistic (military) weapons use high-detail model forms from `hd_models.py` (1/32-block
cubes on an `hd` bone scaled 0.5) and extra hitscan params: `spread` (degrees, halved while
aiming), `pellets`, `burst` + `burst_gap`, `spinup`, `tracer_every` (0 = none),
`tracer_step`, `impact_size`, and per-shot `recoil` / `shell` / `smoke` (engine/firearm.js).
Bolts and lobs take `blast` (crater radius, mobGriefing-gated). Their sounds come from
`sounds.py` (`gx.gun.*`, synthesised .ogg files in RP/sounds/gx).

DPS budget: toy ≈ 3 (nerf blasters), common ≈ 8, rare ≈ 14, epic ≈ 22, mythic ≈ 30; ultimates trade DPS for burst
with a ≥ 45 s cooldown. `build_weapons.py` rejects a dps more than 20% off budget.

## Model forms

`model.py` builds each silhouette from `model = {form, ...}`. Distinct silhouettes come
from the form plus per-weapon dimensions:

| form | extra keys | silhouette |
|---|---|---|
| `rifle` | `len, thick, tall, scope, scope_len, fins, drum, underbarrel` | long barrel + stock |
| `sniper` | `len` | very long barrel + big optic + bipod |
| `pistol` | `tall` | compact sidearm |
| `revolver` | — | cylinder + 6 chambers |
| `smg` | `len, twin` | stubby, one or two barrels |
| `cannon` | `len` | thick tube + shoulder rest + core cage |
| `launcher` | `len` | fat tube + drum |
| `mortar` | — | squat tube, high angle |
| `lance` | `len, rings` | long barrel + floating ring emitters |
| `staff` | `len` | rod + orb head |
| `gauntlet` | — | armour block + palm emitter |
| `bow` | — | limbs + string |
| `disc` | — | chamber + disc emitter |
| `sprayer` | — | nozzle + tank + vial |
| `rack` | `tubes` | multi-tube missile rack |
| `kit` | — | briefcase turret kit |

Every model also takes `metal` (base colour, default `#59616d`) and `grip`.

## Archetype params

* **hitscan** — `range, damage, rate, pierce, ricochet, falloff, headshot_mult,
  tracer_size, muzzle_size, bonus_vs {family, mult}`
* **bolt** — `speed, gravity, homing, homing_turn, lifetime, rate, damage, count, spread,
  size, muzzle_size, pierce, bounce, split, split_at, split_speed, split_life,
  split_homing, max_splits, stick, fuse, aoe, aoe_mult, auto, twin_barrels, grief`
* **beam** — `range, dps, width, heat_rate, tick_rate, refract, refract_glass`
* **charge** — `mode` (`hitscan`/`bolt`/`lob`), `hold_ticks, min_ticks, range, pierce,
  width, heat_rate, tiers: [{ticks, damage, range, pierce, size, heat, cooldown, ...}]`
* **cone** — `range, angle, dps, status, knockback, rate, charge, hold_ticks,
  charge_mult, particle_size, muzzle_size, grief`
* **lob** — `speed, gravity, aoe, damage, fuse, lifetime, count, spread, rate, size`
* **chain** — `range, jumps, radius, falloff, damage, rate, auto`
* **deploy** — `entity, duration, cap, dps, range, interval, rate, hover, place_range`
* **field** — zones are spawned by hooks (`{"field": kind, "radius", "life", "dps",
  "pull", "push", "extra"}`), not fired directly
* **tether** — `range, damage, rate, pull, stun, grapple_cooldown`

## Effect vocabulary (damage.js)

```python
{"dmg": 6, "cause": "projectile"}
{"status": "slowness", "ticks": 40, "amp": 2}
{"vfx": "gx:spark_burst", "size": 0.4, "life": 0.5, "count": 6, "at": "hit"|"self"}
{"field": "sun_scar", "radius": 3, "life": 120, "dps": 4, "pull": 0,
 "extra": {"status": [{"id": "weakness", "ticks": 40, "amp": 0}],
           "collapse": {"dmg": 8, "knock": 1.4}, "spawn": "gx:ember_trail"}}
{"knockback": 1.2, "dir": "away"|"up"|"toward"}
{"heal": 4}
{"chain": {"jumps": 3, "radius": 6, "falloff": 0.8}}
{"grief": {"radius": 3, "from": ["minecraft:sand"], "to": "minecraft:glass", "cap": 20}}
{"stun": 60}                      # machines only (gx_* families)
{"bonus_vs": {"family": "gx_droid", "mult": 1.4}}
```

`grief` only ever runs when `mobGriefing` is true, and is capped.

## VFX vocabulary

Six layers per weapon, all required, all distinct from the other 49:

1. `idle` — ambient particle at low rate (spawned every 8 ticks)
2. `charge` — particles converging on the muzzle
3. `muzzle` — unique flash shape/colour
4. `body` — projectile/beam body (core + glow + trail)
5. `impact` — flash + shockwave ring + debris
6. `screen` — glyph name for hit/overheat/charge feedback (`vignette_heat`, ...)

Particle effect names available (see `particles.py`):

```
gx:orb_{teardrop,dart,glob,needle,disc,soft_orb,shard,droplet,star,paw,bone,hex,plume}
gx:beam_{bar,needle,teardrop,disc,plume,fork}
gx:dot_{dot,dot_ring,dot_cross}
gx:ring_wave  gx:shock_disc  gx:spark_burst  gx:debris_burst  gx:crystal_burst
gx:muzzle_flash  gx:star_flash  gx:smoke_trail  gx:ember_trail
gx:lightning_fork  gx:static_arc  gx:swirl  gx:field_glow  gx:snow_mote
```

## Custom twist modules

`archetypes/custom/<id>.js` is an ES module exporting any of:

```js
export function onPress(ctx)   { return false; }  // true = consume the press
export function onHold(ctx)    { return false; }  // true = consume this tick
export function onRelease(ctx) { return false; }  // true = consume the release
export function onHit(ctx, target) {}             // called by the archetype on a hit
export function onTick(ctx, bolt) {}              // bolt archetype only, per projectile
export function onDetonate(ctx, bolt, loc) {}     // bolt archetype only
export function onDeploy(ctx, entity) {}
export function onDeployHit(ctx, target, entity) {}
export function onTether(ctx, target) {}
```

`ctx` = `{player, dim, def, st, tick, eye, view, pvp, point}`. State (`st`) is per player
and per weapon, with a scratch bag at `st.scratch`. Helpers to reuse:
`bolt.fire(ctx, overrides)`, `bolt.splitBolt(b, n, opts)`, `vfx.spawn/line/impact/muzzle`,
`sound.play`, `heat.add/cool/isHot/inVentZone/clear`, `GLYPHS` from
`../../generated/weapons.js`.

## Validation

`build_weapons.py` fails when: the roster is not 73, ids repeat, a required key is
missing, a tier/archetype/scope is unknown, dps is outside budget, a vfx layer is missing,
the sound recipe is empty, a `(palette, projectile, muzzle)` or `(family, projectile,
muzzle)` tuple repeats, or a palette colour is missing. `tools/build.py` then checks every
weapon has its item JSON, attachable, geometry, emissive texture, icon, atlas entry,
lang name + description, and recipe.
