// Twist: three parallel beams converge at a focal distance dialled with sneak-tap
// (8/16/32 blocks); damage scales x3 at focus and falls to x0.3 out of focus.

import { raycast, dist } from "../../engine/ray.js";
import { applyEffects, hurt } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";
import * as sound from "../../engine/sound.js";
import * as heat from "../../engine/heat.js";
import { muzzleLoc } from "../hitscan.js";

const FOCALS = [8, 16, 32];

export function onPress(ctx) {
  const st = ctx.st;
  if (!ctx.player.isSneaking) return false;              // normal fire
  st.mode = ((st.mode ?? 0) + 1) % FOCALS.length;        // dial the focal distance
  try { ctx.player.playSound("note.pling", { volume: 0.4, pitch: 1.2 + 0.2 * st.mode }); }
  catch { /* ignore */ }
  return true;
}

export function onHold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.reload > 0 || st.cooldown > 0) return true;
  if (d.heat && heat.isHot(st, d)) return true;

  st.beam = (st.beam ?? 0) + 1;
  heat.add(st, d, p.heat_rate ?? 1);

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 40);
  const c = { ...ctx, point: r.point };
  const tickRate = p.tick_rate ?? 4;

  if (ctx.tick % tickRate === 0 && r.entity) {
    const focal = FOCALS[st.mode ?? 1];
    const off = Math.abs(dist(ctx.eye, r.point) - focal);
    const mult = Math.max(p.out_mult ?? 0.3, Math.min(p.focus_mult ?? 3, 3 - 2.7 * (off / focal)));
    applyEffects(c, d.hooks?.on_hit, r.entity);
    hurt(r.entity, (p.dps ?? 10) * tickRate / 20 * mult, c, "magic");
  }

  vfx.line(ctx.dim, muzzleLoc(ctx), r.point, d.vfx.body, d.palette,
           { step: 0.5, max: 40, size: p.width ?? 0.2, life: 0.2 });
  if (!st.beamStarted) {
    st.beamStarted = true;
    sound.play(ctx.player, d.sound);
    vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette,
               { size: p.width ?? 0.3, effect: d.vfx.muzzle });
  }
  return true;
}
