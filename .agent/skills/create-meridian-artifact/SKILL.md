---
name: create-meridian-artifact
description: Maintainer procedure to add or change Meridian kit artifacts — skill, agent, workflow, routing, and every registry surface. Use when extending the harness, creating /investigate, or onboarding a new slash command.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create Meridian artifact (maintainer)

> **Canonical map:** `.agent/references/protocol/instruction-surfaces.md`  
> **This skill:** step-by-step procedure + per-artifact checklists in `references/`.

Use when adding or changing anything in `.agent/` that agents or managers invoke: **skill**, **agent**, **workflow** (slash command), or **delivery template**.

**Do not** edit `.cursor/`, `.claude/`, or `.agents/skills/` directly — run `sync_kit.sh` after `.agent/` changes.

---

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/registry-checklist.md` | **Mandatory** — full surface list by artifact type |
| `references/skill-template.md` | Creating a new skill |
| `references/agent-template.md` | Creating a new agent |
| `references/workflow-template.md` | Creating a new slash workflow |
| `.agent/references/protocol/instruction-surfaces.md` | Protocol-level changes, EPIC-13, validator |
| `.agent/ARCHITECTURE.md` | Agent/skill/workflow tables |
| `.agent/skills/meridian-routing/SKILL.md` | New intent → agent routing row |

---

## When to trigger

- "Create a new skill / agent / workflow for Meridian"
- "Register `/foo` in the kit"
- "What files do I update when adding an agent?"
- Extending the harness (`code-investigator`, `backlog-surveyor`, new operator, new pass/review)
- After creating artifacts — verify nothing was missed

---

## Decision: what are you adding?

| You need | Create | Also register |
| -------- | ------ | ------------- |
| Station procedure (one owner) | `.agent/agents/{owner}/references/{pass}/` (`PROCEDURE.md` + checklists) | Workflow → `@owner` only; `station-references.md` |
| Shared cross-station procedure | `.agent/skills/{name}/SKILL.md` — **only if 2+ agents** | Agent frontmatter on each consumer |
| Persona + gates + output | `.agent/agents/{name}/agent.md` | Shared skills only in frontmatter; routing matrix |
| Human slash command | `.agent/workflows/{name}.md` | `meridian.mdc` table; `agents-help.md` |
| Delivery file shape | `.agent/references/templates/` + `INDEX.md` | `TEMPLATE_SOURCES.md` |
| Routing only | `meridian-routing` matrix row | `agents-help.md` intent lookup |

**Order of work (recommended):** agent references → workflow → registries → sync → validate. Add `.agent/skills/` only when truly shared.

---

## Procedure

### Phase 0 — scope

1. Name in **kebab-case** (`investigate-codebase`, `code-investigator`, `investigate`).
2. Classify: read-only report | doc pass | delivery authoring | implementation.
3. Pick **owning agent** (existing or new).
4. Read `references/registry-checklist.md` for the artifact type — print the checklist in output.

### Phase 1 — station references (default)

1. Create `.agent/agents/{owner}/references/{pass-name}/PROCEDURE.md` (+ checklists).
2. Do **not** create `.agent/skills/{pass-name}/` unless a second agent shares the procedure.

### Phase 1b — shared skill (rare)

1. Copy `references/skill-template.md` only when **2+ agents** need the same procedure.
2. Create `.agent/skills/{skill-name}/SKILL.md`.

### Phase 2 — agent (if needed)

1. Copy `references/agent-template.md`.
2. Create `.agent/agents/{agent-name}.md`.
3. List skills in frontmatter (including `meridian-routing` unless read-only sub-call).
4. Define: Phase 0, mission, forbidden, delegation, output block.

### Phase 3 — workflow (if needed)

1. Copy `references/workflow-template.md`.
2. Create `.agent/workflows/{command}.md` (filename = slash without `/`).
3. Wire: `@owner` + path to `agents/{owner}/references/{pass}/` checklist.
4. Modes via `$ARGUMENTS` table when applicable.
5. **No product code** unless workflow is `/implement-us`.

### Phase 4 — registries (mandatory)

Walk **every** applicable row in `references/registry-checklist.md`:

| Priority | Surface | Typical |
| -------- | ------- | ------- |
| P0 | `meridian-routing` | New intent keywords |
| P0 | `agents-help.md` | Agent group + slash row + intent lookup |
| P0 | `meridian.mdc` | Slash commands table |
| P1 | `ARCHITECTURE.md` | Agents / skills / workflows tables |
| P1 | `usage-guide.md` | New situation recipe |
| P1 | `instruction-surfaces.md` | Quick lookup row if new pattern |
| P2 | `README.md` | One line if user-facing |
| P2 | `app-visual-studio/src/command-catalog.ts` | Only extension palette commands — **not** chat slash |
| P2 | `create-meridian-artifact` → `registry-checklist.md` § **K** | New extension view (SQLite-backed tab) |

**Auto-sync (no manual edit):** `.cursor/commands/`, `.cursor/skills/`, `.cursor/agents/`, `.agents/skills/workflow-*`, `.codex/agents/*.toml`, `.opencode/*` — via sync script.

### Phase 5 — sync and validate

```bash
./.agent/scripts/sync_kit.sh
python3 .agent/scripts/validate_meridian.py . --sqlite-only --strict-kit-md
```

### Phase 6 — dogfood decision (kit protocol changes)

If behavior of the **Meridian protocol** changed (not just a new optional operator):

1. `date +"%Y-%m-%d"` and `date +"%H:%M"`
2. `meridian_delivery.py prepend-decision` with rationale and files touched.

---

## Anti-patterns

| Wrong | Right |
| ----- | ----- |
| Edit `.cursor/commands/foo.md` | Edit `.agent/workflows/foo.md` + sync |
| Skill body with 500-line checklist | `references/checklist.md` + "when to read" table |
| Agent without forbidden section | Explicit forbidden + delegate table |
| Workflow without output block | Copy pattern from `/security-review` |
| New slash only in workflow file | Also `meridian.mdc` + `agents-help.md` |
| `name:` mismatch with folder | Folder `foo/` → `name: foo` |

---

## Output

```txt
Artifact type: skill | agent | workflow | template | routing
Names: skill=… agent=… workflow=/…
Files created:
Registries updated:
Sync: done | pending
Validate: pass | fail (…)
Checklist gaps:
Next: test /command in chat | prepend-decision | PR
```
