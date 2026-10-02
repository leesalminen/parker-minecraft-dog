// charge: hold to charge, tiers on release, optional overcharge penalty.
// `params.mode` decides what the release produces: hitscan beam, bolt, or lob arc.

import { raycast, add, norm, dist, entitiesNear } from "../engine/ray.js";
import { applyEffects, hurt } from "../engine/damage.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import { muzzleLoc } from "./hitscan.js";
import * as bolt from "./bolt.js";

export function press(ctx) { ctx.st.charge = 0; ctx.st.charging = true; }

export function hold(ctx) {
  const d = ctx.def, st = ctx.st;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  if (d.heat && heat.isHot(st, d)) return;
  st.charge = (st.charge ?? 0) + 1;
  heat.add(st, d, (d.params.heat_rate ?? 0.4));

  // Motes converge on the muzzle while charging.
  const t = Math.min(1, st.charge / (d.params.hold_ticks ?? 20));
  if (ctx.tick % 2 === 0) {
    const m = muzzleLoc(ctx);
    vfx.spawn(ctx.dim, d.vfx.charge, m, { color: d.palette.core, size: 0.25 + 0.5 * t,
                                          life: 0.2, count: 3, speed: 1.2 });
  }
  if (st.charge === 1) sound.play(ctx.player, d.sound);
  if (d.custom?.onHold) { try { d.custom.onHold(ctx); } catch { /* ignore */ } }
}

export function release(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  st.charging = false;
  const ticks = st.charge ?? 0;
  st.charge = 0;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (ticks < (p.min_ticks ?? 1)) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }

  const tier = (p.tiers || []).filter((t) => ticks >= t.ticks).pop() || { damage: p.damage ?? 8 };
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  heat.add(st, d, tier.heat ?? (p.heat_per_shot ?? 0));
  if (tier.cooldown) st.cooldown = tier.cooldown * 20;

  if (p.mode === "bolt") {
    bolt.fire(ctx, { force: true, speed: tier.speed ?? p.speed ?? 20,
                     gravity: tier.gravity ?? p.gravity ?? 0, aoe: tier.aoe ?? p.aoe ?? 0,
                     damage: tier.damage, lifetime: tier.lifetime ?? p.lifetime ?? 80,
                     size: tier.size ?? 0.8, count: 1 });
    return;
  }
  if (p.mode === "lob") {
    bolt.fire(ctx, { force: true, speed: tier.speed ?? 14, gravity: tier.gravity ?? 0.25,
                     aoe: tier.aoe ?? 3, damage: tier.damage, fuse: tier.fuse ?? 0,
                     size: tier.size ?? 0.7, count: 1 });
    return;
  }

  // hitscan beam release
  const r = raycast(ctx.dim, ctx.eye, ctx.view, tier.range ?? p.range ?? 40, { ignoreId: ctx.player.id });
  const c = { ...ctx, point: r.point };
  const pierce = tier.pierce ?? p.pierce ?? 1;
  const targets = r.entity ? r.hits.slice(0, pierce).map((h) => h.entity) : [];
  for (const t of targets) {
    applyEffects(c, d.hooks?.on_hit, t);
    hurt(t, tier.damage, c, "magic");
    if (d.custom?.onHit) { try { d.custom.onHit(c, t); } catch { /* ignore */ } }
  }
  vfx.line(ctx.dim, muzzleLoc(ctx), r.point, d.vfx.body, d.palette,
           { step: 0.45, max: 40, size: tier.width ?? p.width ?? 0.4, life: 0.3 });
  vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette, { size: tier.size ?? 1.0, count: 4, effect: d.vfx.muzzle });
  vfx.impact(ctx.dim, r.point, d.palette, { radius: tier.aoe ?? 1.0, sparks: 6 });
  if (p.grief) applyEffects(c, [{ grief: p.grief }], null);
  sound.play(ctx.player, d.sound);
}

export function idle(ctx) { ctx.st.charge = 0; ctx.st.charging = false; }
