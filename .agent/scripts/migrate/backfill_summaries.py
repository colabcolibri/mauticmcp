#!/usr/bin/env python3
"""Backfill summary column for delivery artifacts (US-0118)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import backfill_summaries, bootstrap, db_exists  # noqa: E402


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Backfill summary fields in meridian.db")
    parser.add_argument("package_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    if not db_exists(root):
        bootstrap(root)
    counts = backfill_summaries(root)
    for key, value in counts.items():
        print(f"{key}: {value} summaries written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
