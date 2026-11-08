#!/usr/bin/env python3
"""Tests for meridian_lifecycle hygiene helpers (US-0166)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
)
from meridian_lifecycle import (  # noqa: E402
    collect_hygiene_findings,
    lifecycle_eligible_for_story,
    sprint_close_eligible,
)
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402

US_BODY = """---
id: US-0001
title: One
epic: EPIC-01
version: v1
sprint: v1-S1
status: ✅
moscow: Must
depends_on: []
ready: false
done_when: Done
tests: none
tests_status: n/a
---

# US-0001 — One

## Intent

### Acceptance

- [x] Done

### Why

Why text here for the story slice under test.

### Where

Where text here for the release under test.

## Plan

### Approach

- First approach bullet explains the slice clearly enough.
- Second approach bullet names reuse of existing helpers.

### Architecture refs

- `docs/05_architecture.md` — § Repository context

### API / DB impact

- n/a

### Security notes

- n/a

### Related decisions

- n/a

### Planned

- [x] Step

## Record

### Files

- a.ts

### Backend

- n/a

### Frontend

- n/a

### Scripts / Docs

- n/a

### Executed

- ok

## Boundaries

### Out of scope for this story

- Other work

### Notes

- n/a
"""


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n", encoding="utf-8")
        bootstrap(root)
        conn = connect(root)
        try:
            upsert_version(
                conn,
                {"id": "v1", "title": "v1", "status": "active"},
                "",
                {"objective": "obj"},
            )
            upsert_epic(
                conn,
                {"id": "EPIC-01", "title": "Epic", "status": "active"},
                "",
                {"capability": "cap"},
            )
            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "active",
                    "goal": "g",
                    "done_when": "d",
                },
                "# v1-S1\n",
                {"goal": "g", "out_of_scope": "n/a", "retrospective": None},
                [],
            )
            fm, body, full = read_markdown_text(US_BODY)
            upsert_user_story(conn, fm, full, extract_us_sections(body), [])
            conn.commit()

            finding = sprint_close_eligible(conn, "v1-S1")
            if finding is None:
                print("FAIL: expected sprint close eligible")
                return 1
            findings = collect_hygiene_findings(conn)
            if not any(f["id"] == "v1-S1" for f in findings):
                print(f"FAIL: hygiene missing sprint: {findings}")
                return 1
            cascade = lifecycle_eligible_for_story(conn, "US-0001")
            if cascade.get("sprint") is None:
                print(f"FAIL: cascade missing sprint: {cascade}")
                return 1
        finally:
            conn.close()

    print("OK: lifecycle hygiene tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
