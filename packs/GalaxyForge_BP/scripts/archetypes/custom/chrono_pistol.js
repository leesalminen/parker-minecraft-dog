// Twist: a hit tags the target for 3 s, recording its position every tick.  Sneak-fire
// rewinds it to where it stood, dealing damage proportional to the distance travelled.
// A failed teleport is sanctioned by DEVIATIONS.md: the damage and the streak still land.

import * as vfx from "../../engine/vfx.js";
import * as sound from "../../engine/sound.js";
import { hurt } from "../../engine/damage.js";
import { isProtected } from "../../engine/safety.js";
import { dist } from "../../engine/ray.js";

const TICK_TOCK = [["note.pling", 0.6, 0.7, 0], ["note.pling", 0.6, 1.2, 4]];

function targetFor(ctx, tag) {
    try { return ctx.dim.getEntity(tag.id) ?? null; } catch { return null; }
}

export function onHit(ctx, target) {
    if (isProtected(target, ctx.player, {})) return;      // never tag a pup / tamed mob
    const p = ctx.def.params, st = ctx.st, loc = target.location;
    st.scratch.tag = { id: target.id, until: ctx.tick + (p.rewind_ticks ?? 60),
                       trail: [{ x: loc.x, y: loc.y, z: loc.z }], dist: 0 };
    vfx.spawn(ctx.dim, "gx:ring_wave", loc,
              { color: ctx.def.palette.accent, size: 1.0, life: 0.5 });   // clock-face ring
    vfx.spawn(ctx.dim, "gx:field_glow", loc,
              { color: ctx.def.palette.glow, size: 1.2, life: 0.6, alpha: 0.35 });
}

/** Record the tagged target's path each tick while the pistol is held. */
export function onHold(ctx) {
    const st = ctx.st, tag = st.scratch.tag;
    if (!tag) return false;
    if (ctx.tick > tag.until) { st.scratch.tag = null; return false; }
    const target = targetFor(ctx, tag);
    if (!target) { st.scratch.tag = null; return false; }

    const loc = target.location;
    const last = tag.trail[tag.trail.length - 1];
    tag.dist += dist(last, loc);
    tag.trail.push({ x: loc.x, y: loc.y, z: loc.z });
    while (tag.trail.length > (ctx.def.params.trail_max ?? 60)) tag.trail.shift();
    if (ctx.tick % 4 === 0) {
        vfx.spawn(ctx.dim, "gx:field_glow", loc,
                  { color: ctx.def.palette.glow, size: 0.5, life: 0.4, alpha: 0.4 });
    }
    return false;
}

export function onPress(ctx) {
    const d = ctx.def, p = d.params, st = ctx.st;
    const tag = st.scratch.tag;
    if (ctx.player.isSneaking !== true || !tag || tag.trail.length < 2) return false; // normal shot
    if (ctx.tick - (st.scratch.rewindAt ?? -999) < (p.rewind_cooldown ?? 30)) return false;

    const target = targetFor(ctx, tag);
    st.scratch.tag = null;
    st.scratch.rewindAt = ctx.tick;
    if (!target) return true;

    const start = tag.trail[0];
    const here = target.location;
    const dmg = Math.min(p.rewind_dmg_max ?? 30, tag.dist * (p.rewind_dmg_per_block ?? 3));

    // The recorded path plays back as a streak of afterimages.
    vfx.line(ctx.dim, here, start, d.vfx.body, d.palette, { step: 1.2, max: 30, size: 0.2, life: 0.5 });
    for (let i = 0; i < tag.trail.length; i += 4) {
        vfx.spawn(ctx.dim, "gx:star_flash", tag.trail[i], { color: d.palette.glow, size: 0.3, life: 0.6 });
    }
    sound.play(ctx.player, TICK_TOCK);

    try { target.teleport(start); } catch { /* unsupported spot: damage + streak only */ }
    if (!isProtected(target, ctx.player, {})) hurt(target, dmg, ctx, "magic");
    vfx.spawn(ctx.dim, "gx:ring_wave", start, { color: d.palette.accent, size: 1.2, life: 0.5 });
    return true;
}
