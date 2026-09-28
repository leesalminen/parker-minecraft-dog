// Twist: continuous fire ramps the flame orange -> yellow -> blue over 4 s; at blue the
// cone deals x1.5 damage.  The tank gauge drains as heat climbs, and flames only spread
// through flammable blocks while mobGriefing is on.

import * as vfx from "../../engine/vfx.js";
import { hurt, grief } from "../../engine/damage.js";
import { isProtected } from "../../engine/safety.js";
import { muzzleLoc } from "../hitscan.js";

const RAMP = 80;             // 4 s of unbroken fire to reach blue

const ORANGE = [1, 0.45, 0.1];
const YELLOW = [1, 0.9, 0.35];
const BLUE = [0.35, 0.7, 1];

export function onPress(ctx) { ctx.st.scratch.ramp = 0; return false; }

export function onHold(ctx) {
  const d = ctx.def, st = ctx.st;
  st.scratch.ramp = Math.min(RAMP, (st.scratch.ramp ?? 0) + 1);
  st.fuel = 1 - Math.min(1, (st.heat || 0) / (d.heat?.max ?? 100));
  if (ctx.tick % 2 === 0) {
    const t = st.scratch.ramp / RAMP;
    const col = t >= 1 ? BLUE : t >= 0.5 ? YELLOW : ORANGE;
    vfx.spawn(ctx.dim, d.vfx.muzzle, muzzleLoc(ctx),
              { color: col, size: 0.6 + t * 0.5, life: 0.25, count: 2, speed: 0.8 });
  }
  return false;                                     // the cone archetype owns the spray
}

export function onRelease(ctx) {
  const st = ctx.st;
  st.scratch.ramp = 0;
  st.fuel = 1 - Math.min(1, (st.heat || 0) / (ctx.def.heat?.max ?? 100));
  return false;
}

export function onHit(ctx, target) {
  const d = ctx.def, st = ctx.st;
  if (isProtected(target, ctx.player, { pvp: false })) return;
  try { target.setOnFire(d.params.ignite ?? 5, true); } catch { /* ignore */ }
  if ((st.scratch?.ramp ?? 0) >= RAMP) {
    hurt(target, (d.params.dps ?? 14) * 0.5 / 20, ctx, "magic");   // blue flame: x1.5
  }
  if (ctx.tick % 20 === 0 && d.params.grief) {
    grief({ ...ctx, point: target.location }, d.params.grief);
  }
}
