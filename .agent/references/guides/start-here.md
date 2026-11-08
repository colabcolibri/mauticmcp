# What is Meridian

Meridian is a protocol for building software with AI. The core idea is simple: **documentation comes before code**. You define what the product is, who it is for, and how it should work — then the AI implements it, guided by those files.

Without this, AI agents hallucinate scope, repeat decisions already made, and produce code that does not match what the team actually agreed on. Meridian solves that by making documentation the source of truth that both humans and agents read.

---

## New project or existing codebase?

**New project:** run `/init-meridian`. The agent asks up to 5 questions about the product and creates the foundation documents from your answers.

**Existing codebase:** run `/init-meridian` with your project open. The agent reads the code first — package files, folder structure, README, any existing docs. Then it asks only what it could not determine. It creates **`docs/inventory/as-is.md`** (a transitional capability map) and populates the phase documents from what it observed, marking every inference as an assumption for you to review and approve. Legacy work is captured in inventory and phase docs — not as retroactive user stories with `✅`.

Either way, the result is the same: a `docs/` folder with the structure below, ready to complete and approve. Existing codebases also get `docs/inventory/` until you promote and archive the as-is map.

---

## The four phases

Every project goes through these four phases in order. Each one unlocks the next — you cannot skip.

### Phase 1 — Project definition

Define what the project is before anything technical. This is about identity, purpose, and audience — not code.

You answer: *What problem does this product solve? Who uses it? What is explicitly out of scope?*

Documents produced:
- `00_scope.md` — what the product is and is not
- `03_user_types.md` — who uses it and how they relate to each other

**Gate:** `00_scope.md` approved → unlocks Phase 2.

### Phase 2 — Structure definition

Once you know what the product is, define how it is built.

Documents produced:
- `01_tech_stack.md` — languages, frameworks, infrastructure
- `02_security.md` — threats, sensitive data, auth model, compliance posture
- `04_principles.md` — code quality and design conventions
- `05_architecture.md` — how the system is divided into modules and services
- `06_database.md` — data model and migrations
- `07_api_contracts.md` — API definitions
- `08_environments.md` — dev, staging, production
- `09_design_system.md` — **UI products only** — visual and UX contract (flows, theme, type, tokens, components, showcase index)

**Gate:** `05_architecture.md` approved → unlocks Phase 3.

**Design operator (UI products):** after `01_tech_stack` is drafted → `/design-pass bootstrap` → `/design-flow` → `/design-theme` → human approves `09` → `/design-showcase` → refine UI US → `/design-review` before close.

**Security operator:** `/security-pass` deepens `02` → after `/implement-us` run `/security-review` (and `/dependency-audit` when deps change) before close on sensitive US.

**Privacy operator:** `/privacy-pass` deepens **LGPD (Brazil)** and **GDPR (EU/EEA)** in `02_security` — separate sections, official regulator URLs (ANPD, EUR-Lex, EDPB). Not legal advice; checklist + doc contract.

**HAR:** when agents need external accounts, payments, or production secrets → `⛔ Ação humana necessária` (P0 in `rules/MERIDIAN.md`).

**Quality operator:** `/test-pass bootstrap` deepens `10_test_strategy.md` when tests in scope → `/test-review` before `/complete-us` on Must US with `tests: required`. Declare optional robust gates per product: `.meridian/projects.json` → `qualitySiege` (`kit` | `standard` | `full`) — see [agentic-quality-model.md](../references/agentic-quality-model.md).

**SEO operator (optional):** `/seo-pass` when public indexable web is in scope → `12_marketing_seo.md`. Skip CLI-only backends.

### Phase 3 — Backlog definition

With the architecture approved, define what will be built and in what order.

Artifacts created in this phase:
- **Epic** — a large product capability (e.g. "User authentication")
- **Version** — a go-live release that groups epics (v1, v2, …)
- **Sprint** — a time-boxed unit within a version with a single goal
- **User story** — an executable task: one slice of one epic

**Gate:** epic and version exist → user stories can be created.

### Phase 4 — Execution

The AI implements each user story, guided by the files from Phase 3. You review the code, then close the story with evidence.

```
/create-us  →  /refine-us  →  /review-us  →  /implement-us  →  /complete-us
```

**No code without `ready: true`** (only `/review-us` attests that). No `✅` without evidence in the Record.

Cycles (discovery → standards → planning → build → attest) are named in [agent-areas.md](../agents/agent-areas.md). They are not extra agents.

If you do not know **which agent** should run, `/deus-ex` (dispatch only). Health numbers stay `/status`.

---

## The document structure

```
docs/
  00_scope.md              Phase 1 — what the product is
  01_tech_stack.md         Phase 2 — technology choices
  02_security.md           Phase 2 — security model
  03_user_types.md         Phase 1 — who uses the product
  04_principles.md         Phase 2 — code and quality conventions
  05_architecture.md       Phase 2 — system structure (gate for backlog)
  architecture/            Phase 2 — optional architecture detail (indexed from 05)
  06_database.md           Phase 2 — data model
  07_api_contracts.md      Phase 2 — API definitions
  08_environments.md       Phase 2 — dev, staging, production
  09_design_system.md      Phase 2 — UI products: design contract (optional for CLI-only)
  11_decisions.md          Always on — decision log index (store: .meridian/meridian.db)
  architecture/            Optional detail indexed from 05
  inventory/as-is.md       Mode B only — transitional; archive after promotion
  discovery/               Optional product discovery artifacts
  ../.meridian/
    delivery.json          Connector profile (commit)
    meridian.db            Delivery backlog — epics, versions, sprints, US (gitignored)
    projects.json          Optional — multi-product repos (several docs/ trees)
```

Delivery templates (US, epic, version shape) live in **`.agent/references/templates/`** — not under `docs/`.

### Several `docs/` folders (monorepo)

One kit (`.agent/`) at the repo root can serve **multiple products**. Each product owns a folder named exactly **`docs`** — anywhere in the tree (`docs`, `apps/pkg/docs`, `cliente-x/docs`, …). Folders like `docs-extra` are **not** Meridian projects.

| Layer | File | Role |
| ----- | ---- | ---- |
| A — manifest | `.meridian/projects.json` | Declares ids, names, `default`, `exclude`, optional `qualitySiege` per product |
| B — discovery | automatic | Finds every `docs/` with Meridian fingerprint (`00_scope` or `us/`) |
| Active project | picker / setting / **saved** | Board, validate, and agent work target one `docs/` at a time; choice persists across tab reopens |
| **Project context strip** | Board + Deliverables toolbar | First row: **Project** — name, `docs/` path, US count; dropdown when N>1 (v2.04) |

Template: `projects-manifest-template.md`. Extension: **Meridian: Select Active Project**; tab titles like `Board — App OSC (42)`.

---

## How the delivery artifacts work

### Epic → Version → Sprint → User Story

Each artifact answers a different question:

- **Epic** — *What capability are we building?* A product capability in user language. May span multiple versions.
- **Version** — *What goes live in this release?* A go-live package that groups epics and stories.
- **Sprint** — *What do we complete this week?* A time box with a single goal and a small set of stories.
- **User story** — *What is the smallest executable slice?* One task, one epic, one version.

```
Epic ──── Version ──── Sprint ──── User Story
│                                  │
└── product capability             └── executable task
```

A story references its epic and version in frontmatter only (`epic: EPIC-02`, `version: v1`). The story body explains its own slice in its own words — never copies from the epic.

### How user stories move

A user story is not a ticket. It is a document with a full lifecycle:

| State | What it means |
| ----- | ------------- |
| `ready: false` | Created — Intent written, Plan drafted. Not ready to implement. |
| `ready: true` | Refined — Plan complete, Approach written, tests concrete. Ready to implement. |
| `status: ✅` | Complete — Record filled, acceptance evidenced, tests done. |

**Forbidden:** `.meridian/drafts/`, `us-*-refine.md`, `us-*-complete.md`, `docs/us/*.md`. “Plan drafted” / “narrative draft” = `ready: false` in **SQLite** (`user_stories`) — not files on disk.

The story has four sections:

- **Intent** — why this slice exists, what the user can do after it, where it sits in the release
- **Plan** — how it will be implemented: Approach bullets, architecture refs, API/DB impact, security notes, test plan
- **Record** — what was actually done: files changed, layers touched, tests executed (filled on close)
- **Boundaries** — what is explicitly out of scope for this story

The **Approach** (inside Plan) is the technical direction for the agent. It is optional at create, but required before `ready: true`. Minimum 2 bullets explaining what changes, where in the codebase, and why.

---

## Document maturity

Phase documents (`00`–`08`, `11`) follow a maturity path. **Only you set `approved`** — the agent sets `draft` or `review`, never `approved`.

| Status | Meaning |
| ------ | ------- |
| `draft` | Being written — not yet ready for human review |
| `review` | Ready for human review — agent proposes, you decide |
| `approved` | Human has reviewed and approved — unlocks dependents |

---

## Scrum and Meridian

Meridian adapts Scrum for **one manager + AI agents** — files as source of truth, no story points, no mandatory Feature layer.

| Need | File |
| ---- | ---- |
| Map artifacts, ceremonies, bugs, spikes | [scrum-meridian-map.md](../scrum/scrum-meridian-map.md) (includes synthesis diagram) |
| Learn Scrum in depth (optional) | [scrum-guide-complete.md](../scrum/scrum-guide-complete.md) — human onboarding only |

Agents use **scrum-meridian-map.md**, not the full Scrum guide, unless you ask otherwise.

---

## What Meridian does not do

- Does not write code without a `ready: true` user story
- Does not mark work done without evidence in the Record
- Does not make scope decisions — you do
- Does not approve its own documents — you do
- Does not manage deploys or CI — those are referenced in docs, not run by Meridian
- Does not `git commit` on its own — after you close a US in docs, you commit (or explicitly ask the agent to). See `commit-after-us-close.md`
- Does not use story points, velocity, or burndown as required fields
- Does not auto-prioritize the backlog — you choose Must US and sprint order

---

## Anatomy of each artifact

Reference section — open when you need the detail on a specific file's fields and sections.

### User Story (US-XXXX)

**Frontmatter:**

| Field | What it is |
| ----- | ---------- |
| `id` | Permanent identifier — `US-0001`. Never changes. |
| `title` | What it delivers, not how. |
| `epic` | Parent epic id (`EPIC-02`). Frontmatter only — no epic text in the body. |
| `version` | Which release this ships in (`v1`). |
| `sprint` | Sprint id when in sprint backlog; empty at create. Required before `ready: true`. |
| `status` | `❌` not started · `🔶` partial · `✅` done · `🧊` frozen · `🚫` deprecated |
| `moscow` | `Must` · `Should` · `Could` · `Won't` |
| `depends_on` | US ids that must be `✅` before this one. |
| `ready` | `false` at create · `true` after refine (requires sprint allocation). Gate for implementation. |
| `done_when` | One measurable sentence — the observable done condition. |
| `tests` | `required` — must pass · `none` — explicitly skipped (document why) |
| `tests_status` | `pending` · `done` · `n/a` |

**Board (extension):** agents write `status` and `ready` only. The IDE derives 📋 Backlog / 📌 Todo from `❌` + `ready`; other columns from `status`, tests fields, and toggles — see [artifact-reference.md](../protocol/artifact-reference.md#user-story-us-xxxx).

**Body sections:**

`## Intent` → `### Acceptance` (verifiable checklist), `### Why` (problem + before/after), `### Where` (position in release, deps, what it unblocks)

`## Plan` → `### Approach` (required at refine — 2+ bullets: what, where in codebase, why), `### Architecture refs`, `### API / DB impact`, `### Security notes`, `### Planned` (numbered test steps)

`## Record` → `### Files` (real paths), `### Backend / Frontend / Scripts / Docs` (layer summary), `### Executed` (actual test output)

`## Boundaries` → `### Out of scope for this story`, `### Notes`

---

### Epic (EPIC-XX)

**Frontmatter:**

| Field | What it is |
| ----- | ---------- |
| `id` | `EPIC-01`, `EPIC-02` — permanent. |
| `title` | Short capability name in user language. |
| `status` | `active` · `complete` · `paused` |
| `versions` | Releases this epic ships across (`[v1, v2]`). |
| `profiles` | User types from `03_user_types.md` this epic serves. |
| `outcome` | One sentence — what is true at product level when done. |

**Body:** `## Capability` (two paragraphs: user problem today → what the product offers after), `## Expected outcome` (observable done signal — not "all US ✅"), `## Out of scope for this epic` (bullets with rationale), `## Notes` (optional)

---

### Version (vX)

**Frontmatter:**

| Field | What it is |
| ----- | ---------- |
| `id` | `v0`, `v1`, `v2` — sequential. |
| `title` | Short release name. |
| `status` | `planned` · `active` · `complete` |
| `outcome` | One sentence — what is true at product level when this ships. |

**Body:** `## Objective` (release theme — not a ticket list), `## Done criteria` (observable close condition), `## Included in this version` (epics/US by id + one line why), `## Explicitly out` (with rationale), `## Go-live checklist`, `## Sprints`

---

### Sprint (vX-SY)

**Frontmatter:**

| Field | What it is |
| ----- | ---------- |
| `id` | `v1-S1` — must match filename. |
| `version` | Parent version — must exist in SQLite (`list versions`). |
| `goal` | One sentence — what this sprint proves or delivers. |
| `done_when` | Observable close condition. |
| `stories` | Canonical US id list (used by validation). Writes `sprint_id` on each US. |
| `status` | `planned` · `active` · `complete` |

**Body:** `## Goal` (why this sprint, why now), `## Scope` (table of US), `## Out of scope for this sprint`, `## Retrospective` (mandatory on close — even one line each)

---

### Decision log (SQLite)

Append-only in `.meridian/meridian.db` (`decisions` table). Every significant decision — technology choice, architecture change, scope adjustment, security posture — is prepended via CLI (newest `entry_index` = 0 per day), never edited in place.

Each entry requires: `time` (`HH:MM` from `date +"%H:%M"`), `title`, `affected_document`, `what_changed`, `why_changed`, `impact`, `responsible`. Calendar day from `date +"%Y-%m-%d"`.

```bash
python3 .agent/scripts/meridian_delivery.py prepend-decision --date "$(date +"%Y-%m-%d")" ...
```

Workflow: **`/update-decisions-log`**. Never invent date or time. Never `Write` on `docs/decisions/*.json`.

---

For commands and step-by-step instructions, open **[usage-guide.md](./usage-guide.md)**.

For **agents, slash command groups, and numbered steps**, open **[agents-help.md](./agents-help.md)**.

**Kit maintainers:** when the protocol changes, open **[instruction-surfaces.md](../protocol/instruction-surfaces.md)** — map of every place that carries instructions (kit, extension, mirrors).
