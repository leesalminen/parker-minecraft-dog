// Twist: the bolt splits into 3 homing shards at 12 blocks (or on impact), shards keep
// the parent's remaining pierce, and can re-split once on a wall bounce.

import * as bolt from "../bolt.js";
import { dist } from "../../engine/ray.js";

export function onTick(c, b) {
  const p = c.def.params;
  if (!b.splitDone && b.splits === 0 && dist(b.loc, b.origin) >= (p.split_at ?? 12)) {
    b.splitDone = true;
    bolt.splitBolt(b, p.split ?? 3, { homing: p.split_homing, speed: p.split_speed });
  }
  if (b.lastBounces !== undefined && b.bounces > b.lastBounces &&
      b.splits < (p.max_splits ?? 2)) {
    bolt.splitBolt(b, p.split ?? 3, { homing: p.split_homing, speed: p.split_speed });
  }
  b.lastBounces = b.bounces;
}
