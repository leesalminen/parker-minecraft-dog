// Twist: paw bolts heal a tamed galaxy:pup and grant Speed + Strength for 10 s instead of
// hurting it.  Sneak-fire launches a bone starburst that calls every tamed pup within 30
// blocks to your side, dashing them along a stardust trail.

import * as bolt from "../bolt.js";
import * as vfx from "../../engine/vfx.js";
import { heal, status } from "../../engine/damage.js";
import { isTamed } from "../../engine/safety.js";
import { dist } from "../../engine/ray.js";
import { projectiles } from "../../engine/state.js";
import { muzzleLoc } from "../hitscan.js";

const PUP = "galaxy:pup";

export function onPress(ctx) {
    const d = ctx.def, p = d.params, st = ctx.st;
    if (ctx.player.isSneaking !== true) return false;      // ordinary paw bolt
    if (st.reload > 0 || st.cooldown > 0) return true;
    if (ctx.tick - st.lastFire < (p.rate ?? 10)) return true;
    const mag = d.ammo.mag;
    if ((st.ammo ?? mag) <= 0) { st.wantReload = true; return true; }

    st.lastFire = ctx.tick;
    st.ammo = Math.max(0, (st.ammo ?? mag) - 1);

    // Bone-shaped starburst: a fat bone-particle slug that dashes the pack home.
    bolt.fire(ctx, { force: true, count: 1, size: (p.size ?? 0.5) * 1.8,
                     damage: (p.damage ?? 15) * 0.6, aoe: p.aoe ?? 2 });
    const b = projectiles[projectiles.length - 1];
    if (b && b.def === d && b.ownerId === ctx.player.id) b.bone = true;
    vfx.spawn(ctx.dim, "gx:orb_bone", muzzleLoc(ctx),
              { color: d.palette.accent, size: 0.9, life: 0.4, count: 3 });

    const home = ctx.player.location;
    const pups = pupsNear(ctx.dim, home, p.call_radius ?? 30);
    pups.forEach((pup, i) => {
        const a = (i / Math.max(1, pups.length)) * Math.PI * 2;
        const r = (p.dash_offset ?? 0.6) + 0.8 * i;
        const dest = { x: home.x + Math.cos(a) * r, y: home.y, z: home.z + Math.sin(a) * r };
        vfx.line(ctx.dim, pup.location, dest, "gx:star_flash", d.palette,
                 { step: 1.4, max: 20, size: 0.3, life: 0.5 });
        try { pup.teleport(dest); } catch { /* ignore */ }
        vfx.spawn(ctx.dim, "gx:star_flash", dest, { color: d.palette.glow, size: 0.6, life: 0.4 });
    });
    return true;
}

export function onHit(ctx, target) {
    if (!target || target.typeId !== PUP) return;
    const p = ctx.def.params, d = ctx.def, loc = target.location;
    heal(target, p.heal ?? 8);
    status(target, "speed", p.buff_ticks ?? 200, 1);
    status(target, "strength", p.buff_ticks ?? 200, 1);
    try { target.applyImpulse({ x: 0, y: 0.35, z: 0 }); } catch { /* ignore */ }   // happy jump
    vfx.spawn(ctx.dim, "gx:star_flash", loc,
              { color: d.palette.glow, size: 0.7, life: 0.5, count: 2 });         // hearts
    vfx.spawn(ctx.dim, "gx:orb_paw", loc, { color: d.palette.accent, size: 0.6, life: 0.6 });
    vfx.spawn(ctx.dim, "gx:smoke_trail", loc, { color: d.palette.trail, size: 0.4, life: 0.8 });
}

/** Stardust wake behind the bone slug. */
export function onTick(c, b) {
    if (!b.bone || b.life % 2 !== 0) return;
    vfx.spawn(b.dim, "gx:orb_bone", b.loc, { color: b.pal.accent, size: b.size, life: 0.3 });
}

/** Every tamed pup of the galaxy family inside the call radius. */
function pupsNear(dim, loc, radius) {
    let list = [];
    try { list = dim.getEntities({ families: ["galaxy_pup"], location: loc, maxDistance: radius }); }
    catch { list = []; }
    return list.filter((e) => e && e.typeId === PUP && isTamed(e) &&
                              dist(loc, e.location) <= radius);
}
