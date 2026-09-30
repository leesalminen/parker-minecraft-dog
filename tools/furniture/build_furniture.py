#!/usr/bin/env python3
"""Galaxy Home furniture generator.

    python3 tools/furniture/build_furniture.py            # (re)generate blocks, geometry, textures, terrain_texture entries
    python3 tools/furniture/build_furniture.py --check    # validate only
    python3 tools/furniture/build_furniture.py --preview out.png   # front-view contact sheet

Also runs as part of `python3 tools/creatures/build_all.py` (via tools/creatures/extras/furniture.py), which is what
adds the block names to the shared en_US.lang.  Output (all under packs/GalaxyForge_{BP,RP}):
    BP blocks/gx_furn_<id>.json                 RP models/blocks/gx_furn_<id>.geo.json
    RP textures/blocks/gx_furn/<material>.png   RP textures/terrain_texture.json (gx_furn_* keys merged in)
"""
import json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "creatures"))
import lib
from lib import write_png, rgb
import materials
import pieces

BP, RP, NS = lib.BP, lib.RP, lib.NS
PREFIX = "furn_"
GROUP = "itemGroup.name.gx_home"
FORMAT = "1.21.0"
TILE = materials.T
FACES = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
ROTS = {"south": 180, "west": 90, "east": 270}   # cardinal_direction -> Y rotation; "north" is the unrotated model


# ------------------------------------------------------------------ helpers
def bid(p): return f"{NS}:{PREFIX}{p['id']}"
def tex_key(mat): return f"gx_furn_{mat}"


def face_mat(mat, f):
    """Resolve a box's material spec for face letter f -> (material name, fit)."""
    if isinstance(mat, dict):
        m = mat.get(f) or (mat.get("front") if f == "s" else None) or (mat.get("side") if f in "nsew" else None) \
            or (mat.get("top") if f == "u" else None) or (mat.get("bottom") if f == "d" else None) or mat.get("*")
    else:
        m = mat
    fit = m.startswith("@")
    return m.lstrip("@"), fit


def face_uv(f, box, fit):
    _, x0, y0, z0, x1, y1, z1 = box
    if fit: return [0, 0], [TILE, TILE]
    if f in "ns": return [x0 * 2, (16 - y1) * 2], [(x1 - x0) * 2, (y1 - y0) * 2]
    if f in "ew": return [z0 * 2, (16 - y1) * 2], [(z1 - z0) * 2, (y1 - y0) * 2]
    return [x0 * 2, z0 * 2], [(x1 - x0) * 2, (z1 - z0) * 2]


def union(boxes):
    return (min(b[1] for b in boxes), min(b[2] for b in boxes), min(b[3] for b in boxes),
            max(b[4] for b in boxes), max(b[5] for b in boxes), max(b[6] for b in boxes))


def rot_box(b, deg):
    """Rotate an (x0,y0,z0,x1,y1,z1) pixel box about the block's Y axis (same convention as minecraft:transformation)."""
    t = math.radians(deg); c, s = round(math.cos(t)), round(math.sin(t))
    pts = [(c * (x - 8) + s * (z - 8) + 8, -s * (x - 8) + c * (z - 8) + 8) for x in (b[0], b[3]) for z in (b[2], b[5])]
    xs, zs = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), b[1], min(zs), max(xs), b[4], max(zs))


def bbox_component(b):
    b = [max(0, min(16, v)) for v in b]
    return {"origin": [b[0] - 8, b[1], b[2] - 8], "size": [b[3] - b[0], b[4] - b[1], b[5] - b[2]]}


def collision_boxes(p):
    """List of boxes for collision, or [] for none.  Default: union of the visible boxes."""
    if p["col"] is False: return []
    if p["col"] is None: return [union(p["boxes"])]
    return [tuple(b) for b in p["col"]]


def selection_box(p):
    return tuple(p["sel"]) if p["sel"] else union(p["boxes"])


def box_component(boxes, deg=0):
    """Bedrock allows a single collision box component; multiple boxes are merged into their union."""
    if not boxes: return False
    bs = [rot_box(b, deg) if deg else b for b in boxes]
    u = (min(b[0] for b in bs), min(b[1] for b in bs), min(b[2] for b in bs),
         max(b[3] for b in bs), max(b[4] for b in bs), max(b[5] for b in bs))
    return bbox_component(u)


# ------------------------------------------------------------------ emitters
def decoplanar(boxes, eps=0.02):
    """Avoid z-fighting: where two boxes have same-facing faces on the same plane (a drawer-front box laid over a
    carcass), pull the bigger box's face back by eps so the smaller one wins.  Collision uses the original boxes."""
    bs = [list(b) for b in boxes]
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            A, Bx = bs[i], bs[j]
            for ax in range(3):
                o1, o2 = [k for k in range(3) if k != ax]
                lo = lambda b, k: b[1 + k]; hi = lambda b, k: b[4 + k]
                if min(hi(A, o1), hi(Bx, o1)) - max(lo(A, o1), lo(Bx, o1)) <= 0: continue
                if min(hi(A, o2), hi(Bx, o2)) - max(lo(A, o2), lo(Bx, o2)) <= 0: continue
                area = lambda b: (hi(b, o1) - lo(b, o1)) * (hi(b, o2) - lo(b, o2))
                big = A if area(A) >= area(Bx) else Bx
                for side in (1, 4):
                    if A[side + ax] == Bx[side + ax]:
                        big[side + ax] += eps if side == 1 else -eps
    return [tuple(b) for b in bs]


def geometry(p):
    cubes = []
    for box in decoplanar(p["boxes"]):
        mat, x0, y0, z0, x1, y1, z1 = box
        uv = {}
        for f, name in FACES.items():
            m, fit = face_mat(mat, f)
            o, sz = face_uv(f, box, fit)
            uv[name] = {"uv": o, "uv_size": sz, "material_instance": m}
        cubes.append({"origin": [x0 - 8, y0, z0 - 8], "size": [x1 - x0, y1 - y0, z1 - z0], "uv": uv})
    return {"format_version": "1.21.0", "minecraft:geometry": [{
        "description": {"identifier": f"geometry.gx_furn_{p['id']}", "texture_width": TILE, "texture_height": TILE,
                        "visible_bounds_width": 2, "visible_bounds_height": 2, "visible_bounds_offset": [0, 0.5, 0]},
        "bones": [{"name": "body", "pivot": [0, 0, 0], "cubes": cubes}]}]}


def used_materials(p):
    out = []
    for box in p["boxes"]:
        for f in FACES:
            m, _ = face_mat(box[0], f)
            if m not in out: out.append(m)
    return out


def tile_color(mat):
    fn = materials.MATERIALS[mat][0]
    acc, n = [0, 0, 0], 0
    for y in range(0, TILE, 4):
        for x in range(0, TILE, 4):
            c = fn(x, y)
            if c is None: continue
            c = rgb(c)
            if c[3] < 128: continue
            for i in range(3): acc[i] += c[i]
            n += 1
    return "#%02x%02x%02x" % tuple(a // max(1, n) for a in acc)


def block(p):
    mats = used_materials(p)
    inst = {"*": {"texture": tex_key(mats[0]), "render_method": materials.MATERIALS[mats[0]][1]}}
    for m in mats:
        inst[m] = {"texture": tex_key(m), "render_method": materials.MATERIALS[m][1],
                   "ambient_occlusion": False, "face_dimming": True}
    comps = {
        "minecraft:geometry": f"geometry.gx_furn_{p['id']}",
        "minecraft:material_instances": inst,
        "minecraft:collision_box": box_component(collision_boxes(p)),
        "minecraft:selection_box": bbox_component(selection_box(p)),
        "minecraft:light_dampening": 0,
        "minecraft:destructible_by_mining": {"seconds_to_destroy": 0.6},
        "minecraft:destructible_by_explosion": {"explosion_resistance": 3},
        "minecraft:map_color": tile_color(max(mats, key=lambda m: sum(1 for b in p["boxes"] if face_mat(b[0], "u")[0] == m))),
    }
    if p["light"]: comps["minecraft:light_emission"] = p["light"]
    desc = {"identifier": bid(p),
            "menu_category": {"category": "construction", "group": GROUP, "is_hidden_in_commands": False}}
    perms = []
    if p["rot"]:
        desc["traits"] = {"minecraft:placement_direction": {"enabled_states": ["minecraft:cardinal_direction"]}}
        for d, deg in ROTS.items():
            perms.append({"condition": f"query.block_state('minecraft:cardinal_direction') == '{d}'",
                          "components": {"minecraft:transformation": {"rotation": [0, deg, 0]},
                                         "minecraft:collision_box": box_component(collision_boxes(p), deg),
                                         "minecraft:selection_box": bbox_component(rot_box(selection_box(p), deg))}})
    out = {"format_version": FORMAT, "minecraft:block": {"description": desc, "components": comps}}
    if perms: out["minecraft:block"]["permutations"] = perms
    return out


def emit_textures():
    used = sorted({m for p in pieces.PIECES for m in used_materials(p)})
    for m in used:
        fn = materials.MATERIALS[m][0]
        px = []
        for y in range(TILE):
            for x in range(TILE):
                c = fn(x, y)
                px.append((0, 0, 0, 0) if c is None else rgb(c))
        write_png(RP / f"textures/blocks/gx_furn/{m}.png", px, TILE, TILE)
    path = RP / "textures/terrain_texture.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.setdefault("resource_pack_name", "GalaxyForge")
    data.setdefault("texture_name", "atlas.terrain")
    data.setdefault("padding", 8)
    data.setdefault("num_mip_levels", 4)
    td = {k: v for k, v in data.get("texture_data", {}).items() if not k.startswith("gx_furn_")}
    for m in used: td[tex_key(m)] = {"textures": f"textures/blocks/gx_furn/{m}"}
    data["texture_data"] = dict(sorted(td.items()))
    lib.dump(path, data)
    return used


def run():
    ids = [p["id"] for p in pieces.PIECES]
    assert len(ids) == len(set(ids)), "duplicate furniture ids"
    used = emit_textures()
    for p in pieces.PIECES:
        lib.dump(BP / f"blocks/gx_{PREFIX}{p['id']}.json", block(p))
        lib.dump(RP / f"models/blocks/gx_{PREFIX}{p['id']}.geo.json", geometry(p))
        lib.lang(f"tile.{bid(p)}.name", p["name"])
    lib.lang("itemGroup.name.gx_home", "Galaxy Home")
    print(f"  furniture: {len(pieces.PIECES)} pieces, {len(used)} materials")
    return check()


# ------------------------------------------------------------------ validation
def check():
    errs = []
    terr = json.loads((RP / "textures/terrain_texture.json").read_text())["texture_data"]
    for p in pieces.PIECES:
        bp_path = BP / f"blocks/gx_{PREFIX}{p['id']}.json"
        geo_path = RP / f"models/blocks/gx_{PREFIX}{p['id']}.geo.json"
        try:
            b = json.loads(bp_path.read_text()); g = json.loads(geo_path.read_text())
        except Exception as e:
            errs.append(f"{p['id']}: {e}"); continue
        if not str(b.get("format_version", "")).startswith("1.21."): errs.append(f"{p['id']}: bad block format_version")
        mb = b["minecraft:block"]
        if mb["description"]["identifier"] != bid(p): errs.append(f"{p['id']}: identifier mismatch")
        comps = mb["components"]
        geo_id = g["minecraft:geometry"][0]["description"]["identifier"]
        if comps["minecraft:geometry"] != geo_id: errs.append(f"{p['id']}: geometry id mismatch")
        for name, inst in comps["minecraft:material_instances"].items():
            if inst["texture"] not in terr: errs.append(f"{p['id']}: texture {inst['texture']} not in terrain_texture.json")
        inst_names = set(comps["minecraft:material_instances"])
        for cube in g["minecraft:geometry"][0]["bones"][0]["cubes"]:
            o, s = cube["origin"], cube["size"]
            if not (-8 <= o[0] and o[0] + s[0] <= 8 and 0 <= o[1] and o[1] + s[1] <= 16 and -8 <= o[2] and o[2] + s[2] <= 8):
                errs.append(f"{p['id']}: cube outside the block {o} {s}")
            if min(s) <= 0: errs.append(f"{p['id']}: degenerate cube {o} {s}")
            for f in cube["uv"].values():
                if f["material_instance"] not in inst_names: errs.append(f"{p['id']}: unknown instance {f['material_instance']}")
        for key in ("minecraft:collision_box", "minecraft:selection_box"):
            cands = [comps[key]] + [pm["components"][key] for pm in mb.get("permutations", [])]
            for c in cands:
                if c is False: continue
                o, s = c["origin"], c["size"]
                if not (-8 <= o[0] and o[0] + s[0] <= 8 and 0 <= o[1] and o[1] + s[1] <= 16 and -8 <= o[2] and o[2] + s[2] <= 8):
                    errs.append(f"{p['id']}: {key} out of bounds {c}")
    for m in {m for p in pieces.PIECES for m in used_materials(p)}:
        if not (RP / f"textures/blocks/gx_furn/{m}.png").exists(): errs.append(f"missing texture {m}")
    if len(pieces.PIECES) < 50: errs.append(f"only {len(pieces.PIECES)} pieces")
    if errs:
        print("\n".join(errs), file=sys.stderr)
        if __name__ == "__main__": sys.exit(1)
    return errs


# ------------------------------------------------------------------ preview (front view, from +Z)
def preview(out, scale=4, cols=10):
    from lib import write_png
    n = len(pieces.PIECES); rows = (n + cols - 1) // cols; cell = 16 * scale + 4
    W, H = cols * cell, rows * cell
    img = [(30, 32, 40, 255)] * (W * H)
    for i, p in enumerate(pieces.PIECES):
        ox, oy = (i % cols) * cell + 2, (i // cols) * cell + 2
        for py in range(16 * scale):
            for px in range(16 * scale):
                x, y = px / scale, 16 - (py + .5) / scale
                best = None
                for box in p["boxes"]:
                    _, x0, y0, z0, x1, y1, z1 = box
                    if x0 <= x < x1 and y0 <= y < y1 and (best is None or z1 > best[0][6]): best = (box, z1)
                if not best: continue
                box = best[0]
                m, fit = face_mat(box[0], "s")
                o, sz = face_uv("s", box, fit)
                tx = o[0] + (x - box[1]) / max(1e-6, box[4] - box[1]) * sz[0] if fit else x * 2
                ty = o[1] + (box[5] - y) / max(1e-6, box[5] - box[2]) * sz[1] if fit else (16 - y) * 2
                c = materials.MATERIALS[m][0](int(min(TILE - 1, max(0, tx))), int(min(TILE - 1, max(0, ty))))
                if c is None: continue
                c = rgb(c)
                if c[3] < 255:
                    a = c[3] / 255; bg = img[(oy + py) * W + ox + px]
                    c = tuple(int(c[k] * a + bg[k] * (1 - a)) for k in range(3)) + (255,)
                img[(oy + py) * W + ox + px] = c
    write_png(Path(out), img, W, H)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check(); print("ok")
    elif "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1])
    else:
        run()
        print("Run python3 tools/creatures/build_all.py to add the lang entries to en_US.lang.")
