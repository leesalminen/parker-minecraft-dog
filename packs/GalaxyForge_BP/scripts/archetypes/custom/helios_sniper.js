// Twist: sneak-hold 1s steadies the reticle (hold breath); a kill shot beyond 60 blocks
// is a kill-cam beat that slows every mob near the impact for 2 s.

import * as charge from "../charge.js";
import * as vfx from "../../engine/vfx.js";
import { entitiesNear, dist } from "../../engine/ray.js";
import { status } from "../../engine/damage.js";
import { muzzleLoc } from "../hitscan.js";

export function onHold(ctx) {
  const d = ctx.def, st = ctx.st;
  if (ctx.player.isSneaking) {
    st.scratch.breath = (st.scratch.breath ?? 0) + 1;
    if (st.scratch.breath === (d.params.breath_ticks ?? 20)) {
      vfx.spawn(ctx.dim, "gx:ring_wave", muzzleLoc(ctx),
                { color: d.palette.core, size: 0.35, life: 0.4 });
    }
  } else {
    st.scratch.breath = 0;
  }
  return false;                       // let the charge archetype keep charging
}

export function onRelease(ctx) {
  ctx.st.scratch.breath = 0;
  charge.release(ctx);
  return true;
}

export function onHit(ctx, target) {
  if (dist(ctx.point, ctx.player.location) <= 60) return;
  let dead = true;
  try {
    const h = target.getComponent("minecraft:health");
    dead = !h || h.currentValue <= 0;
  } catch { /* removed on death */ }
  if (!dead) return;

  for (const e of entitiesNear(ctx.dim, ctx.point, 6, { excludeTypes: ["minecraft:player"] })) {
    if (e.typeId === "galaxy:pup") continue;
    status(e, "slowness", 40, 1);
  }
  vfx.spawn(ctx.dim, "gx:star_flash", ctx.point,
            { color: ctx.def.palette.core, size: 2.2, life: 0.5 });
}
