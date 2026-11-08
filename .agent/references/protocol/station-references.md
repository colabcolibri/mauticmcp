# Station skills — agents + skills (kit v3)

> Procedures live in **`.agent/skills/`** only. **No workflows.** Invoke `/skill-name` or `@agent`.

## Layers

```txt
Human  →  /us-create, /data-engineering   (skill slash)
       →  @story-maker, @data-engineer     (agent mention)
       →  .agent/skills/{name}/SKILL.md    (procedure — single source of truth)
       →  docs/                            (artifacts)
```

| Layer | Invoke? | Purpose |
| ----- | ------- | ------- |
| **Skill** | Yes (`/us-create`) | Procedure, modes, checklists, CLI |
| **Agent** | Yes (`@story-maker`) | Persona, gates, which skills to load |
| **Workflow** | **Removed** | Was redundant alias — do not recreate |

## Rule

**One source of truth:** `.agent/skills/{name}/SKILL.md` — never duplicate in `agent.md`.

## Shared skills

| Skill | Used by |
| ----- | ------- |
| `meridian-routing` | All stations |
| `update-decisions-log` | Most stations |
| `init-project` | scrum-master, product-owner, technical-writer |
| `discover-product` | product-owner, ux-researcher |
| `create-meridian-artifact` | Maintainers |

## Adding a domain skill

1. Create `.agent/skills/{skill-name}/SKILL.md` (+ checklists in same folder).
2. Add to owner `agent.md` frontmatter `skills:` list.
3. Symlink `.agent/agents/{owner}/references/{skill-name}` → `../../../skills/{skill-name}`.
4. Update `agent-station-map.md`, `meridian-routing`, `agents-help.md`.
5. **Do not** create `.agent/workflows/`.

## IDE adapter

`sync_kit.sh` symlinks `.cursor/skills/` and `.cursor/agents/` — not commands.
