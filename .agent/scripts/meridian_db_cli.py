#!/usr/bin/env python3
"""CLI for Meridian SQLite delivery store — query and write operations (US-0116, US-0119)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_db import (  # noqa: E402
    bootstrap,
    connect,
    db_exists,
    delivery_counts,
    fetch_decisions_for_date,
    is_meridian_package,
    list_decision_dates,
    next_epic_id,
    next_sprint_id,
    next_user_story_id,
    prepend_decision,
    record_board_snapshot,
    set_summary,
    upsert_delivery_from_markdown,
    upsert_epic,
    upsert_sprint,
    upsert_user_story,
    upsert_version,
    validate_decision_entry,
    validate_story_open_sprint,
)
from meridian_lifecycle import (  # noqa: E402
    collect_hygiene_findings,
    lifecycle_eligible_for_story,
)
from meridian_markdown_parse import (  # noqa: E402
    extract_epic_sections,
    extract_sprint_sections,
    extract_us_sections,
    extract_version_sections,
    parse_depends_on,
    read_markdown_file,
    read_markdown_text,
)
from meridian_delivery_config import write_delivery_config  # noqa: E402

BOOTSTRAP_CMD = "python3 .agent/scripts/meridian_delivery.py bootstrap"
AUTO_BOOTSTRAP_COMMANDS = frozenset(
    {
        "counts",
        "list",
        "show",
        "implement-gate",
        "lifecycle-hygiene",
        "lifecycle-eligible",
    }
)


def ensure_delivery_db(root: Path, command: str) -> bool:
    if db_exists(root):
        return True
    if command in AUTO_BOOTSTRAP_COMMANDS and is_meridian_package(root):
        bootstrap(root)
        write_delivery_config(root)
        return True
    print(f"ERROR: meridian.db not found — run: {BOOTSTRAP_CMD}", file=sys.stderr)
    return False

US_TEMPLATE_BODY = """# {id} — {title}

**As** Process Manager,
**I want** {title_lower},
**so that** delivery data is tracked in SQLite.

## Intent

### Acceptance

- [ ] Criterion pending refine

### Why

Created via meridian_db_cli.

### Where

Version {version}, epic {epic}.

## Plan

### Architecture refs

- `docs/05_architecture.md` — § Repository context

### API / DB impact

- SQLite `user_stories` row.

### Security notes

- _n/a_

### Related decisions

- _n/a_

### Planned

- [ ] **manual** — refine and implement

## Record

### Files

_(fill on close)_

### Backend

_n/a_

### Frontend

_n/a_

### Scripts / Docs

_(fill on close)_

### Executed

_(pending until close)_

## Boundaries

### Out of scope for this story

- TBD on refine.

### Notes

- Created by meridian_db_cli create-us.
"""

EPIC_TEMPLATE_BODY = """# {id} — {title}

## Capability

{capability}

## Expected outcome

{expected_outcome}

## Out of scope for this epic

{out_of_scope}

## Notes

{notes}
"""

VERSION_TEMPLATE_BODY = """# {id} — {title}

## Objective

{objective}

## Done criteria

{done_criteria}

## Included in this version

{included}

## Explicitly out

{explicitly_out}

## Go-live checklist

### Product

- [ ] TBD on refine

### Ops

- [ ] TBD on refine
"""

SPRINT_TEMPLATE_BODY = """# {id} — {title}

## Goal

{goal_body}

## Scope

| US | Status | MoSCoW | Depends on | Epic | Description |
| -- | ------ | ------ | ---------- | ---- | ----------- |
| _(add rows on refine)_ | | | | | |

## Out of scope for this sprint

{out_of_scope}

## Retrospective

_(fill at sprint close)_
"""

ENTITY_TABLE = {
    "user_stories": ("user_stories", "id"),
    "user_story": ("user_stories", "id"),
    "us": ("user_stories", "id"),
    "epics": ("epics", "id"),
    "epic": ("epics", "id"),
    "versions": ("versions", "id"),
    "version": ("versions", "id"),
    "sprints": ("sprints", "id"),
    "sprint": ("sprints", "id"),
    "decisions": ("decisions", "decision_date"),
}


def _root(args) -> Path:
    return Path(args.package_root).resolve()


def cmd_counts(args) -> int:
    root = _root(args)
    counts = delivery_counts(root)
    for key, value in counts.items():
        print(f"{key}: {value}")
    return 0


def cmd_list(args) -> int:
    root = _root(args)
    if args.entity == "decisions":
        conn = connect(root)
        try:
            if getattr(args, "date", None):
                for index, entry in enumerate(fetch_decisions_for_date(conn, args.date)):
                    print(f"{args.date}\t{index}\t{entry.get('time', '')}\t{entry.get('title', '')}")
            else:
                for decision_date, count in list_decision_dates(conn):
                    print(f"{decision_date}\t{count}")
        finally:
            conn.close()
        return 0
    table, _ = ENTITY_TABLE.get(args.entity, (None, None))
    if not table:
        print(f"ERROR: unknown entity {args.entity}", file=sys.stderr)
        return 1
    conn = connect(root)
    try:
        query = f"SELECT id, title, status"
        if table == "user_stories":
            query += ", ready, version_id, epic_id"
        elif table == "sprints":
            query += ", version_id"
        query += f" FROM {table} WHERE 1=1"
        params: list[str] = []
        if args.status and table == "user_stories":
            query += " AND status = ?"
            params.append(args.status)
        if args.version:
            col = "version_id" if table in ("user_stories", "sprints") else "id"
            if table == "versions":
                query += " AND id = ?"
            else:
                query += f" AND {col} = ?"
            params.append(args.version)
        if args.epic and table == "user_stories":
            query += " AND epic_id = ?"
            params.append(args.epic)
        if args.ready is not None and table == "user_stories":
            query += " AND ready = ?"
            params.append(1 if args.ready == "true" else 0)
        query += " ORDER BY id"
        for row in conn.execute(query, params):
            if table == "user_stories":
                print(
                    f"{row['id']}\t{row['title']}\t{row['status']}\tready={row['ready']}\t{row['version_id']}\t{row['epic_id']}"
                )
            elif table == "sprints":
                print(f"{row['id']}\t{row['title']}\t{row['status']}\t{row['version_id']}")
            else:
                print(f"{row['id']}\t{row['title']}\t{row['status']}")
    finally:
        conn.close()
    return 0


def cmd_show(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        row = conn.execute(
            "SELECT * FROM user_stories WHERE id = ?", (args.story_id,)
        ).fetchone()
        if not row:
            print(f"ERROR: {args.story_id} not found", file=sys.stderr)
            return 1
        if not args.full:
            print(f"id: {row['id']}")
            print(f"title: {row['title']}")
            print(f"status: {row['status']}")
            print(f"epic: {row['epic_id']}")
            print(f"version: {row['version_id']}")
            print(f"ready: {bool(row['ready'])}")
            print(f"done_when: {row['done_when']}")
            if row["summary"]:
                print(f"\n--- summary ---\n{row['summary']}")
            else:
                print("\n(summary not set — run backfill_summaries.py)")
            return 0
        print(row["body_markdown"] or "")
        for label, col in [
            ("intent_acceptance", "intent_acceptance"),
            ("intent_why", "intent_why"),
            ("plan_approach", "plan_approach"),
        ]:
            if row[col]:
                print(f"\n--- {label} ---\n{row[col]}")
    finally:
        conn.close()
    return 0


def cmd_search(args) -> int:
    root = _root(args)
    table, _ = ENTITY_TABLE.get(args.entity, ("user_stories", "id"))
    conn = connect(root)
    needle = f"%{args.query}%"
    try:
        if table == "user_stories":
            rows = conn.execute(
                """
                SELECT id, title, status FROM user_stories
                WHERE title LIKE ? OR summary LIKE ? OR intent_why LIKE ?
                ORDER BY id
                """,
                (needle, needle, needle),
            )
        else:
            rows = conn.execute(
                f"SELECT id, title, status FROM {table} WHERE title LIKE ? OR summary LIKE ? ORDER BY id",
                (needle, needle),
            )
        for row in rows:
            print(f"{row['id']}\t{row['title']}\t{row['status']}")
    finally:
        conn.close()
    return 0


def cmd_create_us(args) -> int:
    root = _root(args)
    bootstrap(root)
    story_id = next_user_story_id(root)
    title = args.title
    body = US_TEMPLATE_BODY.format(
        id=story_id,
        title=title,
        title_lower=title.lower(),
        version=args.version,
        epic=args.epic,
    )
    fm = {
        "id": story_id,
        "title": title,
        "epic": args.epic,
        "version": args.version,
        "status": "❌",
        "moscow": args.moscow,
        "depends_on": "[]",
        "ready": "false",
        "done_when": args.done_when,
        "tests": "required",
        "tests_status": "pending",
    }
    conn = connect(root)
    try:
        upsert_user_story(conn, fm, body, extract_us_sections(body), [])
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    print(story_id)
    return 0


def cmd_create_epic(args) -> int:
    root = _root(args)
    bootstrap(root)
    epic_id = args.id or next_epic_id(root)
    title = args.title
    capability = args.capability or (
        f"Today users lack a clear capability for “{title}”. "
        f"This epic adds that behavior in the product."
    )
    expected = args.expected_outcome or (
        f"The manager recognizes {epic_id} as done when Must user stories are ✅ "
        f"and the capability is observable without reading every US file."
    )
    out_of_scope = args.out_of_scope or "- TBD on refine."
    notes = args.notes or "- Created by meridian_db_cli create-epic."
    body = EPIC_TEMPLATE_BODY.format(
        id=epic_id,
        title=title,
        capability=capability,
        expected_outcome=expected,
        out_of_scope=out_of_scope,
        notes=notes,
    )
    fm = {
        "id": epic_id,
        "title": title,
        "status": args.status,
        "versions": args.versions,
        "profiles": args.profiles,
        "outcome": args.outcome or title,
    }
    conn = connect(root)
    try:
        upsert_epic(conn, fm, body, extract_epic_sections(body))
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    print(epic_id)
    return 0


def cmd_create_version(args) -> int:
    root = _root(args)
    bootstrap(root)
    version_id = args.id
    title = args.title
    objective = args.objective or (
        f"This release delivers “{title}” — theme and user-visible changes for {version_id}."
    )
    done = args.done_criteria or (
        f"{version_id} is complete when documented done criteria are met and "
        f"Must stories for this version are ✅."
    )
    body = VERSION_TEMPLATE_BODY.format(
        id=version_id,
        title=title,
        objective=objective,
        done_criteria=done,
        included=args.included or "- _(add epics/US on refine)_",
        explicitly_out=args.explicitly_out or "- TBD on refine.",
    )
    fm = {
        "id": version_id,
        "title": title,
        "status": args.status,
        "outcome": args.outcome or title,
    }
    conn = connect(root)
    try:
        upsert_version(conn, fm, body, extract_version_sections(body))
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    print(version_id)
    return 0


def cmd_create_sprint(args) -> int:
    root = _root(args)
    bootstrap(root)
    sprint_id = args.id or next_sprint_id(root, args.version)
    title = args.title
    goal_body = args.goal or (
        f"This sprint proves progress on “{title}” within {args.version}."
    )
    body = SPRINT_TEMPLATE_BODY.format(
        id=sprint_id,
        title=title,
        goal_body=goal_body,
        out_of_scope=args.out_of_scope or "- TBD on refine.",
    )
    stories = [s.strip() for s in args.stories.split(",") if s.strip()] if args.stories else []
    fm = {
        "id": sprint_id,
        "version": args.version,
        "title": title,
        "status": args.status,
        "goal": args.goal or title,
        "done_when": args.done_when,
        "stories": str(stories),
    }
    conn = connect(root)
    try:
        upsert_sprint(conn, fm, body, extract_sprint_sections(body), stories)
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    print(sprint_id)
    return 0


def _read_markdown_input(_args) -> str:
    return sys.stdin.read()


def _cmd_update_markdown(args, entity: str, entity_id: str) -> int:
    text = _read_markdown_input(args)
    if not text.strip():
        print("ERROR: empty input", file=sys.stderr)
        return 1
    try:
        upsert_delivery_from_markdown(_root(args), entity, entity_id, text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Updated {entity_id}")
    return 0


def cmd_update_us(args) -> int:
    return _cmd_update_markdown(args, "user_stories", args.story_id)


def cmd_patch_record(args) -> int:
    root = _root(args)
    text = sys.stdin.read()
    if not text.strip():
        print("ERROR: empty patch on stdin", file=sys.stderr)
        return 1
    try:
        from meridian_db import patch_user_story_record  # noqa: PLC0415

        patch_user_story_record(root, args.story_id, text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Patched Record for {args.story_id}")
    return 0


def cmd_update_epic(args) -> int:
    return _cmd_update_markdown(args, "epics", args.epic_id)


def cmd_update_version(args) -> int:
    return _cmd_update_markdown(args, "versions", args.version_id)


def cmd_update_sprint(args) -> int:
    return _cmd_update_markdown(args, "sprints", args.sprint_id)


def cmd_set_ready(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        ready = args.ready == "true"
        if ready:
            validate_story_open_sprint(conn, args.story_id)
        conn.execute(
            "UPDATE user_stories SET ready = ?, updated_at = datetime('now') WHERE id = ?",
            (1 if ready else 0, args.story_id),
        )
        if conn.total_changes == 0:
            print(f"ERROR: {args.story_id} not found", file=sys.stderr)
            return 1
        conn.commit()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    record_board_snapshot(root)
    return 0


def cmd_set_in_progress(args) -> int:
    from meridian_db import apply_migrations

    root = _root(args)
    apply_migrations(root)
    conn = connect(root)
    try:
        flag = args.in_progress == "true"
        conn.execute(
            "UPDATE user_stories SET in_progress = ?, updated_at = datetime('now') WHERE id = ?",
            (1 if flag else 0, args.story_id),
        )
        if conn.total_changes == 0:
            print(f"ERROR: {args.story_id} not found", file=sys.stderr)
            return 1
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    print(f"{args.story_id} in_progress={'true' if args.in_progress == 'true' else 'false'}")
    return 0


def cmd_set_summary(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        ok = set_summary(conn, "user_stories", args.story_id, args.text)
        if not ok:
            print(f"ERROR: {args.story_id} not found", file=sys.stderr)
            return 1
        conn.commit()
    finally:
        conn.close()
    print(f"Summary set for {args.story_id}")
    return 0


def cmd_delete_us(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        conn.execute("DELETE FROM sprint_stories WHERE story_id = ?", (args.story_id,))
        conn.execute("DELETE FROM user_stories WHERE id = ?", (args.story_id,))
        conn.commit()
    finally:
        conn.close()
    record_board_snapshot(root)
    return 0


def cmd_implement_gate(args) -> int:
    from meridian_implement_gate import check_implement_gate

    result = check_implement_gate(_root(args), args.story_id)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for check in result["checks"]:
            mark = "PASS" if check["passed"] else "FAIL"
            detail = check.get("detail") or ""
            print(f"{mark}\t{check['name']}\t{detail}")
        if result["ok"]:
            print(f"OK: implement gate passed for {args.story_id}")
        else:
            print(f"BLOCKED: cannot implement {args.story_id}", file=sys.stderr)
    return 0 if result["ok"] else 1


def _decision_entry_from_args(args) -> dict[str, str]:
    if args.from_json:
        path = Path(args.from_json)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("from-json must be a decision entry object")
        return payload
    required = {
        "time": args.time,
        "title": args.title,
        "affected_document": args.affected_document,
        "what_changed": args.what_changed,
        "why_changed": args.why_changed,
        "impact": args.impact,
        "responsible": args.responsible,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"missing required flags: {', '.join(missing)} (or use --from-json)")
    return required


def cmd_prepend_decision(args) -> int:
    root = _root(args)
    try:
        entry = _decision_entry_from_args(args)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    errors = validate_decision_entry(entry)
    if errors:
        print(f"ERROR: {'; '.join(errors)}", file=sys.stderr)
        return 1
    conn = connect(root)
    try:
        prepend_decision(conn, args.date, entry)
        conn.commit()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    if args.json:
        print(
            json.dumps(
                {"decision_date": args.date, "entry_index": 0, "entry": entry},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"OK: prepended decision on {args.date} at index 0")
        print(f"title: {entry.get('title')}")
        print(f"time: {entry.get('time')}")
    return 0


def cmd_lifecycle_hygiene(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        findings = collect_hygiene_findings(conn)
    finally:
        conn.close()
    if args.json:
        print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
        return 0
    if not findings:
        print("Lifecycle hygiene: no finished-but-open containers.")
        return 0
    print(f"Lifecycle hygiene: {len(findings)} finding(s)")
    for item in findings:
        print(f"- [{item['kind']}] {item['id']}: {item['reason']}")
        print(f"  → {item['suggested_command']}")
    return 0


def cmd_lifecycle_eligible(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        payload = lifecycle_eligible_for_story(conn, args.story_id)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"story: {payload['storyId']} status={payload['storyStatus']}")
    for key in ("sprint", "epic", "version"):
        item = payload.get(key)
        if item:
            print(f"{key} eligible: {item['id']} — {item['suggested_command']}")
        else:
            print(f"{key} eligible: (none)")
    return 0


def cmd_show_decisions(args) -> int:
    root = _root(args)
    conn = connect(root)
    try:
        entries = fetch_decisions_for_date(conn, args.date)
    finally:
        conn.close()
    if not entries and not args.json:
        print(f"No decisions for {args.date}", file=sys.stderr)
        return 1
    payload = {"date": args.date, "entries": entries}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"date: {args.date}")
        print(f"entries: {len(entries)}")
        for index, entry in enumerate(entries):
            print(f"\n--- [{index}] {entry.get('time', '')} — {entry.get('title', '')} ---")
            for field in (
                "affected_document",
                "what_changed",
                "why_changed",
                "impact",
                "responsible",
            ):
                if entry.get(field):
                    print(f"{field}: {entry[field]}")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Meridian DB CLI — see .agent/references/templates/sqlite-delivery-operations.md"
    )
    parser.add_argument("--package-root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    counts = sub.add_parser("counts", help="Row counts per delivery table")
    counts.set_defaults(func=cmd_counts)

    list_p = sub.add_parser("list", help="List entities (tab-separated)")
    list_p.add_argument("entity", choices=sorted(set(ENTITY_TABLE.keys())))
    list_p.add_argument("--status")
    list_p.add_argument("--version")
    list_p.add_argument("--epic")
    list_p.add_argument("--ready", choices=["true", "false"])
    list_p.add_argument("--date", help="Decision date (YYYY-MM-DD) when entity=decisions")
    list_p.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Show US summary or --full body")
    show.add_argument("story_id")
    show.add_argument("--full", action="store_true")
    show.set_defaults(func=cmd_show)

    search = sub.add_parser("search", help="Search title/summary")
    search.add_argument("query")
    search.add_argument("--entity", default="user_stories")
    search.set_defaults(func=cmd_search)

    create = sub.add_parser("create-us")
    create.add_argument("--title", required=True)
    create.add_argument("--epic", required=True)
    create.add_argument("--version", required=True)
    create.add_argument("--moscow", default="Must")
    create.add_argument("--done-when", default="TBD")
    create.set_defaults(func=cmd_create_us)

    epic = sub.add_parser("create-epic")
    epic.add_argument("--title", required=True)
    epic.add_argument("--id", help="EPIC-XX; default next id")
    epic.add_argument("--versions", default="[v1]")
    epic.add_argument("--profiles", default="[Process Manager]")
    epic.add_argument("--status", default="active")
    epic.add_argument("--outcome")
    epic.add_argument("--capability")
    epic.add_argument("--expected-outcome")
    epic.add_argument("--out-of-scope")
    epic.add_argument("--notes")
    epic.set_defaults(func=cmd_create_epic)

    version = sub.add_parser("create-version")
    version.add_argument("--id", required=True, help="e.g. v11")
    version.add_argument("--title", required=True)
    version.add_argument("--status", default="planned")
    version.add_argument("--outcome")
    version.add_argument("--objective")
    version.add_argument("--done-criteria")
    version.add_argument("--included")
    version.add_argument("--explicitly-out")
    version.set_defaults(func=cmd_create_version)

    sprint = sub.add_parser("create-sprint")
    sprint.add_argument("--version", required=True)
    sprint.add_argument("--title", required=True)
    sprint.add_argument("--id", help="vX-Sn; default next for version")
    sprint.add_argument("--status", default="planned")
    sprint.add_argument("--goal")
    sprint.add_argument("--done-when", default="TBD")
    sprint.add_argument("--stories", help="comma-separated US ids")
    sprint.add_argument("--out-of-scope")
    sprint.set_defaults(func=cmd_create_sprint)

    update = sub.add_parser("update-us", help="Upsert US from markdown on stdin (heredoc)")
    update.add_argument("story_id")
    update.set_defaults(func=cmd_update_us)

    patch_record = sub.add_parser(
        "patch-record",
        help="Merge ## Record (+ optional Acceptance, frontmatter) into existing US — additive close; never replaces Intent/Plan",
    )
    patch_record.add_argument("story_id")
    patch_record.set_defaults(func=cmd_patch_record)

    update_epic = sub.add_parser("update-epic", help="Upsert epic from markdown on stdin (heredoc)")
    update_epic.add_argument("epic_id")
    update_epic.set_defaults(func=cmd_update_epic)

    update_version = sub.add_parser(
        "update-version", help="Upsert version from markdown on stdin (heredoc)"
    )
    update_version.add_argument("version_id")
    update_version.set_defaults(func=cmd_update_version)

    update_sprint = sub.add_parser(
        "update-sprint", help="Upsert sprint from markdown on stdin (heredoc)"
    )
    update_sprint.add_argument("sprint_id")
    update_sprint.set_defaults(func=cmd_update_sprint)

    ready = sub.add_parser("set-ready")
    ready.add_argument("story_id")
    ready.add_argument("--ready", choices=["true", "false"], default="true")
    ready.set_defaults(func=cmd_set_ready)

    wip = sub.add_parser(
        "set-in-progress",
        help="Claim US for Doing column (in_progress); not a status emoji",
    )
    wip.add_argument("story_id")
    wip.add_argument("--in-progress", choices=["true", "false"], default="true")
    wip.set_defaults(func=cmd_set_in_progress)

    summary = sub.add_parser("set-summary")
    summary.add_argument("story_id")
    summary.add_argument("--text", required=True)
    summary.set_defaults(func=cmd_set_summary)

    delete = sub.add_parser("delete-us")
    delete.add_argument("story_id")
    delete.set_defaults(func=cmd_delete_us)

    gate = sub.add_parser("implement-gate", help="Check /implement-us gate for a US")
    gate.add_argument("story_id")
    gate.add_argument("--json", action="store_true")
    gate.set_defaults(func=cmd_implement_gate)

    prepend = sub.add_parser(
        "prepend-decision",
        help="Prepend decision entry at index 0 for decision_date (SQLite)",
    )
    prepend.add_argument("--date", required=True, help="YYYY-MM-DD")
    prepend.add_argument("--time", help="HH:MM (24h local)")
    prepend.add_argument("--title")
    prepend.add_argument("--affected-document")
    prepend.add_argument("--what-changed")
    prepend.add_argument("--why-changed")
    prepend.add_argument("--impact")
    prepend.add_argument("--responsible")
    prepend.add_argument("--from-json", help="Path to single decision entry JSON object")
    prepend.add_argument("--json", action="store_true", help="Print result as JSON")
    prepend.set_defaults(func=cmd_prepend_decision)

    show_dec = sub.add_parser("show-decisions", help="Show decisions for a calendar day")
    show_dec.add_argument("--date", required=True, help="YYYY-MM-DD")
    show_dec.add_argument("--json", action="store_true")
    show_dec.set_defaults(func=cmd_show_decisions)

    hygiene = sub.add_parser(
        "lifecycle-hygiene",
        help="List finished-but-open sprints/epics/versions (warnings for /status)",
    )
    hygiene.add_argument("--json", action="store_true")
    hygiene.set_defaults(func=cmd_lifecycle_hygiene)

    eligible = sub.add_parser(
        "lifecycle-eligible",
        help="After /complete-us — containers eligible to close for a story",
    )
    eligible.add_argument("story_id")
    eligible.add_argument("--json", action="store_true")
    eligible.set_defaults(func=cmd_lifecycle_eligible)

    args = parser.parse_args()
    create_commands = {"create-us", "create-epic", "create-version", "create-sprint"}
    if args.command not in create_commands:
        if not ensure_delivery_db(Path(args.package_root).resolve(), args.command):
            return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
