---
name: sprint-create
description: Creates a Meridian sprint row in SQLite linked to a version. Use when planning execution slices within a release.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create sprint (Meridian)

> **v11:** sprints live in SQLite — never create `docs/sprints/*.md`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/INDEX.md` | Before any sprint create |
| `references/sprint-template.md` | **Mandatory** |
| Parent version | `meridian_delivery.py list versions` |

## Delivery commands

```bash
python3 .agent/scripts/meridian_delivery.py list sprints --version v11
python3 .agent/scripts/meridian_delivery.py create-sprint --version v11 --title "Sprint name" --stories US-0001,US-0002
python3 .agent/scripts/meridian_delivery.py update-sprint v11-S1 <<'EOF'
---
id: v11-S1
version: v11
title: ...
status: planned
---
# v11-S1 — ...
(body per sprint-template.md)
EOF
```

Never Write `docs/sprints/`. Persist with `update-sprint` on **stdin** (heredoc) — no scratch files.

## Preconditions

- Version row exists (`list versions`).
- Version is `planned` or `active`.
- `05_architecture.md` `approved` before creating new US.

## Procedure

1. Read `INDEX.md` + `sprint-template.md`.
2. `list sprints --version vX` → next id `vX-Sn`.
3. `sprint-create` then `update-sprint` with full markdown on stdin (heredoc) when body needs refinement.
4. New US → `/create-us` after gates.

## Output

```txt
Sprint created:
ID: vX-SY
Version:
Stories:
Saved: yes | no
```
