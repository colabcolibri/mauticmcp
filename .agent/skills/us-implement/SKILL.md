---
name: us-implement
description: Gates implementation of a Meridian user story — verifies ready true, Plan, deps and architecture refs before product code. Use with /implement-us US-XXXX.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Implement user story (Meridian)

> **v11:** load US from SQLite — never assume `docs/us/*.md` on disk.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `references/implement-gate-checklist.md` | **Mandatory** |
| `.agent/references/templates/code-quality-at-us-time.md` | **Mandatory** |
| Target US | `meridian_delivery.py show US-XXXX --full` |
| `docs/05_architecture.md`, `docs/04_principles.md` | Refs + quality |

## Delivery commands

```bash
python3 .agent/scripts/meridian_delivery.py implement-gate US-0115
python3 .agent/scripts/meridian_delivery.py implement-gate US-0115 --json
python3 .agent/scripts/meridian_delivery.py show US-0115 --full
python3 .agent/scripts/meridian_delivery.py set-in-progress US-0115 --in-progress true
```

## Hard gate

| Check | Requirement |
| ----------- | --------- |
| Architecture | `05_architecture.md` `approved` |
| US row | exists in SQLite |
| `ready` | `true` |
| Dependencies | all `depends_on` at `✅` |

If gate fails → **no product code**; recommend `/refine-us` then `/review-us`.

## Procedure

1. Run `implement-gate`; read checklist + US `--full`.
2. If passed → `set-in-progress US-XXXX --in-progress true` then implement per Acceptance and Planned (DRY/SRP).
3. Close with `us-complete` / `/complete-us` — not in same turn unless asked. That path clears `in_progress`.

## Output

```txt
Implement gate:
US: US-XXXX
Result: PASS | BLOCKED
Blockers:
Next: code | /refine-us US-XXXX
```
