# Phase doc template — `04_principles.md`

**Agent:** `technical-writer`  
**Product path:** `docs/04_principles.md`  
**Read at:** `/refine-us`, `/implement-us`  
**Depends on:** `01`, `02`, `03` | **Blocks:** `05`

---

## What this document is for

`04_principles` defines **how code is organized and judged** in this product: where logic lives (DRY), layer boundaries (SRP), team Definition of Done, conventions, error handling. Shorter than architecture — **paths and rules**, not component catalogs.

Every US implementation should cite this implicitly via Plan refs to `04_principles`.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Infer layers from repo (Mode B) or agree conventions (Mode A) |
| Before `05` approved | Layer table must match architecture layers |
| New package/folder introduced by epic | Update DRY table; log if structural |
| Repeated US review feedback (“wrong layer”) | Strengthen conventions section |

## How to complete each section

### DRY — where each type of logic lives

For each concern type, name **one** canonical path. If duplicated today, note “(consolidate in US-XXXX)” in Gaps. Include duplication policy: when copy is acceptable temporarily.

### Single responsibility — layers

Minimum three rows. Columns: layer, responsibility, may import from, must not. Must match `05` layer names exactly.

### SOLID

Map only principles that change daily decisions. Skip textbook definitions — one line per principle on **this** codebase.

### Definition of Done

Checklist for **any** US close — align with Meridian (`Record`, tests, reviews). Add product-specific bars (coverage, design review, security review).

### Mandatory conventions

Naming, imports, commit format, language of docs vs code, linter configs with paths.

### Error handling

Per layer: pattern, user-visible shape, logging rules (no secrets in logs).

### Security-aware coding

Bullet rules tying to `02`: server-side authz, validation boundaries.

### Gaps

Uncertain paths marked `(review)` until architect confirms.

## Depth checklist

- [ ] DRY table has real paths, not “domain layer”
- [ ] Layer table ≥3 rows, aligned with `05`
- [ ] DoD checklist usable by `/complete-us`
- [ ] Error handling names API envelope or UI pattern


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Layer names match `05_architecture`
- Test commands in DoD match `10` when exists
- Validation library matches `01` and `07`

## Gate

`approved` before `05` — architect uses layer table as hard constraint.

## Related

- `code-quality-at-us-time.md`, `writing-guide.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Code Principles
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [01_tech_stack.md, 02_security.md, 03_user_types.md]
blocks: [05_architecture.md]
---

# 04 — Principles

_Agents read this at `/refine-us` and `/implement-us` — be specific with paths, not slogans._

## DRY — where each type of logic lives

| Concern | Single source of truth | Path / package |
| ------- | ---------------------- | -------------- |
| Domain rules / business logic | | |
| Validation schemas | | |
| API clients / SDK wrappers | | |
| UI primitives (read-only) | | |
| Composed UI templates | | |
| Constants / enums | | |
| Scripts / CLI | | |

**Duplication policy:** when is copy acceptable vs extract?

## Single responsibility — layers

| Layer | Responsibility | May import from | Must not |
| ----- | -------------- | --------------- | -------- |
| Domain / core | | | UI, HTTP |
| Application / use cases | | | |
| Infrastructure | DB, HTTP, FS | | domain rules |
| UI / presentation | | | direct DB |
| Scripts / kit | | | product shortcuts |

_Align with `05_architecture` § Layers._

## SOLID (project-specific)

| Principle | How we apply it here |
| --------- | -------------------- |
| SRP | _(via layer table)_ |
| OCP | |
| LSP | |
| ISP | |
| DIP | |

_Skip rows that do not apply — do not paste textbook definitions only._

## Definition of Done (team-wide)

A user story is done when:

- [ ] All Acceptance items verified with evidence in `## Record`
- [ ] `tests: required` → `tests_status: done` and commands in Record § Executed
- [ ] No new linter **errors** (warnings documented if accepted)
- [ ] Security-sensitive US → `/security-review` or Plan cites `02_security`
- [ ] UI Must US → Plan cites `09_design_system` when approved
- [ ] Human manager reviewed diff; one commit per US (policy)

## Mandatory conventions

| Area | Rule | Tool / config |
| ---- | ---- | ------------- |
| Naming | | |
| Imports | | |
| Commits | conventional / free | |
| Branching | | |
| Language | pt-BR docs / en code / … | |

## Error handling

| Layer | Pattern | User-visible | Logged |
| ----- | ------- | ------------ | ------ |
| API | envelope shape | message code | stack in dev only |
| UI | toast / inline field | | |
| CLI | exit codes | | |

## Security-aware coding

- Never log secrets or full PII
- Authorization checks on server for every mutating action
- Validate at trust boundaries — see `02_security`

## Gaps / open questions

| # | Topic | Owner |
| - | ----- | ----- |
| 1 | | |

## Gate

Human `approved` before architecture finalization.

