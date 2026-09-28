# Deviations from the engine prompt

Every item below is a deliberate, documented substitution — nothing was silently dropped.

## 1. Zoom uses the `/camera fov_set` command, clamped to 30 degrees

**Spec'd:** Phase 0 spike `player.camera` stable APIs → Slowness → glyph overlay, pick one.

**Finding:** `@minecraft/server`'s `Camera.setFov` is **beta-only** under the stable track;
using it would require the Beta APIs experiment, which the prompt forbids because it breaks
Realms and console joins. Slowness does not affect FOV in Bedrock at all. The `/camera`
command's `fov_set` / `fov_clear` subcommands are available without experiments (present in
the 1.26.51 client), but the engine clamps a custom FOV to [30, 110] degrees.

**Substitution:** `engine/scope.js` issues `camera @s fov_set <fov> 0.15 linear` once when the
player starts aiming (sneaking) a weapon with `zoom > 1` and `camera @s fov_clear` when they
stop, switch weapons or holster (via `engine/cmd.js`, never per tick). FOV is derived from a
70-degree baseline, so 1.5x = 50, 2x = 39, and anything from about 2.6x up hits the 30-degree
floor. The glyph vignette and reticle still draw on top. Weapons declare `zoom: 4` as before.

## 2. Scope overlay is the glyph technique, not custom JSON UI

Per the prompt, no custom JSON UI. Scopes/reticles/HUD use `setTitle`/`updateSubtitle`/
`setActionBar` with private-use glyphs from `font/glyph_E2.png`.

**Page choice:** the prompt says "glyph_E1.png etc.". This pack uses **E2**, because
vanilla already fills cells in E0/E1 with emoji and overwriting them would break vanilla
emoji. E2..F8 are free in vanilla, so E2 cannot collide.

**Overlay coverage:** the exact on-screen size of the vignette grid depends on the client's
title scale, which cannot be measured without the console. The grid width/rows in
`scope.js` (`WIDTH = 9`) is the single tuning knob; TESTING.md flags it.

## 3. First-person pose numbers are conservative

Vanilla's trident needs a large rotation because its pole is drawn along +Y. Our weapons
are drawn along -Z (muzzle forward), which is already the held orientation, so the shared
`animation.gx_weapon.wield` pose is identity plus a small `aim` tilt. This avoids guessing
large offsets blind. If the weapon sits oddly in hand on the PS5, the numbers in
`RP/animations/gx_weapon.animation.json` are the tuning knob.

## 4. Lobbies / aim state

The prompt lists ADS as "sneak toggles scope" and alt-fire as "sneak + use". These collide,
so they are resolved as: **sneak = aim** (dot on, scope overlay), **sneak + use = alt-fire**.
Documented in `engine/input.js`.

## 5. Knockback API signature

`Entity.applyKnockback` has had two stable signatures across 1.x. `engine/damage.js` tries
both and falls back to `applyImpulse`, so knockback works on either. Verified on console is
still required (TESTING.md).

## 6. Charged weapons declare `archetype` as their delivery form

Weapons the spec calls "charge + hitscan" (plasma_lance, helios_sniper, railgun_mk2) use
`archetype: charge` with `params.mode: hitscan`, so the charge tier table decides the
delivery. This keeps one implementation of charging.

## 7. Lob and bolt share the script projectile

The prompt says "prefer particles over entities everywhere possible". `lob` therefore
delegates flight to the same entity-free ray-marched bolt as `bolt`, adding gravity, fuse
and an AoE. No projectile entities are spawned for any of the 50 weapons; only the two
`deploy` entities exist as real entities.

## 8. Ultimates' block damage

Orbital Designator, Supernova Rifle and Black Hole Cannon can change blocks only when
`mobGriefing` is true, capped (20-30 blocks), exactly as specced. When the gamerule is
false the weapon still does full entity damage.

## 9. Bio family approximations

* **acid_sprayer** — "Corrode stacks 3x" cannot be expressed as an escalating amplifier on a
  status effect. Approximated: each hit refreshes Weakness + Poison-lite (4 s), and the
  lingering `acid_pool` field applies the fully-stacked coat (Weakness amp 2 + Poison) to
  anything standing in it. The sprayer is pump-action (`params.burst`) rather than
  channeled, because a channeled cone would push a new puddle every spray tick per mob.
* **spore_launcher** — the "mobs killed inside the cloud spawn a mushroom puff (+XP)" line
  is dropped: the effect vocabulary has no kill event and script cannot grant XP. The cloud
  still drifts spore motes via its `extra.spawn`. The spore darts are forced to
  `splits = 1, aoe = 0` so they cannot re-split/re-detonate into a cascade.
* **nanite_swarm_rifle** — "tick damage while attached" has no attach hook; approximated
  with Poison amp 1 on hit. Kill detection is approximated by hit counting (the swarm
  dissolves after its third distinct target).

## 10. Support family approximations

* **sonic_cannon** — "hits arrive delayed by distance (visible wave speed)" is dropped: the
  cone archetype resolves damage on the release tick. The expanding arc bands and the
  knockback are kept, so the wave still reads visually.
* **seeker_rack** — the spec asks for scope `lock` + `rangefinder`. They cannot coexist:
  `engine/scope.js` binds the distance readout to `rangefinder`/`scope4`/`scope8`, and the
  lock reticle is its own overlay. The weapon uses `lock` (red brackets), which is the
  twist-relevant half.
* **sentinel_kit** — "turrets that share line-of-sight sync fire" is approximated by
  distance (another same-owner turret within 16 blocks grants +25% damage); script has no
  cheap LOS query per turret per tick.

## 11. Energy cell economy

One shared `gx:energy_cell` item (4 per craft) replaces per-weapon ammo items, as the
prompt prefers. Heat-only weapons (e.g. Plasma Repeater) never consume cells.
