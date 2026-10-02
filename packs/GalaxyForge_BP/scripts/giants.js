// Giant armor.  A full set (all four pieces from the same set) makes the wearer physically bigger (the
// gx:size_* events in entities/player.json switch `minecraft:scale`), applies the set's buffs, and unlocks:
//   - sprint ram: running into mobs smashes them (damage + knockback + the set's perk)
//   - landing stomp: a shockwave when a heavy set lands from a jump or fall
//   - melee perk: frost slows, magma ignites, storm strikes lightning, ender launches
// Each set also has a matching weapon (GIANT_WEAPONS); hitting with it applies the set's perk (or bash / sunder /
// cleave / wither for sets without one), whether or not the full set is worn.
// Set data comes from scripts/generated/giants.js (tools/creatures/extras/giant_armor.py).  Players, villagers,
// tamed pets and anything with a rider are never hit.

import { world, system } from "@minecraft/server";
import { GIANTS, GIANT_PREFIX, GIANT_WEAPONS } from "./generated/giants.js";

const SLOTS = ["Head", "Chest", "Legs", "Feet"];
const PIECES = ["helmet", "chestplate", "leggings", "boots"];
const SKIP_FAMILIES = ["player", "villager", "inanimate"];
const SKIP_TYPES = ["minecraft:armor_stand", "minecraft:wandering_trader", "minecraft:npc"];
const RAM_COOLDOWN = 8;
const LIGHTNING_COOLDOWN = 30;

const states = new Map();   // player id -> { set, size, hit: Map(entity id -> tick), ground, vy, bolt }
let tick = 0;

function stateOf(p) {
  let st = states.get(p.id);
  if (!st) { st = { set: null, size: 1, hit: new Map(), ground: true, vy: 0, bolt: 0 }; states.set(p.id, st); }
  return st;
}

function wornSet(p) {
  try {
    const eq = p.getComponent("minecraft:equippable");
    let id = null;
    for (let i = 0; i < 4; i++) {
      const t = eq.getEquipment(SLOTS[i])?.typeId;
      if (!t || !t.startsWith(GIANT_PREFIX) || !t.endsWith("_" + PIECES[i])) return null;
      const s = t.slice(GIANT_PREFIX.length, t.length - PIECES[i].length - 1);
      if (id !== null && s !== id) return null;
      id = s;
    }
    return GIANTS[id] ? id : null;
  } catch { return null; }
}

function setSize(p, st, event, size) {
  if (st.size === size) return;
  try { p.triggerEvent(event); st.size = size; } catch { /* ignore */ }
}

// every 10 ticks: detect the worn set, resize, refresh buffs
function refresh(p) {
  const st = stateOf(p);
  const id = wornSet(p);
  if (id !== st.set) {
    const old = st.set && GIANTS[st.set];
    if (old) for (const fx of Object.keys(old.fx)) { try { p.removeEffect(fx); } catch { /* ignore */ } }
    st.set = id;
    const g = id && GIANTS[id];
    setSize(p, st, g ? g.event : "gx:size_reset", g ? g.scale : 1);
    if (g) { try { p.onScreenDisplay.setActionBar(`§6${g.name}§r  |  ${g.scale}x size  |  sprint into mobs to smash them`); } catch { /* ignore */ } }
  }
  const g = id && GIANTS[id];
  if (!g) return;
  for (const [fx, amp] of Object.entries(g.fx)) {
    try { p.addEffect(fx, 40, { amplifier: amp, showParticles: false }); } catch { /* ignore */ }
  }
}

function targets(p, center, radius) {
  let found;
  try {
    found = p.dimension.getEntities({ location: center, maxDistance: radius, excludeFamilies: SKIP_FAMILIES, excludeTypes: SKIP_TYPES });
  } catch { return []; }
  return found.filter((e) => {
    if (e.id === p.id) return false;
    try {
      if (!e.getComponent("minecraft:health")) return false;
      if (e.getComponent("minecraft:is_tamed")) return false;
      const riders = e.getComponent("minecraft:rideable")?.getRiders();
      return !(riders && riders.length);
    } catch { return false; }
  });
}

function knock(e, dx, dz, h, v) {
  try { e.applyKnockback(dx, dz, h, v); }
  catch { try { e.applyImpulse({ x: dx * h * 0.5, y: v * 0.5, z: dz * h * 0.5 }); } catch { /* ignore */ } }
}

function perk(p, st, g, e, name = g.perk) {
  try {
    if (name === "bash") knock(e, p.getViewDirection().x, p.getViewDirection().z, 2.2, 0.5);
    else if (name === "sunder") e.addEffect("weakness", 160, { amplifier: 1 });
    else if (name === "wither") e.addEffect("wither", 100, { amplifier: 1 });
    else if (name === "cleave") {
      for (const o of targets(p, e.location, 3)) {
        if (o.id !== e.id) o.applyDamage(6, { cause: "entityAttack", damagingEntity: p });
      }
    }
    else if (name === "frost") e.addEffect("slowness", 100, { amplifier: 3 });
    else if (name === "fire") e.setOnFire(6, true);
    else if (name === "launch") knock(e, 0, 0, 0, 1.6);
    else if (name === "lightning" && tick - st.bolt >= LIGHTNING_COOLDOWN) {
      st.bolt = tick;
      p.dimension.spawnEntity("minecraft:lightning_bolt", e.location);
    }
  } catch { /* ignore */ }
}

function ram(p, st, g) {
  const v = p.getVelocity();
  if (!p.isSprinting || Math.hypot(v.x, v.z) < 0.12) return;
  const view = p.getViewDirection();
  const len = Math.hypot(view.x, view.z) || 1;
  const fx = view.x / len, fz = view.z / len;
  const reach = 1.2 + g.scale * 0.6;
  const l = p.location;
  const center = { x: l.x + fx * reach * 0.6, y: l.y + g.scale * 0.8, z: l.z + fz * reach * 0.6 };
  for (const e of targets(p, center, reach * 0.9 + g.scale * 0.6)) {
    if (tick - (st.hit.get(e.id) ?? -99) < RAM_COOLDOWN) continue;
    st.hit.set(e.id, tick);
    try {
      e.applyDamage(g.ram, { cause: "entityAttack", damagingEntity: p });
      knock(e, fx, fz, 1.2 + g.scale * 0.5, 0.45 + g.scale * 0.1);
      perk(p, st, g, e);
      p.dimension.spawnParticle("minecraft:critical_hit_emitter", e.location);
    } catch { /* ignore */ }
  }
}

function stomp(p, st, g) {
  const radius = 3 + g.scale;
  const l = p.location;
  try { p.dimension.spawnParticle("minecraft:huge_explosion_emitter", l); } catch { /* ignore */ }
  try { p.dimension.playSound("random.explode", l, { volume: 0.6, pitch: 0.6 }); } catch { /* ignore */ }
  for (const e of targets(p, l, radius)) {
    const dx = e.location.x - l.x, dz = e.location.z - l.z;
    const d = Math.hypot(dx, dz) || 1;
    try {
      e.applyDamage(g.stomp, { cause: "entityAttack", damagingEntity: p });
      knock(e, dx / d, dz / d, 1.5, 0.7);
      perk(p, st, g, e);
    } catch { /* ignore */ }
  }
}

// every 2 ticks: ram + landing stomp for players wearing a set
function fast(p) {
  const st = stateOf(p);
  const g = st.set && GIANTS[st.set];
  const onGround = p.isOnGround;
  const vy = p.getVelocity().y;
  if (g) {
    ram(p, st, g);
    if (g.stomp > 0 && onGround && !st.ground && st.vy < -0.6) stomp(p, st, g);
  }
  st.ground = onGround;
  st.vy = vy;
  if (st.hit.size > 64) { for (const [id, t] of st.hit) if (tick - t > 40) st.hit.delete(id); }
}

system.runInterval(() => {
  tick += 2;
  let players;
  try { players = world.getAllPlayers(); } catch { return; }
  for (const p of players) {
    try { if (tick % 10 === 0) refresh(p); fast(p); } catch { /* ignore */ }
  }
}, 2);

world.afterEvents.entityHitEntity.subscribe((ev) => {
  try {
    const p = ev.damagingEntity;
    if (p?.typeId !== "minecraft:player") return;
    const st = states.get(p.id);
    const g = st?.set && GIANTS[st.set];
    if (g?.perk) perk(p, st, g, ev.hitEntity);
    const held = p.getComponent("minecraft:equippable")?.getEquipment("Mainhand")?.typeId;
    const w = held && GIANT_WEAPONS[held];
    if (w?.perk && !(g && g.perk === w.perk)) perk(p, st ?? stateOf(p), GIANTS[w.set], ev.hitEntity, w.perk);
  } catch { /* ignore */ }
});

world.afterEvents.playerLeave.subscribe((ev) => { states.delete(ev.playerId); });
