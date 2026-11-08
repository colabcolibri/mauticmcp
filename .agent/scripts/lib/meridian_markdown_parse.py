#!/usr/bin/env python3
"""Shared Markdown + frontmatter parsing for Meridian kit scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from meridian_section_contracts import (  # noqa: E402
    extract_section_body,
    extract_subsection_body,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter_dict(text: str) -> dict[str, str]:
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


def parse_depends_on(value: str | None) -> list[str]:
    if not value or value == "[]":
        return []
    if value.startswith("["):
        inner = value.strip().strip("[]")
        if not inner:
            return []
        try:
            parsed = json.loads(value.replace("'", '"'))
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except json.JSONDecodeError:
            pass
        return [part.strip() for part in inner.split(",") if part.strip()]
    return [part.strip() for part in value.split(",") if part.strip()]


def format_depends_on(ids: list[str]) -> str:
    cleaned = [item.strip() for item in ids if item and str(item).strip()]
    if not cleaned:
        return "[]"
    return "[" + ", ".join(cleaned) + "]"


def parse_stories_list(value: str | None) -> list[str]:
    return parse_depends_on(value)


def read_markdown_file(path: Path) -> tuple[dict[str, str], str, str]:
    text = path.read_text(encoding="utf-8")
    return read_markdown_text(text)


def read_markdown_text(text: str) -> tuple[dict[str, str], str, str]:
    fm = parse_frontmatter_dict(text)
    match = FRONTMATTER_RE.match(text)
    body = text[match.end() :] if match else text
    return fm, body, text


def extract_us_preamble(body: str) -> str:
    """Text before the first ## section (As / I want / so that + optional H1)."""
    content = body
    if content.lstrip().startswith("---"):
        _, content, _ = read_markdown_text(content)
    match = re.search(r"^## ", content, re.MULTILINE)
    if not match:
        return content.strip()
    return content[: match.start()].strip()


def extract_us_sections(body: str) -> dict[str, str | None]:
    intent = extract_section_body(body, "Intent") or ""
    plan = extract_section_body(body, "Plan") or ""
    record = extract_section_body(body, "Record") or ""
    boundaries = extract_section_body(body, "Boundaries") or ""
    return {
        "intent_acceptance": extract_subsection_body(intent, "Acceptance"),
        "intent_why": extract_subsection_body(intent, "Why"),
        "intent_where": extract_subsection_body(intent, "Where"),
        "plan_approach": extract_subsection_body(plan, "Approach"),
        "plan_architecture_refs": extract_subsection_body(plan, "Architecture refs"),
        "plan_api_db": extract_subsection_body(plan, "API / DB impact"),
        "plan_security": extract_subsection_body(plan, "Security notes"),
        "plan_decisions": extract_subsection_body(plan, "Related decisions"),
        "plan_planned": extract_subsection_body(plan, "Planned"),
        "record_files": extract_subsection_body(record, "Files"),
        "record_backend": extract_subsection_body(record, "Backend"),
        "record_frontend": extract_subsection_body(record, "Frontend"),
        "record_scripts": extract_subsection_body(record, "Scripts / Docs"),
        "record_executed": extract_subsection_body(record, "Executed"),
        "boundaries_out_of_scope": extract_subsection_body(
            boundaries, "Out of scope for this story"
        ),
        "boundaries_notes": extract_subsection_body(boundaries, "Notes"),
    }


def extract_epic_sections(body: str) -> dict[str, str | None]:
    return {
        "capability": extract_section_body(body, "Capability"),
        "expected_outcome": extract_section_body(body, "Expected outcome"),
        "out_of_scope": extract_section_body(body, "Out of scope for this epic"),
        "notes": extract_section_body(body, "Notes"),
    }


def extract_version_sections(body: str) -> dict[str, str | None]:
    return {
        "objective": extract_section_body(body, "Objective")
        or extract_section_body(body, "Goal"),
        "done_criteria": extract_section_body(body, "Done criteria"),
        "included": extract_section_body(body, "Included in this version"),
        "explicitly_out": extract_section_body(body, "Explicitly out"),
        "go_live": extract_section_body(body, "Go-live checklist"),
    }


def extract_sprint_sections(body: str) -> dict[str, str | None]:
    return {
        "goal_body": extract_section_body(body, "Goal"),
        "scope_table": extract_section_body(body, "Scope"),
        "out_of_scope": extract_section_body(body, "Out of scope for this sprint"),
        "retrospective": extract_section_body(body, "Retrospective"),
    }


def format_delivery_frontmatter(frontmatter: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        if value is None:
            continue
        text = str(value).strip()
        if not text and key == "sprint":
            continue
        if not text:
            lines.append(f"{key}:")
            continue
        if any(ch in text for ch in ' "\n') or text.startswith("["):
            escaped = text.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
        else:
            lines.append(f"{key}: {text}")
    lines.append("---")
    return "\n".join(lines)


def replace_h2_section(body: str, heading: str, new_inner: str) -> str:
    """Replace one ## section body; ``new_inner`` is content under the H2 (may include ###)."""
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(body)
    inner = new_inner.strip()
    if not inner:
        return body
    if not match:
        return body.rstrip() + f"\n\n## {heading}\n\n{inner}\n"
    start = match.end()
    rest = body[start:]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    before = body[: match.start()].rstrip()
    after = body[end:].lstrip() if next_heading else ""
    mid = f"## {heading}\n\n{inner}"
    if after:
        return f"{before}\n\n{mid}\n\n{after}"
    return f"{before}\n\n{mid}\n"


def replace_h3_in_section(section: str, heading: str, new_inner: str) -> str:
    """Replace one ### subsection inside an H2 section body."""
    pattern = re.compile(rf"^### {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(section)
    inner = new_inner.strip()
    if not inner:
        return section
    if not match:
        return section.rstrip() + f"\n\n### {heading}\n\n{inner}\n"
    start = match.end()
    rest = section[start:]
    next_heading = re.search(r"^### ", rest, re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(section)
    before = section[: match.start()].rstrip()
    after = section[end:].lstrip() if next_heading else ""
    mid = f"### {heading}\n\n{inner}"
    if after:
        return f"{before}\n\n{mid}\n\n{after}"
    return f"{before}\n\n{mid}\n"


def patch_us_record_markdown(existing_text: str, patch_text: str) -> str:
    """Merge close patch into existing US markdown — Record + optional Acceptance + frontmatter."""
    existing_fm, existing_body, _ = read_markdown_text(existing_text)
    patch_fm, patch_body, _ = read_markdown_text(patch_text)

    merged_fm = dict(existing_fm)
    for key, value in patch_fm.items():
        merged_fm[key] = value

    body = existing_body

    record_patch = extract_section_body(patch_body, "Record")
    if record_patch is not None:
        body = replace_h2_section(body, "Record", record_patch)
    elif patch_body.strip() and extract_section_body(patch_body, "Intent") is None:
        if re.search(
            r"^### (Files|Backend|Frontend|Scripts / Docs|Executed)\s*$",
            patch_body,
            re.MULTILINE,
        ):
            body = replace_h2_section(body, "Record", patch_body.strip())

    intent_patch = extract_section_body(patch_body, "Intent")
    if intent_patch is not None:
        acceptance = extract_subsection_body(intent_patch, "Acceptance")
        if acceptance is not None:
            intent_section = extract_section_body(body, "Intent")
            if intent_section:
                new_intent = replace_h3_in_section(intent_section, "Acceptance", acceptance)
                body = replace_h2_section(body, "Intent", new_intent)

    return f"{format_delivery_frontmatter(merged_fm)}\n\n{body.lstrip()}\n"


def merge_us_sprint_into_markdown(body_markdown: str, sprint_id: str | None) -> str:
    """Inject sprint_id from SQLite into US export frontmatter (display-only; body unchanged)."""
    fm, body, _ = read_markdown_text(body_markdown)
    if not fm and not sprint_id:
        return body_markdown
    if sprint_id:
        fm["sprint"] = sprint_id
    else:
        fm.pop("sprint", None)
    return f"{format_delivery_frontmatter(fm)}\n{body.lstrip()}"
