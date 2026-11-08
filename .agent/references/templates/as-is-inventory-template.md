# As-is inventory template (Mode B migration only)

> **Transitional artifact** — not a phase doc (`00`–`11`). Created during `/init-meridian` Mode B; absorbed into approved phase docs and epics, then archived or deleted.

Read this template before creating `docs/inventory/as-is.md`.

---

## When to use

| Situation | Action |
| --------- | ------ |
| New project (Mode A) | **Do not create** — no legacy to map |
| Existing codebase (Mode B) | **Create** during init; human reviews before promoting |
| `05_architecture` approved | Promote rows to phase docs + epics; archive inventory |

---

## File location

```txt
docs/inventory/as-is.md
```

Optional archive after promotion: `docs/inventory/archive/as-is-YYYY-MM-DD.md`

---

## Template body

```md
---
title: As-is inventory
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
purpose: transitional
promoted_to: []
---

# As-is inventory

> Map of what already exists in the codebase **before** Meridian backlog work.
> Rows with **high** confidence feed `00_scope`, `05_architecture`, and epic candidates.
> **Do not** create retroactive user stories with `✅` from this file.

## How to read this file

| Column | Meaning |
| ------ | ------- |
| Capability | User-facing behavior in plain language — not folder names |
| Evidence | Paths, routes, models, or docs that prove it exists |
| Confidence | `high` · `medium` · `low` — how sure the inference is |
| Epic candidate | Suggested `EPIC-XX` id or `—` if too small |
| Gaps | Unknown behavior, missing tests, tech debt, or questions for the manager |

## Capabilities

| Capability | Evidence | Confidence | Epic candidate | Gaps |
| ---------- | -------- | ---------- | -------------- | ---- |
| … | `src/…`, route `…` | high | EPIC-01 | … |

## Assumptions (needs human review)

- …

## Promotion checklist

When a row is validated, move knowledge out of this file:

- [ ] Product behavior → `docs/00_scope.md` (in scope / current state)
- [ ] Users / roles → `docs/03_user_types.md`
- [ ] System structure → `docs/05_architecture.md`
- [ ] Data model → `docs/06_database.md`
- [ ] APIs → `docs/07_api_contracts.md`
- [ ] Large capability block → epic in SQLite (`epic-create`; `status: complete` if already shipped)
- [ ] Past technical choice → `prepend-decision`

After `05_architecture` is **approved**, archive or delete this file. Do not maintain two sources of truth.

## Baseline version (optional)

If the product already shipped significant work before Meridian:

1. Create epics from **high** confidence rows (no retroactive US).
2. Create version `v0` in SQLite — baseline release documenting pre-Meridian state.
3. Mark completed epics `status: complete` and list them under v0.
4. New work starts in `v1`+ as normal user stories.

Do **not** mark v0 epics done via fake `✅` user stories.

## Open questions

- …
```

---

## Agent rules

| Do | Don't |
| -- | ----- |
| Infer from code, README, issues | Invent features not evidenced |
| Mark every inference in Assumptions | Set `confidence: high` without evidence |
| Suggest epic ids only | Create epics, versions, or US during init |
| Keep one table row per capability | List `src/` tree as inventory |

---

## Lifecycle

```txt
Codebase → docs/inventory/as-is.md (draft)
         → human review
         → phase docs + epics (+ optional v0)
         → 05_architecture approved
         → archive inventory
         → US only for forward work (v1+)
```
