"""Five die-cast (Hot Wheels-style) toy cars: low, wide-tyred, metallic clear-coat paint, chrome, flames and stripes,
with orange 'track piece' accents. Rideable, one seat."""
import math
from lib import *
from .toycars_common import *

ORANGE = "#ff6a00"


def pw(z, table):
    for zmax, v in table:
        if z < zmax:
            return v
    return table[-1][1]


def sidef(p):
    return p.face in ("east", "west")


def roundel(p, cz, cy, r, colour):
    x, y, z = p.p
    return colour if sidef(p) and (z - cz) ** 2 + (y - cy) ** 2 <= r * r else None


def flicker(bone, base=0.2, rate=2600, lo=0.7, amp=0.5, axis=2):
    e = ["1", "1", "1"]
    e[axis] = f"query.modified_move_speed > 0.02 ? ({lo} + {amp} * math.sin(query.life_time * {rate})) : {base}"
    return {bone: {"scale": e}}


def stripes_top(p, centre, half, edge_col=ORANGE, col="#f4f4f4"):
    """Racing stripes on top faces (|x| == centre, or a single stripe when centre = 0)."""
    if p.face != "top":
        return None
    d = abs(abs(p.p[0]) - centre)
    if d < half:
        return col
    if d < half + 0.9:
        return edge_col
    return None


# =============================================================================== 1. muscle car
def muscle():
    car = Car(pivot_y=6)
    car.cube("body", [-5, 3, -11], [10, 1, 22], "dark")
    lower_yb = lambda z: 7 if (-10 <= z <= -4 or 4 <= z <= 10) else 4
    slices(car, "body", -12, 12, 2, lambda z: 7, lower_yb,
           lambda z: 7 if z < -10 else (8 if z < -2 else 9), "paint")
    cab_top = {-4: 10, -2: 11, 0: 12, 2: 12, 4: 11, 6: 10}
    slices(car, "body", -4, 8, 2, lambda z: 5.5, lambda z: 9, lambda z: cab_top[int(math.floor(z / 2.0)) * 2], "paint")

    def decal(p):
        x, y, z = p.p
        ax = abs(x)
        if ax < 6.0 and y > 8.5:                                # greenhouse
            if sidef(p) and -3.6 < z < 7.6 and 9.6 < y < 11.4 and abs(z - 1.6) > 0.5:
                return "GLASS"
            if p.face == "top" and (z < 0 or z > 4.0) and y > 9.5:
                return "GLASS"
            if p.face == "front" and y > 9.0 and z < -3.5:
                return "GLASS"
            if p.face == "back" and y > 9.0 and z > 7.5:
                return "GLASS"
        s = stripes_top(p, 2.3, 1.0)
        if s and y > 7.5:
            return s
        if sidef(p) and ax > 6.5:
            if 4.0 <= y < 5.0:
                return ORANGE
            if 5.0 <= y < 5.6:
                return "#f4f4f4"
            dl = door_lines(p, -2.6, 4.2, 5.6, 8.9)
            if dl:
                return dl
            r = roundel(p, 0.8, 7.0, 1.5, "#f4f4f4")
            if r:
                return ORANGE if abs(z - 0.8) < 0.6 else r
            if z < -3.4:
                f = flame_decal(-12, -3.4, 5.6, 8.6)(p)
                if f:
                    return f
        return None
    car.cube("body", [-2, 8, -10], [4, 1, 5], "black")               # hood scoop
    car.cube("body", [-2, 8, -11], [4, 1, 1], "grille")
    car.cube("body", [-6, 4, -13], [12, 2, 1], "chrome")             # front bumper
    car.cube("body", [-6, 3, -12], [12, 1, 2], "orange")             # splitter
    car.sym("body", [3.5, 5, -13.5], [3, 3, 1], "head")
    car.cube("body", [-3, 6, -13], [6, 2, 1], "grille")
    car.cube("body", [-6, 4, 12], [12, 2, 1], "chrome")              # rear bumper
    car.sym("body", [1, 6, 12], [5, 2, 1], "lamp_r")
    car.sym("body", [4, 3, 12], [2, 2, 2], "chrome")                 # exhaust tips
    car.cube("body", [-5, 9, 9], [10, 1, 3], "paint")                # duck tail
    car.sym("body", [5.5, 9, -1.5], [2, 1, 1], "chrome")             # mirrors
    car.bone("flame_l", "body", [-4, 4, 13.5])
    car.cube("flame_l", [-4.5, 3.5, 14], [1, 1, 3], "flame")
    car.bone("flame_r", "body", [4, 4, 13.5])
    car.cube("flame_r", [3.5, 3.5, 14], [1, 1, 3], "flame")
    for n, x, z in (("wheel_fl", 6.6, -7), ("wheel_fr", -6.6, -7), ("wheel_rl", 6.6, 7), ("wheel_rr", -6.6, 7)):
        car.wheel(n, x, z, 3.2, 3, "tire", "hub")
    skins = dc_skins("#1f5fd8", decal, 7.2)
    fx = merge(flicker("flame_l"), flicker("flame_r", rate=2900))
    anims = make_anims(car, fx=fx)
    return make_spec(car, "toycar_muscle", "Flame Roller", ("#1f5fd8", ORANGE), skins, anims,
                     speed=0.72, box=(1.3, 0.85), seat=(0, 0.28, 0.1), visible=(3.0, 1.6, 0.5))


# =============================================================================== 2. hot rod
def hotrod():
    car = Car(pivot_y=5)
    car.sym("body", [2, 3, -11], [2, 2, 22], "dark")
    car.cube("body", [-6.5, 2, -9.5], [13, 1, 1], "chrome_lo")
    car.cube("body", [-8, 3.5, 5.5], [16, 2, 2], "dark")
    car.cube("body", [-3, 5, -10], [6, 4, 8], "engine")
    car.sym("body", [3, 9, -9], [1, 2, 7], "chrome")
    car.cube("body", [-2, 9, -8], [4, 3, 5], "chrome")
    car.cube("body", [-1.5, 12, -7], [3, 2, 3], "black")
    car.sym("body", [4.5, 6, -10], [1, 1, 10], "chrome_lo")
    for z in (-8, -5, -2):
        car.sym("body", [3, 7, z], [2, 1, 1], "chrome_lo")
    car.cube("body", [-4, 4, -12], [8, 7, 1], "grille")               # radiator shell
    car.cube("body", [-5, 3, -13], [10, 1, 1], "chrome")              # bumper
    car.sym("body", [4, 8, -13], [3, 3, 2], "head")
    slices(car, "body", -1, 9, 2, lambda z: 5, lambda z: 5, lambda z: 10, "paint")
    slices(car, "body", -1, 8, 3, lambda z: 4.5, lambda z: 10, lambda z: 13, "paint")
    car.cube("body", [-5, 5, 9], [10, 3, 3], "paint")
    car.cube("body", [-5, 3.5, 12], [10, 1, 1], "chrome")
    car.sym("body", [1.5, 6, 12], [3, 1, 1], "lamp_r")
    car.cube("body", [-3, 5, 4], [6, 3, 3], "seat")

    def decal(p):
        x, y, z = p.p
        ax = abs(x)
        if y > 10 and ax < 5:
            if sidef(p) and -0.5 < z < 6.5 and 10.5 < y < 12.3 and abs(z - 3.0) > 0.4:
                return "GLASS"
            if p.face == "front" and y > 10.5 and z < 0.5:
                return "GLASS"
            if p.face == "back" and y > 10.5 and z > 6.6:
                return "GLASS"
        if sidef(p) and ax > 4.4:
            if 5.0 <= y < 6.0:
                return ORANGE
            f = flame_decal(-1, 9, 6.0, 10.2)(p)
            if f:
                return f
        if p.face == "top" and ax < 1.0 and z > 8.5:
            return "#f4f4f4"
        return None
    for n, x, z, r, w in (("wheel_fl", 7.5, -9.5, 2.6, 2), ("wheel_fr", -7.5, -9.5, 2.6, 2),
                          ("wheel_rl", 7.5, 7, 4.6, 5), ("wheel_rr", -7.5, 7, 4.6, 5)):
        car.wheel(n, x, z, r, w, "tire", "hub")
    skins = dc_skins("#7a22c8", decal, 8.0)
    car.bone("blower", "body", [0, 10.5, -6])
    car.cube("blower", [-1.5, 11.5, -8.5], [3, 1, 1], "chrome")
    fx = {"blower": {"rotation": ["0", "math.sin(query.life_time * 2000) * 8", "0"]}}
    anims = make_anims(car, fx=fx, bump=0.22)
    return make_spec(car, "toycar_hotrod", "Scorch Rod", ("#7a22c8", "#ffb01f"), skins, anims,
                     speed=0.7, box=(1.3, 0.9), seat=(0, 0.32, 0.25), visible=(3.0, 1.7, 0.55))


# =============================================================================== 3. drag racer
def dragster():
    car = Car(pivot_y=5)
    nose_w = {-12: 1, -10: 1, -8: 1.5, -6: 2, -4: 2.5}
    slices(car, "body", -12, -2, 2, lambda z: nose_w[int(math.floor(z / 2.0)) * 2], lambda z: 3,
           lambda z: 5 if z < -6 else 6, "paint")
    car.cube("body", [-3, 3, -2], [6, 2, 7], "dark")
    car.sym("body", [2, 5, -2], [1, 3, 6], "paint")                  # cockpit walls
    car.cube("body", [-2, 5, -2], [4, 3, 1], "paint")                # dash
    car.cube("body", [-2, 5, 3], [4, 1, 2], "seat")
    car.sym("body", [2, 5, 4], [1, 7, 1], "chrome_lo")               # roll hoop
    car.cube("body", [-2, 12, 4], [4, 1, 1], "chrome_lo")
    car.cube("body", [-3, 4, 5], [6, 5, 6], "engine")                # engine
    car.cube("body", [-2, 9, 6], [4, 3, 4], "chrome")                # blower
    car.cube("body", [-2, 12, 6.5], [4, 2, 3], "black")
    car.cube("body", [-4, 4, 11], [8, 4, 1], "dark")
    car.sym("body", [3.5, 6, 5], [1, 1, 6], "chrome_lo")             # headers
    for i, z in enumerate((5, 7, 9)):
        car.sym("body", [3.5, 7, z], [1, 3, 1], "chrome_lo")
        car.bone(f"jet_l{i}", "body", [3.5, 10, z + 0.5])
        car.cube(f"jet_l{i}", [3.5, 10, z], [1, 2, 1], "flame")
        car.bone(f"jet_r{i}", "body", [-3.5, 10, z + 0.5])
        car.cube(f"jet_r{i}", [-4.5, 10, z], [1, 2, 1], "flame")
    car.cube("body", [-6, 2, -13], [12, 1, 3], "orange")             # front wing
    car.sym("body", [6, 2, -13], [1, 3, 3], "paint")
    car.cube("body", [-5, 3, -8.5], [10, 1, 1], "chrome_lo")         # front axle
    car.cube("body", [-7, 14, 9], [14, 1, 4], "paint")               # rear wing
    car.sym("body", [7, 10, 9], [1, 6, 4], "orange")
    car.sym("body", [3, 8, 11], [1, 6, 1], "dark")
    car.cube("body", [-2, 8, 12], [4, 3, 2], "orange")               # chute pack

    def decal(p):
        x, y, z = p.p
        if p.face == "top" and abs(x) < 0.8 and z < 0:
            return "#0e1012"
        if sidef(p) and z < 4:
            f = flame_decal(-12, 3.5, 3.0, 7.6)(p)
            if f:
                return f
        if p.face == "top" and z < -1 and abs(abs(x) - 1.5) < 0.5:
            return "#f4f4f4"
        return None
    car.wheel("wheel_fl", 4.5, -8.5, 2.5, 1, "tire", "hub")
    car.wheel("wheel_fr", -4.5, -8.5, 2.5, 1, "tire", "hub")
    car.wheel("wheel_rl", 8.0, 8.0, 5.0, 5, "tire", "hub")
    car.wheel("wheel_rr", -8.0, 8.0, 5.0, 5, "tire", "hub")
    skins = dc_skins("#35c83e", decal, 4.8)
    skins["tire"] = tire_painter("#0f1013", "#d8dde4", "#4c5058", False, 8, 0.6, ORANGE)
    fx = {}
    for i in range(3):
        for nm in "lr":
            fx.update(flicker(f"jet_{nm}{i}", 0.3, 2500 + 300 * i, 0.9, 0.5, 1))
    anims = make_anims(car, fx=fx, bump=0.12)
    return make_spec(car, "toycar_dragster", "Nitro Dragster", ("#35c83e", ORANGE), skins, anims,
                     speed=0.9, box=(1.3, 0.8), seat=(0, 0.3, 0.05), visible=(3.0, 1.7, 0.55))


# =============================================================================== 4. twin mill
def twinmill():
    car = Car(pivot_y=5)
    tail_w = {-2: 3.5, 0: 3.5, 2: 3.5, 4: 3.5, 6: 3, 8: 2.5, 10: 2}
    slices(car, "body", -2, 12, 2, lambda z: tail_w[int(math.floor(z / 2.0)) * 2], lambda z: 3,
           lambda z: 6 if z < 8 else 5, "paint")
    car.cube("body", [-1, 3, -12], [2, 3, 10], "dark")               # spine between the engines
    car.cube("body", [-3, 6, 0], [6, 2, 7], "glass")                 # canopy
    car.cube("body", [-2, 8, 1], [4, 1, 5], "glass")
    car.cube("body", [-2.5, 6, 7], [5, 2, 2], "paint")
    car.cube("body", [-4, 6, 12], [8, 1, 1], "chrome_lo")
    for sx, nm in ((1, "r"), (-1, "l")):
        x0 = 1 if sx > 0 else -6
        b = f"eng_{nm}"
        car.bone(b, "body", [sx * 3.5, 6, -7])
        car.cube(b, [x0, 4, -12], [5, 5, 10], "engine")
        car.cube(b, [x0 + 0.5, 9, -11], [1, 2, 8], "chrome")
        car.cube(b, [x0 + 3.5, 9, -11], [1, 2, 8], "chrome")
        car.cube(b, [x0 + 0.5, 9, -9], [4, 3, 4], "chrome")
        car.cube(b, [x0 + 1, 12, -8.5], [3, 2, 3], "black")
        car.cube(b, [x0, 4, -13], [5, 5, 1], "grille")
        car.cube(b, [x0 + (5 if sx > 0 else -1), 6, -10], [1, 1, 9], "chrome_lo")
    car.cube("body", [-7, 3, -14], [14, 1, 2], "orange")            # front spoiler
    car.cube("body", [-5, 2, -7.5], [10, 1, 1], "chrome_lo")
    car.cube("body", [-5, 8, 11], [10, 1, 3], "paint")             # tail wing
    car.sym("body", [3, 5, 11], [1, 3, 1], "dark")
    car.sym("body", [1.5, 4, 12], [3, 1, 1], "lamp_r")

    def decal(p):
        x, y, z = p.p
        if p.face == "top" and abs(x) < 1.2 and z > 5:
            return ORANGE
        if sidef(p) and z > -2:
            f = flame_decal(-2, 12, 3, 5.7)(p)
            if f:
                return f
        return None
    car.wheel("wheel_fl", 8.2, -6.5, 3.0, 2, "tire", "hub")
    car.wheel("wheel_fr", -8.2, -6.5, 3.0, 2, "tire", "hub")
    car.wheel("wheel_rl", 8.0, 7.5, 4.2, 4, "tire", "hub")
    car.wheel("wheel_rr", -8.0, 7.5, 4.2, 4, "tire", "hub")
    skins = dc_skins("#0fb59a", decal, 5.0)
    fx = merge({"eng_l": {"position": ["math.sin(query.life_time * 2900) * 0.12 * (1 + query.modified_move_speed * 8)", "0", "0"],
                           "rotation": ["0", "0", "math.sin(query.life_time * 2400) * 0.5"]}},
               {"eng_r": {"position": ["math.sin(query.life_time * 3100 + 2) * 0.12 * (1 + query.modified_move_speed * 8)", "0", "0"],
                          "rotation": ["0", "0", "math.sin(query.life_time * 2600) * 0.5"]}})
    anims = make_anims(car, fx=fx, bump=0.14)
    return make_spec(car, "toycar_twinmill", "Twin Piston", ("#0fb59a", "#c8ccd2"), skins, anims,
                     speed=0.76, box=(1.35, 0.9), seat=(0, 0.3, 0.2), visible=(3.0, 1.7, 0.55))


# =============================================================================== 5. dune buggy
def dunebuggy():
    car = Car(pivot_y=5)
    car.cube("body", [-5, 3, -6], [10, 2, 16], "dark")
    car.sym("body", [4, 5, -4], [1, 3, 12], "paint")
    car.cube("body", [-4, 5, -5], [8, 3, 1], "paint")
    nose = {-12: (3, 6), -10: (4, 7), -8: (4.5, 7), -6: (5, 8)}
    slices(car, "body", -12, -4, 2, lambda z: nose[int(math.floor(z / 2.0)) * 2][0], lambda z: 4,
           lambda z: nose[int(math.floor(z / 2.0)) * 2][1], "paint")
    car.cube("body", [-4, 8, -4], [8, 3, 1], "glass")
    car.cube("body", [-2, 5, -1], [4, 4, 4], "seat_o")               # bucket seat
    car.cube("body", [-2, 9, 2], [4, 3, 1], "seat_o")
    car.cube("body", [-3, 4, 6], [6, 4, 5], "engine")                # flat engine in the back
    car.cube("body", [-1.5, 8, 7.5], [3, 2, 3], "chrome")
    car.sym("body", [3, 5.5, 5], [1, 1, 8], "chrome_lo")             # pipes
    car.sym("body", [2, 5, 12], [2, 2, 2], "chrome")
    car.bone("flame_l", "body", [-3, 6, 13])
    car.cube("flame_l", [-3.5, 5.5, 14], [1, 1, 2], "flame")
    car.bone("flame_r", "body", [3, 6, 13])
    car.cube("flame_r", [2.5, 5.5, 14], [1, 1, 2], "flame")
    for z in (-3.5, 4.5):                                            # roll cage
        car.sym("body", [4, 8, z], [1, 7, 1], "chrome_lo")
        car.cube("body", [-4, 15, z], [8, 1, 1], "chrome_lo")
    car.sym("body", [4, 15, -3.5], [1, 1, 9], "chrome_lo")
    car.sym("body", [4, 5, -2], [1, 1, 8], "chrome_lo")
    car.cube("body", [-5, 3, -13], [10, 1, 1], "chrome")
    car.sym("body", [3, 5, -13], [2, 2, 1], "head")
    car.sym("body", [1.5, 16, -3.5], [2, 2, 1], "lamp_y")
    car.cube("body", [-0.5, 16, -3.5], [1, 2, 1], "lamp_y")
    car.sym("body", [6, 8, -11.5], [3, 1, 6], "paint")               # mudguards
    car.sym("body", [1, 4, 12], [2, 2, 1], "lamp_r")

    def decal(p):
        x, y, z = p.p
        if p.face == "top" and z < -4 and abs(x) < 1.3:
            return checker(p, 1.0, "#f4f4f4", "#16181c") if int(z) % 2 == 0 else "#16181c"
        if sidef(p) and z < -4:
            f = flame_decal(-12, -4, 4, 7.6)(p)
            if f:
                return f
        if sidef(p) and z >= -4 and 5 <= y < 6:
            return ORANGE
        return None
    car.wheel("wheel_fl", 7.5, -8.5, 3.6, 3, "tire", "hub")
    car.wheel("wheel_fr", -7.5, -8.5, 3.6, 3, "tire", "hub")
    car.wheel("wheel_rl", 8.5, 8.0, 4.6, 5, "tire", "hub")
    car.wheel("wheel_rr", -8.5, 8.0, 4.6, 5, "tire", "hub")
    skins = dc_skins("#8ad42a", decal, 6.0)
    skins["tire"] = tire_painter("#111316", ORANGE, "#4c5058", True, 8, 0.68, "#f4f4f4")
    fx = merge(flicker("flame_l"), flicker("flame_r", rate=3000))
    anims = make_anims(car, fx=fx, bump=0.3)
    return make_spec(car, "toycar_dunebuggy", "Sand Skipper", ("#8ad42a", ORANGE), skins, anims,
                     speed=0.7, box=(1.45, 1.0), seat=(0, 0.34, 0.05), visible=(3.0, 1.8, 0.6))


SPECS = [muscle(), hotrod(), dragster(), twinmill(), dunebuggy()]
