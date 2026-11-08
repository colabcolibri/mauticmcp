#!/usr/bin/env python3
"""Tests for meridian_doctor.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "meridian_doctor.py"


def run_doctor(project: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), str(project), *extra],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_doctor_fails_without_agent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run_doctor(Path(tmp))
        assert code == 1
        assert "Missing .agent/" in out


def test_doctor_ok_minimal_kit() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        agent = root / ".agent"
        agent.mkdir()
        (agent / "MERIDIAN.md").write_text("# Meridian\n", encoding="utf-8")
        (agent / "VERSION").write_text("1.0.0\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "00_scope.md").write_text("# Scope\n", encoding="utf-8")
        code, out = run_doctor(root, "--skip-parity")
        assert code == 0
        assert "healthy" in out.lower() or "OK with" in out


if __name__ == "__main__":
    test_doctor_fails_without_agent()
    test_doctor_ok_minimal_kit()
    print("OK: meridian_doctor tests passed")
