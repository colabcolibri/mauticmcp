---
name: sprint-complete
description: Closes a Meridian sprint in SQLite after sprint review — fills Retrospective, sets status complete, logs decisions. Use with /complete-sprint vX-SY.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Complete sprint (Meridian)

> **v11:** read/write sprint via `meridian_delivery.py` — never `docs/sprints/*.md`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `../sprint-create/references/sprint-template.md` | Close rules + Retrospective |
| `references/retrospective-checklist.md` | **Mandatory** — evidence bar; placeholder is invalid |
| Target sprint | `meridian_db_export.py . --entity sprints --id vX-SY` |
| Listed US | `meridian_delivery.py show US-XXXX` per story in sprint |
| `../update-decisions-log/SKILL.md` | Retrospective decisions |

## Delivery commands

```bash
python3 .agent/scripts/meridian_db_export.py . --entity sprints --id v11-S1 --format markdown
python3 .agent/scripts/meridian_delivery.py update-sprint v11-S1 <<'EOF'
---
id: v11-S1
version: v11
status: complete
...
---
# v11-S1 — ...
(## Retrospective filled)
EOF
```

## Procedure

1. Export sprint markdown (`meridian_db_export` or `show`); read US statuses via `show`.
2. Summarize delivery vs `goal` and `done_when`.
3. **Add** filled `## Retrospective` per `retrospective-checklist.md` (What worked / What to improve with facts). Placeholder `_(fill at sprint close)_` is rejected by `update-sprint`.
4. Set frontmatter `status: complete`. Persist with `update-sprint` full markdown on stdin. CLI **raises** if linked US are not all ✅/🚫/🧊, the sprint has no stories, or Retrospective is placeholder.
5. `prepend-decision` if warranted.
6. `validate_meridian.py`

## Output

```txt
Sprint completed:
ID: vX-SY
Status: complete
US delivered: N ✅ / N 🔶 / N ❌
Retrospective filled: yes | no
Decisions logged: yes | no
Next: /plan-sprint | /create-us
```
