# Agent stations — folder layout (kit v3)

Each station is **one folder**; procedures are **skills**:

```txt
.agent/agents/{slug}/
  agent.md          persona, gates, skills: list (P1)
  references/       symlinks → .agent/skills/{skill}/

.agent/skills/{skill}/
  SKILL.md          procedure (canonical)
```

| Invoke | Path |
| ------ | ---- |
| Human (preferred) | `@slug` + request — agent loads skills |
| Optional slash | `/workflow` → alias to `@slug` + skill |
| Persona | `.agent/agents/{slug}/agent.md` |
| Procedure | `.agent/skills/{skill}/SKILL.md` |

## IDE adapters

`sync_kit.sh` creates:

```txt
.cursor/agents/{slug}.md  →  ../../.agent/agents/{slug}/agent.md
.cursor/skills/{skill}/   →  ../../.agent/skills/{skill}/
```

## Routing docs (not personas)

Station map, personas, areas: `.agent/references/agents/` — kit-wide routing, not per-station definitions.
