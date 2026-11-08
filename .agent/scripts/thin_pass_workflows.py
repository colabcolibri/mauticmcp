#!/usr/bin/env python3
"""One-shot maintainer script: thin pass workflows + sync modes into PROCEDURE.md."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".agent" / "workflows"

PASS_FILES = [
    "database-pass.md",
    "ux-pass.md",
    "a11y-pass.md",
    "i18n-pass.md",
    "api-pass.md",
    "perf-pass.md",
    "seo-pass.md",
    "payment-pass.md",
    "release-pass.md",
    "design-pass.md",
    "test-pass.md",
    "security-pass.md",
    "privacy-pass.md",
    "design-flow.md",
    "design-theme.md",
    "design-showcase.md",
    "design-review.md",
    "dependency-audit.md",
    "test-review.md",
    "security-review.md",
]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1].strip(), parts[2].lstrip("\n")


def section(text: str, name: str) -> str:
    # Header line only — do not use `.*` with re.S or it consumes the whole file.
    pat = rf"^## {re.escape(name)}[^\n]*\n(.*?)(?=^## |\Z)"
    m = re.search(pat, text, re.M | re.S)
    return m.group(1).strip() if m else ""


def parse_route(line: str) -> tuple[str, str, str, str] | None:
    m = re.search(
        r"Use (@\S+(?:\s+\([^)]+\))?)\s+.*?`\.agent/agents/([^/]+)/references/([^/`]+)/`"
        r".*?`([^`]+)`",
        line,
    )
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3), m.group(4)


def filter_critical_rules(critical: str, checklist: str) -> list[str]:
    kept: list[str] = []
    for line in critical.splitlines():
        s = line.strip()
        if not s or s == "---":
            continue
        if re.match(r"^1\.\s+Use @", s):
            continue
        if re.match(r"^2\.\s+Read `", s) and checklist in s:
            continue
        if re.match(r"^2\.\s+\*\*Mandatory read:\*\*", s):
            continue
        kept.append(s)
    renumbered: list[str] = []
    n = 1
    for line in kept:
        line = re.sub(r"^\d+\.\s+", "", line)
        renumbered.append(f"{n}. {line}")
        n += 1
    return renumbered


def thin_workflow(path: Path) -> tuple[str, str | None]:
    body = path.read_text(encoding="utf-8")
    fm, rest = split_frontmatter(body)
    title_m = re.search(r"^# (.+)$", rest, re.M)
    title = f"# {title_m.group(1)}" if title_m else f"# /{path.stem}"
    critical_raw = section(rest, "Critical rules")
    first_line = next((ln for ln in critical_raw.splitlines() if ln.strip().startswith("1.")), "")
    route = parse_route(first_line)
    if not route:
        raise ValueError(f"cannot parse route in {path.name}")
    agent, slug, ref, checklist = route
    proc_path = f"`.agent/agents/{slug}/references/{ref}/PROCEDURE.md`"
    extra = filter_critical_rules(critical_raw, checklist)
    modes = section(rest, "Modes (`$ARGUMENTS`)") or section(rest, "Modes")
    output = section(rest, "Output")
    after = section(rest, "After") or section(rest, "When to run")
    task = section(rest, "Task")

    lines = [
        "---",
        fm,
        "---",
        "",
        title,
        "",
        "$ARGUMENTS",
        "",
        "---",
        "",
        "## Station",
        "",
        f"| | |",
        f"| --- | --- |",
        f"| Agent | {agent} |",
        f"| Procedure | {proc_path} |",
        f"| Checklist | `{checklist}` (same folder) |",
        "",
    ]
    if extra:
        lines.extend(["## Critical rules (this command)", ""] + extra + [""])
    if modes:
        lines.extend(["## Modes (`$ARGUMENTS`)", "", modes, ""])
    if output:
        lines.extend(["## Output", "", output, ""])
    if after:
        lines.extend(["## When to run", "", after, ""])
    lines.extend(
        [
            "---",
            "",
            "> **Procedure:** execute steps in PROCEDURE.md — do not duplicate a `## Task` block in this workflow.",
            "",
        ]
    )
    new_body = "\n".join(lines)
    return new_body, task if task else None


def sync_procedure(slug: str, ref: str, modes: str, task: str | None, path: Path) -> bool:
    proc = ROOT / ".agent" / "agents" / slug / "references" / ref / "PROCEDURE.md"
    if not proc.is_file():
        return False
    text = proc.read_text(encoding="utf-8")
    changed = False
    if modes and "## Modes" not in text:
        block = f"\n## Modes (`$ARGUMENTS`)\n\n{modes}\n"
        if "## Procedure" in text:
            text = text.replace("## Procedure", block + "\n## Procedure", 1)
        else:
            text += block
        changed = True
    if task and task not in text:
        steps = f"\n## Workflow steps (from `/{{cmd}}`)\n\n```txt\n{task}\n```\n"
        steps = steps.replace("{cmd}", path.stem)
        text += steps
        changed = True
    if changed:
        proc.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    for name in PASS_FILES:
        path = WF / name
        if not path.is_file():
            print(f"skip missing {name}")
            continue
        body, task = thin_workflow(path)
        rest = split_frontmatter(path.read_text(encoding="utf-8"))[1]
        modes = section(rest, "Modes (`$ARGUMENTS`)") or section(rest, "Modes")
        m = re.search(
            r"agents/([^/]+)/references/([^/`]+)/",
            body,
        )
        if m:
            sync_procedure(m.group(1), m.group(2), modes, task, path)
        path.write_text(body, encoding="utf-8")
        print(f"thinned {name}")


if __name__ == "__main__":
    main()
