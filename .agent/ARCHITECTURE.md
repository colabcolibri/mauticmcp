# Meridian agent architecture

> Structure of agents, skills, rules and scripts — kit v3 (skills-only, no workflows).

---

## Purpose

| Layer | File | Audience |
| ------ | ------- | ------- |
| Kit monorepo | `README.md` | Humans (GitHub, onboarding) |
| Portable kit | `.agent/` | Copy to client projects; Antigravity, ag-kit, Cursor, Claude Code |
| IDE adapters | `.cursor/`, `.claude/`, `.agents/skills/`, `.codex/` (local, gitignored) | Cursor, Claude Code, Codex (symlinks + generated TOMLs → `.agent/`) — see [IDE_ADAPTERS.md](./IDE_ADAPTERS.md) |
| Always-on rules | `.agent/rules/meridian.mdc` + `.agent/rules/MERIDIAN.md` | Agents |
| Master protocol | `.agent/MERIDIAN.md` | Full governance |
| Operations | `.agent/agents`, `skills` | Personas and procedures |
| Human references | `.agent/references/` | `INDEX.md`, `guides/`, `protocol/`, `agents/`, `scrum/`, `templates/` |

The VS Code extension (`app-visual-studio/`) is the optional monitor for Meridian folders; it is not the source of truth. Help panels read `.agent/references/guides/` and `.agent/references/protocol/` at runtime — see [instruction-surfaces.md](./references/protocol/instruction-surfaces.md) when the protocol changes.

### Why `.agent` and `.cursor`?

- **`.agent/`** — Antigravity convention; copyable to projects and other tools.
- **`.cursor/`** — **local** adapter (generated symlinks; **do not commit**).

**Edit in `.agent/`** and run `./.agent/scripts/sync_kit.sh` to recreate adapters in `.cursor/`, `.claude/`, Codex paths, and `.opencode/` (required after clone).

---

## Directory structure

```txt
.agent/                    # canonical source (Antigravity / distribution)
  MERIDIAN.md
  rules/MERIDIAN.md
  agents/                    # {slug}/agent.md + references/ → skills/
    README.md
  skills/                    # {name}/SKILL.md — canonical procedures
  board-ui/                  # HTML monitor (python3 .agent/board)
  scripts/
    validate_meridian.py
    migrate_us_v2_structure.py
    sync_kit.sh
  references/                # INDEX, guides/, protocol/, agents/, scrum/, templates/, plans/

.cursor/                   # Cursor adapter (local, gitignored — sync_kit.sh)
  rules/meridian.mdc       # alwaysApply
  skills/                  # symlinks → .agent/skills/
  agents/                  # symlinks → .agent/agents/{slug}/agent.md

.opencode/                 # OpenCode adapter (local, gitignored — sync_kit.sh)
  agents/
  skills/
```

---

## Rule priority

```txt
P0  .agent/rules/MERIDIAN.md
P1  .agent/MERIDIAN.md + .agent/agents/{agent}/agent.md
P2  .agent/skills/  (+ agent `references/` symlinks → skills)
      + references/templates/         artifact structure (canonical)
```

Skills are invoked as `/skill-name` in chat (e.g. `/us-create`); agents as `@slug`. See [kit-v3-migration.md](./references/protocol/kit-v3-migration.md).

---

## Agents

Eighteen stations. Each agent lists **skills** in frontmatter (domain + shared). Procedures live in `.agent/skills/`. See [station-references.md](./references/protocol/station-references.md).

| Agent | Purpose | Shared skills |
| ----- | ------- | ------------- |
| `deus-ex` | Allocate next station (pass only) | meridian-routing, update-decisions-log |
| `product-owner` | `00_scope`, discovery, epics | discover-product, init-project, update-decisions-log, meridian-routing |
| `technical-writer` | Phase docs `01`, `04`, `11`; SEO operator | init-project, update-decisions-log, meridian-routing |
| `ux-researcher` (Iris) | `03_user_types`, `/ux-pass` | discover-product, update-decisions-log, meridian-routing |
| `data-engineer` (Mnemosyne) | `06_database.md` | update-decisions-log, meridian-routing |
| `devops-engineer` (Vulcan) | `08_environments.md` | update-decisions-log, meridian-routing |
| `security-champion` (Janus) | `02`, security passes | update-decisions-log, meridian-routing |
| `technical-architect` (Daedalus) | `05`, `07`, `/api-pass`, MCP | update-decisions-log, meridian-routing |
| `design-system-owner` (Harmonia) | `09`, design/i18n/a11y passes | update-decisions-log, meridian-routing |
| `quality-owner` (Themis) | `10`, test/perf passes | update-decisions-log, meridian-routing |
| `sprint-planner` (Hesperus) | versions, sprints, epic close | update-decisions-log, meridian-routing |
| `story-maker` (Penelope) | US create + refine | update-decisions-log, meridian-routing |
| `story-checker` (Argus) | US review + complete | update-decisions-log, meridian-routing |
| `developer` (Hephaestus) | `/us-implement` | update-decisions-log, meridian-routing |
| `scrum-master` (Kairos) | Governance, status, init | init-project, update-decisions-log, meridian-routing |
| `code-investigator` (Hermes) | `/investigate` read-only | update-decisions-log, meridian-routing |
| `backlog-surveyor` (Metis) | `/survey-backlog` reconcile + gap-led US | update-decisions-log, meridian-routing |
| `flow-specialist` (Ariadne) | `/map-flow` on-demand interaction maps | update-decisions-log, meridian-routing |

Each agent includes: phases 0/-1, mission, **station references**, prohibitions, output format, delegation.

---

## Skills (`.agent/skills/`)

Domain procedures (e.g. `us-create`, `data-engineering`, `design-system`) and shared utilities (`meridian-routing`, `update-decisions-log`, …). Each station's `agent.md` declares which skills to load.

**Agent mirror:** `agents/{slug}/references/{skill}/` symlinks → `skills/{skill}/` for template registry paths.

See `.agent/skills/` and skill `create-meridian-artifact` to extend the kit.

**Workflows removed (v3.1):** `.agent/workflows/README.md` is a redirect only. Full command map: [agents-help.md](./references/guides/agents-help.md).

---

## Scripts

```bash
# Structure + semantic validation (US Plan/Record, epic prose, board sync hints)
python3 .agent/scripts/validate_meridian.py <project-root>
python3 .agent/scripts/validate_meridian.py <project-root> --json   # CI

# One-time US schema migration (flat sections → Intent/Plan/Record/Boundaries)
python3 .agent/scripts/migrate_us_v2_structure.py <project-root>
python3 .agent/scripts/migrate_us_v2_structure.py <project-root> --restore-preamble

# IDE adapters (after clone or kit changes)
./.agent/scripts/sync_kit.sh
```

---

## Authority

1. User instruction
2. `.agent/MERIDIAN.md`
3. `.agent/rules/MERIDIAN.md`
4. Agents
5. Skills

---

## Difference vs Antigravity kit

| Antigravity | Meridian |
| ----------- | -------- |
| `README.md` + `rules/GEMINI.md` | `README.md` (kit repo) + `.agent/` + `rules/MERIDIAN.md` |
| 37 code/stack skills | 10 document governance skills |
| `intelligent-routing` (technical domains) | `meridian-routing` (docs/US phases) |
| Plan files `{task-slug}.md` | `docs/` phases `00`–`11` + US |
| Long agents for implementation | Agents for documentation and gates before code |
