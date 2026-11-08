"""Build the kit HTML monitor snapshot from existing delivery exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from meridian_board_columns import stories_with_columns
from meridian_board_watch import db_fingerprint
from meridian_db import db_exists, export_decisions_json, export_planning_json


def build_snapshot(package_root: str | Path) -> dict[str, Any]:
    root = Path(package_root).resolve()
    if not db_exists(root):
        return {
            "error": "meridian.db not found",
            "hint": "python3 .agent/scripts/meridian_delivery.py bootstrap",
            "packageRoot": str(root),
            "generation": db_fingerprint(root),
        }
    planning = export_planning_json(root)
    decisions = export_decisions_json(root)
    stories = stories_with_columns(list(planning.get("userStories") or []))
    return {
        "packageRoot": planning.get("packageRoot", str(root)),
        "generation": db_fingerprint(root),
        "userStories": stories,
        "versions": planning.get("versions") or [],
        "epics": planning.get("epics") or [],
        "sprints": planning.get("sprints") or [],
        "decisions": decisions,
    }
