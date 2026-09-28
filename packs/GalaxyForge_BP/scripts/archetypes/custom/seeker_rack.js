// Twist: hold to bank one lock every 0.6 s (up to four, echoed by the lock glyph in the
// subtitle), then release to ripple-fire that many homing missiles.  Each missile lifts
// off, arcs over and dives onto its target; a wall hit sets off its AoE instead of dudding.

import * as bolt from "../bolt.js";
import { system } from "@minecraft/server";
import { GLYPHS } from "../../generated/weapons.js";

function clearLocks(st) { st.scratch.locks = 0; st.scratch.lockAt = 0; }

export function onPress(ctx) {
  const st = ctx.st, d = ctx.def;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return true; }
  clearLocks(st);
  return true;                                  // the rack fires on release, not on press
}

export function onHold(ctx) {
  const st = ctx.st, p = ctx.def.params;
  const gap = p.lock_ticks ?? 12;
  if (ctx.tick - (st.scratch.lockAt ?? -999) < gap) return true;
  st.scratch.lockAt = ctx.tick;
  st.scratch.locks = Math.min((st.scratch.locks ?? 0) + 1, p.max_locks ?? 4);
  try { ctx.player.onScreenDisplay.updateSubtitle(GLYPHS.scope_lock.repeat(st.scratch.locks)); }
  catch { /* ignore */ }
  return true;
}

export function onRelease(ctx) {
  const st = ctx.st, d = ctx.def, p = d.params;
  const n = Math.min(st.scratch.locks ?? 0, p.max_locks ?? 4);
  clearLocks(st);
  if (!n || st.reload > 0 || st.cooldown > 0) return true;
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - n);
  for (let i = 0; i < n; i++) {
    system.runTimeout(() => {
      try { bolt.fire(ctx, { force: true, count: 1, spread: 0, homing: p.homing ?? 6,
                             damage: p.damage ?? 8, aoe: p.aoe ?? 2 }); }
      catch { /* player gone */ }
    }, i * (p.fire_gap ?? 4));
  }
  return true;
}

/** Lift the missile for its first few ticks so it arcs up before homing dives it down. */
export function onTick(c, b) {
  const p = c.def.params;
  if (b.arc === undefined) b.arc = p.arc_ticks ?? 10;
  if (b.arc <= 0) return;
  b.arc--;
  b.vel = { x: b.vel.x, y: b.vel.y + (p.arc_lift ?? 0.5), z: b.vel.z };
}
