# Station reference template — copy to `.agent/agents/{slug}/references/{pass}/PROCEDURE.md`

> **Kit v12:** domain procedures live under the owning agent, not `.agent/skills/`. Use `.agent/skills/` only for cross-station shared skills (see `station-references.md`).

```markdown
# {Title}

> One-sentence purpose. Loaded by @{agent-slug} — humans invoke `/workflow-name` or @{agent-slug}, not this path directly.

## Selective reading

| File | When to read |
| ---- | ------------ |
| `{checklist}.md` | **Mandatory** — … |

## When to trigger

- `/workflow-name` or keywords …
- …

## Procedure

### Phase 0 — context
1. …

### Phase 1 — …
1. …

## Forbidden

| Forbidden | Why |
| --------- | --- |
| … | … |

## Output

\`\`\`txt
Field:
Next:
\`\`\`
```

## Rules

- Folder name = pass name (kebab-case), sibling to `PROCEDURE.md`.
- Keep `PROCEDURE.md` under ~120 lines; move checklists to the same folder.
- Delivery templates: edit canonical path per `TEMPLATE_SOURCES.md`; registry symlinks under `.agent/references/templates/`.
