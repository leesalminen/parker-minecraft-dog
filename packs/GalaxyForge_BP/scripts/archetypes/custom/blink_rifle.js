// Twist: the orb teleports you to its impact point (safe-spot search, 5 s cooldown from
// the def).  Aiming fires a swap shot instead: you and the mob you hit trade places.

import { world } from "@minecraft/server";
import * as bolt from "../bolt.js";
import { projectiles } from "../../engine/state.js";
import { isProtected } from "../../engine/safety.js";
import * as vfx from "../../engine/vfx.js";

const SEARCH = 2;      // safe-spot search radius, in blocks

export function onPress(ctx) {
  const fired = bolt.fire(ctx);
  if (!fired) return true;
  const b = projectiles[projectiles.length - 1];
  if (b && b.def === ctx.def && b.ownerId === ctx.player.id) b.swap = ctx.st.aim === true;
  return true;
}

export function onDetonate(ctx, b, loc) {
  if (b.swap) return;
  const player = livePlayer(ctx.player.id);
  if (!player) return;
  const dest = safeSpot(b.dim, loc);
  if (!dest) return;

  vfx.spawn(b.dim, "gx:star_flash", b.origin, { color: b.pal.core, size: 1.2, life: 0.3 });
  try { player.teleport(dest); } catch { return; }
  vfx.line(b.dim, b.origin, dest, "gx:beam_needle", b.pal,
           { step: 0.8, max: 24, size: 0.2, life: 0.35 });
  vfx.spawn(b.dim, "gx:star_flash", dest, { color: b.pal.core, size: 1.2, life: 0.3 });
}

export function onHit(ctx, target, b) {
  if (!b || !b.swap) return;
  if (isProtected(target, ctx.player, {})) return;
  const player = livePlayer(ctx.player.id);
  if (!player) return;
  const dest = safeSpot(target.dimension, target.location);
  if (!dest) return;

  const mine = { ...player.location };
  try { target.teleport(mine); } catch { return; }
  try { player.teleport(dest); } catch { /* ignore */ }
  vfx.spawn(b.dim, "gx:star_flash", mine, { color: b.pal.core, size: 1.0, life: 0.3 });
  vfx.spawn(b.dim, "gx:star_flash", dest, { color: b.pal.core, size: 1.0, life: 0.3 });
}

/** The bolt context only carries the owner id, so resolve the real Player by id. */
function livePlayer(id) {
  try { return world.getAllPlayers().find((p) => p.id === id) ?? null; } catch { return null; }
}

/** Nearest two-air-block pocket with solid ground under it (never the void, never a wall). */
function safeSpot(dim, loc) {
  const x0 = Math.floor(loc.x), y0 = Math.floor(loc.y), z0 = Math.floor(loc.z);
  for (let r = 0; r <= SEARCH; r++) {
    for (let dx = -r; dx <= r; dx++) {
      for (let dz = -r; dz <= r; dz++) {
        for (let dy = 0; dy <= 2; dy++) {
          const base = { x: x0 + dx, y: y0 + dy, z: z0 + dz };
          if (!clear(dim, base)) continue;
          if (!solid(dim, { x: base.x, y: base.y - 1, z: base.z })) continue;
          return { x: base.x + 0.5, y: base.y, z: base.z + 0.5 };
        }
      }
    }
  }
  return null;
}

function clear(dim, loc) {
  try {
    const feet = dim.getBlock(loc);
    const head = dim.getBlock({ x: loc.x, y: loc.y + 1, z: loc.z });
    return !!feet && !!head && feet.isAir && head.isAir;
  } catch { return false; }
}

function solid(dim, loc) {
  try { const b = dim.getBlock(loc); return !!b && !b.isAir; } catch { return false; }
}
