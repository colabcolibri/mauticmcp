# Kit references — index

> **Navigation hub** for `.agent/references/`. Templates and phase-doc shells stay in `templates/`; historical audits in `plans/`.

## Read order (manager)

| Order | File | Purpose |
| ----- | ---- | ------- |
| 1 | [guides/how-to-use.md](./guides/how-to-use.md) | Extension vs chat, what you type |
| 2 | [guides/start-here.md](./guides/start-here.md) | Concepts, phases, gates |
| 3 | [guides/usage-guide.md](./guides/usage-guide.md) | Recipes by situation |
| 4 | [guides/agents-help.md](./guides/agents-help.md) | Slash commands, agents, steps |

## Folders

| Folder | Audience | Contents |
| ------ | -------- | -------- |
| [guides/](./guides/) | Manager + agents | Onboarding and day-to-day narrative |
| [protocol/](./protocol/) | Maintainers + agents | Kit governance, surfaces, trust, artifacts |
| [agents/](./agents/) | Agents + routing | Personas, areas, station map |
| [scrum/](./scrum/) | Manager + agents | Scrum ↔ Meridian mapping |
| [templates/](./templates/) | Agents | Registry, contracts, delivery templates |
| [plans/](./plans/) | Maintainers | Historical improvement audits (not loaded by default) |

## Quick lookup

| Need | File |
| ---- | ---- |
| Station folder layout (v2) | [../agents/README.md](../agents/README.md) — `{slug}/agent.md` + `references/` |
| Who owns `/ux-pass`? | [agents/agent-station-map.md](./agents/agent-station-map.md) |
| Call sign for Iris | [agents/agent-personas.md](./agents/agent-personas.md) |
| Upgrade from harness 1.x | [protocol/kit-v2-migration.md](./protocol/kit-v2-migration.md) |
| Where procedures live (v2) | [protocol/station-references.md](./protocol/station-references.md) |
| Where to edit when protocol changes | [protocol/instruction-surfaces.md](./protocol/instruction-surfaces.md) |
| US field detail | [protocol/artifact-reference.md](./protocol/artifact-reference.md) |
| Bugs, spikes, ceremonies | [scrum/scrum-meridian-map.md](./scrum/scrum-meridian-map.md) |
| Commit after `/complete-us` | [protocol/commit-after-us-close.md](./protocol/commit-after-us-close.md) |
| IDE adapters / harness bridge | [protocol/ide-integration.md](./protocol/ide-integration.md) |

## Layout

```txt
.agent/references/
  INDEX.md          ← you are here
  guides/           human onboarding + commands lookup
  protocol/         kit contract + maintainer map
  agents/           routing, personas, areas
  scrum/            delivery mapping (+ optional textbook)
  templates/        artifact registry + phase-doc shells
  plans/            archived maintainer plans
```
