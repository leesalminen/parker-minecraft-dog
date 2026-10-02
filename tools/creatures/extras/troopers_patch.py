"""Blaster-bolt projectile entities + AI fixes for the trooper specs (runs after the specs are emitted).

* gx:blaster_bolt_red / _blue: fast, gravity-free, emissive bolts that troopers shoot.
* clones: never attack the player; shoot monsters, imperials and droids; defend their owner once tamed.
* imperials: also hunt clones.  Everyone shoots a bit faster than the generic ranged default.
"""
import json
import lib
from lib import BP, RP, dump, write_png

BOLTS = {"red": ("#ff2a1f", "#ffd0c8", 3, 5), "blue": ("#2f8bff", "#d0e8ff", 4, 6)}
CLONES = ("clone_trooper", "clone_commander", "clone_heavy")
IMPERIALS = ("stormtrooper", "sandtrooper", "scout_trooper")


def bolt(name, glow, core, dmin, dmax):
    ident = f"gx:blaster_bolt_{name}"
    key = f"gx_blaster_bolt_{name}"
    dump(BP / f"entities/{key}.json", {"format_version": "1.16.0", "minecraft:entity": {
        "description": {"identifier": ident, "is_spawnable": False, "is_summonable": True, "is_experimental": False,
                        "runtime_identifier": "minecraft:snowball"},
        "components": {
            "minecraft:type_family": {"family": ["projectile", "blaster_bolt"]},
            "minecraft:collision_box": {"width": 0.2, "height": 0.2},
            "minecraft:physics": {},
            "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
            "minecraft:conditional_bandwidth_optimization": {},
            "minecraft:projectile": {
                "power": 2.6, "gravity": 0.0, "inertia": 1.0, "liquid_inertia": 1.0, "uncertainty_base": 1.5,
                "hit_sound": "random.fizz", "anchor": 1, "offset": [0, -0.1, 0],
                "on_hit": {"impact_damage": {"damage": {"min": dmin, "max": dmax}, "knockback": True, "catch_fire": False},
                           "remove_on_hit": {}}},
            "minecraft:timer": {"time": 3, "looping": False, "time_down_event": {"event": "gx:despawn", "target": "self"}},
        },
        "events": {"gx:despawn": {"add": {"component_groups": []}}}}})
    # the timer above is only a placeholder hook; real lifetime is handled by the engine's projectile despawn
    ent = json.loads((BP / f"entities/{key}.json").read_text())
    ent["minecraft:entity"]["components"].pop("minecraft:timer")
    ent["minecraft:entity"]["events"] = {}
    dump(BP / f"entities/{key}.json", ent)

    px = [(0, 0, 0, 0)] * 256
    for i in range(256):
        x, y = i % 16, i // 16
        px[i] = lib.glow(core if (x + y) % 5 == 0 else glow)
    write_png(RP / f"textures/entity/{key}.png", px, 16, 16)
    dump(RP / f"entity/{key}.entity.json", {"format_version": "1.10.0", "minecraft:client_entity": {"description": {
        "identifier": ident, "materials": {"default": "entity_emissive_alpha"},
        "textures": {"default": f"textures/entity/{key}"}, "geometry": {"default": "geometry.gx_blaster_bolt"},
        "render_controllers": ["controller.render.gx_blaster_bolt"]}}})


def run():
    for name, (glow, core, lo, hi) in BOLTS.items():
        bolt(name, glow, core, lo, hi)
    dump(RP / "models/entity/gx_blaster_bolt.geo.json", {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.gx_blaster_bolt", "texture_width": 16, "texture_height": 16,
                        "visible_bounds_width": 2, "visible_bounds_height": 2, "visible_bounds_offset": [0, 0, 0]},
        "bones": [{"name": "bolt", "pivot": [0, 0, 0], "cubes": [
            {"origin": [-1, -1, -5], "size": [2, 2, 10], "uv": [0, 0]},
            {"origin": [-1.5, -1.5, -2], "size": [3, 3, 4], "uv": [0, 0]}]}]}]})
    dump(RP / "render_controllers/gx_blaster_bolt.render_controllers.json", {"format_version": "1.10.0", "render_controllers": {
        "controller.render.gx_blaster_bolt": {"geometry": "Geometry.default", "materials": [{"*": "Material.default"}],
                                              "textures": ["Texture.default"]}}})

    for cid in CLONES:
        path = BP / f"entities/gx_{cid}.json"
        if not path.exists():
            continue
        ent = json.loads(path.read_text())
        e = ent["minecraft:entity"]
        c = e["components"]
        c["minecraft:behavior.nearest_attackable_target"] = {
            "priority": 2, "must_see": True, "reselect_targets": True,
            "entity_types": [{"filters": {"all_of": [
                {"test": "is_family", "subject": "other", "value": "monster"},
                {"test": "is_family", "subject": "other", "operator": "!=", "value": "clone"}]}, "max_dist": 26}]}
        c["minecraft:behavior.ranged_attack"].update({"attack_interval_min": 0.7, "attack_interval_max": 1.6})
        e["component_groups"]["gx:tame"].update({
            "minecraft:behavior.owner_hurt_by_target": {"priority": 1},
            "minecraft:behavior.owner_hurt_target": {"priority": 2}})
        dump(path, ent)
    for sid in IMPERIALS:
        path = BP / f"entities/gx_{sid}.json"
        if not path.exists():
            continue
        ent = json.loads(path.read_text())
        c = ent["minecraft:entity"]["components"]
        c["minecraft:behavior.nearest_attackable_target"]["entity_types"].append(
            {"filters": {"test": "is_family", "subject": "other", "value": "clone"}, "max_dist": 28})
        c["minecraft:behavior.ranged_attack"].update({"attack_interval_min": 0.9, "attack_interval_max": 2.0})
        dump(path, ent)
