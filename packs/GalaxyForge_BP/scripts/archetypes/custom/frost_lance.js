// Twist: the beam stacks Chill on a target once per second of contact.  Five stacks freeze
// it solid (Slowness 255 for 3 s) and the ice shatters in a crystal burst.

import { status } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

const STACK_TICKS = 20;      // 1 s of contact per stack
const CHILL_MAX = 5;
const FREEZE_TICKS = 60;     // 3 s

export function onHit(ctx, target) {
  let last = 0;
  try { last = Number(target.getDynamicProperty("gx:chill_at")) || 0; } catch { /* ignore */ }
  if (ctx.tick - last < STACK_TICKS) return;         // one stack per second of contact

  let n = 0;
  try { n = Number(target.getDynamicProperty("gx:chill")) || 0; } catch { /* ignore */ }
  n++;
  try {
    target.setDynamicProperty("gx:chill_at", ctx.tick);
    target.setDynamicProperty("gx:chill", n);
  } catch { /* ignore */ }

  if (n < (ctx.def.params.chill_max ?? CHILL_MAX)) return;

  // Five stacks: freeze solid, then shatter (burst + reset so it can freeze again).
  status(target, "slowness", ctx.def.params.freeze_ticks ?? FREEZE_TICKS, 255);
  vfx.spawn(ctx.dim, "gx:crystal_burst", target.location,
            { color: ctx.def.palette.core, size: 0.9, life: 0.5, count: 6, speed: 1.1 });
  try { target.setDynamicProperty("gx:chill", 0); } catch { /* ignore */ }
}
