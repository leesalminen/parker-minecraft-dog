# Phase 0 spikes — findings

The engine prompt asks for spikes on the real target (PS5 via a hosted world / Realm).
I can't join a console world from here, so each spike is split into **verified locally**
(docs, schemas, static analysis, generated output) and **must be confirmed by Lee on the
PS5**. Nothing was guessed where a primary source existed.

## Spike 1 — script module loads on a console-joined world

**Verified locally.** Manifest module + dependency shape taken from the official versioning
table:

| `@minecraft/server` | Minecraft |
|---|---|
| **1.11.0** | **1.21.0** |

`min_engine_version` is `[1,21,0]`, so the newest **stable** module supported is **1.11.0**.
`GalaxyForge_BP/manifest.json` now declares:

```json
{ "type": "script", "language": "javascript", "uuid": "6f2c1a84-…",
  "entry": "scripts/main.js", "version": [1, 0, 0] }
…
{ "module_name": "@minecraft/server", "version": "1.11.0" }
```

No `-beta` suffix anywhere, so the Beta APIs experiment is **not** required and Realms /
console joins are unaffected. `tools/build.py` fails the build if a beta dependency ever
creeps in.

**Must confirm on PS5:** join the hosted world and check the log shows no
`[Scripting]` load error, and that firing any weapon does something.

## Spike 2 — title-glyph overlay renders a scope and a crosshair

**Verified locally.** Bedrock loads `font/glyph_<page>.png` directly for its code page —
there is no JSON provider file (`resource_pack/font/glyph_E1.json` 404s in Mojang's
`bedrock-samples`). The sheet is 256×256 = 16×16 cells of 16×16 px; cell index `i` maps to
codepoint `0xE2xx` where `xx = i` (row-major).

`tools/weapons/glyphs.py` generates `RP/font/glyph_E2.png` with 63 glyphs (scope corners
and edges, four reticles, mil-dot, lock brackets, rangefinder, hourglass, hit/kill/heart/
bone/paw markers, frost/heat/void/toxic/whiteout vignettes, HUD pips, heat and charge
segments, cell/battery/fuel/vent icons). **Page E2, not E1**: vanilla fills cells in E0/E1
with emoji, so E1 would clobber them; E2..F8 are unused by vanilla.

`engine/scope.js` composes the overlay as a `\n`-separated grid of corner/edge/centre
glyphs pushed through `player.onScreenDisplay.setTitle`, and `engine/hud.js` puts ammo /
heat / charge readouts on the action bar. Both cache the last string and only re-issue on
change, so nothing flickers.

**Must confirm on PS5:** the overlay's on-screen size depends on the client's title scale,
which can't be measured off-console. `WIDTH = 9` in `scope.js` is the single tuning knob;
if the vignette is too small, raise it.

## Spike 3 — best zoom technique

**Verified locally, decision made.** Checked all three options against the stable docs:

* `player.camera` / `Camera.setCamera` — **beta only**. The stable docs page 404s and the
  API requires the Beta APIs experiment, which the prompt forbids (it breaks Realms and
  console joins). Rejected.
* Slowness effect — in Bedrock it slows movement only; it does **not** narrow FOV. Rejected.
* Glyph overlay alone — works on stable APIs, needs no experiment. **Chosen.**

`scope.js` therefore presents zoom as a closing vignette plus a reticle drawn at range,
and weapons still declare `zoom: 4` behind the same interface. Recorded in
`DEVIATIONS.md` §1.

## Spike 4 — 60 particles/tick does not stutter

**Verified locally (static).** The budget is enforced in `engine/state.js`
(`CAP = {particles: 60, rays: 8, queries: 4}`), reset every tick by `beginTick()`, and
every `vfx.spawn` / `raycast` / `entitiesNear` charges against it and silently no-ops when
exhausted. Beams are capped at 40 billboard particles per call (`vfx.line`, `max: 40`),
and bolts spawn exactly one body particle per tick.

`tools/weapons/tests/engine.test.mjs` exercises the budget path (the field test must
re-`beginTick()` between pulses or the query cap starves it), so the cap is known to be
live rather than decorative.

**Must confirm on PS5:** 60 particles/tick plus one raycast is the designed ceiling. On a
base PS5 this should hold; if it hitches during a beam + several bolts, drop `CAP.particles`
to 40 — it is a one-line change.

## Spike 5 — `getBlockFromRay` + `getEntitiesFromRay` at 100 blocks per tick

**Verified locally.** Both are stable `Dimension` methods in 1.11.0:
`getBlockFromRay(location, direction, options?: BlockRaycastOptions)` and
`getEntitiesFromRay(location, direction, options?: EntityRaycastOptions)`, both taking
`maxDistance`. `engine/ray.js` calls each once per cast, clamps the entity hit to the block
hit distance, sorts hits by distance, and charges one unit of the ray budget.

The 100-block case is the Helios Sniper / Railgun (`range: 100` / `150`) — a single raycast
per shot, never per tick, so it stays inside the 8-rays-per-tick cap.

**Must confirm on PS5:** fire Helios Sniper and Railgun Mk II at a mob ~100 blocks away and
confirm the hit registers without a tick spike.

## What Lee must test (summary)

1. World loads with the script module, no experiment toggle.
2. Scope overlay + laser dot + action-bar HUD render at a usable size (`WIDTH` knob).
3. Firing any weapon produces bolts/beams/particles and damage.
4. Long-range shots (100+ blocks) land.
5. A 60-particle beam + 3 bolts tick holds framerate.
6. Weapon pose in hand looks right (`RP/animations/gx_weapon.animation.json` knob).
