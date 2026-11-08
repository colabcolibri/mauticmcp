"""Derived kanban column for the kit HTML monitor.

Mirrors `resolveColumn` in app-visual-studio/src/board-webview-html.ts.
Do not add this field to meridian_db_export --format planning.
"""

from __future__ import annotations

from typing import Any, Mapping

COLUMN_ORDER = (
    "backlog",
    "todo",
    "doing",
    "🔶",
    "🧪",
    "✅",
    "🧊",
    "🚫",
)

COLUMN_LABELS = {
    "backlog": "📋 Backlog",
    "todo": "📌 Todo",
    "doing": "🔨 Doing",
    "🔶": "🔶 Partial",
    "🧪": "🧪 Tests",
    "✅": "✅ Done",
    "🧊": "🧊 Frozen",
    "🚫": "🚫 Deprecated",
}


def resolve_column(story: Mapping[str, Any]) -> str:
    status = story.get("status") or ""
    if status == "🧊":
        return "🧊"
    if status == "🚫":
        return "🚫"
    in_progress = story.get("inProgress") is True
    if in_progress and status in ("❌", "🔶"):
        return "doing"
    if status == "❌":
        return "todo" if story.get("ready") is True else "backlog"
    if story.get("tests") == "required" and story.get("testsStatus") == "pending":
        return "🧪"
    return status or "backlog"


def stories_with_columns(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for story in stories:
        row = dict(story)
        row["column"] = resolve_column(story)
        out.append(row)
    return out
