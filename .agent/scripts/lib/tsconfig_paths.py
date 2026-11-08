"""Resolve TypeScript path aliases from tsconfig/jsconfig (stdlib only)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_TSCONFIG_NAMES = ("tsconfig.json", "jsconfig.json")


def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments without touching string literals (e.g. glob `**/*.ts`)."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_string = False
    escape = False
    while i < n:
        ch = text[i]
        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                i += 2
                while i < n and text[i] not in "\r\n":
                    i += 1
                continue
            if nxt == "*":
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i = min(i + 2, n)
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def _resolve_extends_path(config_dir: Path, spec: str) -> Path | None:
    raw = spec.strip().strip('"')
    if raw.startswith("."):
        base = (config_dir / raw).resolve()
    else:
        base = (config_dir / raw).resolve()
    candidates = [base]
    if base.suffix.lower() != ".json":
        candidates.append(Path(str(base) + ".json"))
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _merge_compiler_options(base: dict[str, object], child: dict[str, object]) -> dict[str, object]:
    merged = dict(base)
    for key, value in child.items():
        if key == "paths" and isinstance(value, dict) and isinstance(merged.get("paths"), dict):
            paths = dict(merged["paths"])
            paths.update(value)
            merged["paths"] = paths
        else:
            merged[key] = value
    return merged


def load_compiler_options(config_path: Path, _seen: set[Path] | None = None) -> tuple[dict[str, object], Path]:
    config_path = config_path.resolve()
    seen = _seen or set()
    if config_path in seen:
        return {}, config_path.parent
    seen.add(config_path)
    raw = strip_jsonc(config_path.read_text(encoding="utf-8", errors="replace"))
    data = json.loads(raw)
    options: dict[str, object] = {}
    if "extends" in data:
        parent_path = _resolve_extends_path(config_path.parent, str(data["extends"]))
        if parent_path:
            parent_opts, _ = load_compiler_options(parent_path, seen)
            options = dict(parent_opts)
    child_opts = data.get("compilerOptions")
    if isinstance(child_opts, dict):
        options = _merge_compiler_options(options, child_opts)
    return options, config_path.parent


def find_tsconfig(start: Path, workspace: Path | None = None) -> Path | None:
    current = start.resolve()
    stop = workspace.resolve() if workspace else None
    while True:
        for name in _TSCONFIG_NAMES:
            candidate = current / name
            if candidate.is_file():
                return candidate
        if stop is not None and current == stop:
            break
        parent = current.parent
        if parent == current:
            break
        if stop is not None:
            try:
                parent.relative_to(stop)
            except ValueError:
                break
        current = parent
    return None


@dataclass(frozen=True)
class PathAliasRule:
    prefix: str
    suffix: str
    target_prefix: str
    target_suffix: str


def _compile_alias(key: str, target: str) -> PathAliasRule | None:
    if "*" not in key:
        return None
    star = key.index("*")
    key_pre, key_post = key[:star], key[star + 1 :]
    if "*" not in target:
        return None
    t_star = target.index("*")
    t_pre, t_post = target[:t_star], target[t_star + 1 :]
    return PathAliasRule(key_pre, key_post, t_pre, t_post)


class TsconfigPathResolver:
    """Map import specifiers (e.g. @/foo) to repo-relative source paths."""

    def __init__(self, base_dir: Path, rules: list[PathAliasRule], exact: dict[str, list[str]]) -> None:
        self.base_dir = base_dir.resolve()
        self.rules = rules
        self.exact = exact

    @classmethod
    def from_root(cls, root: Path, workspace: Path | None = None) -> TsconfigPathResolver:
        config = find_tsconfig(root, workspace)
        if not config:
            return cls(root, [], {})
        options, config_dir = load_compiler_options(config)
        base_url = options.get("baseUrl", ".")
        base_dir = (config_dir / str(base_url)).resolve()
        paths = options.get("paths")
        if not isinstance(paths, dict):
            return cls(base_dir, [], {})
        rules: list[PathAliasRule] = []
        exact: dict[str, list[str]] = {}
        for key, raw_targets in paths.items():
            if not isinstance(key, str):
                continue
            targets = raw_targets if isinstance(raw_targets, list) else [raw_targets]
            targets = [str(t) for t in targets]
            if "*" in key:
                for target in targets:
                    rule = _compile_alias(key, target)
                    if rule:
                        rules.append(rule)
            else:
                exact[key] = targets
        rules.sort(key=lambda r: len(r.prefix), reverse=True)
        return cls(base_dir, rules, exact)

    def candidate_paths(self, spec: str) -> list[Path]:
        if spec.startswith("."):
            return []
        out: list[Path] = []
        if spec in self.exact:
            for target in self.exact[spec]:
                out.append((self.base_dir / target).resolve())
            return out
        for rule in self.rules:
            if not spec.startswith(rule.prefix):
                continue
            if rule.suffix and not spec.endswith(rule.suffix):
                continue
            middle = spec[len(rule.prefix) : len(spec) - len(rule.suffix) if rule.suffix else len(spec)]
            rel = f"{rule.target_prefix}{middle}{rule.target_suffix}"
            out.append((self.base_dir / rel).resolve())
        return out
