# Workflow template

Filename = slash without slash: `/investigate` → `investigate.md`

## Alias workflow (default — kit v3)

**Preferred human entry:** `@agent` in chat. Workflow is an optional slash alias — **no `## Task`**, no duplicated rules.

```markdown
---
description: One line — deliverable and owner.
---

# /{command} — {short title}

$ARGUMENTS

---

**Invoke:** @{agent-slug} — load skill `{skill-name}` and execute with `$ARGUMENTS`.

Slash is optional. Same work: **`@{agent-slug}`** + your request.

---
```

## Multi-skill alias

When one slash maps to multiple skills (e.g. `/plan-sprint`):

```markdown
**Invoke:** @{agent-slug} — load the skill that matches `$ARGUMENTS` among `version-create`, `sprint-create`.
```

## Procedure lives in skill

All steps, modes, checklists, and output → `.agent/skills/{skill-name}/SKILL.md` only.

## After creating

1. Add or update `.agent/skills/{skill}/SKILL.md`
2. Add skill to owner `agent.md` frontmatter + `references/` symlink
3. `.agent/rules/meridian.mdc` slash table (if new command)
4. `agent-station-map.md`, `meridian-routing`, `agents-help.md`
5. `./.agent/scripts/sync_kit.sh`
