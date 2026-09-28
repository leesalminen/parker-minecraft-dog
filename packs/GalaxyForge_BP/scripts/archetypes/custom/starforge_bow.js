// Twist: a stuck arrow becomes a constellation node (8 s).  While the bow is held, nodes
// link with luminous lines, and three or more form a twinkling star field that burns mobs
// inside (10 dps).  Past five nodes the oldest is recycled.

import { world } from "@minecraft/server";
import { getState, tick } from "../../engine/state.js";
import { spawnField } from "../../engine/damage.js";
import * as vfx from "../../engine/vfx.js";

const LINK = "gx:beam_needle";

/** The bolt's ctx.player is a stub, so resolve the wielder's live state by id. */
function stateFor(id) {
    try {
        const p = world.getAllPlayers().find((x) => x.id === id);
        return p ? getState(p) : null;
    } catch { return null; }
}

export function onTick(c, b) {
    if (!b.stuck || b.node) return;
    const st = stateFor(b.ownerId);
    if (!st) return;
    b.node = true;
    const nodes = st.scratch.nodes ?? (st.scratch.nodes = []);
    nodes.push({ x: b.loc.x, y: b.loc.y, z: b.loc.z,
                 until: tick + (c.def.params.node_life ?? 160) });
    while (nodes.length > (c.def.params.node_max ?? 5)) nodes.shift();
    vfx.spawn(b.dim, "gx:star_flash", b.loc, { color: b.pal.core, size: 0.6, life: 0.3 });
}

export function onHold(ctx) {
    const d = ctx.def, p = d.params, st = ctx.st;
    const nodes = st.scratch.nodes ?? (st.scratch.nodes = []);
    for (let i = nodes.length - 1; i >= 0; i--) if (nodes[i].until <= ctx.tick) nodes.splice(i, 1);
    if (nodes.length < 2) return false;

    // Luminous lines between every pair of live nodes (a full constellation diagram).
    if (ctx.tick % (p.node_link ?? 24) === 0) {
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                vfx.line(ctx.dim, nodes[i], nodes[j], LINK, d.palette,
                         { step: 1.0, max: 24, size: 0.16, life: 0.5 });
            }
        }
    }

    // Three nodes close a triangle: a star field burns anything inside it.
    if (nodes.length >= 3 && ctx.tick - (st.scratch.fieldAt ?? -999) > 40) {
        st.scratch.fieldAt = ctx.tick;
        const mid = nodes.reduce((a, n) => ({ x: a.x + n.x / nodes.length,
                                              y: a.y + n.y / nodes.length,
                                              z: a.z + n.z / nodes.length }),
                                 { x: 0, y: 0, z: 0 });
        spawnField({ ...ctx, point: mid }, "constellation",
                   { radius: p.field_radius ?? 4, life: p.field_life ?? 80,
                     dps: p.field_dps ?? 10, extra: { spawn: "gx:star_flash" } });
        vfx.spawn(ctx.dim, "gx:field_glow", mid,
                  { color: d.palette.accent, size: (p.field_radius ?? 4) * 2, life: 0.6, alpha: 0.3 });
    }
    return false;
}
