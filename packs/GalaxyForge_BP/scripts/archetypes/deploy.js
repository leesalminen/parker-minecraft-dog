// deploy: spawns a gx entity (combat drone / sentinel turret), capped per player.
// Drones orbit their owner; turrets stay put.  Both fire small lasers at hostile mobs,
// and never at pups, tamed mobs or players (safety.js enforces the targeting filter).

import { deployables } from "../engine/state.js";
import { raycast, add, norm, dist, entitiesNear } from "../engine/ray.js";
import { hurt } from "../engine/damage.js";
import { isProtected } from "../engine/safety.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import { muzzleLoc } from "./hitscan.js";
import { world, ItemStack } from "@minecraft/server";

export function press(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 20)) return;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  const mine = deployables.filter((x) => x.ownerId === ctx.player.id && x.kind === p.entity).length;
  if (mine >= (p.cap ?? 2)) return;

  st.lastFire = ctx.tick;
  if (d.ammo.type === "cell") st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);
  const cd = p.cooldown ?? d.cooldown;
  if (cd) st.cooldown = cd * 20;

  let loc;
  if (p.hover) loc = add(ctx.player.location, { x: 0, y: 2.2, z: 0 }, 1);
  else {
    const r = raycast(ctx.dim, ctx.eye, ctx.view, p.place_range ?? 8, { ignoreId: ctx.player.id });
    loc = r.point || add(ctx.eye, ctx.view, 4);
    loc = { x: Math.floor(loc.x) + 0.5, y: Math.floor(loc.y) + 0.1, z: Math.floor(loc.z) + 0.5 };
  }
  let e;
  try { e = ctx.dim.spawnEntity(p.entity, loc); } catch { return; }
  deployables.push({
    entity: e, ownerId: ctx.player.id, kind: p.entity, dim: ctx.dim, def: d,
    life: (p.duration ?? 20) * 20, dps: p.dps ?? 6, range: p.range ?? 12,
    interval: p.interval ?? 10, last: 0, hover: !!p.hover, loc, refund: d.ammo.type === "cell",
  });
  sound.play(ctx.player, d.sound);
  vfx.impact(ctx.dim, loc, d.palette, { radius: 1.0 });
  if (d.custom?.onDeploy) { try { d.custom.onDeploy(ctx, e); } catch { /* ignore */ } }
}

export function hold() {}
export function release() {}
export function idle() {}

export function tickDeployables() {
  for (let i = deployables.length - 1; i >= 0; i--) {
    const u = deployables[i];
    let e = u.entity;
    try { if (!e || e.isValid === false) throw new Error("gone"); } catch { deployables.splice(i, 1); continue; }
    if (u.life-- <= 0) {
      if (u.refund) refund(u);
      try { e.remove(); } catch { /* ignore */ }
      deployables.splice(i, 1);
      continue;
    }
    // drones follow their owner; turrets hold position
    if (u.hover) {
      const owner = playerById(u.ownerId);
      if (owner) {
        const t = Math.floor(u.life / 10);
        const off = { x: Math.cos(t) * 2.2, y: 2.2, z: Math.sin(t) * 2.2 };
        try { e.teleport(add(owner.location, off)); } catch { /* ignore */ }
      }
    }
    if (u.last-- > 0) continue;
    u.last = u.interval;
    fireAtNearest(u, e);
  }
}

function fireAtNearest(u, e) {
  const near = entitiesNear(u.dim, e.location, u.range, {});
  const hostile = (t) => {
    if (!t || isProtected(t, null, {})) return false;
    const fams = t.getComponent("minecraft:type_family")?.getFamily?.() ?? [];
    // hostile mobs only: never farm animals, never the pup, never a player
    return fams.includes("monster");
  };
  // Focus order: if the owner is aiming at a hostile inside range, the drone takes it.
  let target = null;
  const owner = u.hover ? playerById(u.ownerId) : null;
  if (owner) {
    let best = -1;
    let view = null;
    try { view = owner.getViewDirection(); } catch { /* ignore */ }
    if (view) {
      for (const t of near) {
        if (!hostile(t)) continue;
        if (dist(owner.location, t.location) > u.range) continue;
        const to = norm({ x: t.location.x - owner.location.x,
                          y: (t.location.y + 0.9) - owner.location.y,
                          z: t.location.z - owner.location.z });
        const dot = to.x * view.x + to.y * view.y + to.z * view.z;
        if (dot > best) { best = dot; target = t; }
      }
    }
  }
  if (!target) target = near.find(hostile);
  if (!target) {
    vfx.spawn(u.dim, "gx:field_glow", e.location, { color: u.def.palette.glow, size: 1.2, life: 0.4, alpha: 0.25 });
    return;
  }
  const c = { player: { id: u.ownerId, location: e.location, dimension: u.dim }, dim: u.dim,
              def: u.def, st: {}, point: target.location, pvp: false };
  hurt(target, u.dps * u.interval / 20, c, "projectile");
  vfx.line(u.dim, add(e.location, { x: 0, y: 1.2, z: 0 }, 1), target.location, "gx:beam_bar",
           u.def.palette, { step: 0.8, max: 16, size: 0.14, life: 0.15 });
  if (u.def.custom?.onDeployHit) { try { u.def.custom.onDeployHit(c, target, e); } catch { /* ignore */ } }
}

function playerById(id) {
  try { return world.getAllPlayers().find((p) => p.id === id) ?? null; } catch { return null; }
}

function refund(u) {
  const p = playerById(u.ownerId);
  if (!p) return;
  try { p.getComponent("minecraft:inventory").container.addItem(new ItemStack("gx:energy_cell", 1)); }
  catch { /* inventory full */ }
}
