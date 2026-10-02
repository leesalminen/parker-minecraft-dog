"""Storm-trooper style imperials (hostile) and clone-trooper style allies (tameable, shoot back)."""
from specs.troopers_common import build

EMPIRE_LOOT = [("minecraft:iron_ingot", 1, 2), ("minecraft:redstone", 0, 2), ("minecraft:quartz", 0, 2)]
BLASTER_RED, BLASTER_BLUE = "gx:blaster_bolt_red", "gx:blaster_bolt_blue"


def imperial(**kw):
    b = {"role": "hostile", "health": 24, "speed": 0.28, "damage": 3, "box": [0.7, 2.0], "ranged": True, "range": 20,
         "projectile": BLASTER_RED, "family": ["stormtrooper", "trooper", "empire"],
         "loot": EMPIRE_LOOT, "sound": ("skeleton", [0.8, 0.95]), "xp": 6,
         "spawn": {"biomes": ["overworld"], "weight": 4, "herd": [3, 5]}}
    b.update(kw)
    return b


def clone(**kw):
    b = {"role": "companion", "health": 30, "speed": 0.3, "damage": 4, "box": [0.7, 2.0], "ranged": True, "range": 22,
         "projectile": BLASTER_BLUE, "family": ["clone", "trooper", "republic"],
         "tame_items": ["minecraft:cooked_beef", "minecraft:bread", "minecraft:cooked_porkchop"],
         "sound": ("villager", [0.7, 0.8]), "xp": 0,
         "spawn": {"biomes": ["overworld"], "weight": 3, "herd": [2, 4]}}
    b.update(kw)
    return b


SPECS = [build(c) for c in [
    dict(id="stormtrooper", name="Storm Trooper", egg=("#eef0f2", "#1b1d20"), style="storm", base="#eef0f2", dark="#b4bac0",
         under="#1b1d20", grime=0.05, behavior=imperial()),
    dict(id="sandtrooper", name="Sand Trooper", egg=("#d8d1bd", "#c86a24"), style="storm", base="#dcd3bb", dark="#a2977c",
         under="#4a4436", grime=0.55, pauldron=("r", "orange", "#c46a26"), pack_canteen=True, backpack=True,
         behavior=imperial(spawn={"biomes": ["desert", "mesa"], "weight": 6, "herd": [3, 5]})),
    dict(id="scout_trooper", name="Scout Trooper", egg=("#dfe2e5", "#25282c"), style="scout", base="#e2e5e8", dark="#a0a6ac",
         under="#25282c", grime=0.1, backpack=True,
         behavior=imperial(health=20, speed=0.34, range=26, spawn={"biomes": ["forest", "taiga"], "weight": 3, "herd": [1, 2]})),
    dict(id="clone_trooper", name="Clone Trooper", egg=("#eceef0", "#2f6fd6"), style="clone", base="#eceef0", dark="#b0b6bc",
         under="#20242a", accent="#2f6fd6", pauldron=("r", "blue", "#2f6fd6"), backpack=True, behavior=clone()),
    dict(id="clone_commander", name="Clone Commander", egg=("#e8e4d8", "#e0a020"), style="commander", base="#e8e4d8",
         dark="#aaa590", under="#20242a", accent="#e0a020", kama="#b87a12", fin=True,
         pauldron=("l", "gold", "#e0a020"), behavior=clone(health=40, damage=5)),
    dict(id="clone_heavy", name="Heavy Clone Trooper", egg=("#e9e9ec", "#d63a2f"), style="heavy", base="#e9e9ec",
         dark="#b0b0b6", under="#20242a", accent="#d63a2f", pauldron=("both", "red", "#d63a2f"), backpack=True,
         scale=1.1, behavior=clone(health=55, damage=6, speed=0.26, box=[0.8, 2.2])),
]]
