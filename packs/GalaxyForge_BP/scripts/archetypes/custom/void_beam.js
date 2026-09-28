// Twist: every beam hit stacks a Void Mark on the target (a ring over its head).  The
// fourth mark tears a rift: the target is yanked upward and released with heavy damage.

import { isProtected } from "../../engine/safety.js";
import { hurt } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

export function onHit(ctx, target) {
  if (!target) return;
  if (isProtected(target, ctx.player, {})) return;

  let n = 0;
  try { n = Number(target.getDynamicProperty("gx:void_mark")) || 0; } catch { return; }
  n++;

  const loc = target.location;
  if (n < (ctx.def.params.marks ?? 4)) {
    try { target.setDynamicProperty("gx:void_mark", n); } catch { /* ignore */ }
    vfx.spawn(ctx.dim, "gx:ring_wave", { x: loc.x, y: loc.y + 2.0, z: loc.z },
              { color: ctx.def.palette.glow, size: 0.4 + n * 0.12, life: 0.4 });
    return;
  }

  try { target.setDynamicProperty("gx:void_mark", 0); } catch { /* ignore */ }
  try { target.teleport({ x: loc.x, y: loc.y + 4, z: loc.z }); } catch { /* ignore */ }
  hurt(target, ctx.def.params.rift_damage ?? 20, ctx, "magic");
  vfx.spawn(ctx.dim, "gx:star_flash", loc, { color: ctx.def.palette.core, size: 1.6, life: 0.4 });
  vfx.spawn(ctx.dim, "gx:ring_wave", loc, { color: ctx.def.palette.glow, size: 2.4, life: 0.5 });
}
