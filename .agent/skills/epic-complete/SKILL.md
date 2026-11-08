---
name: epic-complete
description: Closes a Meridian epic in SQLite after outcome review — confirms no open Must US, sets status complete. Use with /complete-epic EPIC-XX.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Complete epic (Meridian)

> **v11:** read/write epic via `meridian_delivery.py` — never `docs/epics/*.md`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `../epic-create/references/epic-template.md` | Close rules + status |
| `references/epic-close-checklist.md` | **Mandatory** — Must US + outcome bar |
| Target epic | `meridian_db_export.py . --entity epics --id EPIC-XX` |
| Hygiene | `meridian_delivery.py lifecycle-hygiene` / `lifecycle-eligible` |
| `../update-decisions-log/SKILL.md` | Follow-up decisions |
| `.agent/references/scrum/scrum-meridian-map.md` | Prefer new epic over reopen |

## Delivery commands

```bash
python3 .agent/scripts/meridian_db_export.py . --entity epics --id EPIC-16 --format raw
python3 .agent/scripts/meridian_delivery.py lifecycle-hygiene
python3 .agent/scripts/meridian_delivery.py update-epic EPIC-16 <<'EOF'
---
id: EPIC-16
title: ...
status: complete
versions: [v11]
profiles: [...]
outcome: "..."
---
# EPIC-16 — ...
(## Expected outcome confirmed; Notes may cite close date)
EOF
```

## Procedure

1. Export epic; list Must US — any status not in ✅/🚫/🧊 **blocks** (`update-epic` raises). Zero US also blocks.
2. Confirm outcome narrative still true; frontmatter `outcome` must be a real sentence.
3. Remind manager: large follow-ups → **new epic**, do not reopen `complete`.
4. Set frontmatter `status: complete`; `update-epic` with **full** exported markdown + status edit (do not rebuild epic from template memory).
5. `prepend-decision` if warranted.
6. Optionally run `lifecycle-hygiene` / `validate_meridian.py`.

## Output

```txt
Epic completed:
ID: EPIC-XX
Status: complete
Must US open blocked: none | [ids]
Outcome confirmed: yes | no
Decisions logged: yes | no
Next: check version eligibility | /create-epic (for follow-up) | /plan-sprint
```

## Forbidden

- Closing while real open Must US remain
- Silent reopen of `complete` → `active` for large new scope (create EPIC-YY instead)
