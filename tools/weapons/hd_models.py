"""High-detail held models for the realistic (military) weapons.

Drawn at twice the usual density: 1 unit = 1/32 block.  write_model() puts these cubes on
an `hd` child bone that the shared `animation.gx_weapon.hd` scales by 0.5, so the hand
origin and every shared hold pose stay exactly as they are for the other 53 weapons.

Same axis convention as model.py: muzzle toward -Z, receiver bottom at y = 0, pistol grip
hanging below the origin (the hand).  Every model is built from real-proportion parts
(receivers, rails, optics, raked grips, curved magazines, stocks) with material skins
instead of emissive panels.

Forms may return {"cubes": [...], "spin": [...], "spin_pivot": [x, y, z]}; spin cubes go on
a child bone that rotates while the trigger is held (minigun barrels).
"""
import math

from lib import glow, shade, mix, rgb, noise3

HD = {}


def hd(name):
    def deco(fn):
        HD[name] = fn
        return fn
    return deco


# ------------------------------------------------------------------ primitives
def R(x, y, z, w, h, d, skin, rot=None, pivot=None):
    """Box with its min corner at (x, y, z); optional X-axis rotation (degrees) about pivot.

    Bedrock X rotation maps (y, z) -> (y cos a + z sin a, -y sin a + z cos a) about the pivot
    (vanilla cow: its body is authored upright and +90 lays it down with the udder beneath),
    so a positive angle swings a part hanging below the pivot back toward +z.
    """
    c = {"o": [x, y, z], "s": [w, h, d], "skin": skin}
    if rot:
        c["rot"], c["pivot"] = rot, pivot
    return c


def C(w, h, d, y, z, skin, x=0.0, rot=None, pivot=None):
    """Box w*h*d centred on x, bottom at y, front (muzzle-side) face at z."""
    return R(x - w / 2, y, z, w, h, d, skin, rot, pivot)


def hang(w, d, top, zc, lengths, angles, skin, x=0.0):
    """Chain of boxes hanging down from (top, zc), each rotated by its own angle about the
    bottom-centre of the previous one: smooth raked grips and curved magazines."""
    out, y, z = [], top, zc
    for h, a in zip(lengths, angles):
        out.append(C(w, h, d, y - h, z - d / 2, skin, x=x, rot=a, pivot=[x, y, z]))
        r = math.radians(a)
        y, z = y - h * math.cos(r), z + h * math.sin(r)
    return out, (y, z)


def barrel(z_front, z_back, dia, y, skin="steel"):
    return C(dia, dia, z_back - z_front, y, z_front, skin)


def grip(z_top, y_top, h, d=4, w=3, rake=1.0, step=3, skin="polymer"):
    """Pistol grip hanging from y_top at z_top (its front), raked back by about
    atan(rake / step), with a flared heel at the bottom."""
    a = round(math.degrees(math.atan2(rake, step)), 1)
    body, (y, z) = hang(w, d, y_top, z_top + d / 2, [h], [a], skin)
    return body + [C(w + 1, 1, d + 1, y - 1, z - (d + 1) / 2, skin, rot=a, pivot=[0, y, z])]


def mag(z_front, y_top, h, d=5, w=3, curve=0.0, step=3, skin="steel"):
    """Box magazine; `curve` > 0 bends it forward (toward the muzzle) as it drops."""
    n = max(1, round(h / 4)) if curve else 1
    seg = [h // n + (1 if i < h % n else 0) for i in range(n)]
    angles = [-curve * 40 * (i + 0.5) / n for i in range(n)]
    body, (y, z) = hang(w, d, y_top, z_front + d / 2, seg, angles, skin)
    a = angles[-1]
    return body + [C(w + 1, 1, d + 1, y - 1, z - (d + 1) / 2, "polymer", rot=a, pivot=[0, y, z])]


def trigger(z_front, y, length=6):
    """Trigger guard loop + blade under a receiver whose bottom is at y."""
    return [C(1, 1, length, y - 4, z_front, "steel"),
            C(1, 3, 1, y - 3, z_front, "steel"),
            C(1, 3, 1, y - 3.5, z_front + length / 2 - 0.5, "steel")]


def rail(z0, z1, y, w=3):
    return C(w, 1, z1 - z0, y, z0, "rail")


def scope(z0, z1, y, tube=4, bell=6, eye=5):
    """Rifle scope sitting on a rail whose top is at y; objective bell at the front (z0)."""
    L = z1 - z0
    yc = y + 3 + bell / 2
    zm = z0 + L / 2
    c = [
        C(bell, bell, 5, yc - bell / 2, z0, "steel"),                       # objective bell
        C(bell - 2, bell - 2, 1, yc - (bell - 2) / 2, z0 - 1, "glass"),     # front lens
        C(bell - 1, bell - 1, 2, yc - (bell - 1) / 2, z0 + 5, "steel"),     # taper
        C(tube, tube, L - 12, yc - tube / 2, z0 + 7, "steel"),              # main tube
        C(eye, eye, 5, yc - eye / 2, z1 - 5, "steel"),                      # ocular
        C(eye - 2, eye - 2, 1, yc - (eye - 2) / 2, z1, "glass"),            # rear lens
        C(3, 2, 3, yc + tube / 2, zm - 1.5, "aluminum"),                   # elevation turret
        R(tube / 2, yc - 1.5, zm - 1.5, 2, 3, 3, "aluminum"),               # windage turret
    ]
    for rz in (z0 + 8, z1 - 9):                                           # rings + mounts
        c.append(C(tube + 2, 2, 2, yc - tube / 2 - 1, rz, "gunmetal"))
        c.append(C(3, int(max(1, yc - tube / 2 - 1 - y)), 2, y, rz, "gunmetal"))
    return c


def red_dot(z, y):
    """Tube red-dot on a rail whose top is at y."""
    return [C(3, 1, 4, y, z + 1, "gunmetal"),
            C(4, 4, 6, y + 1, z, "gunmetal"),
            C(3, 3, 1, y + 1.5, z - 1, "glass"),
            C(1, 1, 1, y + 2.5, z + 5, "red"),
            C(2, 1, 2, y + 5, z + 2, "aluminum")]


def holo(z, y):
    """Holographic sight: open window with side plates and a glass pane."""
    return [C(5, 1, 7, y, z, "gunmetal"),
            R(-2.5, y + 1, z, 1, 5, 7, "gunmetal"), R(1.5, y + 1, z, 1, 5, 7, "gunmetal"),
            C(5, 1, 7, y + 6, z, "gunmetal"),
            C(3, 4, 1, y + 1, z + 1, "glass"),
            C(1, 1, 1, y + 3, z + 5, "red")]


def acog(z, y):
    """Short fat prism scope."""
    return [C(3, 2, 6, y, z + 1, "gunmetal"),
            C(5, 5, 8, y + 2, z, "gunmetal"),
            C(6, 6, 3, y + 1.5, z - 3, "gunmetal"),
            C(4, 4, 1, y + 2.5, z - 4, "glass"),
            C(3, 3, 1, y + 3, z + 8, "glass"),
            C(1, 2, 3, y + 7, z + 1, "red")]


def bipod(z, y):
    """Bipod under a barrel whose bottom is at y."""
    return [C(4, 2, 3, y - 2, z, "steel"),
            C(1, 10, 1, y - 12, z + 1, "steel", x=-2), C(1, 10, 1, y - 12, z + 1, "steel", x=2),
            C(2, 1, 2, y - 13, z + 0.5, "rubber", x=-2), C(2, 1, 2, y - 13, z + 0.5, "rubber", x=2)]


def stock_m4(z, y):
    return [C(3, 3, 10, y + 3.5, z, "gunmetal"),                  # buffer tube
            C(4, 6, 9, y + 2, z + 4, "polymer"),
            C(4, 5, 4, y - 3, z + 9, "polymer"),
            C(4, 11, 1, y - 3, z + 13, "rubber")]


def stock_fixed(z, y, skin="polymer", butt="steel", length=18):
    """Fixed rifle stock dropping from the receiver line to a butt plate."""
    s = length // 3
    return [C(4, 6, s, y + 1, z, skin),
            C(4, 8, s, y - 1, z + s, skin),
            C(4, 10, length - 2 * s, y - 3, z + 2 * s, skin),
            C(4, 10, 1, y - 3, z + length, butt)]


# ------------------------------------------------------------------ forms
@hd("pistol")
def _pistol(m):
    """M9-style service pistol: open-top slide, alloy frame, raked grip."""
    c = [
        C(4, 4, 22, 2, -18, "steel"),                 # slide
        C(2, 2, 3, 3, -20, "bore"),                   # barrel crown
        C(1, 1, 1, 6, -17, "steel"),                  # front sight
        C(3, 1, 2, 6, 1, "steel"),                    # rear sight
        R(2, 3, -2, 1, 2, 3, "bore"),                 # ejection port
        C(4, 2, 18, 0, -14, "gunmetal"),              # frame / dust cover
        C(2, 2, 2, 4, 4, "steel"),                    # hammer
        C(5, 1, 3, 5, -1, "steel"),                   # safety / decocker
    ]
    c += grip(-1, 0, 12, d=6, w=4, rake=1.2, step=3, skin="polymer")
    c += [C(5, 1, 7, -13, 3, "gunmetal")]             # mag baseplate
    c += trigger(-8, 0, 6)
    return c


@hd("revolver")
def _revolver(m):
    """Large-frame .44 double-action with full-lug barrel."""
    L = m.get("barrel", 16)
    c = [
        C(4, 7, 11, 0, -6, "chrome"),                 # frame
        C(6, 6, 7, 0.5, -5.5, "cylinder"),            # cylinder
        C(3, 3, L, 3.5, -6 - L, "chrome"),            # barrel
        C(3, 2, L, 1.5, -6 - L, "chrome"),            # ejector-rod shroud (full lug)
        C(2, 1, L, 6.5, -6 - L, "chrome"),            # top rib
        C(2, 2, 1, 4, -7 - L, "bore"),                # crown
        C(1, 2, 2, 7.5, -5 - L, "red"),               # red ramp insert
        C(3, 1, 2, 7, 2, "steel"),                    # rear sight
        C(2, 3, 2, 5, 4, "steel"),                    # hammer spur
    ]
    c += grip(0, 0, 12, d=5, w=4, rake=1.6, step=3, skin="wood")
    c += trigger(-4, 0, 6)
    return c


@hd("smg")
def _smg(m):
    """MP5-style roller-delayed SMG: slim receiver, cocking tube, curved mag, slim stock."""
    c = [
        C(4, 6, 24, 0, -14, "steel"),                 # receiver
        C(3, 2, 14, 6, -14, "steel"),                 # cocking tube
        R(-3, 5, -13, 1, 1, 3, "steel"),              # cocking handle
        C(5, 4, 9, -1, -22, "polymer"),               # handguard
        barrel(-28, -22, 2, 3),
        C(3, 3, 3, 2.5, -31, "bore"),                 # tri-lug muzzle
        C(3, 4, 2, 5, -20, "steel"),                  # front sight hood
        C(1, 2, 1, 6, -19.5, "steel"),
        C(3, 3, 2, 6, 5, "steel"),                    # drum rear sight
        C(4, 3, 7, -3, -6, "polymer"),                # trigger housing
    ]
    c += mag(-11, -1, 12, d=4, w=3, curve=0.35, skin="steel")
    c += grip(2, -3, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-3, -3, 5)
    c += [C(3, 3, 4, 2, 10, "steel"),                 # stock
          C(1, 2, 10, 4, 12, "steel", x=-1.5), C(1, 2, 10, 4, 12, "steel", x=1.5),
          C(4, 9, 2, -2, 21, "rubber")]
    return c


@hd("tommy")
def _tommy(m):
    """Thompson M1928: finned barrel, Cutts compensator, drum, wood furniture."""
    c = [
        C(5, 6, 20, 0, -12, "steel"),                 # receiver
        C(2, 2, 2, 6, -7, "steel"),                   # cocking knob
        C(3, 3, 2, 6, 3, "steel"),                    # Lyman rear sight
        barrel(-30, -12, 3, 2),
        C(4, 4, 4, 1.5, -34, "bore"),                 # Cutts compensator
        C(1, 2, 1, 5.5, -33, "steel"),                # front sight
        C(4, 10, 5, -10, -24, "wood"),                # vertical foregrip
        C(4, 2, 6, -1, -25, "steel"),                 # foregrip mount
        C(4, 12, 12, -12, -12, "steel"),              # 50-round drum
        C(5, 9, 9, -10.5, -10.5, "drum"),             # drum face
    ]
    for k in range(6):
        c.append(C(5, 5, 1, 1, -28 + 2 * k, "steel"))  # cooling fins
    c += grip(2, 0, 11, d=4, w=3, rake=1.0, skin="wood")
    c += trigger(-2, 0, 5)
    c += stock_fixed(8, 0, skin="wood", butt="steel", length=18)
    return c


@hd("ar15")
def _ar15(m):
    """AR-15 family (M4A1 / M16A4): options barrel, handguard, stock, optic."""
    hg, bl = m.get("handguard", 12), m.get("barrel", 5)
    zf = -7 - hg
    c = [
        C(4, 4, 14, -1, -6, "gunmetal"),              # lower receiver
        C(4, 4, 16, 3, -7, "gunmetal"),               # upper receiver
        R(2, 4, -4, 1, 2, 5, "polymer"),              # ejection port cover
        R(2, 4, 2, 1, 2, 2, "steel"),                 # forward assist
        C(2, 1, 2, 6, 9, "polymer"),                  # charging handle
        rail(-7, 9, 7),
        C(4, 3, 6, -4, -8, "gunmetal"),               # magwell
        barrel(zf - bl, zf, 2, 4),
        C(3, 3, 4, 3.5, zf - bl - 4, "bore"),         # birdcage flash hider
    ]
    if m.get("hg_style", "quad") == "quad":
        c += [C(6, 6, hg, 2, zf, "vent"), rail(zf, -7, 8),
              R(3, 4, zf, 1, 2, hg, "rail"), R(-4, 4, zf, 1, 2, hg, "rail"),
              C(1, 3, 1, 9, zf + 1, "steel")]         # folding front sight
    else:
        c += [C(6, 6, hg, 2, zf, "ribbed"),
              C(3, 3, 3, 3.5, zf - 3, "steel"),       # A-frame front sight base
              C(1, 5, 1, 6.5, zf - 2, "steel")]
    c += mag(-7.5, -4, 12, d=5, w=3, curve=0.3, skin="aluminum")
    c += grip(2, -1, 11, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-2, -1, 4)
    c += stock_m4(9, 0) if m.get("stock", "m4") == "m4" else stock_fixed(9, 1, "polymer", "steel", 18)
    optic = m.get("optic", "holo")
    if optic == "holo":
        c += holo(-4, 8)
    elif optic == "acog":
        c += acog(-6, 8)
    elif optic == "red_dot":
        c += red_dot(-3, 8)
    return c


@hd("ak")
def _ak(m):
    """AK-47: stamped receiver, wood furniture, banana mag, slant brake."""
    c = [
        C(5, 5, 20, 0, -9, "steel"),                  # receiver
        C(4, 1, 18, 5, -8, "steel"),                  # dust cover
        C(3, 2, 3, 5, -12, "steel"),                  # rear sight block
        C(5, 4, 11, 1, -21, "wood"),                  # lower handguard
        C(4, 2, 9, 5, -21, "wood"),                   # upper handguard over gas tube
        C(3, 3, 2, 5, -23, "steel"),                  # gas block
        C(2, 2, 3, 6, -26, "steel"),                  # gas tube tip
        barrel(-35, -21, 2, 3),
        C(3, 3, 2, 2.5, -32, "steel"),                # front sight block
        C(1, 3, 1, 5.5, -32, "steel"),                # front post
        C(3, 3, 3, 2.5, -38, "bore"),                 # slant brake
        R(2.5, 3, -3, 2, 1, 2, "steel"),              # charging handle
        R(2.5, 1, -2, 1, 1, 7, "steel"),              # selector lever
    ]
    c += mag(-8, 0, 16, d=5, w=3, curve=0.55, skin="bakelite")
    c += grip(3, 0, 11, d=4, w=3, rake=1.1, skin="wood")
    c += trigger(-2, 0, 5)
    c += stock_fixed(11, 0, skin="wood", butt="steel", length=18)
    return c


@hd("scar")
def _scar(m):
    """SCAR-H: monolithic FDE upper, full-length rail, folding stock, 7.62 box mag."""
    c = [
        C(5, 6, 26, 1, -16, "tan"),                   # upper
        rail(-16, 10, 7),
        R(2.5, 3, -16, 1, 2, 10, "rail"), R(-3.5, 3, -16, 1, 2, 10, "rail"),
        C(4, 3, 12, -2, -4, "tan"),                   # lower
        barrel(-30, -16, 3, 3),
        C(3, 3, 3, 3, -33, "bore"),                   # flash hider
        R(-3.5, 4, -12, 1, 1, 3, "steel"),            # charging handle
        C(4, 3, 7, -1, -10, "tan"),                   # magwell
        C(4, 6, 10, 0, 10, "tan"),                    # stock
        C(3, 2, 7, 6, 12, "polymer"),                 # cheek riser
        C(4, 10, 2, -3, 20, "rubber"),                # butt pad
        C(1, 3, 1, 8, -15, "steel"),                  # folded front sight
    ]
    c += mag(-9.5, -1, 11, d=5, w=3, curve=0.1, skin="polymer")
    c += grip(2, -2, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-3, -2, 4)
    c += red_dot(-3, 8)
    return c


@hd("dmr")
def _dmr(m):
    """M14 EBR: chassis, long receiver, muzzle brake, 4x scope, adjustable stock."""
    c = [
        C(6, 5, 30, -2, -18, "polymer"),              # chassis
        C(5, 5, 22, 2, -10, "steel"),                 # receiver
        rail(-18, 12, 7),
        R(3, 3, -18, 1, 2, 12, "rail"), R(-4, 3, -18, 1, 2, 12, "rail"),
        barrel(-34, -18, 3, 3),
        C(4, 4, 4, 2.5, -38, "bore"),                 # muzzle brake
        R(2.5, 4, -2, 2, 1, 3, "steel"),              # op-rod handle
        C(3, 3, 10, 1, 12, "gunmetal"),               # stock tube
        C(4, 8, 6, -3, 20, "polymer"),                # stock body
        C(3, 2, 6, 5, 19, "polymer"),                 # cheek riser
        C(4, 8, 1, -3, 26, "rubber"),
    ]
    c += mag(-7, -2, 10, d=5, w=3, curve=0.1, skin="steel")
    c += grip(3, -2, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-2, -2, 5)
    c += scope(-12, 6, 8, tube=4, bell=6, eye=5)
    c += bipod(-24, -2)
    return c


@hd("bolt_sniper")
def _bolt_sniper(m):
    """M24 / Mosin: one-piece stock, bolt action, long barrel.  Options: stock skin, scope."""
    wood = m.get("stock_skin", "od")
    bl = m.get("barrel", 24)
    c = [
        C(5, 4, 26, -1, -26, wood),                   # forend
        C(4, 5, 16, 2, -10, "steel"),                 # action
        barrel(-26 - bl, -10, 3, 3.5),
        C(3, 3, 2, 3.5, -28 - bl, "bore"),            # crown
        R(2, 5, 4, 3, 1, 1, "steel"),                 # bolt handle
        R(4, 3.5, 3.5, 2, 2, 2, "steel"),             # bolt knob
        C(5, 5, 10, -1, 0, wood),                     # wrist
        C(5, 7, 8, -3, 10, wood),                     # comb
        C(5, 9, 6, -5, 18, wood),                     # butt
        C(5, 9, 1, -5, 24, "rubber" if wood == "od" else "steel"),
    ]
    if m.get("bands"):
        c += [C(6, 6, 1, -1.5, -24, "steel"), C(6, 6, 1, -1.5, -12, "steel"),
              C(4, 2, 18, 3, -28, wood),              # upper handguard
              C(3, 3, 2, 6.5, -28 - bl, "steel")]     # hooded front sight
    c += grip(4, -1, 8, d=5, w=4, rake=1.3, skin=wood)
    c += trigger(-1, -1, 5)
    if m.get("scope", "long") == "long":
        c += scope(-14, 6, 7, tube=4, bell=6, eye=5)
    else:
        c += scope(-10, 4, 7, tube=3, bell=4, eye=4)
    if m.get("bipod"):
        c += bipod(-22, -1)
    return c


@hd("anti_materiel")
def _barrett(m):
    """M82: slab receiver, fluted heavy barrel, double-chamber brake, monopod, bipod."""
    c = [
        C(6, 8, 30, 0, -18, "gunmetal"),              # receiver
        rail(-18, 10, 8),
        barrel(-44, -18, 4, 4),
        C(6, 6, 10, 3, -28, "gunmetal"),              # barrel shroud / spring housing
        C(8, 5, 2, 3.5, -50, "bore"),                 # brake front chamber
        C(4, 4, 1, 4, -48, "steel"),
        C(8, 5, 2, 3.5, -47, "steel"),                # brake rear chamber
        C(4, 7, 9, -6, -12, "steel"),                 # box mag
        C(6, 8, 10, 0, 12, "gunmetal"),               # stock body
        C(2, 6, 2, -6, 18, "gunmetal"),               # monopod
        C(6, 10, 2, -1, 22, "rubber"),                # butt pad
        C(4, 2, 8, 8, 12, "polymer"),                 # cheek rest
        C(2, 2, 12, 11, -14, "steel"),                # carry handle
        C(2, 3, 2, 8, -14, "steel"), C(2, 3, 2, 8, -4, "steel"),
    ]
    c += grip(3, 0, 11, d=5, w=4, rake=1.2, skin="polymer")
    c += trigger(-2, 0, 5)
    c += scope(-12, 8, 9, tube=5, bell=7, eye=6)
    c += [C(6, 2, 3, 1, -32, "steel"),
          C(1, 12, 1, -10, -31, "steel", x=-3), C(1, 12, 1, -10, -31, "steel", x=3),
          C(3, 1, 2, -11, -31.5, "rubber", x=-3), C(3, 1, 2, -11, -31.5, "rubber", x=3)]
    return c


@hd("pump_shotgun")
def _pump(m):
    """Remington 870: receiver, vent-rib barrel, mag tube, pump forend, wood stock."""
    c = [
        C(5, 6, 14, 0, -8, "steel"),                  # receiver
        R(2.5, 2, -6, 1, 3, 5, "bore"),               # ejection port
        barrel(-36, -8, 3, 3.5),
        C(1, 1, 26, 6.5, -35, "steel"),               # vent rib
        C(1, 1, 1, 7.5, -35, "brass"),                # bead sight
        C(3, 3, 1, 3.5, -37, "bore"),                 # crown
        barrel(-32, -8, 3, 0.5, "steel"),             # magazine tube
        C(3, 3, 1, 0.5, -33, "steel"),                # mag cap
        C(5, 5, 10, -0.5, -24, "pump"),               # pump forend
    ]
    c += grip(3, 0, 10, d=4, w=3, rake=1.2, skin="wood")
    c += trigger(-3, 0, 5)
    c += stock_fixed(6, 0, skin="wood", butt="rubber", length=20)
    return c


@hd("auto_shotgun")
def _aa12(m):
    """AA-12: slab receiver, carry handle, drum, integrated stock."""
    c = [
        C(6, 8, 24, 0, -16, "od"),                    # receiver
        C(6, 4, 10, -3, -16, "vent"),                 # lower handguard
        barrel(-30, -16, 3, 4),
        C(4, 4, 3, 3.5, -33, "bore"),                 # muzzle
        C(2, 2, 14, 10, -12, "polymer"),              # carry handle
        C(2, 2, 2, 8, -12, "polymer"), C(2, 2, 2, 8, 0, "polymer"),
        C(1, 2, 1, 12, -11, "steel"),                 # front sight
        C(4, 12, 12, -13, -8, "polymer"),             # 20-round drum
        C(6, 9, 9, -11.5, -6.5, "drum"),
        C(6, 8, 14, 0, 8, "od"),                      # stock
        C(6, 10, 2, -2, 22, "rubber"),
    ]
    c += grip(5, 0, 11, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(1, 0, 4)
    return c


@hd("lmg")
def _lmg(m):
    """M249 SAW: feed-tray cover, belt, 200-round pouch, barrel handle, bipod."""
    c = [
        C(6, 7, 20, 0, -12, "gunmetal"),              # receiver
        C(6, 2, 12, 7, -10, "gunmetal"),              # feed cover
        rail(-10, 2, 9),
        C(6, 4, 10, -1, -22, "polymer"),              # handguard
        barrel(-40, -12, 3, 3.5),
        C(3, 3, 4, 3.5, -44, "bore"),                 # flash hider
        C(2, 1, 8, 9, -26, "polymer"),                # barrel carry handle
        C(1, 3, 1, 6.5, -25, "steel"), C(1, 3, 1, 6.5, -19, "steel"),
        C(1, 4, 1, 6.5, -39, "steel"),                # front sight
        C(5, 11, 10, -11, -12, "canvas"),             # 200-round pouch
        R(-5, 4, -8, 2, 2, 7, "belt"),                # belt into the feed tray
        C(4, 6, 14, -1, 8, "polymer"),                # stock
        C(4, 9, 2, -3, 22, "rubber"),
    ]
    c += grip(3, 0, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-1, 0, 4)
    c += bipod(-34, 3.5)
    return c


@hd("minigun")
def _minigun(m):
    """M134: six-barrel cluster on a spinning bone, motor housing, feed chute, handles."""
    yc = 2.0                                          # barrel cluster axis (y)
    spin = []
    for k in range(6):
        a = math.radians(60 * k)
        x, y = 3 * math.cos(a), yc + 3 * math.sin(a)
        spin.append(C(2, 2, 34, y - 1, -46, "steel", x=x))
        spin.append(C(2, 2, 1, y - 1, -47, "bore", x=x))
    spin += [C(9, 9, 1, yc - 4.5, -42, "gunmetal"), C(9, 9, 1, yc - 4.5, -28, "gunmetal")]
    c = [
        C(10, 10, 10, yc - 5, -16, "gunmetal"),       # rotor housing
        C(8, 8, 12, yc - 4, -6, "steel"),             # motor
        C(6, 6, 2, yc - 3, 6, "aluminum"),            # motor end cap
        C(2, 2, 14, 9, -14, "polymer"),               # carry handle
        C(2, 3, 2, 7, -14, "polymer"), C(2, 3, 2, 7, -2, "polymer"),
        R(-8, -2, -12, 3, 3, 14, "belt"),             # feed chute
        C(8, 2, 2, -6, 7, "steel"),                   # rear spade cross bar
        C(2, 8, 2, -12, 7, "polymer", x=-4), C(2, 8, 2, -12, 7, "polymer", x=4),
    ]
    c += grip(1, -2, 10, d=4, w=3, rake=0.8, skin="polymer")
    c += trigger(-3, -2, 4)
    return {"cubes": c, "spin": spin, "spin_pivot": [0, yc, 0]}


@hd("rocket_tube")
def _rocket_tube(m):
    """Shoulder-fired tube (M20 bazooka / Carl Gustaf): options dia, length, skin, extras."""
    dia, L = m.get("dia", 6), m.get("length", 56)
    skin = m.get("tube_skin", "od")
    front = -L // 2 - 6
    back = front + L
    c = [
        C(dia, dia, L, 0, front, skin),               # launch tube
        C(dia + 2, dia + 2, 2, -1, front - 1, "bore"),  # muzzle rim
        C(dia + 3, dia + 3, 5, -1.5, back, "bore"),   # venturi / rear bell
        C(dia + 1, dia + 1, 2, -0.5, front + 8, "yellow"),  # warning band
        C(3, 9, 4, -9, -14, "wood" if skin == "od" else "polymer"),  # front hand grip
        C(4, 5, 10, -5, 6, "rubber"),                 # shoulder rest
        R(-dia / 2 - 3, 3, -8, 3, 3, 10, "steel"),    # sight / telescope
        R(-dia / 2 - 3, 3.5, -9, 2, 2, 1, "glass"),
        R(-dia / 2 - 2, 1, -6, 2, 2, 2, "steel"),     # sight bracket
    ]
    if m.get("gustaf"):
        c += [C(dia + 2, dia + 2, 2, -1, front + 14, "gunmetal"),   # heat shield bands
              C(dia + 2, dia + 2, 2, -1, back - 12, "gunmetal")]
    c += grip(2, 0, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-2, 0, 4)
    return c


@hd("javelin")
def _javelin(m):
    """FGM-148: fat launch tube with end caps and the command launch unit on the left."""
    c = [
        C(9, 9, 46, -2, -30, "od"),                   # tube
        C(11, 11, 3, -3, -33, "rubber"),              # front cap
        C(11, 11, 3, -3, 16, "rubber"),               # rear cap
        C(10, 10, 1, -2.5, -8, "yellow"),             # band
        R(-13, -2, -8, 7, 8, 12, "tan"),              # CLU body
        R(-12, -1, -10, 5, 5, 2, "glass"),            # CLU objective
        R(-12, 0, 4, 4, 4, 3, "rubber"),              # eyepiece
        R(-14, 6, -6, 2, 2, 8, "polymer"),            # CLU handle
        C(4, 5, 10, -7, 4, "rubber"),                 # shoulder pad
    ]
    c += grip(2, -2, 10, d=4, w=3, rake=1.0, skin="polymer")
    c += trigger(-2, -2, 4)
    return c


@hd("grenade_launcher")
def _m79(m):
    """M79: fat break-open barrel, leaf sight, wood forend and stock."""
    c = [
        C(6, 6, 18, 1, -26, "aluminum"),              # 40 mm barrel
        C(6, 6, 1, 1, -27, "bore"),
        C(5, 6, 8, 0, -8, "steel"),                   # receiver / breech
        C(3, 5, 1, 7, -6, "steel"),                   # leaf sight
        C(1, 2, 1, 7, -24, "steel"),                  # front sight blade
        C(5, 3, 12, -2, -20, "wood"),                 # forend
    ]
    c += grip(1, 0, 9, d=5, w=4, rake=1.5, skin="wood")
    c += trigger(-5, 0, 5)
    c += stock_fixed(4, 0, skin="wood", butt="rubber", length=20)
    return c


# ------------------------------------------------------------------ materials
MATERIALS = {
    "steel": "#2f3237", "gunmetal": "#3e4146", "polymer": "#1f2124", "tan": "#b29873",
    "od": "#4d5733", "wood": "#6d3e1e", "chrome": "#b7bcc3", "cylinder": "#a9aeb5",
    "brass": "#c9a24a", "bore": "#2a2c30", "glass": "#23405f", "rail": "#27292c",
    "vent": "#232528", "ribbed": "#26282b", "rubber": "#151515", "bakelite": "#6a2a17",
    "red": "#ff2a1a", "yellow": "#d4ac2a", "canvas": "#5c6444", "aluminum": "#74787e",
    "drum": "#26282c", "pump": "#2a2c2f", "belt": "#b8913c",
}


def material_colors(m):
    cols = dict(MATERIALS)
    cols.update(m.get("colors", {}))
    return cols


def painters(m):
    """Skin painters for the hd materials: subtle noise, bevelled edges, and per-material
    detail (wood grain, rail ridges, vent slots, bores, lens glint, belt links)."""
    cols = material_colors(m)

    def bevel(p, c):
        if p.x == 0 or p.y == 0:
            return shade(c, 1.14)
        if p.x == p.fw - 1 or p.y == p.fh - 1:
            return shade(c, 0.84)
        return c

    def plain(name, amp=0.1, scale=1.4, seed=5):
        base = cols[name]

        def f(p):
            n = noise3(p.p[0], p.p[1], p.p[2], seed, scale)
            return bevel(p, shade(base, 1.0 - amp + 2 * amp * n))
        return f

    def wood(p):
        base = cols["wood"]
        g = noise3(p.p[0] * 0.4, p.p[1] * 2.2, p.p[2] * 0.25, 71, 1.0)
        line = (p.p[1] * 1.7 + 3.0 * g) % 2.0 < 0.35
        c = shade(base, 0.8 + 0.35 * g)
        return bevel(p, shade(c, 0.7) if line else c)

    def rail_f(p):
        c = shade(cols["rail"], 0.95 + 0.1 * noise3(p.p[0], p.p[1], p.p[2], 13, 1.0))
        if p.face not in ("front", "back") and math.floor(p.p[2]) % 2 == 0:
            c = shade(c, 0.55)
        return c

    def vent(p):
        c = bevel(p, shade(cols["vent"], 0.95 + 0.1 * noise3(p.p[0], p.p[1], p.p[2], 17, 1.0)))
        if p.face in ("east", "west", "bottom") and 1 <= p.y < p.fh - 1 \
                and math.floor(p.p[2]) % 4 in (1, 2):
            c = shade(c, 0.35)
        return c

    def ribbed(p):
        c = bevel(p, cols["ribbed"])
        if p.face in ("east", "west", "bottom", "top") and math.floor(p.p[2]) % 2 == 0:
            c = shade(c, 0.7)
        return c

    def pump(p):
        c = shade(cols["pump"], 0.95 + 0.1 * noise3(p.p[0], p.p[1], p.p[2], 19, 1.0))
        if p.face != "front" and p.face != "back" and math.floor(p.p[2]) % 2 == 0:
            c = shade(c, 0.6)
        return c

    def bore(p):
        c = bevel(p, shade(cols["bore"], 0.95 + 0.1 * noise3(p.p[0], p.p[1], p.p[2], 23, 1.0)))
        if p.face == "front" and 1 <= p.x < p.fw - 1 and 1 <= p.y < p.fh - 1:
            return "#050506"
        return c

    def glass(p):
        t = (p.x + p.y) / max(1, p.fw + p.fh - 2)
        c = mix("#9fd4ff", cols["glass"], min(1.0, 0.25 + t))
        return glow(c) if p.x == 1 and p.y == 1 else c

    def red(p):
        return glow(cols["red"])

    def cylinder(p):
        c = bevel(p, shade(cols["cylinder"], 0.9 + 0.2 * noise3(p.p[0], p.p[1], p.p[2], 29, 2.0)))
        if p.face in ("east", "west", "top", "bottom") and (p.x + p.y) % 3 == 0:
            c = shade(c, 0.75)
        return c

    def chrome(p):
        t = p.y / max(1, p.fh - 1)
        return bevel(p, shade(cols["chrome"], 1.15 - 0.35 * t))

    def drum(p):
        c = bevel(p, cols["drum"])
        if p.face in ("east", "west"):
            cx, cy = (p.fw - 1) / 2, (p.fh - 1) / 2
            r = math.hypot(p.x - cx, p.y - cy)
            if r < 1.2:
                return shade(cols["aluminum"], 1.1)
            if abs(r - cx * 0.7) < 0.5:
                return shade(c, 0.6)
        return c

    def belt(p):
        k = math.floor(p.p[2]) % 2
        return bevel(p, cols["brass"] if k == 0 else shade(cols["steel"], 1.2))

    def grip_tex(name):
        base = cols[name]

        def f(p):
            c = shade(base, 0.92 + 0.12 * noise3(p.p[0], p.p[1], p.p[2], 37, 0.8))
            if (p.x + p.y) % 2 == 0 and p.face in ("east", "west"):
                c = shade(c, 0.82)
            return bevel(p, c)
        return f

    out = {k: plain(k) for k in cols}
    out.update({"wood": wood, "rail": rail_f, "vent": vent, "ribbed": ribbed, "pump": pump,
                "bore": bore, "glass": glass, "red": red, "cylinder": cylinder,
                "chrome": chrome, "drum": drum, "belt": belt,
                "polymer": grip_tex("polymer"),
                "canvas": plain("canvas", amp=0.2, scale=0.6, seed=41),
                "tan": plain("tan", amp=0.06, scale=2.0, seed=43),
                "od": plain("od", amp=0.08, scale=2.0, seed=47)})
    return out


# ------------------------------------------------------------------ icon
def _inside(pts, u, v):
    """Point in convex quad (either winding), with a little slack so thin parts survive."""
    sign = 0
    for i in range(4):
        (au, av), (bu, bv) = pts[i], pts[(i + 1) % 4]
        cross = (bu - au) * (v - av) - (bv - av) * (u - au)
        L = math.hypot(bu - au, bv - av) or 1
        if abs(cross) / L < 0.35:
            continue
        sg = 1 if cross > 0 else -1
        if sign and sg != sign:
            return False
        sign = sg
    return True


def render_icon(parts, m, size=32):
    """Right-side orthographic view of the model (muzzle to the right), 32x32 RGBA."""
    cols = material_colors(m)
    cubes = parts["cubes"] + parts.get("spin", [])
    z0 = min(c["o"][2] for c in cubes) - 1; z1 = max(c["o"][2] + c["s"][2] for c in cubes) + 1
    y0 = min(c["o"][1] for c in cubes) - 1; y1 = max(c["o"][1] + c["s"][1] for c in cubes) + 1
    s = (size - 2) / max(z1 - z0, y1 - y0)
    ox = (size - (z1 - z0) * s) / 2
    oy = (size - (y1 - y0) * s) / 2
    px = [(0, 0, 0, 0)] * (size * size)
    depth = [-1e9] * (size * size)
    for c in cubes:
        (x, y, z), (w, h, d) = c["o"], c["s"]
        near = x + w
        col = rgb(cols.get(c["skin"], "#555555"))
        if c["skin"] == "wood":
            col = rgb(shade(col, 1.1))
        quad = [(y + h, z), (y + h, z + d), (y, z + d), (y, z)]
        if c.get("rot"):
            a = math.radians(c["rot"])
            py_, pz = c["pivot"][1], c["pivot"][2]
            quad = [(py_ + (qy - py_) * math.cos(a) + (qz - pz) * math.sin(a),
                     pz - (qy - py_) * math.sin(a) + (qz - pz) * math.cos(a)) for qy, qz in quad]
        # screen: u grows toward the muzzle (-z), v grows downward (-y)
        pts = [(ox + (z1 - qz) * s, oy + (y1 - qy) * s) for qy, qz in quad]
        top_v = min(v for _, v in pts); bot_v = max(v for _, v in pts)
        for py in range(size):
            for pxl in range(size):
                cu, cv = pxl + 0.5, py + 0.5
                if _inside(pts, cu, cv):
                    i = py * size + pxl
                    if near >= depth[i]:
                        depth[i] = near
                        t = (cv - top_v) / max(0.01, bot_v - top_v)
                        px[i] = shade(col[:3], 1.25 - 0.45 * t)[:3] + (255,)
    # dark outline around the silhouette
    out = list(px)
    for py in range(size):
        for pxl in range(size):
            if px[py * size + pxl][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                qx, qy = pxl + dx, py + dy
                if 0 <= qx < size and 0 <= qy < size and px[qy * size + qx][3]:
                    out[py * size + pxl] = (12, 12, 14, 255)
                    break
    return out
