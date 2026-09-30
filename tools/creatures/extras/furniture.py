"""Hook: Galaxy Home furniture (see tools/furniture/build_furniture.py and docs/furniture.md)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "furniture"))


def run():
    import build_furniture
    errs = build_furniture.run()
    if errs:
        raise SystemExit("furniture validation failed")
