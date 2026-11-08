# Refine checklist — US ready for implementation

Use after `/us-create`, before any product code. Mark `ready: true` only when **every** required row passes **and** `/us-review` attests (`story-checker`). `/us-refine` must leave `ready: false`.

Read `writing-guide.md` — match the refine golden example before checking rows below.

---

## Required sections

| # | Check | Pass when |
| - | ----- | --------- |
| 1 | Preamble | **I want** = verb + object in user language; **so that** = outcome they feel |
| 2 | Intent / `### Why` | 2+ sentences: gap today → what this US changes |
| 3 | Intent / `### Where` | 2+ sentences: deps, unblocks, scope |
| 4 | Plan / `### Approach` | **required** — ≥2 bullets, full sentences; no bare filenames |
| 5 | Plan / Architecture refs | `docs/05…` or `docs/architecture/*` — § **exact heading** |
| 6 | Plan / API / DB impact | `_n/a_` + phrase **or** named endpoint/table |
| 7 | Intent / Acceptance | ≥2 items; observable; `[ ]` not `[x]` until close |
| 8 | Plan / Planned | Numbered manual steps + exact test command when `tests: required` |
| 9 | `done_when` | One measurable sentence |
| 10 | Epic link | `epic:` in frontmatter only — body explains slice |
| 11 | Sprint | `sprint: vX-SY`; sprint `planned`/`active` before `ready: true` |
| 12 | INVEST | Small slice; testable; deps justified |
| 13 | DRY / SRP | Reuse named in Approach; **Out of scope** real |
| 14 | Quality profile | `tests: required` + profile ≥ `standard` → AC maps to test layer |
| 15 | Related decisions | `_n/a_` or `YYYY-MM-DD — title` when scope/arch/security shifts |

See `.agent/references/scrum/scrum-meridian-map.md` for bugs/spikes (no extra artifact types).

## UI stories (when Acceptance is visual)

- [ ] Plan Architecture refs include `09` § Screen flows (or named flow) after `/design-flow`
- [ ] Theme/type: cite `09` § Colors / Typography — no “pick a nice blue”
- [ ] Responsive: what happens at the narrow breakpoint is in Approach, not only “must be responsive”
- [ ] Multi-step UI (dialog, branches, empty/error): Plan cites `/map-flow` artifact or mermaid — **or** one-line skip rationale from triage; simple single-screen US do not require a map

## Approach — good vs bad

| Bad | Good |
| --- | ---- |
| `- KanbanView.tsx` | `- Update KanbanView to filter stories before column split so v0 cards never render when v1 is selected.` |
| `- see architecture` | `- Reuse monitor filter context so Deliverables (US-0025) shares version state without a second source of truth.` |
| `- implement filter` | `- Add VersionFilterBar above columns; persist selection in MonitorVersionFilterContext when switching tabs.` |

---

## Placeholder patterns (fail until replaced)

- `_(fill in` / `_(pending)_` / `§ [section name` / `path/to/…`
- `add when implementation scope is known`
- `verify acceptance criteria end-to-end` without numbered steps
- Approach bullets under 6 words with no verb

---

## Frontmatter

```yaml
ready: false   # /create-us — narrative draft (`ready` flag in SQLite; not a draft file)
ready: true    # /refine-us — implement allowed
```

**Forbidden:** `.meridian/drafts/`, `us-*-refine.md` — persist with `update-us` (stdin) only.

---

## What refine does **not** do

- Does not fill `## Record` (that's `/complete-us`)
- Does not mark acceptance `[x]` or `status: ✅`
- Does not write product code
