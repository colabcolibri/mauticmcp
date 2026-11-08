#!/usr/bin/env python3
"""Remove legacy delivery Markdown/JSON after verified SQLite migration (US-0123)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import delivery_md_paths  # noqa: E402


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Purge delivery .md/json (keeps phase docs)")
    parser.add_argument("package_root", nargs="?", default=".")
    parser.add_argument("--dry-run", action="store_true", help="List files only")
    parser.add_argument(
        "--require-verify",
        action="store_true",
        help="Run verify_md_sqlite_parity.py first; abort on failure",
    )
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    docs = root / "docs"

    if args.require_verify:
        verify_script = _SCRIPT_DIR / "verify_md_sqlite_parity.py"
        result = subprocess.run(
            [sys.executable, str(verify_script), str(root)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("ABORT: verify_md_sqlite_parity.py failed:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return 2

    paths = delivery_md_paths(docs)
    if not paths:
        print("No delivery markdown/json files to purge.")
        return 0

    print(f"{'Would delete' if args.dry_run else 'Deleting'} {len(paths)} file(s):")
    for path in paths:
        rel = path.relative_to(root)
        print(f"  {rel}")
        if not args.dry_run:
            path.unlink()

    if not args.dry_run:
        for folder in ("us", "epics", "versions", "sprints"):
            d = docs / folder
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
                print(f"Removed empty directory {d.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
