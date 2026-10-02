// Twist: the storm picks its own targets — after a one-second telegraph ring, three
// strikes land on the nearest mob inside the circle (mobs standing in water take +50%).

import { system } from "@minecraft/server";
import * as vfx from "../../engine/vfx.js";
import * as sound from "../../engine/sound.js";
import { raycast, entitiesNear, dist } from "../../engine/ray.js";
import { hurt, status } from "../../engine/damage.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 40)) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return true; }
  st.lastFire = ctx.tick;
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  if (p.cooldown) st.cooldown = p.cooldown * 20;

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 80, { ignoreId: ctx.player.id });
  const cast = { ...ctx, point: r.point || { ...ctx.eye } };

  vfx.spawn(ctx.dim, "gx:ring_wave", cast.point,
            { color: d.palette.glow, size: p.strike_radius ?? 5, life: 1.0 });
  vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette,
             { size: p.muzzle_size ?? 0.8, effect: d.vfx.muzzle });
  sound.play(ctx.player, d.sound);

  const lead = p.telegraph_ticks ?? 20;
  for (let i = 0; i < (p.strikes ?? 3); i++) {
    system.runTimeout(() => { try { strike(cast); } catch { /* ignore */ } },
                      lead + i * (p.strike_gap ?? 10));
  }
  return true;                                   // the archetype never throws a bolt
}

function strike(ctx) {
  const d = ctx.def, p = d.params;
  const near = entitiesNear(ctx.dim, ctx.point, p.strike_radius ?? 5,
                            { excludeTypes: ["minecraft:player"] });
  let best = null, bestD = Infinity;
  for (const e of near) {
    const dd = dist(e.location, ctx.point);
    if (dd < bestD) { bestD = dd; best = e; }
  }
  const at = best ? { ...best.location } : { ...ctx.point };

  vfx.line(ctx.dim, { x: at.x, y: at.y + 10, z: at.z }, at, "gx:lightning_fork", d.palette,
           { step: 1.2, max: 12, size: 0.7, life: 0.3 });
  vfx.spawn(ctx.dim, "gx:lightning_fork", at, { color: d.palette.core, size: 1.6, life: 0.35 });
  vfx.impact(ctx.dim, at, d.palette, { radius: 1.8, sparks: 6 });
  sound.play(ctx.player, [["ambient.weather.thunder", 0.6, 1.2, 0]]);

  for (const e of near) {
    const c = { ...ctx, point: e.location };
    let dmg = p.strike_dmg ?? 6;
    if (isWet(ctx.dim, e.location)) dmg *= p.wet_mult ?? 1.5;
    hurt(e, dmg, c, "lightning");
    status(e, "slowness", p.strike_stun ?? 10, 1);
    vfx.spawn(ctx.dim, "gx:static_arc", e.location,
              { color: d.palette.core, size: 0.9, life: 0.25 });
  }
}

function isWet(dim, loc) {
  try {
    const b = dim.getBlock({ x: Math.floor(loc.x), y: Math.floor(loc.y), z: Math.floor(loc.z) });
    return !!b && (b.typeId === "minecraft:water" || b.typeId === "minecraft:flowing_water");
  } catch { return false; }
}
