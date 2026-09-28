// field: persistent zones (singularity, sun-scar, magma pool, stasis bubble, whiteout).
// Zones are plain data; they pull / push, tick damage and apply statuses, then collapse.

import { fields } from "../engine/state.js";
import { add, norm, dist, entitiesNear } from "../engine/ray.js";
import { hurt, status, knock } from "../engine/damage.js";
import { isProtected } from "../engine/safety.js";
import * as vfx from "../engine/vfx.js";

export function press() {}
export function hold() {}
export function release() {}
export function idle() {}

export function tickFields() {
  for (let i = fields.length - 1; i >= 0; i--) {
    const f = fields[i];
    if (f.life-- <= 0) { collapse(f); fields.splice(i, 1); continue; }

    // visuals
    if (f.life % 4 === 0) {
      vfx.spawn(f.dim, "gx:field_glow", f.loc, { color: f.color, size: f.radius * 2, life: 0.6, alpha: 0.3 });
    }
    if (f.pull || f.push || f.dps || f.extra?.status) {
      const near = entitiesNear(f.dim, f.loc, f.radius, {});
      const c = { player: { id: f.ownerId, location: f.loc, dimension: f.dim }, dim: f.dim,
                  def: { palette: { glow: f.color } }, st: {}, point: f.loc, pvp: false };
      for (const e of near) {
        if (!e || isProtected(e, null, {})) continue;
        const to = norm({ x: f.loc.x - e.location.x, y: f.loc.y - e.location.y, z: f.loc.z - e.location.z });
        if (f.pull) knock(e, c, f.pull, "toward");
        if (f.push) knock(e, c, f.push, "away");
        if (f.dps && f.life % 20 === 0) hurt(e, f.dps, c, "magic");
        if (f.extra?.status && f.life % 20 === 0) {
          for (const s of f.extra.status) status(e, s.id, s.ticks ?? 40, s.amp ?? 0);
        }
      }
    }
    if (f.extra?.spawn && f.life % 20 === 0) {
      const a = Math.random() * Math.PI * 2;
      const p = { x: f.loc.x + Math.cos(a) * f.radius, y: f.loc.y + 0.4, z: f.loc.z + Math.sin(a) * f.radius };
      vfx.spawn(f.dim, f.extra.spawn, p, { color: f.color, size: 0.5, life: 0.6, count: 1, speed: 0.6 });
    }
  }
}

function collapse(f) {
  if (!f.extra?.collapse) return;
  vfx.spawn(f.dim, "gx:star_flash", f.loc, { color: f.color, size: f.radius, life: 0.4 });
  vfx.spawn(f.dim, "gx:ring_wave", f.loc, { color: f.color, size: f.radius * 1.4, life: 0.6 });
  const near = entitiesNear(f.dim, f.loc, f.radius + 1, {});
  const c = { player: { id: f.ownerId, location: f.loc, dimension: f.dim }, dim: f.dim,
              def: { palette: { glow: f.color } }, st: {}, point: f.loc, pvp: false };
  for (const e of near) {
    if (!e || isProtected(e, null, {})) continue;
    if (f.extra.collapse.dmg) hurt(e, f.extra.collapse.dmg, c, "explosion");
    knock(e, c, f.extra.collapse.knock ?? 1.2, "away");
  }
}
