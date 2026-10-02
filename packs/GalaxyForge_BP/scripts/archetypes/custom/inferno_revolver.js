// Twist: fan the hammer (sneak-fire empties the cylinder in 0.8 s with wide spread) and a
// speedloader QTE - a press inside the green window loads an explosive round.

import { system } from "@minecraft/server";
import * as vfx from "../../engine/vfx.js";
import * as sound from "../../engine/sound.js";
import { raycast, add, norm, entitiesNear, eyeOf, viewOf } from "../../engine/ray.js";
import { applyEffects, hurt } from "../../engine/damage.js";
import { isProtected } from "../../engine/safety.js";
import { muzzleLoc } from "../hitscan.js";
import { GLYPHS } from "../../generated/weapons.js";

/** Random cone spread around a direction. */
function jitter(dir, degrees) {
  if (!degrees) return dir;
  const a = (Math.random() - 0.5) * 2 * degrees * Math.PI / 180;
  const b = (Math.random() - 0.5) * 2 * degrees * Math.PI / 180;
  const right = { x: dir.z, y: 0, z: -dir.x };
  return norm({ x: dir.x + right.x * Math.tan(a), y: dir.y + Math.tan(b),
                z: dir.z + right.z * Math.tan(a) });
}

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.reload > 0) return speedloader(ctx);
  if (ctx.tick - st.lastFire < (p.rate ?? 20)) return true;
  if (st.cooldown > 0) return true;
  const left = Math.max(0, st.ammo ?? d.ammo.mag);
  if (left <= 0) { st.wantReload = true; st.scratch.loadStart = ctx.tick; return true; }
  if (ctx.player.isSneaking === true) return fan(ctx, left);

  st.lastFire = ctx.tick;
  st.ammo = left - 1;
  const boom = !!st.scratch.explosive;
  st.scratch.explosive = 0;
  shoot(ctx, ctx.view, boom);
  return true;
}

/** Fan the hammer: the whole cylinder inside `fan_ticks`, wide spread, first round explodes. */
function fan(ctx, left) {
  const d = ctx.def, p = d.params, st = ctx.st;
  st.lastFire = ctx.tick;
  st.ammo = 0;
  const boom = !!st.scratch.explosive;
  st.scratch.explosive = 0;
  const gap = Math.max(1, Math.round((p.fan_ticks ?? 16) / left));
  for (let i = 0; i < left; i++) {
    system.runTimeout(() => {
      try {
        const c = { ...ctx, eye: eyeOf(ctx.player), view: viewOf(ctx.player) };
        shoot(c, jitter(c.view, p.fan_spread ?? 14), boom && i === 0);
      } catch { /* ignore */ }
    }, i * gap);
  }
  return true;
}

/** Speedloader QTE: pressing late in the reload arms an explosive round for the cylinder. */
function speedloader(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const spent = ctx.tick - (st.scratch.loadStart ?? ctx.tick);
  if (spent >= (p.qte_from ?? 32)) {
    st.scratch.explosive = 1;
    st.scratch.loadStart = ctx.tick;
    try { ctx.player.onScreenDisplay.updateSubtitle(GLYPHS.marker_kill); } catch { /* ignore */ }
    vfx.spawn(ctx.dim, "gx:ring_wave", add(ctx.eye, ctx.view, 0.8),
              { color: d.palette.glow, size: 0.8, life: 0.3 });
  }
  return true;
}

function shoot(ctx, dir, boom) {
  const d = ctx.def, p = d.params;
  const r = raycast(ctx.dim, ctx.eye, dir, p.range ?? 32, { ignoreId: ctx.player.id });
  const point = r.point || add(ctx.eye, dir, p.range ?? 32);
  const c = { ...ctx, point };
  if (r.entity && !isProtected(r.entity, ctx.player, { pvp: false })) {
    applyEffects(c, d.hooks?.on_hit, r.entity);
    hurt(r.entity, p.damage ?? 15, c, "projectile");
    try { r.entity.setOnFire(p.ignite ?? 5, true); } catch { /* ignore */ }
  }
  if (boom) boomAt(c, point);
  vfx.line(ctx.dim, add(ctx.eye, dir, 0.8), point, d.vfx.body, d.palette,
           { step: 0.7, max: 40, size: p.tracer_size ?? 0.22, life: 0.15 });
  vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette,
             { size: p.muzzle_size ?? 0.6, count: 4, effect: d.vfx.muzzle });
  sound.play(ctx.player, d.sound);
}

function boomAt(c, point) {
  const d = c.def, p = d.params, aoe = p.boom_aoe ?? 3;
  vfx.impact(c.dim, point, d.palette, { radius: aoe, sparks: 8 });
  vfx.spawn(c.dim, "gx:ring_wave", point, { color: d.palette.glow, size: aoe * 2, life: 0.4 });
  for (const e of entitiesNear(c.dim, point, aoe, { excludeTypes: ["minecraft:player"] })) {
    if (isProtected(e, c.player, { pvp: false })) continue;
    hurt(e, p.boom_damage ?? 10, { ...c, point }, "explosion");
  }
}
