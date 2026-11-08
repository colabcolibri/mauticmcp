---
name: epic-create
description: Creates a Meridian epic in SQLite after architecture is approved. Use when defining a new product capability before user stories.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create epic (Meridian)

> **v11:** epics live in SQLite — never create `docs/epics/*.md`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/writing-guide.md` | Epic prose + golden example |
| `.agent/references/scrum/scrum-meridian-map.md` | Epic lifecycle |
| `references/epic-template.md` | **Mandatory** — `body_markdown` shape |
| `docs/03_user_types.md` | Validate `profiles` |

## Delivery commands

```bash
python3 .agent/scripts/meridian_delivery.py list versions
python3 .agent/scripts/meridian_delivery.py create-epic --title "..." --versions "[v11]"
python3 .agent/scripts/meridian_delivery.py update-epic EPIC-15 <<'EOF'
---
id: EPIC-15
title: ...
status: active
versions: [v11]
profiles: [...]
outcome: "..."
---
# EPIC-15 — ...
(body per epic-template.md)
EOF
```

Never Write `docs/epics/`. Persist with `update-epic` on **stdin** (heredoc) — no scratch files.

## Preconditions

| Doc | Required status |
| --- | -------------- |
| `05_architecture.md` | `approved` |
| `00_scope.md` | in scope |
| `03_user_types.md` | `approved` |

## Procedure

1. Read `writing-guide.md` + `epic-template.md`.
2. `epic-create` (prints id) or use `next` from `list epics`.
3. Compose full markdown per template; `update-epic EPIC-XX` with markdown on stdin (heredoc).
4. Validate `profiles` vs `03_user_types.md`; `versions` vs `list versions`.
5. `prepend-decision` if boundaries change.

## Output

```txt
Epic created:
ID: EPIC-XX
Outcome:
Versions:
Profiles:
Narrative complete: yes | no
Next: /create-us for slices
```
