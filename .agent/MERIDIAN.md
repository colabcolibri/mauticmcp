# Meridian — protocol manifest

> Define the meridian before writing code.

This file is the **master manifest** for agents: principles, gates, and where to read operational detail.
It is **not** the structural contract for epics, versions, or user stories — use templates for that.

Human onboarding: [`README.md`](../README.md). This file is for agents and advanced reference.

**Protocol version:** 2.0 (US schema: Intent / Plan / Record / Boundaries)

---

## 1. What Meridian is

Meridian is a Scrum-inspired workflow protocol for building software with AI agents.

- **The spec is the project** — code implements what is documented in `docs/`.
- **The person is manager** — agents propose and execute; humans approve direction and ✅.
- **Files are the source of truth** — not chat, not a dashboard, not manually edited board JSON.
- **Minimal surface** — Markdown + JSON only; apps and extensions are optional monitors.

Meridian is not a mesh of autonomous agents. It is a minimal, auditable loop.

---

## 2. Core principles

| # | Principle |
| - | --------- |
| 1 | Documentation precedes product code |
| 2 | Status reflects evidence, not optimism |
| 3 | Decisions live in `.meridian/meridian.db` (`decisions` table). Prepend via `meridian_delivery.py prepend-decision`. **Clock:** run `date +"%Y-%m-%d"` and `date +"%H:%M"` before CLI — workflow `/update-decisions-log` |
| 4 | Board / planning UI reads SQLite (`meridian_db_export --format planning`); `board_snapshots` on upsert — never maintain `docs/kanban/board.json` as source |
| 5 | Simplicity over bureaucracy — use agents/skills for detail, not duplicate specs here |

---

## 3. Rule priority (agents)

```txt
P0  .agent/rules/MERIDIAN.md          always-on gates and routing
P1  .agent/MERIDIAN.md (this file)    manifest + phase order
P2  .agent/skills/                    domain + shared skills (procedures)
      + .agent/agents/{agent}/agent.md   persona + skill list
      + references/templates/         artifact structure (canonical)
```

**Do not invent US/epic/version structure from this file alone.** Read `section-contracts.md` and the full template before Write.

---

## 4. Kit layout

See `.agent/ARCHITECTURE.md` for the full map. Minimum:

```txt
.agent/
  MERIDIAN.md              ← this manifest
  rules/MERIDIAN.md        ← P0 always-on
  ARCHITECTURE.md          ← kit structure
  agents/                  ← {slug}/agent.md + references/ → skills/
  skills/                  ← all procedures (invoke /skill-name)
  references/templates/    ← INDEX, section-contracts, us-template, …
  scripts/
    validate_meridian.py
    migrate_us_v2_structure.py   # one-off US schema migration
    sync_kit.sh

docs/                        ← phase docs only (path varies in monorepos)
  00_scope.md … 11_decisions.md
  architecture/  inventory/  discovery/
.meridian/
  delivery.json              ← connector profile (commit)
  meridian.db                ← epics, versions, sprints, US, decisions (gitignored)
  projects.json              ← optional — multi-product monorepos; per-product qualitySiege
```

**Multi-product repos:** one `.agent/` kit root; each Meridian product = one folder named exactly `docs` (any path). `.meridian/projects.json` declares ids, default, exclude; discovery finds unnamed `docs/` trees. **Active project** (saved) selects which tree board/validate/US target. IDE: **Project** toolbar row in Board/Deliverables + **Select Active Project**. Maintainer map: `references/protocol/instruction-surfaces.md` (EPIC-13 checklist). Template: `projects-manifest-template.md`.

**IDE adapters:** edit `.agent/`, run `./.agent/scripts/sync_kit.sh` for all adapters (`.cursor/`, `.claude/`, Codex, `.opencode/`). Do not commit adapter folders. See [IDE_ADAPTERS.md](./IDE_ADAPTERS.md).

---

## 5. Phase documents (`00`–`11`)

### Frontmatter (all phase docs)

```yaml
---
title: Document name
status: draft | review | approved
version: 1.0
updated: YYYY-MM-DD
depends_on: []
blocks: []
---
```

**Maturity:** `draft → review → approved`. Relevant change returns to `review`. Dependents stay at `draft` until predecessors are `approved`.

### Dependency order

```txt
11_decisions.md (stub)             starts day 1; never blocks
00_scope                           unblocks all
01_tech_stack                      → 02, 04, 08
02_security                        → 03, 04
03_user_types                      → 04, 05, 06, 07
04_principles                      → 05
05_architecture                    → 06, 07, 08 + US creation gate
06_database                        → 07
07_api_contracts
08_environments
```

### Required content per document

**Do not duplicate here.** Read:

| Document | Agent | Template / skill |
| -------- | ----- | ---------------- |
| `00_scope.md` | `product-owner` | `init-project` → `doc-templates.md` |
| `01_tech_stack.md` | `technical-writer` | `doc-templates.md` |
| `02_security.md` | `security-champion` | `doc-templates.md` + `security-review` |
| `03_user_types.md` | `technical-writer` | `doc-templates.md` |
| `04_principles.md` | `technical-writer` | `doc-templates.md` |
| `05_architecture.md` | `technical-architect` | `doc-templates.md` + `architecture-folder-guide.md` + `security-review` |
| `06_database.md` | `technical-writer` | `doc-templates.md` |
| `07_api_contracts.md` | `technical-writer` | `doc-templates.md` |
| `08_environments.md` | `technical-writer` | `doc-templates.md` |
| `11_decisions.md` | any | stub + `decision-template.md` |

---

## 6. Delivery artifacts (SQLite)

After `05_architecture` is `approved`:

| Artifact | Store | Create | Close |
| -------- | ----- | ------ | ----- |
| Epic | `epics` table | `/create-epic` | — |
| Version | `versions` table | `/create-version` | go-live checklist |
| Sprint | `sprints` table | `/plan-sprint` | `/complete-sprint` |
| User story | `user_stories` table | `/create-us` | `/complete-us` |
| Decision log | `decisions` table | `/update-decisions-log` | prepend only |
| Board snapshot | `board_snapshots` | auto on upsert | — |

CLI: `python3 .agent/scripts/meridian_delivery.py` — see `sqlite-delivery-operations.md`.

Templates registry: `.agent/references/templates/INDEX.md`  
Canonical edit paths: `TEMPLATE_SOURCES.md`  
Prose quality: `writing-guide.md`  
Fixed headings: `section-contracts.md`  
Lifecycle: `lifecycle.md`

---

## 7. User stories — schema v2

US body uses **four phase groups** (validated by script + monitor):

```txt
## Intent       → Acceptance, Why, Where
## Plan         → Approach (optional at create, **required at refine**), Architecture refs, API/DB, Security, Related decisions, Planned
## Record       → Files, Backend, Frontend, Scripts/Docs, Executed
## Boundaries   → Out of scope for this story, Notes
```

Full template: `us-template.md`. Do not use flat `## Acceptance`, `## Context & constraints`, or `## Technical implementation` — legacy format.

### Frontmatter (required)

`id`, `title`, `epic`, `version`, `status`, `moscow`, `depends_on`, `done_when`, `tests`, `tests_status`

Strict US also require `ready: true | false`.

### Status rules

| Symbol | Meaning |
| ------ | ------- |
| ❌ | Not started |
| 🔶 | Partial — **Missing:** required in Intent/Acceptance |
| ✅ | Done — evidence + filled Record when applicable |
| 🧊 | Frozen for this version |
| 🚫 | Deprecated — won't implement (superseded or cancelled) |

Board columns **Backlog** and **Todo** are not stored in SQLite: the extension derives 📋 Backlog / 📌 Todo from `status: ❌` plus `ready` (`false` → Backlog, `true` → Todo). Partial, Tests, Done, Frozen, and Deprecated follow `status`, `tests`, and toggles as in `docs/05_architecture.md`. Agents set `status` and `ready` — not board header labels.

- `✅` requires proven acceptance; if `tests: required`, then `tests_status: done`, Plan/Planned `[x]`, Record/Executed filled.
- `✅` requires `## Record` with real paths in `### Files` (skill `us-complete`).
- US may leave ❌ only when all `depends_on` are ✅.

### US lifecycle

```txt
/create-us     → Intent + Plan draft, ready: false   (forbidden: draft files — SQLite only)
/refine-us     → deepen Plan + Approach (required), ready stays false
/review-us     → DoR attest (ready: true) or report-only
implement      → developer gate: ready + Plan filled
/complete-us   → Record + status ✅
/sync-board    → removed in v11 (board reads SQLite)
commit (human) → after close + board sync; one commit per US — see commit-after-us-close.md
```

Agents: `story-maker` (create/refine), `story-checker` (review/complete).

---

## 8. Board JSON

Schema: `board-schema.md`. Generated from US frontmatter — never maintained by hand as source of truth.

```bash
python3 .agent/scripts/validate_meridian.py <project-folder>
python3 .agent/scripts/validate_meridian.py <project-folder> --json
```

### Decision log

- Table `decisions` in `.meridian/meridian.db` — prepend via `meridian_delivery.py prepend-decision`
- **Before CLI:** run `date +"%Y-%m-%d"` (`--date`) and `date +"%H:%M"` (`--time`)
- Workflow `/update-decisions-log` + skill `update-decisions-log`; templates `decision-template.md`, `decision-schema.md`
- Never edit old decision rows; legacy `docs/decisions/*.json` is import-only (purge after migrate)
- US Plan **Related decisions** cites the log as `YYYY-MM-DD — title` after `prepend-decision` (not a parallel store)

---

## 9. Agents and routing

| Need | Agent | Entry |
| ---- | ----- | ----- |
| Allocate station | `deus-ex` | `/deus-ex` |
| Status / gates | `scrum-master` | `/status` |
| Discovery, scope, epic | `product-owner` | `/discover`, `/create-epic` |
| UX research | `ux-researcher` | `/ux-pass` |
| Phase docs `01`,`04`,`11` | `technical-writer` | `/document-project`, `/audit-docs` |
| `07` API contracts | `technical-architect` | `/api-pass` |
| `02` security | `security-champion` | `/security-pass`, `/security-review`, `/dependency-audit`, `/payment-pass` |
| `05` architecture | `technical-architect` | `/architecture`, `/architecture mcp`, `/api-pass` |
| `06` database | `data-engineer` | `/database-pass` |
| `08` environments | `devops-engineer` | `/release-pass` (human push/deploy) |
| `09` design | `design-system-owner` | `/design-pass`, `/design-flow`, `/design-theme`, `/i18n-pass`, `/a11y-pass`, `/design-showcase`, `/design-review` |
| Quality / tests | `quality-owner` | `/test-pass`, `/test-review`, `/perf-pass` |
| Versions / sprints | `sprint-planner` | `/create-version`, `/plan-sprint`, `/complete-sprint` |
| US cook | `story-maker` | `/create-us`, `/refine-us` |
| US attest | `story-checker` | `/review-us`, `/complete-us` |
| US implement | `developer` | `/implement-us` (requires `ready: true`) |
| Decisions | any relevant agent | `/update-decisions-log` |
| Auto-pick | `meridian-routing` skill | — |

Always announce: `🤖 Applying knowledge from @[agent-slug] (CallSign)...` — see [agent-personas.md](references/agents/agent-personas.md).

### Agent may

Create drafts, suggest decisions, implement approved US, run tests, update docs, regenerate board, report blockers.

### Agent must not

- Start product code without `/implement-us` gate or US `ready: true`
- Create US before `05_architecture` approved and epic/version exist
- Mark `✅` without evidence or filled Record
- Write to `docs/decisions/` or edit old decision rows
- Prepend decisions without running `date +"%Y-%m-%d"` and `date +"%H:%M"` first (use `prepend-decision` CLI)
- Edit `board.json` as primary source
- Expose secrets or run destructive commands without confirmation

If documentation is missing, report: what blocks, why, smallest fix, offer draft.

---

## 10. Bootstrap

Use workflow `/init-meridian` and skill `init-project`. Two modes:

**Mode A — New project:** agent interviews user (up to 5 questions), creates `docs/` from answers.

**Mode B — Existing codebase:** agent reads code first, creates `docs/inventory/as-is.md` (capability table with evidence), infers scope and tech, asks only what is unclear, populates phase docs from inventory + observations. All inferences marked as assumptions for human review. No retroactive US with `✅`; optional baseline version `v0` for pre-Meridian epics.

Both modes:

1. Create `docs/` phase docs + bootstrap SQLite (`meridian_delivery.py bootstrap`)
2. Stub `11_decisions.md`; initial decision via `prepend-decision`
3. Draft `00_scope.md`; populated, not blank
4. Follow dependency order for remaining phase docs
5. Epics/versions after architecture approved (SQLite bootstrap)
6. `.gitignore` before secrets or dependencies land

Human guide: `.agent/references/INDEX.md` → `guides/start-here.md`  
Operational guide: `.agent/references/guides/usage-guide.md`  
Maintainer map (where to edit instructions): `.agent/references/protocol/instruction-surfaces.md`  
Agents & commands (groups, steps): `.agent/references/guides/agents-help.md`  
Scrum ↔ Meridian (agents + managers): `.agent/references/scrum/scrum-meridian-map.md`  
Scrum textbook (human only, optional): `.agent/references/scrum/scrum-guide-complete.md`

---

## 11. Pre-code checklist

Before product code for a US:

- [ ] `05_architecture` approved; epic and version exist
- [ ] Target US exists; `ready: true`
- [ ] `## Plan` filled (no placeholders); Architecture refs readable
- [ ] `depends_on` US all ✅
- [ ] Acceptance observable; tests planned if required

If any fail → `/refine-us` or phase doc work first.

---

## 12. Done checklist

Delivery is done when:

- Code matches US acceptance
- Build/lint/test passed as applicable
- Intent/Acceptance marked `[x]` (or `🔶` + Missing:)
- `## Record` filled (Files + layers + Executed when tests required)
- `tests_status: done` when `tests: required`
- `status: ✅` in frontmatter
- `board_snapshots` updated on upsert (no manual board.json)
- Cross-cutting changes in decision log (skill `update-decisions-log` + real clock)

**Repository (human, after the above):** one git commit per closed US — code + SQLite delivery state in scope. Agents suggest message on close; they do not commit unless the manager explicitly asks. See `.agent/references/protocol/commit-after-us-close.md`.

---

## 13. Management tools

Meridian works without any app. Optional tools (e.g. the VS Code extension in `app-visual-studio/`) read the same folder — they are not the source of truth.

---

## 14. Operational phrase

> If it is not documented, it is not ready to be implemented.  
> If it has been implemented, it must be reflected in the documentation.  
> If an agent worked, the process manager must be able to audit what changed.
