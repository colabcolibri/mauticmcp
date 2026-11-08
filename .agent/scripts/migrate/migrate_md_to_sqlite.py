#!/usr/bin/env python3
"""Migrate Meridian delivery artifacts from Markdown/JSON files to SQLite."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from meridian_db import (  # noqa: E402
    apply_migrations,
    bootstrap,
    connect,
    delivery_counts,
    import_board_snapshot,
    import_decisions,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
)
from meridian_markdown_parse import (  # noqa: E402
    extract_epic_sections,
    extract_sprint_sections,
    extract_us_sections,
    extract_version_sections,
    parse_depends_on,
    parse_stories_list,
    read_markdown_file,
)


def migrate_delivery(package_root: Path) -> dict[str, int]:
    docs = package_root / "docs"
    counts = {"versions": 0, "epics": 0, "sprints": 0, "user_stories": 0}
    conn = connect(package_root)
    try:
        for path in sorted((docs / "versions").glob("v*.md")):
            if not re.match(r"v\d+(\.\d+)*\.md$", path.name):
                continue
            fm, body, full = read_markdown_file(path)
            upsert_version(conn, fm, full, extract_version_sections(body))
            counts["versions"] += 1

        for path in sorted((docs / "epics").glob("EPIC-*.md")):
            fm, body, full = read_markdown_file(path)
            upsert_epic(conn, fm, full, extract_epic_sections(body))
            counts["epics"] += 1

        for path in sorted((docs / "us").glob("US-*.md")):
            fm, body, full = read_markdown_file(path)
            depends = parse_depends_on(fm.get("depends_on"))
            upsert_user_story(conn, fm, full, extract_us_sections(body), depends)
            counts["user_stories"] += 1

        for path in sorted((docs / "sprints").glob("v*-S*.md")):
            fm, body, full = read_markdown_file(path)
            stories = parse_stories_list(fm.get("stories"))
            upsert_sprint(conn, fm, full, extract_sprint_sections(body), stories)
            counts["sprints"] += 1

        conn.commit()
    finally:
        conn.close()
    return counts


def migrate_decisions_and_board(package_root: Path) -> dict[str, int]:
    docs = package_root / "docs"
    conn = connect(package_root)
    try:
        decision_count = import_decisions(conn, docs)
        card_count = import_board_snapshot(conn, docs, source="import")
        conn.commit()
    finally:
        conn.close()
    return {"decisions": decision_count, "board_cards": card_count}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Migrate Meridian docs to SQLite")
    parser.add_argument("package_root", nargs="?", default=".")
    parser.add_argument(
        "--decisions-only",
        action="store_true",
        help="Import only decisions and board snapshot",
    )
    parser.add_argument(
        "--delivery-only",
        action="store_true",
        help="Import only epics/versions/sprints/US",
    )
    args = parser.parse_args()
    root = Path(args.package_root).resolve()

    bootstrap(root)

    if args.decisions_only:
        result = migrate_decisions_and_board(root)
        print(f"Decisions imported: {result['decisions']}")
        print(f"Board snapshot cards: {result['board_cards']}")
    elif args.delivery_only:
        result = migrate_delivery(root)
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        delivery = migrate_delivery(root)
        extra = migrate_decisions_and_board(root)
        for key, value in delivery.items():
            print(f"{key}: {value}")
        print(f"decisions: {extra['decisions']}")
        print(f"board_cards: {extra['board_cards']}")

    totals = delivery_counts(root)
    print(f"DB totals: {totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
