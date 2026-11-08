# Sprint template

> A sprint is a time-boxed delivery unit within a version. It has a clear goal, a defined scope, and a done condition. Do not use it as a task list — use it to communicate intent and measure delivery.

```md
---
id: v1-S1
version: v1
title: Short sprint name
status: planned
goal: "One sentence: what this sprint proves or delivers."
done_when: "Observable condition to close the sprint — not 'all US done'."
stories: [US-0023, US-0024]
---

# v1-S1 — Short sprint name

## Goal

One or two sentences. Why this sprint, why now. What changes for the user or the system by the end of it — not a list of tickets.

## Scope

| US      | Status | MoSCoW | Depends on | Epic    | Description                  |
| ------- | ------ | ------ | ---------- | ------- | ---------------------------- |
| US-0023 | ❌     | Must   | —          | EPIC-03 | Short description of the US  |
| US-0024 | ❌     | Must   | US-0023    | EPIC-03 | Short description of the US  |

## Out of scope for this sprint

What is explicitly deferred — and why (capacity, dependency, priority).

- …

## Retrospective

_(fill at sprint close)_

- What worked:
- What to improve:
- Decisions to log:
```

## Rules

- `id` must match filename (`v1-S1.md`).
- **`stories:` order** in frontmatter is the sprint priority (top first) — no separate priority field on US.
- While `status: active`, do not add US to the sprint without manager request; new work goes to backlog or next sprint (see `scrum-meridian-map.md`).
- Before `status: complete`, manager performs **sprint review** (increment vs `goal` and US Acceptance) then fills **Retrospective**.
- `version` must exist in SQLite (`list versions`).
- `goal` is one measurable sentence — not a copy of the version objective.
- `stories` in frontmatter is the canonical list used by validation; body table is for human readability.
- `status`: `planned` → `active` → `complete`.
- **Retrospective** is mandatory on close — `update-sprint` **rejects** `_(fill at sprint close)_` and empty bullets. Checklist: `sprint-complete/references/retrospective-checklist.md`.
- Do not start a sprint without at least one `ready: true` US.
- Do **not** assign new US to a `complete` sprint — plan a new sprint. Reopening `complete` → `planned`/`active` requires frontmatter `reopen: true` plus a decision log entry (kit rejects silent reopen).
- Do **not** set `complete` while any linked US is still ❌ or 🔶.

## Sprint status

| Value | Meaning |
| ----- | ------- |
| `planned` | Defined, not yet started |
| `active` | In progress — one sprint active per version at a time |
| `complete` | Done when closed — Retrospective filled |
