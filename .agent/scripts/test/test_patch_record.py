"""Tests for patch-record merge (US close safety)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(_LIB))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    patch_user_story_record,
    upsert_epic,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import extract_us_sections, read_markdown_text  # noqa: E402


BASE_US = """---
id: US-0999
title: Patch record test
epic: EPIC-01
version: v1
status: ❌
ready: true
moscow: Must
depends_on: []
done_when: "Done."
tests: required
tests_status: pending
---

# US-0999 — Patch record test

**As** Tester,
**I want** safe close patches,
**so that** refined Plan survives.

## Intent

### Acceptance

- [ ] First criterion observable
- [ ] Second criterion observable

### Why

This slice exists because full replace upserts wipe refined Intent and Plan when agents only send Record on close.

### Where

v1 test harness. No dependencies.

## Plan

### Approach

- Reuse `patch_us_record_markdown` to merge Record without touching Approach bullets.
- Validator blocks boilerplate on status ✅.

### Architecture refs

- `docs/05_architecture.md` — § Repository context

### API / DB impact

- _n/a_

### Security notes

- _n/a_

### Related decisions

- _n/a_

### Planned

- [ ] **automated** — `python3 test_patch_record.py`

## Record

### Files

_(fill on close)_

### Backend

_(fill on close)_

### Frontend

_(fill on close)_

### Scripts / Docs

_(fill on close)_

### Executed

_(pending until close)_

## Boundaries

### Out of scope for this story

- Epic patch-record.

### Notes

- Test fixture only.
"""


class PatchRecordTests(unittest.TestCase):
    def test_patch_preserves_plan_and_merges_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "00_scope.md").write_text("---\nstatus: approved\n---\n", encoding="utf-8")
            bootstrap(root)

            conn = connect(root)
            from meridian_db import upsert_sprint  # noqa: PLC0415

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
            body = BASE_US.replace("US-0999", "US-0001")
            fm, body_only, full = read_markdown_text(body)
            fm["id"] = "US-0001"
            fm["epic"] = "EPIC-01"
            fm["version"] = "v1"
            fm["ready"] = "false"
            upsert_user_story(conn, fm, full, extract_us_sections(body_only), [])
            upsert_sprint(
                conn,
                {
                    "id": "v1-S1",
                    "version": "v1",
                    "title": "S1",
                    "status": "active",
                },
                "",
                {"goal_body": "goal"},
                ["US-0001"],
            )
            conn.commit()
            conn.close()

            patch = """---
status: ✅
tests_status: done
sprint: v1-S1
ready: true
---
## Record

### Files

- `.agent/scripts/lib/meridian_markdown_parse.py` — patch merge

### Backend

- _n/a_

### Frontend

- _n/a_

### Scripts / Docs

- _n/a_

### Executed

- `python3 test_patch_record.py` — passed

## Intent

### Acceptance

- [x] First criterion observable
- [x] Second criterion observable
"""
            patch_user_story_record(root, "US-0001", patch)

            conn = connect(root)
            row = conn.execute(
                "SELECT body_markdown, plan_approach, intent_why, status FROM user_stories WHERE id='US-0001'"
            ).fetchone()
            conn.close()

            body = row["body_markdown"] or ""
            self.assertIn("patch_us_record_markdown", row["plan_approach"] or "")
            self.assertIn("full replace upserts", row["intent_why"] or "")
            self.assertEqual(row["status"], "✅")
            self.assertIn("meridian_markdown_parse.py", body)
            self.assertNotIn("_(fill on close)_", body)


if __name__ == "__main__":
    unittest.main()
