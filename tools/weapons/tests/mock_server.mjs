// Minimal @minecraft/server mock so the engine's pure logic can be unit-tested in Node.
// Only the surface the engine actually touches is implemented.

export const gameRules = { mobGriefing: false };

// Event signals keep their handlers so a test can fire them (see fire.test.mjs).
function signal() {
  const handlers = [];
  return { handlers, subscribe(fn) { handlers.push(fn); return fn; }, emit(e) { for (const h of handlers) h(e); } };
}

export const world = {
  gameRules,
  afterEvents: {
    itemStartUse: signal(),
    itemReleaseUse: signal(),
    itemStopUse: signal(),
    itemUse: signal(),
    itemUseOn: signal(),
    playerLeave: signal(),
    entityDie: signal(),
  },
  players: [],
  getPlayers() { return this.players; },
  getAllPlayers() { return this.players; },
  sendMessage() {},
};

export const intervals = [];

/** Test clock for i-frame emulation; fire.test.mjs advances it once per simulated tick. */
export const clock = { tick: 0 };

export const system = {
  runInterval: (cb) => { intervals.push(cb); return intervals.length; },
  runTimeout: (cb) => { cb(); return 1; },
  clearRun: () => {},
};

export class MolangVariableMap {
  setColorRGB() {}
  setColorRGBA() {}
  setFloat() {}
  setVector3() {}
  setSpeedAndDirection() {}
}

export class ItemStack {
  constructor(typeId, amount = 1) {
    this.typeId = typeId;
    this.amount = amount;
  }
  getDynamicProperty() { return undefined; }
  setDynamicProperty() {}
  clone() { return new ItemStack(this.typeId, this.amount); }
}

/** A fake entity with the component surface the engine reads. */
export function mob(id, opts = {}) {
  const health = {
    currentValue: opts.hp ?? 20,
    defaultValue: 20,
    effectiveMax: 20,
    // Direct health writes (the i-frame bypass in damage.js) count as damage taken.
    setCurrentValue(v) { if (v < this.currentValue) e.damageTaken += this.currentValue - v; this.currentValue = v; },
    resetToMaxValue() { this.currentValue = 20; },
  };
  const e = {
    id,
    typeId: opts.typeId ?? "minecraft:zombie",
    location: { x: opts.x ?? 0, y: opts.y ?? 0, z: opts.z ?? 0 },
    isValid: true,
    damageTaken: 0,
    effects: [],
    getComponent(name) {
      if (name === "minecraft:type_family") return { getFamily: () => opts.families ?? ["monster"] };
      if (name === "minecraft:is_tamed") return opts.tamed ? { isTamed: true } : undefined;
      if (name === "minecraft:health") return health;
      return undefined;
    },
    getHeadLocation() { return { x: e.location.x, y: e.location.y + 1.6, z: e.location.z }; },
    getViewDirection() { return { x: 0, y: 0, z: 1 }; },
    // opts.iframes emulates Bedrock's 10-tick hurt cooldown: a hit inside the window only
    // lands if it beats the previous one, and then only the difference.
    applyDamage(n) {
      let eff = n;
      if (opts.iframes) {
        if (clock.tick - e.hurtTick < 10) { eff = n > e.hurtAmount ? n - e.hurtAmount : 0; if (eff) e.hurtAmount = n; }
        else { e.hurtTick = clock.tick; e.hurtAmount = n; }
      }
      e.damageTaken += eff;
      health.currentValue -= eff;
      return eff > 0;
    },
    hurtTick: -99,
    hurtAmount: 0,
    addEffect(id, ticks, options) { e.effects.push({ id, ticks, amp: options?.amplifier ?? 0 }); return {}; },
    applyKnockback() {},
    applyImpulse() {},
    applyEffect() {},
    teleport(loc) { e.location = { ...loc }; },
    tryTeleport() { return true; },
    remove() { e.isValid = false; },
    setDynamicProperty(k, v) { e[k] = v; },
    getDynamicProperty(k) { return e[k]; },
    matches() { return true; },
  };
  return e;
}

/** A fake dimension that can be told what a ray hits. */
export function makeDim(opts = {}) {
  const particles = [];
  return {
    id: "minecraft:overworld",
    particles,
    rayBlock: opts.rayBlock ?? null,
    rayEntities: opts.rayEntities ?? [],
    entities: opts.entities ?? [],
    getBlockFromRay() {
      return this.rayBlock ? { block: this.rayBlock, faceLocation: opts.rayPoint ?? { x: 0, y: 0, z: 0 } } : undefined;
    },
    getEntitiesFromRay(origin, dir, o = {}) {
      if (!opts.geometricRays) return this.rayEntities.map((e, i) => ({ entity: e, distance: i + 1 }));
      // Real ray test: hit entities whose body centre lies within 1 block of the ray.
      const out = [];
      for (const e of this.rayEntities) {
        const c = { x: e.location.x - origin.x, y: e.location.y + 0.9 - origin.y, z: e.location.z - origin.z };
        const t = c.x * dir.x + c.y * dir.y + c.z * dir.z;
        const perp = Math.hypot(c.x - dir.x * t, c.y - dir.y * t, c.z - dir.z * t);
        if (t >= 0 && t <= (o.maxDistance ?? Infinity) && perp < 1) out.push({ entity: e, distance: t });
      }
      return out;
    },
    getEntities() { return this.entities; },
    getBlock() { return undefined; },
    spawnParticle(effect, loc, molang) { particles.push({ effect, loc, molang }); },
    playSound() {},
    spawnEntity(id, loc) {
      return mob("deployed", { typeId: id, x: loc.x, y: loc.y, z: loc.z, families: ["gx_ally"] });
    },
  };
}

/** A minimal weapon def good enough to exercise the archetypes. */
export function def(over = {}) {
  return {
    id: "test_weapon",
    name: "Test Weapon",
    archetype: "bolt",
    scope: "iron",
    dps: 8,
    palette: { name: "test", core: "#ffffff", glow: "#00ffff", trail: "#004466", accent: "#88ffff" },
    dot: { style: "dot", color: "#00ffff", range: 64 },
    ammo: { type: "cell", mag: 10 },
    heat: null,
    hud: { kind: "ammo" },
    vfx: { idle: "gx:orb_soft_orb", charge: "gx:swirl", muzzle: "gx:star_flash",
           body: "gx:orb_teardrop", impact: "gx:ring_wave", screen: "vignette_heat" },
    params: { speed: 40, lifetime: 40, rate: 4, damage: 5, count: 1, size: 0.3 },
    hooks: { on_hit: [], on_tick: [] },
    sound: [["random.bow", 0.5, 1.5, 0]],
    custom: null,
    ...over,
  };
}

export function ctxFor(dim, weapon, st = {}, playerId = "p1") {
  return {
    player: { id: playerId, location: { x: 0, y: 0, z: 0 }, dimension: dim },
    dim, def: weapon, st, tick: 100, eye: { x: 0, y: 1.6, z: 0 }, view: { x: 0, y: 0, z: 1 },
    pvp: false, point: null,
  };
}
