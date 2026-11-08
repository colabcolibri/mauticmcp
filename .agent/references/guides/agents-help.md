# Agents & commands help

Explicit map of **who does what**, **which group they belong to**, and **which step to run** in Meridian.

| Read first | File |
| ---------- | ---- |
| Concepts (phases, US, gates) | [start-here.md](./start-here.md) |
| Day-to-day situations | [usage-guide.md](./usage-guide.md) |
| Agentic trust / earned no-read policy | [agentic-trust-policy.md](../protocol/agentic-trust-policy.md) |
| Agentic quality model / qualitySiege profiles | [agentic-quality-model.md](../protocol/agentic-quality-model.md) |
| **This file** | Agents, slash commands, skills, step order |
| Scrum mapping | [scrum-meridian-map.md](../scrum/scrum-meridian-map.md) |
| **Station map** | [agent-station-map.md](../agents/agent-station-map.md) — cook vs attest |
| Call signs | [agent-personas.md](../agents/agent-personas.md) — mythic names for all 18 agents |
| **Station skills** | [station-references.md](../protocol/station-references.md) — agents + skills (kit v3) |
| **Upgrade from 2.x** | [kit-v3-migration.md](../protocol/kit-v3-migration.md) |
| **Areas** | [agent-areas.md](../agents/agent-areas.md) — discovery, standards, planning, build, attest |

---

## How the harness is layered

```txt
Human (manager)
    ↓
/skill-name  OR  @agent
    ↓
.agent/skills/{name}/SKILL.md
    ↓
docs/
```

| Layer | Role | You invoke |
| ----- | ---- | ---------- |
| **Skill** | Full procedure | `/us-create`, `/data-engineering`, … |
| **Agent** | Persona + gates + skill list | `@story-maker`, `@data-engineer`, … |

**No workflows folder.** Catalog: [agents-help.md](./agents-help.md).

**Routing:** describe the task in chat → `Applying knowledge from @[agent] (CallSign)…`. Override with `@agent-name`.

**Priority:** P0 rules → MERIDIAN.md → agent → skills → templates.

---

## Agent groups

Eighteen live actors. Line: [agent-station-map.md](../agents/agent-station-map.md). Call signs: [agent-personas.md](../agents/agent-personas.md). `deus-ex` allocates; the others cook or attest.

### Group 1 — Orchestration

Keeps you as manager. `deus-ex` picks the station. `scrum-master` reports health and runs init/daily.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`deus-ex`** (Machina) | “Who should run?”, which station | Handoff block only | Cook US; `ready`; `✅`; product code; `/status` numbers |
| **`scrum-master`** (Kairos) | Project health, phase progression, init, daily loop | All `docs/` (read), decision log | Invent MVP code; approve docs; mark ✅ without Record; allocate stations (`deus-ex`) |

**When to use:** `/deus-ex` or `@deus-ex` for allocation; `/status`, `/init-meridian`, `/daily-with-ai` for ceremonies and health.

**Skills (`deus-ex`):** `deus-dispatch`, `meridian-routing`  
**Skills (`scrum-master`):** `init-project`, `update-decisions-log`, `meridian-routing`

---

### Group 2 — Scope & framing

Defines *what the product is* before structure and code.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`product-owner`** (Clio) | Problem, users, in/out of scope, assumptions, risks, epics | `docs/00_scope.md`, SQLite epics | Tech stack, architecture, US |
| **`ux-researcher`** (Iris) | Personas, JTBD, journey hypotheses | `docs/03_user_types.md`, discovery inputs | Tokens, `09`, code |

**When to use:** `/discover`, `/create-epic` (Clio); `/ux-pass` (Iris) before `/design-flow`.

**Skills (PO):** `discover-product`, `epic-create`, …  
**Skills (UX):** `ux-research`, `discover-product`, …

---

### Group 3 — Documentation & phase docs

Writes and reviews phase documents and product-facing docs agents can execute.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`technical-writer`** (Calliope) | Phase docs `01`, `04`, `07`, `11` | `docs/01_*`, `04_*`, `07_*`, `11_*` | `06`, `08`, `09`; approve docs; US |
| **`data-engineer`** (Mnemosyne) | Persistence contract | `docs/06_database.md` | App code; `05` boundaries |
| **`devops-engineer`** (Vulcan) | Environments, CI/CD, rollback runbooks | `docs/08_environments.md` | `git push`, prod deploy |

**When to use:** `/document-project`, `/audit-docs` (Calliope); `/database-pass` (Mnemosyne); `/release-pass` (Vulcan).

**Skills:** see [agent-station-map.md](../agents/agent-station-map.md)

---

### Group 4 — Security & architecture

Hardens structure before backlog and implementation.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`security-champion`** | Threat model, secrets, OWASP, AI-agent safety, Git hygiene | `docs/02_security.md` | Skip security to ship faster |
| **`technical-architect`** | System boundaries, modules, integrations, consistency | `docs/05_architecture.md` | Architecture before scope/security drafts exist |

**When to use:** `/security-pass`, `/architecture`, security review before merge.

**Skills:** `security-doc`, `security-privacy`, `security-code`, `security-supply-chain`, `update-decisions-log`, `meridian-routing` (architect **consults** `security-code`, does not own `/security-review`)

**Gate:** `05_architecture.md` must be **`approved`** before epics/versions/US (enforced by `sprint-planner` and `story-maker`).

---

### Group 5 — Delivery planning

Turns approved architecture into releases, sprints, and execution order.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`sprint-planner`** | Versions, sprints, MoSCoW, go-live checklist, story sequencing | SQLite `versions`, `sprints` | Create US before architecture approved |

**When to use:** `/create-version`, `/plan-sprint`, roadmap and sprint scope.

**Skills:** `version-create`, `sprint-create`, `sprint-complete`, `epic-complete`, `update-decisions-log`, `meridian-routing`

---

### Group 6 — Board & user stories

Owns the executable backlog and honest execution state.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`story-maker`** | Cook intent-led US Intent/Plan | SQLite `user_stories` | Set `ready` or `✅`; product code; gap reconcile |
| **`story-checker`** | Attest DoR (`ready`) and DoD (`✅`) | SQLite `user_stories` | Cook Plan; implement |

**When to use:** `/create-us`, `/refine-us` → maker; `/review-us`, `/complete-us` → checker.

**Skills (maker):** `us-create`, `us-refine`, `update-decisions-log`, `meridian-routing`  
**Skills (checker):** `us-review`, `us-complete`, `update-decisions-log`, `meridian-routing`

---

### Group 7 — Backlog reconcile

Finds traceability debt and creates **gap-derived** US (`ready: false`) after evidence review.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`backlog-surveyor`** | Reconcile docs, inventory, SQLite, optional code vs backlog | Gap report; gap-led US in SQLite | Set `ready` or `✅`; product code; create epics; intent-led `/create-us` |

**When to use:** `/survey-backlog` (default `report`); `/survey-backlog apply` after you approve gap ids; after `/document-project` or before `/complete-epic`.

**Skills:** `backlog-reconcile`, `us-create` (apply only), `investigate-codebase` (narrow consult), `update-decisions-log`, `meridian-routing`

---

### Group 8 — Interaction flows (on demand)

Maps UI and feature processes when helpful — **triage skips simple US** (not a rigid gate).

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`flow-specialist`** | Feature/screen interaction maps, branches, empty/error | Chat mermaid (`light`) or `docs/architecture/diagrams/feature-*.md` | Product code; approve `09`; replace full `/design-flow` |

**When to use:** `/map-flow` before `/refine-us` on multi-step UI; optional anytime you need clarity. Skip is valid for trivial slices.

**Skills:** `map-interaction-flow`, `investigate-codebase` (code mode), `update-decisions-log`, `meridian-routing`

---

### Group 9 — Code investigation (read-only)

Trace flows and explain behavior before refine, spike, or architecture updates.

| Agent | Serves for | Primary artifacts | Does not |
| ----- | ---------- | ----------------- | -------- |
| **`code-investigator`** | How code works, where logic lives, flow traces | Investigation report (chat) | Product code; US/epic without manager ask |

**When to use:** `/investigate`, "how does X work?", before `/refine-us` when Plan needs code facts.

**Skills:** `investigate-codebase`, `update-decisions-log`, `meridian-routing`

---

## Slash command groups

Slash command groups — workflows in **six groups**. Each maps to one primary agent (sometimes two).

### Group A — Bootstrap

| Step | Command | Agent | What it does |
| ---- | ------- | ----- | ------------ |
| A1 | **`/init-meridian`** | `scrum-master` | Creates `docs/` tree, initial scope, decision log, empty board. **Mode B (existing codebase):** also `docs/inventory/as-is.md` — transitional capability map; no retroactive US. **No product code.** |

---

### Group B — Session & orientation

| Step | Command | Agent | What it does |
| ---- | ------- | ----- | ------------ |
| B0 | **`/deus-ex`** | `deus-ex` | Dispatch: next agent + next command. Does **not** execute that station. |
| B1 | **`/status`** | `scrum-master` | Read-only health: kit root, Meridian projects (multi-`docs/` repos), active product, phase doc statuses, US counts, blockers. |
| B2 | **`/daily-with-ai`** | `scrum-master` | Guided session: status → pick story → implement → close → sync. |
| B3 | **`/agents-help`** | `scrum-master` | Opens this reference; summarizes groups and current-step hints. |

---

### Group C — Phase documents (structure)

Complete in order: `00` → `01` → `02` → `03` → `04` → **`05`** → `06` → `07` → `08`.

| Step | Command | Agent | Target doc | What it does |
| ---- | ------- | ----- | ---------- | ------------ |
| C1 | *(conversation)* | `product-owner` | `00_scope.md` | Scope, users, out of scope. |
| C1b | **`/discover`** | `product-owner` (Clio) | `docs/discovery/product-brief.md` | Product discovery before scope. **No code.** |
| C1c | **`/ux-pass`** | `ux-researcher` (Iris) | `03_user_types.md` | Personas, JTBD, journey hypotheses. Modes: `bootstrap`, `US-XXXX`. **Doc only.** |
| C2 | *(conversation)* | `technical-writer` (Calliope) | `01`, `04`, `07` | Draft phase documents (not `03`, `06`, `08` — specialist owners). |
| C2b | **`/database-pass`** | `data-engineer` (Mnemosyne) | `06_database.md` | Schema, migrations, retention. Modes: `bootstrap`, `US-XXXX`. **Doc only.** |
| C2c | **`/release-pass`** | `devops-engineer` (Vulcan) | `08_environments.md` | Local run, env vars, CI/CD catalog, deploy/rollback runbooks. Human executes push/deploy. **Doc only.** |
| C3 | **`/security-pass`** | `security-champion` | `02_security.md` + `08` CI rows | Threat model, secrets, OWASP, agent safety; bootstrap uses `security-bootstrap.md` + `ci-gates-bootstrap.md`. |
| C3b | **`/privacy-pass`** | `security-champion` | `02_security.md` § LGPD + GDPR | Brazil (ANPD) and EU (EDPB) privacy sections; official refs in checklist. **Doc only.** |
| C4 | **`/architecture`** | `technical-architect` | `05_architecture.md` + optional `docs/architecture/` + `docs/architecture/diagrams/` | Overview, detail files, **diagram index** (multi-file Mermaid maps for IDE); gate for backlog. Skill: `generate-architecture-diagram`. |
| C5 | **`/design-pass`** | `design-system-owner` | `09_design_system.md` | Contract: tokens, stack, components. Modes: `bootstrap`, `US-XXXX`. **Doc only.** |
| C5b | **`/design-flow`** | `design-system-owner` | `09` § Screen flows | Jobs → screens → states; web vs app vs extension. **Doc only.** |
| C5c | **`/design-theme`** | `design-system-owner` | `09` § Theme + type | Modes, semantic tokens, type ramp integrity. **Doc only.** |
| C5d | **`/i18n-pass`** | `design-system-owner` (Harmonia) | `09` § i18n | Locales, fallback, formats. **Doc only.** |
| C5e | **`/a11y-pass`** | `design-system-owner` (Harmonia) | `09` § a11y | WCAG-oriented baseline. **Doc only.** |
| C5f | **`/api-pass`** | `technical-architect` (Daedalus) | `07_api_contracts.md` | API/boundary contract. **Doc only.** |
| C5g | **`/payment-pass`** | `security-champion` (Janus) | `02` § Payments | Billing security. **Doc only.** |
| C10b | **`/perf-pass`** | `quality-owner` (Themis) | `10` § Performance | Budgets, CWV, CI gates. **Doc only.** |
| C12b | **`/seo-pass geo`** | `technical-writer` + `geo-optimization` | `12` § GEO | AI discoverability. **Doc only.** |
| C6 | **`/design-showcase`** | `design-system-owner` | `09` § Showcase + US drafts | Plan catalog routes; creates showcase US for `developer`. **No code.** |
| C7 | **`/design-review`** | `design-system-owner` | Report | Audit live UI vs `09` + showcase. **No code.** |
| C8 | **`/security-review`** | `security-champion` | Report | Audit code vs `02` + US security acceptance. **No code.** |
| C9 | **`/dependency-audit`** | `security-champion` | Report | Lockfiles and supply chain hygiene. **No code.** |
| C10 | **`/test-pass`** | `quality-owner` | `10_test_strategy.md` | Pyramid, runners, coverage; bootstrap runs `quality-profile` then `test-stack-catalog.md` + `ci-gates-catalog.md` for `08` CI (gates up to declared tier). Modes: `bootstrap`, `US-XXXX`. **Doc only.** |
| C11 | **`/test-review`** | `quality-owner` | Report | Audit US tests vs strategy before close. **No code.** |
| C12 | **`/seo-pass`** | `seo-strategy` + `technical-writer` | `12_marketing_seo.md` | Public web only — meta, sitemap, CWV. **Doc only.** Skip CLI-only. |
| C13 | **`/investigate`** | `code-investigator` (Hermes) | Report | Read-only codebase trace and explanation. **No code.** |
| C15 | **`/document-project`** | `technical-writer` (Calliope) | `docs/` + `inventory/as-is.md` | Brownfield baseline in phase docs. **No US.** |
| C16 | **`/audit-docs`** | `technical-writer` (Calliope) | Report | Phase docs depth and drift vs code. **Report only** unless `apply`. |
| C17 | **`/survey-backlog`** | `backlog-surveyor` (Metis) | Report and/or US | Reconcile backlog gaps. **`report`** default; **`apply`** creates US (`ready: false`) for approved gaps. |
| C18 | **`/map-flow`** | `flow-specialist` (Ariadne) | Report and/or diagram file | Triage → skip, `light`, `standard`, `product`, or `code` interaction maps. **Not mandatory** for simple US. |

**HAR (ação humana necessária):** agents stop for external accounts, OAuth/PAT, billing, production credentials — see `rules/MERIDIAN.md`. Not a slash command; applies during any workflow.

**UI products:** create `09` stub at `/init-meridian` when stack has UI. Run `/design-pass bootstrap` after `01_tech_stack`, then `/design-flow` and `/design-theme` before treating `09` as complete. Human approves `09` before Must UI US ship.

**Tested products:** create `10` stub when automated tests in scope. Run `/test-pass bootstrap` after `01_tech_stack`.

**Human gate:** you set `status: approved` on each doc. Agent never sets `approved`.

---

### Group D — Backlog artifacts

**Prerequisite:** `05_architecture.md` is **`approved`**.

| Step | Command | Agent | Output | What it does |
| ---- | ------- | ----- | ------ | ------------ |
| D1 | **`/create-epic`** | `product-owner` | `EPIC-XX` in SQLite | Product capability block. |
| D2 | **`/create-version`** | `sprint-planner` | `vX` in SQLite | Release grouping epics/US. |
| D3 | **`/plan-sprint`** | `sprint-planner` | `vX-SY` in SQLite | Time-boxed goal + story list. |
| D4 | **`/complete-sprint vX-SY`** | `sprint-planner` | sprint `status: complete` | Sprint review + Retrospective filled. |
| D5 | **`/complete-epic EPIC-XX`** | `sprint-planner` | epic `status: complete` | No open Must US; outcome confirmed. |
| D6 | **`/survey-backlog`** | `backlog-surveyor` | Gap report and/or US | After `05` approved; optional after `/document-project`. Use **`apply`** only after approving gap rows. |

Order: **Epic → Version → Sprint** (sprint optional but recommended) → User story → **`/complete-us` cascade invites** `/complete-sprint` / `/complete-epic` when containers are eligible (slash commands remain for recovery).

Epic/version **close:** `/complete-epic` for epics; version via `update-version` when invited by cascade or hygiene. Prefer new epic over reopening `complete`.

---

### Group E — User story lifecycle

| Step | Command | Agent | US state after | What it does |
| ---- | ------- | ----- | -------------- | ------------ |
| E1 | **`/create-us`** | `story-maker` | `ready: false` | New US: Intent + draft Plan. |
| E2 | **`/refine-us US-XXXX`** | `story-maker` | `ready: false` | Approach, arch refs, concrete tests. Does **not** set ready. |
| E3 | **`/review-us US-XXXX`** | `story-checker` | `ready: true` if DoR attest | Audit; only path that sets `ready`. Report-only leaves ready unchanged. |
| E4 | **`/implement-us US-XXXX`** | `developer` | — | Gate: `ready: true`, deps, Plan; then product code. **Block if not attested.** |
| E5 | *(manager review)* | human | — | Review diff and run tests. |
| E6 | **`/complete-us US-XXXX`** | `story-checker` | `status: ✅` | Fills Record; **lifecycle cascade** offers sprint/epic/version close. |

**Rules:** no code without E3 (`ready: true`) **and** E4 gate. No ✅ without E6 (`## Record` + evidence).

### Pass / bounce / consult

Every station ends with a **handoff** block: `station`, `agent`, `done`, `blocker`, `next agent`, `next command`, `artifact id`. The next agent reads the artifact + block, not the previous persona.

| Interaction | Meaning |
| ----------- | ------- |
| **Pass** | Work finished; handoff names the next owner and slash command |
| **Bounce** | Checker reject → one station back (`story-checker` → `story-maker`; specialist review → `developer`). Skip to `product-owner` only for **scope** |
| **Consult** | `technical-architect` and `code-investigator` mid-station; they must not set `ready`, `✅`, or write product code |

---

### Group F — Decisions & validation

| Step | Command / action | Agent / tool | What it does |
| ---- | ---------------- | ------------ | ------------ |
| F1 | **`/update-decisions-log`** | any + skill | `prepend-decision` in SQLite. Run `date` first. Never edit old rows. |
| F2 | **`validate_meridian.py`** | script | `python3 .agent/scripts/validate_meridian.py <project-root>` — structure, US contracts, board. |
| F3 | **Meridian: Validate Project** *(extension)* | IDE command | Same validator from VS Code/Cursor sidebar. |

---

## End-to-end steps (numbered)

Use this as the canonical sequence. Skip steps only when the artifact already exists and is approved.

```txt
 0. /deus-ex (when lost on who/station)     [Group B]  deus-ex — pass, do not cook
 1. /init-meridian                          [Group A]  scrum-master
 2. Complete 00_scope → approve             [Group C]  product-owner (Clio)
 2b. /discover (optional)                    [Group C]  product-owner
 2c. /ux-pass → approve 03                  [Group C]  ux-researcher (Iris)
 3. Complete 01, 04, 07 (draft → approve)  [Group C]  technical-writer (Calliope)
 4. /security-pass → approve 02             [Group C]  security-champion (Janus)
 5. /architecture → approve 05              [Group C]  technical-architect (Daedalus)  ← GATE
 5b. /design-pass bootstrap → approve 09     [Group C]  design-system-owner (Harmonia)    (UI products)
 5b2. /design-flow + /design-theme + /i18n-pass + /a11y-pass  [Group C]  design-system-owner (UI)
 5c. /design-showcase (catalog US)          [Group C]  design-system-owner    (UI products)
 6. /database-pass → approve 06              [Group C]  data-engineer (Mnemosyne)
 6a. /api-pass → approve 07                  [Group C]  technical-architect (Daedalus) — when API in scope
 6b. /payment-pass → approve 02 payments     [Group C]  security-champion (Janus) — when billing in scope
 6c. /release-pass → approve 08             [Group C]  devops-engineer (Vulcan)
 6d. /test-pass + /perf-pass → approve 10    [Group C]  quality-owner (Themis)   (when tests in scope)
 6e. /seo-pass + /seo-pass geo               [Group C]  technical-writer — public web only
 6f. /architecture mcp                      [Group C]  technical-architect — when agent tools in scope
 7. /create-epic                            [Group D]  product-owner
 8. /create-version                         [Group D]  sprint-planner
 9. /plan-sprint                            [Group D]  sprint-planner
10. /survey-backlog report                    [Group D]  backlog-surveyor  (optional; brownfield / hygiene)
10b. /survey-backlog apply                    [Group D]  backlog-surveyor  (gap-derived US; ready false)
11. /create-us                               [Group E]  story-maker
12. /refine-us US-XXXX                       [Group E]  story-maker  (Plan; ready stays false)
13. /review-us US-XXXX                       [Group E]  story-checker → ready: true
14. /implement-us US-XXXX                    [Group E]  developer → gate then code
15. /design-review (UI US)                   [Group C]  design-system-owner → before close
15b. /security-review (sensitive US)          [Group C]  security-champion → before close
15c. /test-review (tests: required)           [Group C]  quality-owner → before close
16. Manager review diff + tests              [Group E]  human
17. /complete-us US-XXXX                     [Group E]  story-checker
18. git commit (human)                       [Group F]  you — one US per commit
19. /status or /daily-with-ai                [Group B]  scrum-master → back to step 11
20. /complete-sprint vX-SY (when sprint done) [Group D]  sprint-planner — after US in sprint closed
```

---

## Skills (domain + shared)

All procedures live in **`.agent/skills/{name}/SKILL.md`**. Agents declare which skills they load in `agent.md` frontmatter.

**Shared** (multiple stations):

| Skill | Used by | Purpose |
| ----- | ------- | ------- |
| `meridian-routing` | all agents | Pick correct station from intent |
| `update-decisions-log` | most agents | Prepend decision JSON |
| `init-project` | scrum-master, product-owner, technical-writer | Bootstrap `docs/` |
| `discover-product` | product-owner, ux-researcher | `/discover` brief |
| `create-meridian-artifact` | maintainers | Extend kit registry |

**Domain** (owned by one station) — examples:

| Agent | Skills |
| ----- | ------ |
| `story-maker` | `us-create`, `us-refine` |
| `security-champion` | `security-doc`, `security-code`, `payment-integration`, … |
| `design-system-owner` | `design-system`, `design-flow`, `i18n-localization`, … |

`agents/{slug}/references/{skill}/` symlinks → `skills/{skill}/` (template registry paths).

Full contract: [station-references.md](../protocol/station-references.md).

---

## Intent → agent quick lookup

| You want to… | Group | Agent | Command |
| ------------ | ----- | ----- | ------- |
| Who should run this / which station | B | `deus-ex` | `/deus-ex` |
| Start or migrate project | A | `scrum-master` | `/init-meridian` |
| See blockers and next step | B | `scrum-master` | `/status` |
| Full guided day | B | `scrum-master` | `/daily-with-ai` |
| Open this manual | B | `scrum-master` | `/agents-help` |
| Define scope | C | `product-owner` (Clio) | chat + `00_scope`, `/discover` |
| UX research / personas | C | `ux-researcher` (Iris) | `/ux-pass` |
| Draft phase docs | C | `technical-writer` (Calliope) | chat — `01`, `04`, `07` |
| Database contract | C | `data-engineer` (Mnemosyne) | `/database-pass` |
| Environments / CI | C | `devops-engineer` (Vulcan) | `/release-pass` |
| Security doc | C | `security-champion` (Janus) | `/security-pass` |
| Security code audit | C | `security-champion` | `/security-review`, `/dependency-audit` |
| Test strategy | C | `quality-owner` | `/test-pass`, `/test-pass bootstrap` |
| Test audit | C | `quality-owner` | `/test-review` |
| Architecture doc | C | `technical-architect` | `/architecture` |
| New epic | D | `product-owner` | `/create-epic` |
| New version / sprint | D | `sprint-planner` | `/create-version`, `/plan-sprint`, `/complete-sprint` |
| New / refine / review / close US | E | `story-maker` / `story-checker` / `developer` | `/create-us`, `/refine-us`, `/review-us`, `/implement-us`, `/complete-us` |
| Backlog gaps / missing US | D | `backlog-surveyor` (Metis) | `/survey-backlog`, `/survey-backlog apply` |
| UI / feature interaction map | C / E | `flow-specialist` (Ariadne) | `/map-flow`, `/map-flow light US-XXXX` |
| Board refresh | — | Extension reads SQLite on save |
| Log a decision | F | any | `/update-decisions-log` |
| Design contract (`09`) | C | `design-system-owner` | `/design-pass`, `/design-pass bootstrap` |
| Screen flows / IA | C | `design-system-owner` | `/design-flow` |
| Theme / type hierarchy | C | `design-system-owner` | `/design-theme` |
| Design catalog plan | C | `design-system-owner` | `/design-showcase` |
| Design UI audit | C | `design-system-owner` | `/design-review` |
| Code investigation | C | `code-investigator` | `/investigate` |
| Brownfield baseline | C | `technical-writer` | `/document-project` |
| Phase doc audit | C | `technical-writer` | `/audit-docs` |
| Product discovery | C | `product-owner` | `/discover` |
| Extend Meridian kit | — | `create-meridian-artifact` skill | edit `.agent/` + `sync_kit.sh` |
| Validate structure | F | script / extension | `validate_meridian.py` or **Validate Project** |

---

## IDE extension commands (separate layer)

These are **not** agents. They read the **active** `docs/` in the editor (extension `app-visual-studio`). In monorepos, **one active project** at a time — see [usage-guide.md § Multiple Meridian projects](./usage-guide.md#multiple-meridian-projects).

| Group | Command | Purpose |
| ----- | ------- | ------- |
| Views | **Open Board**, **Open Versions**, **Open Sprints**, **Open Epics**, **Open Decisions** | Board: 📋 Backlog · 📌 Todo · 🔨 Doing · 🔶 Partial · 🧪 Tests · ✅ Done (from `status` + `ready` + `in_progress` + tests); toggles 🧊 Frozen · 🚫 Deprecated. Other tabs read-only; **Project** row shows name + `docs/` path |
| Governance | **Select Active Project**, **Validate Project**, **Sync Board**, **Show Workspace Status** | Switch product (saved); validate `packageRoot`; board JSON; list all projects |
| Help | **Open Command Help**, **Open Agents Help** | Extension catalog; kit `agents-help.md` at runtime |

**Multi-product UI:** Board and Deliverables show which `docs/` is loaded; dropdown switches product and refreshes open tabs. Status bar shows project name when N>1. Install: Marketplace **Meridian Harness** or `pnpm install:cursor` in `app-visual-studio/`.

---

## Invocation cheat sheet

| Method | Example | When |
| ------ | ------- | ---- |
| Slash command | `/refine-us US-0017` | Known workflow step |
| Explicit agent | `@story-maker refine US-0017` | Override routing |
| Natural language | “Implement US-0017” | Run `/implement-us US-0017` if `ready: true`; else block |
| Read-only check | `/status` | Start of every session |

---

## Related files

| Path | Content |
| ---- | ------- |
| `.agent/skills/*/SKILL.md` | All procedures — invoke `/skill-name` |
| `.agent/agents/{slug}/agent.md` | Persona + skills list — invoke `@slug` |
| `.agent/references/guides/usage-guide.md` | Situation-based how-to |
| `.agent/references/guides/start-here.md` | Concepts and artifact anatomy |
