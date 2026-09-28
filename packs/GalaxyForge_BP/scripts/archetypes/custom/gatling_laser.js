// Twist: six-barrel spin-up. Rate ramps 4 -> 24 shots/s over one second, the wielder is
// slowed while spun up, full spin merges the bolts into a hairline beam, and releasing
// keeps the barrels firing for half a second (momentum).

import { system } from "@minecraft/server";
import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { add, eyeOf, viewOf } from "../../engine/ray.js";
import { muzzleLoc } from "../hitscan.js";

const SPIN_TICKS = 20;
const MIN_RATE = 4;
const MAX_RATE = 24;

function gapFor(spin) {
  const rate = MIN_RATE + (MAX_RATE - MIN_RATE) * (spin / SPIN_TICKS);
  return Math.max(1, Math.round(20 / rate));
}

function shoot(ctx, st, d) {
  if (st.reload > 0 || st.cooldown > 0) return false;
  if ((st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return false; }
  st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  bolt.fire(ctx, { force: true, count: 1, damage: d.params.damage });
  try { ctx.player.addEffect("slowness", 10, { amplifier: 0, showParticles: false }); }
  catch { /* ignore */ }
  return true;
}

export function onPress(ctx) { ctx.st.scratch.spin = 0; return true; }

export function onHold(ctx) {
  const d = ctx.def, st = ctx.st;
  st.scratch.spin = Math.min(SPIN_TICKS, (st.scratch.spin ?? 0) + 1);
  if (ctx.tick - (st.lastFire ?? -999) < gapFor(st.scratch.spin)) return true;
  if (!shoot(ctx, st, d)) return true;
  st.lastFire = ctx.tick;
  if (st.scratch.spin >= SPIN_TICKS) {
    vfx.line(ctx.dim, muzzleLoc(ctx), add(ctx.eye, ctx.view, 24), "gx:beam_needle",
             d.palette, { step: 1.0, max: 24, size: 0.12, life: 0.1 });
  }
  return true;
}

export function onRelease(ctx) {
  const d = ctx.def, st = ctx.st;
  const spun = st.scratch.spin ?? 0;
  st.scratch.spin = 0;
  if (spun <= 0) return true;
  let left = d.params.momentum_ticks ?? 10;           // 0.5 s of spin-down
  const step = () => {
    if (left-- <= 0) return;
    const c = { ...ctx, eye: eyeOf(ctx.player), view: viewOf(ctx.player) };
    if (shoot(c, ctx.st, d)) system.runTimeout(step, 2);
  };
  system.runTimeout(step, 2);
  return true;
}
