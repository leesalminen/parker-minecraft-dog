// beam: channeled continuous ray with tick damage, heat and optional glass refraction.

import { raycast, add, norm, entitiesNear } from "../engine/ray.js";
import { applyEffects, hurt } from "../engine/damage.js";
import * as vfx from "../engine/vfx.js";
import * as sound from "../engine/sound.js";
import * as heat from "../engine/heat.js";
import { muzzleLoc } from "./hitscan.js";

const REFRACTIVE = ["minecraft:glass", "minecraft:ice", "minecraft:tinted_glass",
                    "minecraft:blue_ice", "minecraft:frosted_ice", "minecraft:stained_glass"];

export function press(ctx) { ctx.st.beam = 0; ctx.st.beamStarted = false; }

export function hold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.reload > 0 || st.cooldown > 0) return;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) { st.wantReload = true; return; }
  if (d.heat && heat.isHot(st, d)) return;

  st.beam = (st.beam ?? 0) + 1;
  heat.add(st, d, p.heat_rate ?? 1);

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range);
  const c = { ...ctx, point: r.point };
  const tickRate = p.tick_rate ?? 4;

  if (ctx.tick % tickRate === 0) {
    const dmg = (p.dps ?? 10) * tickRate / 20;
    if (r.entity) {
      applyEffects(c, d.hooks?.on_hit, r.entity);
      hurt(r.entity, dmg, c, "magic");
      if (d.custom?.onHit) { try { d.custom.onHit(c, r.entity); } catch { /* ignore */ } }
    }
    if (p.refract && r.block && REFRACTIVE.includes(r.block.typeId)) refract(ctx, r, dmg);
  }

  vfx.line(ctx.dim, muzzleLoc(ctx), r.point, d.vfx.body, d.palette,
           { step: 0.5, max: 40, size: p.width ?? 0.25, life: 0.2 });

  if (!st.beamStarted) {
    st.beamStarted = true;
    sound.play(ctx.player, d.sound);
    vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette, { size: p.width ?? 0.3, effect: d.vfx.muzzle });
  }
  if (d.custom?.onHold) { try { d.custom.onHold(c); } catch { /* ignore */ } }
}

export function release(ctx) { ctx.st.beam = 0; ctx.st.beamStarted = false; }
export function idle(ctx) { ctx.st.beam = 0; ctx.st.beamStarted = false; }

/** Prism twist: three spectrum beams fan out from the glass entry point. */
function refract(ctx, r, dmg) {
  const d = ctx.def;
  const base = r.point;
  const dir = ctx.view;
  const right = norm({ x: dir.z, y: 0, z: -dir.x });
  for (let i = -1; i <= 1; i++) {
    const fan = norm(add(dir, right, i * 0.28));
    const rr = raycast(ctx.dim, add(base, fan, 0.3), fan, ctx.def.params.range * 0.6);
    vfx.line(ctx.dim, add(base, fan, 0.3), rr.point, "gx:beam_bar", d.palette,
             { step: 0.6, max: 24, size: 0.16 });
    if (rr.entity) {
      const c = { ...ctx, point: rr.point };
      hurt(rr.entity, dmg * 0.7, c, "magic");
      applyEffects(c, d.hooks?.on_hit, rr.entity);
    }
  }
  vfx.spawn(ctx.dim, "gx:star_flash", base, { color: d.palette.core, size: 0.8, life: 0.25 });
}
