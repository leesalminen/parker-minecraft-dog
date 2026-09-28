// Twist: the coil stores charge — once three shots land inside 2 s, a beat later the arc
// reaches one target further out.  The extra jump is deferred a tick so it gets its own
// query budget (a same-tick jump would be starved by the chain's own lookups).

import { system } from "@minecraft/server";
import * as chain from "../chain.js";
import { entitiesNear } from "../../engine/ray.js";
import { hurt } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

export function onPress(ctx) {
  const d = ctx.def, p = d.params, st = ctx.st;
  if (ctx.tick - st.lastFire < (p.rate ?? 8)) return false;
  if (st.reload > 0 || st.cooldown > 0) return false;
  if (d.ammo.type === "cell" && (st.ammo ?? d.ammo.mag) <= 0) return false;

  if (ctx.tick - (st.scratch.lastShot ?? -9999) > (p.streak_ticks ?? 40)) st.scratch.streak = 0;
  st.scratch.streak = (st.scratch.streak ?? 0) + 1;
  st.scratch.lastShot = ctx.tick;
  st.scratch.hit = [];
  st.scratch.hitIds = new Set();

  if ((st.scratch.streak ?? 0) < (p.streak_shots ?? 3)) return false;   // let the archetype fire

  chain.arc(ctx);                                  // charged shot, fired here
  const last = st.scratch.hit[st.scratch.hit.length - 1];
  if (last) {
    const from = { ...last.location };
    const ids = new Set(st.scratch.hitIds);
    system.runTimeout(() => { try { extraJump(ctx, from, ids); } catch { /* ignore */ } }, 1);
  }
  return true;
}

export function onHit(ctx, target) {
  const st = ctx.st;
  if (!st.scratch.hit) return;
  st.scratch.hit.push(target);
  st.scratch.hitIds.add(target.id);
}

function extraJump(ctx, from, ids) {
  const d = ctx.def, p = d.params;
  const near = entitiesNear(ctx.dim, from, p.radius ?? 6, { excludeTypes: ["minecraft:player"] });
  const next = near.find((e) => e && !ids.has(e.id));
  if (!next) return;
  hurt(next, (p.damage ?? 7) * (p.falloff ?? 0.85), { ...ctx, point: next.location }, "lightning");
  vfx.line(ctx.dim, from, next.location, "gx:lightning_fork", d.palette,
           { step: 0.6, max: 20, size: 0.5, life: 0.25 });
  vfx.spawn(ctx.dim, "gx:static_arc", next.location,
            { color: d.palette.core, size: 1.1, life: 0.3 });
}
