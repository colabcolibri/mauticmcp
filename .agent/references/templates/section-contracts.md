# Section contracts — delivery artifacts

> **Source of truth for structure.** Validators mirror this file. **Writing quality** is in `writing-guide.md`.

---

## User story (`us-template.md`) — schema v2

Four phase groups replace flat H2 siblings. No legacy aliases.

### Frontmatter

| Field | Create (`/create-us`) | Strict (has `ready`) |
| ----- | -------------------- | -------------------- |
| `id`, `title`, `epic`, `version`, `status`, `moscow`, `depends_on` | required | required |
| `sprint` | omit or empty (product backlog) | required (`vX-SY`, same `version`, sprint `planned`/`active`) |
| `ready` | `false` | required |
| `done_when`, `tests`, `tests_status` | required | required |

### `##` sections (fixed order)

| # | Section | Phase | Create | Refine | Close |
| - | ------- | ----- | ------ | ------ | ----- |
| 1 | Intent | Why we do this | Acceptance + Why + Where | tighten | mark `[x]` only — **text unchanged** |
| 2 | Plan | How we will do it | Architecture refs + Planned draft | optional Approach + concrete tests | **unchanged** — use `patch-record` on close |
| 3 | Record | What shipped | placeholders | unchanged | Files + layers + Executed |
| 4 | Boundaries | What we skip | Out of scope | optional | optional |

### `###` under Intent

Acceptance · Why · Where

### `###` under Plan

Architecture refs · API / DB impact · Security notes · Related decisions · Planned

**Optional:** Approach — add on `/refine-us`; not required for validation.

### `###` under Record

Files · Backend · Frontend · Scripts / Docs · Executed

### `###` under Boundaries

Out of scope for this story · Notes

### Close (`/complete-us`) — additive only

Read `close-us-contract.md`. Source of truth = `show US-XXXX --full`. **Add** Record; flip acceptance `[x]`; set status. **Never** copy `us-template.md` or `implementation-template.md` as the full body.

---

## Epic (`epic-template.md`)

| `##` section | Required |
| ------------ | -------- |
| Capability | yes — prose (see writing-guide) |
| Expected outcome | yes — prose |
| Out of scope for this epic | yes |
| Notes | recommended |

---

## Version (`version-template.md`)

| `##` section | Required |
| ------------ | -------- |
| Objective | yes (alias: `Goal`) — prose |
| Done criteria | yes — prose |
| Included in this version | yes |
| Explicitly out | yes |
| Go-live checklist | yes |

---

## Validation

```bash
python3 .agent/scripts/validate_meridian.py <project-folder>
```

Monitor uses the same structural rules in TypeScript.
