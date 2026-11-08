---
name: us-complete
description: Closes a Meridian user story in SQLite after implementation — adds Record and status without deleting refined content. Use when marking US done or after /implement-us.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Complete user story (Meridian)

> **P0:** `/complete-us` is **additive** — add Record + mark acceptance + status. **Never** rebuild the US from a template.  
> **Forbidden:** helper `.py` scripts; copying `us-template.md` or `implementation-template.md` into CLI.

## Selective reading (order matters)

| # | File | When to read |
| - | ---- | ------------ |
| 1 | `references/close-us-contract.md` | **Mandatory first** — additive-only rules |
| 2 | Target US | `meridian_delivery.py show US-XXXX --full` — **mandatory before any write** |
| 3 | `references/implementation-template.md` | Record **heading examples only** — not the US body |
| 4 | `.agent/references/templates/section-contracts.md` | Plan **unchanged** on close |
| 5 | `.agent/references/protocol/commit-after-us-close.md` | Suggested commit only |

**Do not read `us-template.md` for close body** — that template is for `/create-us` and `/refine-us` only.

## Delivery commands

```bash
python3 .agent/scripts/meridian_delivery.py show US-0115 --full   # 1 — mandatory
python3 .agent/scripts/meridian_delivery.py patch-record US-0115 <<'EOF'   # 2 — preferred
---
status: ✅
tests_status: done
---
## Record

### Files

- `path/to/file.ts` — what changed

### Backend

- _n/a_

### Frontend

- _n/a_

### Scripts / Docs

- _n/a_

### Executed

- `pnpm test` — passed
- **suggested commit:** `feat(scope): summary (US-0115)`

## Intent

### Acceptance

- [x] criterion one (unchanged text — only checkbox)
- [x] criterion two
EOF
python3 .agent/scripts/meridian_delivery.py set-summary US-0115 --text "4-8 sentence summary"
python3 .agent/scripts/meridian_delivery.py lifecycle-eligible US-0115
```

**`update-us` fallback:** only when you must edit outside Record. Pipe the **entire** markdown from `show --full` with surgical edits — if the body got shorter, you deleted content.

## Preconditions

| Check | Requirement |
| ----------- | --------- |
| `show --full` | run in this session **before** any persist |
| Dependencies | all `depends_on` at `✅` |
| Evidence | tests/build passed |
| Record | real paths — no template placeholders |
| Preserved | Why, Where, Approach, Architecture refs, Boundaries **unchanged** |

## Procedure

1. Read `close-us-contract.md`.
2. **`show --full`** — this is the document you extend; not `us-template.md`.
3. Inspect `git diff` / test output.
4. **Add** filled `## Record`; flip acceptance `[x]`; mark Planned `[x]` where done; set `tests_status` / `status`.
5. **`patch-record`** (default) — never send only Record to `update-us`.
6. `set-in-progress US-XXXX --in-progress false` (also cleared automatically when status is `✅`).
7. **Never** copy template files into the CLI; never shorten Intent/Plan to stubs.
8. `prepend-decision` + Plan **Related decisions** when protocol/architecture changed.
9. `lifecycle-eligible` — ask manager before container close.

## Output

```txt
US completed:
ID: US-XXXX
Persist: patch-record | update-us (full body)
Preserved Intent/Plan: yes | NO — STOP
Implementation summary:
Files touched:
Decisions logged: yes | no
Suggested commit:
Lifecycle cascade:
Next (human): commit per commit-after-us-close.md
```
