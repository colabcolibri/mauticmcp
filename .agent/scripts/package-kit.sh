#!/usr/bin/env bash
# Build a distributable Meridian kit tarball ( .agent only — no app-desktop ).
#
# Usage (from meridian monorepo root):
#   ./.agent/scripts/package-kit.sh
#   KIT_VERSION=1.0.0 ./.agent/scripts/package-kit.sh
#   ./.agent/scripts/package-kit.sh --out /tmp/releases
#
# Output:
#   dist/meridian-kit-<version>/
#   dist/meridian-kit-<version>.tar.gz

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_SRC="${REPO_ROOT}/.agent"
OUT_BASE="${REPO_ROOT}/dist"
VERSION="${KIT_VERSION:-}"

usage() {
  cat <<'EOF'
package-kit.sh — build meridian-kit tarball for distribution

Usage:
  package-kit.sh [options]

Options:
  --out DIR     Output directory (default: <repo>/dist)
  -h, --help    This help

Environment:
  KIT_VERSION   Release version (default: git describe or 0.0.0-dev)

The tarball includes: README.md, LICENSE, VERSION, install.sh, .agent/
It does NOT include app-desktop, app-visual-studio, or extension VSIX.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      OUT_BASE="$2"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "${VERSION}" ]]; then
  if git -C "${REPO_ROOT}" describe --tags --match 'kit-v*' --always 2>/dev/null | grep -qv '^kit-v'; then
    VERSION="$(git -C "${REPO_ROOT}" describe --tags --match 'kit-v*' 2>/dev/null | sed 's/^kit-v//')"
  elif git -C "${REPO_ROOT}" describe --tags --always 2>/dev/null; then
    VERSION="$(git -C "${REPO_ROOT}" describe --tags --always | tr '/' '-')"
  else
    VERSION="0.0.0-dev"
  fi
fi

STAGE="${OUT_BASE}/meridian-kit-${VERSION}"
ARCHIVE="${OUT_BASE}/meridian-kit-${VERSION}.tar.gz"

echo "Meridian kit package"
echo "  Version: ${VERSION}"
echo "  Source:  ${AGENT_SRC}"
echo "  Stage:   ${STAGE}"
echo ""

rm -rf "${STAGE}"
mkdir -p "${STAGE}"

rsync -a \
  --exclude '.DS_Store' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  "${AGENT_SRC}/" "${STAGE}/.agent/"

cp "${REPO_ROOT}/LICENSE" "${STAGE}/LICENSE"
cp "${AGENT_SRC}/KIT_README.md" "${STAGE}/README.md"
echo "${VERSION}" > "${STAGE}/VERSION"

cat > "${STAGE}/install.sh" <<'INSTALL'
#!/usr/bin/env bash
# Meridian kit — bootstrap installer (distribution package root).
# Usage: ./install.sh [options] [TARGET_DIR]
set -euo pipefail
KIT_DIR="$(cd "$(dirname "$0")" && pwd)"
export MERIDIAN_KIT_SRC="${KIT_DIR}/.agent"
exec "${KIT_DIR}/.agent/scripts/install-meridian-kit.sh" "$@"
INSTALL
chmod +x "${STAGE}/install.sh"
chmod +x "${STAGE}/.agent/scripts/"*.sh

mkdir -p "${OUT_BASE}"
tar -czf "${ARCHIVE}" -C "${OUT_BASE}" "meridian-kit-${VERSION}"

echo "Created:"
echo "  ${STAGE}/"
echo "  ${ARCHIVE}"
echo ""
echo "Publish ${ARCHIVE} as a GitHub Release asset (tag: kit-v${VERSION})."
echo "Users: tar -xzf meridian-kit-${VERSION}.tar.gz && cd meridian-kit-${VERSION} && ./install.sh /path/to/project"
