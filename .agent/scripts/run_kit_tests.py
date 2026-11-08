#!/usr/bin/env python3
"""Run all kit tests under test/test_*.py — used by CI and local dev."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_TEST_DIR = _SCRIPT_DIR / "test"


def main() -> int:
    tests = sorted(_TEST_DIR.glob("test_*.py"))
    if not tests:
        print("No test files found", file=sys.stderr)
        return 1

    failed: list[str] = []
    for path in tests:
        print(f"--- {path.name} ---")
        result = subprocess.run([sys.executable, str(path)], cwd=_SCRIPT_DIR)
        if result.returncode != 0:
            failed.append(path.name)

    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1

    print(f"OK: all {len(tests)} kit tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
