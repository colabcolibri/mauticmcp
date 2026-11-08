# Artifact reference

> Field-level detail for delivery and phase artifacts. For concepts and gates, read [start-here.md](../guides/start-here.md). For commands, use [agents-help.md](../guides/agents-help.md).

---

## User story (US-XXXX)

**Frontmatter (SQLite / export):**

| Field | What it is |
| ----- | ---------- |
| `id` | Permanent identifier — `US-0001`. Never changes. |
| `title` | What it delivers, not how. |
| `epic` | Parent epic id (`EPIC-02`). Frontmatter only — no epic text in the body. |
| `version` | Which release this ships in (`v1`). |
| `sprint` | Sprint id (`v1-S1`) when allocated; omit or empty on product backlog. Column `sprint_id` in SQLite. Required before `ready: true`. |
| `status` | `❌` not started · `🔶` partial · `✅` done · `🧊` frozen · `🚫` deprecated |
| `moscow` | `Must` · `Should` · `Could` · `Won't` |
| `depends_on` | US ids that must be `✅` before this one. |
| `ready` | `false` at create · `true` after refine. Gate for implementation (requires `sprint` + planned/active sprint). |
| `done_when` | One measurable sentence — the observable done condition. |
| `tests` | `required` — must pass · `none` — explicitly skipped (document why) |
| `tests_status` | `pending` · `done` · `n/a` |

**Board (extension, not stored in SQLite):** columns are computed when you open **Open Board**. Set `status`, `ready`, and `in_progress` — never a “column” field. 📋 Backlog = `status: ❌` and `ready: false`; 📌 Todo = `status: ❌`, `ready: true`, `in_progress` false; 🔨 Doing = `in_progress` true with `❌` or `🔶`; 🔶 Partial = `status: 🔶` and not in progress; 🧊 / 🚫 = same symbols in `status`; Tests column when `tests: required` and `tests_status: pending`. Header emojis are UI labels only.

**Body sections:**

- `## Intent` → `### Acceptance`, `### Why`, `### Where`
- `## Plan` → `### Approach` (required at refine), `### Architecture refs`, `### API / DB impact`, `### Security notes`, `### Planned`
- `## Record` → `### Files`, layer summaries, `### Executed`
- `## Boundaries` → `### Out of scope for this story`, `### Notes`

Templates: `.agent/references/templates/us-template.md`, `writing-guide.md`.

---

## Epic (EPIC-XX)

| Field | What it is |
| ----- | ---------- |
| `id` | `EPIC-01`, `EPIC-02` — permanent. |
| `title` | Short capability name in user language. |
| `status` | `active` · `complete` · `paused` |
| `versions` | Releases this epic ships across (`[v1, v2]`). |
| `profiles` | User types from `03_user_types.md` this epic serves. |
| `outcome` | One sentence — what is true at product level when done. |

**Body:** `## Capability`, `## Expected outcome`, `## Out of scope for this epic`, `## Notes`

---

## Version (vX)

| Field | What it is |
| ----- | ---------- |
| `id` | `v0`, `v1`, `v2` — sequential. |
| `title` | Short release name. |
| `status` | `planned` · `active` · `complete` |
| `outcome` | One sentence — what is true when this ships. |

**Body:** `## Objective`, `## Done criteria`, `## Included in this version`, `## Explicitly out`, `## Go-live checklist`, `## Sprints`

---

## Sprint (vX-SY)

| Field | What it is |
| ----- | ---------- |
| `id` | `v1-S1` — primary key in `sprints` table. |
| `version` | Parent version id (FK). |
| `goal` | One sentence — what this sprint proves or delivers. |
| `done_when` | Observable close condition. |
| `stories` | US id list (order = priority). On save, sets each US `sprint_id` and rebuilds `sprint_stories` / `stories_json`. |
| `status` | `planned` · `active` · `complete` |

**Body:** `## Goal`, `## Scope`, `## Out of scope for this sprint`, `## Retrospective` (mandatory on close)

---

## Decision log (`decisions/YYYY-MM-DD.json`)

Append-only. Prepend entries; never edit old rows.

Each entry: `time` (`HH:MM`), `title`, `affected_document`, `what_changed`, `why_changed`, `impact`, `responsible`.

Workflow: **`/update-decisions-log`**. Agent must run `date +"%Y-%m-%d"` and `date +"%H:%M"` before Write.

---

## Phase documents (`00`–`11`)

Maturity: `draft` → `review` → `approved` (human sets `approved` only).

Section contracts: `.agent/skills/init-project/references/doc-templates.md` + `phase-docs/*.md`.
