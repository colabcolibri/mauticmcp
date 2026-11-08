"""Integrity gates for closing sprints and epics (retrospective + Must US)."""

from __future__ import annotations

import re
import sqlite3
from meridian_lifecycle import sprint_stories, terminal_story_status

RETRO_PLACEHOLDER_RE = re.compile(
    r"fill at sprint close|_\(fill|_pending until close_|tbd retro",
    re.IGNORECASE,
)

EMPTY_BULLET_ONLY_RE = re.compile(
    r"what worked:\s*(?:-\s*)*\s*what to improve:\s*(?:-\s*)*(?:decisions to log:\s*(?:-\s*|_n/a_)*)?\s*$",
    re.IGNORECASE | re.DOTALL,
)

MIN_RETRO_CHARS = 80
MIN_EPIC_OUTCOME_CHARS = 24


def retrospective_is_filled(text: str | None) -> bool:
    raw = (text or "").strip()
    if len(raw) < MIN_RETRO_CHARS:
        return False
    if RETRO_PLACEHOLDER_RE.search(raw):
        return False
    collapsed = re.sub(r"\s+", " ", raw)
    if EMPTY_BULLET_ONLY_RE.match(collapsed):
        return False
    lowered = raw.lower()
    if "what worked" in lowered and "what to improve" in lowered:
        return True
    # Allow a dense paragraph retro without those headings if long enough
    return len(raw) >= 160


def sprint_complete_blockers(
    conn: sqlite3.Connection,
    sprint_id: str,
    retrospective: str | None,
    stories_from_frontmatter: list[str] | None = None,
) -> list[str]:
    blockers: list[str] = []
    if not retrospective_is_filled(retrospective):
        blockers.append(
            f"{sprint_id}: cannot set status complete — Retrospective is empty or placeholder. "
            "Fill What worked / What to improve with evidence (US Records, validator WARNs, station bounces). "
            "Decisions to log may be _n/a_."
        )
    rows = sprint_stories(conn, sprint_id)
    ids = {r["id"] for r in rows}
    if stories_from_frontmatter:
        ids.update(s for s in stories_from_frontmatter if s)
    if not ids:
        blockers.append(
            f"{sprint_id}: cannot set status complete — sprint has no linked user stories."
        )
        return blockers
    open_ids: list[str] = []
    for sid in sorted(ids):
        row = conn.execute(
            "SELECT id, status FROM user_stories WHERE id = ?", (sid,)
        ).fetchone()
        if not row:
            blockers.append(f"{sprint_id}: stories list references unknown {sid}")
            continue
        if not terminal_story_status(row["status"]):
            open_ids.append(f"{sid} ({row['status']})")
    if open_ids:
        blockers.append(
            f"{sprint_id}: cannot set status complete — non-terminal US remain: "
            + ", ".join(open_ids)
        )
    return blockers


def epic_complete_blockers(conn: sqlite3.Connection, epic_id: str, outcome: str | None) -> list[str]:
    blockers: list[str] = []
    must_rows = conn.execute(
        """
        SELECT id, status FROM user_stories
        WHERE epic_id = ? AND moscow = 'Must'
        ORDER BY id
        """,
        (epic_id,),
    ).fetchall()
    open_must = [
        f"{r['id']} ({r['status']})"
        for r in must_rows
        if not terminal_story_status(r["status"])
    ]
    if open_must:
        blockers.append(
            f"{epic_id}: cannot set status complete — open Must US: " + ", ".join(open_must)
        )
    total = conn.execute(
        "SELECT COUNT(*) AS c FROM user_stories WHERE epic_id = ?",
        (epic_id,),
    ).fetchone()
    if not must_rows and (not total or int(total["c"]) == 0):
        blockers.append(
            f"{epic_id}: cannot set status complete — epic has no user stories."
        )
    oc = (outcome or "").strip()
    if len(oc) < MIN_EPIC_OUTCOME_CHARS:
        blockers.append(
            f"{epic_id}: cannot set status complete — frontmatter outcome is missing or too thin "
            f"(need ≥{MIN_EPIC_OUTCOME_CHARS} characters, observable product signal)."
        )
    return blockers


def collect_closed_container_warnings(conn: sqlite3.Connection) -> list[str]:
    """Existing complete rows that fail the same bar (WARN — do not fail historical dogfood)."""
    warnings: list[str] = []
    for sprint in conn.execute(
        "SELECT id, retrospective, body_markdown FROM sprints WHERE status = 'complete'"
    ):
        retro = sprint["retrospective"]
        if not retro and sprint["body_markdown"]:
            from meridian_markdown_parse import extract_sprint_sections

            retro = extract_sprint_sections(sprint["body_markdown"] or "").get("retrospective")
        for msg in sprint_complete_blockers(conn, sprint["id"], retro, None):
            if "cannot set status complete" in msg:
                warnings.append("container-integrity: " + msg.replace("cannot set status complete — ", "status complete but "))
            else:
                warnings.append(f"container-integrity: {msg}")
    for epic in conn.execute("SELECT id, outcome FROM epics WHERE status = 'complete'"):
        for msg in epic_complete_blockers(conn, epic["id"], epic["outcome"]):
            warnings.append(
                "container-integrity: "
                + msg.replace("cannot set status complete — ", "status complete but ")
            )
    return warnings
