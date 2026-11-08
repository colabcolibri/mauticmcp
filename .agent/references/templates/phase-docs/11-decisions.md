# Phase doc template — `11_decisions.md`

**Agent:** any + `update-decisions-log`  
**Product path:** `docs/11_decisions.md`  
**Entries:** SQLite `.meridian/meridian.db` only

---

## What this document is for

`11_decisions` explains **how decisions are recorded** — schema, CLI, prepend rules. The canonical history is in SQLite, not markdown files under `docs/decisions/`. This stub is rules + optional human index.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Copy stub; run first `prepend-decision` |
| Any material doc change | Prepend decision row; set affected doc to `review` if needed |
| Process change | Update “When to log” table; log meta-decision |

## How to complete

Keep JSON shape and CLI examples accurate. Optional index table is convenience — SQLite wins on conflict. Never instruct editing old decision rows.

## Depth checklist

- [ ] Entry shape documented
- [ ] CLI example uses `date` commands
- [ ] “When to log” table reflects team practice
- [ ] First decision logged at init


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Related

- `/update-decisions-log`, `decision-template.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Decision Log
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: []
blocks: []
---

# 11 — Decision log

Decisions live in **SQLite**: `.meridian/meridian.db` → table `decisions`.

`docs/11_decisions.md` is the human index (this file). The canonical store is the database, not JSON files under `docs/decisions/`.

## Entry shape

Each row stores `decision_date`, `entry_index` (0 = newest that day), and `payload_json`:

```json
{
  "time": "HH:MM",
  "title": "Objective title",
  "affected_document": "path/to/doc.md",
  "what_changed": "factual description",
  "why_changed": "context and motivation",
  "impact": "affected docs; mark review",
  "responsible": "role or person"
}
```

- `time` = real clock when logged (`date +"%H:%M"`). Do not round or invent.
- New entries are **prepended** (`entry_index` 0) for the calendar day.
- Never edit or delete old rows.

## Write

```bash
date +"%Y-%m-%d"
date +"%H:%M"
python3 .agent/scripts/meridian_delivery.py prepend-decision \
  --date "YYYY-MM-DD" \
  --time "HH:MM" \
  --title "…" \
  --affected-document "docs/…" \
  --what-changed "…" \
  --why-changed "…" \
  --impact "…" \
  --responsible "manager"
```

Workflow: `/update-decisions-log` + skill `update-decisions-log`.

## When to log

| Event | Log? |
| ----- | ---- |
| Project started (init) | yes — first entry |
| Phase doc `approved` → `review` after edit | yes |
| Security / architecture material change | yes |
| US scope change after refine | yes |
| Typo fix | no |

## Recent decisions (index)

_Manual optional index — source of truth remains SQLite._

| Date | Title | Affected |
| ---- | ----- | -------- |
| | Project started with Meridian | `docs/` |

## Gate

`status: approved` on this stub means rules are understood — not that history is complete.

