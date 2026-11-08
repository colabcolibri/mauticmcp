#!/usr/bin/env python3
"""Compute a scoped source import graph as JSON (US-0163)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from import_graph import (  # noqa: E402
    DEFAULT_EXCLUDES,
    build_import_graph,
    graph_to_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic import graph for a package path (excludes node_modules by default)."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Package or folder to scan (required — never scans the whole disk).",
    )
    parser.add_argument(
        "--workspace",
        default="",
        help="Optional workspace root; --root must resolve inside it.",
    )
    parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Optional output file (default: stdout).",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2

    if args.workspace:
        workspace = Path(args.workspace).expanduser().resolve()
        try:
            root.relative_to(workspace)
        except ValueError:
            print(
                f"ERROR: root {root} is outside workspace {workspace}",
                file=sys.stderr,
            )
            return 2

    graph = build_import_graph(
        root,
        excludes=DEFAULT_EXCLUDES,
        workspace=Path(args.workspace).expanduser().resolve() if args.workspace else None,
    )
    payload = graph_to_json(graph)
    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
        print(f"Wrote {out_path} ({graph['meta']['nodeCount']} nodes)", file=sys.stderr)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
