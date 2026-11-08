#!/usr/bin/env python3
"""Tests for privacy validator warnings."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from validate_meridian import (  # noqa: E402
    validate_privacy_sections_in_02,
    validate_sqlite_privacy_refs,
)


class PrivacySectionValidationTest(unittest.TestCase):
    def test_warns_missing_lgpd_section_when_compliance_cites_lgpd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "02_security.md").write_text(
                "---\nstatus: approved\n---\n# 02\nCompliance: LGPD\n",
                encoding="utf-8",
            )
            warnings: list[str] = []
            validate_privacy_sections_in_02(docs, warnings)
            self.assertTrue(any("LGPD" in w for w in warnings))


class PrivacyRefValidationTest(unittest.TestCase):
    def test_warns_must_privacy_us_without_privacy_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "02_security.md").write_text(
                "---\nstatus: approved\n---\n# 02\n",
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
                (
                    "US-0997",
                    "Must",
                    "❌",
                    "### Acceptance\n- [ ] LGPD titular export endpoint\n",
                    "docs/05_architecture.md",
                ),
            )
            conn.commit()
            conn.close()

            warnings: list[str] = []
            validate_sqlite_privacy_refs(root, docs, warnings)
            self.assertTrue(any("US-0997" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
