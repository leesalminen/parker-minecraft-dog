// Twist: mining cutter. Dig speed ramps while the beam stays on the same block, ore
// blocks sparkle, and the blocks mined are counted in the action bar. Every block change
// goes through the grief effect (mobGriefing-gated, capped).

import { raycast, add } from "../../engine/ray.js";
import { applyEffects, hurt, grief } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";
import * as sound from "../../engine/sound.js";
import * as heat from "../../engine/heat.js";
import { muzzleLoc } from "../hitscan.js";

export function onHold(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.reload > 0 || st.cooldown > 0) return true;
  if (d.heat && heat.isHot(st, d)) return true;

  st.beam = (st.beam ?? 0) + 1;
  heat.add(st, d, p.heat_rate ?? 1);

  const r = raycast(ctx.dim, ctx.eye, ctx.view, p.range ?? 6);
  const point = r.point || add(ctx.eye, ctx.view, p.range ?? 6);

  if (r.entity && ctx.tick % (p.tick_rate ?? 4) === 0) {
    const c = { ...ctx, point };
    applyEffects(c, d.hooks?.on_hit, r.entity);
    hurt(r.entity, (p.dps ?? 10) * (p.tick_rate ?? 4) / 20, c, "magic");
  } else if (r.block) {
    mine(ctx, r.block, { ...ctx, point });
  }

  vfx.line(ctx.dim, muzzleLoc(ctx), point, d.vfx.body, d.palette,
           { step: 0.3, max: 12, size: p.width ?? 0.2, life: 0.2 });
  if (!st.beamStarted) {
    st.beamStarted = true;
    st.charges = 0;
    st.scratch.mineBlock = null;
    sound.play(ctx.player, d.sound);
    vfx.muzzle(ctx.dim, muzzleLoc(ctx), d.palette,
               { size: 0.35, effect: d.vfx.muzzle });
  }
  return true;
}

function mine(ctx, block, c) {
  const d = ctx.def, p = d.params, st = ctx.st;
  const id = block.typeId;
  if (!(p.mineable ?? []).includes(id)) return;

  const key = `${block.location.x},${block.location.y},${block.location.z}`;
  if (st.scratch.mineBlock !== key) { st.scratch.mineBlock = key; st.scratch.ramp = 0; }
  st.scratch.ramp = Math.min(p.ramp_ticks ?? 60, (st.scratch.ramp ?? 0) + 1);

  // ramp: 8 ticks per block when cold, 2 ticks at full ramp
  const every = Math.max(2, Math.round(8 - 6 * st.scratch.ramp / (p.ramp_ticks ?? 60)));
  if (ctx.tick % every !== 0) return;

  // base.y + 1 puts the target block at the first slot grief tries (dy = -1)
  const n = grief({ ...c, point: { x: block.location.x, y: block.location.y + 1, z: block.location.z } },
                  { radius: 0, from: [id], to: "minecraft:air", cap: 1 });
  if (!n) return;

  st.charges = Math.min(p.charges ?? 12, (st.charges ?? 0) + 1);
  vfx.spawn(ctx.dim, "gx:ember_trail", c.point,
            { color: d.palette.glow, size: 0.25, life: 0.6 });
  vfx.spawn(ctx.dim, "gx:spark_burst", c.point,
            { color: d.palette.core, size: 0.3, life: 0.3, count: 4 });
  if (id.includes("_ore")) {
    vfx.spawn(ctx.dim, "gx:crystal_burst", c.point,
              { color: d.palette.accent, size: 0.5, life: 0.5, count: 3 });
  }
}
