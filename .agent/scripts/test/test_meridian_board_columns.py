#!/usr/bin/env python3
"""Column mapping for kit HTML monitor (US-0196 / US-0198)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_board_columns import resolve_column  # noqa: E402


def main() -> int:
    cases = [
        ({"status": "❌", "ready": False, "inProgress": False}, "backlog"),
        ({"status": "❌", "ready": True, "inProgress": False}, "todo"),
        ({"status": "❌", "ready": True, "inProgress": True}, "doing"),
        ({"status": "🔶", "ready": True, "inProgress": True}, "doing"),
        ({"status": "🔶", "ready": True, "inProgress": False}, "🔶"),
        (
            {
                "status": "✅",
                "ready": True,
                "inProgress": False,
                "tests": "required",
                "testsStatus": "pending",
            },
            "🧪",
        ),
        ({"status": "✅", "ready": True, "tests": "none", "testsStatus": "n/a"}, "✅"),
        ({"status": "🧊"}, "🧊"),
        ({"status": "🚫"}, "🚫"),
    ]
    for story, expected in cases:
        got = resolve_column(story)
        assert got == expected, f"{story} -> {got!r} expected {expected!r}"
    print("OK: board column mapping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
