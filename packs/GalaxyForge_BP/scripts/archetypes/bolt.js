// bolt: script-simulated projectile, ray-marched per tick, no entity (cheapest on console).
// Supports gravity, homing, split, bounce and an on_hit effect list.

import { projectiles, MAX_PROJECTILES } from "../engine/state.js";
import { raycast, add, norm, dist, entitiesNear, spreadDir } from "../engine/ray.js";
import { applyEffects, hurt, knock, crater } from "../engine/damage.js";
import * as firearm from "../engine/firearm.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import { muzzleLoc } from "./hitscan.js";

function mul(v, s) { return { x: v.x * s, y: v.y * s, z: v.z * s }; }

export function press(ctx) { fire(ctx); }
export function hold(ctx) { if (ctx.def.params.auto) fire(ctx); }
export function release() {}
export function idle() {}

export function fire(ctx, override = {}) {
  const d = ctx.def, p = { ...d.params, ...override }, st = ctx.st;
  const rate = p.rate ?? 4;
  if (!override.force && ctx.tick - st.lastFire < rate) return false;
  if (st.reload > 0 || st.cooldown > 0) return false;
  if (d.ammo.type === "cell" && !override.force && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return false; }
  if (d.heat && heat.isHot(st, d)) return false;

  if (!override.force) {
    st.lastFire = ctx.tick;
    if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
    heat.add(st, d, d.heat?.per_shot ?? 0);
    const cd = p.cooldown ?? d.cooldown;
    if (cd) st.cooldown = cd * 20;
  }

  const count = p.count ?? 1;
  for (let i = 0; i < count; i++) {
    const dir = spreadDir(ctx.view, count > 1 ? (p.spread ?? 4) : 0);
    projectiles.push({
      def: d, ownerId: ctx.player.id, dim: ctx.dim, pal: d.palette,
      loc: add(ctx.eye, dir, 1.2), origin: add(ctx.eye, dir, 1.2), vel: mul(dir, p.speed ?? 40),
      life: p.lifetime ?? 80, bounces: 0, pierce: p.pierce ?? 0, splits: 0,
      gravity: p.gravity ?? 0, homing: p.homing ?? 0, fuse: p.fuse ?? 0,
      damage: p.damage ?? 6, aoe: p.aoe ?? 0, aoe_mult: p.aoe_mult ?? 1,
      size: p.size ?? 0.4, stuck: false, stuckTicks: 0, effect: d.vfx.body,
      onHit: d.hooks?.on_hit, tickHook: d.hooks?.on_tick, custom: d.custom ?? null,
      trail: d.vfx.trail ?? null,
    });
  }
  const m = muzzleLoc(ctx);
  vfx.muzzle(ctx.dim, m, d.palette, { size: p.muzzle_size ?? 0.4, effect: d.vfx.muzzle });
  sound.play(ctx.player, d.sound);
  if (!override.force) firearm.after(ctx, m);
  return true;
}

/** Advance every live bolt one tick. Called once per tick from main.js. */
export function tickBolts(ctxTick) {
  if (projectiles.length > MAX_PROJECTILES) projectiles.splice(0, projectiles.length - MAX_PROJECTILES);
  for (let i = projectiles.length - 1; i >= 0; i--) {
    const b = projectiles[i];
    const p = b.def.params;
    if (b.forceDetonate) { detonate(b, b.loc); projectiles.splice(i, 1); continue; }
    if (b.life-- <= 0) { projectiles.splice(i, 1); continue; }
    if (b.stuck) {
      // Stuck bolts sit still: no ray-march, so a wall full of darts cannot starve the
      // per-tick raycast budget that live bolts need to register hits.
      b.stuckTicks++;
      if (p.fuse && b.stuckTicks >= p.fuse) { detonate(b, b.loc); projectiles.splice(i, 1); continue; }
      if (b.stuckTicks % 4 === 0) vfx.spawn(b.dim, b.effect, b.loc, { color: b.pal.core, size: b.size, life: 0.25 });
      continue;
    }
    if (b.gravity) b.vel = { x: b.vel.x, y: b.vel.y - b.gravity, z: b.vel.z };

    if (b.homing) {
      const near = entitiesNear(b.dim, b.loc, b.homing, { excludeTypes: ["minecraft:player"] });
      const t = near.find((e) => e && e.id !== b.ownerId);
      if (t) {
        const to = norm({ x: t.location.x - b.loc.x, y: (t.location.y + 0.9) - b.loc.y, z: t.location.z - b.loc.z });
        const s = Math.sqrt(b.vel.x ** 2 + b.vel.y ** 2 + b.vel.z ** 2) || 1;
        const turn = p.homing_turn ?? 0.25;
        const nv = norm({ x: b.vel.x / s + to.x * turn, y: b.vel.y / s + to.y * turn, z: b.vel.z / s + to.z * turn });
        b.vel = mul(nv, s);
      }
    }

    const step = mul(b.vel, 1 / 20);
    const next = add(b.loc, step);
    const dir = norm(step);
    const r = raycast(b.dim, b.loc, dir, dist(b.loc, next) + 0.6, { ignoreId: b.ownerId });
    const c = { player: { id: b.ownerId, location: b.loc, dimension: b.dim }, dim: b.dim,
                def: b.def, st: {}, point: r.point, pvp: false };

    if (r.entity) { hitBolt(b, r.entity, c, i); continue; }
    if (r.block) {
      if (b.bounces < (p.bounce ?? 0)) {
        b.bounces++;
        const n = { x: 0, y: 1, z: 0 };
        const dot = b.vel.x * n.x + b.vel.y * n.y + b.vel.z * n.z;
        b.vel = { x: b.vel.x - 2 * dot * n.x, y: b.vel.y - 2 * dot * n.y, z: b.vel.z - 2 * dot * n.z };
        b.loc = add(r.point, norm(b.vel), 0.3);
        vfx.spawn(b.dim, "gx:star_flash", r.point, { color: b.pal.core, size: 0.4, life: 0.15 });
        continue;
      }
      if (p.stick) { b.stuck = true; b.loc = r.point; }
      else if (b.aoe) { detonate(b, r.point); projectiles.splice(i, 1); continue; }
      else { projectiles.splice(i, 1); continue; }
    } else {
      b.loc = next;
    }

    vfx.spawn(b.dim, b.effect, b.loc, { color: b.pal.core, size: b.size, life: 0.25 });
    if (b.trail) vfx.trailPoint(b.dim, b.loc, b.trail, b.pal, { size: 0.3, life: 0.5 });
    if (b.custom?.onTick) { try { b.custom.onTick(c, b); } catch { /* ignore */ } }
  }
}

function hitBolt(b, target, c, index) {
  const p = b.def.params;
  applyEffects(c, b.onHit, target);
  hurt(target, b.damage, c, "projectile");
  if (b.custom?.onHit) { try { b.custom.onHit(c, target, b); } catch { /* ignore */ } }
  if (p.split && b.splits < (p.max_splits ?? 1)) {
    const n = p.split;
    for (let k = 0; k < n; k++) {
      const dir = spreadDir(norm(b.vel), 22);
      projectiles.push({ ...b, splits: b.splits + 1, loc: add(c.point, dir, 0.4),
                         vel: mul(dir, (p.split_speed ?? p.speed)), life: p.split_life ?? 40,
                         pierce: b.pierce, homing: p.split_homing ?? 0 });
    }
  }
  vfx.impact(b.dim, c.point, b.pal, { radius: b.size ?? 0.5, sparks: 4 });
  if (b.aoe && !p.split) detonate(b, c.point);
  if (p.pierce && b.pierce > 0) { b.pierce--; return; }
  projectiles.splice(index, 1);
}

/** Split a live bolt into homing shards (used by splitter_rifle's twist). */
export function splitBolt(b, count, opts = {}) {
  const p = b.def.params;
  const base = norm(b.vel);
  for (let k = 0; k < count; k++) {
    const dir = spreadDir(base, opts.spread ?? 22);
    projectiles.push({
      ...b, splits: b.splits + 1, forceDetonate: false,
      loc: add(b.loc, dir, 0.4), origin: { ...b.loc },
      vel: mul(dir, opts.speed ?? (p.split_speed ?? p.speed)),
      life: opts.life ?? (p.split_life ?? 40),
      pierce: opts.pierce ?? b.pierce,
      homing: opts.homing ?? (p.split_homing ?? 0),
    });
  }
  vfx.spawn(b.dim, "gx:debris_burst", b.loc, { color: b.pal.core, size: 0.6, life: 0.4,
                                               count: 6, speed: 1.2 });
  return count;
}

export function detonate(b, loc) {
  const p = b.def.params;
  const aoe = b.aoe ?? 3;
  const c = { player: { id: b.ownerId, location: loc, dimension: b.dim }, dim: b.dim,
              def: b.def, st: {}, point: loc, pvp: false };
  if (b.custom?.onDetonate) { try { b.custom.onDetonate(c, b, loc); } catch { /* ignore */ } }
  vfx.impact(b.dim, loc, b.pal, { radius: aoe, sparks: 8 });
  vfx.spawn(b.dim, "gx:ring_wave", loc, { color: b.pal.glow, size: aoe * 2, life: 0.5 });
  const near = entitiesNear(b.dim, loc, aoe, { excludeTypes: ["minecraft:player"] });
  if (p.blast) {
    // Real explosion presentation: vanilla blast particles, a world-audible boom, and a crater
    // (crater() is mobGriefing-gated and skips unbreakable blocks and containers).
    try { b.dim.spawnParticle("minecraft:huge_explosion_emitter", loc); } catch { /* ignore */ }
    try { b.dim.playSound("gx.gun.explosion", loc, { volume: 4, pitch: 0.9 + Math.random() * 0.2 }); } catch { /* ignore */ }
    crater(c, loc, p.blast);
  }
  for (const e of near) {
    const dmg = b.damage * (b.aoe_mult ?? 1);
    hurt(e, dmg, c, "explosion");
    if (p.blast) knock(e, c, 0.8 + aoe * 0.1, "up");
    applyEffects(c, b.onHit, e);
    if (b.custom?.onHit) { try { b.custom.onHit(c, e, b); } catch { /* ignore */ } }
  }
  if (p.grief) applyEffects(c, [{ grief: p.grief }], null);
}
