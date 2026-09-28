// Twist: firing at the ground, or while airborne, turns the blast into a rocket jump —
// the recoil launches you upward and the cone still sweeps everything around you.

import * as vfx from "../../engine/vfx.js";
import { muzzleLoc } from "../hitscan.js";

export function onRelease(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const t = Math.min(1, (st.charge ?? 0) / (p.hold_ticks ?? 20));
  const downward = ctx.view.y < -0.5;
  const airborne = ctx.player.isJumping === true;
  if (!downward && !airborne) return false;      // ordinary palm blast: let the cone fire

  const push = (p.jump_power ?? 0.8) * (1 + t * (p.charge_mult ?? 1));
  try {
    ctx.player.applyImpulse({ x: -ctx.view.x * push, y: Math.max(0.6, push), z: -ctx.view.z * push });
  } catch { /* ignore */ }

  vfx.spawn(ctx.dim, "gx:shock_disc", muzzleLoc(ctx),
            { color: d.palette.core, size: 1.4, life: 0.4 });
  vfx.spawn(ctx.dim, "gx:ring_wave", ctx.player.location,
            { color: d.palette.glow, size: 2.0 + t, life: 0.4 });
  return false;                                  // the cone blast still lands this tick
}
