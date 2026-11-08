#!/usr/bin/env python3
"""Tests for import_graph builder (US-0163)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent / "lib"))

from import_graph import build_import_graph  # noqa: E402


def _edge_set(graph: dict) -> set[tuple[str, str]]:
    return {(e["from"], e["to"]) for e in graph["edges"]}


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "node_modules" / "x").mkdir(parents=True)
        (root / "node_modules" / "x" / "index.js").write_text("export default 1\n")
        (root / "a.ts").write_text('import { b } from "./b.js";\nexport const a = b;\n')
        (root / "b.ts").write_text("export const b = 1;\n")
        graph = build_import_graph(root)
        ids = {n["id"] for n in graph["nodes"]}
        if "a.ts" not in ids or "b.ts" not in ids:
            print(f"FAIL: nodes {ids}")
            return 1
        if any("node_modules" in n["id"] for n in graph["nodes"]):
            print("FAIL: node_modules leaked into graph")
            return 1
        if not any(e["from"] == "a.ts" and e["to"] == "b.ts" for e in graph["edges"]):
            print(f"FAIL: missing edge a.ts -> b.ts: {graph['edges']}")
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pkg = root / "lib"
        pkg.mkdir()
        (pkg / "index.ts").write_text('export { util } from "./util";\n')
        (pkg / "util.ts").write_text("export const util = 1;\n")
        (root / "main.ts").write_text('import { util } from "./lib";\nexport { util };\n')
        graph = build_import_graph(root)
        edges = _edge_set(graph)
        if ("main.ts", "lib/index.ts") not in edges:
            print(f"FAIL: extensionless dir import: {edges}")
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "loader.ts").write_text('const m = await import("./mod.ts");\nexport default m;\n')
        (root / "mod.ts").write_text("export default {};\n")
        graph = build_import_graph(root)
        if not any(e["from"] == "loader.ts" and e["to"] == "mod.ts" for e in graph["edges"]):
            print(f"FAIL: dynamic import(): {graph['edges']}")
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pkg").mkdir()
        (root / "pkg" / "__init__.py").write_text("from .utils import helper\n")
        (root / "pkg" / "utils.py").write_text("def helper(): pass\n")
        (root / "app.py").write_text("from .pkg.utils import helper\n")
        graph = build_import_graph(root)
        if not any(e["from"] == "app.py" and e["to"] == "pkg/utils.py" for e in graph["edges"]):
            print(f"FAIL: python relative import: {graph['edges']}")
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tsconfig.json").write_text(
            '{"compilerOptions":{"baseUrl":".","paths":{"@/*":["src/*"]}}}\n'
        )
        (root / "src").mkdir()
        (root / "src" / "util.ts").write_text("export const u = 1;\n")
        (root / "src" / "main.ts").write_text('import { u } from "@/util";\nexport { u };\n')
        graph = build_import_graph(root)
        if not any(e["from"] == "src/main.ts" and e["to"] == "src/util.ts" for e in graph["edges"]):
            print(f"FAIL: tsconfig path alias: {graph['edges']}")
            return 1
        if not graph.get("meta", {}).get("pathAliases"):
            print("FAIL: meta.pathAliases not set")
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tsconfig.json").write_text(
            """{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": [".expo/types/**/*.ts", "src/**/*.tsx"]
}
"""
        )
        (root / "src").mkdir()
        (root / "src" / "util.ts").write_text("export const u = 1;\n")
        (root / "src" / "main.ts").write_text('import { u } from "@/util";\nexport { u };\n')
        graph = build_import_graph(root)
        if not any(e["from"] == "src/main.ts" and e["to"] == "src/util.ts" for e in graph["edges"]):
            print(f"FAIL: tsconfig glob in include must not break JSONC parse: {graph['edges']}")
            return 1

    print("OK: import graph tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
