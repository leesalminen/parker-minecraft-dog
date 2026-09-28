// Twist: the nanite cloud flocks toward the nearest mob, re-seeks the next one after each
// kill, and dissolves after three targets.

import { entitiesNear, norm, dist } from "../../engine/ray.js";

function nearest(dim, loc, range, skipId, ownerId) {
  const near = entitiesNear(dim, loc, range, { excludeTypes: ["minecraft:player"] });
  let best = null, bestD = Infinity;
  for (const e of near) {
    if (!e || e.id === ownerId || e.id === skipId) continue;
    const d = dist(loc, e.location);
    if (d < bestD) { bestD = d; best = e; }
  }
  return best;
}

function steer(b, t, p, flock) {
  const s = Math.sqrt(b.vel.x ** 2 + b.vel.y ** 2 + b.vel.z ** 2) || 1;
  const to = norm({ x: t.location.x - b.loc.x, y: (t.location.y + 0.9) - b.loc.y,
                    z: t.location.z - b.loc.z });
  const turn = p.homing_turn ?? 0.35;
  const side = norm({ x: -to.z, y: 0, z: to.x });
  const swirl = flock ? Math.sin((b.life ?? 0) * 0.6) * flock : 0;
  const nv = norm({ x: b.vel.x / s + to.x * turn + side.x * swirl,
                    y: b.vel.y / s + to.y * turn,
                    z: b.vel.z / s + to.z * turn + side.z * swirl });
  b.vel = { x: nv.x * s, y: nv.y * s, z: nv.z * s };
}

export function onTick(c, b) {
  const p = c.def.params;
  const t = nearest(b.dim, b.loc, p.homing ?? 30, null, b.ownerId);
  if (!t) return;
  if (b.targetId !== t.id) { b.targetId = t.id; b.retargets = (b.retargets ?? 0) + 1; }
  steer(b, t, p, p.flock ?? 0.3);            // flocking: a slight curl keeps the cloud loose
}

export function onHit(c, target, b) {
  const p = c.def.params;
  if ((b.retargets ?? 0) >= (p.max_retargets ?? 3)) { b.pierce = 0; return; }  // dissolve
  b.pierce = Math.max(1, b.pierce);          // hitBolt's pierce branch keeps it flying
  const next = nearest(b.dim, target.location, p.retarget_range ?? 8, target.id, b.ownerId);
  if (next) steer(b, next, p, 0);            // re-home; onTick books the new target
}
