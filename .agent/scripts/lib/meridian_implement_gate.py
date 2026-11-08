#!/usr/bin/env python3
"""Implement gate checks for /implement-us — SQLite + phase docs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from meridian_db import (
    check_story_dependencies_satisfied,
    connect,
    db_exists,
    load_story_dependencies,
    validate_story_open_sprint,
)
from meridian_markdown_parse import read_markdown_text

PLACEHOLDER_MARKERS = (
    "_(fill in",
    "_(pending)_",
    "§ [section name",
    "§ …",
    "path/to/…",
    "add when implementation scope is known",
    "§ tbd",
)

IMPLEMENTABLE_STATUSES = frozenset({"❌", "🔶"})


def _read_phase_frontmatter(docs: Path, filename: str) -> dict[str, str]:
    path = docs / filename
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def _is_placeholder(text: str | None) -> bool:
    if not text or not text.strip():
        return True
    lowered = text.lower()
    substantive = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
        and not line.strip().startswith("#")
        and line.strip() not in ("- _n/a_", "_n/a_", "- n/a", "n/a")
    ]
    if not substantive:
        return True
    joined = "\n".join(substantive).lower()
    return any(marker in joined for marker in PLACEHOLDER_MARKERS)


def _approach_bullet_count(approach: str | None) -> int:
    if not approach:
        return 0
    count = 0
    for line in approach.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")) and len(stripped) > 2:
            body = stripped.lstrip("-* ").strip()
            if body and body.lower() not in ("n/a", "_n/a_"):
                count += 1
    return count


def _architecture_refs_ok(refs: str | None, docs: Path) -> tuple[bool, str]:
    if _is_placeholder(refs):
        return False, "Architecture refs missing or placeholder"
    arch_path = docs / "05_architecture.md"
    if not arch_path.is_file():
        return False, "docs/05_architecture.md not found"
    text = refs or ""
    if "docs/architecture/" in text:
        for match in re.findall(r"docs/architecture/[A-Za-z0-9_./-]+\.md", text):
            rel = match.replace("docs/", "")
            if not (docs / rel).is_file():
                return False, f"Architecture ref file not found: {match}"
    if "§" in text or "05_architecture" in text:
        return True, ""
    if text.strip():
        return True, ""
    return False, "Architecture refs empty"


def check_implement_gate(package_root: str | Path, story_id: str) -> dict[str, Any]:
    """Return gate result dict: ok, story_id, checks[], failures[]."""
    root = Path(package_root).resolve()
    docs = root / "docs"
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    def add_check(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            failures.append({"check": name, "detail": detail})

    if not db_exists(root):
        add_check("meridian.db", False, f"run: python3 .agent/scripts/meridian_delivery.py bootstrap")
        return {"ok": False, "story_id": story_id, "checks": checks, "failures": failures}

    arch_fm = _read_phase_frontmatter(docs, "05_architecture.md")
    add_check(
        "05_architecture approved",
        arch_fm.get("status") == "approved",
        f"status={arch_fm.get('status') or 'missing'}",
    )

    conn = connect(root)
    try:
        row = conn.execute("SELECT * FROM user_stories WHERE id = ?", (story_id,)).fetchone()
        if not row:
            add_check("user story exists", False, f"{story_id} not in SQLite")
            return {"ok": False, "story_id": story_id, "checks": checks, "failures": failures}

        epic_id = row["epic_id"]
        version_id = row["version_id"]
        epic_ok = conn.execute("SELECT 1 FROM epics WHERE id = ?", (epic_id,)).fetchone() is not None
        version_ok = (
            conn.execute("SELECT 1 FROM versions WHERE id = ?", (version_id,)).fetchone() is not None
        )
        add_check(
            "epic + version",
            epic_ok and version_ok,
            f"epic={epic_id} ({'ok' if epic_ok else 'missing'}), version={version_id} ({'ok' if version_ok else 'missing'})",
        )

        ready = bool(row["ready"])
        add_check("ready", ready, "ready must be true — run /review-us after /refine-us")

        if ready:
            try:
                validate_story_open_sprint(conn, story_id)
                add_check("sprint scope", True, "assigned to planned/active sprint")
            except ValueError as exc:
                add_check("sprint scope", False, str(exc))

        approach = row["plan_approach"]
        approach_ok = not _is_placeholder(approach) and _approach_bullet_count(approach) >= 2
        add_check(
            "plan approach",
            approach_ok,
            f"need ≥2 Approach bullets; found {_approach_bullet_count(approach)}",
        )

        refs_ok, refs_detail = _architecture_refs_ok(row["plan_architecture_refs"], docs)
        add_check("architecture refs", refs_ok, refs_detail)

        deps = load_story_dependencies(conn, story_id)
        deps_ok, blocking = check_story_dependencies_satisfied(conn, story_id)
        add_check(
            "depends_on",
            deps_ok,
            f"blocking: {', '.join(blocking)}" if blocking else (f"deps: {deps}" if deps else "none"),
        )

        status = row["status"] or ""
        status_ok = status in IMPLEMENTABLE_STATUSES
        add_check(
            "story status",
            status_ok,
            f"status={status} (must be ❌ or 🔶)",
        )

        body = row["body_markdown"] or ""
        if body.strip():
            _fm, body_only, _full = read_markdown_text(body)
            plan_present = "## Plan" in body_only
            add_check("plan section", plan_present, "body_markdown must contain ## Plan")
    finally:
        conn.close()

    ok = len(failures) == 0
    return {"ok": ok, "story_id": story_id, "checks": checks, "failures": failures}
