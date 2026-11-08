#!/usr/bin/env python3
"""Seed minimal delivery data into a meridian-teste workspace (DB-only smoke)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    upsert_epic,
    upsert_user_story,
    upsert_version,
    record_board_snapshot,
)
from meridian_markdown_parse import extract_epic_sections, extract_us_sections, extract_version_sections  # noqa: E402

US_BODY = """# {id} — {title}

**As** tester,
**I want** {title_lower},
**so that** I can validate SQLite delivery.

## Intent

### Acceptance

- [ ] Observable outcome for {id}

### Why

Smoke data for meridian-teste database checks.

### Where

Version v1, epic EPIC-01.

## Plan

### Approach

- Validate upsert and depends_on junction.

## Record

### Files

- n/a

### Backend

- n/a

### Frontend

- n/a

### Scripts / Docs

- n/a

### Executed

- n/a

## Boundaries

### Out of scope for this story

- Product code

### Notes

- Test fixture only.
"""


def _us_markdown(story_id: str, title: str, depends: list[str]) -> tuple[dict, str]:
    from meridian_markdown_parse import format_depends_on

    fm = {
        "id": story_id,
        "title": title,
        "epic": "EPIC-01",
        "version": "v1",
        "status": "❌",
        "moscow": "Must",
        "depends_on": format_depends_on(depends),
        "ready": "false",
        "done_when": f"{story_id} seeded in meridian-teste.",
        "tests": "required",
        "tests_status": "pending",
    }
    body = US_BODY.format(id=story_id, title=title, title_lower=title.lower())
    full = "---\n" + "\n".join(f"{k}: {v}" for k, v in fm.items()) + f"\n---\n{body}\n"
    return fm, full


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <package_root>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1]).resolve()
    docs = root / "docs"
    if not (docs / "00_scope.md").is_file():
        print("ERROR: docs/00_scope.md missing — not a meridian-teste folder", file=sys.stderr)
        return 1

    bootstrap(root)
    conn = connect(root)
    try:
        version_md = """---
id: v1
title: Test version
status: active
---

# v1 — Test version

## Objective

SQLite smoke tests.

## Done criteria

- DB readable from extension

## Included in this version

- US-0001 to US-0003

## Explicitly out

- Production features

## Go-live checklist

- n/a
"""
        epic_md = """---
id: EPIC-01
title: Database smoke epic
status: active
versions: [v1]
profiles: [developer]
outcome: Validate SQLite delivery
---

# EPIC-01 — Database smoke epic

## Capability

Minimal epic for meridian-teste.

## Expected outcome

Board and form load from SQLite.

## Out of scope for this epic

- Full product scope
"""
        from meridian_markdown_parse import read_markdown_text

        v_fm, v_body, v_full = read_markdown_text(version_md)
        e_fm, e_body, e_full = read_markdown_text(epic_md)
        upsert_version(conn, v_fm, v_full, extract_version_sections(v_body))
        upsert_epic(conn, e_fm, e_full, extract_epic_sections(e_body))

        for story_id, title, depends in [
            ("US-0001", "Base story", []),
            ("US-0002", "Depends on base", ["US-0001"]),
            ("US-0003", "Depends on two", ["US-0001", "US-0002"]),
        ]:
            fm, full = _us_markdown(story_id, title, depends)
            _, body, _ = read_markdown_text(full)
            upsert_user_story(conn, fm, full, extract_us_sections(body), depends)

        conn.commit()
    finally:
        conn.close()

    record_board_snapshot(root)
    print(f"Seeded meridian-teste DB at {root / '.meridian' / 'meridian.db'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
