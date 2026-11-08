"""Shared paths for Meridian kit scripts (stdlib only)."""

from __future__ import annotations

from pathlib import Path

LIB_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = LIB_DIR.parent
REPO_ROOT = SCRIPTS_DIR.parents[1]
MIGRATIONS_DIR = REPO_ROOT / ".agent" / "migrations"
MIGRATE_DIR = SCRIPTS_DIR / "migrate"
TEST_DIR = SCRIPTS_DIR / "test"
DEV_DIR = SCRIPTS_DIR / "dev"


def setup_lib_path() -> None:
    import sys

    lib = str(LIB_DIR)
    if lib not in sys.path:
        sys.path.insert(0, lib)
