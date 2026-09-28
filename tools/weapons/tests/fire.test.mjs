// End-to-end trigger test: drives the real main.js tick loop against the mock world and
// checks that every weapon actually does something when the trigger is held, and that
// shot-type weapons keep firing (rapid fire) instead of stopping after one shot or at 0 ammo.
//
//   node --experimental-loader ./tools/weapons/tests/loader.mjs tools/weapons/tests/fire.test.mjs

import test from "node:test";
import assert from "node:assert/strict";

import { world, intervals, mob, makeDim, ItemStack, clock, gameRules } from "./mock_server.mjs";
import { WEAPONS } from "../../../packs/GalaxyForge_BP/scripts/generated/weapons.js";
import "../../../packs/GalaxyForge_BP/scripts/main.js";

function player(id, itemId, dim) {
  const p = mob(id, { typeId: "minecraft:player", families: ["player"] });
  p.dimension = dim;
  p.selectedSlotIndex = 0;
  p.isSneaking = false;
  p.sounds = 0;
  p.playSound = () => { p.sounds++; };
  p.commands = [];
  p.runCommand = (c) => { p.commands.push(c); return { successCount: 1 }; };
  p.onScreenDisplay = { setTitle() {}, setActionBar() {}, updateSubtitle() {} };
  const slots = [new ItemStack(itemId)];
  const base = p.getComponent;
  p.getComponent = (name) => name === "minecraft:inventory"
    ? { container: { size: 1, getItem: (i) => slots[i], setItem: (i, v) => { slots[i] = v; } } }
    : base(name);
  return p;
}

function run(ticks, each) {
  for (let i = 0; i < ticks; i++) { each?.(i); for (const cb of intervals) cb(); clock.tick++; }
}

/** Press-and-hold `itemId` at a mob 5 blocks ahead for `hold` ticks, then release. */
function holdAt(itemId, hold, { iframes = true, sneak = false, after = 20 } = {}) {
  const target = mob(`t_${itemId}_${clock.tick}`, { z: 5, hp: 100000, iframes });
  target.hits = 0;
  const apply = target.applyDamage;
  target.applyDamage = (n, o) => { target.hits++; return apply(n, o); };
  const dim = makeDim({ rayEntities: [target], entities: [target], geometricRays: true });
  const p = player(`p_${itemId}_${clock.tick}`, itemId, dim);
  p.isSneaking = sneak;
  world.players = [p];
  world.afterEvents.itemStartUse.emit({ source: p });
  run(hold);
  world.afterEvents.itemStopUse.emit({ source: p });
  run(after);
  return { target, p, dim };
}

test("main.js registered exactly one tick loop", () => {
  assert.equal(intervals.length, 1);
});

for (const [itemId, w] of Object.entries(WEAPONS)) {
  if (w.archetype === "field") continue;  // fields are placed by hooks, never fired directly
  test(`${itemId} (${w.archetype}) fires while the trigger is held`, () => {
    if (process.env.GX_TRACE) console.error("start", itemId);
    const target = mob(`t_${w.id}`, { z: 5, hp: 100000 });
    const dim = makeDim({ rayEntities: [target], entities: [target], geometricRays: true });
    let spawned = 0;
    const spawn = dim.spawnEntity.bind(dim);
    dim.spawnEntity = (...a) => { spawned++; return spawn(...a); };
    const p = player(`p_${w.id}`, itemId, dim);
    world.players = [p];

    // Hold for 6 s (right-click repeats every 4 ticks; long enough for the 5 s ultimate
    // charge), then let go for 8 s so slow projectiles such as the black hole arrive.
    run(120, (i) => {
      if (i % 4 === 0) world.afterEvents.itemUse.emit({ source: p, itemStack: new ItemStack(itemId) });
    });
    run(160);
    const acted = target.damageTaken > 0 || spawned > 0;
    assert.ok(acted, `${itemId} did nothing (no damage, no spawn)`);
  });
}

test("shot-type weapons keep firing while held (rapid fire, unlimited ammo)", () => {
  // Pistol-style single-shot weapon: at RAPID_RATE 4 over a 60-tick hold it must land far
  // more than one magazine's worth of hits.
  const w = WEAPONS["gx:foam_popper"];
  const target = mob("t_rapid", { z: 5, hp: 100000 });
  const dim = makeDim({ rayEntities: [target], entities: [target], geometricRays: true });
  const p = player("p_rapid", "gx:foam_popper", dim);
  world.players = [p];
  run(60, (i) => { if (i % 4 === 0) world.afterEvents.itemUse.emit({ source: p }); });
  run(20);
  const shots = target.damageTaken / w.params.damage;
  assert.ok(shots > w.ammo.mag, `only ${shots} shots landed (mag ${w.ammo.mag})`);
});

test("true press-and-hold (itemStartUse -> itemStopUse) keeps firing, then stops", () => {
  const w = WEAPONS["gx:foam_popper"];
  const target = mob("t_hold", { z: 5, hp: 100000 });
  const dim = makeDim({ rayEntities: [target], entities: [target], geometricRays: true });
  const p = player("p_hold", "gx:foam_popper", dim);
  world.players = [p];
  world.afterEvents.itemStartUse.emit({ source: p });   // one event, no right-click repeats
  run(60);
  world.afterEvents.itemStopUse.emit({ source: p });
  run(40);
  const held = target.damageTaken;
  assert.ok(held / w.params.damage > w.ammo.mag, `only ${held / w.params.damage} shots while held`);
  run(40);
  assert.equal(target.damageTaken, held, "kept firing after the trigger was released");
});

// ---------------------------------------------------------------- realistic weapons

test("rapid fire lands through Bedrock's 10-tick hurt cooldown (i-frames)", () => {
  // M249: 3 dmg every 2 ticks.  Vanilla-style applyDamage alone would land one hit per 10
  // ticks (~18 over 60 ticks); the i-frame-aware hurt() must land (nearly) all of them.
  const w = WEAPONS["gx:m249_saw"];
  const { target } = holdAt("gx:m249_saw", 60);
  const shots = target.damageTaken / w.params.damage;
  assert.ok(shots >= 25, `only ${shots} rounds of damage landed in 60 ticks`);
});

test("minigun spins up before the first round, then fires every tick", () => {
  const w = WEAPONS["gx:m134_minigun"];
  const early = holdAt("gx:m134_minigun", w.params.spinup - 2, { after: 0 });
  assert.equal(early.target.damageTaken, 0, "fired before spin-up finished");
  const full = holdAt("gx:m134_minigun", w.params.spinup + 40);
  assert.ok(full.target.damageTaken / w.params.damage >= 30, `only ${full.target.damageTaken / w.params.damage} rounds`);
});

test("M16A4 fires a three-round burst per pull", () => {
  const w = WEAPONS["gx:m16a4"];
  const { target } = holdAt("gx:m16a4", 1, { after: 10 });
  assert.equal(target.damageTaken, w.params.damage * 3);
});

test("shotgun pellets are summed into one hit per target", () => {
  // Some pellets of the spread miss at 5 blocks; the ones that connect arrive as one hit.
  const w = WEAPONS["gx:remington_870"];
  const { target } = holdAt("gx:remington_870", 1, { after: 10 });
  assert.equal(target.hits, 1);
  assert.ok(target.damageTaken >= w.params.damage * 4, `only ${target.damageTaken} damage`);
});

test("bolt-action keeps its own cadence instead of the rapid-fire clamp", () => {
  const w = WEAPONS["gx:m24_sws"];
  assert.equal(w.params.rate, 30);
  const { target } = holdAt("gx:m24_sws", 61);
  assert.equal(target.hits, 3);   // ticks 0, 30, 60
});

test("scoped weapons zoom with the camera FOV while sneaking and reset after", () => {
  const { p } = holdAt("gx:m24_sws", 5, { sneak: true, after: 1 });
  assert.ok(p.commands.some((c) => /^camera @s fov_set 30\.0 /.test(c)), p.commands.join(" | "));
  p.isSneaking = false;
  run(2);
  assert.ok(p.commands.includes("camera @s fov_clear"), p.commands.join(" | "));
  assert.ok(p.commands.some((c) => c.startsWith("camerashake add @s ")), "no recoil shake");
});

test("launchers leave a crater only when mobGriefing is on", () => {
  const blast = (griefing) => {
    gameRules.mobGriefing = griefing;
    const removed = [];
    const target = mob(`t_blast_${griefing}`, { z: 6, hp: 100000 });
    const dim = makeDim({ rayEntities: [target], entities: [target], geometricRays: true });
    dim.getBlock = (l) => ({ typeId: l.y < -2 ? "minecraft:bedrock" : "minecraft:dirt",
                             setType(t) { removed.push([l, t]); } });
    const p = player(`p_blast_${griefing}`, "gx:m20_bazooka", dim);
    world.players = [p];
    world.afterEvents.itemStartUse.emit({ source: p });
    run(1);
    world.afterEvents.itemStopUse.emit({ source: p });
    run(30);
    gameRules.mobGriefing = false;
    return { removed, target };
  };
  const off = blast(false);
  assert.ok(off.target.damageTaken > 0, "rocket did no damage");
  assert.equal(off.removed.length, 0);
  const on = blast(true);
  assert.ok(on.removed.length > 5, `crater removed ${on.removed.length} blocks`);
  assert.ok(on.removed.every(([, t]) => t === "minecraft:air"));
});
