// Twist: two barrels alternate (muzzle flashes alternate sides); every 12th shot is a
// golden tracer that pings a hit marker with a coin sound.

import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) { return fire(ctx); }
export function onHold(ctx) { return fire(ctx); }

function fire(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < p.rate) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
  st.lastFire = ctx.tick;
  st.ammo = Math.max(0, (st.ammo ?? mag) - 1);

  st.scratch.shot = (st.scratch.shot ?? 0) + 1;
  const golden = st.scratch.shot % (p.tracer_every ?? 12) === 0;
  const side = st.scratch.shot % 2 === 0 ? 1 : -1;
  const snap = { ...ctx, eye: { x: ctx.eye.x + 0.16 * side, y: ctx.eye.y - 0.1, z: ctx.eye.z } };

  bolt.fire(snap, { force: true, count: 1,
                    damage: p.damage * (golden ? 2 : 1),
                    size: golden ? 0.35 : p.size });

  if (golden) {
    try { ctx.player.playSound("random.orb", { volume: 0.5, pitch: 1.8 }); } catch { /* ignore */ }
    vfx.spawn(ctx.dim, "gx:star_flash", muzzleLoc(snap),
              { color: [1, 0.85, 0.3], size: 0.6, life: 0.2 });
  }
  return true;
}
