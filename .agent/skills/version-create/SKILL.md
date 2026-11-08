---
name: version-create
description: Creates a Meridian release row in SQLite. Use when defining a new product version before user stories.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create version (Meridian)

> **v11:** versions live in SQLite — never create `docs/versions/*.md`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/writing-guide.md` | Release prose |
| `references/version-template.md` | **Mandatory** |
| `docs/00_scope.md` | Scope alignment |

## Delivery commands

```bash
python3 .agent/scripts/meridian_delivery.py create-version --id v11 --title "Release name"
python3 .agent/scripts/meridian_delivery.py update-version v11 <<'EOF'
---
id: v11
title: ...
status: planned
outcome: "..."
---
# v11 — ...
(body per version-template.md)
EOF
```

Never Write `docs/versions/`. Persist with `update-version` on **stdin** (heredoc) — no scratch files.

## Preconditions

| Doc | Required status |
| --- | -------------- |
| `05_architecture.md` | `approved` |
| `00_scope.md`, `03_user_types.md` | aligned |

## Procedure

1. Read `writing-guide.md` + `version-template.md`.
2. `version-create` then refine body via `update-version` with markdown on stdin (heredoc).
3. `prepend-decision` if boundaries change.
4. `validate_meridian.py`

## Output

```txt
Version created:
ID: vX
Outcome:
Narrative complete: yes | no
Next: /plan-sprint → /create-us
```
