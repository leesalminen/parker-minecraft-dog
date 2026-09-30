"""Five LEGO-style brick toy cars (rideable, one seat). Built from studded bricks on a 4-unit stud grid."""
import math
from lib import *
from .toycars_common import *


def lego_skins(decals=None, extra=None):
    s = brick_palette(decals)
    s.update({
        "glass": glass(), "chrome": chrome(4.0), "tire": tire_painter("#16181b", "#d5d9de", "#6b7078", False, 8, 0.6),
        "hub": hubcap(chrome(-30.0)), "minihead": minihead,
        "lamp_y": lamp("#ffe680"), "lamp_r": lamp("#ff2a2a"), "lamp_b": lamp("#2a7bff"),
        "lamp_c": lamp("#39e6ff"), "lamp_w": lamp("#f4fbff"), "lamp_o": lamp("#ffab1f"),
    })
    if extra:
        s.update(extra)
    return s


def side(p):
    return p.face in ("east", "west")


def circle(z, y, cz, cy, r):
    return (z - cz) ** 2 + (y - cy) ** 2 <= r * r


def base_car(wheel_r=3, wheel_w=3, wx=9.5, wz=8.0, rear_r=None, chassis=True, y0=2):
    car = Car(pivot_y=4)
    if chassis:
        car.cube("body", [-8, y0, -12], [16, 2, 24], "dgrey_s")
    rr = rear_r or wheel_r
    car.wheel("wheel_fl", wx, -wz, wheel_r, wheel_w, "tire", "hub")
    car.wheel("wheel_fr", -wx, -wz, wheel_r, wheel_w, "tire", "hub")
    car.wheel("wheel_rl", wx, wz, rr, wheel_w, "tire", "hub")
    car.wheel("wheel_rr", -wx, wz, rr, wheel_w, "tire", "hub")
    return car


def blink(bone, on_positive=True, rate=900):
    op = ">" if on_positive else "<"
    e = f"math.sin(query.life_time * {rate}) {op} 0 ? 1 : 0.01"
    return {bone: {"scale": [e, e, e]}}


# =============================================================================== 1. police
def police():
    def blue_d(p):
        x, y, z = p.p
        if side(p) and -4 <= z < 4 and 4 <= y < 9:
            if abs(z + 0.0) < 0.5:
                return "#b9c2cc"
            if circle(z, y, -2.0, 6.5, 1.8) and abs(z + 2) + abs(y - 6.5) < 2.2:
                return "#f6c90e"
            return "#eef0ee"
        if p.face == "top" and -4 <= z < 4 and False:
            return None
        return None
    car = base_car()
    car.cube("body", [-8, 2, -14], [16, 2, 2], "white_s")
    car.cube("body", [-6, 3, -15], [12, 4, 1], "black_s")
    car.cube("body", [-6, 2, 12], [12, 2, 1], "black_s")
    car.cube("body", [-8, 2, 12], [16, 2, 2], "white_s")
    car.brick("body", 0, 0, 4, 2, 4, 4, "blue")                       # hood
    car.sym("body", [-7, 5, -13], [2, 2, 1], "lamp_y")                # headlights
    car.cube("body", [-4, 5, -13], [8, 2, 1], "black_s")               # grille
    car.cube("body", [-3, 5.5, -13.5], [6, 1, 1], "chrome")
    car.brick("body", 0, 2, 1, 2, 4, 5, "blue")                       # doors / cab walls
    car.brick("body", 3, 2, 1, 2, 4, 5, "blue")
    car.brick("body", 1, 2, 2, 1, 4, 3, "dgrey")                      # dashboard
    car.cube("body", [-2, 7, -3.5], [4, 1, 1], "black_s")
    car.brick("body", 1, 3, 2, 1, 4, 2, "dgrey")                      # seat base
    car.cube("body", [-4, 6, 2], [8, 5, 2], "black_s")                # seat back
    car.brick("body", 0, 4, 4, 2, 4, 4, "blue")                       # trunk
    car.sym("body", [-7, 5, 12], [2, 2, 1], "lamp_r")                 # tail lights
    for px, pz in ((-8, -4), (6, -4), (-8, 2), (6, 2)):               # pillars
        car.cube("body", [px, 9, pz], [2, 4, 2], "white_s")
    car.cube("body", [-6, 9, -4], [12, 4, 1], "glass")                # windscreen
    car.cube("body", [-6, 9, 3], [12, 4, 1], "glass")
    car.sym("body", [-8, 9, -2], [1, 4, 4], "glass")
    car.brick("body", 0, 2, 4, 2, 13, 2, "white")                     # roof
    car.bone("lightbar", "body", [0, 17, 0])
    car.cube("lightbar", [-6, 16, -2], [12, 1, 4], "black_s")
    car.bone("siren_r", "lightbar", [-3, 18, 0])
    car.cube("siren_r", [-5, 17, -1], [4, 2, 2], "lamp_r")
    car.bone("siren_b", "lightbar", [3, 18, 0])
    car.cube("siren_b", [1, 17, -1], [4, 2, 2], "lamp_b")
    car.cube("lightbar", [-1, 17, -1], [2, 2, 2], "white_s")
    car.minifig("body", 0, 9, 8, "blue", "dgrey", "black")             # cop standing on the boot
    skins = lego_skins({"blue": blue_d})
    fx = merge(blink("siren_r", True), blink("siren_b", False))
    anims = make_anims(car, fx=fx)
    return make_spec(car, "toycar_police", "Brick Patrol", ("#0d5fb8", "#eef0ee"), skins, anims,
                     seat=(0, 0.3, 0.05), visible=(3.0, 1.8, 0.6))


# =============================================================================== 2. fire truck
def firetruck():
    def red_d(p):
        x, y, z = p.p
        if side(p):
            if 5.5 <= y < 6.5 and z > -12:
                return "#eef0ee"
            if z >= 0 and 6.5 <= y < 10:                     # roller-shutter lockers
                if (y * 1.0) % 1.5 < 0.6:
                    return "#7d848c"
                return "#a9b0b8"
        if p.face == "front" and abs(x) < 6 and 5 <= y < 8:
            return "#d8dde2"
        return None
    car = base_car()
    car.cube("body", [-8, 2, -14], [16, 2, 2], "yellow_s")
    car.cube("body", [-6, 4, -14], [12, 1, 1], "grey_s")
    car.brick("body", 0, 0, 4, 1, 4, 5, "red")                        # engine front
    car.sym("body", [-7, 5, -13], [2, 2, 1], "lamp_y")
    car.cube("body", [-3, 4.5, -13], [6, 3, 1], "chrome")             # grille plate
    car.cube("body", [-2, 8, -12.5], [4, 1, 1], "lamp_o")
    car.brick("body", 0, 1, 1, 2, 4, 5, "red")                        # cab sides
    car.brick("body", 3, 1, 1, 2, 4, 5, "red")
    car.brick("body", 1, 1, 2, 1, 4, 2, "dgrey")                      # floor / dash
    car.brick("body", 1, 2, 2, 1, 4, 2, "dgrey")
    car.cube("body", [-4, 6, -2], [8, 5, 2], "black_s")               # seat back
    for px, pz in ((-8, -8), (6, -8), (-8, -2), (6, -2)):
        car.cube("body", [px, 9, pz], [2, 4, 2], "red_s")
    car.cube("body", [-6, 9, -8], [12, 4, 1], "glass")
    car.sym("body", [-8, 9, -6], [1, 4, 4], "glass")
    car.brick("body", 0, 1, 4, 2, 13, 2, "red")                       # cab roof
    car.brick("body", 0, 3, 4, 2, 4, 6, "red")                        # equipment body
    car.brick("body", 0, 5, 4, 1, 4, 2, "red")                        # rear step
    car.cube("body", [-8, 2, 12], [16, 2, 2], "yellow_s")
    car.sym("body", [-7, 4, 12], [2, 2, 1], "lamp_r")
    car.minifig("body", 4, 7, 10, "yellow", "black", "yellow")        # firefighter on the back step
    # hose reel + pump panel on the roof line
    car.cube("body", [-7, 11, 1], [3, 3, 8], "grey_s")
    # ladder bone (sways a little)
    car.bone("ladder", "body", [0, 11, 6])
    car.cube("ladder", [-4, 10, 2], [2, 1, 12], "grey_s")
    car.cube("ladder", [2, 10, 2], [2, 1, 12], "grey_s")
    car.cube("ladder", [-4, 11, 2], [1, 1, 12], "chrome")
    car.cube("ladder", [3, 11, 2], [1, 1, 12], "chrome")
    for i in range(6):
        car.cube("ladder", [-3, 11, 3 + 2 * i], [6, 1, 1], "grey_s")
    car.cube("ladder", [-1, 12, 12], [2, 2, 2], "yellow_s")            # nozzle
    car.bone("beacon", "body", [0, 16, -4])
    car.cube("beacon", [-2, 15, -5], [4, 2, 2], "lamp_r")
    car.cube("beacon", [-1, 15, -3], [2, 1, 1], "lamp_w")
    car.cube("body", [-1, 17, -5], [2, 1, 2], "white_s")
    skins = lego_skins({"red": red_d})
    fx = merge(blink("beacon", True, 700), {"ladder": {"rotation": ["math.sin(query.life_time * 90) * 1.5", "0", "0"]}})
    anims = make_anims(car, fx=fx)
    return make_spec(car, "toycar_firetruck", "Brick Blazer", ("#c9161f", "#f6c90e"), skins, anims,
                     seat=(0, 0.3, -0.35), visible=(3.0, 1.8, 0.6))


# =============================================================================== 3. race car
def racer():
    def white_d(p):
        x, y, z = p.p
        if side(p):
            if circle(z, y, 2.0, 5.5, 2.5):
                # roundel with a "1"
                if abs(z - 2.0) < 0.6 and 4.0 <= y <= 7.0:
                    return "#eef0ee"
                if abs(z - 1.2) < 0.6 and 6.0 <= y <= 7.0:
                    return "#eef0ee"
                return "#0d5fb8"
            if y < 4.0 + 3 and z < -3:
                return checker(p, 1.5, "#eef0ee", "#191b1f") if y >= 5.5 else None
        return None

    def red_d(p):
        x, y, z = p.p
        if p.face == "top" and abs(x) < 1.0 and z > -12:
            return "#eef0ee"
        return None
    car = Car(pivot_y=4)
    car.cube("body", [-4, 2, -12], [8, 2, 24], "dgrey_s")
    car.cube("body", [-8, 2, -14], [16, 1, 4], "yellow_s")            # front wing
    car.sym("body", [-8, 2, -14], [1, 4, 4], "red_s")
    car.brick("body", 1, 0, 2, 2, 4, 3, "red")                        # nose
    car.brick("body", 1, 2, 2, 1, 4, 4, "red")                        # dash
    car.cube("body", [-3, 8, -3.5], [6, 2, 1], "glass")
    car.cube("body", [-3, 6, -2], [6, 1, 1], "black_s")
    car.brick("body", 1, 3, 2, 1, 4, 2, "dgrey")
    car.cube("body", [-3, 6, 2], [6, 4, 2], "black_s")                 # seat back
    car.brick("body", 0, 2, 1, 3, 4, 3, "white")                      # side pods
    car.brick("body", 3, 2, 1, 3, 4, 3, "white")
    car.brick("body", 1, 4, 2, 2, 4, 6, "red")                        # engine cover
    car.cube("body", [-2, 11, 4], [4, 4, 4], "dgrey_s")               # airbox
    car.cube("body", [-1, 12, 3.5], [2, 2, 1], "black_s")
    car.cube("body", [-1, 10, 9], [2, 3, 2], "dgrey_s")
    car.cube("body", [-8, 12, 9], [16, 1, 5], "white_s")              # rear wing
    car.cube("body", [-8, 13, 9], [16, 1, 2], "blue_s")
    car.sym("body", [-8, 8, 9], [1, 6, 5], "red_s")
    car.sym("body", [-7, 5, 12], [2, 2, 1], "lamp_r")
    car.cube("body", [-2, 5, 12], [4, 2, 1], "lamp_o")
    for z in (-7, 8):                                                  # wishbones
        car.sym("body", [4, 3, z - 0.5], [4, 1, 1], "dgrey_s")
    car.wheel("wheel_fl", 9.5, -7, 3, 3, "tire", "hub")
    car.wheel("wheel_fr", -9.5, -7, 3, 3, "tire", "hub")
    car.wheel("wheel_rl", 10.0, 8, 4, 4, "tire", "hub")
    car.wheel("wheel_rr", -10.0, 8, 4, 4, "tire", "hub")
    skins = lego_skins({"white": white_d, "red": red_d})
    fx = {"body": {"rotation": ["0", "0", "math.sin(query.life_time * 60) * 0.3"]}}
    anims = make_anims(car, fx=fx, bump=0.12)
    return make_spec(car, "toycar_racer", "Brick Racer", ("#c9161f", "#f6c90e"), skins, anims,
                     speed=0.8, box=(1.4, 0.85), seat=(0, 0.28, 0.0), visible=(3.0, 1.6, 0.5))


# =============================================================================== 4. monster truck
def monster():
    def orange_d(p):
        x, y, z = p.p
        if side(p) and z < 4 and 9 <= y < 15:
            d = flame_decal(-12, 3, 9, 14.5)(p)
            if d:
                return d
        if p.face in ("front",) and z < -12 and abs(x) < 6 and 10 <= y < 12:
            return "#191b1f"
        return None
    car = Car(pivot_y=8)
    car.cube("body", [-6, 7, -12], [12, 2, 24], "dgrey_s")             # frame
    for z in (-7, 7):
        car.cube("body", [-8, 5, z - 1], [16, 2, 2], "dgrey_s")       # axles
        car.sym("body", [5, 7, z - 0.5], [2, 3, 1], "yellow_s")        # shocks
        car.sym("body", [6, 6, z - 1.5], [2, 2, 3], "chrome")
    for name, x, z in (("wheel_fl", 10.5, -7), ("wheel_fr", -10.5, -7), ("wheel_rl", 10.5, 7), ("wheel_rr", -10.5, 7)):
        car.wheel(name, x, z, 5, 5, "tire", "hub")
    car.cube("body", [-8, 6, -14], [16, 3, 2], "black_s")             # bumper
    car.cube("body", [-2, 7, -15], [4, 2, 1], "yellow_s")
    car.cube("body", [-6, 9, -13], [12, 1, 1], "chrome")
    car.brick("body", 0, 0, 4, 2, 9, 4, "orange")                     # hood
    car.sym("body", [-7, 10, -13], [2, 2, 1], "lamp_y")
    car.cube("body", [-4, 10, -13], [8, 2, 1], "black_s")
    car.cube("body", [-2, 13, -8], [4, 2, 3], "black_s")              # hood scoop
    car.cube("body", [-1, 15, -7], [2, 1, 1], "lamp_o")
    car.brick("body", 0, 2, 1, 2, 9, 5, "orange")
    car.brick("body", 3, 2, 1, 2, 9, 5, "orange")
    car.brick("body", 1, 2, 2, 1, 9, 3, "dgrey")
    car.brick("body", 1, 3, 2, 1, 9, 2, "dgrey")
    car.cube("body", [-4, 11, 2], [8, 5, 2], "black_s")
    for px, pz in ((-8, -4), (6, -4), (-8, 2), (6, 2)):
        car.cube("body", [px, 14, pz], [2, 4, 2], "black_s")
    car.cube("body", [-6, 14, -4], [12, 4, 1], "glass")
    car.cube("body", [-6, 14, 3], [12, 4, 1], "glass")
    car.sym("body", [-8, 14, -2], [1, 4, 4], "glass")
    car.brick("body", 0, 2, 4, 2, 18, 2, "black")
    car.brick("body", 0, 4, 4, 2, 9, 3, "orange")                     # bed
    # roll bar + light bar
    car.sym("body", [-7, 12, 9], [1, 7, 1], "chrome")
    car.cube("body", [-7, 19, 9], [14, 1, 1], "chrome")
    car.cube("body", [-7, 18, 5], [1, 1, 5], "chrome")
    car.cube("body", [6, 18, 5], [1, 1, 5], "chrome")
    for i in range(4):
        car.cube("body", [-6 + 3.5 * i, 20, 8.5], [2, 2, 2], "lamp_y")
    car.bone("stack_l", "body", [-6, 12, 5])
    car.cube("stack_l", [-7, 12, 4], [2, 8, 2], "chrome")
    car.cube("stack_l", [-7.5, 20, 3.5], [3, 1, 3], "black_s")
    car.bone("stack_r", "body", [6, 12, 5])
    car.cube("stack_r", [5, 12, 4], [2, 8, 2], "chrome")
    car.cube("stack_r", [4.5, 20, 3.5], [3, 1, 3], "black_s")
    car.cube("body", [-8, 6, 12], [16, 3, 2], "black_s")
    car.sym("body", [-7, 10, 12], [2, 2, 1], "lamp_r")
    skins = lego_skins({"orange": orange_d})
    skins["tire"] = tire_painter("#16181b", "#e8b90f", "#4a4f57", True, 8, 0.5)
    fx = merge({"stack_l": {"rotation": ["math.sin(query.life_time * 900) * 3", "0", "0"]}},
               {"stack_r": {"rotation": ["math.sin(query.life_time * 900 + 90) * 3", "0", "0"]}})
    anims = make_anims(car, fx=fx, bump=0.3)
    return make_spec(car, "toycar_monster", "Brick Crusher", ("#f26a12", "#191b1f"), skins, anims,
                     hp=36, speed=0.6, box=(1.4, 1.3), seat=(0, 0.6, 0.0), visible=(3.2, 2.2, 0.7))


# =============================================================================== 5. space rover
def rover():
    def white_d(p):
        x, y, z = p.p
        if side(p) and 5 <= y < 6.2:
            return "#f26a12"
        if side(p) and circle(z, y, -8.0, 6.8, 1.4) and z < -6:
            return "#0d5fb8"
        return None

    def solar(p):
        x, y, z = p.p
        c = mix("#0e2a5c", "#1c56a8", noise3(x, y, z, 61, 2.0))
        if (z % 2.0) < 0.6 or (y % 2.0) < 0.6:
            c = "#b9c8dc"
        if p.face in ("top", "bottom"):
            c = "#8a96a8"
        return c
    car = base_car(4, 4, 10, 8.0, chassis=False)
    car.cube("body", [-8, 3, -12], [16, 2, 24], "grey_s")
    car.brick("body", 1, 0, 2, 2, 5, 3, "white")                       # nose
    car.sym("body", [-3, 6, -13], [2, 1, 1], "lamp_c")
    car.cube("body", [-4, 5, -13], [8, 1, 1], "orange_s")
    car.brick("body", 0, 2, 1, 2, 5, 4, "white")
    car.brick("body", 3, 2, 1, 2, 5, 4, "white")
    car.brick("body", 1, 2, 2, 1, 5, 3, "grey")
    car.brick("body", 1, 3, 2, 1, 5, 2, "dgrey")
    car.cube("body", [-4, 7, 2], [8, 5, 2], "dgrey_s")
    for px, pz in ((-8, -4), (7, -4), (-8, 3), (7, 3)):                # roll frame
        car.cube("body", [px, 9, pz], [1, 7, 1], "chrome")
    car.cube("body", [-8, 15, -4], [16, 1, 1], "chrome")
    car.cube("body", [-8, 15, 3], [16, 1, 1], "chrome")
    car.sym("body", [-8, 15, -3], [1, 1, 6], "chrome")
    car.cube("body", [-5, 16, -4], [10, 1, 1], "lamp_w")
    car.brick("body", 0, 4, 4, 2, 5, 4, "grey")                        # cargo box
    car.sym("body", [8, 9, 4], [1, 7, 8], "solar_")                    # folded solar wings
    car.sym("body", [8, 8, 5], [1, 1, 6], "dgrey_s")
    car.bone("mast", "body", [0, 10, 7])
    car.cube("mast", [-1, 10, 6], [2, 6, 2], "chrome")
    car.bone("dish", "mast", [0, 16, 7])
    car.cube("dish", [-1, 16, 6], [2, 1, 2], "grey_s")
    car.cube("dish", [-2, 17, 5], [4, 1, 4], "white_s")
    car.cube("dish", [-3, 18, 4], [6, 1, 6], "white_s")
    car.cube("dish", [-4, 19, 3], [8, 1, 8], "white_s")
    car.cube("dish", [-0.5, 20, 6.5], [1, 3, 1], "chrome")
    car.cube("dish", [-1, 23, 6], [2, 1, 2], "lamp_c")
    car.bone("antenna", "body", [-7, 16, -3])
    car.cube("antenna", [-7.5, 16, -3.5], [1, 6, 1], "chrome")
    car.cube("antenna", [-7.5, 22, -3.5], [1, 1, 2], "orange_s")
    car.sym("body", [-7, 7, 12], [2, 2, 1], "lamp_r")
    car.sym("body", [-7, 5.5, -14.5], [2, 1, 1], "lamp_o")
    skins = lego_skins({"white": white_d}, {"solar_": solar})
    fx = merge({"dish": {"rotation": ["0", "query.life_time * 60", "0"]}},
               {"antenna": {"rotation": ["math.sin(query.life_time * 300) * 6", "0", "math.sin(query.life_time * 380) * 4"]}})
    anims = make_anims(car, fx=fx)
    return make_spec(car, "toycar_rover", "Brick Rover", ("#eef0ee", "#f26a12"), skins, anims,
                     speed=0.62, box=(1.4, 1.0), seat=(0, 0.33, 0.0), visible=(3.0, 1.9, 0.6))


SPECS = [police(), firetruck(), racer(), monster(), rover()]
