// Command fallback for the few presentation features with no stable script API: camera FOV
// (zoom) and camera shake (recoil).  Never used for game logic, only on aim edges and shots.

export function run(entity, cmd) {
  try {
    if (typeof entity.runCommand === "function") { entity.runCommand(cmd); return true; }
    if (typeof entity.runCommandAsync === "function") {
      entity.runCommandAsync(cmd).catch(() => { /* command unavailable */ });
      return true;
    }
  } catch { /* command unavailable or rejected */ }
  return false;
}
