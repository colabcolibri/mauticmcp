#!/usr/bin/env python3
"""JSON export of delivery artifacts for IDE monitor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_db import (  # noqa: E402
    db_exists,
    export_decisions_json,
    export_delivery_json,
    export_entity_markdown,
    export_planning_json,
    upsert_delivery_from_markdown,
)
from meridian_delivery_form import (  # noqa: E402
    export_entity_form,
    import_entity_form_json,
)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Export delivery data as JSON")
    parser.add_argument("package_root", nargs="?", default=".")
    parser.add_argument("--probe", action="store_true", help="Exit 0 if DB exists")
    parser.add_argument(
        "--format",
        choices=["raw", "planning", "decisions", "form"],
        default="raw",
        help="raw=markdown bodies; planning=structured for extension; decisions=decision log; form=editable fields",
    )
    parser.add_argument(
        "--entity",
        choices=["us", "epics", "versions", "sprints"],
        help="single entity folder (with --id)",
    )
    parser.add_argument("--id", help="entity id, e.g. US-0125 or EPIC-15")
    parser.add_argument(
        "--write",
        action="store_true",
        help="upsert raw markdown from stdin (advanced; requires --entity and --id)",
    )
    parser.add_argument(
        "--write-form",
        action="store_true",
        help="upsert from structured JSON stdin (requires --entity and --id)",
    )
    args = parser.parse_args()
    root = Path(args.package_root).resolve()

    if args.probe:
        return 0 if db_exists(root) else 1

    if not db_exists(root):
        print(json.dumps({"error": "meridian.db not found"}))
        return 1

    if args.entity or args.id:
        if not args.entity or not args.id:
            print(json.dumps({"error": "both --entity and --id are required"}))
            return 1
        if args.write_form:
            json_text = sys.stdin.read()
            try:
                row = import_entity_form_json(root, args.entity, args.id, json_text)
            except (ValueError, json.JSONDecodeError) as exc:
                print(json.dumps({"ok": False, "error": str(exc)}))
                return 1
            print(json.dumps({"ok": True, **row}, ensure_ascii=False))
            return 0
        if args.write:
            markdown_text = sys.stdin.read()
            try:
                row = upsert_delivery_from_markdown(root, args.entity, args.id, markdown_text)
            except ValueError as exc:
                print(json.dumps({"ok": False, "error": str(exc)}))
                return 1
            print(json.dumps({"ok": True, **row}, ensure_ascii=False))
            return 0
        try:
            if args.format == "form":
                row = export_entity_form(root, args.entity, args.id)
            else:
                row = export_entity_markdown(root, args.entity, args.id)
        except ValueError as exc:
            print(json.dumps({"error": str(exc)}))
            return 1
        if row is None:
            print(json.dumps({"error": "not found"}))
            return 1
        print(json.dumps(row, ensure_ascii=False))
        return 0

    if args.format == "planning":
        print(json.dumps(export_planning_json(root), ensure_ascii=False))
    elif args.format == "decisions":
        print(json.dumps(export_decisions_json(root), ensure_ascii=False))
    else:
        print(json.dumps(export_delivery_json(root), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
