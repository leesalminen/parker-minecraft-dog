// lob: arcing script bolt with a fuse and an on_land field.  Delegates the flight to
// bolt.js (no entity), so the only cost is a ray-march per tick.

import * as bolt from "./bolt.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import { muzzleLoc } from "./hitscan.js";
import * as firearm from "../engine/firearm.js";

export function press(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 20)) return;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  st.lastFire = ctx.tick;
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  const cd = p.cooldown ?? d.cooldown;
  if (cd) st.cooldown = cd * 20;
  bolt.fire(ctx, { force: true, count: p.count ?? 1, spread: p.spread ?? 0,
                   speed: p.speed ?? 14, gravity: p.gravity ?? 0.2, aoe: p.aoe ?? 3,
                   damage: p.damage ?? 8, fuse: p.fuse ?? 0, lifetime: p.lifetime ?? 120,
                   size: p.size ?? 0.6 });
  const m = muzzleLoc(ctx);
  vfx.muzzle(ctx.dim, m, d.palette, { size: p.muzzle_size ?? 0.6, count: 4, effect: d.vfx.muzzle });
  sound.play(ctx.player, d.sound);
  firearm.after(ctx, m);
}

export function hold() {}
export function release() {}
export function idle() {}
