// Twist: the slug's shockwave ring knocks everything near the path away, and the crossing
// scars a glowing glass tunnel (block changes only run while mobGriefing is true).

import * as vfx from "../../engine/vfx.js";
import { entitiesNear } from "../../engine/ray.js";
import { knock, grief } from "../../engine/damage.js";
import { mobGriefing } from "../../engine/safety.js";

export function onHit(ctx, target) {
  const p = ctx.def.params;
  const at = target?.location ?? ctx.point;
  for (const e of entitiesNear(ctx.dim, at, p.knock_radius ?? 3.5,
                               { excludeTypes: ["minecraft:player"] })) {
    knock(e, ctx, p.knock ?? 1.4, "away");
  }
  vfx.spawn(ctx.dim, "gx:shock_disc", at,
            { color: ctx.def.palette.glow, size: p.knock_radius ?? 3.5, life: 0.5 });
  if (mobGriefing()) grief({ ...ctx, point: at }, p.grief ?? { radius: 2, to: "minecraft:glass", cap: 20 });
}
