#!/usr/bin/env python3
"""Smoke test for Meridian SQLite schema (US-0105)."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import apply_migrations, bootstrap, list_tables, resolve_db_path  # noqa: E402

EXPECTED_TABLES = {
    "schema_migrations",
    "epics",
    "versions",
    "sprints",
    "sprint_stories",
    "story_dependencies",
    "user_stories",
    "decisions",
    "board_snapshots",
}


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n")

        msg = bootstrap(root)
        assert "Applied migrations" in msg or "up to date" in msg

        db_path = resolve_db_path(root)
        assert db_path.exists(), "meridian.db was not created"

        import sqlite3

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        tables = set(list_tables(conn))
        missing = EXPECTED_TABLES - tables
        if missing:
            print(f"FAIL: missing tables: {sorted(missing)}")
            return 1

        row = conn.execute("SELECT COUNT(*) AS c FROM schema_migrations").fetchone()
        if row["c"] < 1:
            print("FAIL: schema_migrations empty")
            return 1

        cols = conn.execute("PRAGMA table_info(user_stories)").fetchall()
        col_names = {c["name"] for c in cols}
        if "ready" not in col_names:
            print("FAIL: user_stories.ready column missing")
            return 1
        if "summary" not in col_names:
            print("FAIL: user_stories.summary column missing")
            return 1
        if "sprint_id" not in col_names:
            print("FAIL: user_stories.sprint_id column missing")
            return 1
        if "in_progress" not in col_names:
            print("FAIL: user_stories.in_progress column missing")
            return 1

        conn.close()

        # idempotent re-run
        msg2 = bootstrap(root)
        if "already up to date" not in msg2:
            print(f"FAIL: expected idempotent message, got: {msg2}")
            return 1

    print("OK: meridian_db schema smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
