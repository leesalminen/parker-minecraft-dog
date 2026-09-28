// Twist: three meteor charges, one refilling every 12 s.  A marker beam paints the spot;
// 1 s later five meteors streak down over 3 s, each landing with a 4-block crater.

import { system } from "@minecraft/server";
import * as hitscan from "../hitscan.js";
import * as vfx from "../../engine/vfx.js";
import { raycast, add, entitiesNear } from "../../engine/ray.js";
import { hurt } from "../../engine/damage.js";
import { isProtected } from "../../engine/safety.js";
import { GLYPHS } from "../../generated/weapons.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const max = p.charges ?? 3;
  if (st.charges === undefined) st.charges = max;
  if (st.reload > 0 || st.cooldown > 0) return true;
  if (ctx.tick - st.lastFire < (p.rate ?? 40)) return true;
  if (st.charges <= 0) {
    try { ctx.player.onScreenDisplay.updateSubtitle(GLYPHS.hourglass); } catch { /* ignore */ }
    return true;
  }

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 90);
  const point = r.point || add(ctx.eye, ctx.view, p.range ?? 90);
  if (!hitscan.shot(ctx)) return true;              // the marker beam itself

  st.charges--;
  if (st.charges < max) refill(ctx);
  st.cooldown = p.inbound_ticks ?? 20;              // meteors inbound in 1 s
  meteors(ctx, point);
  return true;
}

/** One charge every `refill_ticks`, driven by a self-rescheduling timeout. */
function refill(ctx) {
  const d = ctx.def, st = ctx.st, max = d.params.charges ?? 3;
  if (st.scratch.refilling) return;
  st.scratch.refilling = true;
  const step = () => {
    try {
      st.charges = Math.min(max, (st.charges ?? 0) + 1);
      if (st.charges < max) system.runTimeout(step, d.params.refill_ticks ?? 240);
      else st.scratch.refilling = false;
    } catch { /* ignore */ }
  };
  system.runTimeout(step, d.params.refill_ticks ?? 240);
}

function meteors(ctx, point) {
  const d = ctx.def, p = d.params;
  const n = p.meteor_count ?? 5, gap = p.meteor_gap ?? 15, spread = p.meteor_spread ?? 6;
  const aoe = p.meteor_aoe ?? 4;
  for (let i = 0; i < n; i++) {
    system.runTimeout(() => {
      try {
        const loc = { x: point.x + (Math.random() - 0.5) * spread, y: point.y,
                      z: point.z + (Math.random() - 0.5) * spread };
        vfx.line(ctx.dim, { x: loc.x, y: loc.y + 24, z: loc.z }, loc, "gx:ember_trail",
                 d.palette, { step: 1.0, max: 30, size: 0.7, life: 0.35 });
        vfx.impact(ctx.dim, loc, d.palette, { radius: aoe, sparks: 8 });
        vfx.spawn(ctx.dim, "gx:field_glow", loc,
                  { color: d.palette.glow, size: aoe * 2, life: 0.6, alpha: 0.3 });
        const c = { ...ctx, point: loc };
        for (const e of entitiesNear(ctx.dim, loc, aoe, { excludeTypes: ["minecraft:player"] })) {
          if (isProtected(e, ctx.player, { pvp: false })) continue;
          hurt(e, p.meteor_damage ?? 12, c, "explosion");
        }
      } catch { /* ignore */ }
    }, (p.marker_delay ?? 20) + i * gap);
  }
}
