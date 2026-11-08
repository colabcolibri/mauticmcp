# Usage guide

How to work with Meridian day-to-day. This file covers commands, checks, and the sequence of actions for each situation.

For concepts (what is an epic, how phases work, what `ready` means), read **[start-here.md](./start-here.md)** first.

For **agent groups, who serves what, and the numbered step sequence**, read **[agents-help.md](./agents-help.md)**.

**Kit maintainers:** **[instruction-surfaces.md](../protocol/instruction-surfaces.md)** — every place that carries instructions (kit, extension, mirrors).

**Scrum ↔ Meridian:** [scrum-meridian-map.md](../scrum/scrum-meridian-map.md) (operational). Optional deep dive: [scrum-guide-complete.md](../scrum/scrum-guide-complete.md).

---

## VS Code extension (Meridian Harness)

The **extension** shows and validates `docs/`. **Chat slash commands** create and change them. You are the manager in both.

| You want to… | Use | Not |
| ------------ | --- | --- |
| See kanban, versions, epics | Extension: **Open Board**, **Open Versions**, … **or** `python3 .agent/board` | `/create-us` |
| Copy a newer kit after updating the extension | Status bar `harness A → B` or **Meridian: Upgrade Harness** | Reload only |
| Validate project | Extension: **Validate Project** | Manual edits |
| Bootstrap or change docs | Chat: `/init-meridian`, `/create-us`, `/complete-us`, … | Extension forms (v5) |
| Health check | Chat: `/status` | — |
| Who should run this | Chat: `/deus-ex` | Guessing an `@` worker |

**Reading order in the IDE** (Meridian sidebar → Commands):

1. **How to use** — extension vs chat, workflow vs agent
2. **Start here** — concepts (this file’s companion)
3. **Usage guide** — situations below
4. **Agents & slash commands** — full command map

**Setup:** Install extension → **Install Harness** → `/init-meridian` if no `docs/` → **Open Board**.

---

## Where are you right now?

Run `/status` at any point to get blockers, current state, and suggested next action.

| Situation | What to do |
| --------- | ---------- |
| No `docs/` folder yet | [Start a new project](#start-a-new-project) |
| Existing codebase, no `docs/` | [Migrate an existing project](#migrate-an-existing-project) |
| `docs/` exists, phase docs incomplete | [Work through the phase documents](#work-through-the-phase-documents) |
| UI screens look unstructured or themes clash | [Design flows and themes](#design-flows-and-themes) |
| Architecture approved, no backlog yet | [Build the backlog](#build-the-backlog) |
| Backlog exists, ready to implement | [Implement a user story](#implement-a-user-story) |
| Implementation done, not recorded | [Close a user story](#close-a-user-story) |
| Monorepo with several `docs/` trees | [Multiple Meridian projects](#multiple-meridian-projects) |

---

## Multiple Meridian projects

When the repo has **more than one** folder named exactly `docs` with Meridian content (any layout — root `docs/`, `apps/pkg/docs`, etc.):

1. **Discovery (B)** — tools scan for `docs/` + fingerprint (`00_scope.md` or `us/US-*.md`). `docs-extra` and other names are ignored.
2. **Manifest (A)** — optional `.meridian/projects.json` at kit root: ids, names, `default`, `exclude`, optional `qualitySiege` per product (`kit` | `standard` | `full`).
3. **Active project** — one `docs/` at a time for board, validate, `/status`, and US work. Choice is **saved** (`workspaceState` per kit root + optional VS Code setting `meridian.activeProject`) — reopening Board does **not** ask again.

| Action | How |
| ------ | --- |
| Declare products | Create `.meridian/projects.json` (see `projects-manifest-template.md`) |
| Declare quality tier | `projects[].qualitySiege` or `delivery.json` → `options.qualitySiege` — `quality-profile` CLI; see `agentic-quality-model.md` |
| See which `docs/` is on screen | **Board / Versions / Sprints / Epics** — first toolbar row **Project** (name, path, US count) |
| Switch in IDE | Dropdown in that toolbar, **Meridian: Select Active Project**, or status bar when N>1 |
| First visit only | Quick Pick when N>1 and no saved choice — once; then silent until you switch |
| Validate | `python3 .agent/scripts/validate_meridian.py <package-folder>` — folder that **owns** `docs/`, not always repo root |
| Agent | `/status` lists projects; confirm active `docs/` before creating or editing US |

---

## Start a new project

Run: **`/init-meridian`**

The agent will ask up to 5 questions about the product — problem, users, scope, technology, and security constraints. Answer what you know; leave gaps for later.

What gets created:
- `docs/` folder tree with all phase document stubs
- `docs/00_scope.md` populated with your answers
- `.meridian/meridian.db` bootstrapped via `meridian_delivery.py bootstrap`
- Initial decision via `prepend-decision`

After this, go to [Work through the phase documents](#work-through-the-phase-documents).

---

## Migrate an existing project

Run: **`/init-meridian`** with your codebase open in the IDE.

The agent reads the codebase first — package files, folder structure, README, any existing docs. Then it asks only what it could not infer.

What gets created:

- Same `docs/` tree as a new project, but phase documents are populated from the code — not blank
- **`docs/inventory/as-is.md`** — transitional map of existing capabilities (table with evidence, confidence, epic candidates)
- Every inference marked as an assumption for your review

### Migration sequence (existing codebase)

```
/init-meridian → review inventory → approve phase docs → epics (+ optional v0) → US for new work only
```

| Step | You do | Result |
| ---- | ------ | ------ |
| 1 | Run `/init-meridian` | `docs/inventory/as-is.md` + draft phase docs |
| 2 | Review inventory table — fix confidence and gaps | Validated as-is map |
| 3 | Promote rows into `00_scope`, `05_architecture`, etc. | Phase docs reflect reality |
| 4 | Approve `05_architecture` (human) | Backlog gate unlocked |
| 5 | `/create-epic` for major existing capabilities; optional **`v0`** baseline version | Epics `complete` where already shipped — **no retroactive US** |
| 6 | `/create-version` **v1**+ and `/create-us` | Forward work only |
| 7 | Archive or delete `docs/inventory/as-is.md` | Single source of truth in phase docs |

After step 2, review `docs/00_scope.md` and `docs/05_architecture.md` — correct anything the agent got wrong, then follow the same path as a new project.

---

## Work through the phase documents

Phase documents must be completed in order. Each one unlocks the next.

```
00_scope → 01_tech_stack → 02_security → 03_user_types
         → 04_principles → 05_architecture (gate)
         → 06_database → 07_api_contracts → 08_environments
```

### Working on a phase document

1. Run `/status` to see which document is next and what is blocking it.
2. Open one document per conversation — do not mix documents.
3. Ask the agent to draft, fill gaps, or review a specific section.
4. Use specialized commands when available:
   - **`/architecture`** — draft or review `05_architecture.md`
   - **`/security-pass`** — draft or review `02_security.md`
   - **`/design-pass`**, **`/design-flow`**, **`/design-theme`** — `09` contract, journeys, theme/type (UI products)
5. When a document is ready, **you** set `status: review` in the frontmatter.
6. After your review, **you** set `status: approved`. The agent never sets `approved`.

### The architecture gate

`05_architecture.md` must be `approved` before you can create epics, versions, or user stories. If `/status` shows the backlog is blocked, this is almost always why.

### Decisions

Any significant decision made while working on a document — technology choice, architectural tradeoff, security posture — should be logged:

- Run **`/update-decisions-log`** — agent uses `prepend-decision` (run `date` first).
- Never edit existing entries.

## Design flows and themes

UI products need more than a token table. The owner is always `design-system-owner` — extra skills, not a new agent.

| Pain | Command | Lands in `09` |
| ---- | ------- | ------------- |
| Screens without a journey; missing empty/error; desktop IA on phone | `/design-flow` | § Screen flows + what changes at each breakpoint |
| Broken dark mode, one-off hex, four body sizes | `/design-theme` | § Theme modes + type ramp (one size per role) |
| Stack, components, showcase | `/design-pass` / `/design-showcase` | Rest of `09` |
| Live UI vs contract | `/design-review` | Report |

Run flow and theme **before** treating `09` as ready to approve. Code still goes through `/implement-us`.

---

## Build the backlog

**Gate:** `docs/05_architecture.md` must be `approved`.

### Sequence

Create in this order — each one is required before the next:

1. **Epic** — a product capability: `/create-epic`
2. **Version** — a release that groups epics: `/create-version`
3. **Sprint** *(optional but recommended)* — a time-boxed unit within a version: `/plan-sprint`
4. **User story** — an executable task: `/create-us`

### Create a user story

Run: **`/create-us`**

The agent will ask what user, what action, and what slice. It creates the file with Intent (Why + Where) filled and Plan drafted. The story is saved with `ready: false` — it is not ready to implement yet.

After creating, run **`/review-us US-XXXX`** to get a quality audit of the story before refining it.

### Refine a user story

Run: **`/refine-us US-XXXX`** (`story-maker`)

This is the step that cooks the Plan. The agent:
- Writes the **Approach** (minimum 2 explanatory bullets — the technical direction)
- Sets exact architecture section references
- Writes concrete test steps under Planned
- Leaves `ready: false`

Then run **`/review-us US-XXXX`** (`story-checker`) to attest DoR. That is the only command that sets `ready: true`.

A story without `ready: true` cannot be implemented.

### Sprint priority and scope

- Order of work in a sprint = `stories: [US-…]` in the sprint frontmatter (first = highest priority).
- While a sprint is `active`, new requests go to the backlog or the next sprint — not silently appended mid-sprint unless you decide and log it.
- Close a sprint with **Retrospective** filled and sprint review — run **`/complete-sprint vX-SY`**, not only a manual status edit.

### Bugs and spikes

- **Bug:** create a US with fix acceptance (or fix inside the current US if introduced this session). No `docs/bugs/` folder.
- **Spike:** US with timebox in Notes and knowledge outcome → decision log; no production deliverable required.

Details: [scrum-meridian-map.md](../scrum/scrum-meridian-map.md).

### After backlog changes

Board refreshes when `.meridian/meridian.db` changes (extension webview, or kit HTML SSE after `python3 .agent/board`) and after any `meridian_delivery.py` upsert (`board_snapshots`).

**Column model:** the board does not store column ids in SQLite. 📋 **Backlog** = `status: ❌` and `ready: false` (after `/create-us`); 📌 **Todo** = same status with `ready: true` (after `/review-us` DoR attest) and `in_progress` false; 🔨 **Doing** = `in_progress` true; **Partial** = `status: 🔶` and not in progress; **Frozen** / **Deprecated** = `🧊` / `🚫` with toolbar toggles. Agents edit `status`, `ready`, and `in_progress` only.

---

## Investigate how something works

Use when you need to understand existing code **without** implementing or rewriting phase docs.

1. `/investigate how does {feature} work?` — default depth `medium`
2. Optional: `/investigate path:src/auth/ quick` — narrow scope
3. Optional: `/investigate US-0042` — limit to US Plan scope
4. Hand off per report: `/refine-us`, `/architecture`, spike US, or `/update-decisions-log`

**Not** for full brownfield baseline (`/document-project`) or security audit (`/security-review`).

---

## Reconcile backlog gaps

Use when docs, inventory, or delivery SQLite show work that never became a user story.

1. `/survey-backlog` or `/survey-backlog report` — gap matrix only (default).
2. Optional scope: `/survey-backlog EPIC-03`, `/survey-backlog inventory-only`.
3. After you approve gap ids: `/survey-backlog apply GAP-001 GAP-002` or `/survey-backlog apply EPIC-03`.
4. Hand off: `/refine-us` for thin Plans, then `/review-us`.

**Not** for ad-hoc features (`/create-us` with `@story-maker`) or phase doc-only audits (`/audit-docs`).

Typical after `/document-project` or before `/complete-epic`.

---

## Implement a user story

### Choose the story

Pick a Must story with `ready: true` and no pending `depends_on`. Run `/status` if unsure.

If Plan is thin because you do not know how the code works yet: run `/investigate` first, then `/refine-us`, then `/implement-us`.

One US per implementation session. Do not mix stories in one conversation.

### Ask the agent to implement

Run: **`/implement-us US-XXXX`**

The workflow gates on `ready: true`, filled Plan, and satisfied `depends_on`, then implements. If blocked, run **`/refine-us US-XXXX`** first.

You can also ask in natural language — the agent must run the same gate before coding:

> "Run `/implement-us US-0017`" or "Implement US-0017 per Acceptance."

### Review the output

- Review the diff in the IDE.
- Run build and tests.
- If partially complete: mark `status: 🔶` with `Missing:` in Acceptance. Do not use `/complete-us` yet.
- If complete with evidence: go to [Close a user story](#close-a-user-story).

---

## Close a user story

Run: **`/complete-us US-XXXX`**

**Before running, confirm:**
- All `depends_on` stories are `✅`
- Acceptance criteria are verifiable with evidence (not just "it works")
- If `tests: required` — tests have been run and passed

**What the agent writes in the story file:**
- `## Record` — real file paths changed, layer summary, executed test output
- Acceptance items checked `[x]`
- Frontmatter: `status: ✅`, `tests_status: done`
- If there was a cross-cutting decision → `prepend-decision`

**After closing:**
- Board snapshot updates automatically on upsert
- Verify the story in the extension board
- Go to [Commit after close](#commit-after-close) — human step; not part of `/complete-us`

---

## Commit after close

Full rules: **`commit-after-us-close.md`** in this folder.

After **`/complete-us`** for one US:

1. Review `git diff` — scope must match `## Record` / `### Files` (one US only).
2. Confirm lint/build and `validate_meridian.py` if `docs/` changed.
3. **You** run `git add` + `git commit` (or ask the agent explicitly: “commita com a mensagem sugerida”).
4. Message: `type(scope): summary (US-XXXX)` — the agent may have written **suggested commit** under `### Executed`.

Agents do **not** commit when marking ✅. Partial work (`🔶`) — no delivery commit until close.

---

## Daily session loop

For experienced users, **`/daily-with-ai`** runs a guided session: checks status, surfaces the right story, and walks through the appropriate workflow.

If you prefer to drive manually:
1. `/status` — what is blocked, what is next
2. One focused conversation per concern (document, backlog, implement — not mixed)
3. `/complete-us` when a slice is done
4. **Commit** — one commit per closed US (see [Commit after close](#commit-after-close))

---

## Validate the structure

```bash
python3 .agent/scripts/validate_meridian.py <project-folder>
python3 .agent/scripts/validate_meridian.py <project-folder> --json   # machine-readable
```

Run at the project root. Fix errors before creating US or marking docs `approved`.

---

## Slash command reference

| Command | What it does |
| ------- | ------------ |
| `/init-meridian` | Start or migrate a project — creates `docs/` and governance |
| `/status` | Session start — blockers, current state, next action |
| `/architecture` | Draft or review `05_architecture.md` |
| `/security-pass` | Draft or review `02_security.md` |
| `/create-epic` | New epic row in SQLite |
| `/create-version` | New version row in SQLite |
| `/plan-sprint` | New sprint row in SQLite |
| `/update-decisions-log` | Prepend decision via `prepend-decision` |
| `/complete-sprint vX-SY` | Close sprint — retrospective + status complete |
| `/create-us` | New user story (gates: architecture approved + epic + version exist) |
| `/review-us US-XXXX` | Quality audit — read-only, no changes, no `ready` |
| `/refine-us US-XXXX` | Deepen Plan and Approach — does not set `ready` |
| `/review-us US-XXXX` | Audit or DoR attest — only path that sets `ready: true` |
| `/implement-us US-XXXX` | Gate + implement — requires `ready: true` |
| `/complete-us US-XXXX` | Close story — fills Record, marks `✅` (SQLite upsert) |
| `/investigate` | Read-only code trace — how/where/flow with evidence |
| `/survey-backlog` | Reconcile backlog gaps — report default; `apply` creates US (`ready: false`) |
| `/map-flow` | Interaction flow maps — triage may skip; `light` / `standard` / `product` / `code` modes |
| `/discover` | Product discovery brief — before scope |
| `/document-project` | Brownfield baseline in phase docs — no US |
| `/audit-docs` | Audit phase docs vs code — report only |
| `/daily-with-ai` | Full guided session loop |
| `/agents-help` | Agent groups, slash command groups, numbered steps — open `.agent/references/guides/agents-help.md` |

---

## Things that will not work

- Asking the agent to implement without a `ready: true` story
- Marking `✅` in chat without running `/complete-us` in the files
- Editing delivery markdown/json on disk when `meridian.db` exists
- Creating US before `05_architecture.md` is `approved`
- Mixing document work, backlog work, and implementation in one conversation
- Setting `approved` on a document you did not read
- Using `status: ✅` without a filled `## Record`
- Marking ✅ and moving to the next US without committing the closed slice (unless you batch commits intentionally)
- Letting the agent `git commit` without your explicit request
