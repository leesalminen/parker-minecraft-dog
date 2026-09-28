// Twist: the channel widens the cone over time.  The angle lives in st.scratch.angle and
// drives an extra push on mobs inside the growing wedge, plus a settling snowdrift.

import { knock } from "../../engine/damage.js";
import { add, norm, entitiesNear } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onPress(ctx) {
  ctx.st.scratch.angle = ctx.def.params.angle ?? 90;
  return false;                                     // the cone archetype owns the first spray
}

export function onHold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const base = p.angle ?? 90;
  st.scratch.angle = Math.min(p.max_angle ?? 140, (st.scratch.angle ?? base) + (p.widen_step ?? 0.7));
  const half = (st.scratch.angle / 2) * Math.PI / 180;
  const range = p.range ?? 12;
  const cosLimit = Math.cos(half);

  // Push everything inside the (now wider) wedge away from the muzzle.
  if (ctx.tick % 4 === 0) {
    const near = entitiesNear(ctx.dim, add(ctx.eye, ctx.view, range * 0.5), range + 1,
                              { excludeTypes: ["minecraft:player"] });
    for (const e of near) {
      const to = norm({ x: e.location.x - ctx.eye.x, y: (e.location.y + 0.9) - ctx.eye.y,
                        z: e.location.z - ctx.eye.z });
      if (to.x * ctx.view.x + to.y * ctx.view.y + to.z * ctx.view.z < cosLimit) continue;
      knock(e, ctx, p.knock ?? 0.45, "away");
    }
  }

  // Snowdrift: motes settle on the ground across the widening fan.
  if (ctx.tick % 3 === 0) {
    const right = norm({ x: ctx.view.z, y: 0, z: -ctx.view.x });
    const a = (Math.random() - 0.5) * 2 * half;
    const dir = norm(add(ctx.view, right, Math.tan(a)));
    const at = add(add(ctx.eye, dir, 1 + Math.random() * range), { x: 0, y: -0.9, z: 0 });
    vfx.spawn(ctx.dim, "gx:snow_mote", at,
              { color: d.palette.core, size: 0.5, life: 0.8, count: 2, speed: 0.5 });
  }
  return false;                                     // let the cone archetype deal damage/slow
}

export function onRelease(ctx) {
  ctx.st.scratch.angle = ctx.def.params.angle ?? 90;
  return false;
}
