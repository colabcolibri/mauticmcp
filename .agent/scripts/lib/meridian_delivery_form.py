#!/usr/bin/env python3
"""Structured delivery form export/import — build markdown, validate, upsert."""

from __future__ import annotations

import json
import re
from typing import Any

from meridian_db import export_entity_markdown, upsert_delivery_from_markdown
from meridian_db import connect, fetch_delivery_form_catalog, load_story_dependencies
from meridian_markdown_parse import (
    extract_epic_sections,
    extract_sprint_sections,
    extract_us_preamble,
    extract_us_sections,
    extract_version_sections,
    format_depends_on,
    parse_depends_on,
    read_markdown_text,
)
from meridian_section_contracts import (
    validate_epic_structure,
    validate_us_structure,
    validate_version_structure,
)


def _split_preamble(body: str) -> tuple[str, str]:
    match = re.search(r"^## ", body, re.MULTILINE)
    if not match:
        return extract_us_preamble(body), ""
    idx = match.start()
    return body[:idx].strip(), body[idx:].strip()


def _format_frontmatter(frontmatter: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        if value is None:
            continue
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def _section_block(heading: str, body: str | None) -> str:
    content = (body or "").strip()
    return f"## {heading}\n\n{content}\n"


def _subsection_block(heading: str, body: str | None) -> str:
    content = (body or "").strip()
    return f"### {heading}\n\n{content}\n"


def build_us_markdown(
    frontmatter: dict[str, str],
    preamble: str,
    sections: dict[str, str | None],
) -> str:
    body_parts: list[str] = []
    if preamble.strip():
        body_parts.append(preamble.strip())
        body_parts.append("")

    intent = "\n".join(
        [
            _subsection_block("Acceptance", sections.get("intent_acceptance")),
            _subsection_block("Why", sections.get("intent_why")),
            _subsection_block("Where", sections.get("intent_where")),
        ]
    ).strip()
    body_parts.append(f"## Intent\n\n{intent}\n")

    plan_parts = [
        _subsection_block("Approach", sections.get("plan_approach")),
        _subsection_block("Architecture refs", sections.get("plan_architecture_refs")),
        _subsection_block("API / DB impact", sections.get("plan_api_db")),
        _subsection_block("Security notes", sections.get("plan_security")),
        _subsection_block("Related decisions", sections.get("plan_decisions")),
        _subsection_block("Planned", sections.get("plan_planned")),
    ]
    plan = "\n".join(part for part in plan_parts if part.strip()).strip()
    body_parts.append(f"## Plan\n\n{plan}\n")

    record = "\n".join(
        [
            _subsection_block("Files", sections.get("record_files")),
            _subsection_block("Backend", sections.get("record_backend")),
            _subsection_block("Frontend", sections.get("record_frontend")),
            _subsection_block("Scripts / Docs", sections.get("record_scripts")),
            _subsection_block("Executed", sections.get("record_executed")),
        ]
    ).strip()
    body_parts.append(f"## Record\n\n{record}\n")

    boundaries = "\n".join(
        [
            _subsection_block(
                "Out of scope for this story",
                sections.get("boundaries_out_of_scope"),
            ),
            _subsection_block("Notes", sections.get("boundaries_notes")),
        ]
    ).strip()
    body_parts.append(f"## Boundaries\n\n{boundaries}\n")

    body = "\n".join(body_parts).strip() + "\n"
    return f"{_format_frontmatter(frontmatter)}\n{body}"


def build_epic_markdown(
    frontmatter: dict[str, str],
    preamble: str,
    sections: dict[str, str | None],
) -> str:
    body_parts: list[str] = []
    if preamble.strip():
        body_parts.append(preamble.strip())
        body_parts.append("")
    body_parts.append(_section_block("Capability", sections.get("capability")))
    body_parts.append(_section_block("Expected outcome", sections.get("expected_outcome")))
    body_parts.append(
        _section_block("Out of scope for this epic", sections.get("out_of_scope"))
    )
    if sections.get("notes"):
        body_parts.append(_section_block("Notes", sections.get("notes")))
    body = "\n".join(body_parts).strip() + "\n"
    return f"{_format_frontmatter(frontmatter)}\n{body}"


def build_version_markdown(
    frontmatter: dict[str, str],
    preamble: str,
    sections: dict[str, str | None],
) -> str:
    body_parts: list[str] = []
    if preamble.strip():
        body_parts.append(preamble.strip())
        body_parts.append("")
    body_parts.append(_section_block("Objective", sections.get("objective")))
    body_parts.append(_section_block("Done criteria", sections.get("done_criteria")))
    body_parts.append(
        _section_block("Included in this version", sections.get("included"))
    )
    body_parts.append(_section_block("Explicitly out", sections.get("explicitly_out")))
    body_parts.append(_section_block("Go-live checklist", sections.get("go_live")))
    body = "\n".join(body_parts).strip() + "\n"
    return f"{_format_frontmatter(frontmatter)}\n{body}"


def build_sprint_markdown(
    frontmatter: dict[str, str],
    preamble: str,
    sections: dict[str, str | None],
) -> str:
    body_parts: list[str] = []
    if preamble.strip():
        body_parts.append(preamble.strip())
        body_parts.append("")
    body_parts.append(_section_block("Goal", sections.get("goal_body")))
    body_parts.append(_section_block("Scope", sections.get("scope_table")))
    body_parts.append(
        _section_block("Out of scope for this sprint", sections.get("out_of_scope"))
    )
    body_parts.append(_section_block("Retrospective", sections.get("retrospective")))
    body = "\n".join(body_parts).strip() + "\n"
    return f"{_format_frontmatter(frontmatter)}\n{body}"


def _validate_markdown(entity: str, entity_id: str, markdown: str) -> tuple[list[str], list[str]]:
    fm, body, _full = read_markdown_text(markdown)
    if fm.get("id") and fm.get("id") != entity_id:
        return [f"frontmatter id {fm.get('id')} does not match {entity_id}"], []
    errors: list[str] = []
    warnings: list[str] = []
    entity_key = entity.lower()
    if entity_key == "us":
        validate_us_structure(entity_id, body, fm, errors, warnings)
    elif entity_key == "epics":
        validate_epic_structure(entity_id, body, errors, warnings)
    elif entity_key == "versions":
        validate_version_structure(entity_id, body, errors, warnings)
    return errors, warnings


def export_entity_form(
    package_root: str,
    entity: str,
    entity_id: str,
) -> dict[str, Any] | None:
    row = export_entity_markdown(package_root, entity, entity_id)
    if not row:
        return None
    fm, body, _full = read_markdown_text(row["raw"])
    preamble, section_body = _split_preamble(body)
    entity_key = entity.lower()
    payload: dict[str, Any] = {
        "entity": entity_key,
        "id": entity_id,
        "frontmatter": fm,
        "preamble": preamble,
        "sections": {},
    }
    if entity_key == "us":
        conn = connect(package_root)
        try:
            depends = load_story_dependencies(conn, entity_id)
            payload["frontmatter"]["depends_on"] = format_depends_on(depends)
            sprint_row = conn.execute(
                "SELECT sprint_id FROM user_stories WHERE id = ?", (entity_id,)
            ).fetchone()
            if sprint_row and sprint_row["sprint_id"]:
                payload["frontmatter"]["sprint"] = sprint_row["sprint_id"]
            elif "sprint" in payload["frontmatter"] and not payload["frontmatter"]["sprint"]:
                payload["frontmatter"].pop("sprint", None)
            payload["catalog"] = fetch_delivery_form_catalog(
                conn, exclude_story_id=entity_id
            )
        finally:
            conn.close()
        payload["sections"] = extract_us_sections(section_body)
    elif entity_key == "epics":
        payload["sections"] = extract_epic_sections(section_body)
    elif entity_key == "versions":
        payload["sections"] = extract_version_sections(section_body)
    elif entity_key == "sprints":
        payload["sections"] = extract_sprint_sections(section_body)
    else:
        raise ValueError(f"unknown entity: {entity}")
    return payload


def build_markdown_from_form(payload: dict[str, Any]) -> str:
    entity = str(payload.get("entity", "")).lower()
    frontmatter = {str(k): str(v) for k, v in (payload.get("frontmatter") or {}).items()}
    preamble = str(payload.get("preamble") or "")
    sections = {
        str(k): (None if v is None else str(v))
        for k, v in (payload.get("sections") or {}).items()
    }
    if entity == "us":
        return build_us_markdown(frontmatter, preamble, sections)
    if entity == "epics":
        return build_epic_markdown(frontmatter, preamble, sections)
    if entity == "versions":
        return build_version_markdown(frontmatter, preamble, sections)
    if entity == "sprints":
        return build_sprint_markdown(frontmatter, preamble, sections)
    raise ValueError(f"unknown entity: {entity}")


def import_entity_form(
    package_root: str,
    entity: str,
    entity_id: str,
    payload: dict[str, Any],
) -> dict[str, str]:
    payload = dict(payload)
    payload["entity"] = entity.lower()
    payload["id"] = entity_id
    if "frontmatter" not in payload or not isinstance(payload["frontmatter"], dict):
        raise ValueError("frontmatter object is required")
    payload["frontmatter"]["id"] = entity_id
    if entity.lower() == "us":
        depends = parse_depends_on(str(payload["frontmatter"].get("depends_on")))
        payload["frontmatter"]["depends_on"] = format_depends_on(depends)
    markdown = build_markdown_from_form(payload)
    errors, _warnings = _validate_markdown(entity, entity_id, markdown)
    if errors:
        raise ValueError("; ".join(errors[:8]))
    upsert_delivery_from_markdown(package_root, entity, entity_id, markdown)
    return {"id": entity_id, "entity": entity.lower()}


def import_entity_form_json(
    package_root: str,
    entity: str,
    entity_id: str,
    json_text: str,
) -> dict[str, str]:
    payload = json.loads(json_text)
    return import_entity_form(package_root, entity, entity_id, payload)
