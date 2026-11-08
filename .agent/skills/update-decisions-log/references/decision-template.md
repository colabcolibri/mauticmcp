# Decision template

Prepend via `meridian_delivery.py prepend-decision` — **never** edit old rows.

**Before CLI:** run `date +"%Y-%m-%d"` → `--date` and `date +"%H:%M"` → `--time` (24h local; real clock only).

## CLI (preferred)

```bash
python3 .agent/scripts/meridian_delivery.py prepend-decision \
  --date "$(date +"%Y-%m-%d")" \
  --time "$(date +"%H:%M")" \
  --title "Objective decision title" \
  --affected-document "path/to/doc.md" \
  --what-changed "factual description of delta" \
  --why-changed "context, constraint or learning that motivated" \
  --impact "list; mark docs that return to review" \
  --responsible "manager or role"
```

## Entry fields (stored in `payload_json`)

| Field | CLI flag |
| ----- | -------- |
| `time` | `--time` |
| `title` | `--title` |
| `affected_document` | `--affected-document` |
| `what_changed` | `--what-changed` |
| `why_changed` | `--why-changed` |
| `impact` | `--impact` |
| `responsible` | `--responsible` |

## When to use

- Scope, stack, security, users, epics, versions, architecture, database, API, environments, acceptance, agent governance.

## Forbidden

- `Write` on `docs/decisions/*.json` when `meridian.db` exists.
- Edit or delete old decision rows.
- Vague entry ("adjusted scope") without listed impact.

## After decision that changes `approved` doc

1. Run `prepend-decision`.
2. Change affected doc `status` to `review`.
3. Inform manager which re-approval is needed.
4. If a US drove or tracks the change → Plan **Related decisions**: `YYYY-MM-DD — title`.
