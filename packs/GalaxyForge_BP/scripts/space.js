// Space: the top of the overworld sky (y >= SPACE_Y).  Without a full Galaxy Space Suit there is no air
// (slow damage + a warning); with it the wearer is safe and gets moon gravity.  Runs once a second.

import { world, system } from "@minecraft/server";

const SPACE_Y = 240;
const SUIT = ["gx:space_helmet", "gx:space_chestplate", "gx:space_leggings", "gx:space_boots"];
const SLOTS = ["Head", "Chest", "Legs", "Feet"];
const warned = new Map();

function suited(player) {
  try {
    const eq = player.getComponent("minecraft:equippable");
    return SLOTS.every((slot, i) => eq.getEquipment(slot)?.typeId === SUIT[i]);
  } catch { return false; }
}

system.runInterval(() => {
  let players;
  try { players = world.getAllPlayers(); } catch { return; }
  for (const p of players) {
    try {
      if (p.dimension.id !== "minecraft:overworld" || p.location.y < SPACE_Y) { warned.delete(p.id); continue; }
      if (suited(p)) {
        p.addEffect("slow_falling", 60, { amplifier: 0, showParticles: false });
        p.addEffect("jump_boost", 60, { amplifier: 3, showParticles: false });
        p.addEffect("night_vision", 260, { amplifier: 0, showParticles: false });
        p.addEffect("resistance", 60, { amplifier: 1, showParticles: false });
        if (!warned.get(p.id)) { warned.set(p.id, true); p.onScreenDisplay.setActionBar("SPACE  |  suit sealed  |  low gravity"); }
      } else {
        p.applyDamage(2, { cause: "suffocation" });
        p.onScreenDisplay.setActionBar("NO AIR! Wear the full Galaxy Space Suit or descend");
      }
    } catch { /* ignore */ }
  }
}, 20);
