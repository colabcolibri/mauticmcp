#!/usr/bin/env python3
"""Tests for design-system validator warnings."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from validate_meridian import validate_sqlite_design_system_refs  # noqa: E402


class DesignSystemRefValidationTest(unittest.TestCase):
    def test_warns_must_ui_us_without_09_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "09_design_system.md").write_text(
                "---\nstatus: approved\n---\n# 09\n",
                encoding="utf-8",
            )
            (root / ".meridian").mkdir()
            db = root / ".meridian" / "meridian.db"
            conn = sqlite3.connect(db)
            conn.execute(
                """
                CREATE TABLE user_stories (
                  id TEXT PRIMARY KEY,
                  moscow TEXT,
                  status TEXT,
                  body_markdown TEXT,
                  plan_architecture_refs TEXT
                )
                """
            )
            conn.execute(
                """
                INSERT INTO user_stories VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "US-0999",
                    "Must",
                    "❌",
                    "### Acceptance\n- [ ] Responsive layout on mobile\n",
                    "docs/05_architecture.md — § Foo",
                ),
            )
            conn.commit()
            conn.close()

            warnings: list[str] = []
            validate_sqlite_design_system_refs(root, docs, warnings)
            self.assertTrue(
                any("US-0999" in w and "09_design_system" in w for w in warnings)
            )

    def test_skips_when_09_not_approved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "09_design_system.md").write_text(
                "---\nstatus: draft\n---\n",
                encoding="utf-8",
            )
            (root / ".meridian").mkdir()
            db = root / ".meridian" / "meridian.db"
            conn = sqlite3.connect(db)
            conn.execute(
                """
                CREATE TABLE user_stories (
                  id TEXT PRIMARY KEY,
                  moscow TEXT,
                  status TEXT,
                  body_markdown TEXT,
                  plan_architecture_refs TEXT
                )
                """
            )
            conn.execute(
                "INSERT INTO user_stories VALUES (?, ?, ?, ?, ?)",
                ("US-0999", "Must", "❌", "visual layout", ""),
            )
            conn.commit()
            conn.close()

            warnings: list[str] = []
            validate_sqlite_design_system_refs(root, docs, warnings)
            self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
