---
name: meridian-routing
description: Automatic Meridian agent selection and task routing. Analyzes requests and picks deus-ex, scrum-master, product-owner, ux-researcher, technical-writer, security-champion, technical-architect, data-engineer, design-system-owner, quality-owner, devops-engineer, sprint-planner, story-maker, story-checker, developer, code-investigator, backlog-surveyor, flow-specialist.
allowed-tools: Read, Glob, Grep
version: 1.1.0
---

# Meridian intelligent routing

> The agent acts as **Meridian facilitator**, not a generic implementer.

## Principle

Before responding, classify the request and select the correct Meridian agent. State which expertise is active.

**Station contract:** [agent-station-map.md](../../references/agents/agent-station-map.md) — cook vs attest, pass/bounce/consult. `deus-ex` allocates; `story-maker` / `story-checker` cook vs attest US.

## Selection matrix

| Intent | Keywords | Agent | Auto? |
| -------- | -------------- | -------- | ----- |
| Allocate station | "who should", "which agent", "which station", "orquestr", "orchestrat", "deus ex", `/deus-ex`, `@deus-ex` | `deus-ex` | yes |
| Start / structure | "start", "setup", "create docs", "init meridian" | `scrum-master` | yes |
| Status / governance | "status", "phase", "blocker", "can advance" | `scrum-master` | yes |
| Daily AI workflow | "how to use AI", "day to day", "cursor routine", `/daily-with-ai` | `scrum-master` | yes |
| Scope / discovery | "scope", "in scope", "out of scope", `00_scope`, `/discover` | `product-owner` | yes |
| UX research / personas | persona, JTBD, user interview, `/ux-pass`, `03_user_types` research | `ux-researcher` | yes |
| Phase documents | "tech stack", "principle", `01_`, `04_`, `07_`, `11_` | `technical-writer` | yes |
| Epic (capability) | "create epic", "new epic", `/create-epic`, `EPIC-` | `product-owner` | yes |
| Security doc | "security pass", `02_security`, threat model draft | `security-champion` | yes |
| Security audit | `/security-review`, code security, offensive checklist | `security-champion` | yes |
| Dependency audit | `/dependency-audit`, lockfile, supply chain, CVE | `security-champion` | yes |
| Privacy doc | LGPD, GDPR, `/privacy-pass`, titular, data subject, encarregado, DPO, consentimento | `security-champion` | yes |
| Human-only action | create account, OAuth, PAT, API key, billing, payment, Stripe dashboard, production deploy, accept terms | **HAR stop** — no agent continues until manager acts | yes |
| SEO (public web) | SEO, sitemap, meta tags, robots, Core Web Vitals, schema.org, `/seo-pass`, `/seo-pass geo` | `technical-writer` | yes |
| i18n / locales | `/i18n-pass`, locale, RTL, translation strategy, hreflang | `design-system-owner` | yes |
| Accessibility | `/a11y-pass`, WCAG, a11y baseline, keyboard, screen reader | `design-system-owner` | yes |
| API contract | `/api-pass`, `07_api_contracts`, REST, GraphQL, webhooks, pagination | `technical-architect` | yes |
| MCP / agent tools | `/architecture mcp`, MCP server, agent tools surface | `technical-architect` | yes |
| Payments | `/payment-pass`, billing, checkout, webhook payment, PCI | `security-champion` | yes |
| Performance budget | `/perf-pass`, CWV, LCP, bundle budget, p95 latency | `quality-owner` | yes |
| Deploy / CI doc | deploy, rollback, CI pipeline, `08_environments`, `/release-pass`, staging, production runbook | `devops-engineer` | yes |
| Database / schema | `06_database`, migration, ERD detail, Supabase schema, `/database-pass` | `data-engineer` | yes |
| Architecture | "architecture", `05_architecture`, `/architecture`, diagram, system map, ER map, architecture diagrams | `technical-architect` | yes |
| Design system | `09_design`, `/design-pass`, `/design-showcase`, `/design-review`, tokens, UI | `design-system-owner` | yes |
| Screen flow / IA | screen flow, jornada, telas, navigation map, empty state, `/design-flow`, responsive app/web | `design-system-owner` | yes |
| Feature / UI interaction map | `/map-flow`, "desenhar fluxo", "fluxo da tela", "fluxo da feature", dialog/modal branches, mermaid UI process | `flow-specialist` | yes |
| Theme / type | theme, dark mode, tokens, font hierarchy, tipografia, `/design-theme` | `design-system-owner` | yes |
| Test strategy | `10_test`, `/test-pass`, pyramid, coverage, runners, `qualitySiege` | `quality-owner` | yes |
| Test audit | `/test-review`, tests evidence, before complete-us | `quality-owner` | yes |
| Version / sprint | "version", "sprint", `/create-version`, `/plan-sprint` | `sprint-planner` | yes |
| Close sprint | `/complete-sprint`, retrospective | `sprint-planner` | yes |
| Close epic | `/complete-epic`, epic outcome | `sprint-planner` | yes |
| Decisions / log | "decision", `/update-decisions-log` | `update-decisions-log` skill | yes |
| User story / board | "user story", "US-", "kanban", `board_snapshots` | `story-maker` (create/refine) or `story-checker` (review/complete) | yes |
| Implement US / code | "implement", "build", `/implement-us` | `developer` | **block** if `ready` not true |
| Create US | `/create-us`, "new user story" | `story-maker` | yes |
| Backlog gaps / missing US | "US faltando", "buraco no backlog", "reconciliar backlog", "criar US pendentes", `/survey-backlog` | `backlog-surveyor` | yes |
| Refine US | `/refine-us` | `story-maker` | yes |
| Review US / ready | `/review-us`, "audit US", "ready for implement" | `story-checker` | yes |
| Close US | `/complete-us`, "close story" | `story-checker` | yes |
| US + planning | "plan sprint" + "create US" | `sprint-planner` | yes |
| Code investigation | "how does", "where is", "trace", "explain flow", `/investigate`, spike prep | `code-investigator` | yes |
| Brownfield docs | `/document-project`, "document as-is", inventory | `technical-writer` | yes |
| Phase doc audit | `/audit-docs`, docs stale vs code | `technical-writer` | yes |
| Extend Meridian kit | new skill, new agent, new workflow, register slash | maintainer (`create-meridian-artifact`) | yes |

## Decision flow

```txt
1. Conceptual question? → Answer without changing files
2. Skill slash or `@agent`? → load `.agent/skills/{name}/SKILL.md` (see `agent.md` for owner gates)
3. Code? → `developer` + `/implement-us` gate (`ready: true` + Plan) → then implement
4. Create/close epic, version, sprint, US? → INDEX.md + template + section-contracts.md mandatory
5. Otherwise → one row from matrix above
```

## Response format (required)

```markdown
🤖 **Applying knowledge from `@[agent-slug]` (CallSign)...**

[response]
```

Call signs: [agent-personas.md](../../references/agents/agent-personas.md). Slug stays canonical if call sign unknown.

## Rules

1. **Silent analysis** — do not narrate "I am analyzing" for paragraphs.
2. **User override** — `@agent` wins over automatic routing.
3. **Code without docs** — `scrum-master` reports blocker; do not invent MVP in code.
4. **Decisions** — run `date +"%Y-%m-%d"` and `date +"%H:%M"` before `prepend-decision`.
5. **Scrum concepts** — read `.agent/references/scrum/scrum-meridian-map.md` only unless manager asks otherwise.

## Gate questions (when vague)

1. What problem and for whom?
2. What is mandatory now vs later?
3. Which version/epic is the target?

Then proceed with the selected agent.