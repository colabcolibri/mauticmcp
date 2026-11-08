#!/usr/bin/env python3
"""Auto-bootstrap on delivery read commands when meridian.db is missing (US-0180)."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT = _SCRIPT_DIR.parents[2]


def main() -> int:
    if not (_REPO_ROOT / "docs" / "00_scope.md").exists():
        print("SKIP: dogfood docs not found", file=sys.stderr)
        return 0

    with tempfile.TemporaryDirectory(prefix="meridian-bootstrap-test-") as tmp:
        root = Path(tmp)
        shutil.copytree(_REPO_ROOT / "docs", root / "docs")
        db_path = root / ".meridian" / "meridian.db"
        if db_path.exists():
            db_path.unlink()

        delivery = _SCRIPTS_ROOT / "meridian_delivery.py"
        result = subprocess.run(
            [sys.executable, str(delivery), "counts", "--package-root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(result.stderr or result.stdout, file=sys.stderr)
            print("FAIL: counts should auto-bootstrap empty Meridian product", file=sys.stderr)
            return 1
        if not db_path.exists():
            print("FAIL: meridian.db was not created by auto-bootstrap", file=sys.stderr)
            return 1
        print("OK: delivery read auto-bootstrap test passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
