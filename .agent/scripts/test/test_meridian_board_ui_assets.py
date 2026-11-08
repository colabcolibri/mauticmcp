#!/usr/bin/env python3
"""Static kit HTML monitor assets (US-0197 / US-0203)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "board-ui"


def main() -> int:
    tokens = (UI / "css" / "tokens.css").read_text(encoding="utf-8")
    assert "appearance: none" in tokens
    assert "color-scheme: dark" in tokens
    layout = (UI / "css" / "layout.css").read_text(encoding="utf-8")
    assert "100dvh" in layout
    assert "overflow: hidden" in layout
    assert "#view-root.view-board" in layout
    board = (UI / "css" / "board.css").read_text(encoding="utf-8")
    assert ".board-track" in board
    assert ".card-narrative" in board
    assert "font-size: 16px" in (UI / "css" / "markdown.css").read_text(encoding="utf-8")
    assert ".md-lane" in (UI / "css" / "markdown.css").read_text(encoding="utf-8")
    assert (UI / "js" / "md-structure.js").is_file()
    assert "flex: 1 1 auto" in board
    index = (UI / "index.html").read_text(encoding="utf-8")
    assert "js/app.js" in index
    assert 'id="toggle-narrative"' in index
    assert "vendor/mermaid.min.js" in index
    assert 'id="filter-sheet"' in index
    assert 'id="detail-sheet"' in index
    app_js = (UI / "js" / "app.js").read_text(encoding="utf-8")
    assert 'detail.entity === "decision"' in app_js
    lists = (UI / "js" / "render-lists.js").read_text(encoding="utf-8")
    assert "data-decision-date" in lists
    assert "renderDecisionDetail" in lists
    for name in ("marked.min.js", "purify.min.js", "mermaid.min.js"):
        path = UI / "vendor" / name
        assert path.is_file() and path.stat().st_size > 1000, path
    print("OK: board-ui assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
