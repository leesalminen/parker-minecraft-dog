#!/usr/bin/env python3
"""Preview the toy-car specs (multi-spec modules): toycars_preview.py <module> <id> <out.png> [--pose json]"""
import importlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib, preview

def main():
    a = sys.argv[1:]
    mod = importlib.import_module(f"specs.{a[0]}")
    spec = next(s for s in mod.SPECS if s["id"] == a[1])
    pose = json.loads(a[a.index("--pose") + 1]) if "--pose" in a else {}
    views = [(0, -10), (90, -10), (180, -10), (35, -22)]
    tiles = [preview.render(spec, yw, pt, pose) for yw, pt in views]
    W, H = tiles[0][1], tiles[0][2]
    sheet = [(0, 0, 0, 0)] * (W * 2 * H * 2)
    for i, (img, _, _) in enumerate(tiles):
        ox, oy = (i % 2) * W, (i // 2) * H
        for y in range(H):
            sheet[(oy + y) * W * 2 + ox:(oy + y) * W * 2 + ox + W] = img[y * W:(y + 1) * W]
    lib.write_png(Path(a[2]), sheet, W * 2, H * 2)
    print("wrote", a[2])
main()
