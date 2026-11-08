#!/usr/bin/env python3
"""Story narrative compaction for kit HTML board (parity with extension)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_UI = _SCRIPT_DIR.parents[1] / "board-ui" / "js" / "story-narrative.js"


def _load_compact_source() -> str:
    return _UI.read_text(encoding="utf-8")


def main() -> int:
    src = _load_compact_source()
    assert "compactStoryNarrative" in src
    assert "US-\\d{4}" in src or "US-\\\\d{4}" in src
    sample = """**As** Process Manager,
**I want** to open the Meridian app locally,
**so that** I can start operating the development flow with visibility."""
    text = sample.strip()
    text = re.sub(r"^#\s+US-\d{4}\s*[—-]\s*.+\n?", "", text, flags=re.I)
    text = text.replace("**", "")
    text = re.sub(r"\s+", " ", text).strip()
    assert "Process Manager" in text
    assert "I want" in text
    assert "so that" in text
    assert "US-0001" not in text
    print("OK: story narrative")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
