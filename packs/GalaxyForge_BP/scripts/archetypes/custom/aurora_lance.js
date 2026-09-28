// Twist: the beam cycles fire -> ice -> shock -> toxic once a second, recolouring the beam
// (and the aim dot) and applying that element's status on contact.  Combos: fire into ice
// shatters for bonus damage, ice into shock arcs to nearby mobs.

import * as vfx from "../../engine/vfx.js";
import { status, hurt, chain } from "../../engine/damage.js";
import { isProtected } from "../../engine/safety.js";
import { muzzleLoc } from "../hitscan.js";

// Per-element palettes in the engine's RGB-float form, plus the colour the aim dot takes.
const ELEMENTS = [
    { name: "fire", dot: [1, 0.45, 0.15],
      pal: { core: [1, 0.95, 0.8], glow: [1, 0.45, 0.15], trail: [0.6, 0.15, 0.05],
             accent: [1, 0.75, 0.35] } },
    { name: "ice", dot: [0.45, 0.8, 1],
      pal: { core: [0.95, 0.99, 1], glow: [0.45, 0.8, 1], trail: [0.1, 0.35, 0.7],
             accent: [0.75, 0.92, 1] } },
    { name: "shock", dot: [1, 0.9, 0.3],
      pal: { core: [1, 1, 0.85], glow: [1, 0.9, 0.3], trail: [0.6, 0.5, 0.05],
             accent: [1, 0.98, 0.6] } },
    { name: "toxic", dot: [0.5, 1, 0.3],
      pal: { core: [0.9, 1, 0.8], glow: [0.5, 1, 0.3], trail: [0.2, 0.55, 0.1],
             accent: [0.75, 1, 0.55] } },
];

export function onPress(ctx) { ctx.st.mode = ctx.st.mode ?? 0; return false; }

export function onHold(ctx) {
    const d = ctx.def, p = d.params, st = ctx.st;
    // beam.hold calls this again in the same tick; advance the cycle only once.
    if (st.scratch.elemTick !== ctx.tick) {
        st.scratch.elemTick = ctx.tick;
        const idx = Math.floor(ctx.tick / (p.element_ticks ?? 20)) % ELEMENTS.length;
        if (idx !== st.mode) {
            st.mode = idx;
            const e = ELEMENTS[idx];
            d.dot.color = e.dot;                       // the aim dot follows the element
            vfx.spawn(ctx.dim, "gx:ring_wave", muzzleLoc(ctx),
                      { color: e.pal.glow, size: 0.9, life: 0.35 });
            vfx.spawn(ctx.dim, "gx:field_glow", ctx.player.location,
                      { color: e.pal.accent, size: 1.6, life: 0.6, alpha: 0.35 });
        }
    }

    const e = ELEMENTS[(st.mode ?? 0) % ELEMENTS.length];
    if (ctx.point) {                                   // recolour the beam body
        vfx.line(ctx.dim, muzzleLoc(ctx), ctx.point, d.vfx.body, e.pal,
                 { step: 0.5, max: 40, size: p.width ?? 0.34, life: 0.2 });
    }
    if (ctx.tick % 8 === 0) {                          // aurora ribbons above the wielder
        vfx.spawn(ctx.dim, d.vfx.idle, ctx.player.location,
                  { color: e.pal.accent, size: 0.35, life: 0.7, alpha: 0.5 });
    }
    return false;                                      // the beam archetype owns the tick
}

export function onRelease(ctx) { ctx.st.mode = ctx.st.mode ?? 0; return false; }

export function onHit(ctx, target) {
    const p = ctx.def.params, st = ctx.st;
    if (isProtected(target, ctx.player, {})) return;
    const e = ELEMENTS[(st.mode ?? 0) % ELEMENTS.length];
    const ticks = p.status_ticks ?? 60;

    if (e.name === "fire") { try { target.setOnFire(4, true); } catch { /* ignore */ } }
    else if (e.name === "ice") status(target, "slowness", ticks, 2);
    else if (e.name === "shock") {
        status(target, "slowness", ticks, 6);          // stun, machine vocabulary
        status(target, "weakness", ticks, 2);
    } else status(target, "poison", ticks, 1);

    const at = ctx.point || target.location;
    vfx.spawn(ctx.dim, "gx:spark_burst", at,
              { color: e.pal.glow, size: 0.5, life: 0.35, count: 4, speed: 1.2 });

    const prev = st.scratch.prevElement;
    const tickDmg = (p.dps ?? 30) * (p.tick_rate ?? 4) / 20;
    if (prev === "fire" && e.name === "ice") {         // shatter combo
        vfx.spawn(ctx.dim, "gx:crystal_burst", target.location,
                  { color: e.pal.core, size: 0.8, life: 0.5, count: 6, speed: 1.1 });
        hurt(target, tickDmg * (p.combo_mult ?? 1.3), ctx, "magic");
    } else if (prev === "ice" && e.name === "shock") { // arc combo
        vfx.spawn(ctx.dim, "gx:lightning_fork", target.location,
                  { color: e.pal.glow, size: 0.9, life: 0.3 });
        chain(ctx, target, { jumps: 2, radius: p.arc_radius ?? 6, falloff: 0.8, dmg: tickDmg * 0.6 });
    }
    st.scratch.prevElement = e.name;
}
