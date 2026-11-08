# Phase doc template — `01_tech_stack.md`

**Agent:** `technical-writer`  
**Product path:** `docs/01_tech_stack.md`  
**Depends on:** `00_scope.md` | **Blocks:** `02`, `04`, `08`, optional `09`/`10`

---

## What this document is for

`01_tech_stack` records **how the product is built**: languages, frameworks, persistence, hosting, and developer tooling. Security (`02`), coding principles (`04`), environments (`08`), and optional design/test docs all depend on choices made here.

Each choice needs a **rationale** tied to scope — not a dependency dump from `package.json` without explanation.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init (after `00` draft) | First fill from interview or repo evidence |
| Before `/security-pass bootstrap` | Surfaces and data layer must be stable enough for `02` |
| Stack change (new framework, DB migration) | Set `review`, update all tables, log decision, re-check `02`/`05`/`08` |
| `/audit-docs` | Verify tables still match repo files |

## How to complete each section

### Summary

One paragraph linking stack to **users and surfaces** from `00_scope`. Example structure: “Warehouse managers use a Next.js web app on Vercel; data in Postgres; background jobs on … because …”

### Runtime and language

Name primary language, runtime version if pinned, package manager. **Rationale column is mandatory** — why this runtime for this product.

### Application surfaces

One row per real surface: web, API, CLI, extension, mobile. Use `_n/a_` only with a short reason. This table drives `02` auth rows and `09` creation.

### Data layer

Database, ORM, migration tool, file storage, cache. If there is no database, explain persistence (files, external API only) in prose — do not leave blank.

### Infrastructure and hosting

Where each environment runs. Local is always documented. Cloud provider and region if applicable.

### Dev tooling

Linter, formatter, test runners, bundler, CI config **with file paths** (Mode B: verify paths exist).

### UI / test stack signals

Check boxes and record stack ids for `/design-pass` and `/test-pass` bootstrap. Uncheck and skip `09`/`10` files when not applicable.

### Discarded alternatives

At init: optional. Before `approved`: list 1–3 rejected options and why (e.g. “MongoDB — team lacks ops experience; Postgres sufficient”).

### Evidence (Mode B)

Map claims to files: `package.json`, `Dockerfile`, `.github/workflows/ci.yml`.

### Gaps / open questions

Unknown versions, unset hosting, undecided test runner — numbered table with what blocks.

## Depth checklist

- [ ] Every technology row has rationale, not only name
- [ ] Surfaces match what scope promises users can access
- [ ] Data layer consistent with what code or plan expects
- [ ] CI path cited if tests exist
- [ ] Discarded alternatives filled before `approved`


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- `02_security` auth surfaces ⊆ application surfaces here
- `08_environments` commands use package manager named here
- `05_architecture` components use technologies listed here

## Gate

`approved` when stack matches reality (Mode B) or signed interview (Mode A). Changes after approval trigger `review` on `02`, `05`, `08`.

## Related

- `/security-pass bootstrap`, `/architecture`, `phase-docs/02-security.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Tech Stack
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [00_scope.md]
blocks: [02_security.md, 04_principles.md, 08_environments.md, 09_design_system.md, 10_test_strategy.md]
---

# 01 — Tech stack

## Summary

_One paragraph tying stack choices to `00_scope` — who uses the product and where it runs._

## Runtime and language

| Layer | Technology | Version (if pinned) | Rationale |
| ----- | ---------- | ------------------- | --------- |
| Primary language | | | |
| Runtime | Node / Python / Go / … | | |
| Package manager | npm / pnpm / poetry / … | | |

## Application surfaces

| Surface | Framework / host | Path in repo | Notes |
| ------- | ---------------- | ------------ | ----- |
| Web app | | | |
| API / backend | | | |
| CLI | | _n/a_ | |
| Extension / desktop | | _n/a_ | |
| Mobile | | _n/a_ | |

## Data layer

| Concern | Choice | Config / path | Notes |
| ------- | ------ | ------------- | ----- |
| Primary database | Postgres / SQLite / none | | |
| ORM / client | | | |
| Migrations | tool + folder | | |
| File / object storage | S3 / local / none | | |
| Cache | Redis / in-memory / none | | |

_Detail schema in `06_database.md` after architecture draft._

## Infrastructure and hosting

| Environment | Provider | Region | Notes |
| ----------- | -------- | ------ | ----- |
| Local | developer machine | — | |
| Staging | | | |
| Production | | | |

## Dev tooling

| Tool | Purpose | Config file |
| ---- | ------- | ----------- |
| Bundler / compiler | | |
| Linter | | |
| Formatter | | |
| Unit test runner | | |
| E2E runner | | |
| CI | GitHub Actions / … | `.github/workflows/…` |

## UI stack signals (if applicable)

_Checkboxes for downstream stubs:_

- [ ] Web UI → create `09_design_system.md`; run `/design-pass bootstrap`
- [ ] Automated tests in scope → create `10_test_strategy.md`; run `/test-pass bootstrap`

**Suggested UI stack id:** _(from `ui-stack-catalog.md`, e.g. `ts-shadcn`)_

**Suggested test stack id:** _(from `test-stack-catalog.md`, e.g. `ts-vitest`)_

## Discarded alternatives

| Option | Why rejected |
| ------ | ------------ |
| | |

_Optional at init; required before `status: approved`._

## Evidence (Mode B)

| Claim | Source file |
| ----- | ----------- |
| | `package.json` / `pyproject.toml` / … |

## Gaps / open questions

| # | Unknown | Blocker for |
| - | ------- | ----------- |
| 1 | | `02_security` / `05_architecture` |

## Gate

Human approves before `/security-pass bootstrap` and architecture work.

