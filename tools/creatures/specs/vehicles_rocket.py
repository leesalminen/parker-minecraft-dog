"""Galaxy Rocket - upright two-seat rocket with a 360-degree glass cabin.  Climbs to the top of the sky (space).
Model faces -Z, y up, ground y=0.  Flight lives in scripts/vehicles.js (tickRocket)."""
import math
from lib import *
from specs.vehicles_common import *

_white = paint("#f1f3f5", "#a9b1b8", 151, 12.0)
red = paint("#d8362b", "#7e1e18", 153, 9.0)
dark = paint("#2b3037", "#14171b", 155, 8.0)
steel = paint("#8a939b", "#3c434a", 157, 7.0)
flame = lamp("#ff9a3a")


def hull(p):
    c = _white(p)
    y = p.p[1]
    if p.face not in ("top", "bottom"):
        if 36 <= y < 46 or 62 <= y < 66:
            return red(p)
        if 50 <= y < 52:
            return dark(p)
    return c


# ---------------------------------------------------------------- tank, skirt, engines
body = cyl_y(0, 0, 14, 82, 48, "hull")
body += cyl_y(0, 0, 8, 6, 52, "dark")                          # skirt ring
body += cyl_y(0, 0, 96, 3, 50, "steel")                        # cabin floor
body += cyl_y(0, 0, 143, 3, 50, "steel")                       # cabin roof
for i, (dy, D) in enumerate(((146, 44), (156, 38), (166, 32), (176, 26), (186, 20), (196, 14), (206, 8))):
    body += cyl_y(0, 0, dy, 10, D, "hull" if i < 4 else "red")
body += cyl_y(0, 0, 216, 8, 4, "steel")
for ex, ez in ((0, 0), (14, 0), (-14, 0), (0, 14), (0, -14)):
    body += cyl_y(ex, ez, 2, 10, 14 if (ex, ez) == (0, 0) else 10, "dark")
    body.append({"o": [ex - 3, 0, ez - 3], "s": [6, 2, 6], "skin": "flame"})

fins = []
for k in range(0, 4):
    for j in range(0, 12):
        e = int(30 * (1 - j / 12.0)) + 2
        y = 4 + j * 5
        if k == 0:
            fins.append({"o": [24, y, -2], "s": [e, 5, 4], "skin": "red"})
        elif k == 1:
            fins.append({"o": [-24 - e, y, -2], "s": [e, 5, 4], "skin": "red"})
        elif k == 2:
            fins.append({"o": [-2, y, 24], "s": [4, 5, e], "skin": "red"})
        else:
            fins.append({"o": [-2, y, -24 - e], "s": [4, 5, e], "skin": "red"})

# ---------------------------------------------------------------- 360-degree cabin (posts + sparse glass)
cabin = []
for k in range(8):
    a = math.radians(22.5 + 45 * k)
    R = 24.0
    cabin.append({"o": [R * math.sin(a) - 1.5, 99, -R * math.cos(a) - 1.5], "s": [3, 44, 3], "skin": "steel"})
for k in range(8):
    cabin.append({"o": [-9, 99, -22.5], "s": [18, 44, 1], "skin": "glass", "rot": [0, 45 * k, 0], "pivot": [0, 121, 0]})
cabin += seat_set(-9, 99, 0, w=12, d=12, back_h=14, skin="fabric", head=True)
cabin += seat_set(9, 99, 0, w=12, d=12, back_h=14, skin="fabric", head=True)
cabin.append({"o": [-6, 99, -14], "s": [12, 8, 4], "skin": "dark"})          # console

bones = [
    {"name": "body", "parent": None, "pivot": [0, 100, 0], "cubes": body + fins},
    {"name": "cabin", "parent": "body", "pivot": [0, 100, 0], "cubes": cabin},
]

anims = {
    "fly": anim(merge({"body": {"position": ["math.sin(query.life_time * 900) * 0.25", "0", "math.cos(query.life_time * 800) * 0.25"]}})),
    "idle": anim(merge({"body": {"position": ["0", "math.sin(query.life_time * 30) * 0.05", "0"]}})),
}

SPEC = {
    "id": "rocket",
    "name": "Galaxy Rocket",
    "egg": ("#f1f3f5", "#d8362b"),
    "glow": True,
    "scale": 1.0,
    "visible": [6.0, 15.0, 6.0],
    "bones": bones,
    "skins": {"default": hull, "hull": hull, "red": red, "dark": dark, "steel": steel, "flame": flame,
              "glass": glass("#9fe4ff"), "fabric": fabric("#3b3f47", "#555b66")},
    "anims": anims,
    "play": [{"fly": "query.has_rider"}, {"idle": "!query.has_rider"}],
    "behavior": {
        "role": "mount",
        "health": 150, "speed": 0.4, "damage": 0, "box": [3.2, 7.0],
        "hover": True, "fly_speed": 0.5, "knockback_resist": 1.0, "family": ["vehicle", "gx_vehicle", "rocket"],
        "ride": {"seats": [[-0.5, 6.2, 0], [0.5, 6.2, 0]]},
        "sound": ("dragon", [0.5, 0.6]),
        "xp": 0,
    },
}
