# Delivery connector profile

> **Machine config:** `.meridian/delivery.json` at the Meridian **product** package root.  
> **Human note (optional):** log connector changes via `prepend-decision` (SQLite).

Agents and skills call **`meridian_delivery.py`** — not `meridian_db_cli.py` directly. The facade reads this file and dispatches to the configured connector driver.

---

## Schema (version 1)

```json
{
  "version": 1,
  "connector": "sqlite",
  "package_root": ".",
  "options": {}
}
```

| Field | Required | Description |
| ----- | -------- | ----------- |
| `version` | yes | Always `1` for this schema |
| `connector` | yes | Backend id — kit ships `sqlite` only |
| `package_root` | yes | Path to folder with `docs/` (relative to repo or absolute) |
| `options` | no | Connector-specific; empty object for sqlite. May include `qualitySiege`: `kit` \| `standard` \| `full` (see `agentic-quality-model.md`) |

### `options.qualitySiege` (optional)

Single-product repos without `.meridian/projects.json` declare the optional robust validation tier here:

```json
{
  "version": 1,
  "connector": "sqlite",
  "package_root": ".",
  "options": {
    "qualitySiege": "standard"
  }
}
```

Monorepos: prefer `projects[].qualitySiege` in `.meridian/projects.json` (wins over `delivery.json`).

Resolve: `python3 .agent/scripts/meridian_delivery.py quality-profile`

### Future: `postgres` (not implemented)

```json
{
  "version": 1,
  "connector": "postgres",
  "package_root": ".",
  "options": {
    "url_env": "MERIDIAN_DATABASE_URL"
  }
}
```

Secrets live in **environment variables** — never in `delivery.json`.

---

## Bootstrap

```bash
python3 .agent/scripts/meridian_delivery.py bootstrap
# or
python3 .agent/scripts/bootstrap_meridian_db.py .
```

Creates/upgrades `meridian.db` and writes default `delivery.json` when missing.

---

## Facade commands

| Command | Purpose |
| ------- | ------- |
| `config` | Print resolved `delivery.json` |
| `bootstrap` | DB + default delivery profile |
| `quality-profile` | Resolve `qualitySiege` tier + expected gates for active package |
| `connectors` | List registered drivers |

All **delivery verbs** pass through unchanged:

```bash
python3 .agent/scripts/meridian_delivery.py counts
python3 .agent/scripts/meridian_delivery.py show US-0115 --full
python3 .agent/scripts/meridian_delivery.py create-us --title "..." --epic EPIC-01 --version v1
python3 .agent/scripts/meridian_delivery.py update-us US-0115 <<'EOF'
---
id: US-0115
...
---
# body
EOF
python3 .agent/scripts/meridian_delivery.py update-epic EPIC-15 <<'EOF'
---
id: EPIC-15
...
---
# body
EOF
python3 .agent/scripts/meridian_delivery.py update-version v11 <<'EOF'
---
id: v11
...
---
# body
EOF
python3 .agent/scripts/meridian_delivery.py update-sprint v11-S1 <<'EOF'
---
id: v11-S1
...
---
# body
EOF
python3 .agent/scripts/meridian_delivery.py implement-gate US-0115
python3 .agent/scripts/meridian_delivery.py prepend-decision --date YYYY-MM-DD --time HH:MM ...
```

Override package root: `--package-root path/to/product`.

**Form export (extension):** still `meridian_db_export.py` for v11 — wired to sqlite until a second driver exists.

---

## Git

| File | Commit? |
| ---- | ------- |
| `.meridian/delivery.json` | **Yes** — project config |
| `.meridian/meridian.db` | **No** — gitignored runtime data |

---

## Skills rule

In every delivery skill `## Delivery commands` section:

1. Read `.meridian/delivery.json` if unsure of connector.
2. Run `python3 .agent/scripts/meridian_delivery.py <verb> …`.
3. Do **not** hardcode `meridian_db_cli.py` or database paths in skill prose.

Canonical verb list: same as `sqlite-delivery-operations.md` § Agent workflow (facade forwards to sqlite driver today).
