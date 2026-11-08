# Agent template — copy to `.agent/agents/{name}/agent.md`

```markdown
---
name: {agent-name}
description: Role in Meridian — primary outputs and slash commands. Does not …
mode: subagent
permission:
  read: allow
  grep: allow
  glob: allow
  bash: allow
  edit: deny
model: inherit
skills: {primary-skill}, update-decisions-log, meridian-routing
---

# {Title}

You are the **{role}** in Meridian: {one sentence mission}.

## Phase 0: Context check

1. …
2. …

---

## Mission

- …
- …

---

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/{command}` | … |

---

## Forbidden

| Forbidden | Why |
| --------- | --- |
| Product code | … |
| … | … |

---

## When to delegate

| Need | Delegate to |
| ---- | ----------- |
| … | `agent` → `/{command}` |

---

## Output

\`\`\`txt
Field:
Gaps:
Next:
\`\`\`
```

## Rules

- List every skill the agent may load in frontmatter `skills:`.
- Read-only operators: set `permission.edit: deny`; implementers set `edit: allow`.
- Always include forbidden + delegation tables.
- Match output format used by sibling agents (`security-champion`, `quality-owner`).
