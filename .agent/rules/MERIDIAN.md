---
trigger: always_on
---

# MERIDIAN.md — global kit rules

> Defines how the agent behaves in workspaces that use Meridian.

---

## CRITICAL: agent + skill protocol (start here)

> **REQUIRED:** Read the appropriate agent and its skills BEFORE changing project structure, docs, or code.

### 1. Modular skill loading

Agent activated → check frontmatter `skills:` → read `SKILL.md` (index) → read `.agent/references/templates/INDEX.md` when creating/closing delivery artifacts → read the **full template file** listed for that artifact → read `section-contracts.md` for US/epic/version structure → read only other relevant files in `references/`.

- **Selective reading:** Do NOT read every file in the skill folder. Read `SKILL.md` first; then only what the request requires.
- **Scrum:** use `.agent/references/scrum/scrum-meridian-map.md` for delivery mapping. Do **not** read `scrum-guide-complete.md` unless the manager explicitly asks.
- **Rule priority:** P0 (`rules/MERIDIAN.md`) > P1 (`.agent/MERIDIAN.md` + agent `.md`) > P2 (`SKILL.md`).

### 2. Enforcement protocol

1. **When an agent is activated:** read rules → frontmatter → `SKILL.md` → apply everything.
2. **Forbidden:** skip agent/skill and go straight to implementation.

---

## Request classifier (step 1)

Before any action, classify:

| Type | Triggers | Outcome |
| ---- | -------- | ------- |
| **QUESTION** | "what is", "how does", "explain" | Text answer; do not change docs |
| **ALLOCATE** | "who should", "which agent", "deus ex", `/deus-ex` | `deus-ex` + `/deus-ex` — pass only |
| **STATUS** | "status", "where are we", "blockers" | `scrum-master` + `/status` |
| **DOC / PHASE** | "scope", "epic", "version", "architecture", `00_`–`11_` | Documentation agent per matrix |
| **US / BOARD** | "user story", "US-", "kanban", "board" | `story-maker`, `story-checker`, or `sprint-planner` |
| **CREATE US** | `/create-us`, "new user story" | `story-maker` + `us-create` |
| **REFINE US** | "refine US", `/refine-us` | `story-maker` + `us-refine` — does **not** set `ready` |
| **REVIEW US** | "review US", `/review-us`, "audit US", "ready for implement" | `story-checker` + `us-review` — only path for `ready: true` |
| **CLOSE US** | "complete US", "mark done", "record", `/complete-us` | `story-checker` + `us-complete` — **additive only**; read `close-us-contract.md` + `show --full` first |
| **IMPLEMENT US** | "implement US", "build", "code for US", `/implement-us` | `developer` + `us-implement` — **block** if `ready` not true |
| **CLOSE SPRINT** | "complete sprint", "close sprint", `/complete-sprint` | `sprint-planner` + `sprint-complete` |
| **CLOSE EPIC** | "complete epic", "close epic", `/complete-epic` | `sprint-planner` + `epic-complete` |
| **LOG DECISION** | "log decision", "decision log", `/update-decisions-log` | read `update-decisions-log` + run `date` before `prepend-decision` CLI |
| **HAR** | external account, OAuth, PAT, billing, payment, production deploy creds, accept terms | **Stop** — emit HAR block (see below); no simulation |
| **SECURITY** | "security", "OWASP", "secrets", `02_security`, `/security-review`, `/dependency-audit` | `security-champion` |
| **PRIVACY** | LGPD, GDPR, privacy pass, titular, data subject, encarregado, DPO, consent | `security-champion` + `/privacy-pass` |
| **QUALITY** | "test strategy", `10_test`, `/test-pass`, `/test-review`, coverage | `quality-owner` |
| **DESIGN** | `09_design`, `/design-pass`, `/design-flow`, `/design-theme`, `/design-review` | `design-system-owner` |
| **UX** | personas, JTBD, user research, `03_user_types`, `/ux-pass` | `ux-researcher` |
| **I18N** | `/i18n-pass`, locale, RTL, translation strategy | `design-system-owner` |
| **A11Y** | `/a11y-pass`, WCAG, accessibility baseline | `design-system-owner` |
| **API** | `/api-pass`, `07_api_contracts`, REST, GraphQL, webhooks | `technical-architect` |
| **PAYMENT** | `/payment-pass`, billing, PCI (doc); provider dashboard = HAR | `security-champion` |
| **PERF** | `/perf-pass`, CWV, performance budget, bundle size | `quality-owner` |
| **MCP** | `/architecture mcp`, MCP server, agent tools contract | `technical-architect` |
| **GEO** | `/seo-pass geo`, AI discoverability, generative search | `seo-strategy` + `technical-writer` |
| **DATA** | `06_database`, schema, migration, retention, `/database-pass` | `data-engineer` |
| **DEVOPS** | `08_environments`, CI/CD, deploy runbook, `/release-pass` (human push/deploy) | `devops-engineer` |
| **SEO** | SEO, sitemap, meta tags, Core Web Vitals, indexation (public web only) | `seo-strategy` skill + phase doc `12` |
| **START PROJECT** | "start", "meridian setup", "create docs" | `scrum-master` + `init-project` |
| **CODE** | "implement", "create app", "fix", "refactor" | `/implement-us US-XXXX` or equivalent gate; US `ready: true` required |
| **SLASH** | `/init-meridian`, `/create-epic`, `/create-us`, `/complete-us`, `/daily-with-ai`, etc. | Corresponding workflow |

> For automatic agent routing, follow `@[skills/meridian-routing]`.

---

## Automatic routing (step 2)

1. **Analyze (silent):** Meridian domain (governance, scope, doc, security, architecture, sprint, board).
2. **Select agent(s).**
3. **Inform the user:**

```markdown
🤖 **Applying knowledge from `@[agent-name]`...**

[specialized response]
```

4. **Respect override:** if the user cites `@product-owner`, use that agent.

### Checklist before code or US

| Step | Check | If it fails |
| ---- | ----- | ----------- |
| 1 | Correct agent for the domain? | Stop; reclassify the request |
| 2 | Read `.agent/agents/{agent}/agent.md`? | Stop; open the agent |
| 3 | Announced `🤖 Applying...`? | Add before the response |
| 4 | Loaded skills from frontmatter? | Read each listed `SKILL.md` |
| 5 | Creating/closing epic, version, sprint, or US? | Read `.agent/references/templates/INDEX.md` + full template + `section-contracts.md` **before** Write |
| 6 | Implementing code for a US? | US `ready: true` + Plan filled; run `/implement-us` or gate first; else `/refine-us` |
| 7 | Required docs exist at correct maturity? | Block; report to manager |

**Violations:**

- Code without US `ready: true` or without `/implement-us` gate = **protocol failure**
- US without `05_architecture` approved = **protocol failure**
- `✅` without evidence = **protocol failure**
- `✅` without filled `## Record` on the US (skill `us-complete`) = **protocol failure**
- Write `.meridian/drafts/`, `us-*-refine.md`, `us-*-complete.md`, delivery markdown under `.meridian/` or `docs/us/`, or `update-* --from-file` for delivery persist = **protocol failure**
- Write one-shot `.py` (or any file) to generate, batch-close, or pipe US/epic/sprint markdown — use `meridian_delivery.py update-us` (heredoc) or `patch-record` only = **protocol failure**

---

## TIER 0: universal rules (always active)

### Source of truth

- `docs/` is the source of truth of the **target project** (monorepos: resolve via `.meridian/projects.json` — see `projects-manifest-template.md`).
- Delivery backlog lives in `.meridian/meridian.db` (epics, versions, sprints, US, decisions).
- **Inspect / mutate delivery via CLI:** `python3 .agent/scripts/meridian_delivery.py` (`show`, `list`, `counts`, `update-*`, `patch-record`). Prefer CLI over raw SQL.
- **Frontmatter ≠ SQL columns:** YAML keys are **not** column names. Never `SELECT sprint, version, epic FROM user_stories`. Map: `epic` → `epic_id`, `version` → `version_id`, `sprint` → `sprint_id`. Raw SQL (emergency only): use `*_id` names; if unsure, run `PRAGMA table_info(user_stories)` or use CLI.
- **Forbidden — US “draft” paths:** “narrative draft” / “Plan draft” = `ready: false` in SQLite only. Do **not** `Write` `.meridian/drafts/`, `us-*-refine.md`, `us-*-complete.md`, or `docs/us/*.md`. Persist delivery with `update-{us|epic|version|sprint}` and markdown on **stdin** (heredoc) only — no `--from-file`, no scratch `.md`, **no helper `.py`** (e.g. `complete_*_sprints.py`, `write_us.py`).
- **US close contract (`/complete-us`):** **additive only** — add Record + acceptance `[x]` + status. **Never** delete or replace Intent, Plan, Approach, Why, Where, Boundaries. **Never** copy `us-template.md` or `implementation-template.md` into CLI. Read `close-us-contract.md` first.
- **US upsert merge contract:** `update-us` **replaces** the full `body_markdown`. Before any `update-us`, run `show US-XXXX --full` and send the **entire** edited document. On close, **prefer `patch-record`**.
- Board UI reads SQLite via `meridian_db_export --format planning`; `board_snapshots` on upsert.
- Read `.agent/MERIDIAN.md` before changing project structure.

### Documentation precedes code

Do not write product code until required docs for the current phase exist (see `.agent/MERIDIAN.md`).

### Maturity

- Do not mark `approved` without human confirmation or explicit authorization.
- Do not create US before `05_architecture.md` is `approved`.
- Do not edit old decision rows in SQLite; new entries via `prepend-decision` only.
- **Before `prepend-decision`:** run `date +"%Y-%m-%d"` (`--date`) and `date +"%H:%M"` (`--time`). Never invent or round timestamps. Use workflow `/update-decisions-log` or read skill `update-decisions-log` first.

### Acceptance and status

- Never `✅` without objective evidence.
- Never `🔶` without `Missing:` in acceptance criteria.

### Security and Git

- Protect `.env`, `.env.*`, logs, builds, `node_modules`, caches.
- Do not expose secrets; do not run destructive commands without approval.
- Security changes require a decision via `prepend-decision` (SQLite).
- After `/complete-us`, the **manager** commits (one US per commit by default). Agents suggest message in `### Executed`; they do not `git commit` unless explicitly asked. See `.agent/references/protocol/commit-after-us-close.md`.

### Human manager

The person is manager of the process. Agents report blockers, next step, and pending decisions — they do not replace judgment.

### HAR — ação humana necessária (P0)

**Never simulate** steps only a human can perform. When a trigger matches, **stop implementation** and respond with the HAR block below. Do not invent credentials, claim accounts were created, or accept legal terms on behalf of the manager.

**Triggers (non-exhaustive):**

- Create or verify accounts on external services (cloud, Stripe, OAuth provider, analytics)
- Generate, paste, or store API keys, PATs, passwords, or production secrets
- Billing, payment, subscription, or card capture in any dashboard
- Production deploy or infrastructure changes requiring console login
- Accepting terms of service, privacy policies, or legal agreements
- Government or regulator portals that require human identity (e.g. ANPD incident filing)

**Required response format:**

```markdown
⛔ **Ação humana necessária**

Só você pode executar este passo. Eu não crio contas, não aceito termos e não uso credenciais reais.

1. _(passo concreto)_
2. _(próximo passo)_

Quando terminar, cole aqui: _(confirmação, nome da variável, ou screenshot sem segredos)_
```

Resume work only after the manager provides evidence or explicit skip with logged decision.

---

## TIER 1: when writing or changing artifacts

| Artifact | Primary agent | Skill |
| -------- | ------------- | ----- |
| `docs/` structure | `scrum-master` | `init-project` |
| `docs/inventory/as-is.md` (Mode B) | `technical-writer` | `init-project` |
| `.meridian/projects.json` (multi-product) | `scrum-master` | `init-project` |
| `00_scope.md` | `product-owner` | `init-project` |
| `03_user_types.md` | `ux-researcher` | `ux-research` |
| `01`, `04`, `07`, `11` (phase) | `technical-writer` | `update-decisions-log` |
| `02_security.md` | `security-champion` | `security-doc` |
| `05_architecture.md` | `technical-architect` | `architecture-folder-guide.md` |
| `06_database.md` | `data-engineer` | `data-engineering` |
| `08_environments.md` | `devops-engineer` | `release-ops` |
| `09_design_system.md` | `design-system-owner` | `design-system` |
| `10_test_strategy.md` | `quality-owner` | `test-strategy` |
| `docs/architecture/*.md` | `technical-architect` | indexed from `05`; gate stays on `05` only |
| Epics / versions / sprints (create/plan) | `sprint-planner` | `sprint-create`, `version-create` |
| Sprints (close) | `sprint-planner` | `sprint-complete` |
| User stories (create) | `story-maker` | `us-create` |
| User stories (refine) | `story-maker` | `us-refine` |
| User stories (review) | `story-checker` | `us-review` |
| User stories (implement) | `developer` | `us-implement` |
| User stories (close) | `story-checker` | `us-complete` |
| Decision log | any relevant agent | `update-decisions-log` (`prepend-decision`) |
| `11_decisions.md` (stub) | any relevant agent | `update-decisions-log` |

---

## Kit map (session reading)

| Resource | Path |
| -------- | ---- |
| Master protocol | `.agent/MERIDIAN.md` |
| Kit architecture | `.agent/ARCHITECTURE.md` |
| **Templates (agents)** | `.agent/references/templates/INDEX.md` + `TEMPLATE_SOURCES.md` + `writing-guide.md` |
| Agents | `.agent/agents/` |
| Skills | `.agent/skills/` |
| Workflows | `.agent/workflows/` |
| Validation | `python3 .agent/scripts/validate_meridian.py <project-folder>` (`--json` for CI) |
| Instruction surfaces (maintainers) | `.agent/references/protocol/instruction-surfaces.md` |

---

## Quick reference

- **Governance:** `scrum-master`
- **Scope:** `product-owner`
- **Phase docs:** `technical-writer`
- **Security:** `security-champion`
- **Architecture:** `technical-architect`
- **Versions/sprints:** `sprint-planner`
- **US cook:** `story-maker`
- **US attest:** `story-checker`
- **Routing:** `meridian-routing`
