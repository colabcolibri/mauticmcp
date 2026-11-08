#!/usr/bin/env bash
# Install Meridian kit into a project: copy .agent/ and sync IDE adapters.
#
# Usage:
#   ./.agent/scripts/install-meridian-kit.sh [options] [TARGET_DIR]
#   MERIDIAN_KIT_SRC=/path/to/source/.agent ./.agent/scripts/install-meridian-kit.sh ~/my-app
#
# Antigravity / .agent-native IDEs: use --no-sync ( .agent/ alone is enough ).

set -euo pipefail

usage() {
  cat <<'EOF'
install-meridian-kit.sh — copy .agent/ and build IDE adapters

Usage:
  install-meridian-kit.sh [options] [TARGET_DIR]

Options:
  --force         Overwrite existing .agent/ (rsync --delete)
  --no-sync       Copy .agent/ only — for Antigravity and other .agent-native IDEs
  --cursor-only   Sync .cursor/ adapter only (after copy)
  --claude-only   Sync .claude/ adapter only (after copy)
  --codex-only    Sync Codex adapters only (after copy)
  --opencode-only Sync OpenCode adapter only (.opencode/) (after copy)
  --dry-run       Show actions without writing
  -h, --help      This help

Environment:
  MERIDIAN_KIT_SRC   Source .agent/ directory (default: kit next to this script)

IDE support:
  Cursor       .agent/ + .cursor/ symlinks (default install)
  Claude Code  .agent/ + .claude/ symlinks (default install)
  Codex        .agent/ + .agents/skills/ + .codex/ (default install)
  OpenCode     .agent/ + .opencode/ commands/agents/skills (default install)
  Antigravity  .agent/ only — pass --no-sync

Examples:
  ./.agent/scripts/install-meridian-kit.sh .
  ./.agent/scripts/install-meridian-kit.sh --no-sync ~/antigravity-project
  ./.agent/scripts/install-meridian-kit.sh --force .
EOF
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_KIT_SRC="$(cd "${SCRIPT_DIR}/.." && pwd)"
FORCE=0
NO_SYNC=0
SYNC_FLAGS=()
DRY_RUN=0
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --no-sync) NO_SYNC=1; shift ;;
    --cursor-only) SYNC_FLAGS=(--cursor-only); shift ;;
    --claude-only) SYNC_FLAGS=(--claude-only); shift ;;
    --codex-only) SYNC_FLAGS=(--codex-only); shift ;;
    --opencode-only) SYNC_FLAGS=(--opencode-only); shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h | --help) usage; exit 0 ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -n "${TARGET}" ]]; then
        echo "Unexpected argument: $1" >&2
        exit 1
      fi
      TARGET="$1"
      shift
      ;;
  esac
done

TARGET="${TARGET:-.}"
mkdir -p "${TARGET}"
TARGET="$(cd "${TARGET}" && pwd)"
KIT_SRC="${MERIDIAN_KIT_SRC:-${DEFAULT_KIT_SRC}}"

if [[ ! -f "${KIT_SRC}/MERIDIAN.md" ]]; then
  echo "ERROR: invalid kit source (missing MERIDIAN.md): ${KIT_SRC}" >&2
  echo "Set MERIDIAN_KIT_SRC to a .agent/ folder from the Meridian kit." >&2
  exit 1
fi

RSYNC_FLAGS=(-a)
if [[ "${FORCE}" -eq 1 ]]; then
  RSYNC_FLAGS+=("--delete")
fi
if [[ "${DRY_RUN}" -eq 1 ]]; then
  RSYNC_FLAGS+=("--dry-run" "-vn")
fi

echo "Meridian kit install"
echo "  Source: ${KIT_SRC}"
echo "  Target: ${TARGET}"
echo ""

if [[ -d "${TARGET}/.agent" && "${FORCE}" -ne 1 && "${DRY_RUN}" -ne 1 ]]; then
  echo "WARNING: ${TARGET}/.agent already exists."
  echo "Re-run with --force to overwrite, or sync adapters only:"
  echo "  ${TARGET}/.agent/scripts/sync_kit.sh"
  exit 1
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "[dry-run] rsync ${RSYNC_FLAGS[*]} ${KIT_SRC}/ ${TARGET}/.agent/"
else
  mkdir -p "${TARGET}/.agent"
  rsync "${RSYNC_FLAGS[@]}" "${KIT_SRC}/" "${TARGET}/.agent/"
  chmod +x "${TARGET}/.agent/scripts/"*.sh 2>/dev/null || true
  echo "Installed: ${TARGET}/.agent/"
fi

if [[ "${NO_SYNC}" -eq 1 ]]; then
  echo "Skipped adapter sync (--no-sync). .agent/ is enough for Antigravity-style tools."
elif [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "[dry-run] (cd ${TARGET} && ${TARGET}/.agent/scripts/sync_kit.sh ${SYNC_FLAGS[*]})"
else
  SYNC="${TARGET}/.agent/scripts/sync_kit.sh"
  if [[ ! -x "${SYNC}" ]]; then
    chmod +x "${SYNC}"
  fi
  if [[ ${#SYNC_FLAGS[@]} -gt 0 ]]; then
    (cd "${TARGET}" && "${SYNC}" "${SYNC_FLAGS[@]}")
  else
    (cd "${TARGET}" && "${SYNC}")
  fi
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "[dry-run] would ensure IDE adapter paths in .gitignore when adapters synced"
elif [[ "${NO_SYNC}" -eq 0 ]]; then
  GITIGNORE="${TARGET}/.gitignore"
  append_gitignore() {
    local entry="$1"
    if [[ -f "${GITIGNORE}" ]]; then
      grep -qxF "${entry}" "${GITIGNORE}" 2>/dev/null && return 0
      if ! grep -q 'Meridian IDE adapters' "${GITIGNORE}" 2>/dev/null; then
        printf '\n# Meridian IDE adapters (local symlinks — regenerate with .agent/scripts/sync_kit.sh)\n' >> "${GITIGNORE}"
      fi
      printf '%s\n' "${entry}" >> "${GITIGNORE}"
      echo "Updated: ${GITIGNORE} (+${entry})"
    else
      cat > "${GITIGNORE}" <<EOF
# Meridian IDE adapters (local symlinks — regenerate with .agent/scripts/sync_kit.sh)
${entry}
EOF
      echo "Created: ${GITIGNORE}"
    fi
  }
  if [[ "${#SYNC_FLAGS[@]}" -eq 0 ]] || [[ "${SYNC_FLAGS[0]:-}" == "--cursor-only" ]]; then
    append_gitignore ".cursor/"
  fi
  if [[ "${#SYNC_FLAGS[@]}" -eq 0 ]] || [[ "${SYNC_FLAGS[0]:-}" == "--claude-only" ]]; then
    append_gitignore ".claude/"
  fi
  if [[ "${#SYNC_FLAGS[@]}" -eq 0 ]] || [[ "${SYNC_FLAGS[0]:-}" == "--codex-only" ]]; then
    append_gitignore ".agents/skills/"
    append_gitignore ".codex/"
    append_gitignore "AGENTS.md"
  fi
  if [[ "${#SYNC_FLAGS[@]}" -eq 0 ]] || [[ "${SYNC_FLAGS[0]:-}" == "--opencode-only" ]]; then
    append_gitignore ".opencode/"
  fi
fi

cat <<EOF

Done.

Next steps:
  1. Open ${TARGET} in your IDE
     - Cursor / Claude Code / Codex / OpenCode: workflows work after adapter sync
     - Antigravity / .agent-native: open project — workflows live in .agent/
  2. If docs/ is missing: /init-meridian
  3. Read .agent/references/guides/agents-help.md or /agents-help
  4. After kit updates: re-run install with --force, or:
        ${TARGET}/.agent/scripts/sync_kit.sh

Note: .cursor/, .claude/, .agents/skills/, .codex/, .opencode/, and AGENTS.md (when symlinked) are local adapters — do not commit them.
      Commit .agent/ if this project owns its kit copy.
      To remove everything later: ${TARGET}/.agent/scripts/uninstall-meridian-kit.sh --all
EOF
