// Twist: the disc boomerangs home after 25 blocks, and a mid-air re-press splits it
// into three (the parent becomes the three, so exactly three fly on).

import * as bolt from "../bolt.js";
import { projectiles } from "../../engine/state.js";
import { dist } from "../../engine/ray.js";
import * as vfx from "../../engine/vfx.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params;
  if (ctx.repeat) return false;                  // holding the trigger just throws more discs
  const air = projectiles.filter((b) => b.def === d && b.ownerId === ctx.player.id && b.life > 0
                                        && b.splits < (p.max_splits ?? 1));
  if (!air.length) return false;                 // nothing splittable out there: throw a disc
  for (const b of air) {
    b.returning = false;                         // the three fly on, they are not caught
    bolt.splitBolt(b, p.split ?? 3, { spread: p.split_spread ?? 26, life: p.split_life ?? 30 });
    b.life = 0;                                  // the parent becomes the three
  }
  vfx.spawn(ctx.dim, "gx:star_flash", ctx.eye,
            { color: d.palette.core, size: 0.8, life: 0.25 });
  return true;
}

export function onTick(c, b) {
  const p = c.def.params;
  if (!b.returning && dist(b.loc, b.origin) >= (p.boomerang ?? 25)) {
    b.returning = true;
    b.vel = { x: -b.vel.x, y: -b.vel.y, z: -b.vel.z };
    vfx.spawn(b.dim, "gx:ring_wave", b.loc, { color: b.pal.core, size: 1.2, life: 0.35 });
  }
  if (b.returning && dist(b.loc, b.origin) < (p.catch_radius ?? 2)) {
    vfx.spawn(b.dim, "gx:star_flash", b.loc, { color: b.pal.core, size: 1.4, life: 0.3 });
    b.life = 0;                                  // caught: the disc is back in hand
  }
}
