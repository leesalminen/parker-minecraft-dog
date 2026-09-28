// Twist: the launched orb is bent by any live singularity field, so your own bolts curve
// into the well instead of flying straight past it.

import { fields } from "../../engine/state.js";
import { norm, dist } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onTick(c, b) {
  const p = c.def.params;
  const range = p.bend_range ?? 18;

  let well = null, best = Infinity;
  for (const f of fields) {
    if (f.kind !== "singularity") continue;
    const d = dist(b.loc, f.loc);
    if (d < best) { best = d; well = f; }
  }
  if (!well || best > range) return;

  // Add a pull vector toward the well centre; the strength ramps up as the bolt closes in.
  // Adding (not re-aiming) means a bolt fired straight away is decelerated and turned
  // around, while one flying past is curved in.
  const to = norm({ x: well.loc.x - b.loc.x, y: well.loc.y - b.loc.y, z: well.loc.z - b.loc.z });
  const s = Math.sqrt(b.vel.x ** 2 + b.vel.y ** 2 + b.vel.z ** 2) || 1;
  const k = (p.bend ?? 0.35) * (1 - best / range) * s;
  let vx = b.vel.x + to.x * k, vy = b.vel.y + to.y * k, vz = b.vel.z + to.z * k;
  const ns = Math.sqrt(vx * vx + vy * vy + vz * vz) || 1;
  const cap = s * 1.5;
  if (ns > cap) { const f = cap / ns; vx *= f; vy *= f; vz *= f; }
  b.vel = { x: vx, y: vy, z: vz };

  if (best < (well.radius ?? 6) && b.life % 3 === 0) {
    vfx.spawn(b.dim, "gx:swirl", b.loc,
              { color: b.pal.core, size: b.size, life: 0.3, count: 1, speed: 0.5 });
  }
}
