#!/usr/bin/env python3
"""Contract tests for meridian_db_export --format planning (US-0175)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT = _SCRIPT_DIR.parents[2]
sys.path.insert(0, str(_SCRIPTS_ROOT / "lib"))

from meridian_db import bootstrap, connect, upsert_epic, upsert_user_story, upsert_version  # noqa: E402

SCHEMA_PATH = _SCRIPT_DIR / "fixtures" / "planning-export.schema.json"
EXPORT_SCRIPT = _SCRIPTS_ROOT / "meridian_db_export.py"

US_BODY = """# US-0001 — Contract seed

## Intent

### Acceptance

- [ ] Works

### Why

Seed for contract test.

### Where

Test fixture.
"""


def _validate_against_schema(data: dict, schema: dict) -> list[str]:
    """Minimal JSON-schema validation (stdlib only) for planning export contract."""
    errors: list[str] = []

    def check_type(value, expected: str, path: str) -> None:
        type_map = {
            "string": str,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        if expected not in type_map or not isinstance(value, type_map[expected]):
            errors.append(f"{path}: expected {expected}, got {type(value).__name__}")

    def walk(instance, subschema: dict, path: str) -> None:
        if "type" in subschema:
            check_type(instance, subschema["type"], path)
        if subschema.get("type") == "object" and isinstance(instance, dict):
            for key in subschema.get("required", []):
                if key not in instance:
                    errors.append(f"{path}: missing required key {key!r}")
            props = subschema.get("properties", {})
            for key, prop_schema in props.items():
                if key in instance:
                    walk(instance[key], prop_schema, f"{path}.{key}")
        if subschema.get("type") == "array" and isinstance(instance, list):
            item_schema = subschema.get("items", {})
            for index, item in enumerate(instance):
                walk(item, item_schema, f"{path}[{index}]")
        if subschema.get("type") == "string" and isinstance(instance, str):
            min_len = subschema.get("minLength")
            if min_len is not None and len(instance) < min_len:
                errors.append(f"{path}: string shorter than minLength {min_len}")
            pattern = subschema.get("pattern")
            if pattern:
                import re

                if not re.match(pattern, instance):
                    errors.append(f"{path}: does not match pattern {pattern!r}")

    walk(instance=data, subschema=schema, path="$")
    return errors


def _seed_minimal_delivery(root: Path) -> None:
    bootstrap(root)
    conn = connect(root)
    try:
        upsert_version(
            conn,
            {"id": "v1", "title": "One", "status": "planned", "outcome": ""},
            "# v1\n",
            {},
        )
        upsert_epic(
            conn,
            {
                "id": "EPIC-01",
                "title": "Seed",
                "status": "active",
                "versions": "[v1]",
                "profiles": "[]",
                "outcome": "",
            },
            "# EPIC-01\n",
            {},
        )
        upsert_user_story(
            conn,
            {
                "id": "US-0001",
                "title": "Contract seed",
                "epic": "EPIC-01",
                "version": "v1",
                "status": "❌",
                "moscow": "Must",
                "depends_on": "[]",
                "ready": "false",
                "done_when": "",
                "tests": "required",
                "tests_status": "pending",
            },
            US_BODY,
            {},
            [],
        )
        conn.commit()
    finally:
        conn.close()


def _export_planning(root: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT), str(root), "--format", "planning"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="meridian-planning-contract-") as tmp:
        root = Path(tmp)
        (root / "docs").mkdir()
        (root / "docs" / "00_scope.md").write_text("# scope\n", encoding="utf-8")
        _seed_minimal_delivery(root)
        payload = _export_planning(root)
        errors = _validate_against_schema(payload, schema)
        if errors:
            for err in errors:
                print(f"FAIL: {err}", file=sys.stderr)
            return 1
        if not payload["userStories"]:
            print("FAIL: userStories empty", file=sys.stderr)
            return 1
        print("OK: planning export contract test passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
