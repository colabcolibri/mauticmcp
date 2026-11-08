#!/usr/bin/env bash
# DEPRECATED — compatibility shim. Use sync_kit.sh (generates ALL adapters).
#
# Kept so existing installs, docs and muscle memory keep working.
# This shim forwards every argument to the canonical generator.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "note: sync_cursor_kit.sh is deprecated — use ./.agent/scripts/sync_kit.sh (same flags, all IDE adapters)." >&2
exec "${ROOT}/.agent/scripts/sync_kit.sh" "$@"
