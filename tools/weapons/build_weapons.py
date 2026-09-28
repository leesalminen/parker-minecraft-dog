"""Emit every Galaxy Forge weapon asset: items, attachables, models, textures, icons,
recipes, particles, glyph font, deploy entities, lang, and scripts/generated/weapons.js.

Run from tools/creatures/build_all.py, which owns lib.LANG / lib.ITEM_TEX.
"""
import importlib
import json
import math
import pkgutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import lib
from lib import BP, RP, dump, lang, write_png, shade, mix, rgb, noise3, hash01
from extras.military_pack import Icon, write_item, write_icon, shapeless, shaped
import model
import hd_models
import particles
import glyphs
import sounds

NS = "gx"
SCRIPTS = BP / "scripts"
CUSTOM_DIR = SCRIPTS / "archetypes/custom"

ARCHETYPES = ["hitscan", "bolt", "beam", "charge", "cone", "lob", "chain", "deploy", "field", "tether"]
SCOPES = ["iron", "holo", "dot", "scope4", "scope8", "thermal", "rangefinder", "lock", "focus"]
TIER_DPS = {"toy": 3, "common": 8, "rare": 14, "epic": 22, "mythic": 30, "ultimate": 30}
ROSTER_SIZE = 73

# Rapid fire: shot-type archetypes re-fire while the trigger is held (main.js), no slower
# than every RAPID_RATE ticks; multi-projectile volleys and lobs every RAPID_VOLLEY ticks.
# Realistic weapons declare a fire_mode (semi / auto / burst / bolt / pump / single) and keep
# their own cadence: a bolt-action rifle still repeats while held, just at bolt speed.
REPEAT_ARCHETYPES = {"hitscan", "bolt", "chain", "lob"}
RAPID_RATE, RAPID_VOLLEY = 4, 8


def rapid_params(d):
    p = dict(d["params"])
    if d["archetype"] in REPEAT_ARCHETYPES and not d.get("fire_mode"):
        cap = RAPID_VOLLEY if (p.get("count", 1) > 1 or d["archetype"] == "lob") else RAPID_RATE
        p["rate"] = min(p.get("rate", cap), cap)
    return p
VFX_LAYERS = ["idle", "charge", "muzzle", "body", "impact", "screen"]
REQUIRED = ["id", "name", "family", "tier", "archetype", "scope", "palette", "shape",
            "dps", "ammo", "params", "hooks", "vfx", "sound", "model", "recipe", "twist"]


# ---------------------------------------------------------------- defs
def load_defs():
    defs = []
    import defs as pkg
    for m in sorted(pkgutil.iter_modules(pkg.__path__), key=lambda x: x.name):
        mod = importlib.import_module(f"defs.{m.name}")
        defs.extend(mod.WEAPONS)
    return defs


def validate(defs, partial=False):
    errs = []
    if len(defs) != ROSTER_SIZE and not partial:
        errs.append(f"expected {ROSTER_SIZE} weapons, found {len(defs)}")
    ids = [d["id"] for d in defs]
    if len(set(ids)) != len(ids):
        errs.append("duplicate weapon ids")
    seen_palette, seen_shape = {}, {}
    for d in defs:
        wid = d.get("id", "?")
        for k in REQUIRED:
            if k not in d:
                errs.append(f"{wid}: missing key {k}")
        if d.get("archetype") not in ARCHETYPES:
            errs.append(f"{wid}: bad archetype {d.get('archetype')}")
        if d.get("scope") not in SCOPES:
            errs.append(f"{wid}: bad scope {d.get('scope')}")
        budget = TIER_DPS.get(d.get("tier", ""), 0)
        if not budget:
            errs.append(f"{wid}: bad tier {d.get('tier')}")
        elif d["tier"] != "ultimate" and abs(d.get("dps", 0) - budget) > budget * 0.2:
            errs.append(f"{wid}: dps {d.get('dps')} outside {d['tier']} budget {budget}")
        for k in ("projectile", "muzzle"):
            if k not in d.get("shape", {}):
                errs.append(f"{wid}: shape.{k} missing")
        pkey = (d.get("palette", {}).get("name"), d["shape"]["projectile"], d["shape"]["muzzle"])
        if pkey in seen_palette:
            errs.append(f"{wid}: shares (palette, projectile, muzzle) with {seen_palette[pkey]}")
        seen_palette[pkey] = wid
        skey = (d["family"], d["shape"]["projectile"], d["shape"]["muzzle"])
        if skey in seen_shape:
            errs.append(f"{wid}: shares {skey} with {seen_shape[skey]}")
        seen_shape[skey] = wid
        for layer in VFX_LAYERS:
            if not d.get("vfx", {}).get(layer):
                errs.append(f"{wid}: vfx.{layer} missing")
        if not d.get("sound"):
            errs.append(f"{wid}: empty sound recipe")
        pal = d.get("palette", {})
        for k in ("core", "glow", "trail", "accent", "name"):
            if k not in pal:
                errs.append(f"{wid}: palette.{k} missing")
    if errs:
        raise SystemExit("weapon validation failed:\n  " + "\n  ".join(errs))
    return defs


# ---------------------------------------------------------------- icons
def _gun_icon(form):
    """16x16 silhouette per model form, coloured by the weapon palette."""
    def paint(path, pal):
        ic = Icon()
        body, glow_c, accent = pal["metal"], pal["core"], pal["accent"]
        dark = shade(body, 0.62)
        if form in ("rifle", "sniper", "lance"):
            ic.line(1, 8, 14, 8, 1, body)
            ic.rect(4, 6, 11, 9, body)
            ic.rect(12, 7, 15, 8, shade(body, 1.15))
            ic.rect(5, 10, 7, 14, dark)
            ic.rect(1, 6, 3, 9, dark)
            ic.rect(4, 5, 10, 5, glow_c)
            ic.rect(13, 6, 15, 7, glow_c)
        elif form == "pistol":
            ic.rect(4, 6, 12, 9, body)
            ic.rect(5, 10, 8, 14, dark)
            ic.rect(11, 7, 15, 8, shade(body, 1.15))
            ic.rect(4, 5, 10, 5, glow_c)
        elif form == "revolver":
            ic.rect(3, 6, 12, 9, body)
            ic.disc(6, 8, 3, accent)
            ic.rect(4, 10, 7, 14, dark)
            ic.rect(12, 7, 15, 8, shade(body, 1.15))
            ic.rect(5, 5, 10, 5, glow_c)
        elif form == "smg":
            ic.rect(3, 6, 12, 9, body)
            ic.rect(4, 10, 7, 13, dark)
            ic.line(2, 7, 12, 7, 0, glow_c)
            ic.line(2, 9, 12, 9, 0, glow_c)
            ic.rect(12, 6, 15, 8, shade(body, 1.1))
        elif form in ("cannon", "launcher", "mortar"):
            ic.rect(2, 5, 11, 10, body)
            ic.rect(11, 6, 15, 9, shade(body, 1.1))
            ic.rect(4, 11, 7, 14, dark)
            ic.rect(3, 4, 10, 4, glow_c)
            ic.rect(12, 7, 15, 8, glow_c)
        elif form == "staff":
            ic.line(7, 2, 7, 14, 1, body)
            ic.disc(7, 4, 3, glow_c)
            ic.rect(6, 11, 9, 14, dark)
        elif form == "gauntlet":
            ic.rect(3, 5, 12, 12, body)
            ic.disc(7, 8, 3, glow_c)
            ic.rect(2, 9, 4, 14, dark)
        elif form == "bow":
            ic.line(4, 2, 4, 14, 1, accent)
            ic.line(4, 2, 11, 8, 0, shade(body, 1.2))
            ic.line(4, 14, 11, 8, 0, shade(body, 1.2))
            ic.rect(9, 7, 14, 9, body)
            ic.rect(12, 7, 14, 8, glow_c)
        elif form == "disc":
            ic.rect(3, 6, 11, 9, body)
            ic.rect(4, 10, 7, 13, dark)
            ic.disc(11, 8, 4, glow_c)
        elif form == "sprayer":
            ic.rect(3, 6, 11, 10, body)
            ic.rect(2, 3, 6, 6, accent)
            ic.rect(11, 7, 15, 9, glow_c)
            ic.rect(4, 10, 7, 14, dark)
        elif form == "rack":
            ic.rect(3, 6, 12, 9, body)
            ic.rect(4, 10, 7, 13, dark)
            ic.rect(8, 4, 10, 7, shade(body, 1.15))
            ic.rect(11, 4, 13, 7, shade(body, 1.15))
            ic.rect(8, 3, 13, 3, glow_c)
        elif form == "kit":
            ic.rect(2, 6, 13, 11, body)
            ic.rect(2, 5, 13, 5, dark)
            ic.rect(6, 7, 9, 10, glow_c)
        else:
            ic.rect(2, 6, 13, 10, body)
            ic.rect(3, 10, 6, 14, dark)
            ic.rect(12, 7, 15, 9, glow_c)
        ic.save(path)
    return paint


def do_icons(defs):
    for d in defs:
        parts = model.hd_parts(d)
        if parts:
            write_icon(f"gx_{d['id']}", lambda path, parts=parts, m=d["model"]:
                       write_png(path, hd_models.render_icon(parts, m, 32), 32, 32))
            continue
        pal = {"metal": d["model"].get("metal", "#59616d"),
               "core": d["palette"]["core"], "accent": d["palette"]["accent"]}
        key = f"gx_{d['id']}"
        write_icon(key, lambda path, pal=pal, form=d["model"]["form"]: _gun_icon(form)(path, pal))


# ---------------------------------------------------------------- items
def do_items(defs):
    for d in defs:
        ident = f"{NS}:{d['id']}"
        comps = {
            "minecraft:icon": f"gx_{d['id']}",
            "minecraft:max_stack_size": 1,
            "minecraft:hand_equipped": True,
            "minecraft:damage": d.get("melee", 2),
            "minecraft:can_destroy_in_creative": False,
            "minecraft:use_animation": "spyglass",
            # The food component only exists so Bedrock treats the item as usable and raises
            # itemStartUse / itemReleaseUse for press-and-hold; 3600 s means it never finishes.
            "minecraft:food": {"nutrition": 0, "saturation_modifier": 0, "can_always_eat": True},
            "minecraft:use_modifiers": {"use_duration": 3600.0,
                                        "movement_modifier": d.get("move_mod", 0.9),
                                        "emit_vibrations": False},
            "minecraft:tags": {"tags": ["minecraft:is_tool"]},
        }
        if d.get("cooldown"):
            comps["minecraft:cooldown"] = {"category": f"gx_{d['id']}", "duration": d["cooldown"]}
        write_item(ident, f"gx_{d['id']}", comps, category="equipment")
        lang(f"item.{ident}", d["name"])
        lang(f"item.{ident}.desc", d.get("description", d["twist"]))
        recipe(d)


def recipe(d):
    ident = f"{NS}:{d['id']}"
    r = d["recipe"]
    if "pattern" in r:
        shaped(ident, r["pattern"], r["key"], r.get("count", 1))
    else:
        shapeless(ident, r["ingredients"], r.get("count", 1))


def do_energy_cell():
    ident = f"{NS}:energy_cell"
    key = "gx_energy_cell"
    def paint(path):
        ic = Icon()
        ic.rect(5, 2, 10, 13, "#3d4653")
        ic.rect(5, 4, 10, 11, "#8fe0ff")
        ic.rect(6, 5, 9, 10, "#eaffff")
        ic.rect(6, 2, 9, 3, "#aab4c0")
        ic.set(6, 12, "#bff0ff")
        ic.save(path)
    write_icon(key, paint)
    write_item(ident, key, {
        "minecraft:icon": key,
        "minecraft:max_stack_size": 64,
        "minecraft:hand_equipped": False,
        "minecraft:glint": True,
    }, category="items")
    lang(f"item.{ident}", "Energy Cell")
    lang(f"item.{ident}.desc", "Ammo for every Galaxy Forge weapon.")
    shapeless(ident, ["minecraft:redstone", "minecraft:amethyst_shard",
                      "minecraft:iron_ingot", "minecraft:glowstone_dust"], count=4)


# ---------------------------------------------------------------- deploy entities
def _entity_assets(name, geo, tex_px, family, health, extra_components, anims=None):
    ident = f"{NS}:{name}"
    dump(BP / f"entities/gx_{name}.json", {"format_version": "1.21.0", "minecraft:entity": {
        "description": {"identifier": ident, "is_spawnable": False, "is_summonable": True,
                        "is_experimental": False},
        "components": dict({
            "minecraft:type_family": {"family": family},
            "minecraft:health": {"value": health, "max": health},
            "minecraft:physics": {},
            "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
            "minecraft:knockback_resistance": {"value": 1.0},
            "minecraft:conditional_bandwidth_optimization": {},
            "minecraft:persistent": {},
            "minecraft:fire_immune": {},
        }, **extra_components),
        "events": {}}})
    geo_name = f"geometry.gx_{name}"
    dump(RP / f"models/entity/gx_{name}.geo.json", {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": geo_name, "texture_width": 32, "texture_height": 32,
                        "visible_bounds_width": 2, "visible_bounds_height": 2,
                        "visible_bounds_offset": [0, 0.5, 0]},
        "bones": geo}]})
    write_png(RP / f"textures/entity/gx_{name}.png", tex_px, 32, 32)
    desc = {"identifier": ident,
            "materials": {"default": "entity_emissive_alpha"},
            "textures": {"default": f"textures/entity/gx_{name}"},
            "geometry": {"default": geo_name},
            "render_controllers": [f"controller.render.gx_{name}"]}
    if anims:
        dump(RP / f"animations/gx_{name}.animation.json", {"format_version": "1.8.0", "animations": anims[0]})
        desc["animations"] = {k: f"animation.gx_{name}.{k}" for k in anims[0]}
        desc["scripts"] = {"animate": list(anims[1])}
    dump(RP / f"entity/gx_{name}.entity.json", {"format_version": "1.10.0",
         "minecraft:client_entity": {"description": desc}})
    dump(RP / f"render_controllers/gx_{name}.render_controllers.json", {"format_version": "1.10.0",
         "render_controllers": {f"controller.render.gx_{name}": {
             "geometry": "Geometry.default", "materials": [{"*": "Material.default"}],
             "textures": ["Texture.default"]}}})


def _flat_texture(paint):
    ic = Icon(32, 32)
    paint(ic)
    return ic.px


def do_deploy_entities():
    # combat drone: body + 4 arms + rotors
    geo = [
        {"name": "body", "pivot": [0, 0, 0], "cubes": [
            {"origin": [-3, -3, -3], "size": [6, 6, 6], "uv": [0, 0]},
            {"origin": [-2, -4, -2], "size": [4, 1, 4], "uv": [0, 16]}]},
        {"name": "rotor0", "parent": "body", "pivot": [-6, 0, -6], "cubes": [
            {"origin": [-7, 0, -7], "size": [3, 1, 3], "uv": [16, 0]},
            {"origin": [-10, 0, -10], "size": [10, 0, 1], "uv": [16, 4]},
            {"origin": [-10, 0, -10], "size": [1, 0, 10], "uv": [16, 4]}]},
        {"name": "rotor1", "parent": "body", "pivot": [6, 0, -6], "cubes": [
            {"origin": [4, 0, -7], "size": [3, 1, 3], "uv": [16, 0]},
            {"origin": [0, 0, -10], "size": [10, 0, 1], "uv": [16, 4]},
            {"origin": [0, 0, -10], "size": [1, 0, 10], "uv": [16, 4]}]},
        {"name": "rotor2", "parent": "body", "pivot": [-6, 0, 6], "cubes": [
            {"origin": [-7, 0, 4], "size": [3, 1, 3], "uv": [16, 0]},
            {"origin": [-10, 0, 0], "size": [10, 0, 1], "uv": [16, 4]},
            {"origin": [-10, 0, 0], "size": [1, 0, 10], "uv": [16, 4]}]},
        {"name": "rotor3", "parent": "body", "pivot": [6, 0, 6], "cubes": [
            {"origin": [4, 0, 4], "size": [3, 1, 3], "uv": [16, 0]},
            {"origin": [0, 0, 0], "size": [10, 0, 1], "uv": [16, 4]},
            {"origin": [0, 0, 0], "size": [1, 0, 10], "uv": [16, 4]}]},
        {"name": "eye", "parent": "body", "pivot": [0, -2, -3], "cubes": [
            {"origin": [-1, -3, -4], "size": [2, 2, 1], "uv": [24, 0]}]},
    ]
    def drone_tex(ic):
        ic.rect(0, 0, 5, 5, "#2f3a48"); ic.rect(6, 0, 11, 5, "#1b2028")
        ic.rect(0, 6, 11, 11, "#8fe0ff"); ic.rect(0, 6, 5, 11, "#eaffff")
        ic.rect(16, 0, 18, 2, "#3d4653"); ic.rect(16, 4, 25, 4, "#9fd8ff")
        ic.rect(24, 0, 25, 1, "#ffffff")
    anims = ({"rotors": {"loop": True, "bones": {f"rotor{i}": {
        "rotation": [0, f"query.life_time * 900"]} for i in range(4)}}}, ["rotors"])
    _entity_assets("combat_drone", geo, _flat_texture(drone_tex), ["gx_ally", "gx_deploy"], 20,
                   {"minecraft:movement": {"value": 0.0}, "minecraft:navigation.hover": {}}, anims)

    # sentinel turret: base + pivot + barrel
    geo = [
        {"name": "base", "pivot": [0, 0, 0], "cubes": [
            {"origin": [-4, 0, -4], "size": [8, 2, 8], "uv": [0, 0]},
            {"origin": [-3, 2, -3], "size": [6, 2, 6], "uv": [0, 8]}]},
        {"name": "head", "parent": "base", "pivot": [0, 4, 0], "cubes": [
            {"origin": [-3, 4, -3], "size": [6, 5, 6], "uv": [16, 0]},
            {"origin": [-1, 6, -3], "size": [2, 2, 1], "uv": [24, 0]}]},
        {"name": "barrel", "parent": "head", "pivot": [0, 6, 0], "cubes": [
            {"origin": [-1, 5, -9], "size": [2, 2, 8], "uv": [0, 16]},
            {"origin": [-2, 4, -11], "size": [4, 4, 2], "uv": [0, 20]}]},
    ]
    def turret_tex(ic):
        ic.rect(0, 0, 7, 7, "#39424f"); ic.rect(8, 0, 13, 7, "#242b33")
        ic.rect(16, 0, 21, 5, "#4a5563"); ic.rect(16, 6, 21, 7, "#7cff9a")
        ic.rect(0, 16, 15, 19, "#3d4653"); ic.rect(0, 20, 3, 23, "#9affc0")
    _entity_assets("sentinel_turret", geo, _flat_texture(turret_tex), ["gx_ally", "gx_deploy"], 20,
                   {"minecraft:movement": {"value": 0.0}, "minecraft:physics": {}})


# ---------------------------------------------------------------- generated JS
def _rgbf(hexc):
    c = rgb(hexc)
    return [round(c[0] / 255, 4), round(c[1] / 255, 4), round(c[2] / 255, 4)]


def do_script_table(defs, chars):
    custom = {}
    for d in defs:
        f = CUSTOM_DIR / f"{d['id']}.js"
        if f.exists():
            custom[d["id"]] = f
    lines = ["// GENERATED by tools/weapons/build_weapons.py - do not edit by hand.",
             "// Regenerate with: python3 tools/creatures/build_all.py", ""]
    for i, (wid, _) in enumerate(custom.items()):
        lines.append(f'import * as __c{i} from "../archetypes/custom/{wid}.js";')
    lines.append("")
    lines.append("export const CUSTOM = {")
    for i, wid in enumerate(custom):
        lines.append(f'  "gx:{wid}": __c{i},')
    lines.append("};")
    lines.append("")
    lines.append("export const GLYPHS = " + json.dumps(chars, ensure_ascii=False) + ";")
    lines.append("")
    table = {}
    for d in defs:
        pal = d["palette"]
        table[f"gx:{d['id']}"] = {
            "id": d["id"], "name": d["name"], "family": d["family"], "tier": d["tier"],
            "archetype": d["archetype"], "dps": d["dps"],
            "cooldown": d.get("cooldown", d.get("params", {}).get("cooldown")),
            "scope": d["scope"], "zoom": d.get("zoom", 1.0),
            "dot": {"style": d.get("dot", {}).get("style", "dot"),
                    "color": _rgbf(d.get("dot", {}).get("color", pal["glow"])),
                    "always": bool(d.get("dot", {}).get("always", False)),
                    "range": d.get("dot", {}).get("range", 64),
                    "show": d.get("dot", {}).get("show", True)},
            "fire_mode": d.get("fire_mode"),
            "ammo": d["ammo"],
            "heat": d.get("heat"),
            "params": rapid_params(d),
            "hooks": d["hooks"],
            "vfx": d["vfx"],
            "sound": d["sound"],
            "hud": d.get("hud", {"kind": "ammo"}),
            "palette": {k: _rgbf(pal[k]) for k in ("core", "glow", "trail", "accent")},
            "silhouette": {"projectile": d["shape"]["projectile"], "muzzle": d["shape"]["muzzle"],
                           "form": d["model"]["form"]},
            "has_custom": d["id"] in custom,
        }
    lines.append("export const WEAPONS = " + json.dumps(table, indent=1) + ";")
    lines.append("")
    lines.append("export function defFor(typeId) { return WEAPONS[typeId]; }")
    lines.append("")
    path = SCRIPTS / "generated/weapons.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")
    return sorted(custom)


# ---------------------------------------------------------------- testing doc
SCOPE_LABEL = {
    "iron": "open sights (no zoom)", "holo": "ring reticle (1.5x)", "dot": "red-dot (2x)",
    "scope4": "4x scope", "scope8": "8x scope", "thermal": "thermal tint",
    "rangefinder": "distance readout", "lock": "lock-on reticle", "focus": "zoom dial",
}


def _test_line(d):
    p = d.get("params", {})
    a = d["archetype"]
    if a == "hitscan":
        base = (f"Press use: {p.get('damage', 5)} dmg per shot at {p.get('range', 40)} blocks, "
                f"{p.get('rate', 5)}-tick cadence. Watch the {d['shape']['projectile']} tracer and "
                f"{d['shape']['muzzle']} muzzle flash, then the {d['vfx']['impact']} impact.")
    elif a == "bolt":
        base = (f"Hold use ({'auto' if p.get('auto') else 'one shot per press'}): "
                f"{p.get('count', 1)}x {d['shape']['projectile']} at {p.get('speed', 40)} b/s, "
                f"muzzle {d['shape']['muzzle']}, impact {d['vfx']['impact']}.")
    elif a == "beam":
        base = (f"Hold use: channel {p.get('dps', 10)} dps over {p.get('range', 20)} blocks; "
                f"heat climbs, release to stop.")
    elif a == "charge":
        base = (f"Hold {p.get('hold_ticks', 20) / 20:.1f}s then release: "
                f"{len(p.get('tiers', []))} tiers, mode {p.get('mode', 'hitscan')}.")
    elif a == "cone":
        base = (f"Hold use: {p.get('angle', 60)}-degree cone, {p.get('range', 8)} blocks, "
                f"{p.get('dps', 10)} dps.")
    elif a == "lob":
        base = (f"Press use: arc at {p.get('speed', 14)} b/s, AoE {p.get('aoe', 3)}; "
                f"watch the {d['shape']['projectile']} lob and its landing ring.")
    elif a == "chain":
        base = (f"Press use: arc jumps {p.get('jumps', 4)} targets within {p.get('radius', 6)} "
                f"blocks, {p.get('falloff', 0.85)} falloff per jump.")
    elif a == "deploy":
        base = (f"Press use: spawns {p.get('entity', '?')}, cap {p.get('cap', 2)}, "
                f"{p.get('duration', 20)}s, {p.get('dps', 6)} dps at {p.get('range', 12)} blocks.")
    elif a == "field":
        base = "Hit a mob to place the zone; stand in it and watch the pull/damage tick."
    else:
        base = (f"Press use: attaches within {p.get('range', 10)} blocks and pulls; "
                f"sneak + use to grapple.")
    return base


def do_testing_doc(defs):
    """Write docs/weapons/TESTING.md: a 30-second in-game check per weapon."""
    lines = [
        "# Galaxy Forge — in-game test checklist",
        "",
        "Generated from the roster by `tools/weapons/build_weapons.py`; regenerate with",
        "`python3 tools/creatures/build_all.py`. Each entry is a 30-second check.",
        "",
        "Before the first weapon: give yourself `gx:energy_cell` x64 and every weapon",
        "(`/give @s gx:pulse_carbine` …), then in a flat world:",
        "",
        "1. Sneak to aim — the scope overlay and laser dot appear, action bar shows the readout.",
        "2. Fire — the weapon fires, bolts/beams/particles render, mobs take damage.",
        "3. Hit your `galaxy:pup` and a tamed wolf — neither takes damage.",
        "4. Empty the magazine, then press use — it reloads from an energy cell.",
        "",
        "## Roster",
        "",
    ]
    for d in defs:
        lines.append(f"### {d['name']} (`gx:{d['id']}`) — {d['tier']}, {d['archetype']}")
        lines.append(f"- Scope: {SCOPE_LABEL.get(d['scope'], d['scope'])}; "
                     f"dot {d['dot']['style']} `{d['dot']['color']}`.")
        lines.append(f"- 30s test: {_test_line(d)}")
        lines.append(f"- Twist: {d['twist']}")
        lines.append(f"- Ammo: {d['ammo']['type']}"
                     + (f", mag {d['ammo'].get('mag')}" if d['ammo'].get('mag') else "")
                     + (f"; heat {d['heat']['max']}" if d.get('heat') else "") + ".")
        lines.append("")
    path = HERE.parents[1] / "docs" / "weapons" / "TESTING.md"
    path.write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------- entry
def run():
    import os
    defs = validate(load_defs(), partial=bool(os.environ.get("GX_PARTIAL")))
    chars = glyphs.write_font()
    particles.write_particles()
    sounds.write_sounds()
    model.write_shared_animations()
    for d in defs:
        model.write_model(d)
    do_icons(defs)
    do_items(defs)
    do_energy_cell()
    do_deploy_entities()
    do_testing_doc(defs)
    customs = do_script_table(defs, chars)
    print(f"  weapons: {len(defs)} items, {len(customs)} custom twist modules")
    return defs


if __name__ == "__main__":
    run()
