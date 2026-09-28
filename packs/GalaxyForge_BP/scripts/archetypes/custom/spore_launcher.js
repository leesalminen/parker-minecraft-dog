// Twist: the pod bursts into a poison cloud and throws three homing spore darts.  The cloud
// is declared on the def's on_hit; the darts need code.
//
// Darts are fired with aoe 0 and splits >= 1 so they never split or detonate a second time:
// only the original pod (splits 0) releases spores.

import * as bolt from "../bolt.js";
import { projectiles } from "../../engine/state.js";
import { spawnField } from "../../engine/damage.js";
import { norm } from "../../engine/ray.js";

export function onDetonate(c, b, loc) {
  if (b.splits > 0) return;                 // a dart just pops; only the pod bursts
  const p = c.def.params;

  // One cloud for the blast itself: on_hit would otherwise stack one per mob caught.
  spawnField({ ...c, point: loc }, "spore_cloud",
             { radius: p.cloud_radius ?? 3, life: p.cloud_life ?? 100, dps: p.cloud_dps ?? 2,
               extra: { status: [{ id: "poison", ticks: 60, amp: 0 }], spawn: "gx:orb_soft_orb" } });
  b.onHit = null;

  const n = p.split ?? 3;
  bolt.fire({ ...c, eye: loc, view: norm(b.vel), tick: 0, st: {} },
            { force: true, count: n, spread: 28, gravity: 0,
              speed: p.split_speed ?? p.speed, homing: p.split_homing ?? 8,
              life: p.split_life ?? 60, damage: p.split_damage ?? p.damage,
              size: p.split_size ?? p.size, aoe: 0 });
  for (let k = 0; k < n; k++) projectiles[projectiles.length - 1 - k].splits = 1;
}
