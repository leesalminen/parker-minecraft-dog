// Twist: Shadow Marks.  Each hit marks the target (the per-target count lives on the
// entity's dynamic property, because a bolt's onHit context carries no live state bag);
// the fifth mark detonates it in a 3-block shadow burst.

import { isProtected } from "../../engine/safety.js";
import { hurt } from "../../engine/damage.js";
import { entitiesNear } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onHit(ctx, target) {
  if (!target) return;
  if (isProtected(target, ctx.player, {})) return;

  let n = 0;
  try { n = Number(target.getDynamicProperty("gx:shadow_mark")) || 0; } catch { return; }
  n++;

  const loc = target.location;
  if (n < (ctx.def.params.marks ?? 5)) {
    try { target.setDynamicProperty("gx:shadow_mark", n); } catch { /* ignore */ }
    vfx.spawn(ctx.dim, "gx:smoke_trail", loc,
              { color: ctx.def.palette.glow, size: 0.4, life: 0.5, alpha: 0.7 });
    return;
  }

  try { target.setDynamicProperty("gx:shadow_mark", 0); } catch { /* ignore */ }

  const p = ctx.def.params;
  const c = { ...ctx, point: loc };
  vfx.spawn(ctx.dim, "gx:debris_burst", loc,
            { color: ctx.def.palette.core, size: 1.2, life: 0.5, count: 6, speed: 1.2 });
  vfx.spawn(ctx.dim, "gx:ring_wave", loc, { color: ctx.def.palette.glow, size: 1.6, life: 0.4 });
  for (const e of entitiesNear(ctx.dim, loc, p.mark_aoe ?? 3,
                               { excludeTypes: ["minecraft:player"] })) {
    if (!e || isProtected(e, ctx.player, {})) continue;
    hurt(e, p.mark_damage ?? 12, c, "magic");
  }
}
