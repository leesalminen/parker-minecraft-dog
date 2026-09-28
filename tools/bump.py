"""Bump a BP/RP pair together and keep their cross-dependencies pointing at the new version.

  python3 tools/bump.py GalaxyForge 1.3.4

Bedrock resolves a pack dependency by uuid *and* version, so a dependency left at an old
version shows up as "Missing dependency" in Pack Info.
"""
import json
import sys
from pathlib import Path

PACKS = Path(__file__).resolve().parent.parent / "packs"


def main(name, version):
    ver = [int(v) for v in version.split(".")]
    paths = [PACKS / f"{name}_BP/manifest.json", PACKS / f"{name}_RP/manifest.json"]
    mans = [json.loads(p.read_text()) for p in paths]
    uuids = {m["header"]["uuid"] for m in mans}
    for p, m in zip(paths, mans):
        m["header"]["version"] = ver
        for d in m.get("dependencies", []):
            if d.get("uuid") in uuids:
                d["version"] = ver
        p.write_text(json.dumps(m, indent=2) + "\n")
    print(f"{name} -> {version}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
