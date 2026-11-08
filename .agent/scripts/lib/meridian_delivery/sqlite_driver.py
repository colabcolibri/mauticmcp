"""SQLite delivery driver — delegates to meridian_db_cli (v11 default)."""

from __future__ import annotations

import sys
from pathlib import Path

from meridian_delivery.registry import register_driver

_SCRIPT_DIR = Path(__file__).resolve().parents[2]


def _normalize_argv(argv: list[str], package_root: Path) -> list[str]:
    """Support legacy trailing `.` and inject --package-root when missing."""
    out = list(argv)
    if out and out[0] == "--":
        out = out[1:]
    if "--package-root" not in out and len(out) >= 2:
        last = out[-1]
        if last in (".", "..") or Path(last).is_dir():
            out = out[:-1]
            out = ["--package-root", str(package_root.resolve())] + out
    if "--package-root" not in out:
        out = ["--package-root", str(package_root.resolve())] + out
    return out


@register_driver("sqlite")
class SqliteDriver:
    name = "sqlite"

    def dispatch(self, package_root: str, argv: list[str]) -> int:
        scripts_dir = str(_SCRIPT_DIR)
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        normalized = _normalize_argv(argv, Path(package_root))
        sys.argv = ["meridian_db_cli.py", *normalized]
        import meridian_db_cli  # noqa: WPS433

        return meridian_db_cli.main()
