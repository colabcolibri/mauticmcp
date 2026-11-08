"""Section contracts for Meridian delivery artifacts (US, epic, version).

Canonical definitions mirror `.agent/references/templates/section-contracts.md`
and `app-visual-studio/src/domain/meridian/section-contracts.ts`.
"""

from __future__ import annotations

import re
from typing import Literal

Severity = Literal["error", "warning"]

US_H2_SECTIONS: tuple[str, ...] = ("Intent", "Plan", "Record", "Boundaries")

US_INTENT_H3: tuple[str, ...] = ("Acceptance", "Why", "Where")

US_PLAN_H3: tuple[str, ...] = (
    "Architecture refs",
    "API / DB impact",
    "Security notes",
    "Related decisions",
    "Planned",
)

US_RECORD_H3: tuple[str, ...] = (
    "Files",
    "Backend",
    "Frontend",
    "Scripts / Docs",
    "Executed",
)

US_BOUNDARIES_H3: tuple[str, ...] = ("Out of scope for this story", "Notes")

US_FRONTMATTER_REQUIRED: tuple[str, ...] = (
    "id",
    "title",
    "epic",
    "version",
    "status",
    "moscow",
    "done_when",
    "tests",
    "tests_status",
)

US_FRONTMATTER_STRICT: tuple[str, ...] = (*US_FRONTMATTER_REQUIRED, "ready", "depends_on")

EPIC_H2_SECTIONS: tuple[str, ...] = (
    "Capability",
    "Expected outcome",
    "Out of scope for this epic",
)

EPIC_H2_ALIASES: dict[str, tuple[str, ...]] = {
    "Out of scope for this epic": ("Out of scope for this epic", "Out of this epic"),
}

VERSION_H2_PREFIXES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Objective", ("Objective", "Goal")),
    ("Done criteria", ("Done criteria",)),
    ("Included in this version", ("Included in this version",)),
    ("Explicitly out", ("Explicitly out",)),
    ("Go-live checklist", ("Go-live checklist",)),
)


def list_h2_sections(body: str) -> list[str]:
    return re.findall(r"^## (.+)$", body, re.MULTILINE)


def list_h3_in_section(body: str, h2_heading: str) -> list[str]:
    section = extract_section_body(body, h2_heading)
    if section is None:
        return []
    return re.findall(r"^### (.+)$", section, re.MULTILINE)


def extract_section_body(text: str, heading: str) -> str | None:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    start = match.end()
    rest = text[start:]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def extract_subsection_body(section: str, heading: str) -> str | None:
    pattern = re.compile(rf"^### {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(section)
    if not match:
        return None
    start = match.end()
    rest = section[start:]
    next_heading = re.search(r"^### ", rest, re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(section)
    return section[start:end].strip()


def validate_us_structure(
    story_name: str,
    body: str,
    frontmatter: dict[str, str],
    errors: list[str],
    warnings: list[str],
) -> None:
    status = frontmatter.get("status")
    strict = "ready" in frontmatter
    h2_present = list_h2_sections(body)

    for field in US_FRONTMATTER_STRICT if strict else US_FRONTMATTER_REQUIRED:
        if field == "depends_on":
            present = field in frontmatter
        else:
            present = field in frontmatter and frontmatter.get(field, "") != ""
        if not present:
            severity: Severity = "error" if strict or field in US_FRONTMATTER_REQUIRED else "warning"
            message = f"{story_name}: missing frontmatter `{field}`."
            if severity == "error":
                errors.append(message)
            else:
                warnings.append(message)

    for section in US_H2_SECTIONS:
        if section not in h2_present:
            errors.append(f"{story_name}: missing required ## {section} (see us-template.md).")

    if strict:
        for subsection in US_INTENT_H3:
            if subsection not in list_h3_in_section(body, "Intent"):
                errors.append(f"{story_name}: missing ### {subsection} under ## Intent.")

        plan_h3 = [
            name.replace(" (optional)", "").strip()
            for name in list_h3_in_section(body, "Plan")
        ]
        for subsection in US_PLAN_H3:
            if subsection not in plan_h3:
                errors.append(f"{story_name}: missing ### {subsection} under ## Plan.")

        for subsection in US_RECORD_H3:
            if subsection not in list_h3_in_section(body, "Record"):
                errors.append(f"{story_name}: missing ### {subsection} under ## Record.")

        for subsection in US_BOUNDARIES_H3:
            if subsection not in list_h3_in_section(body, "Boundaries"):
                errors.append(f"{story_name}: missing ### {subsection} under ## Boundaries.")
    else:
        for subsection in US_BOUNDARIES_H3:
            if subsection not in list_h3_in_section(body, "Boundaries"):
                warnings.append(
                    f"{story_name}: missing ### {subsection} under ## Boundaries (recommended)."
                )

    if status == "✅" and "Record" not in h2_present:
        errors.append(f"{story_name}: status ✅ requires ## Record with delivery evidence.")


def has_h2_match(present: list[str], canonical: str, aliases: tuple[str, ...] | None = None) -> bool:
    options = aliases or (canonical,)
    for option in options:
        if option in present:
            return True
        if any(heading == option or heading.startswith(f"{option} ") for heading in present):
            return True
    return False


def validate_epic_structure(
    epic_name: str,
    body: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    h2_present = list_h2_sections(body)
    for section in ("Capability", "Expected outcome"):
        if section not in h2_present:
            errors.append(f"{epic_name}: missing required ## {section} (see epic-template.md).")

    if not has_h2_match(
        h2_present,
        "Out of scope for this epic",
        EPIC_H2_ALIASES["Out of scope for this epic"],
    ):
        errors.append(
            f"{epic_name}: missing required ## Out of scope for this epic (see epic-template.md)."
        )

    if "Out of this epic" in h2_present and "Out of scope for this epic" not in h2_present:
        warnings.append(
            f"{epic_name}: use ## Out of scope for this epic (template name) instead of ## Out of this epic."
        )


def validate_version_structure(
    version_name: str,
    body: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    h2_present = list_h2_sections(body)
    for canonical, aliases in VERSION_H2_PREFIXES:
        if not has_h2_match(h2_present, canonical, aliases):
            errors.append(
                f"{version_name}: missing required ## {canonical} (see version-template.md)."
            )
        if canonical == "Objective" and "Goal" in h2_present and "Objective" not in h2_present:
            warnings.append(
                f"{version_name}: prefer ## Objective (template) over ## Goal."
            )
