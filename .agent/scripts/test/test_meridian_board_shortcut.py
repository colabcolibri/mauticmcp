#!/usr/bin/env python3
"""Human shortcut .agent/board delegates to meridian_board_serve.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_AGENT = Path(__file__).resolve().parents[2]
_SHORTCUT = _AGENT / "board"


def main() -> int:
    assert _SHORTCUT.is_file()
    result = subprocess.run(
        [sys.executable, str(_SHORTCUT), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Serve the Meridian HTML delivery monitor" in result.stdout
    print("OK: .agent/board --help")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
