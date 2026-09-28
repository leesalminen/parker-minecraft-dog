"""Synthesised firearm sounds for the realistic weapons: RP/sounds/gx/*.ogg plus
RP/sounds/sound_definitions.json.

Vanilla has no gunshot, so each class gets a layered synthetic report: a sharp supersonic
crack (short white-noise burst), a filtered muzzle blast, a low pitch-dropping thump, and a
decaying tail with a slap-back echo.  Mechanical sounds (bolt, pump, brass, minigun motor)
and launcher / explosion sounds use the same building blocks.

Pure stdlib synthesis; ffmpeg (libvorbis) encodes.  .ogg files are committed, so a build
only re-synthesises when a file is missing or GX_SOUNDS=1 is set.
"""
import math
import os
import random
import shutil
import struct
import subprocess
import zlib

from lib import RP, dump

SR = 44100
OUT = RP / "sounds" / "gx"
VERSION = 1


# ------------------------------------------------------------------ building blocks
def buf(sec):
    return [0.0] * int(SR * sec)


def lowpass(x, cutoff):
    a = 1 - math.exp(-2 * math.pi * cutoff / SR)
    y, out = 0.0, []
    for v in x:
        y += a * (v - y)
        out.append(y)
    return out


def highpass(x, cutoff):
    lp = lowpass(x, cutoff)
    return [a - b for a, b in zip(x, lp)]


def noise(n, rng):
    return [rng.uniform(-1, 1) for _ in range(n)]


def add(dst, src, at=0.0, gain=1.0):
    i0 = int(at * SR)
    for i, v in enumerate(src):
        j = i0 + i
        if j >= len(dst):
            break
        dst[j] += v * gain


def env_exp(n, tau, attack=0.0005):
    a = max(1, int(attack * SR))
    return [(i / a if i < a else 1.0) * math.exp(-(i / SR) / tau) for i in range(n)]


def burst(sec, tau, cutoff, rng, hp=None, attack=0.0005):
    n = int(sec * SR)
    x = lowpass(noise(n, rng), cutoff)
    if hp:
        x = highpass(x, hp)
    e = env_exp(n, tau, attack)
    return [a * b for a, b in zip(x, e)]


def thump(sec, f0, f1, tau, drop=0.03):
    n = int(sec * SR)
    out, ph = [], 0.0
    for i in range(n):
        t = i / SR
        f = f1 + (f0 - f1) * math.exp(-t / drop)
        ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * math.exp(-t / tau))
    return out


def ring(sec, f, tau):
    return [math.sin(2 * math.pi * f * i / SR) * math.exp(-(i / SR) / tau) for i in range(int(sec * SR))]


def click(rng, f=3200, tau=0.012, gain=1.0):
    out = burst(0.03, 0.003, 9000, rng, hp=1500)
    add(out, ring(0.05, f, tau), 0, 0.5)
    return [v * gain for v in out]


def finish(x, drive=1.6, peak=0.95):
    x = [math.tanh(v * drive) for v in x]
    m = max(1e-6, max(abs(v) for v in x))
    x = [v / m * peak for v in x]
    fade = int(0.01 * SR)
    for i in range(1, fade + 1):
        x[-i] *= i / fade
    return x


# ------------------------------------------------------------------ recipes
def gunshot(rng, crack=0.8, blast_cut=2600, blast_tau=0.05, boom=(140, 55), boom_gain=0.8,
            boom_tau=0.09, tail_tau=0.35, tail_gain=0.25, echo=0.22, echo_gain=0.25, sec=1.2,
            mech=None):
    x = buf(sec)
    add(x, burst(0.02, 0.0025, 12000, rng, hp=2500), 0, crack)            # supersonic crack
    add(x, burst(0.4, blast_tau, blast_cut, rng), 0.0005, 1.0)             # muzzle blast
    add(x, thump(0.5, boom[0], boom[1], boom_tau), 0, boom_gain)           # low thump
    add(x, burst(sec, tail_tau, 900, rng, attack=0.03), 0.02, tail_gain)   # tail
    if echo:
        add(x, burst(0.5, blast_tau * 2, blast_cut * 0.5, rng), echo, echo_gain)
    if mech:
        for at, f in mech:
            add(x, click(rng, f), at, 0.35)
    return finish(x)


def rocket(rng):
    x = buf(2.2)
    add(x, thump(0.4, 110, 45, 0.12), 0, 1.0)
    add(x, burst(0.3, 0.06, 2000, rng), 0, 0.9)
    n = int(1.8 * SR)
    hiss = lowpass(highpass(noise(n, rng), 500), 3500)
    e = [min(1.0, i / (0.05 * SR)) * math.exp(-(i / SR) / 0.7) for i in range(n)]
    add(x, [a * b for a, b in zip(hiss, e)], 0.03, 0.8)
    return finish(x, drive=1.3)


def explosion(rng, sec=3.0):
    x = buf(sec)
    add(x, burst(0.05, 0.01, 9000, rng, hp=800), 0, 0.9)
    add(x, burst(sec, 0.5, 450, rng, attack=0.004), 0, 1.4)
    add(x, thump(1.5, 70, 28, 0.6, drop=0.1), 0, 1.0)
    add(x, burst(sec, 0.9, 220, rng, attack=0.1), 0.15, 0.8)                # rumble
    return finish(x, drive=2.2)


def launcher_pop(rng):
    x = buf(0.8)
    add(x, thump(0.4, 220, 70, 0.08, drop=0.02), 0, 1.0)
    add(x, burst(0.3, 0.03, 1500, rng), 0, 0.6)
    add(x, click(rng, 2400), 0.0, 0.3)
    return finish(x, drive=1.4)


def bolt_cycle(rng):
    x = buf(0.7)
    for at, f in ((0.0, 2800), (0.12, 3400), (0.34, 2600), (0.46, 3900)):
        add(x, click(rng, f), at, 1.0)
    add(x, burst(0.2, 0.05, 3000, rng, hp=900), 0.14, 0.25)
    return finish(x, drive=1.1, peak=0.7)


def pump_cycle(rng):
    x = buf(0.6)
    for at in (0.0, 0.22):
        add(x, burst(0.12, 0.04, 2500, rng, hp=400), at, 0.6)
        add(x, click(rng, 1900, 0.02), at + 0.08, 1.0)
    return finish(x, drive=1.2, peak=0.75)


def brass(rng):
    x = buf(0.5)
    for at, f in ((0.0, 5200), (0.08, 6100), (0.15, 5600), (0.21, 6600)):
        add(x, ring(0.12, f + rng.uniform(-200, 200), 0.025), at, 0.5 * (1 - at))
    return finish(x, drive=1.0, peak=0.5)


def spin_up(rng):
    n = int(1.0 * SR)
    out, ph = [], 0.0
    for i in range(n):
        t = i / SR
        f = 120 + 520 * (1 - math.exp(-t / 0.35))
        ph += 2 * math.pi * f / SR
        out.append((math.sin(ph) + 0.4 * math.sin(3 * ph) + 0.2 * math.sin(5 * ph))
                   * min(1.0, t / 0.05) * (0.6 + 0.4 * min(1, t / 0.6)))
    add(out, lowpass(noise(n, rng), 1500), 0, 0.15)
    return finish(out, drive=1.0, peak=0.6)


SOUNDS = {
    # id suffix: (generator, variants)
    "pistol": (lambda r: gunshot(r, crack=0.7, blast_cut=3200, blast_tau=0.03, boom=(180, 80),
                                 boom_gain=0.5, tail_tau=0.18, tail_gain=0.15, echo=0.16,
                                 echo_gain=0.15, sec=0.8), 3),
    "magnum": (lambda r: gunshot(r, crack=1.0, blast_cut=2200, blast_tau=0.07, boom=(130, 50),
                                 boom_gain=1.0, tail_tau=0.4, tail_gain=0.3, echo=0.25,
                                 echo_gain=0.3, sec=1.4), 2),
    "smg": (lambda r: gunshot(r, crack=0.5, blast_cut=3600, blast_tau=0.025, boom=(200, 90),
                              boom_gain=0.4, tail_tau=0.12, tail_gain=0.1, echo=0.12,
                              echo_gain=0.1, sec=0.5), 3),
    "rifle": (lambda r: gunshot(r, crack=1.0, blast_cut=3000, blast_tau=0.035, boom=(160, 60),
                                boom_gain=0.6, tail_tau=0.22, tail_gain=0.18, echo=0.18,
                                echo_gain=0.18, sec=0.8), 3),
    "rifle_heavy": (lambda r: gunshot(r, crack=1.0, blast_cut=2400, blast_tau=0.05, boom=(140, 50),
                                      boom_gain=0.8, tail_tau=0.3, tail_gain=0.22, echo=0.2,
                                      echo_gain=0.22, sec=1.0), 3),
    "sniper": (lambda r: gunshot(r, crack=1.2, blast_cut=2000, blast_tau=0.08, boom=(120, 40),
                                 boom_gain=1.0, tail_tau=0.7, tail_gain=0.35, echo=0.45,
                                 echo_gain=0.35, sec=2.0), 2),
    "fifty": (lambda r: gunshot(r, crack=1.3, blast_cut=1600, blast_tau=0.12, boom=(90, 32),
                                boom_gain=1.3, boom_tau=0.16, tail_tau=0.9, tail_gain=0.45,
                                echo=0.5, echo_gain=0.4, sec=2.4), 2),
    "shotgun": (lambda r: gunshot(r, crack=0.6, blast_cut=1800, blast_tau=0.09, boom=(110, 45),
                                  boom_gain=1.1, boom_tau=0.12, tail_tau=0.45, tail_gain=0.3,
                                  echo=0.3, echo_gain=0.3, sec=1.4), 2),
    "minigun": (lambda r: gunshot(r, crack=0.6, blast_cut=3400, blast_tau=0.018, boom=(190, 90),
                                  boom_gain=0.4, tail_tau=0.06, tail_gain=0.08, echo=0,
                                  sec=0.25), 3),
    "rocket": (rocket, 2),
    "explosion": (explosion, 2),
    "launcher": (launcher_pop, 2),
    "bolt": (bolt_cycle, 1),
    "pump": (pump_cycle, 1),
    "brass": (brass, 3),
    "spin": (spin_up, 1),
}


def _encode(samples, path):
    pcm = b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32000)) for v in samples)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1",
                    "-i", "pipe:0", "-c:a", "libvorbis", "-q:a", "5", str(path)],
                   input=pcm, check=True)


def write_sounds():
    """Synthesise missing .ogg files and write sound_definitions.json. Returns sound ids."""
    OUT.mkdir(parents=True, exist_ok=True)
    force = os.environ.get("GX_SOUNDS") == "1"
    have_ffmpeg = shutil.which("ffmpeg") is not None
    defs = {}
    for name, (gen, variants) in SOUNDS.items():
        files = []
        for v in range(variants):
            path = OUT / f"{name}_{v}.ogg"
            if force or not path.exists():
                if not have_ffmpeg:
                    raise SystemExit(f"ffmpeg is needed to synthesise {path.name}")
                _encode(gen(random.Random(zlib.crc32(f"{name}:{v}:{VERSION}".encode()))), path)
            files.append({"name": f"sounds/gx/{name}_{v}", "volume": 1.0, "load_on_low_memory": True})
        defs[f"gx.gun.{name}"] = {"category": "player", "min_distance": 6.0, "max_distance": 96.0,
                                  "sounds": files}
    dump(RP / "sounds" / "sound_definitions.json",
         {"format_version": "1.20.20", "sound_definitions": defs})
    return sorted(defs)
