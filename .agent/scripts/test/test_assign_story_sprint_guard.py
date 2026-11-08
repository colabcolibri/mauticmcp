#!/usr/bin/env python3
"""Tests for assign_story_sprint / reopen hardening (US-0167)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    assign_story_sprint,
    bootstrap,
    connect,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402

US_BODY = """---
id: US-0001
title: One
epic: EPIC-01
version: v1
status: ❌
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

- [ ] x

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

- [ ] Step

## Record

### Files

_(fill on close)_

### Backend

- n/a

### Frontend

- n/a

### Scripts / Docs

- n/a

### Executed

_(pending until close)_

## Boundaries

### Out of scope for this story

- Other

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
                conn, {"id": "v1", "title": "v1", "status": "active"}, "", {"objective": "o"}
            )
            upsert_epic(
                conn, {"id": "EPIC-01", "title": "E", "status": "active"}, "", {"capability": "c"}
            )
            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "planned",
                    "goal": "g",
                    "done_when": "d",
                },
                "# v1-S1\n",
                {"goal": "g", "out_of_scope": "n/a", "retrospective": None},
                [],
            )
            fm, body, full = read_markdown_text(US_BODY)
            upsert_user_story(conn, fm, full, extract_us_sections(body), [])
            # Terminal US required to complete the sprint (container integrity).
            conn.execute("UPDATE user_stories SET status = '✅' WHERE id = 'US-0001'")
            good_retro = (
                "### What worked\n"
                "- Assign-guard kept new US off a closed sprint.\n\n"
                "### What to improve\n"
                "- Do not complete sprints with placeholder retrospectives.\n\n"
                "### Decisions to log\n"
                "- _n/a_\n"
            )
            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "complete",
                    "goal": "g",
                    "done_when": "d",
                },
                "# v1-S1\n\n## Retrospective\n\n" + good_retro,
                {"goal": "g", "out_of_scope": "n/a", "retrospective": good_retro},
                ["US-0001"],
            )
            conn.commit()

            try:
                assign_story_sprint(conn, "US-0001", "v1-S1", version_id="v1")
                print("FAIL: expected assign to complete sprint to raise")
                return 1
            except ValueError as exc:
                if "complete" not in str(exc).lower():
                    print(f"FAIL: unexpected error: {exc}")
                    return 1

            try:
                upsert_sprint(
                    conn,
                    {
                        "id": "v1-S1",
                        "version": "v1",
                        "title": "S1",
                        "status": "planned",
                        "goal": "g",
                        "done_when": "d",
                    },
                    "# v1-S1\n",
                    {"goal": "g", "out_of_scope": "n/a", "retrospective": "done"},
                    [],
                )
                print("FAIL: expected reopen without flag to raise")
                return 1
            except ValueError as exc:
                if "reopen" not in str(exc).lower():
                    print(f"FAIL: unexpected reopen error: {exc}")
                    return 1

            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "planned",
                    "goal": "g",
                    "done_when": "d",
                    "reopen": "true",
                },
                "# v1-S1\n",
                {"goal": "g", "out_of_scope": "n/a", "retrospective": "done"},
                [],
            )
            assign_story_sprint(conn, "US-0001", "v1-S1", version_id="v1")
            conn.commit()
        finally:
            conn.close()

    print("OK: assign/reopen guard tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
