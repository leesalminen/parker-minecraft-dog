// Per-player weapon state, the global tick budget, and the live effect registries.
// Everything here is in-memory; persistent per-item data (ammo/heat) lives on the
// ItemStack via setDynamicProperty and is written on unequip / fire-end, not per tick.

export const CAP = { particles: 60, rays: 24, queries: 8 };

/** Hard ceiling on live script projectiles; the oldest are dropped past it. */
export const MAX_PROJECTILES = 160;

export const budget = { particles: 0, rays: 0, queries: 0 };
export const players = new Map();
export const projectiles = [];   // script-simulated bolts (no entity)
export const fields = [];        // persistent zones (singularity, sun-scar, magma pool...)
export const deployables = [];   // drones and turrets

export let tick = 0;

export function beginTick() {
  tick++;
  budget.particles = 0;
  budget.rays = 0;
  budget.queries = 0;
}

export function spend(kind, n = 1) {
  if (budget[kind] + n > CAP[kind]) return false;
  budget[kind] += n;
  return true;
}

export function getState(player) {
  let s = players.get(player.id);
  if (!s) {
    s = {
      id: player.id, def: null, itemId: null,
      using: false, press: false, release: false, useStart: 0,
      heat: 0, cool: 0, charge: 0, lastFire: -999, shotsInBurst: 0,
      reload: 0, cooldown: 0, vent: 0, ventZone: false, boost: 0,
      zoom: 0, aim: false, mode: 0, scratch: {}, custom: null,
      hudCache: "", scopeCache: "", overlayUntil: 0,
    };
    players.set(player.id, s);
  }
  return s;
}

export function dropState(id) { players.delete(id); }

export function forEachPlayer(fn) { for (const s of players.values()) fn(s); }
