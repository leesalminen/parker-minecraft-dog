// Twist: perfect vent.  At overheat a 2s vent window opens (the action bar shows a
// sliding marker).  Releasing inside the green zone clears heat instantly and grants a
// 3s damage boost; releasing outside it just vents the heat.

import * as bolt from "../bolt.js";
import * as heat from "../../engine/heat.js";
import { GLYPHS } from "../../generated/weapons.js";

export function onPress(ctx) { return maybeFire(ctx); }
export function onHold(ctx) { return maybeFire(ctx); }

function maybeFire(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (st.vent > 0) return true;                      // venting: no firing
  if (heat.isHot(st, d)) { st.vent = 40; return true; }
  if (ctx.tick - st.lastFire < p.rate) return true;
  if (st.reload > 0 || st.cooldown > 0) return true;
  st.lastFire = ctx.tick;
  heat.add(st, d, d.heat.per_shot);
  const mult = st.boost > 0 ? (p.vent_mult ?? 1.35) : 1;
  bolt.fire(ctx, { force: true, count: 1, damage: p.damage * mult });
  return true;
}

export function onRelease(ctx) {
  const st = ctx.st, d = ctx.def;
  if (st.vent > 0) {
    if (heat.inVentZone(st, d)) {
      heat.clear(st);
      st.boost = 60;
      try { ctx.player.onScreenDisplay.updateSubtitle(GLYPHS.marker_kill); } catch { /* ignore */ }
    }
    st.vent = 0;
  }
  return false;
}
