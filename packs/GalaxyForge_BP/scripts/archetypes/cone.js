// cone: short-range spray / shockwave wavefront.  Damages everything inside the cone,
// applies status, and optionally knocks back.  `params.charge` makes it a charge-release
// wave (sonic cannon).

import { add, norm, entitiesNear, dist } from "../engine/ray.js";
import { applyEffects, hurt, knock } from "../engine/damage.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import { muzzleLoc } from "./hitscan.js";

export function press(ctx) {
  const p = ctx.def.params;
  if (p.charge) { ctx.st.charge = 0; ctx.st.charging = true; return; }
  // Cones are channeled by default (hold sprays).  A pump-action burst weapon sets
  // params.burst so a single press delivers one full spray.
  if (p.burst) spray(ctx, 1);
}

export function hold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (p.charge) {
    if (st.reload > 0 || st.cooldown > 0) return;
    st.charge = (st.charge ?? 0) + 1;
    heat.add(st, d, p.heat_rate ?? 0.5);
    if (ctx.tick % 2 === 0) vfx.spawn(ctx.dim, d.vfx.charge, muzzleLoc(ctx),
      { color: d.palette.core, size: 0.3, life: 0.2, count: 2, speed: 1.0 });
    return;
  }
  if (p.burst) return;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  if (d.heat && heat.isHot(st, d)) return;
  heat.add(st, d, p.heat_rate ?? 0.6);
  spray(ctx, 1 / 20);
}

export function release(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (!p.charge) return;
  st.charging = false;
  const t = Math.min(1, (st.charge ?? 0) / (p.hold_ticks ?? 20));
  st.charge = 0;
  if (st.reload > 0 || st.cooldown > 0) return;
  spray(ctx, 1, { wave: true, power: 1 + t * (p.charge_mult ?? 1.0) });
  sound.play(ctx.player, d.sound);
}

export function idle(ctx) { ctx.st.charge = 0; ctx.st.charging = false; }

/** One spray tick. `scale` = seconds of damage (1 for a full burst, 1/20 per tick). */
export function spray(ctx, scale, o = {}) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (d.ammo.type === "cell" && !o.wave && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  const range = p.range ?? 8;
  const halfAngle = ((p.angle ?? 60) / 2) * Math.PI / 180;
  const power = o.power ?? 1;

  const c = { ...ctx, point: add(ctx.eye, ctx.view, range * 0.6) };
  const near = entitiesNear(ctx.dim, add(ctx.eye, ctx.view, range * 0.5), range + 1,
                            { excludeTypes: ["minecraft:player"] });
  const cosLimit = Math.cos(halfAngle);
  for (const e of near) {
    const to = norm({ x: e.location.x - ctx.eye.x, y: (e.location.y + 0.9) - ctx.eye.y, z: e.location.z - ctx.eye.z });
    const dot = to.x * ctx.view.x + to.y * ctx.view.y + to.z * ctx.view.z;
    if (dot < cosLimit) continue;
    const dmg = (p.dps ?? 10) * scale * power;
    applyEffects({ ...c, point: e.location }, d.hooks?.on_hit, e);
    hurt(e, dmg, c, p.cause || "magic");
    if (p.knockback) knock(e, ctx, p.knockback * power, "away");
    if (d.custom?.onHit) { try { d.custom.onHit(c, e); } catch { /* ignore */ } }
  }

  // Spray visuals: a widening fan of billboard particles from the muzzle.
  const n = o.wave ? 12 : 4;
  const right = norm({ x: ctx.view.z, y: 0, z: -ctx.view.x });
  for (let i = 0; i < n; i++) {
    const a = (Math.random() - 0.5) * 2 * halfAngle;
    const dir = norm(add(ctx.view, right, Math.tan(a)));
    const at = add(muzzleLoc(ctx), dir, 1 + Math.random() * range * 0.7);
    vfx.spawn(ctx.dim, d.vfx.body, at, { color: d.palette.core, size: p.particle_size ?? 0.5,
                                         life: o.wave ? 0.5 : 0.3, count: 1, speed: 0.6 });
  }
  vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette, { size: p.muzzle_size ?? 0.6, count: o.wave ? 5 : 2,
                                                  effect: d.vfx.muzzle });
  if (o.wave) {
    vfx.spawn(ctx.dim, "gx:ring_wave", add(ctx.eye, ctx.view, 1.2), { color: d.palette.glow, size: range, life: 0.5 });
    if (p.grief) applyEffects(c, [{ grief: p.grief }], null);
    const cd = p.cooldown ?? d.cooldown;
    if (cd) st.cooldown = cd * 20;
  }
  if (p.rate && !o.wave) {
    if (ctx.tick - st.lastFire < p.rate) return;
    st.lastFire = ctx.tick;
    if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
    sound.play(ctx.player, d.sound);
  }
}
