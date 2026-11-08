#!/usr/bin/env python3
"""Meridian workspace diagnostics — defensive health checks before delivery work.

Unlike generic AI harness installers, Meridian doctor validates gates-ready
structure: kit, adapters, phase docs, delivery SQLite, and first-value steps.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from validate_kit_parity import check_parity  # noqa: E402


def _read_frontmatter_approved(path: Path) -> bool | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    for line in block.splitlines():
        if line.strip().lower().startswith("approved:"):
            val = line.split(":", 1)[1].strip().lower()
            return val in ("true", "yes", "1")
    return None


def run_doctor(project_root: Path, *, skip_parity: bool = False) -> tuple[list[str], list[str], list[str]]:
    """Return (ok_lines, warnings, errors)."""
    ok: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []

    root = project_root.resolve()
    agent = root / ".agent"
    docs = root / "docs"
    meridian = root / ".meridian"
    db_path = meridian / "meridian.db"

    if sys.version_info < (3, 10):
        warnings.append(f"Python {sys.version_info.major}.{sys.version_info.minor} — 3.10+ recommended.")

    if not agent.is_dir():
        errors.append("Missing .agent/ — Meridian: Install Harness (extension) or copy the kit.")
    else:
        ok.append(".agent/ present")
        if not (agent / "MERIDIAN.md").exists():
            errors.append(".agent/MERIDIAN.md missing — kit looks incomplete.")
        version_file = agent / "VERSION"
        if version_file.exists():
            ok.append(f"Harness version: {version_file.read_text(encoding='utf-8').strip()}")
        else:
            warnings.append(".agent/VERSION missing — install predates version stamps; consider Upgrade Harness.")

    if not docs.is_dir():
        warnings.append("Missing docs/ — run /init-meridian or /document-project in chat.")
    else:
        ok.append("docs/ present")
        scope = docs / "00_scope.md"
        arch = docs / "05_architecture.md"
        if not scope.exists():
            warnings.append("Missing docs/00_scope.md — Phase 1 not started.")
        arch_approved = _read_frontmatter_approved(arch)
        if arch_approved is True:
            ok.append("05_architecture.md approved — US creation gate open")
        elif arch_approved is False:
            warnings.append("05_architecture.md not approved — do not create user stories yet.")
        elif arch.exists():
            warnings.append("05_architecture.md has no approved: frontmatter.")

    if db_path.exists():
        ok.append(f"Delivery DB: {db_path.relative_to(root)}")
        try:
            conn = sqlite3.connect(db_path)
            try:
                row = conn.execute("SELECT COUNT(*) FROM user_stories").fetchone()
                if row:
                    ok.append(f"User stories in SQLite: {row[0]}")
            finally:
                conn.close()
        except sqlite3.Error as exc:
            warnings.append(f"meridian.db unreadable: {exc}")
    else:
        warnings.append("Missing .meridian/meridian.db — run /init-meridian or bootstrap after docs/ exists.")

    if not skip_parity:
        parity_errors, parity_warnings = check_parity(root)
        errors.extend(parity_errors)
        warnings.extend(parity_warnings)

    # First-value checklist (binary onboarding target)
    first_value = {
        "kit": agent.is_dir() and (agent / "MERIDIAN.md").exists(),
        "docs": docs.is_dir() and (docs / "00_scope.md").exists(),
        "delivery": db_path.exists(),
        "adapters": (root / ".cursor" / "commands").is_dir(),
    }
    done = sum(1 for v in first_value.values() if v)
    ok.append(f"First-value checklist: {done}/4 ({', '.join(k for k, v in first_value.items() if v) or 'none yet'})")
    if done == 4:
        ok.append("First-value ready — open Board and run /status in chat.")

    return ok, warnings, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Meridian workspace doctor")
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    parser.add_argument("--skip-parity", action="store_true", help="Skip IDE adapter parity checks")
    parser.add_argument("--json", action="store_true", help="Machine-readable summary (minimal)")
    args = parser.parse_args()
    root = Path(args.project).resolve()

    ok_lines, warnings, errors = run_doctor(root, skip_parity=args.skip_parity)

    if args.json:
        import json

        print(
            json.dumps(
                {"ok": ok_lines, "warnings": warnings, "errors": errors, "healthy": not errors},
                indent=2,
            )
        )
    else:
        print("Meridian doctor\n")
        for line in ok_lines:
            print(f"  OK   {line}")
        for line in warnings:
            print(f"  WARN {line}")
        for line in errors:
            print(f"  FAIL {line}")
        print()
        if errors:
            print("Result: unhealthy — fix FAIL items before delivery work.")
        elif warnings:
            print(f"Result: OK with {len(warnings)} warning(s).")
        else:
            print("Result: healthy.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
