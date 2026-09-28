// Twist: 3-round burst; the third bolt is a larger kicker (+50% damage, ring impact).
// Alt-fire (sneak + use) is a single tap.

import { system } from "@minecraft/server";
import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < p.rate) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }

  const single = ctx.player.isSneaking === true;
  const n = single ? 1 : (p.burst ?? 3);
  st.lastFire = ctx.tick;
  st.ammo = Math.max(0, (st.ammo ?? mag) - n);

  const snap = { ...ctx };
  for (let i = 0; i < n; i++) {
    const kicker = !single && i === n - 1;
    if (i === 0) fire(snap, kicker);
    else system.runTimeout(() => { try { fire(snap, kicker); } catch { /* ignore */ } },
                           i * (p.burst_gap ?? 3));
  }
  return true;
}

function fire(ctx, kicker) {
  const p = ctx.def.params;
  bolt.fire(ctx, {
    force: true, count: 1,
    damage: p.damage * (kicker ? (p.kicker_mult ?? 1.5) : 1),
    size: kicker ? p.size * 1.7 : p.size,
  });
  if (kicker) {
    vfx.spawn(ctx.dim, "gx:ring_wave", muzzleLoc(ctx),
              { color: ctx.def.palette.glow, size: 1.1, life: 0.35 });
  }
}
