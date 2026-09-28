// Scope overlay + "zoom".
//
// Real zoom: `/camera @s fov_set` narrows the field of view while aiming (sneaking) and
// `fov_clear` restores it.  `player.camera.setFov` is beta-only (it would force the Beta APIs
// experiment), so the command is issued once per aim edge through engine/cmd.js.  The engine
// clamps a custom FOV to [30, 110] degrees, so zoom tops out near 2.6x against a 70-degree
// view; the glyph scope overlay and reticle sit on top.  Weapons just say `zoom: 4`.

import { GLYPHS as G } from "../generated/weapons.js";
import { rep } from "./hud.js";
import { dotPoint, dist } from "./ray.js";
import { run } from "./cmd.js";

const WIDTH = 9;

function grid(kind, zoom) {
  const center = kind === "scope8" ? G.scope_mildot
    : kind === "scope4" ? G.scope_ring_med
    : kind === "holo" ? G.crosshair_ring
    : kind === "thermal" ? G.crosshair_brackets
    : kind === "lock" ? G.scope_lock
    : kind === "focus" ? G.scope_ring_small
    : G.crosshair_cross;
  const top = G.scope_corner_tl + rep(G.scope_edge_top, WIDTH - 2) + G.scope_corner_tr;
  const mid = G.scope_edge_left + rep(G.spacer, 3) + center + rep(G.spacer, 3) + G.scope_edge_right;
  const bot = G.scope_corner_bl + rep(G.scope_edge_bottom, WIDTH - 2) + G.scope_corner_br;
  const tint = kind === "thermal" ? rep(G.thermal_tint, 3) : "";
  return tint + top + "\n" + mid + "\n" + bot;
}

/** Scope string for a weapon + zoom level. Empty for iron sights. */
export function overlayText(def, st) {
  if (!def || def.scope === "iron") return "";
  return grid(def.scope, def.zoom);
}

const BASE_FOV = 70;
const MIN_FOV = 30;

export function fovFor(zoom) {
  const half = Math.atan(Math.tan(BASE_FOV * Math.PI / 360) / zoom);
  return Math.max(MIN_FOV, Math.min(110, half * 360 / Math.PI));
}

function zoomTo(player, st, zoom) {
  if (zoom === (st.fovZoom ?? 1)) return;
  st.fovZoom = zoom;
  if (zoom > 1) run(player, `camera @s fov_set ${fovFor(zoom).toFixed(1)} 0.15 linear`);
  else run(player, "camera @s fov_clear");
}

export function apply(player, st, def, aiming) {
  zoomTo(player, st, aiming && def && (def.zoom ?? 1) > 1 ? def.zoom : 1);
  const want = aiming ? overlayText(def, st) : "";
  if (want === st.scopeCache) return;
  st.scopeCache = want;
  try {
    player.onScreenDisplay.setTitle(want, { fadeInDuration: 0, stayDuration: 600, fadeOutDuration: 0 });
  } catch { /* ignore */ }
}

/** Rangefinder readout for scopes that spec one (distance to the aim point). */
export function rangefinder(player, st, def) {
  if (def.scope !== "rangefinder" && def.scope !== "scope8" && def.scope !== "scope4") return;
  const p = dotPoint(player.dimension, player.getHeadLocation(), player.getViewDirection(),
                     def.dot?.range ?? 64);
  const d = Math.round(dist(player.location, p));
  try { player.onScreenDisplay.updateSubtitle(`${G.scope_rangefinder} ${d}m`); } catch { /* ignore */ }
}

/** The laser dot: 1 particle per weapon per tick (every other tick is plenty). */
export function laserDot(player, st, def) {
  const style = def.dot?.style ?? "dot";
  const effect = `gx:dot_${style}`;
  const p = dotPoint(player.dimension, player.getHeadLocation(), player.getViewDirection(),
                     def.dot?.range ?? 64);
  return { effect, point: p };
}
