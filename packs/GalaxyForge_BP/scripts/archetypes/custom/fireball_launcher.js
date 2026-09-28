// Twist: the fireball leaves a 1 s burning trail (declared as the ember_trail field) and
// bounces once off the floor (params.bounce).  Alt-fire (sneak + use) throws a triple.

import * as bolt from "../bolt.js";
import { isProtected } from "../../engine/safety.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 20)) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
  st.lastFire = ctx.tick;
  st.ammo = Math.max(0, (st.ammo ?? mag) - 1);

  const alt = ctx.player.isSneaking === true;
  bolt.fire(ctx, { force: true, count: alt ? (p.alt_count ?? 3) : 1,
                   spread: alt ? (p.alt_spread ?? 12) : 0,
                   speed: p.speed, gravity: p.gravity, aoe: p.aoe, damage: p.damage,
                   fuse: p.fuse, lifetime: p.lifetime, size: p.size });
  return true;
}

export function onHit(ctx, target) {
  if (isProtected(target, ctx.player, { pvp: false })) return;
  try { target.setOnFire(ctx.def.params.ignite ?? 5, true); } catch { /* ignore */ }
}
