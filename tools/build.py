#!/usr/bin/env python3
"""Validate the packs and zip them into dist/*.mcaddon.

Checks JSON validity, manifest links, the Galaxy Pup creature assets, and — for the
Galaxy Forge weapon engine — the script module, the pinned stable @minecraft/server
dependency, and that every weapon has its item, attachable, model, textures, icon,
lang entry and recipe.

Double-clicking the .mcaddon on Windows imports both packs into Minecraft.
"""
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
DIST = ROOT / "dist"

sys.path.insert(0, str(ROOT / "tools" / "creatures"))
sys.path.insert(0, str(ROOT / "tools" / "weapons"))

GF_BP = PACKS / "GalaxyForge_BP"
GF_RP = PACKS / "GalaxyForge_RP"


def weapon_checks(errors):
    try:
        import build_weapons
        defs = build_weapons.load_defs()
    except Exception as e:  # pragma: no cover - reported, not raised
        errors.append(f"cannot load weapon defs: {e}")
        return

    lang = (GF_RP / "texts/en_US.lang").read_text() if (GF_RP / "texts/en_US.lang").exists() else ""
    atlas = json.loads((GF_RP / "textures/item_texture.json").read_text())["texture_data"]

    for d in defs:
        wid = d["id"]
        ident = f"gx:{wid}"
        if not (GF_BP / f"items/{wid}.json").exists():
            errors.append(f"weapon {wid}: missing item JSON")
        if not (GF_RP / f"attachables/{wid}.json").exists():
            errors.append(f"weapon {wid}: missing attachable")
        if not (GF_RP / f"models/entity/gx_{wid}.geo.json").exists():
            errors.append(f"weapon {wid}: missing held model geometry")
        if not (GF_RP / f"textures/entity/gx_{wid}.png").exists():
            errors.append(f"weapon {wid}: missing held model texture")
        if not (GF_RP / f"textures/items/gx_{wid}.png").exists():
            errors.append(f"weapon {wid}: missing 16x16 icon")
        if f"gx_{wid}" not in atlas:
            errors.append(f"weapon {wid}: icon not registered in item_texture.json")
        if not (GF_BP / f"recipes/{wid}.json").exists():
            errors.append(f"weapon {wid}: missing recipe")
        if f"item.{ident}=" not in lang:
            errors.append(f"weapon {wid}: missing lang name")
        if f"item.{ident}.desc=" not in lang:
            errors.append(f"weapon {wid}: missing lang description")

    if len(defs) != 73:
        errors.append(f"weapon roster: expected 73, found {len(defs)}")
    if not (GF_RP / "font/glyph_E2.png").exists():
        errors.append("missing font/glyph_E2.png (run tools/creatures/build_all.py)")
    if not (GF_RP / "textures/particle/gx_particles.png").exists():
        errors.append("missing particle atlas (run tools/creatures/build_all.py)")
    if not (GF_BP / "scripts/generated/weapons.js").exists():
        errors.append("missing scripts/generated/weapons.js (run tools/creatures/build_all.py)")
    if not (GF_BP / "scripts/main.js").exists():
        errors.append("missing scripts/main.js")
    for f in (GF_BP / "scripts").rglob("*.js"):
        try:
            text = f.read_text()
        except Exception as e:
            errors.append(f"{f.relative_to(ROOT)}: {e}")
            continue
        if "require(" in text or "module.exports" in text:
            errors.append(f"{f.relative_to(ROOT)}: CommonJS require/module.exports in an ES module pack")
    if not any((GF_RP / "particles").glob("*.json")):
        errors.append("no particle definitions emitted")


def galaxyforge_checks(errors):
    bp = json.loads((GF_BP / "manifest.json").read_text())
    rp = json.loads((GF_RP / "manifest.json").read_text())
    if bp["header"]["version"] != rp["header"]["version"]:
        errors.append("GalaxyForge BP/RP versions differ; bump both together")
    if bp["dependencies"][0]["uuid"] != rp["header"]["uuid"]:
        errors.append("GalaxyForge BP dependency does not point at RP header uuid")
    if rp["dependencies"][0]["uuid"] != bp["header"]["uuid"]:
        errors.append("GalaxyForge RP dependency does not point at BP header uuid")
    if (bp["dependencies"][0]["version"] != rp["header"]["version"]
            or rp["dependencies"][0]["version"] != bp["header"]["version"]):
        errors.append("GalaxyForge BP/RP dependency versions must equal the header versions "
                      "(use tools/bump.py)")

    scripts = [m for m in bp["modules"] if m.get("type") == "script"]
    if not scripts:
        errors.append("GalaxyForge BP manifest has no script module")
    else:
        if scripts[0].get("entry") != "scripts/main.js":
            errors.append("script module entry must be scripts/main.js")
        if scripts[0].get("language") != "javascript":
            errors.append("script module language must be javascript")
    server = [d for d in bp["dependencies"] if d.get("module_name") == "@minecraft/server"]
    if not server:
        errors.append("GalaxyForge BP does not depend on @minecraft/server")
    elif "-beta" in str(server[0]["version"]):
        errors.append("@minecraft/server dependency must be a stable (non-beta) version")

    weapon_checks(errors)


def pup_checks(errors):
    bp = json.loads((PACKS / "GalaxyPup_BP/manifest.json").read_text())
    rp = json.loads((PACKS / "GalaxyPup_RP/manifest.json").read_text())
    if bp["dependencies"][0]["uuid"] != rp["header"]["uuid"]:
        errors.append("Pup BP dependency does not point at RP header uuid")
    if rp["dependencies"][0]["uuid"] != bp["header"]["uuid"]:
        errors.append("Pup RP dependency does not point at BP header uuid")
    if bp["header"]["version"] != rp["header"]["version"]:
        errors.append("Pup BP/RP versions differ; bump both together")
    for png in ("GalaxyPup_RP/textures/entity/galaxy_pup.png",
                "GalaxyPup_RP/textures/items/galaxy_treat.png"):
        if not (PACKS / png).exists():
            errors.append(f"missing {png} (run tools/gen_textures.py)")


def build_mcaddon(name, dirs):
    out = DIST / f"{name}.mcaddon"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for d in dirs:
            for f in sorted((PACKS / d).rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(PACKS))
    return out


def main():
    errors = []
    for f in sorted(PACKS.rglob("*.json")):
        try:
            json.loads(f.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{f.relative_to(ROOT)}: {e}")

    pup_checks(errors)
    galaxyforge_checks(errors)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    out = build_mcaddon("GalaxyPup", ["GalaxyPup_BP", "GalaxyPup_RP"])
    gf = build_mcaddon("GalaxyForge", ["GalaxyForge_BP", "GalaxyForge_RP"])
    bp = json.loads((GF_BP / "manifest.json").read_text())
    print(f"built {out.relative_to(ROOT)} and {gf.relative_to(ROOT)} "
          f"(GalaxyForge v{'.'.join(map(str, bp['header']['version']))})")


if __name__ == "__main__":
    main()
