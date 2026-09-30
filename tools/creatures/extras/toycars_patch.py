"""Post-build patch for the toy cars (specs/toycars_lego.py, specs/toycars_diecast.py).
lib.build_behavior gives every 'mount' the combat/wander goals of a creature; a toy car should just sit parked until
someone climbs in.  It also has no notion of vehicle auto-step, so add minecraft:variable_max_auto_step here:
a ridden car climbs one full block smoothly instead of hopping.  Idempotent; runs after every build_all."""
import json
import lib
from lib import BP

STRIP = ("minecraft:attack", "minecraft:behavior.melee_attack", "minecraft:behavior.hurt_by_target",
         "minecraft:behavior.random_stroll", "minecraft:behavior.look_at_player", "minecraft:behavior.random_look_around",
         "minecraft:follow_range")


def run():
    for f in sorted((BP / "entities").glob("gx_toycar_*.json")):
        d = json.loads(f.read_text())
        c = d["minecraft:entity"]["components"]
        for k in STRIP:
            c.pop(k, None)
        c["minecraft:variable_max_auto_step"] = {"base_value": 1.0625, "controlled_value": 1.0625,
                                                 "jump_prevented_value": 0.5625}
        c["minecraft:fall_damage"] = {"value": 0.25}
        lib.dump(f, d)
