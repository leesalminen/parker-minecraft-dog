"""Post-process the generated vehicle entities (gx:car, gx:plane, gx:helicopter).

lib.build_behavior emits a generic 'mount' (hostile-ish AI: melee, wandering, look-at-player).  A vehicle
must sit still until ridden, never fight and never hurt a small kid, so this strips the AI and adds
crash/fall/fire immunity.  Runs from build_all.py after the creature specs are emitted; idempotent.
Movement/terrain smoothing itself lives in packs/GalaxyForge_BP/scripts/vehicles.js.
"""
import json
import lib
from lib import BP

VEHICLES = ("car", "plane", "helicopter")

STRIP = (
    "minecraft:attack", "minecraft:behavior.melee_attack", "minecraft:behavior.hurt_by_target",
    "minecraft:behavior.nearest_attackable_target", "minecraft:behavior.random_stroll",
    "minecraft:behavior.random_hover", "minecraft:behavior.random_fly",
    "minecraft:behavior.look_at_player", "minecraft:behavior.random_look_around",
    "minecraft:behavior.panic", "minecraft:experience_reward", "minecraft:jump.static",
    "minecraft:horse.jump_strength", "minecraft:can_power_jump", "minecraft:leashable",
    "minecraft:navigation.walk", "minecraft:navigation.hover", "minecraft:navigation.fly",
)

# Damage causes a small kid should never be punished by while driving.
SAFE_CAUSES = ("fall", "fly_into_wall", "contact", "suffocation", "drowning", "fire", "fire_tick",
               "lava", "magma", "block_explosion", "entity_explosion", "lightning", "freezing", "thorns")


def patch(vid):
    path = BP / f"entities/gx_{vid}.json"
    if not path.exists():
        return
    ent = json.loads(path.read_text())
    comps = ent["minecraft:entity"]["components"]
    for k in STRIP:
        comps.pop(k, None)
    comps["minecraft:fire_immune"] = {}
    comps["minecraft:damage_sensor"] = {"triggers": [
        {"cause": c, "deals_damage": False} for c in SAFE_CAUSES]}
    comps["minecraft:pushable"] = {"is_pushable": vid == "car", "is_pushable_by_piston": False}
    comps["minecraft:movement"] = comps.get("minecraft:movement", {"value": 0.2})
    comps["minecraft:nameable"] = {}
    comps["minecraft:physics"] = {}
    if vid == "car":
        # rider steers with mouse yaw + W; jump key does nothing (no horse hop); floats on water.
        comps["minecraft:behavior.float"] = {"priority": 0}
        comps["minecraft:input_ground_controlled"] = {}
    else:
        comps["minecraft:input_air_controlled"] = {"strafe_speed_modifier": 0.4, "backwards_movement_modifier": 0.3}
    ent["minecraft:entity"]["description"]["is_experimental"] = False
    lib.dump(path, ent)


def run():
    for v in VEHICLES:
        patch(v)
