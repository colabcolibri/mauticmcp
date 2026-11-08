"""Tests for qualitySiege profile resolution."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(_LIB))

from meridian_quality_profile import (  # noqa: E402
    resolve_quality_siege,
    validate_quality_siege_value,
)


class QualityProfileTests(unittest.TestCase):
    def test_default_kit_when_unset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agent").mkdir()
            (root / ".agent" / "MERIDIAN.md").write_text("# kit\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "00_scope.md").write_text("---\nstatus: draft\n---\n", encoding="utf-8")
            result = resolve_quality_siege(root)
            self.assertEqual(result["qualitySiege"], "kit")
            self.assertIn("default", result["source"])

    def test_manifest_wins_over_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agent").mkdir()
            (root / ".agent" / "MERIDIAN.md").write_text("# kit\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "00_scope.md").write_text("---\nstatus: draft\n---\n", encoding="utf-8")
            meridian = root / ".meridian"
            meridian.mkdir()
            manifest = {
                "version": 1,
                "projects": [
                    {
                        "id": "main",
                        "name": "Main",
                        "docs": "docs",
                        "qualitySiege": "full",
                    }
                ],
            }
            (meridian / "projects.json").write_text(json.dumps(manifest), encoding="utf-8")
            (meridian / "delivery.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "connector": "sqlite",
                        "package_root": ".",
                        "options": {"qualitySiege": "standard"},
                    }
                ),
                encoding="utf-8",
            )
            result = resolve_quality_siege(root)
            self.assertEqual(result["qualitySiege"], "full")
            self.assertIn("projects.json", result["source"])

    def test_delivery_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agent").mkdir()
            (root / ".agent" / "MERIDIAN.md").write_text("# kit\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "00_scope.md").write_text("---\nstatus: draft\n---\n", encoding="utf-8")
            meridian = root / ".meridian"
            meridian.mkdir()
            (meridian / "delivery.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "connector": "sqlite",
                        "package_root": ".",
                        "options": {"qualitySiege": "standard"},
                    }
                ),
                encoding="utf-8",
            )
            result = resolve_quality_siege(root)
            self.assertEqual(result["qualitySiege"], "standard")
            self.assertIn("delivery.json", result["source"])

    def test_validate_rejects_invalid(self) -> None:
        with self.assertRaises(ValueError):
            validate_quality_siege_value("robust", context="test")


if __name__ == "__main__":
    unittest.main()
