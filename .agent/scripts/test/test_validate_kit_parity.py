#!/usr/bin/env python3
"""Tests for validate_kit_parity.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "validate_kit_parity.py"


def run_parity(project: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), str(project), *extra],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_parity_errors_when_cursor_skills_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skills = root / ".agent" / "skills" / "us-create"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text("---\nname: us-create\n---\n", encoding="utf-8")
        agents = root / ".agent" / "agents" / "developer"
        agents.mkdir(parents=True)
        (agents / "agent.md").write_text("# dev\n", encoding="utf-8")
        (root / ".cursor" / "agents").mkdir(parents=True)
        (root / ".cursor" / "agents" / "developer.md").symlink_to(
            "../../.agent/agents/developer/agent.md"
        )
        code, out = run_parity(root)
        assert code == 1
        assert "ERROR" in out


def test_parity_ok_when_cursor_matches() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skills = root / ".agent" / "skills" / "us-create"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text("---\nname: us-create\n---\n", encoding="utf-8")
        agents = root / ".agent" / "agents" / "developer"
        agents.mkdir(parents=True)
        (agents / "agent.md").write_text("# dev\n", encoding="utf-8")
        cursor_skills = root / ".cursor" / "skills" / "us-create"
        cursor_skills.mkdir(parents=True)
        (cursor_skills / "SKILL.md").symlink_to("../../../.agent/skills/us-create/SKILL.md")
        cursor_agents = root / ".cursor" / "agents"
        cursor_agents.mkdir(parents=True)
        (cursor_agents / "developer.md").symlink_to("../../.agent/agents/developer/agent.md")
        code, out = run_parity(root)
        assert code == 0
        assert "Parity OK" in out


if __name__ == "__main__":
    test_parity_errors_when_cursor_skills_missing()
    test_parity_ok_when_cursor_matches()
    print("OK: validate_kit_parity tests passed")
