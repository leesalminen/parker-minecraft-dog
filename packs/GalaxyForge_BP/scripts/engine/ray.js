// Raycasts. Every raycast is charged against the per-tick budget (CAP.rays = 8), so a
// busy tick can never stall the script watchdog.

import { spend } from "./state.js";

export function add(a, b, s = 1) { return { x: a.x + b.x * s, y: a.y + b.y * s, z: a.z + b.z * s }; }

export function sub(a, b) { return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z }; }

export function len(v) { return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z); }

export function norm(v) {
  const l = len(v) || 1;
  return { x: v.x / l, y: v.y / l, z: v.z / l };
}

export function dist(a, b) { return len(sub(a, b)); }

/** Random cone spread around a direction (small angles). */
export function spreadDir(dir, degrees) {
  if (!degrees) return dir;
  const a = (Math.random() - 0.5) * 2 * (degrees * Math.PI / 180);
  const b = (Math.random() - 0.5) * 2 * (degrees * Math.PI / 180);
  const right = norm({ x: dir.z, y: 0, z: -dir.x });
  return norm(add(add(dir, right, Math.tan(a)), { x: 0, y: 1, z: 0 }, Math.tan(b)));
}

export function eyeOf(player) {
  try { return player.getHeadLocation(); } catch { return player.location; }
}

export function viewOf(player) {
  try { return player.getViewDirection(); } catch { return { x: 0, y: 0, z: 1 }; }
}

export function blockCenter(loc) { return { x: loc.x + 0.5, y: loc.y + 0.5, z: loc.z + 0.5 }; }

/** Cast one ray. Returns the nearest entity / block / impact point along it. */
export function raycast(dim, origin, dir, maxDist, opts = {}) {
  const res = { point: null, entity: null, block: null, face: undefined, dist: maxDist, hits: [], capped: false };
  if (!spend("rays")) { res.capped = true; res.point = add(origin, dir, maxDist); return res; }

  let blockDist = maxDist;
  try {
    const h = dim.getBlockFromRay(origin, dir, {
      maxDistance: maxDist, includeLiquidBlocks: !!opts.liquids, includePassableBlocks: !!opts.passable,
    });
    if (h) {
      res.block = h.block;
      res.face = h.face ?? h.blockFace ?? undefined;
      blockDist = h.faceLocation ? dist(origin, h.faceLocation) : dist(origin, blockCenter(h.block.location));
    }
  } catch { /* unloaded chunk */ }

  if (!opts.noEntities) {
    try {
      const hits = dim.getEntitiesFromRay(origin, dir, { maxDistance: maxDist });
      for (const h of hits) {
        const e = h.entity;
        if (!e || e.id === opts.ignoreId) continue;
        const d = typeof h.distance === "number" ? h.distance : dist(origin, e.location);
        if (d > blockDist) continue;
        res.hits.push({ entity: e, dist: d });
      }
      res.hits.sort((a, b) => a.dist - b.dist);
      if (res.hits.length) { res.entity = res.hits[0].entity; }
    } catch { /* ignore */ }
  }

  const entityDist = res.hits.length ? res.hits[0].dist : maxDist;
  res.dist = Math.min(blockDist, entityDist);
  res.point = add(origin, dir, res.dist);
  return res;
}

/** Where the aim dot lands (block or entity surface, whichever is first). */
export function dotPoint(dim, origin, dir, maxDist) {
  const r = raycast(dim, origin, dir, maxDist, {});
  return r.point;
}

export function entitiesNear(dim, loc, radius, opts = {}) {
  if (!spend("queries")) return [];
  try {
    return dim.getEntities({ location: loc, maxDistance: radius, ...opts });
  } catch { return []; }
}
