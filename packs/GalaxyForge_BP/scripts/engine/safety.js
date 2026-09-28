// The griefing / targeting safety layer. Weapons never hurt galaxy:pup, any tamed mob,
// or a player unless pvp is on; block-changing effects run only when mobGriefing is true.

import { world } from "@minecraft/server";

export const PUP = "galaxy:pup";

export function familiesOf(entity) {
  try {
    const c = entity.getComponent("minecraft:type_family");
    return c ? c.getFamily() : [];
  } catch { return []; }
}

export function isTamed(entity) {
  try {
    const c = entity.getComponent("minecraft:is_tamed");
    return !!(c && c.isTamed);
  } catch { return false; }
}

export function isPlayer(entity) {
  return entity?.typeId === "minecraft:player";
}

/** mobGriefing gate for every block-changing effect. */
export function mobGriefing() {
  try { return world.gameRules.mobGriefing === true; } catch { return false; }
}

/** True when this entity must never be damaged by a weapon. */
export function isProtected(entity, player, opts = {}) {
  if (!entity) return true;
  if (entity.typeId === PUP) return true;
  if (isTamed(entity)) return true;
  if (isPlayer(entity)) return !(opts.pvp ?? false);
  return false;
}

/** Player's own id, so a weapon never shoots its wielder. */
export function isSelf(entity, player) {
  return !!player && entity?.id === player.id;
}
