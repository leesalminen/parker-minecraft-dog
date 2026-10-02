// The declarative effect vocabulary used by every weapon's on_hit / on_tick hooks.
//
//   {"dmg": 6, "cause": "projectile"}
//   {"status": "slowness", "ticks": 40, "amp": 2}
//   {"vfx": "gx:spark_burst", "size": 0.4, "life": 0.5, "count": 6, "at": "hit"|"self"}
//   {"field": "sun_scar", "radius": 5, "life": 120, "dps": 4, "pull": 0}
//   {"knockback": 1.2, "dir": "away"|"up"|"toward"}
//   {"heal": 4}
//   {"chain": {"jumps": 3, "radius": 6, "falloff": 0.8}}
//   {"grief": {"radius": 3, "from": ["minecraft:sand"], "to": "minecraft:glass", "cap": 20}}
//   {"stun": 60}                       // machine-only stun (gx droids / mechs / tanks)
//   {"bonus_vs": {"family": "gx_droid", "mult": 1.4}}
//
// A weapon's signature twist is a hook plus, at most, ~60 lines in archetypes/custom/.

import { world } from "@minecraft/server";
import { fields, spend, tick } from "./state.js";
import { isProtected, isSelf, mobGriefing, familiesOf } from "./safety.js";
import * as vfx from "./vfx.js";
import { dist, entitiesNear, add } from "./ray.js";

// Bedrock ignores (or only diffs) hits that land inside a mob's 10-tick hurt cooldown, which
// silently swallowed most rapid-fire damage.  The first hit in a window goes through
// applyDamage (hurt flash, knockback, kill credit); follow-ups inside the window come off the
// health component directly, and a lethal follow-up is re-issued through applyDamage large
// enough to clear the cooldown's "must exceed the last hit" rule.
const IFRAMES = 10;
const recent = new Map();   // entity id -> { tick, amount }

function prune() {
  if (tick % 200 !== 0) return;
  for (const [id, r] of recent) if (tick - r.tick > 40) recent.delete(id);
}

// Like a bow, damage is attributed to the shooter.  Script bolts carry a stub player
// ({ id, location, dimension }), so resolve the live Player to use as damagingEntity.  Without a
// damaging entity the hit has no attacker: mobs don't aggro, no kill credit / player-kill drops,
// and some mobs ignore it entirely.
function shooterOf(ctx) {
  const p = ctx.player;
  if (!p) return null;
  if (typeof p.getComponent === "function") return p;
  try { return world.getAllPlayers().find((x) => x.id === p.id) ?? null; } catch { return null; }
}

function hp(entity) {
  try { const h = entity.getComponent("minecraft:health"); return h ? h.currentValue : null; }
  catch { return null; }   // entity already dead / unloaded
}

const warned = new Set();
function warnOnce(msg) {
  if (warned.has(msg)) return;
  warned.add(msg);
  console.warn(`[GalaxyForge] ${msg}`);
}

// applyDamage can return true (or throw / return false) without health actually dropping, e.g. a
// mob rejecting the source.  Escalate: attributed hit -> unattributed hit -> health component, and
// stop as soon as health goes down (or the entity is gone, which reads as null).
function strike(entity, amount, opts) {
  const before = hp(entity);
  const landed = () => { const now = hp(entity); return before === null || now === null || now < before; };
  try { entity.applyDamage(amount, opts); } catch (e) { warnOnce(`applyDamage(attributed) threw: ${e?.message ?? e}`); }
  if (landed()) return true;
  if (opts.damagingEntity) {
    try { entity.applyDamage(amount, { cause: opts.cause }); } catch (e) { warnOnce(`applyDamage threw: ${e?.message ?? e}`); }
    if (landed()) return true;
  }
  try {
    const h = entity.getComponent("minecraft:health");
    if (h) { h.setCurrentValue(Math.max(0, before - amount)); return true; }
  } catch (e) { warnOnce(`health fallback threw: ${e?.message ?? e}`); }
  warnOnce(`damage did not land on ${entity.typeId}`);
  return false;
}

export function hurt(entity, amount, ctx, cause) {
  if (!entity || amount <= 0) return false;
  if (isSelf(entity, ctx.player)) return false;
  if (isProtected(entity, ctx.player, { pvp: ctx.pvp })) return false;
  const opts = { cause: cause || "entityAttack" };
  const shooter = shooterOf(ctx);
  if (shooter) opts.damagingEntity = shooter;
  const last = recent.get(entity.id);
  if (last && tick - last.tick < IFRAMES) {
    const h = hp(entity);
    if (h !== null) {
      const left = h - amount;
      if (left > 0) { try { entity.getComponent("minecraft:health").setCurrentValue(left); return true; } catch { /* fall through */ } }
      amount = last.amount + h + 1;
    }
    last.amount = Math.max(last.amount, amount);
    return strike(entity, amount, opts);
  }
  recent.set(entity.id, { tick, amount });
  prune();
  return strike(entity, amount, opts);
}

export function status(entity, id, ticks, amp) {
  if (!entity) return false;
  try { entity.addEffect(id, ticks, { amplifier: amp || 0, showParticles: true }); return true; }
  catch { return false; }
}

export function knock(entity, ctx, power, dir) {
  if (!entity || !power) return;
  const t = entity.location, p = ctx.player.location;
  let dx = t.x - p.x, dz = t.z - p.z, dy = 0;
  if (dir === "toward") { dx = -dx; dz = -dz; }
  if (dir === "up") { dy = 1; }
  const l = Math.sqrt(dx * dx + dz * dz) || 1;
  dx /= l; dz /= l;
  try { entity.applyKnockback(dx, dz, power, dy ? power * 0.8 : 0); return; } catch { /* older sig */ }
  try { entity.applyKnockback({ x: dx * power, z: dz * power }, dy ? power * 0.8 : 0); return; } catch { /* ignore */ }
  try { entity.applyImpulse({ x: dx * power * 0.4, y: dy * power * 0.4, z: dz * power * 0.4 }); } catch { /* ignore */ }
}

export function heal(entity, amount) {
  try {
    const h = entity.getComponent("minecraft:health");
    if (h) h.setCurrentValue(Math.min(h.effectiveMax ?? h.defaultValue ?? 20, h.currentValue + amount));
  } catch { /* ignore */ }
}

export function grief(ctx, spec) {
  if (!mobGriefing()) return 0;
  const cap = spec.cap ?? 20;
  let changed = 0;
  const r = spec.radius ?? 2;
  const base = ctx.point || ctx.player.location;
  for (let dx = -r; dx <= r && changed < cap; dx++) {
    for (let dz = -r; dz <= r && changed < cap; dz++) {
      for (let dy = -1; dy <= 1 && changed < cap; dy++) {
        if (!spend("queries")) return changed;
        try {
          const b = ctx.dim.getBlock({ x: Math.floor(base.x) + dx, y: Math.floor(base.y) + dy, z: Math.floor(base.z) + dz });
          if (!b) continue;
          if (spec.from && !spec.from.includes(b.typeId)) continue;
          b.setType(spec.to || "minecraft:air");
          changed++;
        } catch { /* unloaded / protected */ }
      }
    }
  }
  return changed;
}

// Blocks an explosion never removes, on top of anything holding an inventory.
const UNBREAKABLE = new Set([
  "minecraft:air", "minecraft:bedrock", "minecraft:barrier", "minecraft:obsidian",
  "minecraft:crying_obsidian", "minecraft:reinforced_deepslate", "minecraft:end_portal_frame",
  "minecraft:end_portal", "minecraft:portal", "minecraft:end_gateway", "minecraft:command_block",
  "minecraft:chain_command_block", "minecraft:repeating_command_block", "minecraft:structure_block",
  "minecraft:jigsaw", "minecraft:light_block", "minecraft:water", "minecraft:flowing_water",
  "minecraft:lava", "minecraft:flowing_lava", "minecraft:respawn_anchor", "minecraft:spawner",
]);

/** Spherical crater for explosive launchers.  mobGriefing-gated, capped per blast. */
export function crater(ctx, loc, radius, cap = 80) {
  if (!mobGriefing() || !radius) return 0;
  const cx = Math.floor(loc.x), cy = Math.floor(loc.y), cz = Math.floor(loc.z);
  const r = Math.ceil(radius);
  let n = 0;
  for (let dy = r; dy >= -r; dy--) {
    for (let dx = -r; dx <= r; dx++) {
      for (let dz = -r; dz <= r; dz++) {
        if (dx * dx + dy * dy + dz * dz > radius * radius + Math.random() * radius) continue;
        try {
          const b = ctx.dim.getBlock({ x: cx + dx, y: cy + dy, z: cz + dz });
          if (!b || UNBREAKABLE.has(b.typeId)) continue;
          if (b.getComponent?.("minecraft:inventory")) continue;
          b.setType("minecraft:air");
          if (++n >= cap) return n;
        } catch { /* unloaded / protected */ }
      }
    }
  }
  return n;
}

export function spawnField(ctx, kind, spec) {
  fields.push({
    kind, dim: ctx.dim, loc: { ...(ctx.point || ctx.player.location) }, ownerId: ctx.player.id,
    radius: spec.radius ?? 3, life: spec.life ?? 100, dps: spec.dps ?? 0,
    pull: spec.pull ?? 0, push: spec.push ?? 0, tag: spec.tag ?? null,
    color: ctx.def?.palette?.glow ?? [1, 1, 1], extra: spec.extra ?? {},
  });
}

export function chain(ctx, target, spec) {
  const jumps = spec.jumps ?? 3;
  const radius = spec.radius ?? 6;
  const falloff = spec.falloff ?? 0.8;
  let src = target;
  let dmg = spec.dmg ?? 5;
  const hit = new Set([target?.id]);
  for (let i = 0; i < jumps; i++) {
    const near = entitiesNear(ctx.dim, src.location, radius, { excludeTypes: ["minecraft:player"] });
    const next = near.find((e) => e && !hit.has(e.id) && !isProtected(e, ctx.player, { pvp: ctx.pvp }));
    if (!next) break;
    hurt(next, dmg, ctx, "lightning");
    vfx.spawn(ctx.dim, "gx:lightning_fork", next.location, { color: ctx.def.palette.glow, size: 1.0, life: 0.25 });
    hit.add(next.id);
    src = next;
    dmg *= falloff;
  }
}

/** Apply a hook effect list to a target. */
export function applyEffects(ctx, effects, target) {
  if (!effects) return;
  for (const e of effects) {
    if (e.dmg) {
      let dmg = e.dmg;
      if (e.bonus_vs && target) {
        const fams = familiesOf(target);
        if (fams.includes(e.bonus_vs.family)) dmg *= e.bonus_vs.mult;
      }
      hurt(target, dmg, ctx, e.cause);
    }
    if (e.status) status(target, e.status, e.ticks ?? 40, e.amp ?? 0);
    if (e.stun && target) {
      const fams = familiesOf(target);
      if (fams.some((f) => f.startsWith("gx_"))) {
        status(target, "slowness", e.stun, 6);
        status(target, "weakness", e.stun, 2);
        try { target.setDynamicProperty("gx:stunned", e.stun); } catch { /* ignore */ }
      }
    }
    if (e.vfx) {
      const loc = e.at === "self" ? ctx.player.location : (ctx.point || target?.location || ctx.player.location);
      vfx.spawn(ctx.dim, e.vfx, loc, { color: ctx.def.palette.glow, size: e.size ?? 0.4,
                                       life: e.life ?? 0.4, count: e.count ?? 1, speed: e.speed ?? 0.5 });
    }
    if (e.field) spawnField(ctx, e.field, e);
    if (e.knockback) knock(target, ctx, e.knockback, e.dir);
    if (e.heal && target) heal(target, e.heal);
    if (e.chain && target) chain(ctx, target, e.chain);
    if (e.grief) grief(ctx, e.grief);
  }
}
