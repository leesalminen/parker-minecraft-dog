#!/usr/bin/env python3
"""Seed the Galaxy Pup textures + pack icons.

This is a one-shot starting point. Once textures are painted in Blockbench,
they are the source of truth, so this refuses to overwrite unless --force.
"""
import random
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RP = ROOT / "packs" / "GalaxyPup_RP"
BP = ROOT / "packs" / "GalaxyPup_BP"

WHITE = (244, 244, 244, 255)
SHADE = (224, 224, 226, 255)
GRAY = (196, 196, 200, 255)
DARK = (140, 140, 148, 255)
BLACK = (27, 27, 32, 255)
CLEAR = (0, 0, 0, 0)


def write_png(path, px, w, h):
    raw = b"".join(
        b"\x00" + b"".join(bytes(px[y * w + x]) for x in range(w)) for y in range(h)
    )

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


class Canvas:
    def __init__(self, w, h, fill=CLEAR):
        self.w, self.h = w, h
        self.px = [fill] * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = c

    def save(self, path):
        write_png(path, self.px, self.w, self.h)


def fur(rng, base=WHITE):
    return base if rng.random() < 0.8 else SHADE


def paint_box(cv, u, v, size, paint):
    """Paint a Bedrock box-UV net. paint(face, x, y, fw, fh) -> RGBA.

    Net layout (d = depth): [ top | bottom ] over [ side_r | front | side_l | back ].
    Front is the -Z face (where the pup looks). side_r's column fw-1 and side_l's
    column 0 touch the front face.
    """
    w, h, d = size
    faces = {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "side_r": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "side_l": (u + d + w, v + d, d, h),
        "back": (u + 2 * d + w, v + d, w, h),
    }
    for face, (fx, fy, fw, fh) in faces.items():
        for y in range(fh):
            for x in range(fw):
                cv.set(fx + x, fy + y, paint(face, x, y, fw, fh))


def head_face(x, y):
    """Head front (10x9). Black band across rows 2-3; the muzzle covers cols 2-7, rows 4-8."""
    return BLACK if 2 <= y <= 3 else None


def muzzle_face(x, y):
    """Muzzle front (6x5). Black nose stripe down the middle; with the band it forms the T."""
    return BLACK if 2 <= x <= 3 and y <= 2 else None


def gen_entity(rng):
    cv = Canvas(64, 64)

    def head(face, x, y, fw, fh):
        if face == "front":
            return head_face(x, y) or fur(rng)
        if face == "top":
            return fur(rng, SHADE)
        if face == "bottom":
            return GRAY
        return fur(rng)

    def muzzle(face, x, y, fw, fh):
        if face == "front":
            return muzzle_face(x, y) or WHITE
        if face == "top" and 2 <= x <= 3:
            return BLACK  # nose bridge running back to the band
        return GRAY if face == "bottom" else fur(rng)

    def ear(face, x, y, fw, fh):
        if face == "top" or y == 0:
            return DARK
        return GRAY if face == "front" else WHITE

    def leg(face, x, y, fw, fh):
        if face == "bottom":
            return GRAY
        if face == "top":
            return WHITE
        return BLACK if y == 7 else fur(rng)

    def tail(face, x, y, fw, fh):
        if face in ("side_r", "side_l") and x == 4 or face in ("top", "bottom") and y == 4:
            return BLACK
        return GRAY if face == "back" else fur(rng)

    def body(face, x, y, fw, fh):
        if face == "top":
            return fur(rng, SHADE)
        if face == "bottom":
            return GRAY
        if face in ("side_r", "side_l") and y >= fh - 2:
            return SHADE
        return fur(rng)

    paint_box(cv, 0, 0, (10, 9, 7), head)
    paint_box(cv, 34, 0, (6, 5, 4), muzzle)
    paint_box(cv, 56, 0, (2, 3, 2), ear)
    paint_box(cv, 0, 16, (8, 7, 14), body)
    paint_box(cv, 46, 16, (3, 11, 3), leg)
    paint_box(cv, 0, 40, (2, 2, 8), tail)
    return cv


TREAT = [
    "................",
    "..........*.....",
    ".........*#*....",
    "..........*.....",
    "...##...........",
    "..#pp#..........",
    "..#ppP#.........",
    "...#pPP#........",
    "....#pPP#.......",
    ".....#pPP#..##..",
    "......#pPP##pp#.",
    ".......#pPPPPp#.",
    "........#PPPP#..",
    ".......#pPPP#...",
    ".......#pp##....",
    "........##......",
]


def gen_treat():
    cv = Canvas(16, 16)
    colors = {"#": (90, 40, 110, 255), "p": (250, 200, 235, 255),
              "P": (214, 120, 200, 255), "*": (255, 230, 120, 255)}
    for y, row in enumerate(TREAT):
        for x, ch in enumerate(row):
            if ch in colors:
                cv.set(x, y, colors[ch])
    return cv


def gen_icon(rng):
    """64x64: the pup's face on a starfield."""
    cv = Canvas(64, 64)
    for y in range(64):
        for x in range(64):
            t = y / 63
            cv.set(x, y, (int(30 + 40 * t), int(18 + 10 * t), int(70 + 50 * t), 255))
    for _ in range(40):
        cv.set(rng.randrange(64), rng.randrange(64), (255, 255, 220, 255))
    s, ox, oy = 5, 7, 12  # 10x9 face at 5x

    def block(x, y, c, h=s):
        for dy in range(h):
            for dx in range(s):
                cv.set(ox + x * s + dx, oy + y * s + dy, c)

    for y in range(9):
        for x in range(10):
            block(x, y, head_face(x, y) or WHITE)
    for y in range(5):
        for x in range(6):
            block(x + 2, y + 4, muzzle_face(x, y) or WHITE)
    for ex in (0, 8):
        for x in range(2):
            for dy in range(6):
                for dx in range(s):
                    cv.set(ox + (ex + x) * s + dx, oy - 6 + dy, DARK if dy < 2 else WHITE)
    return cv


def main():
    force = "--force" in sys.argv
    rng = random.Random(7)
    outputs = {
        RP / "textures/entity/galaxy_pup.png": gen_entity(rng),
        RP / "textures/items/galaxy_treat.png": gen_treat(),
    }
    icon = gen_icon(random.Random(3))
    outputs[RP / "pack_icon.png"] = icon
    outputs[BP / "pack_icon.png"] = icon
    for path, cv in outputs.items():
        if path.exists() and not force:
            print(f"skip {path.relative_to(ROOT)} (exists; --force to overwrite)")
            continue
        cv.save(path)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
