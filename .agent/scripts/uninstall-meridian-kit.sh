#!/usr/bin/env bash
# Uninstall Meridian kit from this project — inverse of install-meridian-kit.sh.
#
# Surgical policy (same as sync_kit.sh):
#   - Removes only Meridian-managed artifacts: symlinks targeting .agent/,
#     generated Codex agent TOMLs (# meridian-kit-generated), the AGENTS.md
#     symlink, and empty adapter directories left behind
#   - NEVER touches docs/ or .meridian/ (your delivery data)
#   - NEVER touches real files or symlinks pointing outside .agent/
#
# Usage:
#   ./.agent/scripts/uninstall-meridian-kit.sh              # adapters only (safe)
#   ./.agent/scripts/uninstall-meridian-kit.sh --kit        # also remove .agent/
#   ./.agent/scripts/uninstall-meridian-kit.sh --all        # adapters + kit + gitignore entries
#   ./.agent/scripts/uninstall-meridian-kit.sh --dry-run

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

ADAPTER_ROOTS=(".cursor" ".claude" ".codex" ".agents/skills" ".opencode")
REMOVE_KIT=0
CLEAN_GITIGNORE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
uninstall-meridian-kit.sh — remove Meridian kit artifacts from this project

Usage:
  uninstall-meridian-kit.sh [options]

Options:
  --kit         Also remove .agent/ (WARNING: drops local kit customizations)
  --gitignore   Strip Meridian adapter entries from .gitignore
  --all         Adapters + kit + gitignore entries (full uninstall)
  --dry-run     Print actions without writing
  -h, --help    This help

Default (no flags): remove IDE adapters only — .agent/ stays installed.

Never touched: docs/ phase documents, .meridian/ SQLite delivery data,
and any file that is not Meridian-managed (real files, foreign symlinks).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --kit) REMOVE_KIT=1; shift ;;
    --gitignore) CLEAN_GITIGNORE=1; shift ;;
    --all) REMOVE_KIT=1; CLEAN_GITIGNORE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h | --help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

REMOVED=0
SKIPPED=0

is_meridian_symlink() {
  local item="$1"
  [[ -L "${item}" ]] || return 1
  local target
  target="$(readlink "${item}")"
  [[ "${target}" == *".agent/"* || "${target}" == *".agent" ]]
}

remove_path() {
  local path="$1"
  [[ -e "${path}" || -L "${path}" ]] || return 0
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] remove ${path}"
  else
    rm -rf "${path}"
    echo "removed ${path}"
  fi
  REMOVED=$((REMOVED + 1))
}

skip_path() {
  echo "skip $1 (not Meridian-managed)"
  SKIPPED=$((SKIPPED + 1))
}

remove_meridian_symlinks() {
  local base="$1"
  [[ -d "${base}" ]] || return 0
  while IFS= read -r -d '' item; do
    is_meridian_symlink "${item}" || continue
    remove_path "${item}"
  done < <(find "${base}" -type l -print0 2>/dev/null)
}

remove_generated_codex_tomls() {
  local agents_dir="${ROOT}/.codex/agents"
  [[ -d "${agents_dir}" ]] || return 0
  for toml in "${agents_dir}"/*.toml; do
    [[ -f "${toml}" ]] || continue
    head -n1 "${toml}" 2>/dev/null | grep -q 'meridian-kit-generated' || continue
    remove_path "${toml}"
  done
}

prune_empty_dirs() {
  local base="$1"
  [[ -d "${base}" ]] || return 0
  while IFS= read -r -d '' d; do
    if [[ "${DRY_RUN}" -eq 1 ]]; then
      echo "[dry-run] rmdir ${d} (empty)"
    else
      rmdir "${d}" 2>/dev/null || true
    fi
  done < <(find "${base}" -depth -type d -empty -print0 2>/dev/null)
  if [[ -z "$(ls -A "${base}" 2>/dev/null)" ]]; then
    if [[ "${DRY_RUN}" -eq 1 ]]; then
      echo "[dry-run] rmdir ${base} (empty adapter root)"
    else
      rmdir "${base}" 2>/dev/null || true
    fi
  fi
}

strip_gitignore_block() {
  local f="${ROOT}/.gitignore"
  [[ -f "${f}" ]] || return 0
  grep -q 'Meridian IDE adapters' "${f}" 2>/dev/null || return 0
  local tmp="${f}.meridian-uninstall-tmp"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] strip Meridian adapter entries from ${f}"
  else
    awk '
      BEGIN { skip = 0 }
      /Meridian IDE adapters/ { skip = 1; next }
      skip == 1 {
        if ($0 == ".cursor/" || $0 == ".claude/" || $0 == ".agents/skills/" \
            || $0 == ".codex/" || $0 == ".opencode/" || $0 == "AGENTS.md") next
        skip = 0
      }
      { print }
    ' "${f}" > "${tmp}" && mv "${tmp}" "${f}"
    echo "stripped Meridian adapter entries from ${f}"
  fi
}

echo "Meridian kit uninstall"
[[ "${DRY_RUN}" -eq 1 ]] && echo "(dry-run mode — nothing will be written)"
echo ""

# 1) Meridian symlinks inside each adapter root
for rel in "${ADAPTER_ROOTS[@]}"; do
  remove_meridian_symlinks "${ROOT}/${rel}"
done

# 2) Generated Codex agent TOMLs
remove_generated_codex_tomls

# 3) Root AGENTS.md symlink (only if Meridian-managed)
if [[ -L "${ROOT}/AGENTS.md" ]] && is_meridian_symlink "${ROOT}/AGENTS.md"; then
  remove_path "${ROOT}/AGENTS.md"
elif [[ -e "${ROOT}/AGENTS.md" ]]; then
  skip_path "${ROOT}/AGENTS.md"
fi

# 4) Empty directories left behind (deepest first), incl. empty adapter roots
for rel in "${ADAPTER_ROOTS[@]}"; do
  prune_empty_dirs "${ROOT}/${rel}"
done
# .agents/ parent is kit-created too — drop it when left empty
if [[ -d "${ROOT}/.agents" && -z "$(ls -A "${ROOT}/.agents" 2>/dev/null)" ]]; then
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] rmdir ${ROOT}/.agents (empty)"
  else
    rmdir "${ROOT}/.agents" 2>/dev/null || true
  fi
fi

# 5) Optional: gitignore cleanup
if [[ "${CLEAN_GITIGNORE}" -eq 1 ]]; then
  strip_gitignore_block
fi

# 6) Optional: remove the kit itself
if [[ "${REMOVE_KIT}" -eq 1 ]]; then
  remove_path "${ROOT}/.agent"
  echo ""
  echo "Delivery data preserved: ${ROOT}/.meridian/ (SQLite) and ${ROOT}/docs/."
  echo "The database is NEVER deleted by this script — remove .meridian/ manually if you really want to purge it."
else
  echo ""
  echo "Kit kept: ${ROOT}/.agent (use --kit or --all to remove it)"
fi

echo ""
echo "Done. Removed: ${REMOVED} artifact(s); skipped (foreign): ${SKIPPED}."
echo "Untouched by design: docs/ (phase docs) and .meridian/ (delivery SQLite)."