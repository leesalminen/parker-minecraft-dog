// Heat model shared by every heat-limited weapon.
//
// def.heat = { max, per_shot, cool, vent }   cool is units per second.
// `vent` (optional) marks weapons with the perfect-vent twist: once overheated, a
// 2-second window opens and releasing inside the green zone clears heat instantly.

export function add(st, def, n) {
  if (!def.heat) return;
  st.heat = Math.min(def.heat.max, (st.heat || 0) + n);
}

export function cool(st, def, ticks) {
  if (!def.heat) { st.heat = 0; return; }
  const perTick = (def.heat.cool || 0) / 20;
  st.heat = Math.max(0, (st.heat || 0) - perTick * ticks);
}

export function isHot(st, def) {
  return !!def.heat && (st.heat || 0) >= def.heat.max - 0.001;
}

export function fraction(st, def) {
  if (!def.heat) return 0;
  return Math.max(0, Math.min(1, (st.heat || 0) / def.heat.max));
}

/** Green zone of the vent window: 45%-70% of max heat. */
export function inVentZone(st, def) {
  const f = fraction(st, def);
  return f >= 0.45 && f <= 0.7;
}

export function overheatLock(st) { st.overheat = true; }

export function clear(st) { st.heat = 0; st.overheat = false; }
