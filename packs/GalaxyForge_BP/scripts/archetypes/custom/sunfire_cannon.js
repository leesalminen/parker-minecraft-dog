// Twist: 2.5s charge, then a slow golden sphere that leaves a sun-scar pool.  The melt
// (sand/snow/ice -> glass, gated by mobGriefing) is declared in params.grief.

import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) { ctx.st.charge = 0; ctx.st.charging = true; return true; }

export function onHold(ctx) {
  const d = ctx.def, st = ctx.st;
  const full = d.params.charge_ticks ?? 50;
  st.charge = Math.min(full + 10, (st.charge ?? 0) + 1);
  if (ctx.tick % 3 === 0) {
    vfx.spawn(ctx.dim, d.vfx.charge, muzzleLoc(ctx),
              { color: d.palette.glow, size: 0.4 + 0.8 * (st.charge / full), life: 0.4,
                count: 2, speed: 1.4 });
  }
  return true;
}

export function onRelease(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const t = Math.min(1, (st.charge ?? 0) / (p.charge_ticks ?? 50));
  st.charge = 0; st.charging = false;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
  if (t < 0.35) return true;                       // undercharged: nothing fires
  st.ammo = Math.max(0, (st.ammo ?? mag) - 1);
  bolt.fire(ctx, { force: true, count: 1, speed: p.speed, gravity: p.gravity,
                   damage: p.damage * (0.6 + 0.4 * t), aoe: p.aoe, size: p.size,
                   lifetime: p.lifetime });
  return true;
}
