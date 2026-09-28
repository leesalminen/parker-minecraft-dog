// Twist: 5 s charge, then a slow black hole that swallows other projectiles as it flies.
// The pull and the white collapse are declared in params/hooks; this module owns the
// charge and the swallow.

import * as bolt from "../bolt.js";
import { projectiles } from "../../engine/state.js";
import { dist } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) { ctx.st.charge = 0; ctx.st.charging = true; return true; }

export function onHold(ctx) {
  const d = ctx.def, st = ctx.st;
  const full = d.params.charge_ticks ?? 100;
  st.charge = Math.min(full + 10, (st.charge ?? 0) + 1);
  if (ctx.tick % 3 === 0) {
    const t = Math.min(1, st.charge / full);
    vfx.spawn(ctx.dim, d.vfx.charge, muzzleLoc(ctx),
              { color: d.palette.glow, size: 0.4 + 1.2 * t, life: 0.4, count: 2, speed: 1.5 });
  }
  return true;
}

export function onRelease(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const t = Math.min(1, (st.charge ?? 0) / (p.charge_ticks ?? 100));
  st.charge = 0; st.charging = false;
  if (st.reload > 0 || st.cooldown > 0) return true;
  if ((st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return true; }
  if (t < 0.5) return true;                       // undercharged: the hole does not form
  st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  bolt.fire(ctx, { force: true, count: 1, speed: p.speed, gravity: p.gravity,
                   damage: p.damage * (0.6 + 0.4 * t), aoe: p.aoe, size: p.size,
                   lifetime: p.lifetime });
  return true;
}

export function onTick(c, b) {
  // Anything that strays into the hole is swallowed.  Expire it (life = 0) instead of
  // splicing, so the bolt loop's backwards iteration never skips a projectile.
  const radius = c.def.params.swallow_radius ?? 3;
  for (const o of projectiles) {
    if (o === b || o.dim !== b.dim || o.life <= 0) continue;
    if (dist(o.loc, b.loc) < radius) {
      o.life = 0;
      vfx.spawn(b.dim, "gx:swirl", o.loc,
                { color: b.pal.core, size: 0.6, life: 0.3, count: 1, speed: 0.8 });
    }
  }
}
