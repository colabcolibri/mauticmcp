# Kit v2 migration (1.x → 2.0)

> **Superseded for procedures (kit v3):** domain procedures are canonical in `.agent/skills/` again — see [kit-v3-migration.md](./kit-v3-migration.md). `agents/{slug}/references/` are symlinks; prefer **`@agent`** over slash workflows.

> **Audience:** managers upgrading an existing project from harness **1.1.x** to **2.0.0**.

## Summary

Kit v2 is a **breaking** layout change. Behavior (workflows, SQLite delivery, phase docs) is unchanged; **paths and folder shape** are not.

| Area | 1.x | 2.0 |
| ---- | --- | --- |
| Agent persona | `.agent/agents/{slug}.md` | `.agent/agents/{slug}/agent.md` |
| Domain procedures | `.agent/skills/{pass}/` | `.agent/agents/{owner}/references/{pass}/` |
| Shared skills | many under `.agent/skills/` | only 5 cross-station skills |
| Human references | flat under `.agent/references/` | `guides/`, `protocol/`, `agents/`, `scrum/`, `templates/` |
| Cursor adapter | `.cursor/agents/{slug}.md` → flat file | symlink → `agents/{slug}/agent.md` |

## Upgrade steps

1. Install **Meridian Harness 2.0.0** (Marketplace) and reload.
2. **Meridian: Upgrade Harness** on each product folder (backs up previous kit to `agent-backup/harness-<timestamp>.zip` before overwrite).
3. Run `./.agent/scripts/sync_kit.sh` to refresh `.cursor/`, `.claude/`, Codex, OpenCode adapters.
4. **Meridian: Validate Project** — fix any WARNs; with kit repo: `python3 .agent/scripts/validate_meridian.py . --strict-kit-md`.
5. Update **custom** docs, rules, or scripts that cited old paths (see below).

No migration is required for `.meridian/meridian.db` or `docs/` phase files.

## Path rewrites (if you forked the kit)

```txt
.agent/agents/design-system-owner.md
  → .agent/agents/design-system-owner/agent.md

.agent/skills/design-system/
  → .agent/agents/design-system-owner/references/design-system/

.agent/references/agents-help.md
  → .agent/references/guides/agents-help.md

.agent/references/station-references.md
  → .agent/references/protocol/station-references.md
```

## Invocation (unchanged for humans)

- Still type `/create-us`, `/status`, … — workflows route to `@agent`.
- Still `@design-system-owner` in chat — Cursor reads the flat symlink; canonical file is `agent.md` inside the station folder.

## Rollback

Restore from `agent-backup/harness-*` (zip or folder) created by Upgrade Harness, or reinstall extension **1.1.57** and upgrade again to the older bundle.

See also: [station-references.md](./station-references.md), [INDEX.md](../INDEX.md).
