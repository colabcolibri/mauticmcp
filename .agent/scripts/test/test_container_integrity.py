#!/usr/bin/env python3
"""Sprint/epic complete integrity (retrospective + Must US)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_container_integrity import retrospective_is_filled  # noqa: E402
from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402

GOOD_RETRO = """### What worked
- Close-us stayed additive; Records listed real paths.

### What to improve
- Hygiene invited /complete-sprint before Retrospective had evidence.

### Decisions to log
- _n/a_
"""

US_MD = """---
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


def _boot() -> tuple:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name) / "product"
    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n", encoding="utf-8")
    bootstrap(root)
    conn = connect(root)
    upsert_version(conn, {"id": "v1", "title": "v1", "status": "active"}, "", {"objective": "obj"})
    upsert_epic(
        conn,
        {
            "id": "EPIC-01",
            "title": "Epic",
            "status": "active",
            "outcome": "Manager can close the capability from the board alone.",
        },
        "",
        {"capability": "cap", "expected_outcome": "done"},
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
    return tmp, conn


def main() -> int:
    if retrospective_is_filled("_(fill at sprint close)_"):
        print("FAIL: placeholder counted as filled")
        return 1
    if retrospective_is_filled("What worked:\n- \nWhat to improve:\n-"):
        print("FAIL: empty bullets counted as filled")
        return 1
    if not retrospective_is_filled(GOOD_RETRO):
        print("FAIL: good retro not filled")
        return 1

    tmp, conn = _boot()
    try:
        fm, body, full = read_markdown_text(US_MD)
        upsert_user_story(conn, fm, full, extract_us_sections(body), [])
        conn.commit()

        try:
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
                "# v1-S1\n## Retrospective\n\n_(fill at sprint close)_\n",
                {"retrospective": "_(fill at sprint close)_"},
                ["US-0001"],
            )
            print("FAIL: placeholder retro should raise")
            return 1
        except ValueError as exc:
            if "Retrospective" not in str(exc):
                print(f"FAIL: wrong error: {exc}")
                return 1

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
            "# v1-S1\n## Retrospective\n\n" + GOOD_RETRO,
            {"retrospective": GOOD_RETRO},
            ["US-0001"],
        )

        try:
            upsert_epic(
                conn,
                {
                    "id": "EPIC-01",
                    "title": "Epic",
                    "status": "complete",
                    "outcome": "x",
                },
                "",
                {"capability": "cap"},
            )
            print("FAIL: thin outcome should raise")
            return 1
        except ValueError as exc:
            if "outcome" not in str(exc).lower():
                print(f"FAIL: unexpected epic error: {exc}")
                return 1

        upsert_epic(
            conn,
            {
                "id": "EPIC-01",
                "title": "Epic",
                "status": "complete",
                "outcome": "Manager can close the capability from the board alone.",
            },
            "",
            {"capability": "cap", "expected_outcome": "Observable board close."},
        )
        conn.commit()
    finally:
        conn.close()
        tmp.cleanup()

    print("OK: container integrity tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
