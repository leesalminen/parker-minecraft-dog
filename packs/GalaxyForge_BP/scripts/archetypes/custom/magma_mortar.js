// Twist: pools merge.  A blob landing within 3 blocks of an existing magma pool grows it
// (+1 radius, +4 s) instead of stacking a second pool; mobs inside get Molten (Weakness).

import { fields } from "../../engine/state.js";
import { spawnField } from "../../engine/damage.js";
import { entitiesNear, dist } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onDetonate(c, b, loc) {
  const p = b.def.params;
  const pool = fields.find((f) => f.kind === "magma_pool" && f.dim === c.dim &&
                                  dist(f.loc, loc) <= (p.merge_radius ?? 3));
  if (pool) {
    pool.radius = Math.min(p.pool_max_radius ?? 6, pool.radius + (p.pool_grow ?? 1));
    pool.life = Math.min(p.pool_max_life ?? 240, pool.life + (p.pool_extend ?? 80));
    b.onHit = null;                                 // merged: no second pool at this spot
    vfx.spawn(c.dim, "gx:ring_wave", loc,
              { color: b.pal.glow, size: pool.radius * 1.6, life: 0.5 });
    return;
  }
  // Fresh landing: the declarative on_hit field pools the spot per mob it catches, so make
  // sure the ground still gets one when the blast caught nothing.
  if (!entitiesNear(c.dim, loc, b.aoe ?? 4, { excludeTypes: ["minecraft:player"] }).length) {
    spawnField({ ...c, point: loc }, "magma_pool",
               { radius: p.pool_radius ?? 3, life: p.pool_life ?? 100, dps: p.pool_dps ?? 4,
                 extra: { status: [{ id: "weakness", ticks: 40, amp: 0 }],
                          spawn: "gx:ember_trail" } });
    b.onHit = null;
  }
}
