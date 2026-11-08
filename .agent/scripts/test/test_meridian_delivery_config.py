#!/usr/bin/env python3
"""Smoke tests for meridian_delivery_config and facade."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_delivery_config import (  # noqa: E402
    default_delivery_config,
    delivery_config_path,
    load_delivery_config,
    write_delivery_config,
)


class DeliveryConfigTests(unittest.TestCase):
    def test_default_config(self) -> None:
        cfg = default_delivery_config("/tmp/pkg")
        self.assertEqual(cfg["connector"], "sqlite")
        self.assertEqual(cfg["version"], 1)

    def test_write_and_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "00_scope.md").write_text("# scope\n", encoding="utf-8")
            written = write_delivery_config(root)
            self.assertTrue(delivery_config_path(root).is_file())
            loaded = load_delivery_config(root)
            self.assertEqual(loaded["connector"], written["connector"])


if __name__ == "__main__":
    unittest.main()
