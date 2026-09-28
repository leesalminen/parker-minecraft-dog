// Node unit tests for the Galaxy Forge engine's pure logic: ray-march, heat model,
// cooldowns, chain targeting, safety filter and the griefing gate.
//
//   node --experimental-loader ./tools/weapons/tests/loader.mjs tools/weapons/tests/engine.test.mjs

import test from "node:test";
import assert from "node:assert/strict";

import { gameRules } from "./mock_server.mjs";
import { mob, makeDim, def, ctxFor } from "./mock_server.mjs";

import * as heat from "../../../packs/GalaxyForge_BP/scripts/engine/heat.js";
import * as ray from "../../../packs/GalaxyForge_BP/scripts/engine/ray.js";
import * as safety from "../../../packs/GalaxyForge_BP/scripts/engine/safety.js";
import { applyEffects } from "../../../packs/GalaxyForge_BP/scripts/engine/damage.js";
import { projectiles, fields, beginTick } from "../../../packs/GalaxyForge_BP/scripts/engine/state.js";
import * as bolt from "../../../packs/GalaxyForge_BP/scripts/archetypes/bolt.js";
import * as hitscan from "../../../packs/GalaxyForge_BP/scripts/archetypes/hitscan.js";
import * as chain from "../../../packs/GalaxyForge_BP/scripts/archetypes/chain.js";
import * as field from "../../../packs/GalaxyForge_BP/scripts/archetypes/field.js";

function reset() {
  projectiles.length = 0;
  fields.length = 0;
  beginTick();
}

// ---------------------------------------------------------------- heat model
test("heat model: add clamps, cool drains per second, vent zone is 45-70%", () => {
  const w = def({ heat: { max: 100, per_shot: 10, cool: 20, vent: true } });
  const st = { heat: 0 };
  heat.add(st, w, 10);
  assert.equal(st.heat, 10);
  heat.add(st, w, 500);
  assert.equal(st.heat, 100, "heat clamps at max");
  assert.equal(heat.isHot(st, w), true);
  heat.cool(st, w, 20);
  assert.equal(st.heat, 80, "one second of cooling removes cool units");
  st.heat = 50;
  assert.equal(heat.inVentZone(st, w), true);
  st.heat = 80;
  assert.equal(heat.inVentZone(st, w), false);
  heat.clear(st);
  assert.equal(st.heat, 0);
  assert.equal(heat.isHot(st, w), false);
});

test("heat model: weapons without heat never accumulate", () => {
  const w = def({ heat: null });
  const st = { heat: 0 };
  heat.add(st, w, 50);
  assert.equal(st.heat, 0);
});

// ---------------------------------------------------------------- vector helpers
test("ray helpers: normalise and measure", () => {
  const n = ray.norm({ x: 3, y: 4, z: 0 });
  assert.ok(Math.abs(n.x - 0.6) < 1e-9 && Math.abs(n.y - 0.8) < 1e-9);
  assert.equal(Math.round(ray.len({ x: 3, y: 4, z: 0 })), 5);
  assert.equal(ray.dist({ x: 0, y: 0, z: 0 }, { x: 0, y: 0, z: 5 }), 5);
  const p = ray.add({ x: 1, y: 1, z: 1 }, { x: 0, y: 0, z: 1 }, 10);
  assert.deepEqual(p, { x: 1, y: 1, z: 11 });
});

test("raycast clamps the impact point to the block hit distance", () => {
  reset();
  const dim = makeDim({ rayBlock: { typeId: "minecraft:stone" }, rayPoint: { x: 0, y: 0, z: 5 } });
  const r = ray.raycast(dim, { x: 0, y: 0, z: 0 }, { x: 0, y: 0, z: 1 }, 20);
  assert.equal(Math.round(r.dist), 5);
  assert.equal(Math.round(r.point.z), 5);
  assert.equal(r.block.typeId, "minecraft:stone");
});

// ---------------------------------------------------------------- safety filter
test("safety filter: pup, tamed mobs and players are protected", () => {
  const pup = mob("p1", { typeId: "galaxy:pup" });
  const tamed = mob("t1", { tamed: true });
  const player = mob("pl1", { typeId: "minecraft:player" });
  const zombie = mob("z1", {});

  assert.equal(safety.isProtected(pup, null, {}), true);
  assert.equal(safety.isProtected(tamed, null, {}), true);
  assert.equal(safety.isProtected(player, null, {}), true, "players protected unless pvp");
  assert.equal(safety.isProtected(player, null, { pvp: true }), false);
  assert.equal(safety.isProtected(zombie, null, {}), false);
  assert.equal(safety.familiesOf(zombie)[0], "monster");
});

test("hurt() refuses to damage a pup even when a weapon targets it", () => {
  const pup = mob("p1", { typeId: "galaxy:pup" });
  const dim = makeDim();
  const ctx = ctxFor(dim, def(), {});
  applyEffects(ctx, [{ dmg: 20 }], pup);
  assert.equal(pup.damageTaken, 0);
});

// ---------------------------------------------------------------- griefing gate
test("grief effects do nothing while mobGriefing is false", () => {
  reset();
  gameRules.mobGriefing = false;
  const dim = makeDim();
  const ctx = ctxFor(dim, def(), {});
  const changed = applyEffects(ctx, [{ grief: { radius: 2, to: "minecraft:air", cap: 10 } }], null);
  assert.equal(changed, undefined, "no block writes attempted");
});

// ---------------------------------------------------------------- bolt ray-march
test("bolt: fires, advances by velocity/20 per tick, spawns body particles", () => {
  reset();
  const dim = makeDim();
  const w = def({ params: { speed: 40, lifetime: 40, rate: 4, damage: 5, count: 1, size: 0.3 } });
  const ctx = ctxFor(dim, w, {});
  const fired = bolt.fire(ctx, { force: true });
  assert.equal(fired, true);
  assert.equal(projectiles.length, 1);
  const before = { ...projectiles[0].loc };
  bolt.tickBolts();
  const after = projectiles[0].loc;
  assert.ok(Math.abs(after.z - before.z - 2) < 1e-6, "moves speed/20 = 2 blocks per tick");
  assert.ok(dim.particles.length >= 1, "body particle spawned");
});

test("bolt: expires after its lifetime", () => {
  reset();
  const dim = makeDim();
  const w = def({ params: { speed: 40, lifetime: 2, rate: 4, damage: 5, count: 1, size: 0.3 } });
  bolt.fire(ctxFor(dim, w, {}), { force: true });
  bolt.tickBolts();
  bolt.tickBolts();
  bolt.tickBolts();
  assert.equal(projectiles.length, 0, "bolt removed once life runs out");
});

test("bolt: a hit damages the target and consumes the bolt", () => {
  reset();
  const target = mob("z1", { x: 0, y: 0, z: 5 });
  const dim = makeDim({ rayEntities: [target] });
  const w = def({ params: { speed: 40, lifetime: 40, rate: 4, damage: 7, count: 1, size: 0.3 } });
  bolt.fire(ctxFor(dim, w, {}), { force: true });
  bolt.tickBolts();
  assert.equal(target.damageTaken, 7);
  assert.equal(projectiles.length, 0);
});

test("bolt: AoE detonation hits every unprotected mob in radius", () => {
  reset();
  const a = mob("a", { x: 0, y: 0, z: 1 });
  const b = mob("b", { x: 1, y: 0, z: 1 });
  const dim = makeDim({ rayEntities: [a], entities: [a, b] });
  const w = def({ params: { speed: 40, lifetime: 40, rate: 4, damage: 6, count: 1,
                            size: 0.4, aoe: 4, aoe_mult: 1 } });
  bolt.fire(ctxFor(dim, w, {}), { force: true });
  bolt.tickBolts();
  assert.ok(a.damageTaken >= 6);
  assert.ok(b.damageTaken >= 6, "splash reaches the second mob");
});

// ---------------------------------------------------------------- cooldowns
test("hitscan: rate limiting blocks a second shot inside the cooldown window", () => {
  reset();
  const dim = makeDim({ rayEntities: [mob("z", { x: 0, y: 0, z: 3 })] });
  const w = def({ archetype: "hitscan", params: { range: 40, damage: 6, rate: 10 } });
  const st = {};
  const ctx = ctxFor(dim, w, st);
  assert.equal(hitscan.shot(ctx), true);
  assert.equal(hitscan.shot(ctx), false, "second shot blocked by rate");
  ctx.tick += 10;
  assert.equal(hitscan.shot(ctx), true, "allowed once the rate window elapses");
});

test("hitscan: headshot bonus multiplies damage", () => {
  reset();
  const z = mob("z", { x: 0, y: 0, z: 1 });
  const dim = makeDim({ rayEntities: [z] });
  const w = def({ archetype: "hitscan", params: { range: 40, damage: 5, rate: 1, headshot_mult: 1.8 } });
  hitscan.shot(ctxFor(dim, w, {}));
  assert.equal(z.damageTaken, 9, "5 * 1.8");
});

// ---------------------------------------------------------------- chain targeting
test("chain: jumps between nearby mobs with falloff", () => {
  reset();
  const first = mob("a", { x: 0, y: 0, z: 3 });
  const second = mob("b", { x: 2, y: 0, z: 3 });
  const dim = makeDim({ rayEntities: [first], entities: [second] });
  const w = def({ archetype: "chain",
                 params: { range: 20, damage: 8, jumps: 3, radius: 6, falloff: 0.5 } });
  const ok = chain.arc(ctxFor(dim, w, {}));
  assert.equal(ok, true);
  assert.equal(first.damageTaken, 8);
  assert.equal(second.damageTaken, 4, "second jump falls off by 50%");
});

test("chain: never jumps into a protected mob", () => {
  reset();
  const first = mob("a", { x: 0, y: 0, z: 3 });
  const pup = mob("p", { x: 2, y: 0, z: 3, typeId: "galaxy:pup" });
  const dim = makeDim({ rayEntities: [first], entities: [pup] });
  const w = def({ archetype: "chain", params: { range: 20, damage: 8, jumps: 3, radius: 6, falloff: 1 } });
  chain.arc(ctxFor(dim, w, {}));
  assert.equal(pup.damageTaken, 0);
});

// ---------------------------------------------------------------- fields
test("field zones apply status and expire", () => {
  reset();
  const dim = makeDim({ entities: [mob("z", { x: 0, y: 0, z: 0 })] });
  const ctx = ctxFor(dim, def(), {});
  applyEffects(ctx, [{ field: "stasis", radius: 3, life: 60,
                       extra: { status: [{ id: "slowness", ticks: 40, amp: 255 }] } }], null);
  assert.equal(fields.length, 1);
  const z = dim.entities[0];
  for (let i = 0; i < 20; i++) { beginTick(); field.tickFields(); }
  assert.equal(z.effects.length, 1, "status pulses once per second");
  assert.equal(z.effects[0].id, "slowness");
  for (let i = 0; i < 41; i++) { beginTick(); field.tickFields(); }
  assert.equal(fields.length, 0, "zone removed once its life runs out");
});
