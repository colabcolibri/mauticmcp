#!/usr/bin/env python3
"""Smoke tests for decision log CLI (SQLite prepend)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = REPO_ROOT / ".agent" / "scripts"
sys.path.insert(0, str(SCRIPTS / "lib"))

from meridian_db import bootstrap, connect, fetch_decisions_for_date  # noqa: E402


def _run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCRIPTS / "meridian_delivery.py"), "--package-root", str(root), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "product"
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n")
        bootstrap(root)

        result = _run_cli(
            root,
            "prepend-decision",
            "--date",
            "2026-07-18",
            "--time",
            "14:30",
            "--title",
            "Test decision",
            "--affected-document",
            "docs/00_scope.md",
            "--what-changed",
            "Added scope note",
            "--why-changed",
            "Test",
            "--impact",
            "none",
            "--responsible",
            "agent",
        )
        if result.returncode != 0:
            print(f"FAIL prepend-decision: {result.stderr}")
            return 1

        conn = connect(root)
        try:
            entries = fetch_decisions_for_date(conn, "2026-07-18")
        finally:
            conn.close()
        if len(entries) != 1 or entries[0]["title"] != "Test decision":
            print(f"FAIL: expected one entry, got {entries}")
            return 1

        result2 = _run_cli(
            root,
            "prepend-decision",
            "--date",
            "2026-07-18",
            "--time",
            "15:00",
            "--title",
            "Second decision",
            "--affected-document",
            "docs/05_architecture.md",
            "--what-changed",
            "Arch tweak",
            "--why-changed",
            "Order test",
            "--impact",
            "review 05",
            "--responsible",
            "manager",
        )
        if result2.returncode != 0:
            print(f"FAIL second prepend: {result2.stderr}")
            return 1

        conn = connect(root)
        try:
            entries = fetch_decisions_for_date(conn, "2026-07-18")
        finally:
            conn.close()
        if len(entries) != 2 or entries[0]["title"] != "Second decision":
            print(f"FAIL: prepend order wrong: {[e['title'] for e in entries]}")
            return 1

        show = _run_cli(root, "show-decisions", "--date", "2026-07-18", "--json")
        if show.returncode != 0:
            print(f"FAIL show-decisions: {show.stderr}")
            return 1
        payload = json.loads(show.stdout)
        if payload["date"] != "2026-07-18" or len(payload["entries"]) != 2:
            print(f"FAIL show payload: {payload}")
            return 1

        listed = _run_cli(root, "list", "decisions")
        if listed.returncode != 0 or "2026-07-18" not in listed.stdout:
            print(f"FAIL list decisions: {listed.stdout} {listed.stderr}")
            return 1

    print("OK: decisions CLI smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
