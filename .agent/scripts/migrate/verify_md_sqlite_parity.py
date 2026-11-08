#!/usr/bin/env python3
"""Verify Markdown delivery files match SQLite rows (US-0117)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import connect, db_exists  # noqa: E402
from meridian_markdown_parse import parse_frontmatter_dict, read_markdown_file  # noqa: E402

DELIVERY_CHECKS = [
    ("us", "US-*.md", "user_stories"),
    ("epics", "EPIC-*.md", "epics"),
    ("versions", "v*.md", "versions"),
    ("sprints", "v*-S*.md", "sprints"),
]

COMPARE_FIELDS = {
    "user_stories": ("title", "status"),
    "epics": ("title", "status"),
    "versions": ("title", "status"),
    "sprints": ("title", "status"),
}


def _ready_from_fm(fm: dict[str, str]) -> int:
    return 1 if fm.get("ready", "").lower() == "true" else 0


def verify(package_root: Path) -> dict:
    docs = package_root / "docs"
    report: dict = {"ok": True, "missing_in_db": [], "missing_on_disk": [], "mismatches": []}

    if not db_exists(package_root):
        report["ok"] = False
        report["error"] = "meridian.db not found"
        return report

    conn = connect(package_root)
    try:
        for folder, pattern, table in DELIVERY_CHECKS:
            md_ids: set[str] = set()
            base = docs / folder
            if base.is_dir():
                for path in sorted(base.glob(pattern)):
                    md_ids.add(path.stem)
                    fm, _, _ = read_markdown_file(path)
                    row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (path.stem,)).fetchone()
                    if not row:
                        report["missing_in_db"].append(str(path.relative_to(package_root)))
                        report["ok"] = False
                        continue
                    for field in COMPARE_FIELDS[table]:
                        md_val = fm.get(field if field != "status" else field, fm.get(field))
                        db_val = row[field]
                        if str(md_val) != str(db_val):
                            report["mismatches"].append(
                                {
                                    "id": path.stem,
                                    "field": field,
                                    "md": md_val,
                                    "db": db_val,
                                }
                            )
                            report["ok"] = False
                    if table == "user_stories":
                        if _ready_from_fm(fm) != int(row["ready"]):
                            report["mismatches"].append(
                                {
                                    "id": path.stem,
                                    "field": "ready",
                                    "md": fm.get("ready"),
                                    "db": bool(row["ready"]),
                                }
                            )
                            report["ok"] = False
                        epic = fm.get("epic")
                        version = fm.get("version")
                        if epic and epic != row["epic_id"]:
                            report["mismatches"].append(
                                {"id": path.stem, "field": "epic", "md": epic, "db": row["epic_id"]}
                            )
                            report["ok"] = False
                        if version and version != row["version_id"]:
                            report["mismatches"].append(
                                {
                                    "id": path.stem,
                                    "field": "version",
                                    "md": version,
                                    "db": row["version_id"],
                                }
                            )
                            report["ok"] = False

            db_ids = {r[0] for r in conn.execute(f"SELECT id FROM {table}")}
            for db_id in sorted(db_ids - md_ids):
                if table == "versions" and not re.match(r"^v\d+(\.\d+)*$", db_id):
                    continue
                report["missing_on_disk"].append(f"{folder}/{db_id}.md (db only)")
    finally:
        conn.close()

    return report


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Verify Markdown ↔ SQLite parity")
    parser.add_argument("package_root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    report = verify(root)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        if report.get("error"):
            print(f"ERROR: {report['error']}")
        if report["missing_in_db"]:
            print("Missing in DB:")
            for item in report["missing_in_db"]:
                print(f"  - {item}")
        if report["missing_on_disk"]:
            print("DB-only (ok for new v10 artifacts):")
            for item in report["missing_on_disk"]:
                print(f"  - {item}")
        if report["mismatches"]:
            print("Mismatches:")
            for item in report["mismatches"]:
                print(f"  - {item['id']}.{item['field']}: md={item['md']!r} db={item['db']!r}")
        if report["ok"]:
            print("Parity OK — safe to purge delivery .md when manager approves.")
        else:
            print("Parity FAILED — do not purge.")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
