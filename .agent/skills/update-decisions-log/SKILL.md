---
name: update-decisions-log
description: Prepends a project decision to SQLite (.meridian/meridian.db decisions table). Use when scope, stack, security, architecture, versions or acceptance criteria change.
allowed-tools: Read, Glob, Grep, Bash, Edit
---

# Update decisions log

## Selective reading

| File | When to read |
| ------- | ---------- |
| `references/decision-template.md` | Field checklist for each entry |
| `references/decision-schema.md` | Validation rules |

## When to register

Change in: scope, stack, security, users, epics, versions, architecture, database, API, environments, acceptance, agent governance.

## Prerequisites

- `meridian.db` exists — run `python3 .agent/scripts/meridian_delivery.py bootstrap` if missing.
- **Never** `Write` on `docs/decisions/*.json` when SQLite delivery is active.

## Procedure

1. Determine today's date (`YYYY-MM-DD`) — **run** `date +"%Y-%m-%d"` at project root (never guess).
2. **Capture real clock time** — **run** `date +"%H:%M"` (24h, local). Use for `--time`. Do **not** round or invent.
3. Prepend via CLI (newest entry = `entry_index` 0 for that date):

```bash
python3 .agent/scripts/meridian_delivery.py prepend-decision \
  --date "$(date +"%Y-%m-%d")" \
  --time "$(date +"%H:%M")" \
  --title "Objective decision title" \
  --affected-document "docs/05_architecture.md" \
  --what-changed "factual description of delta" \
  --why-changed "context and motivation" \
  --impact "affected docs; mark review" \
  --responsible "manager or role"
```

Alternative: single entry JSON file → `--from-json /tmp/decision-entry.json`.

4. If an `approved` phase doc changed → set that doc `status: review` + mention in `--impact`.
5. When the change ties to a US → add under Plan **Related decisions**: `YYYY-MM-DD — <title>` (same day/title as the log entry). Log first, then cite in the US via `update-us`.
6. **Never** edit or delete old decision rows (append-only by prepend only).

## Read back

```bash
python3 .agent/scripts/meridian_delivery.py list decisions
python3 .agent/scripts/meridian_delivery.py show-decisions --date YYYY-MM-DD
python3 .agent/scripts/meridian_delivery.py show-decisions --date YYYY-MM-DD --json
```

## Archiving

History lives in SQLite (`decisions` table). Do not compact or rewrite old `entry_index` values except via `prepend-decision` (which shifts indices for the same day).

## Output

```txt
Decision logged:
Store: .meridian/meridian.db (decisions)
Date: YYYY-MM-DD
Clock used: HH:MM (from date command)
Affected document:
Docs moved to review:
Follow-up:
```
