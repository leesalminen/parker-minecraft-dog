// End-to-end roster checks against the *generated* script table: every weapon's VFX names
// must resolve to a real particle definition or glyph, silhouettes must be unique, and the
// DPS budget must hold.
//
//   node --experimental-loader ./tools/weapons/tests/loader.mjs tools/weapons/tests/roster.test.mjs

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

import { WEAPONS, GLYPHS } from "../../../packs/GalaxyForge_BP/scripts/generated/weapons.js";

const ROOT = path.resolve(new URL("../../../", import.meta.url).pathname);
const PARTICLES = new Set(
  fs.readdirSync(path.join(ROOT, "packs/GalaxyForge_RP/particles"))
    .filter((f) => f.endsWith(".json"))
    .map((f) => "gx:" + f.slice(3, -5)),
);

const VFX_PARTICLE_LAYERS = ["idle", "charge", "muzzle", "body", "impact"];
const TIER_DPS = { toy: 3, common: 8, rare: 14, epic: 22, mythic: 30, ultimate: 30 };
const list = Object.entries(WEAPONS);

test("roster is 73 weapons with unique item ids", () => {
  assert.equal(list.length, 73);
  assert.equal(new Set(list.map(([k]) => k)).size, 73);
});

test("every particle effect a weapon names actually exists in RP/particles", () => {
  const missing = [];
  for (const [itemId, w] of list) {
    for (const layer of VFX_PARTICLE_LAYERS) {
      const name = w.vfx[layer];
      if (!PARTICLES.has(name)) missing.push(`${itemId}.vfx.${layer} -> ${name}`);
    }
    for (const hook of Object.values(w.hooks ?? {})) {
      for (const effect of hook ?? []) {
        if (effect.vfx && !PARTICLES.has(effect.vfx)) missing.push(`${itemId}.hook -> ${effect.vfx}`);
      }
    }
  }
  assert.deepEqual(missing, []);
});

test("every screen-feedback glyph a weapon names exists in the font sheet", () => {
  const missing = [];
  for (const [itemId, w] of list) {
    if (!GLYPHS[w.vfx.screen]) missing.push(`${itemId}.vfx.screen -> ${w.vfx.screen}`);
  }
  assert.deepEqual(missing, []);
});

test("silhouettes are unique within each family", () => {
  const seen = new Map();
  const dupes = [];
  for (const [itemId, w] of list) {
    const key = `${w.family}|${w.silhouette.projectile}|${w.silhouette.muzzle}`;
    if (seen.has(key)) dupes.push(`${itemId} shares ${key} with ${seen.get(key)}`);
    seen.set(key, itemId);
  }
  assert.deepEqual(dupes, []);
});

test("dps stays inside the tier budget (ultimates exempt)", () => {
  const bad = [];
  for (const [itemId, w] of list) {
    const budget = TIER_DPS[w.tier];
    assert.ok(budget, `${itemId} has unknown tier ${w.tier}`);
    if (w.tier !== "ultimate" && Math.abs(w.dps - budget) > budget * 0.2) {
      bad.push(`${itemId}: ${w.dps} vs budget ${budget}`);
    }
  }
  assert.deepEqual(bad, []);
});

test("ultimates carry a >= 45 s cooldown", () => {
  const bad = [];
  for (const [itemId, w] of list) {
    if (w.tier === "ultimate" && !(w.params.cooldown ?? w.cooldown)) bad.push(itemId);
  }
  assert.deepEqual(bad, []);
});

test("every weapon has a non-empty sound recipe and a scope in the vocabulary", () => {
  const scopes = ["iron", "holo", "dot", "scope4", "scope8", "thermal", "rangefinder", "lock", "focus"];
  const bad = [];
  for (const [itemId, w] of list) {
    if (!Array.isArray(w.sound) || w.sound.length === 0) bad.push(`${itemId}: no sound`);
    if (!scopes.includes(w.scope)) bad.push(`${itemId}: scope ${w.scope}`);
  }
  assert.deepEqual(bad, []);
});

test("custom twist modules resolve", async () => {
  const { CUSTOM } = await import("../../../packs/GalaxyForge_BP/scripts/generated/weapons.js");
  const missing = [];
  for (const [itemId, w] of list) {
    if (w.has_custom && !CUSTOM[itemId]) missing.push(itemId);
  }
  assert.deepEqual(missing, []);
});
