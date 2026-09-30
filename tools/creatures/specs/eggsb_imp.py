"""Ember Imp - small flying trickster: bat wings, curled horns, forked tail.  Fire immune."""
from eggsb_kit import *

RED, DARK = "#c8321e", "#7a1a12"

skin = coat(RED, dark=DARK, light="#e85a38", under="#e8a060", seed=101, patch=2.5)

def horn(p):
    return mix("#2a1a18", "#5a3a30", (p.p[1] * 0.4) % 1.0)

def membrane(p):
    c = mix("#5a1a2a", "#8a2a3a", noise3(*p.p, 103, 2.0))
    return c if p.face in ("top", "bottom") or (p.x + p.y) % 5 else shade(c, 0.8)

def rune(p, c):
    if p.bone == "body" and p.face == "front" and p.fw >= 4:
        cx = p.fw // 2
        if (p.x in (cx - 1, cx) and 1 <= p.y <= 3) or (p.y == 2 and cx - 2 <= p.x <= cx + 1): return glow("#ffb02a")

def mouth(p):
    c = skin(p)
    if p.face == "front" and p.y == p.fh - 1 and p.fw >= 4 and 0 < p.x < p.fw - 1: return "#2a0808" if p.x % 2 else "#f4ecd8"
    return c

body_skin = coat(RED, dark=DARK, light="#e85a38", under="#e8a060", seed=105, patch=2.5, extra=rune)

bones = biped(4, 6, 3, 4, 2, 2, 5, 2, 2, (6, 5, 5), skin="body", head_skin="face", leg_skin="skin", arm_skin="skin",
              leg_x=1.2, foot_h=1, foot_skin="horn", hand_h=1, hand_skin="horn")
add(bones, "head",
    pair(C([2, 14, -1], [1, 3, 1], "horn", rot=[0, 0, -10], pivot=[2, 14, 0])), pair(C([2.6, 16.5, -0.6], [1, 2, 1], "horn", rot=[0, 0, -45], pivot=[2, 14, 0])),
    pair(C([3, 11.5, -1], [3, 2, 1], "skin", rot=[0, 0, 25], pivot=[3, 12, 0])),        # pointed ears
    pair(C([1, 11, -3.0], [1, 1, 1], "horn")),
    eyes(0.8, 11.4, -2.5, "eye", 2), C([-1, 10.6, -3.4], [2, 1, 1], "skin"))
bones.append(bone("tail", "body", [0, 6, 1.5], [C([-0.5, 4, 1.5], [1, 1, 4], "skin"), C([-0.5, 3, 5.5], [1, 1, 4], "skin", rot=[25, 0, 0], pivot=[0, 4, 5.5]),
                                               C([-1.5, 1.5, 8.5], [3, 3, 1], "tip"), C([-0.5, 1, 9.3], [1, 4, 1], "tip")]))
bones.append(bat_wing("wing_l", "body", 1, 2, 9, 1.5, 9, 6, "horn", "membrane"))
bones.append(bat_wing("wing_r", "body", -1, 2, 9, 1.5, 9, 6, "horn", "membrane"))

anims = biped_anims(walk_amp=35, freq=60, extra_idle=merge(sway("tail", 20, 70, 1), fold("wing_l", "wing_r", 40, 8, 240)))
anims["walk"]["bones"].update(fold("wing_l", "wing_r", 40, 6, 200))
anims["flap"] = flap_anim("wing_l", "wing_r", amp=40, rate=380, extra=merge(sway("tail", 20, 70, 1), {"leg_l": {"rotation": ["20", "0", "0"]}, "leg_r": {"rotation": ["10", "0", "0"]}}))

SPEC = with_visible({
    "id": "imp", "name": "Ember Imp", "egg": ("#c8321e", "#ffb02a"), "glow": True, "scale": 1.0,
    "bones": bones,
    "skins": {"default": skin, "skin": skin, "body": body_skin, "face": mouth, "horn": horn, "membrane": membrane,
              "tip": solid("#5a1410", 0.2, 9), "eye": lambda p: glow("#ffe84a") if p.face == "front" else glow("#ff9a1a")},
    "anims": anims, "play": PLAY_FLY,
    "behavior": {
        "role": "neutral", "health": 14, "speed": 0.28, "fly": True, "fly_speed": 0.3, "damage": 3, "box": [0.5, 0.95],
        "fire_immune": True, "family": ["imp"],
        "spawn": {"biomes": ["desert", "mesa", "swamp"], "weight": 4, "herd": [1, 2]},
        "loot": [("minecraft:gunpowder", 0, 2), ("minecraft:gold_nugget", 0, 2), ("minecraft:coal", 0, 1)],
        "sound": ("vex", [1.1, 1.3]),
    },
})
