// Twist: hold the dot on a spot for 2 s to fill the lock reticle; 1.5 s later a pillar
// of light slams down on the locked spot with a 6-block ground shockwave. 60 s cooldown.

import { system } from "@minecraft/server";
import { raycast, add, entitiesNear } from "../../engine/ray.js";
import { hurt, grief } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

const LOCK_TICKS = 40;    // 2 s on target
const STRIKE_DELAY = 30;  // 1.5 s telegraph

export function onPress(ctx) {
  ctx.st.charge = 0;
  ctx.st.scratch.striking = false;
  return true;
}

export function onHold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.cooldown > 0 || st.scratch.striking) return true;

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 120);
  const point = r.point || add(ctx.eye, ctx.view, p.range ?? 120);
  st.charge = Math.min(LOCK_TICKS, (st.charge ?? 0) + 1);

  if (ctx.tick % 4 === 0) {
    vfx.spawn(ctx.dim, "gx:ring_wave", point,
              { color: d.palette.glow, size: 0.4 + st.charge / 40, life: 0.3 });
  }
  if (st.charge >= LOCK_TICKS) {
    st.scratch.striking = true;
    strike(ctx, point);
  }
  return true;
}

export function onRelease(ctx) {
  ctx.st.charge = 0;
  ctx.st.scratch.striking = false;
  return true;
}

function strike(ctx, point) {
  const d = ctx.def, p = d.params, st = ctx.st;
  st.cooldown = (d.cooldown ?? 60) * 20;
  st.ammo = Math.max(0, (st.ammo ?? d.ammo.mag) - 1);

  // telegraph: a ring on the ground that closes in before the strike lands
  for (let t = 0; t < STRIKE_DELAY; t += 6) {
    system.runTimeout(() => {
      try {
        vfx.spawn(ctx.dim, "gx:ring_wave", point,
                  { color: d.palette.core, size: 1.2 + t / 10, life: 0.5 });
      } catch { /* ignore */ }
    }, t);
  }

  system.runTimeout(() => {
    try {
      vfx.line(ctx.dim, { x: point.x, y: point.y + 24, z: point.z }, point,
               "gx:beam_bar", d.palette, { step: 0.6, max: 40, size: 1.1, life: 0.4 });
      vfx.spawn(ctx.dim, "gx:ring_wave", point, { color: d.palette.core, size: 3.0, life: 0.6 });
      vfx.spawn(ctx.dim, "gx:star_flash", point, { color: d.palette.core, size: 4.0, life: 0.4 });

      const c = { ...ctx, point };
      for (const e of entitiesNear(ctx.dim, point, p.aoe ?? 6,
                                   { excludeTypes: ["minecraft:player"] })) {
        if (e.typeId === "galaxy:pup") continue;
        hurt(e, p.damage ?? 24, c, "magic");
      }
      if (p.grief) grief(c, p.grief);
    } catch { /* ignore */ }
  }, STRIKE_DELAY);
}
