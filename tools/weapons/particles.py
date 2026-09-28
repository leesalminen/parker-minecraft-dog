"""Generate RP/particles/*.json from parametric templates plus one shared shape atlas.

The whole VFX vocabulary is ~9 behaviour templates x a palette supplied at runtime through
`MolangVariableMap` (`variable.color`, `variable.size`, `variable.life`, `variable.count`,
`variable.speed`).  Shapes live in one 256x256 atlas, so 50 weapons do not mean 200 files.

Vocabulary emitted (weapons reference these names in their defs):
  gx:orb_<shape>       single billboard body particle (bolts, orbs, shards, ...)
  gx:beam_<shape>      beam segment with sine shimmer
  gx:dot_<style>       laser dot (point | ring | cross)
  gx:ring_wave         expanding shockwave ring
  gx:shock_disc        expanding disc ring
  gx:spark_burst       directional spark burst
  gx:debris_burst      tumbling debris burst
  gx:crystal_burst     shard burst
  gx:muzzle_flash      muzzle cone flash
  gx:star_flash        bright lens-spike flash
  gx:smoke_trail       rising smoke/steam
  gx:ember_trail       rising embers
  gx:lightning_fork    forked arc
  gx:static_arc        crackling arc
  gx:swirl             spiralling motes
  gx:field_glow        large soft zone glow
  gx:snow_mote         drifting snowflake
"""
import lib
from lib import RP, dump, write_png

ATLAS = 256
CELL = 32
GRID = 8
TEX = "textures/particle/gx_particles"

# ------------------------------------------------------------------ shape painters
def _cell():
    return [[(255, 255, 255, 0)] * CELL for _ in range(CELL)]


def _px(b, x, y, a):
    x, y = int(x), int(y)
    if 0 <= x < CELL and 0 <= y < CELL:
        b[y][x] = (255, 255, 255, int(max(0, min(255, a))))


def _disc(b, cx, cy, r, a0=255, falloff=1.0):
    for y in range(CELL):
        for x in range(CELL):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r:
                a = a0 * (1.0 - falloff * (d / max(r, 0.001)) ** 2)
                _px(b, x, y, a)


def _ring(b, cx, cy, r, thick, a0=255):
    for y in range(CELL):
        for x in range(CELL):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if abs(d - r) <= thick:
                _px(b, x, y, a0 * (1.0 - abs(d - r) / max(thick, 0.001)))


def _line(b, x0, y0, x1, y1, w, a0=255):
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        _disc(b, x, y, w, a0)


def _poly(b, pts, a0=255):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    for y in range(int(min(ys)), int(max(ys)) + 1):
        for x in range(int(min(xs)), int(max(xs)) + 1):
            inside = False
            n = len(pts)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    inside = not inside
            if inside:
                _px(b, x, y, a0)


def _soft_orb(b):
    _disc(b, 15.5, 15.5, 15, 255, 1.15)


def _teardrop(b):
    _disc(b, 21, 15.5, 9, 255, 0.9)
    _poly(b, [(13, 12), (13, 19), (1, 15.5)], 220)


def _dart(b):
    _poly(b, [(24, 15.5), (12, 9), (12, 22)], 255)
    _poly(b, [(12, 12), (12, 19), (2, 15.5)], 200)


def _glob(b):
    _disc(b, 14, 14, 10, 255, 0.8)
    _disc(b, 21, 18, 7, 230, 0.9)
    _disc(b, 10, 21, 6, 210, 0.9)


def _needle(b):
    _line(b, 2, 15.5, 29, 15.5, 1.6, 255)
    _disc(b, 27, 15.5, 3, 255, 0.6)


def _disc_shape(b):
    _ring(b, 15.5, 15.5, 13, 2.5, 255)


def _bar(b):
    for x in range(1, 31):
        a = 255 * min(1.0, min(x, 31 - x) / 4.0)
        for y in range(12, 20):
            _px(b, x, y, a * (1.0 - abs(y - 15.5) / 4.0))


def _star(b):
    _line(b, 15.5, 1, 15.5, 30, 1.6, 255)
    _line(b, 1, 15.5, 30, 15.5, 1.6, 255)
    _disc(b, 15.5, 15.5, 3.5, 255, 0.6)


def _flash(b):
    for ang in range(0, 360, 60):
        import math
        r = math.radians(ang)
        _line(b, 15.5, 15.5, 15.5 + 15 * math.cos(r), 15.5 + 15 * math.sin(r), 1.4, 235)
    _disc(b, 15.5, 15.5, 6, 255, 0.5)


def _ring_shape(b):
    _ring(b, 15.5, 15.5, 13.5, 2.0, 255)


def _fork(b):
    _line(b, 4, 30, 11, 22, 1.4, 255)
    _line(b, 11, 22, 8, 15, 1.4, 255)
    _line(b, 8, 15, 16, 9, 1.4, 255)
    _line(b, 16, 9, 14, 3, 1.4, 255)
    _line(b, 16, 9, 23, 6, 1.2, 200)
    _line(b, 11, 22, 19, 19, 1.2, 200)


def _dot(b):
    _disc(b, 15.5, 15.5, 3.5, 255, 0.5)


def _dot_ring(b):
    _ring(b, 15.5, 15.5, 8.5, 1.6, 255)
    _disc(b, 15.5, 15.5, 1.4, 255)


def _dot_cross(b):
    _line(b, 15.5, 7, 15.5, 24, 1.2, 255)
    _line(b, 7, 15.5, 24, 15.5, 1.2, 255)


def _hex(b):
    import math
    pts = [(15.5 + 13 * math.cos(math.radians(60 * i + 30)), 15.5 + 13 * math.sin(math.radians(60 * i + 30)))
           for i in range(6)]
    _poly(b, pts, 235)


def _cone(b):
    _poly(b, [(6, 27), (25, 27), (15.5, 3)], 200)
    _disc(b, 15.5, 26, 6, 240, 0.8)


def _droplet(b):
    _disc(b, 15.5, 20, 6, 255, 0.8)
    _poly(b, [(11, 17), (20, 17), (15.5, 3)], 220)


def _flake(b):
    import math
    for ang in range(0, 360, 60):
        r = math.radians(ang)
        _line(b, 15.5, 15.5, 15.5 + 13 * math.cos(r), 15.5 + 13 * math.sin(r), 1.0, 240)


def _shard(b):
    _poly(b, [(15.5, 2), (24, 27), (7, 27)], 255)
    _poly(b, [(15.5, 8), (19, 25), (12, 25)], 255)


def _puff(b):
    _disc(b, 15, 17, 11, 150, 1.3)
    _disc(b, 20, 13, 8, 120, 1.4)


def _paw(b):
    _disc(b, 15.5, 20, 5.5, 255, 0.6)
    for dx, dy in ((-7, -6), (-2.5, -9), (2.5, -9), (7, -6)):
        _disc(b, 15.5 + dx, 20 + dy, 2.6, 255, 0.6)


def _heart(b):
    _disc(b, 11, 12, 4.5, 255, 0.6)
    _disc(b, 20, 12, 4.5, 255, 0.6)
    _poly(b, [(6, 14), (25, 14), (15.5, 28)], 255)


def _bone(b):
    _line(b, 9, 11, 22, 20, 2.6, 255)
    _disc(b, 8, 10, 4, 255, 0.7)
    _disc(b, 23, 21, 4, 255, 0.7)


def _swirl(b):
    import math
    for i in range(80):
        t = i / 79
        r = 2 + 13 * t
        a = t * 6.5
        _px(b, 15.5 + r * math.cos(a), 15.5 + r * math.sin(a), 230 * (1 - t))


def _ember(b):
    _disc(b, 15.5, 15.5, 4.5, 255, 1.0)


def _spark(b):
    _line(b, 15.5, 6, 15.5, 25, 1.0, 255)
    _line(b, 6, 15.5, 25, 15.5, 1.0, 255)
    _disc(b, 15.5, 15.5, 2, 255)


def _plume(b):
    _disc(b, 15.5, 22, 7, 220, 1.1)
    _poly(b, [(11, 20), (20, 20), (15.5, 2)], 170)


def _crackle(b):
    for dx, dy in ((8, 10), (15, 8), (22, 12), (11, 18), (19, 20), (15, 24), (6, 22), (24, 21)):
        _disc(b, dx, dy, 1.8, 255)
    _line(b, 8, 10, 15, 8, 0.8, 200)
    _line(b, 15, 8, 22, 12, 0.8, 200)
    _line(b, 11, 18, 19, 20, 0.8, 200)


SHAPES = {
    "soft_orb": _soft_orb, "teardrop": _teardrop, "dart": _dart, "glob": _glob,
    "needle": _needle, "disc": _disc_shape, "bar": _bar, "star": _star,
    "flash": _flash, "ring": _ring_shape, "fork": _fork, "dot": _dot,
    "dot_ring": _dot_ring, "dot_cross": _dot_cross, "hex": _hex, "cone": _cone,
    "droplet": _droplet, "flake": _flake, "shard": _shard, "puff": _puff,
    "paw": _paw, "heart": _heart, "bone": _bone, "swirl": _swirl,
    "ember": _ember, "spark": _spark, "plume": _plume, "crackle": _crackle,
}
ORDER = list(SHAPES)


def _uv(shape):
    i = ORDER.index(shape)
    return {"texture_width": ATLAS, "texture_height": ATLAS,
            "uv": [(i % GRID) * CELL, (i // GRID) * CELL], "uv_size": [CELL, CELL]}


# ------------------------------------------------------------------ behaviour templates
def _base(ident, comps):
    return {"format_version": "1.10.0", "particle_effect": {
        "description": {"identifier": ident,
                        "basic_render_parameters": {"material": "particles_alpha", "texture": TEX}},
        "components": comps}}


def _tint(fade=False):
    a = "variable.color.a * (1.0 - variable.particle_age / variable.particle_lifetime)" if fade \
        else "variable.color.a"
    return {"minecraft:particle_appearance_tinting": {
        "color": ["variable.color.r", "variable.color.g", "variable.color.b", a]}}


def orb(shape):
    return _base(f"gx:orb_{shape}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size", "variable.size"], "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def beam(shape):
    return _base(f"gx:beam_{shape}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size * (0.85 + 0.25 * math.sin(variable.particle_age * 420.0))",
                     "variable.size * (0.85 + 0.25 * math.cos(variable.particle_age * 380.0))"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def dot(style):
    return _base(f"gx:dot_{style}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size", "variable.size"], "facing_camera_mode": "rotate_xyz", "uv": _uv(style)},
        **_tint(False)})


def ring_wave(name, shape, grow):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": [f"variable.size * (0.15 + {grow} * variable.particle_age / variable.particle_lifetime)",
                     f"variable.size * (0.15 + {grow} * variable.particle_age / variable.particle_lifetime)"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def burst(name, shape, gravity, spread):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": "variable.count"},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_sphere": {"offset": [0, 0, 0], "radius": 0.15,
                                           "direction": "outwards", "surface_only": False},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": "variable.speed",
        "minecraft:particle_motion_dynamic": {
            "linear_acceleration": [0, gravity, 0], "linear_drag_coefficient": 1.6},
        "minecraft:particle_appearance_billboard": {
            "size": [f"variable.size * {spread}", f"variable.size * {spread}"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def trail(name, shape, accel):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0.2,
        "minecraft:particle_motion_dynamic": {
            "linear_acceleration": [0, accel, 0], "linear_drag_coefficient": 2.4},
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size * (0.5 + 1.4 * variable.particle_age / variable.particle_lifetime)",
                     "variable.size * (0.5 + 1.4 * variable.particle_age / variable.particle_lifetime)"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def flash(name, shape, spike=6.0):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": [f"variable.size * (1.0 + {spike} * (1.0 - variable.particle_age / variable.particle_lifetime))",
                     f"variable.size * (1.0 + {spike} * (1.0 - variable.particle_age / variable.particle_lifetime))"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def fork(name, shape):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size * (0.9 + 0.3 * math.sin(variable.particle_age * 900.0))",
                     "variable.size * (0.9 + 0.3 * math.cos(variable.particle_age * 830.0))"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def swirl(name, shape):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": "variable.count"},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_sphere": {"offset": [0, 0, 0], "radius": "variable.size * 1.6",
                                           "direction": "outwards"},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": "variable.speed",
        "minecraft:particle_motion_dynamic": {"linear_drag_coefficient": 3.2,
                                              "rotation_acceleration": 220.0},
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size * 0.5", "variable.size * 0.5"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def field_glow(name, shape):
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": "variable.life"},
        "minecraft:particle_initial_speed": 0,
        "minecraft:particle_appearance_billboard": {
            "size": ["variable.size * (0.7 + 0.3 * math.sin(variable.particle_age * 90.0))",
                     "variable.size * (0.7 + 0.3 * math.cos(variable.particle_age * 90.0))"],
            "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(True)})


def shell_eject(name, shape):
    """Ejected brass: flung out of the port along (variable.dir_x, up, variable.dir_z),
    falls, bounces on blocks, fades."""
    return _base(f"gx:{name}", {
        "minecraft:emitter_rate_instant": {"num_particles": 1},
        "minecraft:emitter_lifetime_once": {"active_time": 0.05},
        "minecraft:emitter_shape_point": {"offset": [0, 0, 0],
                                          "direction": ["variable.dir_x", 1.1, "variable.dir_z"]},
        "minecraft:particle_lifetime_expression": {"max_lifetime": 0.9},
        "minecraft:particle_initial_speed": 3.0,
        "minecraft:particle_initial_spin": {"rotation": 0, "rotation_rate": 900},
        "minecraft:particle_motion_dynamic": {"linear_acceleration": [0, -24, 0],
                                              "linear_drag_coefficient": 0.3},
        "minecraft:particle_motion_collision": {"coefficient_of_restitution": 0.3,
                                                "collision_drag": 6, "collision_radius": 0.03},
        "minecraft:particle_appearance_billboard": {
            "size": [0.035, 0.08], "facing_camera_mode": "rotate_xyz", "uv": _uv(shape)},
        **_tint(False)})


ORB_SHAPES = ["teardrop", "dart", "glob", "needle", "disc", "soft_orb", "shard",
              "droplet", "star", "paw", "bone", "hex", "plume"]
BEAM_SHAPES = ["bar", "needle", "teardrop", "disc", "plume", "fork"]
DOT_STYLES = ["dot", "dot_ring", "dot_cross"]


def write_particles():
    """Write the shape atlas and every particle effect. Returns the list of effect names."""
    px = [(0, 0, 0, 0)] * (ATLAS * ATLAS)
    for i, name in enumerate(ORDER):
        b = _cell()
        SHAPES[name](b)
        ox, oy = (i % GRID) * CELL, (i // GRID) * CELL
        for y in range(CELL):
            for x in range(CELL):
                px[(oy + y) * ATLAS + ox + x] = b[y][x]
    write_png(RP / "textures/particle/gx_particles.png", px, ATLAS, ATLAS)

    effects = {}
    for s in ORB_SHAPES:
        effects[f"orb_{s}"] = orb(s)
    for s in BEAM_SHAPES:
        effects[f"beam_{s}"] = beam(s)
    for s in DOT_STYLES:
        effects[f"dot_{s}"] = dot(s)
    effects["ring_wave"] = ring_wave("ring_wave", "ring", 2.6)
    effects["shock_disc"] = ring_wave("shock_disc", "disc", 3.4)
    effects["spark_burst"] = burst("spark_burst", "spark", -6.0, 0.55)
    effects["debris_burst"] = burst("debris_burst", "shard", -14.0, 0.6)
    effects["crystal_burst"] = burst("crystal_burst", "flake", -8.0, 0.6)
    effects["muzzle_flash"] = burst("muzzle_flash", "hex", 0.0, 0.9)
    effects["star_flash"] = flash("star_flash", "flash")
    effects["smoke_trail"] = trail("smoke_trail", "puff", 1.6)
    effects["ember_trail"] = trail("ember_trail", "ember", 2.4)
    effects["lightning_fork"] = fork("lightning_fork", "fork")
    effects["static_arc"] = fork("static_arc", "crackle")
    effects["swirl"] = swirl("swirl", "swirl")
    effects["field_glow"] = field_glow("field_glow", "soft_orb")
    effects["snow_mote"] = orb("flake")
    effects["shell_eject"] = shell_eject("shell_eject", "bar")

    for name, eff in effects.items():
        dump(RP / f"particles/gx_{name}.json", eff)
    return sorted(f"gx:{k}" for k in effects)
