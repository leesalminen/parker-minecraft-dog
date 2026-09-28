// Twist: the phoenix bolt flies out 35 blocks, then its velocity reverses and it curves
// back to the shooter.  Catching it within 2 blocks heals 2 hearts and refunds the shot;
// missing it burns out in a firework.

import { world } from "@minecraft/server";
import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { getState } from "../../engine/state.js";
import { add, sub, norm, len, dist, eyeOf } from "../../engine/ray.js";

const HEAL = 4;              // 2 hearts
const CATCH = 2;             // blocks

function mul(v, s) { return { x: v.x * s, y: v.y * s, z: v.z * s }; }

/** The bolt's ctx.player is a stub, so resolve the real wielder by id (cached per bolt). */
function owner(b) {
  try {
    if (b.owner?.isValid?.()) return b.owner;
    b.owner = world.getAllPlayers().find((p) => p.id === b.ownerId) ?? null;
  } catch { b.owner = null; }
  return b.owner;
}

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 10)) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  const mag = d.ammo.mag;
  if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
  st.lastFire = ctx.tick;
  st.ammo = Math.max(0, (st.ammo ?? mag) - 1);
  bolt.fire(ctx, { force: true, count: 1, homing: p.homing, homing_turn: p.homing_turn });
  return true;
}

export function onTick(c, b) {
  const p = b.def.params;
  if (!b.returning) {
    if (dist(b.loc, b.origin) < (p.turn_at ?? 35)) return;
    b.returning = true;
    b.homing = 0;                                   // stop chasing mobs on the way home
    b.vel = mul(b.vel, -1);                         // reverse: the return leg begins
    vfx.spawn(b.dim, "gx:star_flash", b.loc, { color: b.pal.core, size: 0.9, life: 0.2 });
    return;
  }
  const o = owner(b);
  const goal = o ? eyeOf(o) : b.origin;
  const s = len(b.vel) || 1;
  b.vel = mul(norm(add(norm(b.vel), norm(sub(goal, b.loc)), 0.3)), s);   // swooping return
  if (o && dist(b.loc, eyeOf(o)) < CATCH) { catchIt(c, b, o); return; }
  if (b.life <= 1) {                                // missed: burn out in a firework
    vfx.impact(b.dim, b.loc, b.pal, { radius: 1.4, sparks: 10 });
    vfx.spawn(b.dim, "gx:star_flash", b.loc, { color: b.pal.core, size: 1.6, life: 0.4 });
  }
}

export function onHit(c, target, b) {
  if (!b?.returning) return;
  const o = owner(b);
  if (o && dist(b.loc, eyeOf(o)) < CATCH) catchIt(c, b, o);
}

function catchIt(c, b, o) {
  b.life = 0;
  try {
    const h = o.getComponent("minecraft:health");
    if (h) h.setCurrentValue(Math.min(h.effectiveMax ?? 20, h.currentValue + HEAL));
  } catch { /* ignore */ }
  const st = getState(o);
  st.ammo = Math.min(b.def.ammo.mag, (st.ammo ?? 0) + 1);
  vfx.impact(b.dim, b.loc, b.pal, { radius: 0.9, sparks: 6 });
  vfx.spawn(b.dim, "gx:ring_wave", b.loc, { color: b.pal.glow, size: 1.4, life: 0.4 });
}
