#!/usr/bin/env python3
"""Regenerate every GalaxyForge creature/extra into packs/GalaxyForge_{BP,RP}. Run from repo root."""
import importlib, pkgutil, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

def main():
    only = set(sys.argv[1:])
    specs = []
    import specs as pkg
    for m in pkgutil.iter_modules(pkg.__path__):
        mod = importlib.import_module(f"specs.{m.name}")
        for s in getattr(mod, "SPECS", [getattr(mod, "SPEC", None)]):
            if s: specs.append(s)
    for s in specs:
        if only and s["id"] not in only: continue
        size = lib.emit(s)
        lib.lang(f"entity.{lib.NS}:{s['id']}.name", s["name"])
        lib.lang(f"item.spawn_egg.entity.{lib.NS}:{s['id']}.name", f"{s['name']} Spawn Egg")
        print(f"  {s['id']:<18} tex {size}x{size}  {s['name']}")
    lib.sounds_and_lang(specs)
    try:
        import extras
        for m in pkgutil.iter_modules(extras.__path__):
            importlib.import_module(f"extras.{m.name}").run()
    except ImportError:
        pass
    # Galaxy Forge weapon engine (items, attachables, models, particles, glyphs, scripts)
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "weapons"))
    import build_weapons
    build_weapons.run()
    lib.dump(lib.RP / "textures/item_texture.json", {"resource_pack_name": "GalaxyForge", "texture_name": "atlas.items",
             "texture_data": {k: {"textures": v} for k, v in lib.ITEM_TEX.items()}})
    (lib.RP / "texts").mkdir(parents=True, exist_ok=True)
    (lib.RP / "texts/en_US.lang").write_text("".join(f"{k}={v}\n" for k, v in sorted(lib.LANG.items())))
    (lib.RP / "texts/languages.json").write_text('["en_US"]\n')
    print(f"{len(specs)} creatures")

if __name__ == "__main__":
    main()
