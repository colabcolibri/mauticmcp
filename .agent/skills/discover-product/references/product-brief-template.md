# Product brief template — `docs/discovery/product-brief.md`

> **PO artifact.** Read `discovery-folder-guide.md` before Write. This file explores intent; **`00_scope.md`** is the approved contract for agents.

```md
---
title: Product brief
status: draft
updated: YYYY-MM-DD
---

# Product brief

## Problem

What pain exists today — specific, not "build an app". Who feels it?

## Vision / outcome

One or two sentences: what becomes possible when this product succeeds (user outcome, not tech).

## Users and jobs

| User type | Job to be done | Notes |
| --------- | -------------- | ----- |
| … | … | assumption | evidence |

Feeds `03_user_types.md` on promotion.

## Value

Why this product vs status quo — for the primary user and for the business (if applicable).

## In scope (candidates)

Testable boundaries for the **first meaningful version** — still draft until promoted to `00_scope.md`.

## Out of scope (candidates)

Non-empty. What we are **not** building now.

## Constraints

Time, budget, platform, compliance, legacy systems.

## Assumptions

Explicit guesses — mark `(assumption)` when not validated.

## Epic candidates

Names only — capabilities to explore in `/create-epic` **after** scope direction is clear. No `EPIC-XX` ids here.

- …

## Evidence (existing codebase)

Mode B only — link inventory rows, paths, or docs that support inferences. Empty for greenfield.

## Open questions

Honest unknowns for the manager to resolve before approving scope.

## Promotion notes

_(Optional)_ What to copy into `00_scope.md` and `03_user_types.md` when manager runs promote or `/discover promote`.
```

## Section contract

| Section | Required at first draft |
| ------- | ------------------------ |
| Problem | yes |
| Users and jobs | yes — at least one row |
| Out of scope (candidates) | yes — non-empty |
| Epic candidates | optional until direction stable |
| Evidence | Mode B only |

## Status

| Value | Meaning |
| ----- | ------- |
| `draft` | Discovery in progress |
| `ready for scope` | Manager may promote to `00_scope` / `03_user_types` or ask product-owner to review |
