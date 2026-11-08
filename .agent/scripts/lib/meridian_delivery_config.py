"""Load and validate `.meridian/delivery.json` — connector profile for delivery ops."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DELIVERY_CONFIG_VERSION = 1
DELIVERY_CONFIG_FILENAME = "delivery.json"
MERIDIAN_DIR = ".meridian"
DEFAULT_CONNECTOR = "sqlite"
SUPPORTED_CONNECTORS = frozenset({"sqlite"})


def delivery_config_path(package_root: str | Path) -> Path:
    return Path(package_root).resolve() / MERIDIAN_DIR / DELIVERY_CONFIG_FILENAME


def default_delivery_config(package_root: str | Path | None = None) -> dict[str, Any]:
    if package_root is None:
        pkg = "."
    else:
        root = Path(package_root).resolve()
        pkg = "." if root == Path.cwd().resolve() else str(root)
    return {
        "version": DELIVERY_CONFIG_VERSION,
        "connector": DEFAULT_CONNECTOR,
        "package_root": pkg,
        "options": {},
    }


def _validate_config(data: dict[str, Any], path: Path) -> dict[str, Any]:
    if data.get("version") != DELIVERY_CONFIG_VERSION:
        raise ValueError(
            f"{path}: unsupported version {data.get('version')!r} "
            f"(expected {DELIVERY_CONFIG_VERSION})"
        )
    connector = data.get("connector")
    if connector not in SUPPORTED_CONNECTORS:
        raise ValueError(
            f"{path}: unsupported connector {connector!r} "
            f"(supported: {', '.join(sorted(SUPPORTED_CONNECTORS))})"
        )
    package_root = data.get("package_root")
    if not package_root or not isinstance(package_root, str):
        raise ValueError(f"{path}: package_root must be a non-empty string")
    options = data.get("options", {})
    if not isinstance(options, dict):
        raise ValueError(f"{path}: options must be an object")
    return {
        "version": DELIVERY_CONFIG_VERSION,
        "connector": connector,
        "package_root": package_root,
        "options": options,
    }


def load_delivery_config(
    package_root: str | Path,
    *,
    create_default: bool = False,
) -> dict[str, Any]:
    """Load delivery profile. Missing file → default sqlite config (not written unless create_default)."""
    root = Path(package_root).resolve()
    path = delivery_config_path(root)
    if not path.is_file():
        if create_default:
            return write_delivery_config(root)
        return default_delivery_config(root)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON — {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return _validate_config(data, path)


def write_delivery_config(package_root: str | Path, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Write delivery.json (merge with defaults). Returns validated config."""
    root = Path(package_root).resolve()
    meridian_dir = root / MERIDIAN_DIR
    meridian_dir.mkdir(parents=True, exist_ok=True)
    path = delivery_config_path(root)
    base = default_delivery_config(root)
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                base.update(existing)
        except json.JSONDecodeError:
            pass
    if config:
        base.update(config)
    pr = base.get("package_root", ".")
    if Path(pr).resolve() == root.resolve():
        base["package_root"] = "."
    validated = _validate_config(base, path)
    path.write_text(json.dumps(validated, indent=2) + "\n", encoding="utf-8")
    return validated


def resolve_package_root(
    explicit: str | Path | None = None,
    cwd: Path | None = None,
) -> Path:
    """Resolve product package root: explicit flag → delivery.json → cwd."""
    if explicit is not None:
        return Path(explicit).resolve()
    start = (cwd or Path.cwd()).resolve()
    candidate = start
    for _ in range(12):
        cfg_path = delivery_config_path(candidate)
        if cfg_path.is_file():
            cfg = load_delivery_config(candidate)
            pr = cfg["package_root"]
            if pr == ".":
                return candidate
            return Path(pr).resolve()
        if (candidate / "docs" / "00_scope.md").exists() or (
            candidate / MERIDIAN_DIR / "meridian.db"
        ).exists():
            return candidate
        if candidate.parent == candidate:
            break
        candidate = candidate.parent
    return start
