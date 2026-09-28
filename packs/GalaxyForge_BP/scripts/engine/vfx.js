// Particle spawning. Colour / size / lifetime / count / speed are pushed through
// MolangVariableMap into the shared templates in RP/particles, so one effect name serves
// every palette. Every spawn is charged against the 60-particles-per-tick budget.

import { MolangVariableMap } from "@minecraft/server";
import { spend } from "./state.js";

export function spawn(dim, effect, loc, o = {}) {
  if (!spend("particles")) return false;
  const m = new MolangVariableMap();
  const c = o.color || [1, 1, 1];
  try {
    m.setColorRGBA("color", { red: c[0], green: c[1], blue: c[2], alpha: o.alpha ?? 1 });
    m.setFloat("size", o.size ?? 0.25);
    m.setFloat("life", o.life ?? 0.4);
    m.setFloat("count", o.count ?? 1);
    m.setFloat("speed", o.speed ?? 0.4);
    dim.spawnParticle(effect, loc, m);
    return true;
  } catch { return false; }
}

export function burst(dim, effect, loc, n, o = {}) {
  let k = 0;
  for (let i = 0; i < n; i++) if (spawn(dim, effect, loc, o)) k++;
  return k;
}

/** Standard impact package: flash + shockwave + sparks + lingering scorch. */
export function impact(dim, loc, pal, o = {}) {
  const c = o.color || pal.glow;
  const r = o.radius ?? 1.2;
  spawn(dim, "gx:star_flash", loc, { color: pal.core, size: r * 1.4, life: 0.18 });
  spawn(dim, "gx:ring_wave", loc, { color: c, size: r, life: 0.35 });
  burst(dim, "gx:spark_burst", loc, o.sparks ?? 5,
        { color: c, size: r * 0.35, life: 0.5, count: o.sparks ?? 5, speed: 1.4 });
  spawn(dim, "gx:smoke_trail", loc, { color: pal.trail, size: r * 0.5, life: 0.9 });
}

/** Muzzle flash package: shape + colour are per weapon. */
export function muzzle(dim, loc, pal, o = {}) {
  spawn(dim, o.effect || "gx:muzzle_flash", loc, { color: pal.core, size: o.size ?? 0.5, life: 0.16,
                                                   count: o.count ?? 3, speed: 0.4 });
  spawn(dim, "gx:star_flash", loc, { color: pal.glow, size: (o.size ?? 0.5) * 1.2, life: 0.12 });
}

/** Beam / bolt body particle at a point along the path. */
export function body(dim, loc, effect, pal, o = {}) {
  spawn(dim, effect, loc, { color: pal.core, size: o.size ?? 0.35, life: o.life ?? 0.2 });
  spawn(dim, "gx:orb_soft_orb", loc, { color: pal.glow, size: (o.size ?? 0.35) * 1.6,
                                       life: o.life ?? 0.2, alpha: 0.55 });
}

export function trailPoint(dim, loc, effect, pal, o = {}) {
  spawn(dim, effect, loc, { color: pal.trail, size: o.size ?? 0.3, life: o.life ?? 0.6 });
}

export function lerp(a, b, t) {
  return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, z: a.z + (b.z - a.z) * t };
}

/**
 * Chain of billboard particles along a segment (tracer / beam body).
 * Spaced ~`step` blocks, capped at `max` particles per call (the prompt's ~40).
 */
export function line(dim, a, b, effect, pal, o = {}) {
  const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
  const d = Math.sqrt(dx * dx + dy * dy + dz * dz);
  const step = o.step ?? 0.5;
  const n = Math.min(o.max ?? 40, Math.max(1, Math.round(d / step)));
  let made = 0;
  for (let i = 0; i < n; i++) {
    const t = (i + 0.5) / n;
    if (spawn(dim, effect, lerp(a, b, t), { color: pal.core, size: o.size ?? 0.3, life: o.life ?? 0.2 })) made++;
  }
  return made;
}
