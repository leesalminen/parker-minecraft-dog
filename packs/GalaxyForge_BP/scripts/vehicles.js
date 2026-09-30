// Galaxy vehicles: gx:car, gx:plane, gx:helicopter.
//
// Native components do the basic driving (input_ground_controlled for the car, input_air_controlled
// for the aircraft).  This module layers on the things Bedrock has no component for: gliding up
// slopes / steps without hopping (car), forgiving takeoff, cruise and landing (plane) and hover /
// climb-by-looking / soft landing (helicopter).  See docs/vehicles.md for the reasoning and limits.
//
// Everything runs from ONE system.runInterval and only touches vehicles (family "gx_vehicle").
// Vertical motion is done with applyImpulse so the client sees ordinary smooth physics, never
// teleport pops.  Every tunable is in the CFG block below.

import { world, system } from "@minecraft/server";

const CFG = {
  car: {
    halfWidth: 0.95,     // collision half width; ground must already be reached when this close
    slope: 0.4,          // max climb rise per block travelled (0.4 = ~22 degrees)
    lookahead: 10,       // blocks scanned ahead along the heading
    maxUp: 0.35,         // max climb speed (blocks/tick)
    lead: 1.1,           // finish each rise this far before the nose reaches the step
    slew: 0.06,         // max change in vertical speed per tick (removes any jerk)
    maxDown: 0.16,       // max descent speed while the ground is lower (soft drop-off)
    headroom: 2,         // free blocks needed above a surface for the car to fit
    reach: 3,            // tallest single rise we will ramp up (blocks); higher is treated as a wall
    gain: 0.5,           // P gain on height error
    stuckTicks: 6,       // ticks pressed against a step before the teleport safety net nudges up
  },
  plane: {
    cruise: 0.22,        // blocks/tick the plane keeps once airborne, even with no key held
    takeoff: 0.2,        // ground speed at which looking up lifts the nose off
    turn: 0.09,          // how fast velocity swings toward where the pilot looks
    sinkMax: 0.12,       // never fall faster than this (soft landings, no crashes)
    rollAccel: 0.012,    // ground-roll acceleration while the pilot looks up
    climb: 0.16,         // max climb rate at full up-pitch
  },
  heli: {
    upStart: 30,         // degrees of look-up before the copter climbs
    downStart: 45,       // degrees of look-down before it descends
    maxUp: 0.2,
    maxDown: 0.15,
    drag: 0.93,          // horizontal drag per tick so it stops when you let go
    landSlow: 0.07,      // max descent rate within 2 blocks of the ground
  },
};

const GRAVITY = 0.08;    // vanilla per-tick gravity on a mob, added back when we hold a vertical rate

let debugLogged = false;
function warnOnce(e) {
  if (debugLogged) return;
  debugLogged = true;
  console.warn(`[GalaxyForge/vehicles] ${e?.message ?? e}\n${e?.stack ?? ""}`);
}

// ------------------------------------------------------------------ terrain sampling

const NONSOLID_RE = /(grass|fern|flower|sapling|vine|torch|sign|rail|button|lever|snow_layer|carpet|plant|mushroom|wheat|carrots|potatoes|beetroot|dandelion|poppy|sweet_berry|redstone_wire|tripwire|cobweb|web|banner|pressure_plate|fire|coral_fan|kelp|seagrass|roots|sprouts|petals|moss_carpet|lantern_hanging)/;

function isSolid(block) {
  if (!block) return false;
  if (block.isAir || block.isLiquid) return false;
  if (typeof block.isSolid === "boolean") return block.isSolid;
  return !NONSOLID_RE.test(block.typeId);
}

// Top-surface offset inside the block (bottom slabs are only half a block tall).
function topOffset(block) {
  const id = block.typeId;
  if (id.endsWith("_slab") && !id.includes("double")) {
    try {
      if (block.permutation.getState("minecraft:vertical_half") === "bottom") return 0.5;
    } catch { /* ignore */ }
  }
  return 1;
}

// Height of the highest standable surface in column (x,z) within reach of yRef, or null if none/unloaded.
// Walks down from the top; a surface counts only if `headroom` blocks above it are free, so tree
// canopies, cave roofs and overhangs are ignored instead of being climbed.
function scanColumn(dim, x, z, yRef, cfg) {
  const top = Math.floor(yRef) + cfg.reach + cfg.headroom;
  const bottom = Math.floor(yRef) - 6;
  let air = 0;
  for (let y = top; y >= bottom; y--) {
    let b;
    try { b = dim.getBlock({ x, y, z }); } catch { return null; }
    if (!b) return null;
    if (isSolid(b)) {
      if (air >= cfg.headroom) {
        const h = y + topOffset(b);
        if (h <= yRef + cfg.reach + 0.51) return h;
        return null;      // too tall to climb: a wall
      }
      air = 0;            // solid but no headroom (roof / wall interior): keep looking lower
    } else {
      air++;
    }
  }
  return null;
}

const colCache = new Map();  // "dim|x|z|ybucket" -> { h, t }
let cacheSweep = 0;
function groundAt(dim, wx, wz, yRef, cfg, now) {
  const x = Math.floor(wx), z = Math.floor(wz);
  const key = `${dim.id}|${x}|${z}|${Math.floor(yRef)}`;
  const hit = colCache.get(key);
  if (hit && now - hit.t < 25) return hit.h;
  const h = scanColumn(dim, x, z, yRef, cfg);
  colCache.set(key, { h, t: now });
  if (++cacheSweep > 600) {
    cacheSweep = 0;
    for (const [k, v] of colCache) if (now - v.t > 50) colCache.delete(k);
  }
  return h;
}

// Height above the surface straight below (up to 64 blocks), or Infinity.
function altitude(entity, ignoreLiquid = true) {
  try {
    const hit = entity.dimension.getBlockFromRay(entity.location, { x: 0, y: -1, z: 0 },
      { maxDistance: 64, includeLiquidBlocks: !ignoreLiquid, includePassableBlocks: false });
    if (!hit) return Infinity;
    return entity.location.y - (hit.block.location.y + topOffset(hit.block));
  } catch { return Infinity; }
}

// ------------------------------------------------------------------ helpers

function riders(entity) {
  try { return entity.getComponent("minecraft:rideable")?.getRiders() ?? []; } catch { return []; }
}

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const dirOfYaw = (yawDeg) => {
  const r = (yawDeg * Math.PI) / 180;
  return { x: -Math.sin(r), z: Math.cos(r) };
};

function impulseY(e, dv) {
  if (Math.abs(dv) < 0.002) return;
  try { e.applyImpulse({ x: 0, y: dv, z: 0 }); } catch (err) { warnOnce(err); }
}

// Vertical speed hold for the aircraft.  Hover/fly mobs may or may not have gravity applied by the
// engine, so instead of assuming, learn it: g = how much vertical speed the engine took away since
// we last set it.  Returns the impulse Y that makes the entity's next-tick vertical speed vyDes.
const holdState = new Map();  // id -> { set, g }
function holdVy(e, vyDes, vel, active = true) {
  let s = holdState.get(e.id);
  if (!s) { s = { set: null, g: 0 }; holdState.set(e.id, s); }
  if (!active) { s.set = null; return 0; }
  if (s.set !== null) s.g = s.g * 0.7 + clamp(s.set - vel.y, 0, 0.12) * 0.3;
  const iy = vyDes + s.g - vel.y;
  s.set = vyDes + s.g;
  return iy;
}

// ------------------------------------------------------------------ car

const carState = new Map();  // entity.id -> { stuck, groundHv, assist }

function tickCar(car, now) {
  const cfg = CFG.car;
  const st = carState.get(car.id) ?? { stuck: 0, groundHv: 0, assist: 0, vy: 0 };
  carState.set(car.id, st);

  const dim = car.dimension;
  const loc = car.location;
  const vel = car.getVelocity();
  const hv = Math.hypot(vel.x, vel.z);
  const onGround = car.isOnGround === true;
  if (onGround) st.groundHv = Math.max(hv, st.groundHv * 0.97);

  // heading: where we are going; fall back to where the nose points when (nearly) stopped
  let dx, dz;
  if (hv > 0.05) { dx = vel.x / hv; dz = vel.z / hv; }
  else { const d = dirOfYaw(car.getRotation().y); dx = d.x; dz = d.z; }
  const px = -dz, pz = dx;    // lateral axis

  // ramp target: highest of (surface - slope * distance-beyond-our-own-footprint) over the scan
  let target = -Infinity, bestS = 0, known = false;
  const sample = (s, lat) => {
    const h = groundAt(dim, loc.x + dx * s + px * lat, loc.z + dz * s + pz * lat, loc.y, cfg, now);
    if (h === null) return;
    known = true;
    const t = h - cfg.slope * Math.max(0, s - cfg.halfWidth - cfg.lead);
    if (t > target) { target = t; bestS = s; }
  };
  for (const lat of [-0.8, 0, 0.8]) for (const s of [0, 1, 2]) sample(s, lat);
  for (let s = 3; s <= cfg.lookahead; s += 0.5) sample(s, 0);   // fine steps: ramp starts smoothly, cache dedupes columns
  if (!known) return;         // over the void / unloaded chunk: leave physics alone

  const err = target - loc.y;

  if (err > 0.03) {
    // climbing: feed-forward the ramp's rise rate so we don't lag behind it, plus a P term
    const ff = bestS > cfg.halfWidth + cfg.lead ? hv * cfg.slope : 0;
    let vyDes = clamp(ff + err * cfg.gain, 0.02, cfg.maxUp);
    vyDes = Math.min(vyDes, Math.sqrt(2 * cfg.slew * err * 0.8));   // braking curve: arrive at the crest with ~0 climb speed
    vyDes = clamp(vyDes, st.vy - cfg.slew, st.vy + cfg.slew);   // jerk limit: ease in, never a kick
    st.vy = vyDes;
    impulseY(car, vyDes + GRAVITY - vel.y);
    st.assist = 8;
    // A ground-controlled entity gets weak steering in the air; keep momentum while we carry it up.
    if (!onGround && st.groundHv > 0.1 && hv < st.groundHv * 0.9) {
      const boost = Math.min(0.05, st.groundHv * 0.9 - hv);
      try { car.applyImpulse({ x: dx * boost, y: 0, z: dz * boost }); } catch (e) { warnOnce(e); }
    }
    // safety net: pressed against a step and not rising -> nudge with a tiny teleport
    if (hv < 0.02 && vel.y < 0.02) {
      st.stuck++;
      if (st.stuck > cfg.stuckTicks) {
        try { car.teleport({ x: loc.x, y: loc.y + Math.min(0.2, err), z: loc.z }, { keepVelocity: true }); } catch (e) { warnOnce(e); }
      }
    } else st.stuck = 0;
  } else {
    st.stuck = 0;
    if (st.vy > 0.005 && !onGround) {
      // reached the top of the ramp: ease the climb out instead of cutting it (no hop off the crest)
      st.vy = Math.max(0, st.vy - cfg.slew);
      impulseY(car, st.vy + GRAVITY - vel.y);
    } else if (err < -0.05 && !onGround) {
      // ground fell away: sink softly instead of dropping
      const vyDes = Math.max(-cfg.maxDown, err * 0.2);
      if (vel.y < vyDes) impulseY(car, vyDes + GRAVITY - vel.y);
      st.vy = 0;
    } else st.vy = 0;
  }
}

// ------------------------------------------------------------------ plane

function tickPlane(plane, pilot, now) {
  const cfg = CFG.plane;
  const vel = plane.getVelocity();
  const hv = Math.hypot(vel.x, vel.z);
  const alt = altitude(plane);
  const airborne = alt > 0.6;
  const look = pilot.getViewDirection();                   // unit vector
  const pitchUp = Math.asin(clamp(look.y, -1, 1)) * 180 / Math.PI;   // + = nose up
  const lh = Math.hypot(look.x, look.z) || 1;
  const fx = look.x / lh, fz = look.z / lh;                 // horizontal look direction

  if (!airborne) {
    holdVy(plane, 0, vel, false);
    // ground roll: look up to accelerate down the runway; a little lift once fast enough
    if (pitchUp > 10 && hv < cfg.cruise + 0.05) {
      try { plane.applyImpulse({ x: fx * cfg.rollAccel, y: 0, z: fz * cfg.rollAccel }); } catch (e) { warnOnce(e); }
    }
    if (hv > cfg.takeoff && pitchUp > 8) impulseY(plane, 0.09 - vel.y);
    else if (alt <= 0.3 && vel.y < 0) plane.clearVelocity?.();     // settled on the grass
    return;
  }

  // ---- airborne
  // steer: swing the velocity toward the look direction (banking turn feel)
  const cruiseSp = Math.max(hv, cfg.cruise);
  const wantX = fx * cruiseSp, wantZ = fz * cruiseSp;
  let ix = (wantX - vel.x) * cfg.turn;
  let iz = (wantZ - vel.z) * cfg.turn;
  // auto-throttle: never stall out of the sky with no key held
  if (hv < cfg.cruise) {
    const add = Math.min(0.03, cfg.cruise - hv);
    ix += fx * add; iz += fz * add;
  }
  // vertical: pitch sets climb/dive, level = hold altitude; fast enough to fly, else glide down softly
  let vyDes;
  const flying = hv >= cfg.cruise * 0.7;
  if (flying) vyDes = clamp((pitchUp / 45) * cfg.climb, -cfg.sinkMax * 1.6, cfg.climb);
  else vyDes = -0.05;
  // flare near the ground: never touch down faster than a gentle sink
  if (alt < 3 && vyDes < -0.08) vyDes = -0.08;
  const iy = holdVy(plane, vyDes, vel);
  try { plane.applyImpulse({ x: ix, y: clamp(iy, -0.2, 0.25), z: iz }); } catch (e) { warnOnce(e); }
}

function tickPlaneEmpty(plane) {
  // parked / abandoned: settle to the ground slowly, no crash
  const alt = altitude(plane);
  const vel = plane.getVelocity();
  if (alt > 0.4) {
    const iy = holdVy(plane, -0.07, vel);
    try { plane.applyImpulse({ x: -vel.x * 0.08, y: clamp(iy, -0.2, 0.2), z: -vel.z * 0.08 }); } catch (e) { warnOnce(e); }
  } else holdVy(plane, 0, vel, false);
}

// ------------------------------------------------------------------ helicopter

function tickHeli(heli, pilot) {
  const cfg = CFG.heli;
  const vel = heli.getVelocity();
  const look = pilot.getViewDirection();
  const pitchUp = Math.asin(clamp(look.y, -1, 1)) * 180 / Math.PI;
  const alt = altitude(heli);

  let vyDes = 0;
  if (pitchUp > cfg.upStart) vyDes = clamp((pitchUp - cfg.upStart) / 40, 0, 1) * cfg.maxUp;
  else if (-pitchUp > cfg.downStart) vyDes = -clamp((-pitchUp - cfg.downStart) / 30, 0, 1) * cfg.maxDown;
  if (pilot.isJumping === true) vyDes = Math.max(vyDes, cfg.maxUp * 0.8);   // jump key climbs when the API exposes it
  if (alt < 2 && vyDes < -cfg.landSlow) vyDes = -cfg.landSlow;
  if (alt <= 0.15 && vyDes < 0) vyDes = 0;                                    // on the ground: stay put

  // Take full control of vertical speed (hold altitude when level), drag the sideways drift.
  const iy = holdVy(heli, vyDes, vel, alt > 0.15 || vyDes > 0);
  const ix = -vel.x * (1 - cfg.drag);
  const iz = -vel.z * (1 - cfg.drag);
  try { heli.applyImpulse({ x: ix, y: clamp(iy, -0.25, 0.3), z: iz }); } catch (e) { warnOnce(e); }
}

function tickHeliEmpty(heli) {
  const alt = altitude(heli);
  const vel = heli.getVelocity();
  if (alt > 0.3) {
    const iy = holdVy(heli, -0.1, vel);
    try { heli.applyImpulse({ x: -vel.x * 0.1, y: clamp(iy, -0.2, 0.2), z: -vel.z * 0.1 }); } catch (e) { warnOnce(e); }
  } else holdVy(heli, 0, vel, false);
}

// ------------------------------------------------------------------ main loop

let now = 0;
system.runInterval(() => {
  now++;
  let players;
  try { players = world.getAllPlayers(); } catch { return; }
  if (players.length === 0) return;
  const dims = new Set();
  for (const p of players) { try { dims.add(p.dimension); } catch { /* ignore */ } }

  for (const dim of dims) {
    let list;
    try { list = dim.getEntities({ families: ["gx_vehicle"] }); } catch (e) { warnOnce(e); continue; }
    for (const v of list) {
      try {
        const r = riders(v);
        const pilot = r.length > 0 ? r[0] : null;
        switch (v.typeId) {
          case "gx:car": if (pilot) tickCar(v, now); break;
          case "gx:plane": if (pilot) tickPlane(v, pilot, now); else tickPlaneEmpty(v); break;
          case "gx:helicopter": if (pilot) tickHeli(v, pilot); else tickHeliEmpty(v); break;
          default: break;
        }
      } catch (e) { warnOnce(e); }
    }
  }
  if (now % 200 === 0) {   // drop state for cars that no longer exist
    const live = new Set(), liveAll = new Set();
    for (const dim of dims) {
      try {
        for (const v of dim.getEntities({ families: ["gx_vehicle"] })) { liveAll.add(v.id); if (v.typeId === "gx:car") live.add(v.id); }
      } catch { /* ignore */ }
    }
    for (const id of carState.keys()) if (!live.has(id)) carState.delete(id);
    for (const id of holdState.keys()) if (!liveAll.has(id)) holdState.delete(id);
  }
}, 1);
