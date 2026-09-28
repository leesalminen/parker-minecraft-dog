// Galaxy Forge weapon engine entry point.
//
// One global system.runInterval drives every weapon.  Per-tick caps live in state.js
// (60 particles, 8 raycasts, 4 entity queries), so a busy tick can never stall the
// script watchdog.  No per-weapon intervals, no runCommand in hot paths.

import { world, system } from "@minecraft/server";
import { CUSTOM, GLYPHS, WEAPONS } from "./generated/weapons.js";
import { initInput, pollRelease, heldDef } from "./engine/input.js";
import { getState, beginTick, tick } from "./engine/state.js";
import * as ray from "./engine/ray.js";
import * as hud from "./engine/hud.js";
import * as scope from "./engine/scope.js";
import * as vfx from "./engine/vfx.js";
import * as heat from "./engine/heat.js";
import * as hitscan from "./archetypes/hitscan.js";
import * as bolt from "./archetypes/bolt.js";
import * as beam from "./archetypes/beam.js";
import * as charge from "./archetypes/charge.js";
import * as cone from "./archetypes/cone.js";
import * as lob from "./archetypes/lob.js";
import * as chain from "./archetypes/chain.js";
import * as deploy from "./archetypes/deploy.js";
import * as field from "./archetypes/field.js";
import * as tether from "./archetypes/tether.js";

const ARCH = { hitscan, bolt, beam, charge, cone, lob, chain, deploy, field, tether };

// Hand every def its signature-twist module so archetypes can reach it as `def.custom`.
for (const id of Object.keys(WEAPONS)) WEAPONS[id].custom = CUSTOM[id] ?? null;

// Errors used to be swallowed silently, which made "nothing happens" undebuggable.  Each
// distinct error is now logged once, and while DEBUG is on it is also shown in chat.
const DEBUG = true;
const seen = new Set();
function report(e) {
  const msg = `${e?.message ?? e}`;
  if (seen.has(msg)) return;
  seen.add(msg);
  console.warn(`[GalaxyForge] ${msg}\n${e?.stack ?? ""}`);
  if (DEBUG) { try { world.sendMessage(`§c[GalaxyForge] ${msg}`); } catch { /* ignore */ } }
}

try { initInput(); } catch (e) { report(e); }
if (DEBUG) {
  system.runTimeout(() => { try { world.sendMessage("§a[GalaxyForge] weapon engine loaded"); } catch { /* ignore */ } }, 40);
}

// Kill confirmation: a glyph tick + a coin ping for the tracer weapon.
world.afterEvents.entityDie.subscribe((e) => {
  try {
    const killer = e.damageSource?.damagingEntity;
    if (!killer || killer.typeId !== "minecraft:player") return;
    const st = getState(killer);
    if (!st.def) return;
    hud.flash(killer, st, GLYPHS.marker_kill, 8);
    if (st.def.id === "twin_photon_smg") {
      killer.playSound("random.orb", { volume: 0.4, pitch: 2.0 });
    }
  } catch (e) { report(e); }
});

system.runInterval(() => {
  beginTick();
  let players = [];
  try { players = world.getPlayers(); } catch { players = []; }
  for (const player of players) {
    try { tickPlayer(player); } catch (e) { report(e); /* never let one weapon break the loop */ }
  }
  try { bolt.tickBolts(); } catch (e) { report(e); }
  try { field.tickFields(); } catch (e) { report(e); }
  try { deploy.tickDeployables(); } catch (e) { report(e); }
}, 1);

function makeCtx(player, st, def) {
  return {
    player, dim: player.dimension, def, st, tick,
    eye: ray.eyeOf(player), view: ray.viewOf(player),
    pvp: false, point: null,
  };
}

// Unlimited ammo: magazines stay full, so nothing ever needs a reload item.  The ammo
// fields stay in the defs so heat / cooldown balance is unchanged.
//
// Rapid fire: every shot-type archetype (hitscan, bolt, chain, lob) re-fires while the
// trigger is held, at the weapon's rate (build_weapons.py clamps it to RAPID_RATE).
// Weapons whose twist module has its own onHold keep that behaviour instead.
const REPEAT = new Set(["hitscan", "bolt", "chain", "lob"]);

function pressOnce(ctx, custom, mod, aiming, repeat = false) {
  ctx.repeat = repeat;  // true when re-fired by holding, not a fresh click
  let consumed = false;
  if (custom?.onPress) { try { consumed = !!custom.onPress(ctx); } catch (e) { report(e); } }
  if (!consumed) {
    try {
      if (aiming && mod.alt) mod.alt(ctx);
      else if (mod.press) mod.press(ctx);
    } catch (e) { report(e); }
  }
  ctx.st.lastPress = ctx.tick;
}

function tickPlayer(player) {
  const st = getState(player);
  const def = heldDef(player);

  if (!def) {
    st.def = null;
    scope.apply(player, st, null, false);
    hud.actionBar(player, { hud: { kind: "none" } }, st);
    return;
  }

  st.def = def;
  st.ammo = def.ammo?.mag ?? 0;
  st.reload = 0;
  st.wantReload = false;

  // timers
  if (st.cooldown > 0) st.cooldown--;
  if (st.boost > 0) st.boost--;
  if (st.vent > 0) st.vent--;
  heat.cool(st, def, 1);

  const aiming = player.isSneaking === true;
  st.aim = aiming;

  // laser dot (visible to everyone: it is also an "I am aiming at you" tell)
  if (def.dot?.show !== false && (def.dot?.always || aiming) && tick % 2 === 0) {
    const d = scope.laserDot(player, st, def);
    vfx.spawn(player.dimension, d.effect, d.point,
              { color: def.dot.color, size: 0.3, life: 0.35, alpha: 1 });
  }

  scope.apply(player, st, def, aiming);
  scope.rangefinder(player, st, def);
  hud.actionBar(player, def, st);

  pollRelease(player, st);
  // Held-trigger time, for weapons that spin up before firing (minigun).
  if (st.using) st.spin = (st.spin ?? 0) + 1;
  else { st.spin = 0; st.spinSound = false; }

  // ---- archetype dispatch (custom twist modules get first refusal) ----
  const mod = ARCH[def.archetype];
  const ctx = makeCtx(player, st, def);
  const custom = CUSTOM[`gx:${def.id}`];
  const repeats = REPEAT.has(def.archetype) && !custom?.onHold;

  if (st.press) {
    pressOnce(ctx, custom, mod, aiming);
    st.press = false;
  } else if (st.using && repeats) {
    if (tick - (st.lastPress ?? -9999) >= (def.params.rate ?? 4)) pressOnce(ctx, custom, mod, aiming, true);
  } else if (st.using) {
    let consumed = false;
    if (custom?.onHold) { try { consumed = !!custom.onHold(ctx); } catch (e) { report(e); } }
    if (!consumed) { try { mod.hold?.(ctx); } catch (e) { report(e); } }
  }

  if (st.release) {
    let consumed = false;
    if (custom?.onRelease) { try { consumed = !!custom.onRelease(ctx); } catch (e) { report(e); } }
    if (!consumed) { try { mod.release?.(ctx); } catch (e) { report(e); } }
    st.release = false;
  }

  if (!st.using) { try { mod.idle?.(ctx); } catch (e) { report(e); } }
}
