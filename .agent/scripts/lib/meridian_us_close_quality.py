"""Validator rules for closed (✅) user stories — blocks batch-close boilerplate."""

from __future__ import annotations

import re
from typing import Any

CLOSE_BOILERPLATE_RE = re.compile(
    r"see git diff|implemented and verified per|delivered in v\d+ implementation batch|"
    r"closed after implementation|see original us|_\(fill on close\)_|_\(pending until close\)_",
    re.IGNORECASE,
)

GENERIC_WHY_RE = re.compile(
    r"^EPIC-\d+\s+agentic quality siege\.?$",
    re.IGNORECASE,
)

MIN_WHY_CHARS = 40
MIN_RECORD_FILES_CHARS = 12
MIN_APPROACH_CHARS = 20


def validate_closed_us_row(row: Any, errors: list[str]) -> None:
    """Append errors when a ✅ US looks like a stub or batch-close overwrite."""
    if (row["status"] or "").strip() != "✅":
        return

    story_id = row["id"]
    body = row["body_markdown"] or ""
    why = (row["intent_why"] or "").strip()
    approach = (row["plan_approach"] or "").strip()
    record_files = (row["record_files"] or "").strip()
    acceptance = (row["intent_acceptance"] or "").strip()

    if not re.search(r"\*\*As\*\*.*\*\*I want\*\*", body, re.DOTALL | re.IGNORECASE):
        errors.append(
            f"{story_id}: status ✅ missing user-story preamble (**As** / **I want**) — "
            "likely overwritten; restore from git or re-run /refine-us before /complete-us"
        )

    if len(why) < MIN_WHY_CHARS or GENERIC_WHY_RE.match(why):
        errors.append(
            f"{story_id}: status ✅ has thin or generic ### Why — do not batch-close; "
            "use patch-record from show --full"
        )

    if len(approach) < MIN_APPROACH_CHARS:
        errors.append(
            f"{story_id}: status ✅ missing Plan / ### Approach (required after /refine-us) — "
            "restore refined Plan before close"
        )

    if len(record_files) < MIN_RECORD_FILES_CHARS:
        errors.append(f"{story_id}: status ✅ Record / Files too short — list real paths")

    for field_name, text in (
        ("Record / Files", record_files),
        ("Intent / Acceptance", acceptance),
        ("body", body),
    ):
        if text and CLOSE_BOILERPLATE_RE.search(text):
            errors.append(
                f"{story_id}: status ✅ contains batch-close placeholder in {field_name} — "
                "forbidden boilerplate"
            )
