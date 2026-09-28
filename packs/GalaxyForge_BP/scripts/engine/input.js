// Fire / aim input model.
//
//   fire    : right-click; holding it keeps firing (see the trigger paths below)
//   aim     : sneak (query.is_sneaking) toggles the scope, in first *and* third person
//   alt-fire: press while already sneaking
//   ammo    : unlimited (main.js keeps every magazine full)

import { world } from "@minecraft/server";
import { getState, dropState, tick } from "./state.js";
import { defFor } from "../generated/weapons.js";

export function heldItem(player) {
  try {
    const inv = player.getComponent("minecraft:inventory");
    return inv?.container?.getItem(player.selectedSlotIndex) ?? undefined;
  } catch { return undefined; }
}

export function heldDef(player) {
  const it = heldItem(player);
  if (!it) return null;
  return defFor(it.typeId) ?? null;
}

// Two trigger paths, because which one a platform delivers is not guaranteed:
//  * itemStartUse / itemReleaseUse / itemStopUse: a true press-and-hold.  The weapon items
//    carry a never-finishing `minecraft:food` component purely so Bedrock treats them as
//    usable (`minecraft:use_modifiers` alone does not).
//  * itemUse / itemUseOn: fires on every right-click (in the air / on a block), and repeats
//    while the button is held; a gap of HOLD_GAP ticks counts as a release.
const HOLD_GAP = 7;

function trigger(player) {
  const d = heldDef(player);
  if (!d) return;
  const s = getState(player);
  s.lastUseTick = tick;
  if (s.using) return;
  s.def = d; s.itemId = `gx:${d.id}`;
  s.using = true; s.press = true; s.useStart = tick;
}

function endUse(player) {
  const s = getState(player);
  s.trueHold = false;
  if (!s.using) return;
  s.using = false; s.release = true;
}

/** Called once per tick per player: turns a gap in use repeats into a release. */
export function pollRelease(player, st) {
  if (st.using && !st.trueHold && tick - (st.lastUseTick ?? tick) > HOLD_GAP) {
    st.using = false; st.release = true;
  }
}

export function initInput() {
  world.afterEvents.itemStartUse.subscribe((e) => {
    trigger(e.source);
    getState(e.source).trueHold = true;
  });
  world.afterEvents.itemReleaseUse.subscribe((e) => endUse(e.source));
  world.afterEvents.itemStopUse.subscribe((e) => endUse(e.source));
  world.afterEvents.itemUse.subscribe((e) => trigger(e.source));
  world.afterEvents.itemUseOn?.subscribe((e) => trigger(e.source));
  world.afterEvents.playerLeave.subscribe((e) => dropState(e.playerId));
}
