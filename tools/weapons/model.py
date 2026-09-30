"""Held-model geometry + texture generation for Galaxy Forge weapons.

Reuses the creature framework's UV packer and texture painter (tools/creatures/lib.py).

Every weapon gets:
  * one geometry  `geometry.gx_<id>`  bound to the player's hand bone
  * one emissive texture `textures/entity/gx_<id>.png`
  * one attachable `attachables/<id>.json`

Models are drawn in hand space, 1 unit = 1/16 block, model faces -Z:
the muzzle points down -Z, the grip sits at y <= 0 (the hand).
"""
import lib
import hd_models
from lib import RP, dump, glow, shade, mix, rgb, noise3, hash01, write_png, pack_uvs, make_texture

NS = "gx"
ANIM = "animation.gx_weapon"


# ------------------------------------------------------------------ cubes
def cube(x, y, z, w, h, d, skin="metal", inflate=None):
    c = {"o": [x, y, z], "s": [w, h, d], "skin": skin}
    if inflate:
        c["inflate"] = inflate
    return c


FORMS = {}


def form(name):
    def deco(fn):
        FORMS[name] = fn
        return fn
    return deco


# ------------------------------------------------------------------ forms
@form("rifle")
def _rifle(m):
    L = m.get("len", 20)
    T = m.get("thick", 3)
    H = m.get("tall", 3)
    c = [
        cube(-1, 0, -6, T, H, 12, "metal"),          # receiver
        cube(-1, 0, -6 - L, 2, 2, L, "metal"),       # barrel
        cube(-1, 1, -6 - L + 2, 2, 1, max(2, L - 4), "glow"),   # emissive rail
        cube(-2, -1, -6 - L - 3, 4, 4, 3, "glow"),   # muzzle
        cube(-1, -5, -2, 2, 5, 3, "grip"),           # grip
        cube(-1, -8, -7, 2, 6, 4, "accent"),         # magazine
        cube(-1, 0, 6, T, H, 8, "dark"),             # stock
    ]
    if m.get("scope"):
        c.append(cube(-1, H, -8, 2, 2, m.get("scope_len", 8), "glow"))
    if m.get("fins"):
        c.append(cube(-2, -1, -6 - L + 4, 4, 4, 2, "accent"))
        c.append(cube(-2, -1, -6 - L + 9, 4, 4, 2, "accent"))
    if m.get("drum"):
        c.append(cube(-2, -9, -6, 4, 4, 4, "accent"))
    if m.get("underbarrel"):
        c.append(cube(-1, -3, -6 - L // 2, 2, 3, 6, "dark"))
    return c


@form("sniper")
def _sniper(m):
    L = m.get("len", 34)
    return [
        cube(-1, 0, -8, 3, 3, 14, "metal"),
        cube(-1, 0, -8 - L, 2, 2, L, "metal"),
        cube(-1, 1, -8 - L + 2, 2, 1, L - 4, "glow"),
        cube(-2, -1, -8 - L - 3, 4, 4, 3, "glow"),
        cube(-1, -5, -3, 2, 5, 3, "grip"),
        cube(-1, -7, -8, 2, 4, 3, "accent"),
        cube(-1, 0, 7, 3, 3, 10, "dark"),
        cube(-1, 3, -9, 2, 3, 9, "glow"),            # big optic
        cube(-1, -3, -10, 2, 2, 8, "dark"),          # bipod rail
    ]


@form("pistol")
def _pistol(m):
    H = m.get("tall", 3)
    return [
        cube(-1, 0, -6, 3, H, 8, "metal"),
        cube(-1, 1, -4, 2, 1, 5, "glow"),
        cube(-1, -5, -1, 2, 5, 3, "grip"),
        cube(-1, H, -3, 2, 2, 4, "glow"),
        cube(-2, -1, -9, 4, 4, 3, "glow"),
    ]


@form("revolver")
def _revolver(m):
    return [
        cube(-1, 0, -5, 3, 3, 7, "metal"),
        cube(-2, -1, -1, 4, 4, 4, "accent"),          # cylinder
        cube(-1, -6, 0, 2, 6, 3, "grip"),
        cube(-1, 0, -14, 2, 2, 9, "metal"),
        cube(-2, -1, -17, 4, 4, 3, "glow"),
        cube(-1, 2, -5, 2, 1, 6, "glow"),
    ]


@form("smg")
def _smg(m):
    L = m.get("len", 10)
    twin = m.get("twin", True)
    c = [
        cube(-1, 0, -5, 4, 3, 9, "metal"),
        cube(-1, -4, -1, 2, 4, 3, "grip"),
        cube(-1, -7, -6, 2, 5, 4, "accent"),
        cube(-1, 2, -6, 2, 1, 8, "glow"),
    ]
    if twin:
        c += [cube(-2, 0, -5 - L, 2, 2, L, "metal"), cube(1, 0, -5 - L, 2, 2, L, "metal"),
              cube(-2, -1, -5 - L - 2, 2, 2, 2, "glow"), cube(1, -1, -5 - L - 2, 2, 2, 2, "glow")]
    else:
        c += [cube(-1, 0, -5 - L, 2, 2, L, "metal"), cube(-2, -1, -5 - L - 2, 4, 4, 3, "glow")]
    return c


@form("cannon")
def _cannon(m):
    L = m.get("len", 14)
    return [
        cube(-2, -2, -8, 5, 5, 12, "metal"),
        cube(-3, -3, -8 - L, 6, 6, L, "metal"),
        cube(-3, -3, -8 - L - 3, 6, 6, 3, "glow"),
        cube(-3, 3, -8 - L + 2, 6, 1, L - 4, "glow"),
        cube(-1, -7, -2, 3, 5, 4, "grip"),
        cube(-1, -9, -8, 3, 5, 6, "accent"),
        cube(-2, -2, 6, 5, 5, 6, "dark"),              # shoulder rest
        cube(-1, 5, -6, 3, 2, 6, "glow"),              # core cage
    ]


@form("launcher")
def _launcher(m):
    L = m.get("len", 16)
    return [
        cube(-2, -2, -6, 5, 5, 10, "metal"),
        cube(-2, -2, -6 - L, 4, 4, L, "metal"),
        cube(-3, -3, -6 - L - 2, 6, 6, 3, "glow"),
        cube(-2, 3, -6 - L + 2, 4, 1, L - 4, "glow"),
        cube(-1, -7, -3, 3, 5, 4, "grip"),
        cube(-2, -9, -6, 4, 4, 5, "accent"),           # drum
        cube(-2, -2, 5, 5, 5, 5, "dark"),
    ]


@form("mortar")
def _mortar(m):
    return [
        cube(-2, -1, -4, 5, 8, 8, "metal"),
        cube(-2, 2, -12, 4, 5, 9, "metal"),
        cube(-3, 1, -15, 6, 6, 3, "glow"),
        cube(-1, -7, -2, 3, 6, 4, "grip"),
        cube(-2, -2, 4, 5, 5, 5, "dark"),
        cube(-2, 3, -8, 1, 1, 6, "glow"),
    ]


@form("lance")
def _lance(m):
    L = m.get("len", 30)
    rings = m.get("rings", 3)
    c = [
        cube(-1, -1, -6, 3, 3, 12, "metal"),
        cube(-1, -1, -6 - L, 2, 2, L, "metal"),
        cube(-1, 0, -6 - L + 2, 2, 1, max(2, L - 4), "glow"),
        cube(-2, -2, -6 - L - 3, 4, 4, 3, "glow"),
        cube(-1, -6, -2, 2, 5, 3, "grip"),
        cube(-1, 0, 7, 3, 3, 9, "dark"),
    ]
    for i in range(rings):
        c.append(cube(-3, -3, -10 - i * 8, 6, 6, 1, "glow"))
    return c


@form("staff")
def _staff(m):
    L = m.get("len", 26)
    return [
        cube(-1, -1, -3, 2, 2, L, "metal"),
        cube(-1, -1, -6, 3, 3, 3, "accent"),
        cube(-3, -3, -3 - L, 6, 6, 6, "glow"),          # orb head
        cube(-1, -1, 2, 2, 2, 6, "dark"),
        cube(-1, 1, -8, 2, 1, 8, "glow"),
    ]


@form("gauntlet")
def _gauntlet(m):
    return [
        cube(-3, -4, -6, 6, 8, 8, "metal"),
        cube(-3, -4, -9, 6, 6, 3, "accent"),
        cube(-4, -4, -2, 8, 6, 2, "metal"),
        cube(-2, -2, -11, 4, 4, 2, "glow"),             # palm emitter
        cube(-3, 4, -5, 6, 1, 6, "glow"),
    ]


@form("bow")
def _bow(m):
    return [
        cube(-1, -1, -4, 3, 3, 8, "metal"),
        cube(-1, -6, -6, 2, 12, 2, "accent"),           # upper limb
        cube(-1, -6, 4, 2, 12, 2, "accent"),            # lower limb
        cube(-1, 0, -8, 2, 1, 6, "glow"),
        cube(-1, -1, 4, 2, 2, 5, "dark"),
    ]


@form("disc")
def _disc(m):
    return [
        cube(-1, -1, -5, 3, 3, 9, "metal"),
        cube(-1, -5, -2, 2, 4, 3, "grip"),
        cube(-2, 2, -6, 4, 3, 6, "accent"),             # chamber
        cube(-3, -3, -10, 6, 6, 2, "glow"),             # disc emitter
        cube(-1, 0, 4, 3, 3, 6, "dark"),
    ]


@form("sprayer")
def _sprayer(m):
    return [
        cube(-2, -1, -6, 5, 5, 9, "metal"),
        cube(-2, 1, -11, 3, 3, 6, "metal"),
        cube(-2, 0, -14, 4, 5, 3, "glow"),              # nozzle
        cube(-1, -7, -3, 3, 6, 4, "grip"),
        cube(-2, -2, 3, 5, 6, 6, "accent"),             # tank
        cube(-3, -3, -6, 6, 6, 6, "glow"),              # vial
    ]


@form("rack")
def _rack(m):
    tubes = m.get("tubes", 4)
    c = [
        cube(-2, -2, -5, 5, 5, 10, "metal"),
        cube(-1, -7, -2, 3, 5, 4, "grip"),
        cube(-2, -2, 6, 5, 5, 5, "dark"),
    ]
    for i in range(tubes):
        x = -3 + (i % 2) * 3
        y = 1 + (i // 2) * 3
        c.append(cube(x, y, -5 - 12, 3, 3, 12, "metal"))
        c.append(cube(x, y, -5 - 14, 3, 3, 2, "glow"))
    c.append(cube(-2, 4, -12, 5, 1, 8, "glow"))
    return c


@form("kit")
def _kit(m):
    return [
        cube(-4, -3, -6, 8, 6, 12, "metal"),
        cube(-4, -3, -8, 8, 2, 2, "accent"),
        cube(-1, -9, -3, 3, 6, 4, "grip"),
        cube(-3, -1, -9, 6, 4, 2, "glow"),
        cube(-4, 3, -6, 8, 1, 12, "dark"),
    ]


# ------------------------------------------------------------------ texture painters
def _painters(spec):
    pal = spec["palette"]
    m = spec.get("model", {})
    metal = m.get("metal", "#59616d")
    grip = m.get("grip", "#24282e")
    dark = shade(metal, 0.55)

    def base(p, col, seed):
        n = noise3(p.p[0], p.p[1], p.p[2], seed, 2.6)
        return shade(col, 0.78 + 0.5 * n)

    def f_metal(p):
        return base(p, metal, 11)

    def f_dark(p):
        return base(p, dark, 23)

    def f_grip(p):
        # ribbed grip: dark ridges every other texel row
        c = base(p, grip, 31)
        if p.y % 3 == 0:
            c = shade(c, 1.35)
        return c

    def f_accent(p):
        return base(p, pal["accent"], 47)

    def f_glow(p):
        t = noise3(p.p[0], p.p[1], p.p[2], 59, 1.8)
        return glow(mix(pal["glow"], pal["core"], 0.25 + 0.5 * t))

    return {"metal": f_metal, "dark": f_dark, "grip": f_grip, "accent": f_accent, "glow": f_glow}


# ------------------------------------------------------------------ emitters
def hd_parts(spec):
    """{"cubes", "spin"?, "spin_pivot"?} for a high-detail form, else None."""
    m = spec.get("model", {})
    fn = hd_models.HD.get(m.get("form"))
    if not fn:
        return None
    parts = fn(m)
    return parts if isinstance(parts, dict) else {"cubes": parts}


def write_model(spec):
    """Write geometry, texture and attachable for one weapon. Returns texture size."""
    wid = spec["id"]
    m = spec.get("model", {})
    binding = "q.item_slot_to_bone_name(c.item_slot)"
    hdp = hd_parts(spec)
    if hdp:
        # High-detail models are authored at 1/32 block; the `hd` bone is scaled 0.5 by the
        # shared hd animation so the hand origin and hold poses are unchanged.
        bones = [{"name": "weapon", "cubes": []},
                 {"name": "hd", "parent": "weapon", "cubes": hdp["cubes"]}]
        if hdp.get("spin"):
            bones.append({"name": "spin", "parent": "hd", "pivot": hdp["spin_pivot"],
                          "cubes": hdp["spin"]})
        skins = hd_models.painters(m)
    else:
        bones = [{"name": "weapon", "cubes": FORMS[m.get("form", "rifle")](m)}]
        skins = _painters(spec)
    size = pack_uvs(bones)
    px = make_texture({"id": wid, "skins": skins}, bones, size)
    write_png(RP / f"textures/entity/gx_{wid}.png", px, size, size)

    geo_bones = []
    for b in bones:
        out = []
        for c in b["cubes"]:
            oc = {"origin": c["o"], "size": c["s"], "uv": c["uv"]}
            if c.get("inflate") is not None:
                oc["inflate"] = c["inflate"]
            if c.get("rot"):
                oc["rotation"] = [c["rot"], 0, 0]
                oc["pivot"] = c["pivot"]
            out.append(oc)
        gb = {"name": b["name"], "pivot": b.get("pivot", [0, 0, 0]), "cubes": out}
        if b.get("parent"):
            gb["parent"] = b["parent"]
        else:
            gb["binding"] = binding
        geo_bones.append(gb)
    geo = {"format_version": "1.16.0", "minecraft:geometry": [{"description": {
        "identifier": f"geometry.gx_{wid}", "texture_width": size, "texture_height": size,
        "visible_bounds_width": 5, "visible_bounds_height": 3, "visible_bounds_offset": [0, 0, 0]},
        "bones": geo_bones}]}
    dump(RP / f"models/entity/gx_{wid}.geo.json", geo)

    anims = {"wield": f"{ANIM}.wield", "aim": f"{ANIM}.aim", "charge": f"{ANIM}.charge"}
    animate = ["wield", {"aim": "query.is_sneaking"},
               {"charge": "query.main_hand_item_use_duration > 0.0"}]
    if hdp:
        anims["hd"] = f"{ANIM}.hd"
        animate.append("hd")
        if hdp.get("spin"):
            anims["spin"] = f"{ANIM}.spin"
            animate.append({"spin": "query.main_hand_item_use_duration > 0.0"})
    dump(RP / f"attachables/{wid}.json", {"format_version": "1.10.0", "minecraft:attachable": {
        "description": {
            "identifier": f"{NS}:{wid}",
            "materials": {"default": "entity_emissive_alpha", "enchanted": "entity_alphatest_glint"},
            "textures": {"default": f"textures/entity/gx_{wid}",
                         "enchanted": "textures/misc/enchanted_item_glint"},
            "geometry": {"default": f"geometry.gx_{wid}"},
            "animations": anims,
            "scripts": {"animate": animate},
            "render_controllers": ["controller.render.item_default"]}}})
    return size


def write_shared_animations():
    """One shared wield/aim/charge pose set, reused by all 50 attachables.

    `wield` carries the full first- and third-person hold pose; aim/charge only add
    small third-person nudges on top (Bedrock sums animations on a bone).
    """
    # Third-person pose copied from koukuma5968/minecraft_addon (animation.sniper_rifle.
    # hold_therd_person).  The donor's first-person *hold* rotation (-15.5, 51.7, -36.2)
    # left the barrel ~66 deg upward under vanilla's [95,-45,115] first-person arm, because
    # the donor swaps to a +110 deg X "shot" pose we never had.  FP_ROT below is solved so
    # arm * FP_ROT maps barrel(-z) -> forward and grip -> down (Blockbench first-person
    # preview convention).  Derived, not yet confirmed on device: tune FP_POS on a screenshot.
    FP_POS, FP_ROT, FP_SCALE = (10.0, 12.0, 6.0), (82.636095, 61.260361, -51.574206), 0.85
    TP_POS, TP_ROT = (0.0, 24.0, 0.0), (-92.5, 0.0, 0.0)

    def pose(tp_pos=(0, 0, 0), tp_rot=(0, 0, 0), base=False):
        # Bedrock stacks every running animation on a bone additively, so only `wield` carries
        # the first-person base pose; aim/charge add third-person-only nudges on top of it.
        fp = "c.is_first_person"
        fpos = FP_POS if base else (0, 0, 0)
        frot = FP_ROT if base else (0, 0, 0)
        tpos = [tp_pos[i] + (TP_POS[i] if base else 0) for i in range(3)]
        trot = [tp_rot[i] + (TP_ROT[i] if base else 0) for i in range(3)]
        out = {"position": [f"{fp} ? {fpos[i]} : {tpos[i]}" for i in range(3)],
               "rotation": [f"{fp} ? {frot[i]} : {trot[i]}" for i in range(3)]}
        if base:
            out["scale"] = f"{fp} ? {FP_SCALE} : 1.0"
        return out

    dump(RP / "animations/gx_weapon.animation.json", {"format_version": "1.10.0", "animations": {
        f"{ANIM}.wield": {"loop": True, "bones": {"weapon": pose(base=True)}},
        f"{ANIM}.aim": {"loop": True, "bones": {"weapon": pose((0, 1, 1), (-6, 0, 0))}},
        f"{ANIM}.charge": {"loop": True, "bones": {"weapon": pose((0, 0, 1), (2, 0, 0))}},
        # high-detail models (hd_models.py) are authored at 1/32 block
        f"{ANIM}.hd": {"loop": True, "bones": {"hd": {"scale": [0.5, 0.5, 0.5]}}},
        # minigun barrel cluster spins while the trigger is held
        f"{ANIM}.spin": {"loop": True, "bones": {"spin": {"rotation": [0, 0, "q.life_time * 1440"]}}},
    }})
