// hitscan: instant ray, tracer particle, optional pierce / ricochet / headshot bonus.

import { system, world } from "@minecraft/server";
import { raycast, add, dist, entitiesNear, spreadDir, eyeOf, viewOf } from "../engine/ray.js";
import { applyEffects, hurt } from "../engine/damage.js";
import { familiesOf } from "../engine/safety.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import * as firearm from "../engine/firearm.js";

// Temporary: prints what a shot hit (every 6th round) so "no damage" can be diagnosed in-game.
const DEBUG_SHOTS = true;

export const POLISHED = [
  "minecraft:iron_block", "minecraft:gold_block", "minecraft:quartz_block", "minecraft:glass",
  "minecraft:tinted_glass", "minecraft:polished_andesite", "minecraft:polished_diorite",
  "minecraft:polished_granite", "minecraft:polished_blackstone", "minecraft:polished_deepslate",
  "minecraft:copper_block", "minecraft:netherite_block", "minecraft:diamond_block",
];

const FACE_NORMAL = {
  up: { x: 0, y: 1, z: 0 }, down: { x: 0, y: -1, z: 0 },
  north: { x: 0, y: 0, z: -1 }, south: { x: 0, y: 0, z: 1 },
  east: { x: 1, y: 0, z: 0 }, west: { x: -1, y: 0, z: 0 },
};

export function muzzleLoc(ctx) {
  // Camera-relative: slightly right of and below the crosshair, so the flash sits at the gun
  // and never on the ground / at world-axis offsets from wherever the player faces.
  const v = ctx.view;
  let r = { x: -v.z, y: 0, z: v.x };
  const rl = Math.sqrt(r.x * r.x + r.z * r.z) || 1;
  r = { x: r.x / rl, y: 0, z: r.z / rl };
  const up = { x: r.y * v.z - r.z * v.y, y: r.z * v.x - r.x * v.z, z: r.x * v.y - r.y * v.x };
  return add(add(add(ctx.eye, v, 0.9), r, 0.22), up, -0.18);
}

function reflect(dir, n) {
  const dot = dir.x * n.x + dir.y * n.y + dir.z * n.z;
  return { x: dir.x - 2 * dot * n.x, y: dir.y - 2 * dot * n.y, z: dir.z - 2 * dot * n.z };
}

export function press(ctx) { shot(ctx); }
export function hold(ctx) { if (ctx.def.params.auto) shot(ctx); }
export function release() {}
export function idle() {}

// Optional params (realistic weapons): spread (deg, halved while aiming), pellets (shotgun:
// one ray each, damage summed per target), burst + burst_gap (extra shots on a timer),
// spinup (ticks of held trigger before the first round), tracer_every (0 = none),
// recoil / shell / smoke (engine/firearm.js), impact_size (dust on block hits).
export function shot(ctx, bounce = 0, fromDir = null, fromOrigin = null, sub = false) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (!bounce && !sub) {
    const rate = p.rate ?? 5;
    if (ctx.tick - st.lastFire < rate) return false;
    if (st.reload > 0 || st.cooldown > 0) return false;
    if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return false; }
    if (d.heat && heat.isHot(st, d) && p.heat_stop !== false) return false;
    if (p.spinup && (st.spin ?? 0) < p.spinup) {
      if (!st.spinSound) { st.spinSound = true; sound.play(ctx.player, [["gx.gun.spin", 0.8, 1.0, 0]]); }
      return false;
    }

    st.lastFire = ctx.tick;
    if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
    heat.add(st, d, d.heat?.per_shot ?? 0);
    const cd = p.cooldown ?? d.cooldown;
    if (cd) st.cooldown = cd * 20;
    if (p.burst > 1) scheduleBurst(ctx);
  }

  const origin = fromOrigin || ctx.eye;
  const baseDir = fromDir || ctx.view;
  const pellets = bounce ? 1 : (p.pellets ?? 1);
  const spread = bounce ? 0 : (p.spread ?? 0) * (st.aim ? 0.5 : 1);
  st.shots = (st.shots ?? 0) + 1;
  const every = p.tracer_every ?? 1;
  const tracer = every > 0 && st.shots % every === 0;
  const muzzle = (bounce || fromOrigin) ? add(origin, baseDir, 0.8) : muzzleLoc(ctx);

  const byTarget = new Map();   // entity id -> { t, dmg, point }
  let last = null;
  for (let i = 0; i < pellets; i++) {
    const dir = spread ? spreadDir(baseDir, spread) : baseDir;
    const r = raycast(ctx.dim, origin, dir, p.range, { ignoreId: ctx.player.id });
    const point = r.point || add(origin, dir, p.range);
    if (DEBUG_SHOTS && st.shots % 6 === 1) {
      const hits = r.hits.slice(0, 3).map((h) => `${h.entity.typeId}@${h.dist.toFixed(1)}`).join(", ") || "none";
      let near = "";
      try {
        const es = ctx.dim.getEntities({ location: origin, maxDistance: 40, excludeTypes: ["minecraft:player", "minecraft:item", "minecraft:xp_orb"] });
        let best = null;
        for (const e of es) {
          const v = { x: e.location.x - origin.x, y: e.location.y + 0.9 - origin.y, z: e.location.z - origin.z };
          const l = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z) || 1;
          const ang = Math.acos(Math.max(-1, Math.min(1, (v.x * dir.x + v.y * dir.y + v.z * dir.z) / l))) * 180 / Math.PI;
          if (!best || ang < best.ang) best = { e, ang, l };
        }
        if (best) near = ` nearest-to-crosshair=${best.e.typeId}@${best.l.toFixed(1)}m off=${best.ang.toFixed(1)}deg`;
      } catch { /* ignore */ }
      try {
        world.sendMessage(`§7[shot] ${d.id} range=${p.range} dmg=${p.damage} dir=${dir.x.toFixed(2)},${dir.y.toFixed(2)},${dir.z.toFixed(2)} ` +
          `entities=[${hits}] block=${r.block?.typeId ?? "none"}${r.capped ? " §cRAY-BUDGET-CAPPED" : ""}${near}`);
      } catch { /* ignore */ }
    }
    last = { r, dir, point };

    const hits = r.entity ? (p.pierce ? r.hits.slice(0, p.pierce).map((h) => h.entity) : [r.entity]) : [];
    for (const t of hits) {
      let dmg = p.damage ?? 5;
      if (p.headshot_mult) {
        try {
          const head = t.getHeadLocation();
          if (head && dist(point, head) < 0.7) dmg *= p.headshot_mult;
        } catch { /* ignore */ }
      }
      if (p.falloff && r.dist > p.range * 0.5) dmg *= p.falloff;
      if (p.bonus_vs) {
        const fams = familiesOf(t);
        if (fams.includes(p.bonus_vs.family)) dmg *= p.bonus_vs.mult;
      }
      const e = byTarget.get(t.id);
      if (e) e.dmg += dmg; else byTarget.set(t.id, { t, dmg, point });
    }

    if (tracer && i < 2) {
      vfx.line(ctx.dim, muzzle, point, d.vfx.body, d.palette,
               { step: p.tracer_step ?? 0.7, max: 40, size: p.tracer_size ?? 0.22, life: p.tracer_life ?? 0.16 });
    }
    if (r.block && !hits.length && p.impact_size) {
      vfx.spawn(ctx.dim, d.vfx.impact, point, { color: d.palette.trail, size: p.impact_size, life: 0.45,
                                                count: 4, speed: 1.1 });
    }
  }

  for (const { t, dmg, point } of byTarget.values()) {
    const c = { ...ctx, point };
    applyEffects(c, d.hooks?.on_hit, t);
    hurt(t, dmg, c, "projectile");
    if (ctx.def.custom?.onHit) { try { ctx.def.custom.onHit(c, t); } catch { /* ignore */ } }
  }

  const { r, dir, point } = last;
  const c = { ...ctx, point };
  if (!byTarget.size && r.block && p.ricochet && bounce < p.ricochet && POLISHED.includes(r.block.typeId)) {
    const n = FACE_NORMAL[r.face] || FACE_NORMAL.up;
    const nd = reflect(dir, n);
    const no = add(point, nd, 0.05);
    vfx.spawn(ctx.dim, "gx:star_flash", point, { color: d.palette.core, size: 0.4, life: 0.15 });
    shot(ctx, bounce + 1, nd, no);
    return true;
  }

  if (r.block) {
    const c2 = d.hooks?.on_hit?.find((e) => e.grief);
    if (c2) applyEffects(c, [c2], null);
  }

  if (!bounce) {
    vfx.muzzle(ctx.dim, muzzle, d.palette, { size: p.muzzle_size ?? 0.5, effect: d.vfx.muzzle });
    sound.play(ctx.player, d.sound);
    firearm.after(ctx, muzzle);
  }
  return true;
}

/** Remaining rounds of a burst, each re-aimed along the player's current view. */
function scheduleBurst(ctx) {
  const p = ctx.def.params;
  for (let k = 1; k < p.burst; k++) {
    system.runTimeout(() => {
      try {
        if (ctx.player.isValid === false) return;
        shot({ ...ctx, tick: ctx.tick + k, eye: eyeOf(ctx.player), view: viewOf(ctx.player) }, 0, null, null, true);
      } catch { /* ignore */ }
    }, k * (p.burst_gap ?? 2));
  }
}

/** Second target set for weapons whose twist chains on hit (declared via params.chain). */
export function autoChain(ctx, target) {
  const p = ctx.def.params;
  if (!p.chain) return;
  chain({ ...ctx, point: target.location }, target, p.chain);
}
