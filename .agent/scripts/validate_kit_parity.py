#!/usr/bin/env python3
"""Compare .agent/ kit sources with generated IDE adapters (parity contract)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _skill_dir_names(skills_root: Path) -> set[str]:
    if not skills_root.is_dir():
        return set()
    return {
        p.name
        for p in skills_root.iterdir()
        if p.is_dir() and p.name != "doc.md" and (p / "SKILL.md").is_file()
    }


def _agent_names(agent_dir: Path) -> set[str]:
    agents_root = agent_dir / "agents"
    if not agents_root.is_dir():
        return set()
    names: set[str] = set()
    for station in agents_root.iterdir():
        if station.is_dir() and (station / "agent.md").is_file():
            names.add(f"{station.name}.md")
    return names


def check_parity(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    agent = repo_root / ".agent"
    if not agent.is_dir():
        errors.append("Missing .agent/ — install the Meridian harness first.")
        return errors, warnings

    expected_skills = _skill_dir_names(agent / "skills")
    expected_agents = _agent_names(agent)

    cursor = repo_root / ".cursor"
    if not cursor.is_dir():
        warnings.append("Missing .cursor/ — run .agent/scripts/sync_kit.sh for Cursor.")
    else:
        cursor_agents = {p.name for p in (cursor / "agents").glob("*.md")} if (cursor / "agents").is_dir() else set()
        missing_agents = expected_agents - cursor_agents
        if missing_agents:
            errors.append(
                f".cursor/agents missing {len(missing_agents)} agent(s): "
                + ", ".join(sorted(missing_agents)[:6])
                + ("…" if len(missing_agents) > 6 else "")
            )

        cursor_skills = _skill_dir_names(cursor / "skills")
        missing_skills = expected_skills - cursor_skills
        if missing_skills:
            errors.append(
                f".cursor/skills missing {len(missing_skills)} skill(s): "
                + ", ".join(sorted(missing_skills)[:8])
                + ("…" if len(missing_skills) > 8 else "")
            )
        extra_skills = cursor_skills - expected_skills - {"meridian-authoring"}
        if extra_skills:
            warnings.append(
                f".cursor/skills has unexpected dir(s): {', '.join(sorted(extra_skills)[:6])}"
            )

        commands = cursor / "commands"
        if commands.is_dir() and any(commands.iterdir()):
            warnings.append(
                ".cursor/commands/ has legacy workflow symlinks — run sync_kit.sh --no-prune is false to prune."
            )

    codex_skills = repo_root / ".agents" / "skills"
    if codex_skills.is_dir():
        present = _skill_dir_names(codex_skills)
        workflow_leftovers = {n for n in present if n.startswith("workflow-")}
        if workflow_leftovers:
            warnings.append(
                "Codex has legacy workflow-* skills — run sync_kit.sh to prune."
            )
        missing = expected_skills - present
        if missing:
            warnings.append("Codex .agents/skills out of sync — run sync_kit.sh.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate IDE adapter parity with .agent/")
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()
    root = Path(args.project).resolve()

    errors, warnings = check_parity(root)
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    if warnings:
        print(f"Parity OK with {len(warnings)} warning(s).")
    else:
        print("Parity OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
