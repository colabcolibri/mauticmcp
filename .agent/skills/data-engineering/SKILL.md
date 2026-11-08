---
name: data-engineering
description: Maintains docs/06_database.md — schema, migrations, retention, access. Use for /database-pass. Not module boundaries (technical-architect) or app code (developer).
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Data engineering (Meridian)

> **Scope:** `docs/06_database.md`. ER overview in `05` stays with `technical-architect`; this skill deepens persistence contract.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/database-pass` | Create/update `06` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/database-checklist.md` | **Mandatory** |
| `docs/05_architecture.md` | Always |
| `docs/02_security.md` | When PII or auth touches data |
| `docs/01_tech_stack.md` | ORM, host, migration tool |
| Target US (`show US-XXXX --full`) | `us-align` |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist pass on entire `06` |
| `bootstrap` | **bootstrap** | Read `05` + `01` → storage model + migration policy stub |
| `US-XXXX` | **us-align** | Load US `--full`; map data Acceptance → `06` sections |

---

## Procedure

```txt
- [ ] Read 05 + 02 + 01
- [ ] database-checklist.md
- [ ] If no 06 → copy stub from phase-docs/06-database.md
- [ ] Migration naming: YYYYMMDDHHMMSS per project rule
- [ ] Recommend /refine-us when Must US lacks data refs in Plan
- [ ] prepend-decision on material schema or retention policy changes
```

## Output

```txt
Mode: full | bootstrap | us-align
06_database status:
Schema sections updated:
Migration policy:
US follow-ups:
Next: human approve 06 | /architecture | /refine-us US-XXXX
```
