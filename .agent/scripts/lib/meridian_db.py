#!/usr/bin/env python3
"""SQLite access layer for Meridian 2.0 delivery artifacts."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

US_ID_RE = re.compile(r"^US-\d{4}$")

from meridian_markdown_parse import extract_us_preamble
from meridian_paths import MIGRATIONS_DIR, REPO_ROOT

DB_FILENAME = "meridian.db"
MERIDIAN_DIR = ".meridian"


def resolve_db_path(package_root: str | Path) -> Path:
    return Path(package_root).resolve() / MERIDIAN_DIR / DB_FILENAME


def resolve_migrations_dir() -> Path:
    return MIGRATIONS_DIR


def connect(package_root: str | Path) -> sqlite3.Connection:
    db_path = resolve_db_path(package_root)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def db_exists(package_root: str | Path) -> bool:
    return resolve_db_path(package_root).is_file()


def list_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return [row["name"] for row in rows]


def applied_migrations(conn: sqlite3.Connection) -> set[str]:
    if "schema_migrations" not in list_tables(conn):
        return set()
    rows = conn.execute("SELECT name FROM schema_migrations").fetchall()
    return {row["name"] for row in rows}


def apply_migrations(package_root: str | Path) -> list[str]:
    migrations_dir = resolve_migrations_dir()
    if not migrations_dir.is_dir():
        raise FileNotFoundError(f"Migrations directory not found: {migrations_dir}")

    conn = connect(package_root)
    applied: list[str] = []
    try:
        already = applied_migrations(conn)
        for sql_file in sorted(migrations_dir.glob("*.sql")):
            name = sql_file.name
            if name in already:
                continue
            sql = sql_file.read_text(encoding="utf-8")
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations (name) VALUES (?)",
                (name,),
            )
            applied.append(name)
        conn.commit()
    finally:
        conn.close()
    return applied


def bootstrap(package_root: str | Path) -> str:
    if not is_meridian_package(package_root):
        raise ValueError(
            f"Not a Meridian product folder (missing docs/ fingerprint): {package_root}"
        )
    applied = apply_migrations(package_root)
    conn = connect(package_root)
    try:
        reconcile_msg = reconcile_sprint_links(conn)
        conn.commit()
    finally:
        conn.close()
    parts: list[str] = []
    if applied:
        parts.append(f"Applied migrations: {', '.join(applied)}")
    if reconcile_msg:
        parts.append(reconcile_msg)
    if parts:
        return "; ".join(parts)
    return "Database already up to date"


def is_meridian_package(package_root: str | Path) -> bool:
    docs = Path(package_root).resolve() / "docs"
    if not docs.is_dir():
        return False
    if (docs / "00_scope.md").exists():
        return True
    if db_exists(package_root):
        return True
    return any(docs.glob("us/US-*.md"))


def delivery_md_paths(docs: Path) -> list[Path]:
    """Legacy delivery markdown/json paths (excluded from phase docs)."""
    paths: list[Path] = []
    for folder, pattern in [
        ("us", "US-*.md"),
        ("epics", "EPIC-*.md"),
        ("versions", "v*.md"),
        ("sprints", "v*-S*.md"),
    ]:
        base = docs / folder
        if base.is_dir():
            paths.extend(sorted(base.glob(pattern)))
    decisions = docs / "decisions"
    if decisions.is_dir():
        paths.extend(sorted(decisions.glob("*.json")))
    return paths


def has_delivery_markdown(package_root: str | Path) -> bool:
    docs = Path(package_root).resolve() / "docs"
    return bool(delivery_md_paths(docs))


def _summary_from_frontmatter(frontmatter: dict[str, str]) -> str | None:
    return frontmatter.get("summary") or None


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def upsert_version(
    conn: sqlite3.Connection,
    frontmatter: dict[str, str],
    body: str,
    sections: dict[str, str | None],
) -> None:
    conn.execute(
        """
        INSERT INTO versions (
          id, title, status, outcome, objective, done_criteria,
          included, explicitly_out, go_live, body_markdown, summary, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          title=excluded.title, status=excluded.status, outcome=excluded.outcome,
          objective=excluded.objective, done_criteria=excluded.done_criteria,
          included=excluded.included, explicitly_out=excluded.explicitly_out,
          go_live=excluded.go_live, body_markdown=excluded.body_markdown,
          summary=COALESCE(excluded.summary, versions.summary),
          updated_at=excluded.updated_at
        """,
        (
            frontmatter.get("id"),
            frontmatter.get("title", ""),
            frontmatter.get("status", "planned"),
            frontmatter.get("outcome"),
            sections.get("objective"),
            sections.get("done_criteria"),
            sections.get("included"),
            sections.get("explicitly_out"),
            sections.get("go_live"),
            body,
            _summary_from_frontmatter(frontmatter) or sections.get("summary"),
            _now(),
        ),
    )


def upsert_epic(
    conn: sqlite3.Connection,
    frontmatter: dict[str, str],
    body: str,
    sections: dict[str, str | None],
) -> None:
    epic_id = frontmatter.get("id") or ""
    new_status = frontmatter.get("status", "active")
    if new_status == "complete" and epic_id:
        from meridian_container_integrity import epic_complete_blockers

        blockers = epic_complete_blockers(conn, epic_id, frontmatter.get("outcome"))
        if blockers:
            raise ValueError("; ".join(blockers))
    conn.execute(
        """
        INSERT INTO epics (
          id, title, status, outcome, profiles, versions,
          capability, expected_outcome, out_of_scope, notes, body_markdown, summary, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          title=excluded.title, status=excluded.status, outcome=excluded.outcome,
          profiles=excluded.profiles, versions=excluded.versions,
          capability=excluded.capability, expected_outcome=excluded.expected_outcome,
          out_of_scope=excluded.out_of_scope, notes=excluded.notes,
          body_markdown=excluded.body_markdown,
          summary=COALESCE(excluded.summary, epics.summary),
          updated_at=excluded.updated_at
        """,
        (
            frontmatter.get("id"),
            frontmatter.get("title", ""),
            frontmatter.get("status", "active"),
            frontmatter.get("outcome"),
            frontmatter.get("profiles"),
            frontmatter.get("versions"),
            sections.get("capability"),
            sections.get("expected_outcome"),
            sections.get("out_of_scope"),
            sections.get("notes"),
            body,
            _summary_from_frontmatter(frontmatter) or sections.get("summary"),
            _now(),
        ),
    )


OPEN_SPRINT_STATUSES = frozenset({"planned", "active"})


def _user_stories_has_sprint_column(conn: sqlite3.Connection) -> bool:
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(user_stories)")}
    return "sprint_id" in cols


def parse_sprint_id_from_frontmatter(frontmatter: dict[str, str]) -> str | None:
    raw = (frontmatter.get("sprint") or "").strip()
    if not raw or raw.lower() in {"n/a", "_n/a_", "tbd", "none", "null"}:
        return None
    return raw


def rebuild_sprint_scope_cache(conn: sqlite3.Connection, sprint_id: str) -> None:
    rows = conn.execute(
        """
        SELECT id FROM user_stories
        WHERE sprint_id = ?
        ORDER BY COALESCE(sprint_position, 0) ASC, id ASC
        """,
        (sprint_id,),
    ).fetchall()
    stories = [row["id"] for row in rows]
    conn.execute("DELETE FROM sprint_stories WHERE sprint_id = ?", (sprint_id,))
    for index, story_id in enumerate(stories):
        conn.execute(
            "INSERT OR REPLACE INTO sprint_stories (sprint_id, story_id, position) VALUES (?, ?, ?)",
            (sprint_id, story_id, index),
        )
    conn.execute(
        "UPDATE sprints SET stories_json = ?, updated_at = ? WHERE id = ?",
        (json.dumps(stories), _now(), sprint_id),
    )


def _pick_winning_sprint_row(
    conn: sqlite3.Connection, story_id: str
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT ss.sprint_id, ss.position, s.status AS sprint_status, s.version_id
        FROM sprint_stories ss
        JOIN sprints s ON s.id = ss.sprint_id
        WHERE ss.story_id = ?
        ORDER BY
          CASE s.status WHEN 'active' THEN 0 WHEN 'planned' THEN 1 ELSE 2 END,
          ss.position ASC,
          ss.sprint_id ASC
        LIMIT 1
        """,
        (story_id,),
    ).fetchone()


def reconcile_sprint_links(conn: sqlite3.Connection) -> str:
    """Backfill US sprint_id from junction, dedupe, rebuild sprint caches. Idempotent."""
    if not _user_stories_has_sprint_column(conn):
        return ""

    notes: list[str] = []

    for sprint_row in conn.execute(
        "SELECT id, version_id, stories_json FROM sprints"
    ):
        sprint_id = sprint_row["id"]
        count = conn.execute(
            "SELECT COUNT(*) AS c FROM sprint_stories WHERE sprint_id = ?",
            (sprint_id,),
        ).fetchone()["c"]
        if count:
            continue
        try:
            story_ids = json.loads(sprint_row["stories_json"] or "[]")
        except json.JSONDecodeError:
            story_ids = []
        if not isinstance(story_ids, list) or not story_ids:
            continue
        for index, story_id in enumerate(story_ids):
            sid = str(story_id).strip()
            if not sid:
                continue
            conn.execute(
                """
                INSERT OR IGNORE INTO sprint_stories (sprint_id, story_id, position)
                VALUES (?, ?, ?)
                """,
                (sprint_id, sid, index),
            )
        notes.append(f"rebuilt junction for {sprint_id} from stories_json")

    for row in conn.execute(
        """
        SELECT story_id, COUNT(*) AS c FROM sprint_stories
        GROUP BY story_id HAVING c > 1
        """
    ):
        winner = _pick_winning_sprint_row(conn, row["story_id"])
        if not winner:
            continue
        conn.execute(
            "DELETE FROM sprint_stories WHERE story_id = ? AND sprint_id != ?",
            (row["story_id"], winner["sprint_id"]),
        )
        notes.append(f"deduped {row['story_id']} → {winner['sprint_id']}")

    for row in conn.execute(
        """
        SELECT ss.story_id, ss.sprint_id, ss.position
        FROM sprint_stories ss
        """
    ):
        conn.execute(
            """
            UPDATE user_stories
            SET sprint_id = ?, sprint_position = ?
            WHERE id = ?
            """,
            (row["sprint_id"], row["position"], row["story_id"]),
        )

    for sprint_row in conn.execute("SELECT id FROM sprints"):
        rebuild_sprint_scope_cache(conn, sprint_row["id"])

    conn.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_sprint_stories_story_id
        ON sprint_stories(story_id)
        """
    )

    if notes:
        return f"Sprint link reconcile: {len(notes)} duplicate(s) fixed"
    return ""


def validate_story_open_sprint(conn: sqlite3.Connection, story_id: str) -> None:
    row = conn.execute(
        "SELECT version_id, sprint_id FROM user_stories WHERE id = ?",
        (story_id,),
    ).fetchone()
    if not row:
        raise ValueError(f"user story not found: {story_id}")
    sprint_id = row["sprint_id"]
    if not sprint_id:
        raise ValueError(
            f"{story_id} is not in any sprint — add sprint: <vX-SY> in frontmatter "
            f"or include the US in a sprint stories: list via /plan-sprint"
        )
    sprint = conn.execute(
        "SELECT version_id, status FROM sprints WHERE id = ?", (sprint_id,)
    ).fetchone()
    if not sprint:
        raise ValueError(f"{story_id} references unknown sprint {sprint_id}")
    if sprint["version_id"] != row["version_id"]:
        raise ValueError(
            f"{story_id} version {row['version_id']} does not match sprint {sprint_id} "
            f"(version {sprint['version_id']})"
        )
    if sprint["status"] not in OPEN_SPRINT_STATUSES:
        raise ValueError(
            f"{story_id} sprint {sprint_id} has status {sprint['status']} "
            f"(must be planned or active for ready: true)"
        )


def ensure_ready_has_open_sprint(conn: sqlite3.Connection, story_id: str) -> None:
    row = conn.execute(
        "SELECT ready FROM user_stories WHERE id = ?",
        (story_id,),
    ).fetchone()
    if not row:
        raise ValueError(f"user story not found: {story_id}")
    if not row["ready"]:
        return
    validate_story_open_sprint(conn, story_id)


def assign_story_sprint(
    conn: sqlite3.Connection,
    story_id: str,
    sprint_id: str | None,
    *,
    version_id: str,
    position: int | None = None,
) -> None:
    prev = conn.execute(
        "SELECT sprint_id FROM user_stories WHERE id = ?", (story_id,)
    ).fetchone()
    prev_sprint = prev["sprint_id"] if prev else None

    if not sprint_id:
        conn.execute(
            "UPDATE user_stories SET sprint_id = NULL, sprint_position = NULL WHERE id = ?",
            (story_id,),
        )
        if prev_sprint:
            rebuild_sprint_scope_cache(conn, prev_sprint)
        return

    sprint = conn.execute(
        "SELECT version_id, status FROM sprints WHERE id = ?", (sprint_id,)
    ).fetchone()
    if not sprint:
        raise ValueError(f"sprint not found: {sprint_id}")
    if sprint["version_id"] != version_id:
        raise ValueError(
            f"US {story_id} version {version_id} does not match sprint {sprint_id} "
            f"(version {sprint['version_id']})"
        )
    if sprint["status"] not in OPEN_SPRINT_STATUSES:
        raise ValueError(
            f"cannot assign {story_id} to sprint {sprint_id} with status "
            f"{sprint['status']} — use a planned/active sprint (do not restuff a "
            f"complete sprint; plan a new sprint instead)"
        )

    if position is None:
        if prev_sprint == sprint_id:
            existing = conn.execute(
                "SELECT sprint_position FROM user_stories WHERE id = ?", (story_id,)
            ).fetchone()
            if existing and existing["sprint_position"] is not None:
                position = int(existing["sprint_position"])
        if position is None:
            max_row = conn.execute(
                """
                SELECT COALESCE(MAX(sprint_position), -1) AS m
                FROM user_stories WHERE sprint_id = ?
                """,
                (sprint_id,),
            ).fetchone()
            position = int(max_row["m"]) + 1

    conn.execute(
        """
        UPDATE user_stories SET sprint_id = ?, sprint_position = ? WHERE id = ?
        """,
        (sprint_id, position, story_id),
    )
    if prev_sprint and prev_sprint != sprint_id:
        rebuild_sprint_scope_cache(conn, prev_sprint)
    rebuild_sprint_scope_cache(conn, sprint_id)


def apply_sprint_scope_from_list(
    conn: sqlite3.Connection,
    sprint_id: str,
    version_id: str,
    stories: list[str],
) -> None:
    normalized: list[str] = []
    seen: set[str] = set()
    for item in stories:
        sid = str(item).strip()
        if not sid or sid in seen:
            continue
        seen.add(sid)
        normalized.append(sid)

    in_list = set(normalized)
    for row in conn.execute(
        "SELECT id FROM user_stories WHERE sprint_id = ?", (sprint_id,)
    ):
        if row["id"] not in in_list:
            conn.execute(
                """
                UPDATE user_stories SET sprint_id = NULL, sprint_position = NULL
                WHERE id = ?
                """,
                (row["id"],),
            )

    for index, story_id in enumerate(normalized):
        us = conn.execute(
            "SELECT version_id FROM user_stories WHERE id = ?", (story_id,)
        ).fetchone()
        if not us:
            raise ValueError(f"sprint stories references unknown US: {story_id}")
        if us["version_id"] != version_id:
            raise ValueError(
                f"{story_id} version {us['version_id']} != sprint version {version_id}"
            )
        conn.execute(
            """
            UPDATE user_stories SET sprint_id = ?, sprint_position = ? WHERE id = ?
            """,
            (sprint_id, index, story_id),
        )

    rebuild_sprint_scope_cache(conn, sprint_id)


def upsert_sprint(
    conn: sqlite3.Connection,
    frontmatter: dict[str, str],
    body: str,
    sections: dict[str, str | None],
    stories: list[str],
) -> None:
    sprint_id = frontmatter.get("id") or ""
    new_status = frontmatter.get("status", "planned")
    prev = None
    if sprint_id:
        prev = conn.execute(
            "SELECT status FROM sprints WHERE id = ?", (sprint_id,)
        ).fetchone()
    if (
        prev
        and prev["status"] == "complete"
        and new_status in OPEN_SPRINT_STATUSES
    ):
        reopen_flag = str(frontmatter.get("reopen", "")).strip().lower()
        if reopen_flag not in {"true", "1", "yes"}:
            raise ValueError(
                f"sprint {sprint_id} is complete — reopening to {new_status} requires "
                f"frontmatter reopen: true and a decision log entry "
                f"(prefer a new sprint instead of restuffing a closed one)"
            )
    # reopen is a write-path flag only — never persist as a column
    frontmatter = {k: v for k, v in frontmatter.items() if k != "reopen"}

    if new_status == "complete" and sprint_id:
        from meridian_container_integrity import sprint_complete_blockers

        retro = sections.get("retrospective")
        blockers = sprint_complete_blockers(conn, sprint_id, retro, stories)
        if blockers:
            raise ValueError("; ".join(blockers))

    conn.execute(
        """
        INSERT INTO sprints (
          id, version_id, title, status, goal, done_when, stories_json,
          goal_body, scope_table, out_of_scope, retrospective, body_markdown, summary, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          version_id=excluded.version_id, title=excluded.title, status=excluded.status,
          goal=excluded.goal, done_when=excluded.done_when, stories_json=excluded.stories_json,
          goal_body=excluded.goal_body, scope_table=excluded.scope_table,
          out_of_scope=excluded.out_of_scope, retrospective=excluded.retrospective,
          body_markdown=excluded.body_markdown,
          summary=COALESCE(excluded.summary, sprints.summary),
          updated_at=excluded.updated_at
        """,
        (
            frontmatter.get("id"),
            frontmatter.get("version"),
            frontmatter.get("title", ""),
            new_status,
            frontmatter.get("goal"),
            frontmatter.get("done_when"),
            json.dumps(stories),
            sections.get("goal_body"),
            sections.get("scope_table"),
            sections.get("out_of_scope"),
            sections.get("retrospective"),
            body,
            _summary_from_frontmatter(frontmatter) or sections.get("summary"),
            _now(),
        ),
    )
    sprint_id = frontmatter.get("id") or ""
    version_id = frontmatter.get("version") or ""
    if _user_stories_has_sprint_column(conn):
        apply_sprint_scope_from_list(conn, sprint_id, version_id, stories)
    else:
        conn.execute("DELETE FROM sprint_stories WHERE sprint_id = ?", (sprint_id,))
        for index, story_id in enumerate(stories):
            conn.execute(
                "INSERT OR REPLACE INTO sprint_stories (sprint_id, story_id, position) VALUES (?, ?, ?)",
                (sprint_id, story_id, index),
            )


def normalize_depends_on(depends_on: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for item in depends_on:
        dep = str(item).strip()
        if not dep or dep in seen:
            continue
        seen.add(dep)
        normalized.append(dep)
    return normalized


def validate_story_dependency_ids(
    conn: sqlite3.Connection,
    story_id: str,
    depends_on: list[str],
) -> None:
    depends = normalize_depends_on(depends_on)
    for dep in depends:
        if not US_ID_RE.match(dep):
            raise ValueError(f"depends_on entry '{dep}' is not a valid US id (US-XXXX)")
        if dep == story_id:
            raise ValueError(f"depends_on cannot include self ({story_id})")
        row = conn.execute("SELECT 1 FROM user_stories WHERE id = ?", (dep,)).fetchone()
        if not row:
            raise ValueError(f"depends_on references unknown US: {dep}")
    if depends and _dependency_cycle_exists(conn, story_id, depends):
        raise ValueError(f"depends_on would create a cycle involving {story_id}")


def _dependency_cycle_exists(
    conn: sqlite3.Connection,
    story_id: str,
    new_deps: list[str],
) -> bool:
    visited: set[str] = set()
    stack = list(new_deps)
    while stack:
        current = stack.pop()
        if current == story_id:
            return True
        if current in visited:
            continue
        visited.add(current)
        rows = conn.execute(
            "SELECT depends_on_id FROM story_dependencies WHERE story_id = ?",
            (current,),
        ).fetchall()
        for row in rows:
            stack.append(row["depends_on_id"])
    return False


def sync_story_dependencies(
    conn: sqlite3.Connection,
    story_id: str,
    depends_on: list[str],
) -> list[str]:
    """Write junction rows (call after user_stories row exists)."""
    depends = normalize_depends_on(depends_on)
    conn.execute("DELETE FROM story_dependencies WHERE story_id = ?", (story_id,))
    for index, dep_id in enumerate(depends):
        conn.execute(
            """
            INSERT INTO story_dependencies (story_id, depends_on_id, position)
            VALUES (?, ?, ?)
            """,
            (story_id, dep_id, index),
        )
    return depends


def load_story_dependencies(conn: sqlite3.Connection, story_id: str) -> list[str]:
    rows = conn.execute(
        """
        SELECT depends_on_id FROM story_dependencies
        WHERE story_id = ? ORDER BY position
        """,
        (story_id,),
    ).fetchall()
    if rows:
        return [row["depends_on_id"] for row in rows]
    row = conn.execute(
        "SELECT depends_on_json FROM user_stories WHERE id = ?",
        (story_id,),
    ).fetchone()
    if not row:
        return []
    return json.loads(row["depends_on_json"] or "[]")


def check_story_dependencies_satisfied(
    conn: sqlite3.Connection,
    story_id: str,
) -> tuple[bool, list[str]]:
    blocking: list[str] = []
    for dep in load_story_dependencies(conn, story_id):
        row = conn.execute(
            "SELECT status FROM user_stories WHERE id = ?",
            (dep,),
        ).fetchone()
        if not row or row["status"] != "✅":
            blocking.append(dep)
    return len(blocking) == 0, blocking


def fetch_delivery_form_catalog(
    conn: sqlite3.Connection,
    *,
    exclude_story_id: str | None = None,
) -> dict[str, list[dict[str, str]]]:
    stories: list[dict[str, str]] = []
    for row in conn.execute(
        "SELECT id, title, status FROM user_stories ORDER BY id"
    ):
        if exclude_story_id and row["id"] == exclude_story_id:
            continue
        stories.append(
            {
                "id": row["id"],
                "title": row["title"],
                "status": row["status"],
            }
        )
    epics = [
        {"id": row["id"], "title": row["title"]}
        for row in conn.execute("SELECT id, title FROM epics ORDER BY id")
    ]
    versions = [
        {"id": row["id"], "title": row["title"]}
        for row in conn.execute("SELECT id, title FROM versions ORDER BY id")
    ]
    sprints = [
        {
            "id": row["id"],
            "title": row["title"],
            "status": row["status"] or "",
            "version": row["version_id"] or "",
        }
        for row in conn.execute(
            "SELECT id, title, status, version_id FROM sprints ORDER BY id"
        )
    ]
    return {"stories": stories, "epics": epics, "versions": versions, "sprints": sprints}


def upsert_user_story(
    conn: sqlite3.Connection,
    frontmatter: dict[str, str],
    body: str,
    sections: dict[str, str | None],
    depends_on: list[str],
) -> None:
    story_id = frontmatter.get("id") or ""
    version_id = frontmatter.get("version") or ""
    depends = normalize_depends_on(depends_on)
    validate_story_dependency_ids(conn, story_id, depends)
    ready_val = 1 if frontmatter.get("ready", "").lower() == "true" else 0

    sprint_target: str | None = None
    if _user_stories_has_sprint_column(conn):
        existing = conn.execute(
            "SELECT sprint_id FROM user_stories WHERE id = ?", (story_id,)
        ).fetchone()
        existing_sprint = existing["sprint_id"] if existing else None
        if "sprint" in frontmatter:
            sprint_target = parse_sprint_id_from_frontmatter(frontmatter)
        else:
            sprint_target = existing_sprint
        if ready_val and not sprint_target:
            raise ValueError(
                f"{story_id} ready: true requires sprint assignment "
                f"(frontmatter sprint: vX-SY or sprint stories: list)"
            )

    preamble = extract_us_preamble(body)
    conn.execute(
        """
        INSERT INTO user_stories (
          id, title, epic_id, version_id, status, moscow, depends_on_json, ready,
          done_when, tests, tests_status, preamble,
          intent_acceptance, intent_why, intent_where,
          plan_approach, plan_architecture_refs, plan_api_db, plan_security,
          plan_decisions, plan_planned,
          record_files, record_backend, record_frontend, record_scripts, record_executed,
          boundaries_out_of_scope, boundaries_notes, body_markdown, summary, updated_at
        ) VALUES (
          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        ON CONFLICT(id) DO UPDATE SET
          title=excluded.title, epic_id=excluded.epic_id, version_id=excluded.version_id,
          status=excluded.status, moscow=excluded.moscow, depends_on_json=excluded.depends_on_json,
          ready=excluded.ready, done_when=excluded.done_when, tests=excluded.tests,
          tests_status=excluded.tests_status, preamble=excluded.preamble,
          intent_acceptance=excluded.intent_acceptance, intent_why=excluded.intent_why,
          intent_where=excluded.intent_where, plan_approach=excluded.plan_approach,
          plan_architecture_refs=excluded.plan_architecture_refs, plan_api_db=excluded.plan_api_db,
          plan_security=excluded.plan_security, plan_decisions=excluded.plan_decisions,
          plan_planned=excluded.plan_planned, record_files=excluded.record_files,
          record_backend=excluded.record_backend, record_frontend=excluded.record_frontend,
          record_scripts=excluded.record_scripts, record_executed=excluded.record_executed,
          boundaries_out_of_scope=excluded.boundaries_out_of_scope,
          boundaries_notes=excluded.boundaries_notes, body_markdown=excluded.body_markdown,
          summary=COALESCE(excluded.summary, user_stories.summary),
          updated_at=excluded.updated_at
        """,
        (
            frontmatter.get("id"),
            frontmatter.get("title", ""),
            frontmatter.get("epic"),
            frontmatter.get("version"),
            frontmatter.get("status", "❌"),
            frontmatter.get("moscow", "Must"),
            json.dumps(depends),
            ready_val,
            frontmatter.get("done_when", ""),
            frontmatter.get("tests", "required"),
            frontmatter.get("tests_status", "pending"),
            preamble or None,
            sections.get("intent_acceptance"),
            sections.get("intent_why"),
            sections.get("intent_where"),
            sections.get("plan_approach"),
            sections.get("plan_architecture_refs"),
            sections.get("plan_api_db"),
            sections.get("plan_security"),
            sections.get("plan_decisions"),
            sections.get("plan_planned"),
            sections.get("record_files"),
            sections.get("record_backend"),
            sections.get("record_frontend"),
            sections.get("record_scripts"),
            sections.get("record_executed"),
            sections.get("boundaries_out_of_scope"),
            sections.get("boundaries_notes"),
            body,
            _summary_from_frontmatter(frontmatter) or sections.get("summary"),
            _now(),
        ),
    )
    sync_story_dependencies(conn, story_id, depends)
    if _user_stories_has_sprint_column(conn):
        assign_story_sprint(
            conn,
            story_id,
            sprint_target,
            version_id=version_id,
        )
        if ready_val:
            validate_story_open_sprint(conn, story_id)


DECISION_ENTRY_FIELDS = (
    "time",
    "title",
    "affected_document",
    "what_changed",
    "why_changed",
    "impact",
    "responsible",
)

DECISION_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DECISION_TIME_RE = re.compile(r"^\d{2}:\d{2}$")


def validate_decision_entry(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return ["entry must be an object"]
    time = entry.get("time")
    if not time or not DECISION_TIME_RE.match(str(time)):
        errors.append("time must be HH:MM (24h)")
    title = entry.get("title")
    if not title or not str(title).strip():
        errors.append("title is required")
    for field in DECISION_ENTRY_FIELDS:
        if field in ("time", "title"):
            continue
        if field not in entry or not str(entry.get(field, "")).strip():
            errors.append(f"missing {field}")
    return errors


def validate_decision_date(decision_date: str) -> list[str]:
    if not DECISION_DATE_RE.match(decision_date):
        return ["decision_date must use YYYY-MM-DD format"]
    return []


def prepend_decision(
    conn: sqlite3.Connection,
    decision_date: str,
    entry: dict[str, Any],
) -> int:
    """Prepend entry at index 0 for decision_date. Returns entry_index (always 0)."""
    date_errors = validate_decision_date(decision_date)
    entry_errors = validate_decision_entry(entry)
    errors = date_errors + entry_errors
    if errors:
        raise ValueError("; ".join(errors))
    conn.execute(
        "UPDATE decisions SET entry_index = entry_index + 1 WHERE decision_date = ?",
        (decision_date,),
    )
    conn.execute(
        """
        INSERT INTO decisions (decision_date, entry_index, title, payload_json)
        VALUES (?, 0, ?, ?)
        """,
        (decision_date, entry.get("title"), json.dumps(entry, ensure_ascii=False)),
    )
    return 0


def list_decision_dates(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    rows = conn.execute(
        """
        SELECT decision_date, COUNT(*) AS entry_count
        FROM decisions
        GROUP BY decision_date
        ORDER BY decision_date DESC
        """
    ).fetchall()
    return [(str(row["decision_date"]), int(row["entry_count"])) for row in rows]


def fetch_decisions_for_date(
    conn: sqlite3.Connection,
    decision_date: str,
) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT entry_index, title, payload_json
        FROM decisions
        WHERE decision_date = ?
        ORDER BY entry_index ASC
        """,
        (decision_date,),
    ).fetchall()
    entries: list[dict[str, Any]] = []
    for row in rows:
        payload = json.loads(row["payload_json"])
        payload.setdefault("title", row["title"])
        entries.append(payload)
    return entries


def export_decisions_by_date(package_root: str | Path) -> dict[str, list[dict[str, Any]]]:
    conn = connect(package_root)
    try:
        result: dict[str, list[dict[str, Any]]] = {}
        for decision_date, _ in list_decision_dates(conn):
            result[decision_date] = fetch_decisions_for_date(conn, decision_date)
        return result
    finally:
        conn.close()


def export_decisions_json(package_root: str | Path) -> dict[str, Any]:
    """Structured export for IDE extension decisions webview."""
    by_date = export_decisions_by_date(package_root)
    dates: list[dict[str, Any]] = []
    total_entries = 0
    for decision_date in sorted(by_date.keys(), reverse=True):
        entries = by_date[decision_date]
        total_entries += len(entries)
        dates.append(
            {
                "date": decision_date,
                "count": len(entries),
                "entries": entries,
            }
        )
    return {"dates": dates, "totalEntries": total_entries}


def import_decisions(conn: sqlite3.Connection, docs: Path) -> int:
    decisions_dir = docs / "decisions"
    count = 0
    if not decisions_dir.is_dir():
        return 0
    for path in sorted(decisions_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries = payload.get("entries", [])
        date = payload.get("date", path.stem)
        for index, entry in enumerate(entries):
            conn.execute(
                """
                INSERT INTO decisions (decision_date, entry_index, title, payload_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(decision_date, entry_index) DO UPDATE SET
                  title=excluded.title, payload_json=excluded.payload_json
                """,
                (date, index, entry.get("title"), json.dumps(entry, ensure_ascii=False)),
            )
            count += 1
    return count


def import_board_snapshot(conn: sqlite3.Connection, docs: Path, source: str = "import") -> int:
    board_path = docs / "kanban" / "board.json"
    if not board_path.exists():
        return 0
    payload = board_path.read_text(encoding="utf-8")
    board = json.loads(payload)
    card_count = len(board) if isinstance(board, list) else 0
    conn.execute(
        """
        INSERT INTO board_snapshots (source, card_count, payload_json)
        VALUES (?, ?, ?)
        """,
        (source, card_count, payload),
    )
    return card_count


def export_board_entries(package_root: str | Path) -> list[dict[str, Any]]:
    conn = connect(package_root)
    try:
        rows = conn.execute(
            """
            SELECT id, title, epic_id AS epic, version_id AS version, status, moscow,
                   depends_on_json, done_when, tests, tests_status, ready
            FROM user_stories ORDER BY id
            """
        ).fetchall()
        entries: list[dict[str, Any]] = []
        for row in rows:
            depends = load_story_dependencies(conn, row["id"])
            entries.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "epic": row["epic"],
                    "version": row["version"],
                    "status": row["status"],
                    "moscow": row["moscow"],
                    "depends_on": depends,
                    "done_when": row["done_when"],
                    "tests": row["tests"],
                    "tests_status": row["tests_status"],
                    "ready": bool(row["ready"]),
                }
            )
        return entries
    finally:
        conn.close()


def record_board_snapshot(package_root: str | Path, source: str = "upsert") -> int:
    """Store kanban card snapshot in SQLite only (v11 — no docs/kanban/board.json)."""
    entries = export_board_entries(package_root)
    payload = json.dumps(entries, ensure_ascii=False)
    conn = connect(package_root)
    try:
        conn.execute(
            """
            INSERT INTO board_snapshots (source, card_count, payload_json)
            VALUES (?, ?, ?)
            """,
            (source, len(entries), payload),
        )
        conn.commit()
    finally:
        conn.close()
    return len(entries)


def write_board_json(package_root: str | Path) -> int:
    """Deprecated alias — v11 writes board_snapshots only, not board.json."""
    return record_board_snapshot(package_root, source="legacy-write-board-json")


def load_delivery_markdown_files(package_root: str | Path) -> dict[str, list[tuple[str, str]]]:
    """Return virtual paths and full markdown for validator DB mode."""
    conn = connect(package_root)
    result: dict[str, list[tuple[str, str]]] = {
        "versions": [],
        "epics": [],
        "sprints": [],
        "user_stories": [],
    }
    try:
        for row in conn.execute("SELECT id, body_markdown FROM versions ORDER BY id"):
            text = row["body_markdown"] or ""
            result["versions"].append((f"{row['id']}.md", text))
        for row in conn.execute("SELECT id, body_markdown FROM epics ORDER BY id"):
            text = row["body_markdown"] or ""
            result["epics"].append((f"{row['id']}.md", text))
        for row in conn.execute("SELECT id, body_markdown FROM sprints ORDER BY id"):
            text = row["body_markdown"] or ""
            result["sprints"].append((f"{row['id']}.md", text))
        for row in conn.execute("SELECT id, body_markdown FROM user_stories ORDER BY id"):
            text = row["body_markdown"] or ""
            result["user_stories"].append((f"{row['id']}.md", text))
    finally:
        conn.close()
    return result


def export_planning_json(package_root: str | Path) -> dict[str, Any]:
    """Structured export for IDE extension (no markdown parse in TS)."""
    apply_migrations(package_root)
    conn = connect(package_root)
    try:
        stories = []
        for row in conn.execute(
            """
            SELECT id, title, epic_id, version_id, status, moscow,
                   done_when, tests, tests_status, ready, summary,
                   preamble, body_markdown, sprint_id, in_progress
            FROM user_stories ORDER BY id
            """
        ):
            preamble = (row["preamble"] or "").strip()
            if not preamble and row["body_markdown"]:
                preamble = extract_us_preamble(row["body_markdown"])
            stories.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "epic": row["epic_id"],
                    "version": row["version_id"],
                    "status": row["status"],
                    "moscow": row["moscow"],
                    "dependsOn": load_story_dependencies(conn, row["id"]),
                    "doneWhen": row["done_when"] or "",
                    "tests": row["tests"] or "required",
                    "testsStatus": row["tests_status"] or "pending",
                    "ready": bool(row["ready"]),
                    "inProgress": bool(row["in_progress"]),
                    "summary": row["summary"],
                    "preamble": preamble or None,
                    "sprint": row["sprint_id"] or None,
                }
            )
        versions = []
        for row in conn.execute(
            "SELECT id, title, status, outcome, summary FROM versions ORDER BY id"
        ):
            versions.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "status": row["status"],
                    "outcome": row["outcome"] or "",
                    "summary": row["summary"],
                }
            )
        epics = []
        for row in conn.execute(
            "SELECT id, title, status, outcome, versions, summary FROM epics ORDER BY id"
        ):
            versions_raw = row["versions"] or "[]"
            try:
                version_list = json.loads(versions_raw.replace("'", '"'))
            except json.JSONDecodeError:
                import re

                version_list = re.findall(r"v[\w.-]+", versions_raw)
            epics.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "status": row["status"],
                    "outcome": row["outcome"] or "",
                    "versions": version_list if isinstance(version_list, list) else [],
                    "summary": row["summary"],
                }
            )
        sprints = []
        for row in conn.execute(
            """
            SELECT id, version_id, title, status, goal, done_when, stories_json, summary
            FROM sprints ORDER BY id
            """
        ):
            sprints.append(
                {
                    "id": row["id"],
                    "version": row["version_id"],
                    "title": row["title"],
                    "status": row["status"],
                    "goal": row["goal"] or "",
                    "doneWhen": row["done_when"] or "",
                    "stories": json.loads(row["stories_json"] or "[]"),
                    "summary": row["summary"],
                }
            )
        return {
            "packageRoot": str(Path(package_root).resolve()),
            "userStories": stories,
            "versions": versions,
            "epics": epics,
            "sprints": sprints,
        }
    finally:
        conn.close()


def set_summary(
    conn: sqlite3.Connection,
    entity: str,
    entity_id: str,
    summary: str,
) -> bool:
    table_map = {
        "user_stories": "user_stories",
        "user_story": "user_stories",
        "us": "user_stories",
        "epics": "epics",
        "epic": "epics",
        "versions": "versions",
        "version": "versions",
        "sprints": "sprints",
        "sprint": "sprints",
    }
    table = table_map.get(entity)
    if not table:
        return False
    cur = conn.execute(
        f"UPDATE {table} SET summary = ?, updated_at = ? WHERE id = ?",
        (summary, _now(), entity_id),
    )
    return cur.rowcount > 0


def build_summary_from_story_row(row: sqlite3.Row) -> str:
    """Deterministic summary for backfill (no LLM)."""
    parts = [
        f"{row['id']} — {row['title']}.",
        f"Status {row['status']}, epic {row['epic_id']}, version {row['version_id']}.",
    ]
    if row["ready"]:
        parts.append("Ready for implementation.")
    if row["done_when"]:
        parts.append(f"Done when: {row['done_when']}")
    why = row["intent_why"] if "intent_why" in row.keys() else None
    if why:
        first = why.strip().split("\n")[0][:200]
        if first:
            parts.append(first)
    return " ".join(parts)


def backfill_summaries(package_root: str | Path) -> dict[str, int]:
    conn = connect(package_root)
    counts = {"user_stories": 0, "epics": 0, "versions": 0, "sprints": 0}
    try:
        for row in conn.execute(
            "SELECT * FROM user_stories WHERE summary IS NULL OR summary = ''"
        ):
            conn.execute(
                "UPDATE user_stories SET summary = ?, updated_at = ? WHERE id = ?",
                (build_summary_from_story_row(row), _now(), row["id"]),
            )
            counts["user_stories"] += 1
        for table, fields in [
            ("epics", ("title", "outcome", "status")),
            ("versions", ("title", "outcome", "status")),
            ("sprints", ("title", "goal", "status")),
        ]:
            for row in conn.execute(
                f"SELECT id, {', '.join(fields)} FROM {table} WHERE summary IS NULL OR summary = ''"
            ):
                title, extra, status = row[1], row[2], row[3]
                text = f"{row['id']} — {title}. Status {status}. {extra or ''}".strip()
                conn.execute(
                    f"UPDATE {table} SET summary = ?, updated_at = ? WHERE id = ?",
                    (text[:500], _now(), row["id"]),
                )
                counts[table] += 1
        conn.commit()
    finally:
        conn.close()
    return counts


ENTITY_TABLE_MAP: dict[str, str] = {
    "us": "user_stories",
    "user_story": "user_stories",
    "user_stories": "user_stories",
    "epic": "epics",
    "epics": "epics",
    "version": "versions",
    "versions": "versions",
    "sprint": "sprints",
    "sprints": "sprints",
}


def patch_user_story_record(
    package_root: str | Path,
    story_id: str,
    patch_text: str,
) -> dict[str, str]:
    """Merge Record (and optional Acceptance + frontmatter) into existing US markdown."""
    from meridian_markdown_parse import (  # noqa: PLC0415
        extract_us_sections,
        parse_depends_on,
        patch_us_record_markdown,
        read_markdown_text,
    )

    if not patch_text.strip():
        raise ValueError("empty patch")

    conn = connect(package_root)
    try:
        row = conn.execute(
            "SELECT body_markdown FROM user_stories WHERE id = ?",
            (story_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"{story_id} not found")
        existing = (row["body_markdown"] or "").strip()
        if not existing:
            raise ValueError(f"{story_id} has empty body_markdown — use update-us first")

        merged = patch_us_record_markdown(existing, patch_text)
        fm, body, full = read_markdown_text(merged)
        if fm.get("id") and fm["id"] != story_id:
            raise ValueError(f"patch frontmatter id {fm['id']} does not match {story_id}")
        fm["id"] = story_id
        depends = parse_depends_on(fm.get("depends_on"))
        sections = extract_us_sections(body)

        if (fm.get("status") or "").strip() == "✅":
            from meridian_us_close_quality import (
                validate_closed_us_row,  # noqa: PLC0415
            )

            preview = {
                "id": story_id,
                "status": fm.get("status"),
                "body_markdown": full,
                "intent_why": sections.get("intent_why"),
                "plan_approach": sections.get("plan_approach"),
                "record_files": sections.get("record_files"),
                "intent_acceptance": sections.get("intent_acceptance"),
            }
            close_errors: list[str] = []
            validate_closed_us_row(preview, close_errors)
            if close_errors:
                raise ValueError("; ".join(close_errors))

        upsert_user_story(conn, fm, full, sections, depends)
        status = (fm.get("status") or "").strip()
        if status in ("✅", "🧊", "🚫"):
            cols = {r[1] for r in conn.execute("PRAGMA table_info(user_stories)")}
            if "in_progress" in cols:
                conn.execute(
                    "UPDATE user_stories SET in_progress = 0, updated_at = datetime('now') WHERE id = ?",
                    (story_id,),
                )
        conn.commit()
    finally:
        conn.close()

    record_board_snapshot(package_root)
    return {"id": story_id, "entity": "user_stories"}


def upsert_delivery_from_markdown(
    package_root: str | Path,
    entity: str,
    entity_id: str,
    markdown_text: str,
) -> dict[str, str]:
    """Parse full delivery markdown and upsert the matching SQLite row."""
    from meridian_markdown_parse import (  # noqa: PLC0415
        extract_epic_sections,
        extract_sprint_sections,
        extract_us_sections,
        extract_version_sections,
        parse_depends_on,
        parse_stories_list,
        read_markdown_text,
    )

    if not markdown_text.strip():
        raise ValueError("empty markdown")

    fm, body, full = read_markdown_text(markdown_text)
    row_id = fm.get("id") or entity_id
    if row_id != entity_id:
        raise ValueError(f"frontmatter id {row_id} does not match {entity_id}")
    fm["id"] = entity_id

    entity_key = entity.lower().replace("-", "_")
    conn = connect(package_root)
    try:
        if entity_key in ("us", "user_story", "user_stories"):
            depends = parse_depends_on(fm.get("depends_on"))
            sections = extract_us_sections(body)
            if (fm.get("status") or "").strip() == "✅":
                from meridian_us_close_quality import (
                    validate_closed_us_row,  # noqa: PLC0415
                )

                preview = {
                    "id": entity_id,
                    "status": fm.get("status"),
                    "body_markdown": full,
                    "intent_why": sections.get("intent_why"),
                    "plan_approach": sections.get("plan_approach"),
                    "record_files": sections.get("record_files"),
                    "intent_acceptance": sections.get("intent_acceptance"),
                }
                close_errors: list[str] = []
                validate_closed_us_row(preview, close_errors)
                if close_errors:
                    raise ValueError(
                        "; ".join(close_errors)
                        + " — use `show --full`, edit in place, prefer `patch-record` for close"
                    )
            upsert_user_story(conn, fm, full, sections, depends)
        elif entity_key in ("epic", "epics"):
            upsert_epic(conn, fm, full, extract_epic_sections(body))
        elif entity_key in ("version", "versions"):
            upsert_version(conn, fm, full, extract_version_sections(body))
        elif entity_key in ("sprint", "sprints"):
            stories = parse_stories_list(fm.get("stories"))
            upsert_sprint(conn, fm, full, extract_sprint_sections(body), stories)
        else:
            raise ValueError(f"unknown entity: {entity}")
        conn.commit()
    finally:
        conn.close()

    record_board_snapshot(package_root)
    return {"id": entity_id, "entity": entity}


def export_entity_markdown(
    package_root: str | Path,
    entity: str,
    entity_id: str,
) -> dict[str, str] | None:
    """Return one delivery artifact body_markdown (single-row read)."""
    table = ENTITY_TABLE_MAP.get(entity.lower().replace("-", "_"))
    if not table:
        raise ValueError(f"unknown entity: {entity}")
    conn = connect(package_root)
    try:
        row = conn.execute(
            f"SELECT id, body_markdown FROM {table} WHERE id = ?",
            (entity_id,),
        ).fetchone()
        if not row:
            return None
        raw = (row["body_markdown"] or "").strip()
        if not raw:
            return None
        if table == "user_stories" and _user_stories_has_sprint_column(conn):
            from meridian_markdown_parse import (
                merge_us_sprint_into_markdown,  # noqa: PLC0415
            )

            sprint_row = conn.execute(
                "SELECT sprint_id FROM user_stories WHERE id = ?", (entity_id,)
            ).fetchone()
            sprint_id = sprint_row["sprint_id"] if sprint_row else None
            raw = merge_us_sprint_into_markdown(raw, sprint_id)
        return {"id": row["id"], "entity": entity, "raw": raw}
    finally:
        conn.close()


def export_delivery_json(package_root: str | Path) -> dict[str, Any]:
    files = load_delivery_markdown_files(package_root)
    return {
        "packageRoot": str(Path(package_root).resolve()),
        "userStories": [{"file": name, "raw": raw} for name, raw in files["user_stories"]],
        "epics": [{"file": name, "raw": raw} for name, raw in files["epics"]],
        "versions": [{"file": name, "raw": raw} for name, raw in files["versions"]],
        "sprints": [{"file": name, "raw": raw} for name, raw in files["sprints"]],
    }


def next_user_story_id(package_root: str | Path) -> str:
    conn = connect(package_root)
    try:
        row = conn.execute(
            "SELECT id FROM user_stories ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if not row:
            return "US-0001"
        num = int(str(row["id"]).split("-")[1])
        return f"US-{num + 1:04d}"
    finally:
        conn.close()


def next_epic_id(package_root: str | Path) -> str:
    conn = connect(package_root)
    try:
        rows = conn.execute("SELECT id FROM epics").fetchall()
        max_num = 0
        for row in rows:
            match = re.match(r"^EPIC-(\d+)$", str(row["id"]))
            if match:
                max_num = max(max_num, int(match.group(1)))
        return f"EPIC-{max_num + 1:02d}"
    finally:
        conn.close()


def next_sprint_id(package_root: str | Path, version_id: str) -> str:
    conn = connect(package_root)
    try:
        rows = conn.execute(
            "SELECT id FROM sprints WHERE version_id = ?", (version_id,)
        ).fetchall()
        max_num = 0
        prefix = f"{version_id}-S"
        for row in rows:
            story_id = str(row["id"])
            if story_id.startswith(prefix):
                suffix = story_id[len(prefix) :]
                if suffix.isdigit():
                    max_num = max(max_num, int(suffix))
        return f"{prefix}{max_num + 1}"
    finally:
        conn.close()


def delivery_counts(package_root: str | Path) -> dict[str, int]:
    conn = connect(package_root)
    try:
        return {
            "versions": conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0],
            "epics": conn.execute("SELECT COUNT(*) FROM epics").fetchone()[0],
            "sprints": conn.execute("SELECT COUNT(*) FROM sprints").fetchone()[0],
            "user_stories": conn.execute("SELECT COUNT(*) FROM user_stories").fetchone()[0],
            "decisions": conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0],
        }
    finally:
        conn.close()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Meridian SQLite utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tables", help="List tables").add_argument(
        "package_root", nargs="?", default="."
    )
    migrate_p = sub.add_parser("migrate", help="Apply pending migrations")
    migrate_p.add_argument("package_root", nargs="?", default=".")

    args = parser.parse_args()
    root = getattr(args, "package_root", ".")

    if args.command == "list-tables":
        conn = connect(root)
        try:
            for name in list_tables(conn):
                print(name)
        finally:
            conn.close()
        return 0

    if args.command == "migrate":
        print(bootstrap(root))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
