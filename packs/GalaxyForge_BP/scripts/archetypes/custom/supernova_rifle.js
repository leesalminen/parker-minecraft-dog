// Twist: 3 s overcharge fires a white slug that detonates as a supernova -- white-out
// screen flash, expanding double ring, distance-falloff blast, outward knockback and a
// collapsing field.  60 s cooldown; the melt is declared in params.grief (cap 30).

import { world, system } from "@minecraft/server";
import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { spawnField, hurt, knock } from "../../engine/damage.js";
import { entitiesNear, dist } from "../../engine/ray.js";
import { isProtected } from "../../engine/safety.js";
import { GLYPHS } from "../../generated/weapons.js";
import { muzzleLoc } from "../hitscan.js";

export function onPress(ctx) { ctx.st.charge = 0; ctx.st.charging = true; return true; }

export function onHold(ctx) {
    const d = ctx.def, st = ctx.st;
    const full = d.params.charge_ticks ?? 60;
    st.charge = Math.min(full + 10, (st.charge ?? 0) + 1);
    if (ctx.tick % 2 === 0) {
        const t = Math.min(1, st.charge / full);
        vfx.spawn(ctx.dim, d.vfx.charge, muzzleLoc(ctx),
                  { color: d.palette.core, size: 0.3 + 1.1 * t, life: 0.35, count: 3, speed: 1.6 });
    }
    if (st.charge === full) {                          // fully charged: a hard ring snaps out
        vfx.spawn(ctx.dim, "gx:ring_wave", muzzleLoc(ctx),
                  { color: d.palette.glow, size: 1.6, life: 0.4 });
    }
    return true;
}

export function onRelease(ctx) {
    const d = ctx.def, p = d.params, st = ctx.st;
    const ticks = st.charge ?? 0;
    st.charge = 0; st.charging = false;
    if (st.reload > 0 || st.cooldown > 0) return true;
    const mag = d.ammo.mag;
    if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }
    if (ticks < (p.min_ticks ?? 20)) return true;      // undercharged: nothing fires
    const tier = (p.tiers || []).filter((x) => ticks >= x.ticks).pop() || {};
    st.ammo = Math.max(0, (st.ammo ?? mag) - 1);
    bolt.fire(ctx, { force: true, count: 1, speed: tier.speed ?? p.speed,
                     gravity: p.gravity, damage: tier.damage ?? p.damage,
                     aoe: tier.aoe ?? p.aoe, size: tier.size ?? p.size,
                     lifetime: tier.lifetime ?? p.lifetime });
    st.cooldown = (tier.cooldown ?? p.cooldown ?? 60) * 20;   // after the shot: fire() refuses while hot
    return true;
}

export function onDetonate(ctx, b, loc) {
    const d = ctx.def, p = d.params;
    const radius = p.field_radius ?? 10;

    const owner = livePlayer(b.ownerId);
    if (owner) {
        try { owner.onScreenDisplay.updateSubtitle(GLYPHS.vignette_whiteout); } catch { /* ignore */ }
    }

    // white-out core, then the second ring a moment later (the double ring)
    vfx.spawn(ctx.dim, "gx:star_flash", loc, { color: d.palette.core, size: radius * 1.6, life: 0.4 });
    vfx.spawn(ctx.dim, "gx:ring_wave", loc, { color: d.palette.glow, size: radius, life: 0.5 });
    system.runTimeout(() => {
        try {
            vfx.spawn(ctx.dim, "gx:ring_wave", loc,
                      { color: d.palette.accent, size: radius * 1.6, life: 0.6 });
            vfx.spawn(ctx.dim, "gx:shock_disc", loc, { color: d.palette.trail, size: radius, life: 0.6 });
        } catch { /* ignore */ }
    }, 4);

    // damage falls off with distance from the centre; everything is knocked outward
    const near = entitiesNear(ctx.dim, loc, radius, { excludeTypes: ["minecraft:player"] });
    for (const e of near) {
        if (!e || isProtected(e, null, {})) continue;
        const f = Math.max(0, 1 - dist(loc, e.location) / radius);
        hurt(e, (p.collapse_dmg ?? 20) * f, ctx, "explosion");
        knock(e, ctx, p.collapse_knock ?? 1.6, "away");
    }

    // the nebula lingers, pushes, then collapses inward
    spawnField({ ...ctx, point: loc }, "supernova",
               { radius, life: p.field_life ?? 60, dps: p.field_dps ?? 6, push: p.field_push ?? 0.9,
                 extra: { collapse: { dmg: p.collapse_dmg ?? 20, knock: p.collapse_knock ?? 1.6 },
                          spawn: "gx:star_flash" } });
}

function livePlayer(id) {
    try { return world.getAllPlayers().find((p) => p.id === id) ?? null; } catch { return null; }
}
