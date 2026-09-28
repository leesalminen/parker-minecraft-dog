// chain: an arc that jumps between the N nearest targets, with falloff per jump.

import { raycast, add, norm, dist, entitiesNear } from "../engine/ray.js";
import { applyEffects, hurt } from "../engine/damage.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import { muzzleLoc } from "./hitscan.js";

export function press(ctx) { arc(ctx); }
export function hold(ctx) { if (ctx.def.params.auto) arc(ctx); }
export function release() {}
export function idle() {}

export function arc(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 8)) return false;
  if (st.reload > 0 || st.cooldown > 0) return false;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return false; }
  if (d.heat && heat.isHot(st, d)) return false;
  st.lastFire = ctx.tick;
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  heat.add(st, d, d.heat?.per_shot ?? 0);
  const cd = p.cooldown ?? d.cooldown;
  if (cd) st.cooldown = cd * 20;

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 20);
  let src = r.entity;
  const c = { ...ctx, point: r.point };

  if (!src) {
    // No direct target: still draw the arc into the air so the weapon reads.
    vfx.line(ctx.dim, muzzleLoc(ctx), r.point, d.vfx.body, d.palette,
             { step: 0.6, max: 30, size: 0.3 });
    vfx.spawn(ctx.dim, "gx:lightning_fork", r.point, { color: d.palette.core, size: 0.9, life: 0.25 });
    vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette, { size: p.muzzle_size ?? 0.5 });
    sound.play(ctx.player, d.sound);
    return true;
  }

  let dmg = p.damage ?? 8;
  const jumps = p.jumps ?? 4;
  const radius = p.radius ?? 6;
  const falloff = p.falloff ?? 0.85;
  const seen = new Set([src.id]);

  vfx.line(ctx.dim, muzzleLoc(ctx), src.location, d.vfx.body, d.palette,
           { step: 0.6, max: 30, size: 0.3 });
  vfx.spawn(ctx.dim, "gx:static_arc", src.location, { color: d.palette.core, size: 1.0, life: 0.25 });

  for (let i = 0; i <= jumps; i++) {
    const cc = { ...ctx, point: src.location };
    applyEffects(cc, d.hooks?.on_hit, src);
    hurt(src, dmg, cc, "lightning");
    if (d.custom?.onHit) { try { d.custom.onHit(cc, src); } catch { /* ignore */ } }
    const near = entitiesNear(ctx.dim, src.location, radius, { excludeTypes: ["minecraft:player"] });
    const next = near.find((e) => e && !seen.has(e.id));
    if (!next) break;
    vfx.line(ctx.dim, src.location, next.location, "gx:lightning_fork", d.palette,
             { step: 0.6, max: 20, size: 0.5, life: 0.2 });
    seen.add(next.id);
    src = next;
    dmg *= falloff;
  }

  vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette, { size: p.muzzle_size ?? 0.5, effect: d.vfx.muzzle });
  sound.play(ctx.player, d.sound);
  return true;
}
