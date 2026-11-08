---
name: backlog-reconcile
description: Reconciles docs, inventory, SQLite delivery, and optional code samples against the backlog — reports missing work and optionally creates gap-derived US (ready false). Use with /survey-backlog after 05 approved.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Backlog reconcile (Meridian)

> Finds **traceability debt**: promised or evident work with no `US-XXXX`. **`report`** = read-only matrix. **`apply`** = create US only for manager-approved gap rows.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/survey-backlog` | Gap report and optional gap-derived US drafts |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/reconcile-checklist.md` | **Mandatory** — every run |
| `.agent/skills/us-create/SKILL.md` + `writing-guide.md` + `us-template.md` | **`apply`** mode only |
| `docs/05_architecture.md` | Gate + arch context |
| `docs/inventory/as-is.md` | Brownfield |
| Phase docs with § Gaps | Dimensions 1–2 |

## When to trigger

- `/survey-backlog` or "US faltando", "buraco no backlog", "criar US pendentes", "reconciliar backlog"
- After `/document-project` or before `/complete-epic` when US count looks thin
- After `/audit-docs` when report lists US-sized fixes

**Do not** use for:

- Ad-hoc feature ideas → `/create-us` (`story-maker`)
- Deep code traces → `/investigate` (`code-investigator`)
- Phase doc quality only → `/audit-docs` (no US)
- Setting `ready` or closing US → `story-checker`

---

## Gate

| Check | Action |
| ----- | ------ |
| `05_architecture` not `approved` | **Stop** — report blocker; no `apply` |
| No epics/versions | **Stop** — handoff `product-owner` / `sprint-planner` |
| `apply` without manager approval | **Stop** at report; list gap ids |

---

## Modes (`$ARGUMENTS`)

| Mode | Args example | Behavior |
| ---- | ------------ | -------- |
| `report` | *(default)*, `report`, `EPIC-03` | Checklist only; no SQLite writes |
| `apply` | `apply`, `apply GAP-001 GAP-003`, `apply EPIC-02` | Create US for approved gaps in scope |
| Scope | `inventory-only`, `docs-only`, `v2` | Restrict dimensions |

Parse: if `apply` appears anywhere, mode is `apply` (still require explicit manager approval in the same conversation unless gap ids are listed).

---

## Procedure

### Phase 0 — frame

1. Active product `docs/` (monorepo: `.meridian/projects.json`).
2. `meridian_delivery.py counts` + list epics/US in scope.
3. Confirm `05` approved via frontmatter.
4. Load `references/reconcile-checklist.md`.

### Phase 1 — collect gaps

Walk dimensions 1–5 per checklist. Build table:

| Gap id | Source | Evidence | Suggested epic | Suggested title | Action report/apply/skip |

Mark `skip` when an open US already covers the slice (cite `US-XXXX`).

### Phase 2 — report

Emit output block (below). If mode is `report`, stop after handoff.

### Phase 3 — apply

1. Re-read approved gap rows only.
2. For each: follow `us-create` — `create-us` + `update-us` heredoc, `ready: false`.
3. Link gap evidence in **### Why** and **### Where**.
4. Never set `ready: true`.
5. Optional `prepend-decision` per checklist.

### Phase 4 — handoff

- Thin Plan → `story-maker` `/refine-us`
- DoR → `story-checker` `/review-us`
- New epic needed → `product-owner` `/create-epic`
- Code fact for Plan → `code-investigator` `/investigate`

---

## Forbidden

| Forbidden | Why |
| --------- | --- |
| `ready: true`, `/review-us` attest | `story-checker` |
| `status: ✅`, `/complete-us` | `story-checker` |
| Product code | `developer` |
| Create `EPIC-XX` | `product-owner` |
| US without evidence row | Integrity |
| Intent-led greenfield US | `story-maker` `/create-us` |
| MoSCoW / sprint reorder alone | Human manager |

---

## Output

```txt
Escopo:
Modo: report | apply
Fontes lidas:
Resumo: N gaps | P0 … | P1 … | P2 …

| Gap id | Evidência | Epic | Título sugerido | Ação |
| ------ | --------- | ---- | --------------- | ---- |

US criadas:
Deixado para humano:
Próximo agente:
Próximo comando:
Handoff:
  station: survey-backlog
  agent: backlog-surveyor
  done:
  blocker:
  next agent:
  next command:
  artifact id:
```
