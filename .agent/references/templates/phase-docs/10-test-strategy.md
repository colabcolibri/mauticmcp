# Phase doc template — `10_test_strategy.md` (optional)

**Agent:** `quality-owner`  
**Product path:** `docs/10_test_strategy.md`  
**Skip:** no automated test mandate  
**Deepen:** `/test-pass bootstrap` → `/test-review`

---

## What this document is for

`10_test_strategy` defines **how quality is verified**: test pyramid, runners, folder layout, coverage policy, manual QA when needed. US with `tests: required` cite this in Plan. Does not replace Executed evidence in US Record.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init (when tests in scope) | Stub after `01`/`08` name runners |
| CI change | Update runners + pyramid |
| Flaky test policy | Document in pyramid or Gaps |
| Before closing Must US | `/test-review` vs this doc |

## How to complete each section

Record **test stack id** from `test-stack-catalog.md`. Pyramid table: what belongs in unit vs integration vs e2e — percentages are targets, not laws. Runners: tool + config path per layer. Layout: folder conventions. Coverage: tool + threshold or “advisory”. US conventions: link to Meridian `tests` field and Plan refs.

## Depth checklist

- [ ] Stack id set
- [ ] Commands match `08` CI
- [ ] Pyramid explains what must not be e2e-only
- [ ] `test-strategy-checklist.md` passed before `approved`


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Runners in `01` dev tooling
- CI in `08` runs commands listed here

## Related

- `/test-pass`, `/test-review`, `test-strategy` skill
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Test strategy
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [01_tech_stack.md, 04_principles.md, 08_environments.md]
blocks: []
---

# 10 — Test strategy

## Overview

_Products with automated tests — fill via `/test-pass bootstrap` after `01_tech_stack.md` is drafted._

- **Test stack id:** _(from `test-stack-catalog.md`, e.g. `ts-vitest`)_
- **CI:** _(link `08_environments.md` — when tests run)_

## Pyramid

| Level | Scope | Target % of tests |
| ----- | ----- | ----------------- |
| Unit | Pure logic, helpers | |
| Integration | DB, API modules | |
| E2E | Critical user flows | |

## Runners

| Layer | Tool | Config path |
| ----- | ---- | ----------- |
| Unit | | |
| E2E | | |

## Layout

_Document folder and naming conventions._

## Coverage

- **Tool:** _(c8, istanbul, coverage.py, or none)_
- **Threshold:** _(e.g. 80% lines or "advisory only")_
- **Exclusions:** _

## US conventions

- Must US with `tests: required` cite this doc in Plan § Architecture refs
- Planned steps name commands; Executed lists evidence before `/complete-us`

## Manual testing

_When human QA is required — checklist or staging URL._

