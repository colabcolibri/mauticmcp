#!/usr/bin/env bash
# Sync Meridian kit → IDE adapters (Cursor .cursor/, Claude Code .claude/, Codex .agents/ + .codex/, OpenCode .opencode/).
#
# Canonical generator for ALL adapters. One command, every IDE.
#
# .agent-native IDEs (Antigravity, ag-kit, etc.) read .agent/ directly — no sync needed.
# Use install-meridian-kit.sh --no-sync or skip this script for those tools.
#
# Run from project root:
#   ./.agent/scripts/sync_kit.sh
#   ./.agent/scripts/sync_kit.sh --cursor-only
#   ./.agent/scripts/sync_kit.sh --codex-only
#   ./.agent/scripts/sync_kit.sh --opencode-only
#   ./.agent/scripts/sync_kit.sh --dry-run

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT="${ROOT}/.agent"
CURSOR="${ROOT}/.cursor"
CLAUDE="${ROOT}/.claude"
CODEX="${ROOT}/.codex"
AGENTS_SKILLS="${ROOT}/.agents/skills"
OPENCODE="${ROOT}/.opencode"
REGISTRY="${AGENT}/references/templates"

SYNC_CURSOR=1
SYNC_CLAUDE=1
SYNC_CODEX=1
SYNC_OPENCODE=1
DRY_RUN=0
PRUNE=1

usage() {
  cat <<'EOF'
sync_kit.sh — generate ALL IDE adapters from .agent/ (Cursor, Claude Code, Codex, OpenCode)

Usage:
  sync_kit.sh [options]

Options:
  --cursor-only     Sync .cursor/ only
  --claude-only     Sync .claude/ only
  --codex-only      Sync Codex adapters only (.agents/skills/, .codex/, AGENTS.md)
  --opencode-only   Sync OpenCode adapter only (.opencode/)
  --no-prune        Create/update links but do not remove orphan Meridian artifacts
  --dry-run         Print actions without writing
  -h, --help        This help

Policy:
  - Never deletes adapter folders wholesale
  - Replaces Meridian symlinks (targets under .agent/)
  - Regenerates Meridian-managed .codex/agents/*.toml from .agent/agents/
  - OpenCode agents: symlinks (same as Claude) — canonical agent.md carries permission frontmatter
  - Removes orphan Meridian symlinks and generated agent TOMLs when removed from kit
  - Leaves real files and non-Meridian symlinks untouched

Antigravity and other .agent-native tools: skip this script; .agent/ is enough.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cursor-only) SYNC_CURSOR=1; SYNC_CLAUDE=0; SYNC_CODEX=0; SYNC_OPENCODE=0; shift ;;
    --claude-only) SYNC_CURSOR=0; SYNC_CLAUDE=1; SYNC_CODEX=0; SYNC_OPENCODE=0; shift ;;
    --codex-only) SYNC_CURSOR=0; SYNC_CLAUDE=0; SYNC_CODEX=1; SYNC_OPENCODE=0; shift ;;
    --opencode-only) SYNC_CURSOR=0; SYNC_CLAUDE=0; SYNC_CODEX=0; SYNC_OPENCODE=1; shift ;;
    --no-prune) PRUNE=0; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h | --help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ ! -d "${AGENT}" ]]; then
  echo "ERROR: missing .agent at ${AGENT}" >&2
  exit 1
fi

if [[ "${SYNC_CURSOR}" -eq 1 && ! -d "${REGISTRY}" ]]; then
  echo "ERROR: missing template registry at ${REGISTRY}" >&2
  exit 1
fi

declare -a EXPECTED=()

register_expected() {
  EXPECTED+=("$1")
}

is_meridian_symlink() {
  local item="$1"
  [[ -L "${item}" ]] || return 1
  local target
  target="$(readlink "${item}")"
  [[ "${target}" == *".agent/"* || "${target}" == *".agent" ]]
}

link() {
  local target="$1"
  local linkpath="$2"
  register_expected "${linkpath}"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] link ${linkpath} -> ${target}"
    return 0
  fi
  mkdir -p "$(dirname "${linkpath}")"
  rm -f "${linkpath}"
  ln -s "${target}" "${linkpath}"
  echo "link ${linkpath} -> ${target}"
}

link_if_safe() {
  local target="$1"
  local linkpath="$2"
  if [[ -e "${linkpath}" && ! -L "${linkpath}" ]]; then
    echo "skip ${linkpath} (existing file — not a Meridian symlink)"
    return 0
  fi
  if [[ -L "${linkpath}" ]] && ! is_meridian_symlink "${linkpath}"; then
    echo "skip ${linkpath} (existing symlink outside .agent/)"
    return 0
  fi
  link "${target}" "${linkpath}"
}

parse_frontmatter_field() {
  local file="$1"
  local field="$2"
  awk -v field="$field" '
    BEGIN { n = 0 }
    /^---$/ { n++; next }
    n == 1 && $0 ~ "^" field "[ \t]*:" {
      line = $0
      sub("^" field "[ \t]*:[ \t]*", "", line)
      if (line ~ /^["'\'']/) {
        gsub(/^["'\'']|["'\'']$/, "", line)
      }
      print line
      exit
    }
  ' "${file}"
}

toml_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  printf '%s' "${s}"
}

write_codex_agent_toml() {
  local agent_file="$1"
  local out_file="$2"
  local name description
  name="$(parse_frontmatter_field "${agent_file}" "name")"
  description="$(parse_frontmatter_field "${agent_file}" "description")"
  [[ -n "${name}" ]] || name="$(basename "$(dirname "${agent_file}")")"
  [[ -n "${description}" ]] || description="Meridian agent ${name}"

  register_expected "${out_file}"

  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] write ${out_file} (from ${agent_file})"
    return 0
  fi

  mkdir -p "$(dirname "${out_file}")"
  cat > "${out_file}" <<EOF
# meridian-kit-generated
name = "$(toml_escape "${name}")"
description = "$(toml_escape "${description}")"
developer_instructions = """
Follow the Meridian agent definition at .agent/agents/${name}/agent.md.
Read that file fully before acting. Skills listed in its frontmatter apply.
"""
EOF
  echo "write ${out_file} (from ${agent_file})"
}

prune_orphans() {
  local adapter_root="$1"
  local label="$2"
  [[ -d "${adapter_root}" ]] || return 0

  while IFS= read -r -d '' item; do
    is_meridian_symlink "${item}" || continue
    local found=0 exp
    for exp in "${EXPECTED[@]}"; do
      if [[ "${item}" == "${exp}" ]]; then
        found=1
        break
      fi
    done
    if [[ "${found}" -eq 0 ]]; then
      if [[ "${DRY_RUN}" -eq 1 ]]; then
        echo "[dry-run] remove orphan ${label}: ${item}"
      else
        rm -f "${item}"
        echo "removed orphan ${label}: ${item}"
      fi
    fi
  done < <(find "${adapter_root}" -type l -print0 2>/dev/null)
}

prune_codex_agents() {
  local agents_dir="${CODEX}/agents"
  [[ -d "${agents_dir}" ]] || return 0

  for toml in "${agents_dir}"/*.toml; do
    [[ -f "${toml}" ]] || continue
    head -n1 "${toml}" 2>/dev/null | grep -q 'meridian-kit-generated' || continue
    local found=0 exp
    for exp in "${EXPECTED[@]}"; do
      if [[ "${toml}" == "${exp}" ]]; then
        found=1
        break
      fi
    done
    if [[ "${found}" -eq 0 ]]; then
      if [[ "${DRY_RUN}" -eq 1 ]]; then
        echo "[dry-run] remove orphan codex agent: ${toml}"
      else
        rm -f "${toml}"
        echo "removed orphan codex agent: ${toml}"
      fi
    fi
  done
}

sync_cursor() {
  mkdir -p "${CURSOR}/rules" "${CURSOR}/skills" "${CURSOR}/agents" "${CURSOR}/commands" "${CURSOR}/references/templates"

  for tpl_file in "${REGISTRY}"/*.md; do
    [[ -f "${tpl_file}" ]] || continue
    name="$(basename "${tpl_file}")"
    link "../../../.agent/references/templates/${name}" "${CURSOR}/references/templates/${name}"
  done

  for skill_dir in "${AGENT}"/skills/*/; do
    [[ -d "${skill_dir}" ]] || continue
    name="$(basename "${skill_dir}")"
    link "../../.agent/skills/${name}" "${CURSOR}/skills/${name}"
  done

  mkdir -p "${CURSOR}/skills/meridian-authoring"
  link "../../../.agent/skills/doc.md" "${CURSOR}/skills/meridian-authoring/SKILL.md"

  for station_dir in "${AGENT}"/agents/*/; do
    [[ -d "${station_dir}" ]] || continue
    [[ -f "${station_dir}agent.md" ]] || continue
    slug="$(basename "${station_dir}")"
    link "../../.agent/agents/${slug}/agent.md" "${CURSOR}/agents/${slug}.md"
  done

  link "../../.agent/rules/meridian.mdc" "${CURSOR}/rules/meridian.mdc"
  link "../../.agent/IDE_ADAPTERS.md" "${CURSOR}/README.md"

  if [[ "${PRUNE}" -eq 1 ]]; then
    prune_orphans "${CURSOR}" "cursor"
  fi
}

sync_claude() {
  mkdir -p "${CLAUDE}/agents"

  for station_dir in "${AGENT}"/agents/*/; do
    [[ -d "${station_dir}" ]] || continue
    [[ -f "${station_dir}agent.md" ]] || continue
    slug="$(basename "${station_dir}")"
    link "../../.agent/agents/${slug}/agent.md" "${CLAUDE}/agents/${slug}.md"
  done

  link "../../.agent/IDE_ADAPTERS.md" "${CLAUDE}/README.md"

  if [[ "${PRUNE}" -eq 1 ]]; then
    prune_orphans "${CLAUDE}" "claude"
  fi
}

sync_codex() {
  mkdir -p "${AGENTS_SKILLS}" "${CODEX}/agents"

  for skill_dir in "${AGENT}"/skills/*/; do
    [[ -d "${skill_dir}" ]] || continue
    name="$(basename "${skill_dir}")"
    link "../../.agent/skills/${name}" "${AGENTS_SKILLS}/${name}"
  done

  mkdir -p "${AGENTS_SKILLS}/meridian-authoring"
  link "../../../.agent/skills/doc.md" "${AGENTS_SKILLS}/meridian-authoring/SKILL.md"

  for station_dir in "${AGENT}"/agents/*/; do
    [[ -d "${station_dir}" ]] || continue
    agent_md="${station_dir}agent.md"
    [[ -f "${agent_md}" ]] || continue
    slug="$(basename "${station_dir}")"
    write_codex_agent_toml "${agent_md}" "${CODEX}/agents/${slug}.toml"
  done

  link "../../.agent/IDE_ADAPTERS.md" "${CODEX}/README.md"
  link_if_safe ".agent/rules/AGENTS.md" "${ROOT}/AGENTS.md"

  if [[ "${PRUNE}" -eq 1 ]]; then
    prune_orphans "${AGENTS_SKILLS}" "codex-skills"
    prune_orphans "${CODEX}" "codex"
    prune_codex_agents
  fi
}

sync_opencode() {
  mkdir -p "${OPENCODE}/agents" "${OPENCODE}/skills"

  # Drop legacy generated copies (pre-symlink policy).
  if [[ -d "${OPENCODE}/agents" ]]; then
    for md in "${OPENCODE}/agents"/*.md; do
      [[ -f "${md}" ]] || continue
      [[ -L "${md}" ]] && continue
      if grep -q 'meridian-kit-generated' "${md}" 2>/dev/null; then
        if [[ "${DRY_RUN}" -eq 1 ]]; then
          echo "[dry-run] remove legacy generated opencode agent: ${md}"
        else
          rm -f "${md}"
          echo "removed legacy generated opencode agent: ${md}"
        fi
      fi
    done
  fi

  for station_dir in "${AGENT}"/agents/*/; do
    [[ -d "${station_dir}" ]] || continue
    [[ -f "${station_dir}agent.md" ]] || continue
    slug="$(basename "${station_dir}")"
    link "../../.agent/agents/${slug}/agent.md" "${OPENCODE}/agents/${slug}.md"
  done

  # Skills mirror kit skills (SKILL.md frontmatter already opencode-compatible).
  # NOTE: meridian-authoring (doc.md) is intentionally skipped — doc.md has no
  # SKILL.md frontmatter, which opencode validates strictly. Use Cursor/Codex for it.
  for skill_dir in "${AGENT}"/skills/*/; do
    [[ -d "${skill_dir}" ]] || continue
    name="$(basename "${skill_dir}")"
    link "../../.agent/skills/${name}" "${OPENCODE}/skills/${name}"
  done

  # No OpenCode plugins — agents/commands/skills only. Board UI stays in VS Code.

  link "../../.agent/IDE_ADAPTERS.md" "${OPENCODE}/README.md"

  if [[ "${PRUNE}" -eq 1 ]]; then
    prune_orphans "${OPENCODE}" "opencode"
    # Drop leftover plugins from older kit versions (views/tools).
    if [[ -d "${OPENCODE}/plugins" ]]; then
      if [[ "${DRY_RUN}" -eq 1 ]]; then
        echo "[dry-run] remove ${OPENCODE}/plugins"
      else
        rm -rf "${OPENCODE}/plugins"
        echo "removed ${OPENCODE}/plugins"
      fi
    fi
  fi
}

if [[ "${SYNC_CURSOR}" -eq 1 ]]; then
  sync_cursor
fi

if [[ "${SYNC_CLAUDE}" -eq 1 ]]; then
  sync_claude
fi

if [[ "${SYNC_CODEX}" -eq 1 ]]; then
  sync_codex
fi

if [[ "${SYNC_OPENCODE}" -eq 1 ]]; then
  sync_opencode
fi

echo ""
if [[ "${SYNC_CURSOR}" -eq 1 ]]; then
  echo "Cursor adapter: ${CURSOR}"
fi
if [[ "${SYNC_CLAUDE}" -eq 1 ]]; then
  echo "Claude Code adapter: ${CLAUDE}"
fi
if [[ "${SYNC_CODEX}" -eq 1 ]]; then
  echo "Codex adapter: ${AGENTS_SKILLS} + ${CODEX} (+ AGENTS.md when safe)"
fi
if [[ "${SYNC_OPENCODE}" -eq 1 ]]; then
  echo "OpenCode adapter: ${OPENCODE} (+ AGENTS.md via Codex sync)"
fi
if [[ "${SYNC_CURSOR}" -eq 0 && "${SYNC_CLAUDE}" -eq 0 && "${SYNC_CODEX}" -eq 0 && "${SYNC_OPENCODE}" -eq 0 ]]; then
  echo "Nothing synced (all adapters disabled)."
fi
echo "Source: .agent/ (committed) → local adapters (gitignored)"
echo "Other IDEs: use .agent/ directly — no adapter sync required."
