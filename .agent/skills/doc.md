# Meridian kit authoring

> **Maintainers:** use skill **`create-meridian-artifact`** (`.agent/skills/create-meridian-artifact/SKILL.md`) for the full procedure — skill, agent, workflow, registries, sync, validate.

This file is the lightweight entry point symlinked as `meridian-authoring` in IDE adapters.

---

## Quick links

| Need | Read |
| ---- | ---- |
| Full procedure + checklists | `create-meridian-artifact/SKILL.md` + `references/registry-checklist.md` |
| Surface map | `.agent/references/protocol/instruction-surfaces.md` |
| Agent/skill/workflow tables | `.agent/ARCHITECTURE.md` |
| Sync adapters | `./.agent/scripts/sync_kit.sh` |

---

## Skill folder layout

```txt
.agent/skills/skill-name/
  SKILL.md          # required — index + procedure
  references/       # optional — templates, long checklists
  scripts/          # optional
  assets/           # optional
```

| Scope | Path |
| ----- | ---- |
| Kit (this repo) | `meridian/.agent/skills/` |
| Client project | `<root>/.agent/skills/` |
| Cursor mirror | `<root>/.cursor/skills/` — **sync only, do not edit** |

---

## Minimal skill frontmatter

```yaml
---
name: my-skill
description: Does X in Meridian. Use when user asks for X.
allowed-tools: Read, Glob, Grep
---
```

Rules: `name` = folder name (kebab-case); `description` includes triggers.

---

## Layers

| Layer | Path | Role |
| ----- | ---- | ---- |
| Workflow | `.agent/workflows/{cmd}.md` | Slash command recipe |
| Agent | `.agent/agents/{name}/agent.md` | Persona, gates, output |
| Skill | `.agent/skills/{name}/SKILL.md` | Repeatable procedure |

**Order when adding a full operator:** skill → agent → workflow → registries → sync.

---

## Official kit skills (excerpt)

See `.agent/ARCHITECTURE.md` for the full table. Maintainer skill:

| Skill | Purpose |
| ----- | ------- |
| `create-meridian-artifact` | Add/change skill, agent, workflow, routing |

When adding any skill, update `ARCHITECTURE.md` and walk `create-meridian-artifact/references/registry-checklist.md`.
