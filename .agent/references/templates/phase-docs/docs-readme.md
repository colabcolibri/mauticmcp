# Phase doc template — `docs/README.md`

**Agent:** `technical-writer`  
**Product path:** `docs/README.md`

---

## What this document is for

`docs/README.md` is the **human entry point** to the phase doc tree: what each file is for, current status, how Meridian delivery works (SQLite), and the approval order. It is not a duplicate of the repo root README — link upward when both exist.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Copy stub; set product name and draft statuses |
| Any phase doc `approved` | Update status column in table |
| Delivery model change | Update delivery artifacts section |

## How to complete

One paragraph product summary aligned with `00_scope`. Phase table: keep statuses current. “How to work” section: dependency order and slash commands — agents read this for orientation.

## Depth checklist

- [ ] All phase docs `00`–`11` listed
- [ ] SQLite delivery mentioned (not `docs/us/`)
- [ ] Validate command documented


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Related

- `phase-docs/00-scope.md`, `MERIDIAN.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

# [Project name]

_(One paragraph: what this product is and who maintains these docs.)_

## Phase documents

| Doc | Status | Description |
| --- | ------ | ----------- |
| [00_scope.md](00_scope.md) | draft | Product scope and boundaries |
| [01_tech_stack.md](01_tech_stack.md) | draft | Languages, frameworks, infrastructure |
| [02_security.md](02_security.md) | draft | Threat model, auth, data, secrets |
| [03_user_types.md](03_user_types.md) | draft | Profiles and permissions |
| [04_principles.md](04_principles.md) | draft | DRY, layers, Definition of Done |
| [05_architecture.md](05_architecture.md) | draft | System structure — **gate for backlog** |
| [06_database.md](06_database.md) | draft | Schema and migrations |
| [07_api_contracts.md](07_api_contracts.md) | draft | API / CLI / extension contracts |
| [08_environments.md](08_environments.md) | draft | Local setup, CI, env vars |
| [09_design_system.md](09_design_system.md) | _(optional)_ | UI contract — UI products only |
| [10_test_strategy.md](10_test_strategy.md) | _(optional)_ | Test pyramid — when tests in scope |
| [11_decisions.md](11_decisions.md) | draft | Decision log rules (entries in SQLite) |

## Delivery artifacts

| Artifact | Location | Role |
| -------- | -------- | ---- |
| Epics, versions, sprints, user stories | `.meridian/meridian.db` | Canonical delivery (v11) |
| Decision log entries | `.meridian/meridian.db` → `decisions` | Prepend only |
| Kit templates | `.agent/references/templates/` | Agent contracts — do not copy into `docs/templates/` |

## How to work

1. Approve phase docs in dependency order: `00` → `01` → `02` → `03` → `04` → **`05`** → detail docs.
2. UI products: `/design-pass bootstrap` on `09` after `01` is drafted.
3. Tested products: `/test-pass bootstrap` on `10` after `01` / `08` are drafted.
4. After `05_architecture` is **`approved`**: `/create-epic` → `/create-version` → `/plan-sprint` → `/create-us`.
5. Per US: `/refine-us` → `/implement-us` → `/complete-us` (human commit).
6. Validate: `python3 .agent/scripts/validate_meridian.py .`

## Meridian kit (if present)

| Resource | Path |
| -------- | ---- |
| Protocol | `.agent/MERIDIAN.md` |
| Agents help | `.agent/references/guides/agents-help.md` |
| Start here | `.agent/references/guides/start-here.md` |

