#!/usr/bin/env python3
"""Bootstrap .meridian/meridian.db — thin shim. Canonical: meridian_delivery.py bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_db import bootstrap, is_meridian_package  # noqa: E402
from meridian_delivery_config import write_delivery_config  # noqa: E402


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Create or upgrade Meridian SQLite database for a product package"
    )
    parser.add_argument(
        "package_root",
        nargs="?",
        default=".",
        help="Folder containing docs/ (e.g. . for repo root dogfood)",
    )
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    if not is_meridian_package(root):
        print(f"ERROR: {root} is not a Meridian product (missing docs/ fingerprint).", file=sys.stderr)
        return 1
    try:
        print(bootstrap(root))
        cfg = write_delivery_config(root)
        print(f"delivery.json: connector={cfg['connector']}")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
