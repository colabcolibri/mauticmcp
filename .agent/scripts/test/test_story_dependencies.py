#!/usr/bin/env python3
"""Tests for story_dependencies validation and sync."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    load_story_dependencies,
    upsert_epic,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import extract_us_sections  # noqa: E402

US_BODY = """# US-0001 — First

## Intent

### Acceptance

- [ ] Works

## Plan

### Approach

- step

## Record

### Files

- n/a

## Boundaries

### Out of scope for this story

- n/a
"""


def _seed_base(conn) -> None:
    upsert_version(
        conn,
        {"id": "v10", "title": "v10", "status": "active"},
        "",
        {"objective": "obj"},
    )
    upsert_epic(
        conn,
        {"id": "EPIC-01", "title": "Epic", "status": "active"},
        "",
        {"capability": "cap"},
    )


def _upsert_us(conn, story_id: str, depends: list[str]) -> None:
    fm = {
        "id": story_id,
        "title": story_id,
        "epic": "EPIC-01",
        "version": "v10",
        "status": "❌",
        "moscow": "Must",
        "ready": "false",
        "done_when": "done",
        "tests": "required",
        "tests_status": "pending",
    }
    upsert_user_story(conn, fm, US_BODY, extract_us_sections(US_BODY), depends)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n")
        bootstrap(root)

        conn = connect(root)
        try:
            _seed_base(conn)
            _upsert_us(conn, "US-0001", [])
            _upsert_us(conn, "US-0002", ["US-0001"])
            conn.commit()

            deps = load_story_dependencies(conn, "US-0002")
            if deps != ["US-0001"]:
                print(f"FAIL: expected ['US-0001'], got {deps}")
                return 1

            row = conn.execute(
                "SELECT depends_on_json FROM user_stories WHERE id = ?",
                ("US-0002",),
            ).fetchone()
            if json.loads(row["depends_on_json"]) != ["US-0001"]:
                print("FAIL: depends_on_json not synced")
                return 1

            try:
                _upsert_us(conn, "US-0003", ["US-9999"])
                print("FAIL: should reject unknown depends_on id")
                return 1
            except ValueError as exc:
                if "unknown US" not in str(exc):
                    print(f"FAIL: unexpected error: {exc}")
                    return 1

            try:
                _upsert_us(conn, "US-0001", ["US-0001"])
                print("FAIL: should reject self dependency")
                return 1
            except ValueError as exc:
                if "cannot include self" not in str(exc):
                    print(f"FAIL: unexpected error: {exc}")
                    return 1

            _upsert_us(conn, "US-0003", [])
            _upsert_us(conn, "US-0002", ["US-0003"])
            try:
                _upsert_us(conn, "US-0003", ["US-0002"])
                print("FAIL: should reject dependency cycle")
                return 1
            except ValueError as exc:
                if "cycle" not in str(exc):
                    print(f"FAIL: unexpected error: {exc}")
                    return 1
        finally:
            conn.close()

    print("OK: story_dependencies tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
