#!/usr/bin/env python3
"""Migrate user stories from flat H2 sections to schema v2 (Intent / Plan / Record / Boundaries)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".agent" / "scripts"))

from meridian_section_contracts import (  # noqa: E402
    extract_section_body,
    extract_subsection_body,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
H1_RE = re.compile(r"^# US-\d+ — .+\n+", re.MULTILINE)
PREAMBLE_END_RE = re.compile(r"^## ", re.MULTILINE)

CONTEXT_ALIASES = {
    "Why": ("Why", "Why this story"),
    "Where": ("Where", "Where it fits"),
    "Approach": ("Approach", "Implementation hints (preliminary)"),
    "Architecture refs": ("Architecture refs",),
    "API / DB impact": ("API / DB impact",),
    "Security notes": ("Security notes",),
    "Related decisions": ("Related decisions",),
}

TECH_LAYERS = ("Files", "Backend", "Frontend", "Scripts / Docs")
PLACEHOLDER_FILES = "_(fill on close)_"
PLACEHOLDER_LAYER = "_(fill on close or _n/a_)_"
PLACEHOLDER_EXECUTED = "_(pending until close)_"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    fm: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm, text[match.end() :]


def extract_context_subsection(context: str, canonical: str) -> str:
    for alias in CONTEXT_ALIASES.get(canonical, (canonical,)):
        body = extract_subsection_body(context, alias)
        if body is not None:
            return body.strip()
    return ""


def normalize_acceptance_lines(content: str) -> str:
    lines = [line.rstrip() for line in content.strip().splitlines()]
    normalized: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- [") or stripped.startswith("- ["):
            normalized.append(stripped)
        elif stripped.startswith("- "):
            normalized.append(f"- [ ] {stripped[2:].strip()}")
        else:
            normalized.append(f"- [ ] {stripped}")
    return "\n".join(normalized)


def default_subsection(name: str) -> str:
    if name == "Files":
        return PLACEHOLDER_FILES
    if name == "Executed":
        return PLACEHOLDER_EXECUTED
    if name in TECH_LAYERS:
        return PLACEHOLDER_LAYER
    if name in ("API / DB impact", "Security notes", "Related decisions"):
        return "- _n/a_"
    return "- _n/a_"


def extract_preamble(body: str) -> str:
    trimmed = body.lstrip("\n")
    h1_match = H1_RE.match(trimmed)
    if not h1_match:
        return ""
    rest = trimmed[h1_match.end() :]
    section_match = PREAMBLE_END_RE.search(rest)
    if not section_match:
        return trimmed[: h1_match.end()].rstrip() + "\n\n"
    return trimmed[: h1_match.end() + section_match.start()].rstrip() + "\n\n"


def build_v2_body(old_body: str) -> str:
    preamble = extract_preamble(old_body)
    body = old_body[len(preamble) :] if preamble else old_body

    if body.lstrip().startswith("## Intent"):
        return old_body if preamble else old_body

    acceptance = extract_section_body(body, "Acceptance") or ""
    context = extract_section_body(body, "Context & constraints") or ""
    tech = extract_section_body(body, "Technical implementation") or ""
    tests = extract_section_body(body, "Tests") or ""
    out_of_scope = extract_section_body(body, "Out of scope for this story") or "- _n/a_"
    notes = extract_section_body(body, "Notes") or "- _n/a_"

    why = extract_context_subsection(context, "Why")
    where = extract_context_subsection(context, "Where")
    approach = extract_context_subsection(context, "Approach")
    architecture = extract_context_subsection(context, "Architecture refs") or default_subsection(
        "Architecture refs"
    )
    api_db = extract_context_subsection(context, "API / DB impact") or default_subsection(
        "API / DB impact"
    )
    security = extract_context_subsection(context, "Security notes") or default_subsection(
        "Security notes"
    )
    decisions = extract_context_subsection(context, "Related decisions") or default_subsection(
        "Related decisions"
    )

    planned = extract_subsection_body(tests, "Planned") if tests else ""
    if not planned:
        planned = "- [ ] **manual** — add concrete steps on `/refine-us`"
    executed = extract_subsection_body(tests, "Executed") if tests else PLACEHOLDER_EXECUTED
    if executed is None:
        executed = PLACEHOLDER_EXECUTED

    record_layers: dict[str, str] = {}
    for layer in TECH_LAYERS:
        layer_body = extract_subsection_body(tech, layer) if tech else None
        record_layers[layer] = (layer_body or default_subsection(layer)).strip()

    if tech and not any(record_layers[layer] != default_subsection(layer) for layer in TECH_LAYERS):
        frontend_only = extract_subsection_body(tech, "Frontend")
        if frontend_only:
            record_layers["Frontend"] = frontend_only.strip()
        elif tech.strip() and not tech.strip().startswith("###"):
            record_layers["Frontend"] = tech.strip()

    intent_parts = [
        "## Intent",
        "",
        "### Acceptance",
        "",
        normalize_acceptance_lines(acceptance) or "- [ ] _(fill acceptance criteria)_",
        "",
        "### Why",
        "",
        why or "_(fill on `/create-us`)_",
        "",
        "### Where",
        "",
        where or "_(fill on `/create-us`)_",
        "",
    ]

    plan_parts = ["## Plan", ""]
    if approach:
        plan_parts.extend(["### Approach", "", approach, ""])
    plan_parts.extend(
        [
            "### Architecture refs",
            "",
            architecture,
            "",
            "### API / DB impact",
            "",
            api_db,
            "",
            "### Security notes",
            "",
            security,
            "",
            "### Related decisions",
            "",
            decisions,
            "",
            "### Planned",
            "",
            planned.strip(),
            "",
        ]
    )

    record_parts = ["## Record", ""]
    for layer in TECH_LAYERS:
        record_parts.extend([f"### {layer}", "", record_layers[layer], ""])
    record_parts.extend(["### Executed", "", executed.strip(), ""])

    boundaries_parts = [
        "## Boundaries",
        "",
        "### Out of scope for this story",
        "",
        out_of_scope.strip(),
        "",
        "### Notes",
        "",
        notes.strip(),
        "",
    ]

    return preamble + "\n".join(intent_parts + plan_parts + record_parts + boundaries_parts).rstrip() + "\n"


def restore_preamble_from_git(path: Path, dry_run: bool) -> bool:
    import subprocess

    rel = path.relative_to(REPO_ROOT)
    try:
        old_text = subprocess.check_output(
            ["git", "show", f"HEAD:{rel}"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError:
        return False

    _, old_body = parse_frontmatter(old_text)
    preamble = extract_preamble(old_body)
    if not preamble:
        return False

    current = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(current)
    if preamble.strip() and body.lstrip().startswith("# US-"):
        return False

    intent_idx = body.find("## Intent")
    if intent_idx == -1:
        return False

    new_body = preamble + body[intent_idx:]
    fm_lines = ["---"]
    for key, value in frontmatter.items():
        fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")
    fm_lines.append("")

    output = "\n".join(fm_lines) + new_body
    if dry_run:
        print(f"would restore preamble {path.name}")
    else:
        path.write_text(output, encoding="utf-8")
        print(f"restored preamble {path.name}")
    return True


def migrate_file(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    new_body = build_v2_body(body)
    if new_body == body:
        return False

    if "ready" not in frontmatter:
        status = frontmatter.get("status", "❌")
        frontmatter["ready"] = "true" if status in ("✅", "🔶") else "false"

    fm_lines = ["---"]
    for key, value in frontmatter.items():
        fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")
    fm_lines.append("")

    output = "\n".join(fm_lines) + new_body
    if dry_run:
        print(f"would migrate {path.name}")
    else:
        path.write_text(output, encoding="utf-8")
        print(f"migrated {path.name}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Project folder (Meridian package root; default: .)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--restore-preamble",
        action="store_true",
        help="Restore H1 and user story lines from git HEAD",
    )
    args = parser.parse_args()

    us_dir = REPO_ROOT / args.project / "docs" / "us"
    if not us_dir.is_dir():
        print(f"Missing {us_dir}", file=sys.stderr)
        return 1

    count = 0
    for path in sorted(us_dir.glob("US-*.md")):
        if args.restore_preamble:
            if restore_preamble_from_git(path, args.dry_run):
                count += 1
        elif migrate_file(path, args.dry_run):
            count += 1

    action = "would process" if args.dry_run else "processed"
    if args.restore_preamble:
        action = "would restore" if args.dry_run else "restored"
    print(f"{action} {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
