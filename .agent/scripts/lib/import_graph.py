"""Static import graph helpers — normalize analyzer output into stable JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tsconfig_paths import TsconfigPathResolver

DEFAULT_EXCLUDES = frozenset(
    {
        "node_modules",
        "dist",
        "out",
        "build",
        ".git",
        ".meridian",
        "coverage",
        ".venv",
        "venv",
        "__pycache__",
        ".turbo",
        ".next",
    }
)

_TS_IMPORT_RE = re.compile(
    r"""(?:import\s+(?:type\s+)?(?:[^"';\n]+?\s+from\s+)?"""
    r"""|export\s+(?:type\s+)?(?:\*\s+from|[^"';\n]*?\s+from\s+)"""
    r"""|require\s*\(\s*"""
    r"""|import\s*\(\s*)['"]([^'"]+)['"]""",
    re.MULTILINE,
)
_PY_IMPORT_RE = re.compile(
    r"""^(?:from\s+(\.+[\w.]*)\s+import\s+|import\s+(\.+[\w.]*))""",
    re.MULTILINE,
)

SOURCE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py"}
RESOLVE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py")


def should_skip_dir(name: str, excludes: frozenset[str] = DEFAULT_EXCLUDES) -> bool:
    return name in excludes or name.startswith(".")


def iter_source_files(root: Path, excludes: frozenset[str] = DEFAULT_EXCLUDES) -> list[Path]:
    files: list[Path] = []
    root = root.resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in SOURCE_SUFFIXES:
            continue
        rel_parts = path.relative_to(root).parts
        if any(should_skip_dir(part, excludes) for part in rel_parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def build_file_index(root: Path, files: list[Path]) -> dict[str, str]:
    """Lookup keys (path, extensionless path, directory) → canonical repo-relative file."""
    index: dict[str, str] = {}
    for path in files:
        rel = str(path.relative_to(root)).replace("\\", "/")
        index[rel] = rel
        name = rel.rsplit("/", 1)[-1]
        if "." in name:
            stem = rel.rsplit(".", 1)[0]
            index.setdefault(stem, rel)
        parts = rel.split("/")
        if parts[-1].startswith("index.") and len(parts) > 1:
            dir_key = "/".join(parts[:-1])
            index.setdefault(dir_key, rel)
            index.setdefault(f"./{dir_key}", rel)
    return index


def _file_candidates(target: Path) -> list[Path]:
    if target.suffix in RESOLVE_SUFFIXES:
        stem = target.with_suffix("")
        bases = [target, stem]
    else:
        bases = [target]
    candidates: list[Path] = []
    for base in bases:
        candidates.append(base)
        for suffix in RESOLVE_SUFFIXES:
            candidates.append(base.with_suffix(suffix))
        candidates.append(base / "index.ts")
        candidates.append(base / "index.tsx")
        candidates.append(base / "index.js")
        candidates.append(base / "index.mjs")
        candidates.append(base / "__init__.py")
    return candidates


def lookup_resolved_path(candidate: Path, root: Path, index: dict[str, str]) -> str | None:
    for cand in _file_candidates(candidate):
        if not cand.is_file():
            continue
        try:
            rel = str(cand.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
        return index.get(rel, rel)
    try:
        rel = str(candidate.relative_to(root)).replace("\\", "/")
        if rel in index:
            return index[rel]
    except ValueError:
        pass
    return None


def _resolve_relative_spec(importer: Path, spec: str, root: Path, index: dict[str, str]) -> str | None:
    if not spec.startswith("."):
        return None
    base = (importer.parent / spec).resolve()
    return lookup_resolved_path(base, root, index)


def _resolve_alias_spec(
    spec: str,
    root: Path,
    index: dict[str, str],
    path_resolver: TsconfigPathResolver,
) -> str | None:
    for candidate in path_resolver.candidate_paths(spec):
        resolved = lookup_resolved_path(candidate, root, index)
        if resolved:
            return resolved
    return None


def _python_module_to_path(importer: Path, mod: str) -> Path:
    level = 0
    while level < len(mod) and mod[level] == ".":
        level += 1
    rest = mod[level:].replace(".", "/") if level < len(mod) else ""
    base = importer.parent
    for _ in range(max(0, level - 1)):
        base = base.parent
    if rest:
        return base / rest
    return base


def _resolve_python_import(importer: Path, mod: str, root: Path, index: dict[str, str]) -> str | None:
    if not mod.startswith("."):
        return None
    target = _python_module_to_path(importer, mod)
    return lookup_resolved_path(target, root, index)


def extract_imports(
    path: Path,
    root: Path,
    index: dict[str, str],
    path_resolver: TsconfigPathResolver,
) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    targets: list[str] = []
    seen: set[str] = set()

    def add(target: str | None) -> None:
        if not target or target in seen:
            return
        seen.add(target)
        targets.append(target)

    if path.suffix == ".py":
        for match in _PY_IMPORT_RE.finditer(text):
            mod = match.group(1) or match.group(2)
            if not mod:
                continue
            add(_resolve_python_import(path, mod, root, index))
        return targets

    for match in _TS_IMPORT_RE.finditer(text):
        spec = match.group(1)
        if spec.startswith("."):
            add(_resolve_relative_spec(path, spec, root, index))
        else:
            add(_resolve_alias_spec(spec, root, index, path_resolver))
    return targets


def build_import_graph(
    root: Path,
    *,
    excludes: frozenset[str] = DEFAULT_EXCLUDES,
    workspace: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    files = iter_source_files(root, excludes)
    index = build_file_index(root, files)
    path_resolver = TsconfigPathResolver.from_root(root, workspace)
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []
    seen_edges: set[tuple[str, str]] = set()

    for path in files:
        node_id = str(path.relative_to(root)).replace("\\", "/")
        nodes[node_id] = {"id": node_id, "label": path.name}
        for target in extract_imports(path, root, index, path_resolver):
            if not target or target not in index:
                continue
            if target not in nodes:
                nodes[target] = {"id": target, "label": Path(target).name}
            key = (node_id, target)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append({"from": node_id, "to": target})

    node_list = sorted(nodes.values(), key=lambda n: n["id"])
    edge_list = sorted(edges, key=lambda e: (e["from"], e["to"]))
    meta: dict[str, Any] = {
        "root": str(root),
        "nodeCount": len(node_list),
        "edgeCount": len(edge_list),
        "excludes": sorted(excludes),
    }
    if path_resolver.rules or path_resolver.exact:
        meta["pathAliases"] = True
    return {
        "nodes": node_list,
        "edges": edge_list,
        "meta": meta,
    }


def graph_to_json(graph: dict[str, Any]) -> str:
    return json.dumps(graph, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
