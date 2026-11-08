#!/usr/bin/env python3
"""Kit v3: canonical domain skills in .agent/skills/; agent references/ → symlinks."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / ".agent"
AGENTS = AGENT / "agents"
SKILLS = AGENT / "skills"
WORKFLOWS = AGENT / "workflows"

AGENT_SKILL_OWNERSHIP: dict[str, tuple[str, ...]] = {
    "code-investigator": ("investigate-codebase",),
    "backlog-surveyor": ("backlog-reconcile", "us-create", "investigate-codebase"),
    "flow-specialist": ("map-interaction-flow", "investigate-codebase"),
    "data-engineer": ("data-engineering",),
    "design-system-owner": (
        "accessibility",
        "design-flow",
        "design-system",
        "design-theme",
        "i18n-localization",
    ),
    "developer": ("us-implement",),
    "deus-ex": ("deus-dispatch",),
    "devops-engineer": ("release-ops",),
    "product-owner": ("epic-create",),
    "quality-owner": ("performance-budget", "test-review", "test-strategy"),
    "scrum-master": ("project-status",),
    "security-champion": (
        "payment-integration",
        "security-code",
        "security-doc",
        "security-privacy",
        "security-supply-chain",
    ),
    "sprint-planner": (
        "epic-complete",
        "sprint-complete",
        "sprint-create",
        "version-create",
    ),
    "story-checker": ("us-complete", "us-review"),
    "story-maker": ("us-create", "us-refine"),
    "technical-architect": (
        "api-contract",
        "architecture-doc",
        "generate-architecture-diagram",
        "mcp-integration",
    ),
    "technical-writer": (
        "audit-phase-docs",
        "document-existing-project",
        "geo-optimization",
        "seo-strategy",
    ),
    "ux-researcher": ("ux-research",),
}

AGENT_EXTRA_SHARED: dict[str, tuple[str, ...]] = {
    "product-owner": ("discover-product", "init-project"),
    "ux-researcher": ("discover-product",),
    "scrum-master": ("init-project",),
    "technical-writer": ("init-project",),
}

# workflow stem → (agent slug, primary skill(s))
WORKFLOW_ROUTES: dict[str, tuple[str, str | tuple[str, ...]]] = {
    "agents-help": ("scrum-master", "meridian-routing"),
    "architecture": ("technical-architect", ("architecture-doc", "generate-architecture-diagram", "mcp-integration")),
    "a11y-pass": ("design-system-owner", "accessibility"),
    "api-pass": ("technical-architect", "api-contract"),
    "audit-docs": ("technical-writer", "audit-phase-docs"),
    "complete-epic": ("sprint-planner", "epic-complete"),
    "complete-sprint": ("sprint-planner", "sprint-complete"),
    "complete-us": ("story-checker", "us-complete"),
    "create-epic": ("product-owner", "epic-create"),
    "create-us": ("story-maker", "us-create"),
    "create-version": ("sprint-planner", "version-create"),
    "daily-with-ai": ("scrum-master", "init-project"),
    "database-pass": ("data-engineer", "data-engineering"),
    "dependency-audit": ("security-champion", "security-supply-chain"),
    "design-flow": ("design-system-owner", "design-flow"),
    "design-pass": ("design-system-owner", "design-system"),
    "design-review": ("design-system-owner", "design-system"),
    "design-showcase": ("design-system-owner", "design-system"),
    "design-theme": ("design-system-owner", "design-theme"),
    "deus-ex": ("deus-ex", "deus-dispatch"),
    "discover": ("product-owner", "discover-product"),
    "document-project": ("technical-writer", "document-existing-project"),
    "i18n-pass": ("design-system-owner", "i18n-localization"),
    "implement-us": ("developer", "us-implement"),
    "init-meridian": ("scrum-master", "init-project"),
    "investigate": ("code-investigator", "investigate-codebase"),
    "survey-backlog": ("backlog-surveyor", "backlog-reconcile"),
    "map-flow": ("flow-specialist", "map-interaction-flow"),
    "migrate-delivery": ("scrum-master", "meridian-routing"),
    "payment-pass": ("security-champion", "payment-integration"),
    "perf-pass": ("quality-owner", "performance-budget"),
    "plan-sprint": ("sprint-planner", ("version-create", "sprint-create")),
    "privacy-pass": ("security-champion", "security-privacy"),
    "refine-us": ("story-maker", "us-refine"),
    "release-pass": ("devops-engineer", "release-ops"),
    "review-us": ("story-checker", "us-review"),
    "security-pass": ("security-champion", "security-doc"),
    "security-review": ("security-champion", "security-code"),
    "seo-pass": ("technical-writer", "seo-strategy"),
    "status": ("scrum-master", "project-status"),
    "test-pass": ("quality-owner", "test-strategy"),
    "test-review": ("quality-owner", "test-review"),
    "update-decisions-log": ("scrum-master", "update-decisions-log"),
    "ux-pass": ("ux-researcher", "ux-research"),
}


def discover_procedure_dirs() -> dict[str, Path]:
    """pass name → first real directory under agents/*/references/."""
    found: dict[str, Path] = {}
    for station in sorted(AGENTS.iterdir()):
        if not station.is_dir():
            continue
        refs = station / "references"
        if not refs.is_dir():
            continue
        for entry in sorted(refs.iterdir()):
            if not entry.is_dir() or entry.is_symlink():
                continue
            proc = entry / "PROCEDURE.md"
            if proc.is_file():
                found.setdefault(entry.name, entry)
    return found


def promote_to_skill(pass_dir: Path, pass_name: str) -> Path:
    target = SKILLS / pass_name
    if target.exists():
        if target.is_symlink():
            target.unlink()
        elif not (target / "SKILL.md").is_file() and not (target / "PROCEDURE.md").is_file():
            shutil.rmtree(target)
        else:
            return target
    shutil.move(str(pass_dir), str(target))
    proc = target / "PROCEDURE.md"
    skill = target / "SKILL.md"
    if proc.is_file() and not skill.exists():
        proc.rename(skill)
    elif skill.is_file() and not proc.exists():
        proc.symlink_to("SKILL.md")
    elif skill.is_file() and proc.is_file() and proc.read_text() != skill.read_text():
        proc.unlink()
        proc.symlink_to("SKILL.md")
    elif skill.is_file() and not proc.exists():
        proc.symlink_to("SKILL.md")
    return target


def link_agent_reference(station: Path, pass_name: str, skill_dir: Path) -> None:
    refs = station / "references"
    refs.mkdir(parents=True, exist_ok=True)
    link = refs / pass_name
    rel = Path("../../../skills") / pass_name
    if link.is_symlink():
        link.unlink()
    elif link.is_dir():
        shutil.rmtree(link)
    elif link.exists():
        link.unlink()
    link.symlink_to(rel, target_is_directory=True)


def station_skills(slug: str) -> list[str]:
    domain = list(AGENT_SKILL_OWNERSHIP.get(slug, ()))
    extra = list(AGENT_EXTRA_SHARED.get(slug, ()))
    combined = list(dict.fromkeys([*domain, *extra, *SHARED_SKILLS]))
    return combined


def update_agent_frontmatter(slug: str) -> None:
    path = AGENTS / slug / "agent.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    skills = ", ".join(station_skills(slug))
    if re.search(r"^skills:\s*.+$", text, re.M):
        text = re.sub(r"^skills:\s*.+$", f"skills: {skills}", text, count=1, flags=re.M)
    else:
        text = text.replace("---\n", f"---\nskills: {skills}\n", 1)
    text = re.sub(
        r"> Self-contained procedures under.*?never a separate domain skill\.",
        (
            f"> Domain skills: `.agent/skills/` — loaded by this station (symlinked under `references/`). "
            f"Invoke **`@{slug}`** in chat; slash commands are optional aliases."
        ),
        text,
        flags=re.S,
    )
    text = re.sub(
        r"## Station references\n\n.*?(?=\n## |\n---|\Z)",
        skills_section(slug),
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8")


def skills_section(slug: str) -> str:
    lines = ["## Skills\n"]
    for name in AGENT_SKILL_OWNERSHIP.get(slug, ()):
        lines.append(f"- `{name}/` → `.agent/skills/{name}/SKILL.md`")
    for s in AGENT_EXTRA_SHARED.get(slug, ()):
        lines.append(f"- `{s}/` → `.agent/skills/{s}/SKILL.md` (shared)")
    for s in SHARED_SKILLS:
        lines.append(f"- `{s}/` → `.agent/skills/{s}/SKILL.md` (shared)")
    lines.append("")
    return "\n".join(lines)


def create_architecture_doc_skill() -> None:
    target = SKILLS / "architecture-doc"
    target.mkdir(parents=True, exist_ok=True)
    skill = target / "SKILL.md"
    if skill.is_file():
        return
    wf = WORKFLOWS / "architecture.md"
    body = wf.read_text(encoding="utf-8") if wf.is_file() else ""
    task_m = re.search(r"## Task\n\n```txt\n(.*?)```", body, re.S)
    modes_m = re.search(r"## Modes.*?\n\n(\|.*?\n\n)", body, re.S)
    task = task_m.group(1).strip() if task_m else ""
    modes = modes_m.group(1).strip() if modes_m else ""
    content = f"""---
name: architecture-doc
description: Create or review docs/05_architecture.md and detail files. Use with @technical-architect or /architecture.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Architecture document pass

> Owner station: `technical-architect`. Consult `security-champion` for auth/data boundaries — do not run as owner.

## Modes (`$ARGUMENTS`)

{modes or "| _(empty)_ | **full** | Standard pass on `05` + detail files + diagrams |"}

## Procedure

```txt
{task or "- [ ] technical-architect Phase 0 gate\\n- [ ] Read 00–04 before editing 05"}
```

## Output

```txt
05_architecture status:
Detail files (if any):
Architecture diagrams:
Ready for review: yes | no
```
"""
    skill.write_text(content, encoding="utf-8")
    (target / "PROCEDURE.md").symlink_to("SKILL.md")


def create_project_status_skill() -> None:
    target = SKILLS / "project-status"
    target.mkdir(parents=True, exist_ok=True)
    skill = target / "SKILL.md"
    if skill.is_file():
        return
    wf = WORKFLOWS / "status.md"
    body = wf.read_text(encoding="utf-8") if wf.is_file() else ""
    task_m = re.search(r"## Task\n\n```txt\n(.*?)```", body, re.S)
    output_m = re.search(r"## Output\n\n```txt\n(.*?)```", body, re.S)
    task = task_m.group(1).strip() if task_m else ""
    output = output_m.group(1).strip() if output_m else ""
    content = f"""---
name: project-status
description: Read-only Meridian project health report. Use with @scrum-master or /status.
allowed-tools: Read, Glob, Grep, Bash
---

# Project status (read-only)

> Do not change docs unless `$ARGUMENTS` explicitly requests an edit.

## Procedure

```txt
{task}
```

## Output

```txt
{output}
```
"""
    skill.write_text(content, encoding="utf-8")
    (target / "PROCEDURE.md").symlink_to("SKILL.md")


SHARED_SKILLS = (
    "meridian-routing",
    "update-decisions-log",
)


def relink_agent_references() -> None:
    for slug, names in AGENT_SKILL_OWNERSHIP.items():
        station = AGENTS / slug
        if not station.is_dir():
            continue
        for name in names:
            if (SKILLS / name).is_dir():
                link_agent_reference(station, name, SKILLS / name)


def format_skills(skills: str | tuple[str, ...]) -> str:
    if isinstance(skills, str):
        return f"`{skills}`"
    return ", ".join(f"`{s}`" for s in skills)


def alias_workflow(stem: str, agent: str, skills: str | tuple[str, ...]) -> str:
    wf_path = WORKFLOWS / f"{stem}.md"
    if not wf_path.is_file():
        return ""
    fm_m = re.match(r"^---\n(.*?)\n---", wf_path.read_text(encoding="utf-8"), re.S)
    fm = fm_m.group(1).strip() if fm_m else f"description: /{stem}"
    title = stem.replace("-", " ")
    skill_text = format_skills(skills)
    if isinstance(skills, tuple) and len(skills) > 1:
        load = (
            f"Load the skill that matches `$ARGUMENTS` among {skill_text}, "
            f"or follow `agent.md` when the request spans planning."
        )
    else:
        primary = skills if isinstance(skills, str) else skills[0]
        load = f"Load skill {skill_text} and execute with `$ARGUMENTS`."
    return f"""---
{fm}
---

# /{stem} — {title}

$ARGUMENTS

---

**Invoke:** @{agent} — {load}

Slash is an optional alias. Same work: **`@{agent}`** + your request in chat.

---
"""


def migrate_references() -> list[str]:
    moved: list[str] = []
    procedures = discover_procedure_dirs()
    for pass_name, pass_dir in procedures.items():
        promote_to_skill(pass_dir, pass_name)
        moved.append(pass_name)
    for station in AGENTS.iterdir():
        if not station.is_dir():
            continue
        refs = station / "references"
        if not refs.is_dir():
            continue
        for entry in list(refs.iterdir()):
            if entry.name in procedures or (SKILLS / entry.name).is_dir():
                link_agent_reference(station, entry.name, SKILLS / entry.name)
    return moved


def main() -> None:
    moved = migrate_references()
    create_architecture_doc_skill()
    create_project_status_skill()
    relink_agent_references()
    for slug in sorted(p.name for p in AGENTS.iterdir() if p.is_dir() and (p / "agent.md").is_file()):
        update_agent_frontmatter(slug)
    for stem, (agent, skills) in sorted(WORKFLOW_ROUTES.items()):
        body = alias_workflow(stem, agent, skills)
        if body:
            (WORKFLOWS / f"{stem}.md").write_text(body, encoding="utf-8")
    print(f"Promoted {len(moved)} domain skill(s) to .agent/skills/")
    print(f"Aliased {len(WORKFLOW_ROUTES)} workflow(s)")


if __name__ == "__main__":
    main()
