# Agent station map — maker vs checker

> **Live roster:** eighteen actors. Call signs: [agent-personas.md](./agent-personas.md). `deus-ex` (Machina) dispatches (does not cook). `story-maker` (Penelope) cooks intent-led `/create-us` + `/refine-us`. `backlog-surveyor` (Metis) cooks gap-led `/survey-backlog` apply. `story-checker` (Argus) attests `/review-us` (`ready`) + `/complete-us`.

v11 rename history stays in [plans/agent-roster-and-workflow-v11.md](../plans/agent-roster-and-workflow-v11.md). This file is the **production-line contract**. **Areas:** [agent-areas.md](./agent-areas.md).

## Cook versus attest

| Object | Cook (writes) | Attest (may not be the cook) |
| ------ | ------------- | ----------------------------- |
| Product recipe (scope, epic) | `product-owner` (Clio) | Human `approved` on phase docs |
| User types / personas | `ux-researcher` (Iris) + `product-owner` | Human `approved` on `03` |
| Phase docs `01`/`04`/`11` | `technical-writer` (Calliope) | Human `approved` |
| `07` API contracts | `technical-architect` (Daedalus) | Human `approved` |
| `02` standard | `security-champion` (Janus) | Human `approved`; `/security-review` attests **code** |
| `05` | `technical-architect` (Daedalus) | Human `approved` |
| `06` | `data-engineer` (Mnemosyne) | Human `approved` |
| `08` | `devops-engineer` (Vulcan) | Human `approved`; human executes deploy/push |
| `09` | `design-system-owner` (Harmonia) | Human `approved`; `/design-review` attests **UI** |
| `10` | `quality-owner` (Themis) | Human `approved`; `/test-review` attests **tests** |
| Version / sprint container | `sprint-planner` (Hesperus) | Same agent may **close** container |
| US recipe — intent-led (Intent + Plan) | `story-maker` `/create-us` + `/refine-us` | `story-checker` `/review-us` → `ready: true` |
| US recipe — gap-led (from reconcile) | `backlog-surveyor` `/survey-backlog` **apply** only | `story-checker` `/review-us` → `ready: true` |
| Increment (code) | `developer` (Hephaestus) `/implement-us` | Specialist reviews; `story-checker` `/complete-us` → `✅` |

Who cooks the US must not set `ready` or `✅`.

## Slash → owner

| Command | Owner |
| ------- | ----- |
| `/deus-ex` | `deus-ex` |
| `/init-meridian`, `/status`, `/daily-with-ai`, `/agents-help` | `scrum-master` |
| `/discover`, `/create-epic` | `product-owner` |
| `/ux-pass` | `ux-researcher` |
| `/create-version`, `/plan-sprint`, `/complete-sprint`, `/complete-epic` | `sprint-planner` |
| `/create-us`, `/refine-us` | `story-maker` |
| `/survey-backlog` | `backlog-surveyor` |
| `/review-us`, `/complete-us` | `story-checker` |
| `/implement-us` | `developer` |
| `/security-pass`, `/security-review`, `/privacy-pass`, `/dependency-audit`, `/payment-pass` | `security-champion` |
| `/architecture`, `/api-pass` | `technical-architect` |
| `/database-pass` | `data-engineer` |
| `/release-pass` | `devops-engineer` |
| `/design-pass`, `/design-flow`, `/design-theme`, `/design-showcase`, `/design-review`, `/i18n-pass`, `/a11y-pass` | `design-system-owner` |
| `/test-pass`, `/test-review`, `/perf-pass` | `quality-owner` |
| `/seo-pass` | `technical-writer` + `seo-strategy` |
| `/investigate` | `code-investigator` |
| `/map-flow` | `flow-specialist` |
| Phase docs `01`,`04`,`11`, `/document-project`, `/audit-docs` | `technical-writer` |

Skills may be **shared as tools** (`update-decisions-log`, `init-project`, `discover-product`, `meridian-routing`). Domain procedures live in `.agent/skills/` — agents load them; humans invoke **`@owner`** (slash is optional alias). See [station-references.md](../protocol/station-references.md).

## Eighteen-actor roster

1. `deus-ex` — Machina — dispatch only  
2. `scrum-master` — Kairos — ceremonies, `/status`, init  
3. `product-owner` — Clio — discovery, scope, epic  
4. `ux-researcher` — Iris — personas, `/ux-pass`  
5. `technical-writer` — Calliope — phase prose  
6. `security-champion` — Janus — `02`, security passes  
7. `technical-architect` — Daedalus — `05`, `/api-pass`, `/architecture mcp`  
8. `data-engineer` — Mnemosyne — `06`  
9. `design-system-owner` — Harmonia — `09`, design workflows  
10. `quality-owner` — Themis — `10`, test passes  
11. `devops-engineer` — Vulcan — `08`, `/release-pass`  
12. `sprint-planner` — Hesperus — versions, sprints  
13. `story-maker` — Penelope — intent-led create + refine US  
14. `story-checker` — Argus — review + complete US  
15. `developer` — Hephaestus — implement  
16. `code-investigator` — Hermes — consult  
17. `backlog-surveyor` — Metis — backlog reconcile + gap-led US  
18. `flow-specialist` — Ariadne — on-demand UI / feature interaction maps  

**Harmonia vs Ariadne:** `design-system-owner` maintains `09` and episodic `/design-flow`. `flow-specialist` runs `/map-flow` per feature/US with **triage** (skip allowed) — not a mandatory gate for simple US.

## Allowed interactions

1. **Pass** — handoff block with `next agent` + `next command`.  
2. **Bounce** — checker → maker; specialist gap → owner of that standard.  
3. **Consult** — `technical-architect`, `data-engineer`, `code-investigator`, `flow-specialist` mid-station; no `ready`/`✅`/product code.

## Explicitly not a new agent

| Temptation | Why not |
| ---------- | ------- |
| `security-reviewer` / `test-reviewer` / `design-reviewer` | Same champion + attest skill is SoD enough |
| `committer` / push bot | Git push and prod deploy = **human** (`devops-engineer` documents only) |
| `aiox-master` / mega orchestrator | `deus-ex` allocates; specialists execute |
| OpenAI Symphony daemon | SQLite is the tracker |

## Board mapping (derived columns)

Unchanged — agents set `status`, `ready`, `in_progress` only.
