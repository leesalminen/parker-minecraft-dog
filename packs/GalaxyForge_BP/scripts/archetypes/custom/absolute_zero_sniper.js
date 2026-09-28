// Twist: the declarative on_hit field seals mobs in a stasis bubble.  Hitting a mob inside
// an armed bubble shatters it early: the bubble is consumed and the shot deals bonus damage
// scaled by how many mobs were frozen inside.

import { fields } from "../../engine/state.js";
import { entitiesNear, dist } from "../../engine/ray.js";
import { hurt } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

const GRACE = 3;                 // ticks before a freshly spawned bubble can be shattered

export function onHit(ctx, target) {
  const near = fields.filter((f) => f.kind === "stasis" && f.dim === ctx.dim &&
                       dist(f.loc, target.location) <= (f.radius ?? 3) + 1.5);
  const armed = near.find((f) => f.gx_born !== undefined && ctx.tick - f.gx_born >= GRACE);
  if (!armed) {                  // first hit: arm the bubble this very shot just spawned
    const fresh = near.find((f) => f.gx_born === undefined);
    if (fresh) fresh.gx_born = ctx.tick;
    return;
  }

  const inside = entitiesNear(ctx.dim, armed.loc, armed.radius + 1, {});
  const mult = 1 + inside.length * (ctx.def.params.shatter_mult ?? 0.5);
  hurt(target, (ctx.def.params.damage ?? 20) * mult, ctx, "magic");
  vfx.spawn(ctx.dim, "gx:crystal_burst", target.location,
            { color: ctx.def.palette.core, size: 1.1, life: 0.5, count: 8, speed: 1.2 });
  vfx.spawn(ctx.dim, "gx:ring_wave", armed.loc,
            { color: ctx.def.palette.glow, size: armed.radius * 2, life: 0.5 });
  const i = fields.indexOf(armed);
  if (i >= 0) fields.splice(i, 1);
}
