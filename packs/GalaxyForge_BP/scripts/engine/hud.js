// Glyph HUD: ammo pips, heat gauge, charge bar, fuel, cooldown, hit/kill markers.
// Drawn with player.onScreenDisplay using the private-use glyph sheet (font/glyph_E2.png),
// which is the only overlay technique that works on console.

import { GLYPHS as G } from "../generated/weapons.js";

export function rep(ch, n) { return n > 0 ? ch.repeat(n) : ""; }

export function pips(filled, total) {
  const f = Math.max(0, Math.min(total, Math.round(filled)));
  return rep(G.pip_full, f) + rep(G.pip_empty, Math.max(0, total - f));
}

export function heatBar(frac) {
  const n = 5;
  let s = "";
  for (let i = 0; i < n; i++) {
    const lit = (i + 1) / n <= frac + 0.0001;
    s += lit ? (i < 2 ? G.heat_cool : i < 4 ? G.heat_warm : G.heat_hot) : G.bar_empty;
  }
  return s;
}

export function chargeBar(t) { return G["charge" + Math.max(0, Math.min(4, Math.round(t * 4)))]; }

export function barRow(frac) {
  const n = 10;
  let s = "";
  for (let i = 0; i < n; i++) {
    const lit = (i + 1) / n <= frac + 0.0001;
    s += lit ? (frac > 0.7 ? G.bar_low : frac > 0.4 ? G.bar_mid : G.bar_full) : G.bar_empty;
  }
  return s;
}

/** Per-tick action bar for the held weapon. Only re-issued when the string changes. */
export function actionBar(player, def, st) {
  let text = "";
  const kind = def.hud?.kind ?? "ammo";
  if (kind === "ammo") {
    text = "";  // ammo is unlimited (main.js), so there is nothing to count
  } else if (kind === "heat") {
    text = G.heat_warm + heatBar((st.heat || 0) / (def.heat?.max ?? 100));
  } else if (kind === "fuel") {
    text = G.fuel + barRow(st.fuel ?? 0);
  } else if (kind === "charge") {
    text = G.cell + chargeBar(Math.min(1, (st.charge || 0) / Math.max(1, def.params?.hold_ticks ?? 20)));
  } else if (kind === "charges") {
    const max = def.params?.charges ?? 3;
    text = rep(G.star, Math.max(0, st.charges ?? 0)) + rep(G.ring_small, Math.max(0, max - (st.charges ?? 0)));
  } else if (kind === "mode") {
    const spin = def.params?.spinup;
    text = spin && st.using && (st.spin ?? 0) < spin ? `§6SPIN ${Math.round(100 * (st.spin ?? 0) / spin)}%`
      : `§7${(def.fire_mode ?? "").toUpperCase()}`;
  } else if (kind === "none") {
    text = "";
  }
  if (st.reload > 0) text = G.cell + barRow(1 - st.reload / Math.max(1, def.reload_ticks ?? 40));
  if (st.vent > 0) {
    const f = (st.heat || 0) / (def.heat?.max ?? 100);
    text = heatBar(f) + (f >= 0.45 && f <= 0.7 ? G.marker_kill : G.slider_mark);
  }
  if (st.cooldown > 0) text = G.hourglass + barRow(1 - st.cooldown / Math.max(1, (def.cooldown ?? 1) * 20));
  if (text !== st.hudCache) {
    st.hudCache = text;
    try { player.onScreenDisplay.setActionBar(text); } catch { /* ignore */ }
  }
}

/** Transient glyph flash (hit marker, kill confirm, overheat vignette). */
export function flash(player, st, glyph, ticks = 6) {
  try { player.onScreenDisplay.updateSubtitle(glyph); } catch { /* ignore */ }
  st.scratch.markerUntil = (st.scratch.markerUntil || 0) + ticks;
}

export function clearMarker(player, st) {
  try { player.onScreenDisplay.updateSubtitle(""); } catch { /* ignore */ }
}

export function overlay(player, glyph, ticks = 20) {
  try { player.onScreenDisplay.setTitle(glyph, { fadeInDuration: 0, stayDuration: ticks, fadeOutDuration: 4 }); }
  catch { /* ignore */ }
}
