#!/usr/bin/env python3
"""Tests for ready:true sprint scope guard."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    ensure_ready_has_open_sprint,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402

US_BODY = """---
id: US-0001
title: Guard test
epic: EPIC-01
version: v1
status: ❌
moscow: Must
depends_on: []
ready: true
done_when: Done
tests: required
tests_status: pending
---

# US-0001 — Guard test

## Intent

### Acceptance

- [ ] Works

### Why

Test.

### Where

Test.

## Plan

### Approach

- First bullet explains guard behavior in delivery layer.
- Second bullet names sprint_stories as the source of truth for Todo.

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


def _seed_version_epic(conn) -> None:
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


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n")
        bootstrap(root)
        conn = connect(root)
        try:
            _seed_version_epic(conn)
            fm_d, body_d, full_d = read_markdown_text(
                US_BODY.replace("ready: true", "ready: false")
            )
            upsert_user_story(conn, fm_d, full_d, extract_us_sections(body_d), [])
            conn.commit()
            fm_d["ready"] = "true"
            try:
                upsert_user_story(conn, fm_d, full_d, extract_us_sections(body_d), [])
                conn.commit()
            except ValueError as exc:
                if "sprint" not in str(exc).lower():
                    print(f"FAIL: unexpected error: {exc}")
                    return 1
            else:
                print("FAIL: expected ValueError when ready without sprint")
                return 1

            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "active",
                    "goal": "g",
                    "done_when": "d",
                    "stories": "['US-0001']",
                },
                "# v1-S1\n",
                {"goal": "g", "out_of_scope": "n/a", "retrospective": None},
                ["US-0001"],
            )
            fm_d["ready"] = "true"
            fm_d["sprint"] = "v1-S1"
            upsert_user_story(conn, fm_d, full_d, extract_us_sections(body_d), [])
            conn.commit()
            ensure_ready_has_open_sprint(conn, "US-0001")
        finally:
            conn.close()

    print("OK: ready sprint guard tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
