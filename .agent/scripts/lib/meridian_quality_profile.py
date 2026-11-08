"""Resolve qualitySiege profile for a Meridian product — manifest, delivery, default."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from meridian_delivery_config import (
    MERIDIAN_DIR,
    delivery_config_path,
    load_delivery_config,
)

QualitySiegeProfile = Literal["kit", "standard", "full"]
QUALITY_SIEGE_PROFILES: frozenset[str] = frozenset({"kit", "standard", "full"})
MANIFEST_FILENAME = "projects.json"
KIT_REL = Path(".agent") / "MERIDIAN.md"

PROFILE_GATES: dict[QualitySiegeProfile, tuple[str, ...]] = {
    "kit": (
        "validate_meridian",
        "meridian_delivery_bootstrap",
        "run_kit_tests",
    ),
    "standard": (
        "validate_meridian",
        "meridian_delivery_bootstrap",
        "run_kit_tests",
        "unit_integration_tests",
        "typecheck_lint",
        "pre_commit_validator",
    ),
    "full": (
        "validate_meridian",
        "meridian_delivery_bootstrap",
        "run_kit_tests",
        "unit_integration_tests",
        "typecheck_lint",
        "pre_commit_validator",
        "dependency_audit",
        "codeql",
        "coverage_advisory",
        "mutation_pilot",
        "independent_review",
    ),
}


def find_kit_root(start: str | Path) -> Path | None:
    current = Path(start).resolve()
    for _ in range(12):
        if (current / KIT_REL).is_file():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def _normalize_docs_rel(docs_rel: str) -> str:
    return docs_rel.replace("\\", "/").strip("/")


def _package_root_from_docs(kit_root: Path, docs_rel: str) -> str:
    docs_path = Path(*_normalize_docs_rel(docs_rel).split("/"))
    parent = docs_path.parent
    if str(parent) in ("", "."):
        return "."
    return str(parent).replace("\\", "/")


def _read_manifest(kit_root: Path) -> dict[str, Any] | None:
    path = kit_root / MERIDIAN_DIR / MANIFEST_FILENAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _profile_from_manifest(
    kit_root: Path,
    package_root: Path,
) -> tuple[QualitySiegeProfile | None, str | None]:
    manifest = _read_manifest(kit_root)
    if not manifest:
        return None, None

    package_rel = _normalize_docs_rel(
        str(package_root.resolve().relative_to(kit_root.resolve()))
    )
    if package_rel == ".":
        package_rel = "."

    for entry in manifest.get("projects") or []:
        if not isinstance(entry, dict):
            continue
        docs = entry.get("docs")
        if not isinstance(docs, str):
            continue
        entry_package = _package_root_from_docs(kit_root, docs)
        entry_package_norm = "." if entry_package == "." else _normalize_docs_rel(entry_package)
        package_norm = "." if package_rel == "." else _normalize_docs_rel(package_rel)
        if entry_package_norm != package_norm:
            continue
        raw = entry.get("qualitySiege")
        if isinstance(raw, str) and raw in QUALITY_SIEGE_PROFILES:
            project_id = entry.get("id")
            source = f".meridian/projects.json"
            if isinstance(project_id, str):
                source = f".meridian/projects.json (project {project_id})"
            return raw, source  # type: ignore[return-value]
    return None, None


def _profile_from_delivery(package_root: Path) -> tuple[QualitySiegeProfile | None, str | None]:
    path = delivery_config_path(package_root)
    if not path.is_file():
        return None, None
    try:
        cfg = load_delivery_config(package_root)
    except ValueError:
        return None, None
    options = cfg.get("options", {})
    if not isinstance(options, dict):
        return None, None
    raw = options.get("qualitySiege")
    if isinstance(raw, str) and raw in QUALITY_SIEGE_PROFILES:
        return raw, ".meridian/delivery.json options.qualitySiege"  # type: ignore[return-value]
    return None, None


def resolve_quality_siege(
    package_root: str | Path,
    *,
    kit_root: str | Path | None = None,
) -> dict[str, Any]:
    """Return profile, source, expected gates, and kit root used for lookup."""
    pkg = Path(package_root).resolve()
    kit = Path(kit_root).resolve() if kit_root else find_kit_root(pkg)
    if kit is None:
        kit = pkg

    profile: QualitySiegeProfile | None = None
    source: str | None = None

    manifest_profile, manifest_source = _profile_from_manifest(kit, pkg)
    if manifest_profile:
        profile, source = manifest_profile, manifest_source
    else:
        delivery_profile, delivery_source = _profile_from_delivery(pkg)
        if delivery_profile:
            profile, source = delivery_profile, delivery_source

    if profile is None:
        profile = "kit"
        source = "default (no qualitySiege declared)"

    return {
        "package_root": str(pkg),
        "kit_root": str(kit),
        "qualitySiege": profile,
        "source": source,
        "gates": list(PROFILE_GATES[profile]),
    }


def validate_quality_siege_value(value: Any, *, context: str) -> QualitySiegeProfile:
    if not isinstance(value, str) or value not in QUALITY_SIEGE_PROFILES:
        allowed = ", ".join(sorted(QUALITY_SIEGE_PROFILES))
        raise ValueError(f"{context}: qualitySiege must be one of {allowed}")
    return value  # type: ignore[return-value]
