# Phase doc template — `00_scope.md`

**Agent:** `product-owner` (content) + `technical-writer` (structure)  
**Product path:** `docs/00_scope.md`  
**Init:** read this guide → fill [Document stub](#document-stub) → copy to `docs/00_scope.md`  
**Blocks:** `01_tech_stack.md`, `04_principles.md`, `05_architecture.md`

---

## What this document is for

`00_scope` is the **product charter**. It answers: what problem we solve, for whom, what ships in the first release, and what we deliberately postpone. Every other phase doc and every user story must trace back here. If work cannot be justified by scope, it does not belong in the backlog.

This is not a marketing page. It is the agreement between the manager and the team (human + AI) about **value** and **boundaries**.

## When to write it

| Moment | What you do |
| ------ | ----------- |
| `/init-meridian` Mode A | Draft from interview answers. Do not invent users or features not discussed. |
| `/init-meridian` Mode B | Draft from README + `docs/inventory/as-is.md` + code. Mark every inference. |
| After `/discover` | Merge insights from `docs/discovery/product-brief.md` into scope sections. |
| Scope argument in chat | Update scope first; then log decision; then adjust epics/US. |

## How to complete each section (stub)

Work through the stub **in order**. Replace every `_(…)_` placeholder with real prose or table rows.

### Name and description

Write the **product name** as a concrete noun (not “the platform”). Follow with 2–4 sentences: what the product is, where it runs (browser, extension, CLI, mobile), and who operates it day to day. A reader who has never seen the repo should understand the product category.

### Problem it solves

Use three labeled parts — do not merge into one vague paragraph:

- **Before:** describe the pain in the user’s workflow today. Use their language, not “we need a dashboard”.
- **After:** describe the observable outcome when the product works. Still user language.
- **Why now:** regulation, scale, cost, competitive pressure, or “greenfield hypothesis” — why this release matters now.

If you cannot write Before/After without guessing, add a row to **Open questions** instead of inventing.

### Who it is for

Fill the table with at least one **primary** audience. Each row needs role, context, technical level, and primary need. You will expand each row into a full profile in `03_user_types.md` later — names here must match.

### In initial scope (v1)

List **observable capabilities** — what a user can do in a demo. Minimum three bullets for a real product. Each bullet should be testable (“manager can invite user and assign role”) not implementation (“add invite API”).

Prioritize: if everything is P0, nothing is. This section is v1 only.

### Out of initial scope

List deferrals the manager agreed to. Minimum two items when possible. This section prevents scope creep and wrong US. Be specific (“native iOS app”, “multi-tenant billing”, “SSO with Okta”) not vague (“nice-to-haves”).

### Known constraints

Table: team size, timeline, legal, technology locks. Write `None documented` only if the manager confirmed there are none. Constraints here explain later trade-offs in `01` and `05`.

### Assumptions

Every guess gets a row: assumption text, confidence (high/medium/low), and how to validate. Low confidence assumptions should become **Open questions** unless the manager accepts the risk.

### Open questions

Unresolved interview items. Empty table only when the manager explicitly confirmed “no open questions”. Never leave silent `TBD` in other sections — move unknowns here.

### Current product state (Mode B only)

One summary paragraph of what already ships. Table: capability, evidence path (file, route, screenshot), confidence. Do not create retroactive US for legacy work — inventory + scope capture reality.

## Depth checklist (before `approved`)

- [ ] Problem section has Before, After, Why now — each with substance
- [ ] In scope bullets are user-observable, not tech tasks
- [ ] Out of scope is non-empty and manager-aligned
- [ ] Every primary audience in Who it is for appears again in `03_user_types` (after drafted)
- [ ] No technology stack list dominating scope (belongs in `01`)
- [ ] Open questions or assumptions cover all remaining uncertainty


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- `01_tech_stack` surfaces must support users and in-scope capabilities
- `05_architecture` must not introduce major capabilities not in scope
- Epics in SQLite should cite outcomes that appear in In scope

## Gate

Human sets `status: approved`. Scope alone does not unlock US — need `05_architecture` approved. Material scope change → decision log + set dependent docs to `review`.

## Related

- `init-interview-guide.md`, `writing-guide.md`, `as-is-inventory-template.md` (Mode B)
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Scope
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: []
blocks: [01_tech_stack.md, 04_principles.md, 05_architecture.md]
---

# 00 — Scope

## Name and description

**Product name:** _(concrete noun — not “the app”)_

_(2–4 sentences: what the product is, where it runs, who operates it. Example: “A B2B web app for warehouse managers to track inbound shipments. Runs in the browser; mobile is out of scope for v1.”)_

## Problem it solves

**Before:** _(pain in user language — what breaks today?)_

**After:** _(observable outcome when the product works — not a feature list)_

**Why now:** _(trigger: regulation, scale, team pain, market — or “greenfield” with hypothesis)_

## Who it is for

| Audience | Role / context | Technical level | Primary need |
| -------- | -------------- | --------------- | ------------ |
| Primary | | | |
| Secondary | _(optional)_ | | |

_Detail each profile in `03_user_types.md` after security draft._

## In initial scope (v1)

Observable capabilities — what users can **do**, not how we build it:

1. _(e.g. “Manager can invite a teammate and assign a role”)_
2. _
3. _

## Out of initial scope

Explicit deferrals — prevents creep and wrong US:

- _(e.g. “Native mobile apps”)_
- _(e.g. “Multi-tenant billing”)_
- _

## Known constraints

| Type | Constraint | Impact |
| ---- | ---------- | ------ |
| Team | | |
| Timeline | | |
| Legal / compliance | | |
| Technology | | |

_Use `None documented` only when truly none — otherwise list assumptions._

## Assumptions

| # | Assumption | Confidence | Validate by |
| - | ---------- | ---------- | ----------- |
| 1 | | high / medium / low | |

## Open questions

| # | Question | Owner | Target date |
| - | -------- | ----- | ----------- |
| 1 | | manager | |

_Empty only if manager confirmed all interview answers._

## Current product state (Mode B only)

_(Existing codebase migration — delete this section for greenfield.)_

**Summary:** _(one paragraph: what already ships today)_

| Capability | Evidence (path / route) | Confidence |
| ---------- | ----------------------- | ---------- |
| | | high / medium / low |

## Gate

Human sets `status: approved` before deepening `01_tech_stack` and security work.

