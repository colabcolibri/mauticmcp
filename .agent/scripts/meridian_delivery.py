#!/usr/bin/env python3
"""Meridian delivery facade — connector-agnostic CLI for agents and workflows.

Reads `.meridian/delivery.json` (default connector: sqlite). Skills should call
this script instead of backend-specific tools. See delivery-connector-schema.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_db import bootstrap, is_meridian_package  # noqa: E402
from meridian_delivery.registry import get_driver, list_connectors  # noqa: E402
from meridian_delivery_config import (  # noqa: E402
    load_delivery_config,
    resolve_package_root,
    write_delivery_config,
)
from meridian_quality_profile import resolve_quality_siege  # noqa: E402


def _cmd_config(package_root: Path) -> int:
    cfg = load_delivery_config(package_root, create_default=False)
    cfg_path = package_root / ".meridian" / "delivery.json"
    print(json.dumps({"path": str(cfg_path), "config": cfg}, indent=2))
    return 0


def _cmd_quality_profile(package_root: Path) -> int:
    print(json.dumps(resolve_quality_siege(package_root), indent=2))
    return 0


def _cmd_bootstrap(package_root: Path) -> int:
    if not is_meridian_package(package_root):
        print(
            f"ERROR: {package_root} is not a Meridian product (missing docs/ fingerprint).",
            file=sys.stderr,
        )
        return 1
    try:
        print(bootstrap(package_root))
        cfg = write_delivery_config(package_root)
        print(f"delivery.json: connector={cfg['connector']}")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


def _parse_global_flags(argv: list[str]) -> tuple[Path | None, list[str]]:
    package_root: Path | None = None
    rest: list[str] = []
    i = 0
    while i < len(argv):
        token = argv[i]
        if token == "--package-root" and i + 1 < len(argv):
            package_root = Path(argv[i + 1]).resolve()
            i += 2
            continue
        if token.startswith("--package-root="):
            package_root = Path(token.split("=", 1)[1]).resolve()
            i += 1
            continue
        rest.append(token)
        i += 1
    return package_root, rest


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(
            "Usage: meridian_delivery.py [--package-root PATH] <command> [args...]\n"
            "Facade commands: config | bootstrap | quality-profile | connectors\n"
            "Delivery verbs: counts, list, show, create-us, … (see delivery-connector-schema.md)\n"
            "Config: .meridian/delivery.json (default connector: sqlite)"
        )
        return 0 if argv and argv[0] in ("-h", "--help") else (1 if not argv else 0)

    explicit_root, passthrough = _parse_global_flags(argv)
    package_root = resolve_package_root(explicit_root)

    if passthrough[0] == "config":
        return _cmd_config(package_root)
    if passthrough[0] == "bootstrap":
        return _cmd_bootstrap(package_root)
    if passthrough[0] == "quality-profile":
        return _cmd_quality_profile(package_root)
    if passthrough[0] == "connectors":
        print("\n".join(list_connectors()))
        return 0

    try:
        config = load_delivery_config(package_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if explicit_root is not None:
        config = {**config, "package_root": str(package_root)}

    try:
        driver = get_driver(config["connector"])
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return driver.dispatch(config["package_root"], passthrough)


if __name__ == "__main__":
    raise SystemExit(main())
