"""Tests for closed US quality validator rules."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

_LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(_LIB))

from meridian_us_close_quality import validate_closed_us_row  # noqa: E402


def _row(**kwargs: object) -> SimpleNamespace:
    defaults = {
        "id": "US-0001",
        "status": "✅",
        "body_markdown": "**As** x **I want** y **so that** z\n## Plan\n### Approach\n- Two bullets with enough text here.\n",
        "intent_why": "A" * 50,
        "plan_approach": "- " + "x" * 30,
        "record_files": "- `src/foo.ts` — change",
        "intent_acceptance": "- [x] done",
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class UsCloseQualityTests(unittest.TestCase):
    def test_passes_valid_closed_us(self) -> None:
        errors: list[str] = []
        validate_closed_us_row(_row(), errors)
        self.assertEqual(errors, [])

    def test_rejects_boilerplate_record(self) -> None:
        errors: list[str] = []
        validate_closed_us_row(_row(record_files="See git diff for this US scope."), errors)
        self.assertTrue(any("batch-close" in e for e in errors))

    def test_rejects_missing_approach(self) -> None:
        errors: list[str] = []
        validate_closed_us_row(_row(plan_approach=""), errors)
        self.assertTrue(any("Approach" in e for e in errors))

    def test_skips_non_closed(self) -> None:
        errors: list[str] = []
        validate_closed_us_row(_row(status="❌", record_files="See git diff"), errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
