// Twist: a shard that sticks grows into a 3-spike crystal cluster that slows every mob
// within 3 blocks for 6 s.  Declared as a field so the slow persists after the shard fuses.

import { spawnField } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

export function onDetonate(c, b, loc) {
  const p = b.def.params;
  spawnField({ ...c, point: loc }, "crystal_cluster",
             { radius: p.cluster_radius ?? 3, life: p.cluster_life ?? 120, dps: 0,
               extra: { status: [{ id: "slowness", ticks: 120, amp: 1 }],
                        spawn: "gx:crystal_burst" } });
  vfx.spawn(c.dim, "gx:crystal_burst", loc,
            { color: b.pal.core, size: 0.8, life: 0.5, count: 5, speed: 1.0 });
}
