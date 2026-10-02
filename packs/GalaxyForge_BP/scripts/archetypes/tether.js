// tether: a ray that attaches to a mob (pull it to you) or to a block (grapple yourself).

import { raycast, add, norm, dist, entitiesNear } from "../engine/ray.js";
import { applyEffects, hurt, knock, status } from "../engine/damage.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import { muzzleLoc } from "./hitscan.js";

export function press(ctx) { attach(ctx, false); }

/** Alt-fire (sneak + use): grapple to the block you are looking at. */
export function alt(ctx) { attach(ctx, true); }

export function attach(ctx, grapple) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 6)) return;
  if (grapple && st.cooldown > 0) return;
  st.lastFire = ctx.tick;

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 10, { ignoreId: ctx.player.id });
  const c = { ...ctx, point: r.point };
  vfx.line(ctx.dim, muzzleLoc(ctx), r.point, d.vfx.body, d.palette,
           { step: 0.4, max: 32, size: 0.22, life: 0.25 });

  if (grapple) {
    st.cooldown = (p.grapple_cooldown ?? 3) * 20;
    st.grappleTo = r.point || add(ctx.eye, ctx.view, p.range ?? 10);
    sound.play(ctx.player, d.sound);
    return;
  }

  if (r.entity) {
    st.tether = { id: r.entity.id, until: ctx.tick + 20 };
    applyEffects(c, d.hooks?.on_hit, r.entity);
    hurt(r.entity, p.damage ?? 8, c, "lightning");
    if (p.stun) status(r.entity, "slowness", (p.stun * 20) | 0, 4);
    vfx.spawn(ctx.dim, "gx:ring_wave", r.entity.location, { color: d.palette.glow, size: 1.2, life: 0.4 });
    sound.play(ctx.player, d.sound);
  } else {
    vfx.spawn(ctx.dim, "gx:static_arc", r.point, { color: d.palette.core, size: 0.8, life: 0.25 });
  }
}

export function hold(ctx) {
  const st = ctx.st, d = ctx.def, p = d.params;
  if (st.grappleTo) {
    const to = norm({ x: st.grappleTo.x - ctx.player.location.x,
                      y: st.grappleTo.y - ctx.player.location.y,
                      z: st.grappleTo.z - ctx.player.location.z });
    try { ctx.player.applyImpulse({ x: to.x * 0.55, y: Math.max(0.25, to.y * 0.4), z: to.z * 0.55 }); }
    catch { /* ignore */ }
    vfx.line(ctx.dim, muzzleLoc(ctx), st.grappleTo, d.vfx.body, d.palette, { step: 0.5, max: 30, size: 0.2 });
    if (dist(ctx.player.location, st.grappleTo) < 1.5) st.grappleTo = null;
    return;
  }
  if (!st.tether) return;
  const near = entitiesNear(ctx.dim, ctx.player.location, p.range + 2, {});
  const t = near.find((e) => e && e.id === st.tether.id);
  if (!t) { st.tether = null; return; }
  knock(t, ctx, p.pull ?? 1.0, "toward");
  vfx.line(ctx.dim, muzzleLoc(ctx), t.location, d.vfx.body, d.palette, { step: 0.5, max: 30, size: 0.2 });
  if (d.custom?.onTether) { try { d.custom.onTether(ctx, t); } catch { /* ignore */ } }
}

export function release(ctx) { ctx.st.tether = null; ctx.st.grappleTo = null; }
export function idle(ctx) { ctx.st.tether = null; ctx.st.grappleTo = null; }
