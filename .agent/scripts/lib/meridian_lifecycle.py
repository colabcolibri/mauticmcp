"""Delivery lifecycle hygiene — eligible close detection (US-0166 / US-0168)."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

TERMINAL_STORY_STATUSES = frozenset({"✅", "🚫", "🧊"})
OPEN_SPRINT_STATUSES = frozenset({"planned", "active"})


def terminal_story_status(status: str | None) -> bool:
    return (status or "") in TERMINAL_STORY_STATUSES


def _parse_versions(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        data = json.loads(raw.replace("'", '"'))
        if isinstance(data, list):
            return [str(x) for x in data]
    except json.JSONDecodeError:
        pass
    import re

    return re.findall(r"v[\w.-]+", raw)


def sprint_stories(conn: sqlite3.Connection, sprint_id: str) -> list[sqlite3.Row]:
    rows = conn.execute(
        """
        SELECT id, title, status, moscow
        FROM user_stories
        WHERE sprint_id = ?
        ORDER BY id
        """,
        (sprint_id,),
    ).fetchall()
    return list(rows)


def sprint_close_eligible(conn: sqlite3.Connection, sprint_id: str) -> dict[str, Any] | None:
    sprint = conn.execute(
        "SELECT id, title, status, version_id FROM sprints WHERE id = ?",
        (sprint_id,),
    ).fetchone()
    if not sprint:
        return None
    if sprint["status"] not in OPEN_SPRINT_STATUSES:
        return None
    stories = sprint_stories(conn, sprint_id)
    if not stories:
        return None
    if any(not terminal_story_status(s["status"]) for s in stories):
        return None
    return {
        "kind": "sprint",
        "id": sprint["id"],
        "title": sprint["title"] or sprint["id"],
        "status": sprint["status"],
        "reason": (
            f"All {len(stories)} linked US are terminal (✅/🚫/🧊) but sprint is {sprint['status']}. "
            "Close only via /complete-sprint with a real Retrospective (not the template placeholder)."
        ),
        "suggested_command": f"/complete-sprint {sprint['id']}",
    }


def epic_close_eligible(conn: sqlite3.Connection, epic_id: str) -> dict[str, Any] | None:
    epic = conn.execute(
        "SELECT id, title, status FROM epics WHERE id = ?",
        (epic_id,),
    ).fetchone()
    if not epic or epic["status"] != "active":
        return None
    must_rows = conn.execute(
        """
        SELECT id, status FROM user_stories
        WHERE epic_id = ? AND moscow = 'Must'
        ORDER BY id
        """,
        (epic_id,),
    ).fetchall()
    if not must_rows:
        # No Must US — treat as eligible only when there are zero non-terminal stories of any moscow
        any_open = conn.execute(
            """
            SELECT COUNT(*) AS c FROM user_stories
            WHERE epic_id = ? AND status NOT IN ('✅', '🚫', '🧊')
            """,
            (epic_id,),
        ).fetchone()
        if any_open and int(any_open["c"]) > 0:
            return None
        # Epic with only terminal (or no) stories
        total = conn.execute(
            "SELECT COUNT(*) AS c FROM user_stories WHERE epic_id = ?",
            (epic_id,),
        ).fetchone()
        if not total or int(total["c"]) == 0:
            return None
    else:
        if any(not terminal_story_status(r["status"]) for r in must_rows):
            return None
    return {
        "kind": "epic",
        "id": epic["id"],
        "title": epic["title"] or epic["id"],
        "status": epic["status"],
        "reason": (
            "No real open Must US remain but epic is still active. "
            "Close via /complete-epic only if outcome is still true; do not complete an empty epic."
        ),
        "suggested_command": f"/complete-epic {epic['id']}",
    }


def version_close_eligible(conn: sqlite3.Connection, version_id: str) -> dict[str, Any] | None:
    version = conn.execute(
        "SELECT id, title, status FROM versions WHERE id = ?",
        (version_id,),
    ).fetchone()
    if not version:
        return None
    if version["status"] not in ("planned", "active"):
        return None
    must_rows = conn.execute(
        """
        SELECT id, status FROM user_stories
        WHERE version_id = ? AND moscow = 'Must'
        ORDER BY id
        """,
        (version_id,),
    ).fetchall()
    if not must_rows:
        return None
    if any(not terminal_story_status(r["status"]) for r in must_rows):
        return None
    return {
        "kind": "version",
        "id": version["id"],
        "title": version["title"] or version["id"],
        "status": version["status"],
        "reason": "All Must US are terminal but version is not complete.",
        "suggested_command": f"update-version {version['id']} (set status: complete)",
    }


def collect_hygiene_findings(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for row in conn.execute("SELECT id FROM sprints ORDER BY id"):
        item = sprint_close_eligible(conn, row["id"])
        if item:
            findings.append(item)
    for row in conn.execute("SELECT id FROM epics ORDER BY id"):
        item = epic_close_eligible(conn, row["id"])
        if item:
            findings.append(item)
    for row in conn.execute("SELECT id FROM versions ORDER BY id"):
        item = version_close_eligible(conn, row["id"])
        if item:
            findings.append(item)
    return findings


def lifecycle_eligible_for_story(
    conn: sqlite3.Connection, story_id: str
) -> dict[str, Any]:
    """Cascade helpers after /complete-us — eligible containers for this story's context."""
    story = conn.execute(
        """
        SELECT id, sprint_id, epic_id, version_id, status
        FROM user_stories WHERE id = ?
        """,
        (story_id,),
    ).fetchone()
    if not story:
        raise ValueError(f"user story not found: {story_id}")

    result: dict[str, Any] = {
        "storyId": story_id,
        "storyStatus": story["status"],
        "sprint": None,
        "epic": None,
        "version": None,
    }
    if story["sprint_id"]:
        result["sprint"] = sprint_close_eligible(conn, story["sprint_id"])
    if story["epic_id"]:
        result["epic"] = epic_close_eligible(conn, story["epic_id"])
    if story["version_id"]:
        result["version"] = version_close_eligible(conn, story["version_id"])
    return result
