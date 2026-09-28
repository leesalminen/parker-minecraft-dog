// Twist: turrets of the same owner that share their 16-block line of sight sync fire,
// adding 25% damage on every shot while both stand.  Distance stands in for the
// line-of-sight check (the deploy tick already spends its raycast budget on targeting).

import { deployables } from "../../engine/state.js";
import { dist } from "../../engine/ray.js";
import { hurt } from "../../engine/damage.js";

export function onDeployHit(ctx, target, entity) {
  const p = ctx.def.params;
  const sync = p.sync_range ?? 16;
  let linked = false;
  for (const u of deployables) {
    if (u.entity === entity || u.kind !== p.entity || u.ownerId !== ctx.player.id) continue;
    try { if (dist(u.entity.location, entity.location) <= sync) { linked = true; break; } }
    catch { /* sibling already removed */ }
  }
  if (!linked) return;
  const shot = (p.dps ?? 8) * (p.interval ?? 10) / 20;
  hurt(target, shot * (p.sync_mult ?? 0.25), ctx, "projectile");
}
