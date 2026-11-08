# Instruction surfaces — where to edit when the protocol changes

> **Maintainer map.** When Meridian gains a new rule, artifact, command, or workflow step, walk the checklist in [Protocol change checklist](#protocol-change-checklist) and update every surface listed below.

**Canonical source:** `.agent/` (committed). Everything else is a mirror, runtime read, or extension code that must be updated separately.

---

## Golden rules

1. **Edit `.agent/` first** — never start in `.cursor/` or other IDE adapters.
2. **Run** `./.agent/scripts/sync_kit.sh` — refreshes `.cursor/`, `.claude/`, Codex, and `.opencode/` adapters.
3. **VS Code extension** — Help panels read `.agent/references/guides/` and `.agent/references/protocol/` at runtime after kit install/upgrade; command catalog and README are separate edits.
4. **Record the change** — `prepend-decision` in dogfood when the protocol itself changes.

---

## Layers at a glance

| Layer | Path | Audience | Edit rule | Priority |
| ----- | ---- | -------- | --------- | -------- |
| Master protocol | `.agent/MERIDIAN.md` | Agents + managers | **Canonical** | P0 |
| P0 rules | `.agent/rules/MERIDIAN.md`, `.agent/rules/meridian.mdc` | Agents (always-on) | **Canonical** | P0 |
| References index | `.agent/references/INDEX.md` | Manager + maintainers | **Canonical** | P0 |
| Human onboarding | `.agent/references/guides/start-here.md` | Manager | **Canonical** | P0 |
| Day-to-day guide | `.agent/references/guides/usage-guide.md` | Manager | **Canonical** | P0 |
| Commands & steps | `.agent/references/guides/agents-help.md` | Manager + agents | **Canonical** | P0 |
| Artifact templates | `.agent/references/templates/` + `TEMPLATE_SOURCES.md` | Agents | **Canonical** (see TEMPLATE_SOURCES for edit path) | P0 |
| Agent personas | `.agent/agents/{slug}/agent.md` | Agents | **Canonical** | P0 |
| Station references | `.agent/agents/{slug}/references/{pass}/` | Agents | **Canonical** | P0 |
| Shared skills | `.agent/skills/*/SKILL.md` + `references/` | Agents (cross-station) | **Canonical** | P0 |
| Slash workflows | `.agent/workflows/*.md` | IDE slash commands | **Canonical** | P0 |
| Scrum map | `.agent/references/scrum/scrum-meridian-map.md` | Manager + agents | **Canonical** | P1 |
| Kit architecture | `.agent/ARCHITECTURE.md`, `.agent/IDE_ADAPTERS.md` | Maintainers | **Canonical** | P1 |
| Distribution | `.agent/KIT_README.md`, `.agent/DISTRIBUTION.md` | Humans installing kit | **Canonical** | P2 |
| Repo README | `README.md` | GitHub visitors | **Canonical** | P2 |
| IDE adapters | `.cursor/`, `.claude/`, `.agents/skills/`, `.codex/` | Cursor / Claude Code / Codex | **Mirror** — sync only | — |
| VS Code help (runtime) | `.agent/references/guides/*.md`, `.agent/references/protocol/artifact-reference.md` | Extension user | Same as kit refs — edit `.agent/` | P0 |
| VS Code command catalog | `app-visual-studio/src/command-catalog.ts` | Extension user | **Canonical** for extension UX | P1 |
| VS Code README | `app-visual-studio/README.md` | Marketplace / GitHub | **Canonical** for extension | P2 |
| Validators | `.agent/scripts/validate_meridian.py`, `meridian_section_contracts.py` | CI + agents | **Canonical** when structure changes | P1 |

---

## Surface detail

### P0 — protocol & procedures (agents execute from here)

| What | Where | When to touch |
| ---- | ----- | ------------- |
| Full governance | `.agent/MERIDIAN.md` | New gates, prohibitions, lifecycle rules |
| Short rules | `.agent/rules/MERIDIAN.md` | P0 rule additions |
| Cursor always-on | `.agent/rules/meridian.mdc` | Slash table, required reading paths |
| Bootstrap / migration | `.agent/skills/init-project/SKILL.md` | Mode A/B, new artifacts (e.g. `docs/inventory/`) |
| Slash command | `.agent/workflows/{command}.md` | Command behavior, deliverables, next steps |
| Template registry | `.agent/references/templates/INDEX.md` | New artifact types |
| Template body | `.agent/references/templates/*.md` or skill `references/` per `TEMPLATE_SOURCES.md` | New sections, fields, checklists |
| Agent routing | `.agent/agents/{slug}/agent.md` | Who owns new artifacts |

### P0 — human narrative (managers read in IDE or repo)

| What | Where | When to touch |
| ---- | ----- | ------------- |
| Concepts & phases | `.agent/references/guides/start-here.md` | New phases, artifacts, folder tree |
| Situations & sequences | `.agent/references/guides/usage-guide.md` | New workflows (migrate, close US, etc.) |
| Numbered steps | `.agent/references/guides/agents-help.md` | New slash commands or groups |

### P1 — VS Code extension

| What | Where | Notes |
| ---- | ----- | ----- |
| Agents Help / Usage / Start Here panels | Reads `.agent/references/*.md` via `kit-references.ts` | Updates when kit is installed/upgraded |
| Command palette help | `app-visual-studio/src/command-catalog.ts` | Per-command summaries — edit when commands ship |
| Extension guide panels | `app-visual-studio/src/kit-reference-panels.ts`, `help-webview-html.ts` | Onboarding UX |
| Extension onboarding | `app-visual-studio/README.md` | Install, F5, kit sync |
| Board / Deliverables | `planning-panels.ts`, `board-editor-panel.ts` | Read SQLite via `meridian_db_export --format planning` |

### Mirrors (do not edit)

| Path | Regenerated by |
| ---- | -------------- |
| `.cursor/commands/`, `.cursor/skills/`, `.cursor/agents/`, `.cursor/rules/` | `sync_kit.sh` |
| `.claude/commands/`, `.claude/agents/` | `sync_kit.sh` |
| `.agents/skills/` (incl. `workflow-*`), `.codex/agents/*.toml`, `AGENTS.md` (symlink) | `sync_kit.sh` |
| `.opencode/commands/`, `.opencode/agents/`, `.opencode/skills/` | `sync_kit.sh` |

---

## Protocol change checklist

Use this when adding or changing protocol behavior (example: **as-is inventory** for Mode B migration).

### 1. Define in kit (P0)

- [ ] `.agent/MERIDIAN.md` — bootstrap / lifecycle section
- [ ] `.agent/skills/init-project/SKILL.md` — procedure
- [ ] `.agent/workflows/init-meridian.md` — deliverables + next steps
- [ ] New template if needed — `.agent/references/templates/` + `INDEX.md` + `TEMPLATE_SOURCES.md`
- [ ] `.agent/references/guides/start-here.md` — concepts + `docs/` tree
- [ ] `.agent/references/guides/usage-guide.md` — situations + step table
- [ ] `.agent/references/guides/agents-help.md` — command group row
- [ ] `.agent/rules/MERIDIAN.md` — tier table if new artifact owner
- [ ] `.agent/agents/{slug}/agent.md` — template protocol rows if agent-owned
- [ ] `.agent/references/templates/lifecycle.md` — flow diagram

### 2. Sync mirrors

- [ ] `./.agent/scripts/sync_kit.sh`

### 3. Extension & onboarding (P1–P2)

- [ ] `app-visual-studio/src/command-catalog.ts` — if new shipped command
- [ ] `README.md` — one-line mention if user-facing
- [ ] `.agent/ARCHITECTURE.md` — if new layer or skill

### 4. Validation & dogfood

- [ ] `.agent/scripts/validate_meridian.py` — only if new required paths
- [ ] `python3 .agent/scripts/validate_meridian.py . --sqlite-only --strict-kit-md`
- [ ] Decision log entry via `meridian_delivery.py prepend-decision` when protocol changes

---

## Quick lookup — “I changed X, where do I edit?”

| Change | Edit first | Also update |
| ------ | ---------- | ----------- |
| New slash command | `.agent/workflows/{name}.md` + skill | `agents-help.md`, `meridian.mdc` table, `usage-guide.md`, `sync_kit.sh` |
| New kit skill/agent/workflow | `create-meridian-artifact` skill | `ARCHITECTURE.md`, `registry-checklist.md`, sync + validate |
| New delivery artifact | Template + skill + `INDEX.md` | `start-here.md`, `lifecycle.md`, validator if required |
| Migration / bootstrap step | `init-project/SKILL.md`, `init-meridian.md` | `usage-guide.md`, `start-here.md` |
| New `docs/` folder (optional) | `start-here.md`, `doc-templates.md` | init skill |
| Multi-product / monorepo (resolver) | `projects-manifest-template.md`, `usage-guide.md`, `start-here.md`, `MERIDIAN.md`, `agentic-quality-model.md` | `resolve-meridian-projects.ts`, `meridian-workspace.ts`, `meridian-workspace-picker.ts`, `meridian-context.ts`, `package.json`, `command-catalog.ts`, `05_architecture.md` |
| Multi-product UI context | `usage-guide.md`, `start-here.md`, `agents-help.md`, `projects-manifest-template.md` | `webview-project-context.ts`, `*-webview-html.ts`, `planning-panels.ts`, `board-editor-panel.ts`, `command-catalog.ts`, `app-visual-studio/README.md`, `05_architecture.md` § UI structure |
| Agent behavior only | `.agent/agents/{name}/agent.md` | Usually nothing else |
| Extension-only feature | `app-visual-studio/` + phase docs | Kit only if protocol changes |
| New extension view (SQLite-backed) | `app-visual-studio/src/*-webview-html.ts`, `planning-panels.ts`, `load-*.ts`, `extension.ts`, `package.json`, `command-catalog.ts` | `meridian_db_export.py --format …`, `05_architecture.md` § UI structure, `agents-help.md`, `README.md` |

---

## Multi-product (EPIC-13) — full surface checklist

When changing **several `docs/` trees in one repo** or **project context in the IDE**, touch every row below.

### Kit narrative (P0)

- [ ] `.agent/MERIDIAN.md` — folder tree + multi-product paragraph
- [ ] `.agent/references/guides/start-here.md` — `docs/` tree + monorepo table
- [ ] `.agent/references/guides/usage-guide.md` — [Multiple Meridian projects](#multiple-meridian-projects) section
- [ ] `.agent/references/guides/agents-help.md` — IDE extension commands table
- [ ] `.agent/references/templates/projects-manifest-template.md` — active project + UI + `qualitySiege`
- [ ] `.agent/references/protocol/agentic-quality-model.md` — tiers, migration, validator WARN
- [ ] `.agent/references/templates/delivery-connector-schema.md` — `options.qualitySiege`, `quality-profile` CLI
- [ ] `.agent/workflows/status.md` — resolve active `docs/` in procedure
- [ ] `.agent/skills/init-project/SKILL.md` — Phase 5 manifest proposal

### Extension (P1)

- [ ] `app-visual-studio/src/resolve-meridian-projects.ts`
- [ ] `app-visual-studio/src/meridian-workspace*.ts`, `meridian-context.ts`
- [ ] `app-visual-studio/src/webview-project-context.ts`
- [ ] `app-visual-studio/src/*-webview-html.ts`, `planning-panels.ts`, `board-editor-panel.ts`
- [ ] `app-visual-studio/src/load-*.ts` when new SQLite export format is needed
- [ ] `app-visual-studio/src/command-catalog.ts`
- [ ] `app-visual-studio/README.md`, `CHANGELOG.md`

### Dogfood architecture (P1)

- [ ] `docs/05_architecture.md` — § Activation and `docs/` resolution + § UI structure

### Mirrors

- [ ] `./.agent/scripts/sync_kit.sh`

---

## Related maps

| Map | Path |
| --- | ---- |
| Template canonical paths | `.agent/references/templates/TEMPLATE_SOURCES.md` |
| Kit architecture | `.agent/ARCHITECTURE.md` |
| IDE adapters | `.agent/IDE_ADAPTERS.md` |
| Scrum ↔ Meridian | `.agent/references/scrum/scrum-meridian-map.md` |
| Multi-product manifest | `.agent/references/templates/projects-manifest-template.md` |
