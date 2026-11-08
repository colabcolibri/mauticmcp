# Schema — decision log (SQLite)

Storage: table `decisions` in `.meridian/meridian.db`.

| Column | Meaning |
| ------ | ------- |
| `decision_date` | `YYYY-MM-DD` calendar day |
| `entry_index` | `0` = newest that day; increases for older entries |
| `title` | denormalized title (also inside `payload_json`) |
| `payload_json` | full entry object (fields below) |

## Entry object (`payload_json`)

```json
{
  "time": "17:30",
  "title": "Objective title",
  "affected_document": "path/to/doc.md",
  "what_changed": "factual description",
  "why_changed": "context and motivation",
  "impact": "affected docs; mark review",
  "responsible": "role or person"
}
```

## Rules

| Field | Required | Format |
| ----- | ----------- | ------- |
| `time` | yes | `HH:MM` (24h) — **real clock** at log time (`date +"%H:%M"`) |
| `title` | yes | non-empty string |
| `affected_document` | yes | string |
| `what_changed` | yes | string |
| `why_changed` | yes | string |
| `impact` | yes | string |
| `responsible` | yes | string |

## Order

- **Prepend:** `prepend-decision` inserts at `entry_index` 0 and shifts older rows for that date.
- Days sorted by `decision_date` descending in `list decisions`.

## Write

```bash
python3 .agent/scripts/meridian_delivery.py prepend-decision --date YYYY-MM-DD ...
```

## Read

```bash
python3 .agent/scripts/meridian_delivery.py list decisions
python3 .agent/scripts/meridian_delivery.py show-decisions --date YYYY-MM-DD --json
```

## Validation

```bash
python3 .agent/scripts/validate_meridian.py <project-root>
```

When `meridian.db` exists, `docs/decisions/*.json` must not remain (legacy import only).

## Related

- Rules stub: `docs/11_decisions.md`
- Skill: `update-decisions-log`
- Protocol: `.agent/MERIDIAN.md` §8 Decision log
