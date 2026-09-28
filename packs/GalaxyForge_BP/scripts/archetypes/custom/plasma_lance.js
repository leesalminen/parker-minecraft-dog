// Twist: three energy rings travel down the beam after it fires; each applies a separate
// shockwave hit at the first mob it reaches.

import { system } from "@minecraft/server";
import * as vfx from "../../engine/vfx.js";
import { entitiesNear } from "../../engine/ray.js";
import { hurt } from "../../engine/damage.js";

export function onHit(ctx, target) {
  const p = ctx.def.params;
  const rings = p.rings ?? 3;
  const loc = { ...target.location };
  const base = p.tiers?.[1]?.damage ?? 10;
  for (let i = 0; i < rings; i++) {
    system.runTimeout(() => {
      try {
        vfx.spawn(ctx.dim, "gx:shock_disc", loc, { color: ctx.def.palette.glow, size: 3.0, life: 0.5 });
        const near = entitiesNear(ctx.dim, loc, 3, {});
        const c = { ...ctx, point: loc };
        for (const e of near) hurt(e, base * 0.35, c, "magic");
      } catch { /* ignore */ }
    }, (i + 1) * 4);
  }
}
