#!/usr/bin/env python3
"""Validate basic Meridian project structure.

This script intentionally uses only the Python standard library so it can run in
fresh projects without dependency installation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from meridian_section_contracts import (  # noqa: E402
    extract_section_body,
    validate_epic_structure,
    validate_us_structure,
    validate_version_structure,
)


PHASE_DOCS = [
    "00_scope.md",
    "01_tech_stack.md",
    "02_security.md",
    "03_user_types.md",
    "04_principles.md",
    "05_architecture.md",
    "06_database.md",
    "07_api_contracts.md",
    "08_environments.md",
    "11_decisions.md",
]


AGENT_KIT_PATHS = [
    "ARCHITECTURE.md",
    "MERIDIAN.md",
    "rules/MERIDIAN.md",
    "skills/doc.md",
    "skills/meridian-routing/SKILL.md",
    "skills/init-project/SKILL.md",
    "scripts/validate_meridian.py",
]

REQUIRED_AGENT_STATIONS = [
    "deus-ex",
    "product-owner",
    "technical-writer",
    "security-champion",
    "technical-architect",
    "design-system-owner",
    "quality-owner",
    "sprint-planner",
    "story-maker",
    "story-checker",
    "developer",
    "scrum-master",
    "code-investigator",
    "backlog-surveyor",
    "flow-specialist",
    "ux-researcher",
    "data-engineer",
    "devops-engineer",
]

# kit v2 and earlier — flat persona at agents/{slug}.md
LEGACY_FLAT_AGENT_FILES = [f"{slug}.md" for slug in REQUIRED_AGENT_STATIONS]

LEGACY_AGENTS = [
    "process-manager.md",
    "scope-architect.md",
    "documentation-strategist.md",
    "security-steward.md",
    "architecture-guardian.md",
    "board-keeper.md",
    "backlog-refiner.md",
]

# Kit v3: domain skills canonical in `.agent/skills/`; agents load skills; workflows are aliases.

SHARED_SKILL_DIRS = frozenset({
    "create-meridian-artifact",
    "discover-product",
    "init-project",
    "meridian-routing",
    "update-decisions-log",
})

# Cross-station only — not owned by a single station's references/ symlink set.
DOMAIN_SKILL_DIRS_FORBIDDEN: frozenset[str] = frozenset()


def validate_cursor_adapter(repo_root: Path, warnings: list[str]) -> None:
    cursor = repo_root / ".cursor"
    if not cursor.is_dir():
        warnings.append("Missing .cursor/ — run .agent/scripts/sync_cursor_kit.sh for Cursor IDE.")
        return
    for sub in ("rules", "skills", "agents", "commands"):
        if not (cursor / sub).is_dir():
            warnings.append(f"Missing .cursor/{sub}/ — run sync_cursor_kit.sh")
    rule = cursor / "rules" / "meridian.mdc"
    if rule.exists() and "alwaysApply: true" not in rule.read_text(encoding="utf-8"):
        warnings.append(".cursor/rules/meridian.mdc should set alwaysApply: true")


def validate_codex_adapter(repo_root: Path, warnings: list[str]) -> None:
    skills = repo_root / ".agents" / "skills"
    codex = repo_root / ".codex"
    if not skills.is_dir():
        warnings.append("Missing .agents/skills/ — run .agent/scripts/sync_cursor_kit.sh for Codex.")
        return
    if not codex.is_dir():
        warnings.append("Missing .codex/ — run sync_cursor_kit.sh for Codex subagents.")
        return
    agents_dir = codex / "agents"
    if not agents_dir.is_dir():
        warnings.append("Missing .codex/agents/ — run sync_cursor_kit.sh")


def validate_agent_kit(
    repo_root: Path, errors: list[str], warnings: list[str], *, strict: bool = False
) -> None:
    agent_dir = repo_root / ".agent"
    if not agent_dir.is_dir():
        return
    for rel in AGENT_KIT_PATHS:
        if not (agent_dir / rel).exists():
            warnings.append(f"Missing .agent/{rel} in kit.")
    rules = agent_dir / "rules" / "MERIDIAN.md"
    if rules.exists() and "trigger: always_on" not in rules.read_text(encoding="utf-8"):
        warnings.append(".agent/rules/MERIDIAN.md missing trigger: always_on")
    agents_dir = agent_dir / "agents"
    if agents_dir.is_dir():
        for slug in REQUIRED_AGENT_STATIONS:
            agent_md = agents_dir / slug / "agent.md"
            if not agent_md.is_file():
                warnings.append(f"Missing .agent/agents/{slug}/agent.md")
        for legacy_flat in LEGACY_FLAT_AGENT_FILES:
            legacy_path = agents_dir / legacy_flat
            if legacy_path.is_file():
                msg = (
                    f"Legacy flat agent file: .agent/agents/{legacy_flat} "
                    f"— use .agent/agents/{legacy_flat.removesuffix('.md')}/agent.md (kit v2)"
                )
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)
        for legacy in LEGACY_AGENTS:
            legacy_path = agents_dir / legacy
            if legacy_path.exists():
                msg = f"Legacy agent file still present: .agent/agents/{legacy}"
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)
    skills_dir = agent_dir / "skills"
    if skills_dir.is_dir():
        for required in SHARED_SKILL_DIRS:
            if not (skills_dir / required / "SKILL.md").is_file():
                warnings.append(f"Missing shared skill `.agent/skills/{required}/SKILL.md`")
        for entry in sorted(skills_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            if entry.name == "doc.md":
                continue
            if not (entry / "SKILL.md").is_file():
                warnings.append(f"Skill folder `.agent/skills/{entry.name}/` missing SKILL.md")


CONTEXT_PLACEHOLDER_MARKERS = (
    "_(fill in",
    "_(pending)_",
    "§ [section name",
    "§ …",
    "path/to/…",
    "add when implementation scope is known",
)

TESTS_GENERIC_MARKERS = (
    "add when implementation scope is known",
    "verify acceptance criteria end-to-end",
)


def read_markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    return text[end + 4 :].lstrip("\n")


def is_mostly_placeholder(section: str, markers: tuple[str, ...] = CONTEXT_PLACEHOLDER_MARKERS) -> bool:
    lowered = section.lower()
    substantive = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
        and not line.strip().startswith("#")
        and not line.strip().startswith(">")
        and line.strip() not in ("- _n/a_", "_n/a_")
    ]
    if not substantive:
        return True
    hits = sum(1 for marker in markers if marker.lower() in lowered)
    return hits >= max(1, len(substantive) // 2)


def validate_us_semantics(
    story_name: str,
    status: str | None,
    frontmatter: dict[str, str],
    story_text: str,
    errors: list[str],
    warnings: list[str],
    legacy_missing_context: list[str],
) -> None:
    if status == "✅":
        record = extract_section_body(story_text, "Record")
        if record and is_mostly_placeholder(record):
            warnings.append(
                f"{story_name}: status ✅ but ## Record looks like a placeholder."
            )
        return

    if status in ("🧊", "🚫"):
        return

    if status not in ("❌", "🔶"):
        return

    ready = frontmatter.get("ready", "").lower()
    has_ready_field = "ready" in frontmatter
    plan = extract_section_body(story_text, "Plan")

    if plan is None:
        if has_ready_field:
            warnings.append(
                f"{story_name}: missing ## Plan — run /refine-us before implement."
            )
        else:
            legacy_missing_context.append(story_name)
    elif is_mostly_placeholder(plan):
        warnings.append(
            f"{story_name}: ## Plan not filled — run /refine-us before implement."
        )

    if has_ready_field and ready != "true":
        errors.append(
            f"{story_name}: ready is not true — run /refine-us before /implement-us."
        )

    planned_match = re.search(
        r"^### Planned\s*$([\s\S]*?)(?=^### |\Z)",
        story_text,
        re.MULTILINE,
    )
    planned = planned_match.group(1).strip() if planned_match else None
    if planned:
        lowered = planned.lower()
        if "add when" in lowered or (
            "verify acceptance criteria end-to-end" in lowered
            and not re.search(r"^\d+\.", planned, re.MULTILINE)
        ):
            warnings.append(
                f"{story_name}: Tests/Planned still generic — run /refine-us with concrete steps."
            )


def sqlite_delivery_active(root: Path) -> bool:
    """True when delivery lives in .meridian/meridian.db (SQLite-only workflow)."""
    return (root / ".meridian" / "meridian.db").is_file()


def validate_lifecycle_hygiene(root: Path, warnings: list[str]) -> None:
    """Warn on finished-but-still-open sprints/epics/versions (US-0166)."""
    lib = _SCRIPT_DIR / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from meridian_db import connect  # noqa: WPS433
        from meridian_lifecycle import collect_hygiene_findings  # noqa: WPS433
    except ImportError:
        warnings.append("Lifecycle hygiene skipped — meridian_lifecycle import failed.")
        return
    try:
        conn = connect(root)
        try:
            for finding in collect_hygiene_findings(conn):
                warnings.append(
                    f"Lifecycle hygiene [{finding['kind']} {finding['id']}]: "
                    f"{finding['reason']} → {finding['suggested_command']}"
                )
        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001 — validator must not crash
        warnings.append(f"Lifecycle hygiene check failed: {exc}")


UI_ACCEPTANCE_RE = re.compile(
    r"\b(layout|visual|token|component|responsive|ui\b|a11y|accessibility|"
    r"design system|breakpoint|webview|dialog|button|form field)\b",
    re.IGNORECASE,
)


SECURITY_ACCEPTANCE_RE = re.compile(
    r"\b(auth|security|secret|owasp|encrypt|csrf|xss|injection|token|password|"
    r"permission|rbac|vulnerability)\b",
    re.IGNORECASE,
)

PRIVACY_ACCEPTANCE_RE = re.compile(
    r"\b(lgpd|gdpr|pii|personal data|dados pessoais|titular|data subject|"
    r"encarregado|consent|privacidade|privacy)\b",
    re.IGNORECASE,
)

PLACEHOLDER_PRIVACY_RE = re.compile(
    r"_\(.*\)_|_TBD_|Delete or mark N/A",
    re.IGNORECASE,
)


def validate_sqlite_us_close_quality(root: Path, warnings: list[str]) -> None:
    """Warn when closed US rows contain batch-close boilerplate (legacy debt) or missing refine content."""
    db_path = root / ".meridian" / "meridian.db"
    if not db_path.is_file():
        return

    import sqlite3

    lib = _SCRIPT_DIR / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from meridian_us_close_quality import validate_closed_us_row  # noqa: PLC0415
    except ImportError:
        warnings.append("US close-quality skipped — meridian_us_close_quality import failed.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, status, body_markdown, intent_why, plan_approach,
                   record_files, intent_acceptance
            FROM user_stories
            WHERE status = '✅'
            """
        ).fetchall()
    finally:
        conn.close()

    for row in rows:
        row_errors: list[str] = []
        validate_closed_us_row(row, row_errors)
        for msg in row_errors:
            warnings.append(f"close-quality: {msg}")


def validate_sqlite_container_integrity(root: Path, warnings: list[str]) -> None:
    """Warn when complete sprints/epics fail the close bar (legacy rows stay WARN)."""
    db_path = root / ".meridian" / "meridian.db"
    if not db_path.is_file():
        return
    lib = _SCRIPT_DIR / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from meridian_container_integrity import collect_closed_container_warnings
        from meridian_db import connect
    except ImportError:
        warnings.append("Container integrity skipped — import failed.")
        return
    conn = connect(root)
    try:
        for msg in collect_closed_container_warnings(conn):
            warnings.append(msg)
    finally:
        conn.close()


def validate_sqlite_security_refs(
    root: Path,
    docs: Path,
    warnings: list[str],
) -> None:
    """Warn when open Must US with security acceptance lack 02_security Plan refs."""
    db_path = root / ".meridian" / "meridian.db"
    security_path = docs / "02_security.md"
    if not db_path.is_file() or not security_path.is_file():
        return
    if read_frontmatter(security_path).get("status") != "approved":
        return

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, moscow, status, body_markdown, plan_architecture_refs
            FROM user_stories
            WHERE status IN ('❌', '🔶')
            """
        ).fetchall()
    finally:
        conn.close()

    for row in rows:
        if (row["moscow"] or "").strip() != "Must":
            continue
        body = row["body_markdown"] or ""
        if not SECURITY_ACCEPTANCE_RE.search(body):
            continue
        refs = row["plan_architecture_refs"] or ""
        if "02_security" not in refs:
            warnings.append(
                f"{row['id']}: Must security US missing 02_security in Plan Architecture "
                "refs — run /security-pass or /refine-us"
            )


def validate_sqlite_test_strategy_refs(
    root: Path,
    docs: Path,
    warnings: list[str],
) -> None:
    """Warn when open Must US with tests required lack 10_test_strategy Plan refs."""
    db_path = root / ".meridian" / "meridian.db"
    strategy_path = docs / "10_test_strategy.md"
    if not db_path.is_file() or not strategy_path.is_file():
        return
    if read_frontmatter(strategy_path).get("status") != "approved":
        return

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, moscow, status, body_markdown, plan_architecture_refs, tests
            FROM user_stories
            WHERE status IN ('❌', '🔶')
            """
        ).fetchall()
    finally:
        conn.close()

    for row in rows:
        if (row["moscow"] or "").strip() != "Must":
            continue
        if (row["tests"] or "").strip() != "required":
            continue
        refs = row["plan_architecture_refs"] or ""
        if "10_test_strategy" not in refs:
            warnings.append(
                f"{row['id']}: Must US with tests: required missing 10_test_strategy in "
                "Plan Architecture refs — run /test-pass or /refine-us"
            )


def validate_quality_siege_profile(
    root: Path,
    docs: Path,
    warnings: list[str],
) -> None:
    """Warn when 10 is approved but qualitySiege was never declared (effective kit default)."""
    strategy_path = docs / "10_test_strategy.md"
    if not strategy_path.is_file():
        return
    if read_frontmatter(strategy_path).get("status") != "approved":
        return

    lib = _SCRIPT_DIR / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from meridian_quality_profile import resolve_quality_siege  # noqa: PLC0415
    except ImportError:
        return

    profile = resolve_quality_siege(root, kit_root=root)
    if profile.get("qualitySiege") != "kit":
        return
    source = profile.get("source") or ""
    if "default" not in source:
        return
    warnings.append(
        "10_test_strategy.md is approved but qualitySiege is undeclared (effective kit) — "
        "set projects[].qualitySiege or delivery.json options.qualitySiege; see agentic-quality-model.md"
    )


def validate_privacy_sections_in_02(docs: Path, warnings: list[str]) -> None:
    """Warn when 02 cites LGPD/GDPR compliance but privacy sections are thin."""
    security_path = docs / "02_security.md"
    if not security_path.is_file():
        return
    text = security_path.read_text(encoding="utf-8")
    lower = text.lower()
    if "lgpd" not in lower and "gdpr" not in lower:
        return
    if "privacy — lgpd" not in lower and "privacy - lgpd" not in lower:
        warnings.append(
            "02_security.md cites compliance but missing § Privacy — LGPD (Brazil) — run /privacy-pass"
        )
    elif "privacy — lgpd" in lower or "privacy - lgpd" in lower:
        lgpd_block = text.lower().split("privacy — lgpd", 1)[-1].split("##", 1)[0]
        if PLACEHOLDER_PRIVACY_RE.search(lgpd_block) or lgpd_block.count("| |") > 3:
            warnings.append(
                "02_security.md § Privacy — LGPD looks placeholder-only — run /privacy-pass full"
            )
    if "gdpr" in lower and "privacy — gdpr" not in lower and "privacy - gdpr" not in lower:
        warnings.append(
            "02_security.md cites GDPR but missing § Privacy — GDPR (EU/EEA) — run /privacy-pass"
        )
    elif "privacy — gdpr" in lower or "privacy - gdpr" in lower:
        gdpr_block = text.lower().split("privacy — gdpr", 1)[-1].split("##", 1)[0]
        if PLACEHOLDER_PRIVACY_RE.search(gdpr_block) or gdpr_block.count("| |") > 3:
            warnings.append(
                "02_security.md § Privacy — GDPR looks placeholder-only — run /privacy-pass full"
            )


def validate_sqlite_privacy_refs(
    root: Path,
    docs: Path,
    warnings: list[str],
) -> None:
    """Warn when open Must US with privacy acceptance lack 02_security privacy Plan refs."""
    db_path = root / ".meridian" / "meridian.db"
    security_path = docs / "02_security.md"
    if not db_path.is_file() or not security_path.is_file():
        return
    if read_frontmatter(security_path).get("status") != "approved":
        return

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, moscow, status, body_markdown, plan_architecture_refs
            FROM user_stories
            WHERE status IN ('❌', '🔶')
            """
        ).fetchall()
    finally:
        conn.close()

    for row in rows:
        if (row["moscow"] or "").strip() != "Must":
            continue
        body = row["body_markdown"] or ""
        if not PRIVACY_ACCEPTANCE_RE.search(body):
            continue
        refs = (row["plan_architecture_refs"] or "").lower()
        if "02_security" not in refs:
            warnings.append(
                f"{row['id']}: Must privacy US missing 02_security in Plan Architecture "
                "refs — run /privacy-pass or /refine-us"
            )
            continue
        if "privacy" not in refs and "lgpd" not in refs and "gdpr" not in refs:
            warnings.append(
                f"{row['id']}: Must privacy US missing privacy/LGPD/GDPR in Plan "
                "Architecture refs — run /privacy-pass or /refine-us"
            )


def validate_sqlite_design_system_refs(
    root: Path,
    docs: Path,
    warnings: list[str],
) -> None:
    """Warn when open Must US with UI acceptance lack 09_design_system Plan refs."""
    db_path = root / ".meridian" / "meridian.db"
    design_path = docs / "09_design_system.md"
    if not db_path.is_file() or not design_path.is_file():
        return
    if read_frontmatter(design_path).get("status") != "approved":
        return

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, moscow, status, body_markdown, plan_architecture_refs
            FROM user_stories
            WHERE status IN ('❌', '🔶')
            """
        ).fetchall()
    finally:
        conn.close()

    for row in rows:
        if (row["moscow"] or "").strip() != "Must":
            continue
        body = row["body_markdown"] or ""
        if not UI_ACCEPTANCE_RE.search(body):
            continue
        refs = row["plan_architecture_refs"] or ""
        if "09_design_system" not in refs:
            warnings.append(
                f"{row['id']}: Must UI US missing 09_design_system in Plan Architecture "
                "refs — run /design-pass or /refine-us"
            )


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
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
        data[key.strip()] = value.strip()
    return data


def parse_cli_args(argv: list[str]) -> tuple[Path, bool, bool, bool]:
    json_output = False
    sqlite_only = False
    strict_kit_md = False
    positional: list[str] = []
    for arg in argv:
        if arg == "--json":
            json_output = True
        elif arg == "--sqlite-only":
            sqlite_only = True
        elif arg == "--strict-kit-md":
            strict_kit_md = True
        else:
            positional.append(arg)
    root = Path(positional[0]).resolve() if positional else Path.cwd()
    return root, json_output, sqlite_only, strict_kit_md


def validate_sqlite_only_mode(root: Path, errors: list[str]) -> None:
    if not sqlite_delivery_active(root):
        errors.append("--sqlite-only: missing .meridian/meridian.db — run meridian_delivery.py bootstrap")
        return
    docs = root / "docs"
    lib_dir = _SCRIPT_DIR / "lib"
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))
    from meridian_db import delivery_md_paths  # noqa: PLC0415

    legacy = delivery_md_paths(docs)
    if legacy:
        sample = ", ".join(str(p.relative_to(root)) for p in legacy[:5])
        suffix = "…" if len(legacy) > 5 else ""
        errors.append(f"--sqlite-only: legacy delivery files remain: {sample}{suffix}")
    board = docs / "kanban" / "board.json"
    if board.is_file():
        errors.append("--sqlite-only: remove docs/kanban/board.json (board_snapshots in SQLite)")


def _kit_line_allowed(line: str) -> bool:
    lowered = line.lower()
    allow = (
        "never ",
        "do not",
        "forbidden",
        "legacy",
        "import-only",
        "removed",
        "não ",
        "not write",
        "→",
        "v1)",
        "anti-pattern",
        "grep ok",
        "histórico",
        "proibição",
        "purge",
        "migrate",
        "meridian-v1-old",
        "extension only",
        "not agents",
        "example:",
        "examples:",
    )
    return any(token in lowered for token in allow)


def validate_kit_markdown_v11(kit_root: Path, errors: list[str], warnings: list[str], *, strict: bool) -> None:
    """Flag v1 delivery write paths still present in operational kit markdown."""
    patterns: list[tuple[str, str]] = [
        (r"generate-board-json", "generate-board-json (removed)"),
        (r"/sync-board", "sync-board (removed in v11)"),
        (r"Save `docs/(us|epics|versions|sprints)/", "Save docs/*/ as primary write path"),
        (r"Invoke `generate-board-json`", "generate-board-json invoke"),
        (r"6\. generate-board-json", "workflow step generate-board-json"),
        (r"app-desktop/", "app-desktop (removed — use app-visual-studio)"),
        (r"--from-file", "update-* --from-file (removed — use stdin heredoc)"),
        (r"meridian_db_export\.py[^\n]*--write(?!-form)", "meridian_db_export --write (use meridian_delivery update-*)"),
        (
            r"meridian_db_export\.py[^\n]*--write-form",
            "meridian_db_export --write-form as agent path (extension only)",
        ),
        (r"`process-manager`", "legacy agent process-manager"),
        (r"`board-keeper`", "legacy agent board-keeper"),
        (r"`security-steward`", "legacy agent security-steward"),
        (r"`architecture-guardian`", "legacy agent architecture-guardian"),
        (r"`documentation-strategist`", "legacy agent documentation-strategist"),
        (r"`scope-architect`", "legacy agent scope-architect"),
    ]
    scan_roots = [
        kit_root / "skills",
        kit_root / "workflows",
        kit_root / "agents",
        kit_root / "references",
        kit_root / "MERIDIAN.md",
        kit_root / "rules" / "MERIDIAN.md",
        kit_root / "ARCHITECTURE.md",
    ]
    skill_dead = kit_root / "skills" / "generate-board-json" / "SKILL.md"
    if skill_dead.is_file():
        msg = "skill generate-board-json still exists — remove folder"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)

    for base in scan_roots:
        if base.is_file():
            files = [base]
        elif base.is_dir():
            files = sorted(base.rglob("*.md"))
        else:
            continue
        rel_base = kit_root
        for path in files:
            if "references/plans/" in str(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if _kit_line_allowed(line):
                    continue
                for pattern, label in patterns:
                    if re.search(pattern, line):
                        rel = path.relative_to(rel_base)
                        msg = f"v11 kit drift ({label}): {rel}:{lineno}"
                        if strict:
                            errors.append(msg)
                        else:
                            warnings.append(msg)
                        break


def main() -> int:
    argv = sys.argv[1:]
    root, json_output, sqlite_only_flag, strict_kit_md = parse_cli_args(argv)
    docs = root / "docs"
    sqlite_delivery = sqlite_delivery_active(root) or sqlite_only_flag
    errors: list[str] = []
    warnings: list[str] = []

    kit_root: Path | None = None
    if (root / ".agent" / "MERIDIAN.md").exists():
        kit_root = root
    elif (root.parent / ".agent" / "MERIDIAN.md").exists():
        kit_root = root.parent
    if kit_root is not None:
        if not (kit_root / "README.md").exists():
            warnings.append("Missing README.md at kit repository root.")
        validate_agent_kit(kit_root, errors, warnings, strict=strict_kit_md)
        validate_cursor_adapter(kit_root, warnings)
        validate_codex_adapter(kit_root, warnings)
        validate_kit_markdown_v11(kit_root, errors, warnings, strict=strict_kit_md)

    if sqlite_only_flag:
        validate_sqlite_only_mode(root, errors)

    architecture_approved = False
    if not docs.exists():
        errors.append("Missing docs/ directory.")
    else:
        for filename in PHASE_DOCS:
            path = docs / filename
            if not path.exists():
                errors.append(f"Missing docs/{filename}.")
                continue
            frontmatter = read_frontmatter(path)
            if "status" not in frontmatter:
                errors.append(f"Missing status frontmatter in docs/{filename}.")

        architecture_path = docs / "05_architecture.md"
        if architecture_path.exists():
            architecture_approved = read_frontmatter(architecture_path).get("status") == "approved"

    us_dir = docs / "us"
    epics_dir = docs / "epics"
    versions_dir = docs / "versions"
    sprints_dir = docs / "sprints"
    decisions_dir = docs / "decisions"
    board_path = docs / "kanban" / "board.json"
    story_ids: set[str] = set()
    epic_ids: set[str] = set()
    version_ids: set[str] = set()

    if versions_dir.exists():
        for version_path in sorted(versions_dir.glob("v*.md")):
            if not re.match(r"v\d+(\.\d+)*\.md$", version_path.name):
                errors.append(f"Invalid version filename: {version_path.name}")
                continue
            frontmatter = read_frontmatter(version_path)
            version_id = frontmatter.get("id")
            if not version_id:
                errors.append(f"Missing id in {version_path.name}")
                continue
            if version_id in version_ids:
                errors.append(f"Duplicate version id: {version_id}")
            version_ids.add(version_id)
            if version_path.stem != version_id:
                errors.append(
                    f"{version_path.name}: id {version_id} does not match filename"
                )
            if not re.match(r"^v\d+(\.\d+)*$", str(version_id)):
                errors.append(f"{version_path.name}: id must use vX or vX.Y format")
            if not frontmatter.get("outcome"):
                errors.append(f"Missing outcome in {version_path.name}")
            if not frontmatter.get("title"):
                errors.append(f"Missing title in {version_path.name}")
            validate_version_structure(
                version_path.name,
                read_markdown_body(version_path),
                errors,
                warnings,
            )
    else:
        if not sqlite_delivery:
            errors.append("Missing docs/versions/ directory.")

    if sprints_dir.exists():
        for sprint_path in sorted(sprints_dir.glob("v*-S*.md")):
            if not re.match(r"v\d+(\.\d+)*-S\d+\.md$", sprint_path.name):
                errors.append(f"Invalid sprint filename: {sprint_path.name}")
                continue
            frontmatter = read_frontmatter(sprint_path)
            sprint_id = frontmatter.get("id")
            version_ref = frontmatter.get("version")
            if not sprint_id:
                errors.append(f"Missing id in {sprint_path.name}")
                continue
            if sprint_path.stem != sprint_id:
                errors.append(
                    f"{sprint_path.name}: id {sprint_id} does not match filename"
                )
            if version_ref and version_ids and version_ref not in version_ids:
                errors.append(
                    f"{sprint_path.name}: version {version_ref} does not exist in docs/versions/"
                )

    if epics_dir.exists():
        for epic_path in sorted(epics_dir.glob("EPIC-*.md")):
            if not re.match(r"EPIC-\d+\.md$", epic_path.name):
                errors.append(f"Invalid epic filename: {epic_path.name}")
                continue
            frontmatter = read_frontmatter(epic_path)
            epic_id = frontmatter.get("id")
            if not epic_id:
                errors.append(f"Missing id in {epic_path.name}")
                continue
            if epic_id in epic_ids:
                errors.append(f"Duplicate epic id: {epic_id}")
            epic_ids.add(epic_id)
            if epic_path.stem != epic_id:
                errors.append(
                    f"{epic_path.name}: id {epic_id} does not match filename"
                )
            if "status" not in frontmatter:
                errors.append(f"Missing status in {epic_path.name}")
            if not frontmatter.get("outcome"):
                errors.append(f"Missing outcome in {epic_path.name}")
            if not frontmatter.get("title"):
                errors.append(f"Missing title in {epic_path.name}")
            epic_versions = frontmatter.get("versions") or []
            if isinstance(epic_versions, list):
                for version_ref in epic_versions:
                    if version_ids and version_ref not in version_ids:
                        errors.append(
                            f"{epic_path.name}: versions references unknown {version_ref}"
                        )
            validate_epic_structure(
                epic_path.name,
                read_markdown_body(epic_path),
                errors,
                warnings,
            )
    else:
        if not sqlite_delivery:
            errors.append("Missing docs/epics/ directory.")

    if decisions_dir.is_dir() and list(decisions_dir.glob("*.json")):
        if sqlite_delivery:
            errors.append(
                "Legacy docs/decisions/*.json present — decisions live in "
                ".meridian/meridian.db (use prepend-decision; purge JSON after import)"
            )
        else:
            for decision_path in sorted(decisions_dir.glob("*.json")):
                if not re.match(r"\d{4}-\d{2}-\d{2}\.json$", decision_path.name):
                    errors.append(f"Invalid decision filename: {decision_path.name}")
                    continue
                try:
                    payload = json.loads(decision_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    errors.append(f"Invalid JSON in {decision_path.name}: {exc}")
                    continue
                if not isinstance(payload, dict):
                    errors.append(f"{decision_path.name}: root must be an object")
                    continue
                date = payload.get("date")
                if not date:
                    errors.append(f"Missing date in {decision_path.name}")
                elif date != decision_path.stem:
                    errors.append(
                        f"{decision_path.name}: date {date} does not match filename"
                    )
                elif not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date)):
                    errors.append(f"{decision_path.name}: date must use YYYY-MM-DD format")
                entries = payload.get("entries")
                if not isinstance(entries, list):
                    errors.append(f"{decision_path.name}: entries must be an array")
                    continue
                if not entries:
                    warnings.append(f"{decision_path.name}: no entries in entries array")
                for index, entry in enumerate(entries):
                    if not isinstance(entry, dict):
                        errors.append(f"{decision_path.name}: entries[{index}] must be an object")
                        continue
                    time = entry.get("time")
                    title = entry.get("title")
                    if not time or not re.match(r"^\d{2}:\d{2}$", str(time)):
                        errors.append(
                            f"{decision_path.name}: entries[{index}].time must be HH:MM"
                        )
                    if not title:
                        errors.append(
                            f"{decision_path.name}: entries[{index}].title is required"
                        )
                    for field in (
                        "affected_document",
                        "what_changed",
                        "why_changed",
                        "impact",
                        "responsible",
                    ):
                        if field not in entry:
                            errors.append(
                                f"{decision_path.name}: entries[{index}] missing {field}"
                            )
    elif not sqlite_delivery:
        errors.append("Missing docs/decisions/ directory.")

    if us_dir.exists() and not sqlite_delivery:
        legacy_missing_context: list[str] = []
        for story in sorted(us_dir.glob("US-*.md")):
            match = re.match(r"US-\d{4}\.md$", story.name)
            if not match:
                errors.append(f"Invalid story filename: {story.name} (use US-XXXX with 4 digits)")
                continue
            frontmatter = read_frontmatter(story)
            story_id = frontmatter.get("id")
            status = frontmatter.get("status")
            epic_ref = frontmatter.get("epic")
            version_ref = frontmatter.get("version")
            if story_id:
                if story_id in story_ids:
                    errors.append(f"Duplicate story id: {story_id}")
                story_ids.add(story_id)
                if story.stem != story_id:
                    errors.append(
                        f"{story.name}: id {story_id} does not match filename"
                    )
                if not re.match(r"^US-\d{4}$", story_id):
                    errors.append(f"{story.name}: id must use US-XXXX format (4 digits)")
            else:
                errors.append(f"Missing id in {story}")
            if epic_ref and epic_ids and epic_ref not in epic_ids:
                errors.append(
                    f"{story.name}: epic {epic_ref} does not exist in docs/epics/"
                )
            if version_ref and version_ids and version_ref not in version_ids:
                errors.append(
                    f"{story.name}: version {version_ref} does not exist in docs/versions/"
                )
            story_text = story.read_text(encoding="utf-8")
            validate_us_structure(
                story.name,
                read_markdown_body(story),
                frontmatter,
                errors,
                warnings,
            )
            if status == "🔶" and "Missing:" not in story_text:
                errors.append(f"{story.name} is 🔶 but has no 'Missing:' in acceptance.")

            tests = frontmatter.get("tests")
            tests_status = frontmatter.get("tests_status")
            if tests not in (None, "required", "none"):
                errors.append(f"{story.name}: tests must be required or none.")
            if tests_status not in (None, "pending", "done", "n/a"):
                errors.append(f"{story.name}: tests_status must be pending, done or n/a.")
            effective_tests = tests if tests is not None else "required"
            effective_status = tests_status
            if effective_status is None:
                effective_status = "n/a" if effective_tests == "none" else "pending"
            if effective_tests == "none" and effective_status != "n/a":
                errors.append(f"{story.name}: tests none requires tests_status n/a.")
            if effective_tests == "required" and effective_status == "n/a":
                errors.append(f"{story.name}: tests required cannot use tests_status n/a.")
            if status == "✅" and effective_tests == "required" and effective_status == "pending":
                errors.append(
                    f"{story.name}: status ✅ requires tests_status done when tests required."
                )
            if effective_tests == "required" and "### Planned" not in story_text:
                errors.append(f"{story.name}: tests required needs ### Planned section.")

            validate_us_semantics(
                story.name,
                status,
                frontmatter,
                story_text,
                errors,
                warnings,
                legacy_missing_context,
            )

        if legacy_missing_context:
            sample = ", ".join(legacy_missing_context[:5])
            suffix = "…" if len(legacy_missing_context) > 5 else ""
            warnings.append(
                f"{len(legacy_missing_context)} open US without ## Plan "
                f"(legacy) — run /refine-us before implement: {sample}{suffix}"
            )

        if story_ids and not architecture_approved:
            errors.append(
                "User stories exist but 05_architecture.md is not approved (delivery gate)."
            )

    if sqlite_delivery and docs.exists():
        validate_privacy_sections_in_02(docs, warnings)
        validate_sqlite_design_system_refs(root, docs, warnings)
        validate_sqlite_security_refs(root, docs, warnings)
        validate_sqlite_privacy_refs(root, docs, warnings)
        validate_sqlite_test_strategy_refs(root, docs, warnings)
        validate_quality_siege_profile(root, docs, warnings)
        validate_sqlite_us_close_quality(root, warnings)
        validate_sqlite_container_integrity(root, warnings)
        validate_lifecycle_hygiene(root, warnings)

    if board_path.exists():
        if sqlite_delivery or sqlite_only_flag:
            if sqlite_only_flag:
                errors.append(
                    "--sqlite-only: remove docs/kanban/board.json (board_snapshots in SQLite)"
                )
        else:
            try:
                board = json.loads(board_path.read_text(encoding="utf-8"))
                board_ids = {item.get("id") for item in board if isinstance(item, dict)}
                missing = story_ids - board_ids
                extra = board_ids - story_ids
                if missing:
                    warnings.append(f"Stories missing from board.json: {sorted(missing)}")
                if extra:
                    warnings.append(f"Board items without story file: {sorted(extra)}")
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid board.json: {exc}")
    elif story_ids and not sqlite_delivery:
        errors.append("Missing docs/kanban/board.json.")

    if json_output:
        payload = {
            "ok": len(errors) == 0,
            "project": str(root),
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Meridian validation failed with {len(errors)} error(s).")
        return 1
    print("Meridian validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
