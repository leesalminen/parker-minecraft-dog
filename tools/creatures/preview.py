#!/usr/bin/env python3
"""Render a creature spec to a PNG contact sheet (front / side / back / 3-4 view) without launching the game.
usage: preview.py <spec_module_name> <out.png> [--pose '{"bone":[rx,ry,rz]}'] [--sheet]   (run from repo root)
Pose values are degrees, applied on top of bind pose. Rotation order: X, then Y, then Z. Sign convention for Y/Z is
approximate; +X rotation swings a bone's front (-Z side) UP... check with a test if you depend on it."""
import importlib, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

def load(name):
    m = importlib.import_module(f"specs.{name}")
    return m.SPEC

def rot(p, r, c):
    x, y, z = p[0] - c[0], p[1] - c[1], p[2] - c[2]
    a = math.radians(r[0]); y, z = y * math.cos(a) + z * math.sin(a), -y * math.sin(a) + z * math.cos(a)
    a = math.radians(r[1]); x, z = x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a)
    a = math.radians(r[2]); x, y = x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)
    return (x + c[0], y + c[1], z + c[2])

def num(v): return v if isinstance(v, (int, float)) else 0

def render(spec, yaw_deg, pitch_deg, pose, W=420, H=420):
    bones = json.loads(json.dumps(spec["bones"]))
    size = lib.pack_uvs(bones); tex = lib.make_texture(spec, bones, size)
    byname = {b["name"]: b for b in bones}
    def xf(p, name):
        while name:
            b = byname[name]
            r = [num(x) for x in b.get("rotation", [0, 0, 0])]
            q = pose.get(name)
            if q: r = [r[i] + q[i] for i in range(3)]
            p = rot(p, r, b.get("pivot", [0, 0, 0])); name = b.get("parent")
        return p
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    def cam(p):
        x, y, z = p
        x, z = x * math.cos(yaw) - z * math.sin(yaw), x * math.sin(yaw) + z * math.cos(yaw)
        y, z = y * math.cos(pitch) - z * math.sin(pitch), y * math.sin(pitch) + z * math.cos(pitch)
        return x, y, z
    pts = []
    N = 4
    for b in bones:
        for c in b.get("cubes", []):
            for face, (fx, fy, fw, fh) in lib.face_rects(c).items():
                for ty in range(fh):
                    for tx in range(fw):
                        col = tex[(fy + ty) * size + fx + tx]
                        if col[3] == 0: continue
                        for i in range(N):
                            for j in range(N):
                                p = lib.face_point(c, face, tx + (i + .5) / N, ty + (j + .5) / N)
                                if c.get("rot"): p = rot(p, c["rot"], c.get("pivot", [0, 0, 0]))
                                pts.append((cam(xf(p, b["name"])), col))
    xs = [p[0][0] for p in pts]; ys = [p[0][1] for p in pts]
    sc = min((W - 30) / max(1, max(xs) - min(xs)), (H - 30) / max(1, max(ys) - min(ys)))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    bg = (120, 170, 200, 255)
    img = [bg] * (W * H); zb = [1e9] * (W * H)
    k = max(1, int(sc * 0.25 + 0.99))
    for (x, y, z), col in pts:
        sx, sy = int(W / 2 + (x - cx) * sc), int(H / 2 - (y - cy) * sc)
        for dx in range(k):
            for dy in range(k):
                px, py = sx + dx, sy + dy
                if 0 <= px < W and 0 <= py < H and z < zb[py * W + px]:
                    zb[py * W + px] = z; img[py * W + px] = col
    return img, W, H

def main():
    a = sys.argv[1:]; name, out = a[0], Path(a[1])
    pose = json.loads(a[a.index("--pose") + 1]) if "--pose" in a else {}
    spec = load(name)
    views = [(0, -10), (90, -10), (180, -10), (35, -22)]   # front, side(+X), back, 3/4
    tiles = [render(spec, yw, pt, pose) for yw, pt in views]
    W, H = tiles[0][1], tiles[0][2]
    sheet = [(0, 0, 0, 0)] * (W * 2 * H * 2)
    for i, (img, _, _) in enumerate(tiles):
        ox, oy = (i % 2) * W, (i // 2) * H
        for y in range(H):
            row = img[y * W:(y + 1) * W]
            sheet[(oy + y) * W * 2 + ox: (oy + y) * W * 2 + ox + W] = row
    lib.write_png(out, sheet, W * 2, H * 2)
    print("wrote", out, "(views: front, side, back, 3/4)")

if __name__ == "__main__":
    main()
