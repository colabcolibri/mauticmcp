#!/usr/bin/env python3
"""Tests for meridian_implement_gate."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import bootstrap, connect, upsert_epic, upsert_sprint, upsert_user_story, upsert_version  # noqa: E402
from meridian_implement_gate import check_implement_gate  # noqa: E402
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402

US_READY_BODY = """---
id: US-0001
title: Gate test
epic: EPIC-01
version: v1
sprint: v1-S1
status: ❌
moscow: Must
depends_on: []
ready: true
done_when: Done
tests: required
tests_status: pending
---

# US-0001 — Gate test

## Intent

### Acceptance

- [ ] Works

### Why

Test.

### Where

Test.

## Plan

### Approach

- First bullet explains what changes in the kit scripts layer.
- Second bullet names the SQLite read path and validation exit codes.

### Architecture refs

- `docs/05_architecture.md` — § Repository context

### API / DB impact

- SQLite only.

### Security notes

- n/a

### Related decisions

- n/a

### Planned

- [ ] Run implement-gate CLI

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

- n/a

### Notes

- test
"""


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n")
        (docs / "05_architecture.md").write_text(
            "---\nstatus: approved\n---\n# Architecture\n\n## Repository context\n\nKit at .agent/\n"
        )

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
            fm, body, full = read_markdown_text(US_READY_BODY)
            upsert_user_story(conn, fm, full, extract_us_sections(body), [])
            conn.commit()
        finally:
            conn.close()

        ok = check_implement_gate(root, "US-0001")
        if not ok["ok"]:
            print(f"FAIL: expected pass, got {ok}")
            return 1

        conn = connect(root)
        try:
            conn.execute("UPDATE user_stories SET ready = 0 WHERE id = 'US-0001'")
            conn.commit()
        finally:
            conn.close()

        blocked = check_implement_gate(root, "US-0001")
        if blocked["ok"]:
            print("FAIL: expected block when ready false")
            return 1

    print("OK: implement gate tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
