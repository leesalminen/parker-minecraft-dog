// Twist: globs stick, then detonate 1.5s later and chain-detonate every other stuck glob
// within 3 blocks.  Alt-fire (sneak + use) tightens the spread.

import * as bolt from "../bolt.js";
import { projectiles } from "../../engine/state.js";
import { dist } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < p.rate) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
  st.lastFire = ctx.tick;
  st.ammo = Math.max(0, (st.ammo ?? mag) - 1);

  const spread = ctx.player.isSneaking ? (p.alt_spread ?? p.spread) : p.spread;
  bolt.fire(ctx, { force: true, count: p.count, spread, damage: p.damage,
                   speed: p.speed, gravity: p.gravity, lifetime: p.lifetime,
                   aoe: p.aoe, aoe_mult: p.aoe_mult, size: p.size, fuse: p.fuse });
  return true;
}

export function onDetonate(c, b, loc) {
  const r = c.def.params.chain_radius ?? 3;
  for (const o of projectiles) {
    if (o === b || !o.stuck || o.forceDetonate) continue;
    if (dist(o.loc, loc) > r) continue;
    o.forceDetonate = true;
    vfx.spawn(c.dim, "gx:star_flash", o.loc, { color: o.pal.core, size: 0.6, life: 0.2 });
  }
}
