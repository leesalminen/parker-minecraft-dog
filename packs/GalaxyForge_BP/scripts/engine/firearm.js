// Per-shot presentation for the realistic weapons: camera-shake recoil, ejected brass, and
// a muzzle smoke puff.  Each is opt-in through params (recoil / shell / smoke).

import { MolangVariableMap } from "@minecraft/server";
import { run } from "./cmd.js";
import { spend } from "./state.js";
import * as vfx from "./vfx.js";

const BRASS = { red: 0.85, green: 0.66, blue: 0.3, alpha: 1 };

export function recoil(ctx) {
  const r = ctx.def.params.recoil;
  if (!r) return;
  // Automatic weapons would stack a shake every tick; one shake covers ~3 ticks of fire.
  if (ctx.tick - (ctx.st.lastShake ?? -99) < 3) return;
  ctx.st.lastShake = ctx.tick;
  const k = ctx.st.aim ? 0.6 : 1;
  run(ctx.player, `camerashake add @s ${(r * k).toFixed(2)} ${Math.min(0.45, 0.08 + r * 0.5).toFixed(2)} rotational`);
}

export function shell(ctx, loc) {
  if (!ctx.def.params.shell || !spend("particles")) return;
  const v = ctx.view;
  const m = new MolangVariableMap();
  try {
    m.setColorRGBA("color", BRASS);
    m.setFloat("dir_x", -v.z);   // out of the right-hand ejection port
    m.setFloat("dir_z", v.x);
    ctx.dim.spawnParticle("gx:shell_eject", loc, m);
  } catch { /* ignore */ }
}

export function after(ctx, muzzle) {
  recoil(ctx);
  shell(ctx, muzzle);
  if (ctx.def.params.smoke) {
    vfx.spawn(ctx.dim, "gx:smoke_trail", muzzle, { color: ctx.def.palette.trail, size: 0.25, life: 0.7, alpha: 0.5 });
  }
}
