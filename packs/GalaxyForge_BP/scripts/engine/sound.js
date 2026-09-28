// Sound recipes: vanilla sounds layered with pitch/volume/delay, so every weapon has a
// distinct voice without shipping a single .ogg.
//
//   recipe entry = [soundId, volume, pitch, delayTicks]

import { system } from "@minecraft/server";

export function play(player, recipe) {
  if (!recipe) return;
  for (const [id, vol, pitch, delay] of recipe) {
    if (!delay) {
      try { player.playSound(id, { volume: vol, pitch }); } catch { /* ignore */ }
    } else {
      system.runTimeout(() => {
        try { player.playSound(id, { volume: vol, pitch }); } catch { /* ignore */ }
      }, delay);
    }
  }
}

export function playAt(dim, id, loc, vol = 1, pitch = 1) {
  try { dim.playSound(id, loc, { volume: vol, pitch }); } catch { /* ignore */ }
}
