# Meridian kit scripts

> Python 3 **stdlib only** (no `pip install`). Entry points for humans, CI, extension, and agents.

## Layout (v11)

```txt
.agent/scripts/
  lib/              # shared Python modules
  migrate/          # v1 Markdown → SQLite (one-shot)
  test/             # smoke tests (root shims for CI)
  dev/              # local fixtures (meridian-teste)
  *.py              # runtime CLI + shims (stable paths for extension/CI)
  *.sh              # kit install / sync / package
```

## Runtime (use daily)

| Script | Purpose |
| ------ | ------- |
| `lib/meridian_db.py` | Library: connect, migrations, `upsert_*`, export, board snapshots |
| `lib/meridian_markdown_parse.py` | Library: frontmatter + section parsing |
| `lib/meridian_section_contracts.py` | Library: structural validation helpers |
| `lib/meridian_delivery_form.py` | Library: form ↔ markdown (extension) |
| `bootstrap_meridian_db.py` | Shim — same as `meridian_delivery.py bootstrap` (prefer facade) |
| `meridian_delivery.py` | **Agent facade** — reads `delivery.json`, dispatches connector (`counts`, `show`, `create-us`, `patch-record`, …); `quality-profile` resolves `qualitySiege` tier |
| `meridian_db_cli.py` | SQLite driver (implementation; facade calls this) |
| `lib/meridian_board_columns.py` | Derived kanban `column` for the kit HTML snapshot (not the extension export schema) |
| `meridian_board_serve.py` | Foreground HTML monitor: `127.0.0.1`, ephemeral port, GET snapshot/events |
| `../board` | Human shortcut → same serve (`python3 .agent/board`) |
| `validate_meridian.py` | Governance validator (`--strict-kit-md`, `--json`; deprecated-agent check always on kit) |
| `meridian_delivery_form.py` | Shim — re-exports `lib/meridian_delivery_form.py` for extension path checks |

## Shell (maintainers)

| Script | Purpose |
| ------ | ------- |
| `sync_kit.sh` | Regenerate all IDE adapters (`.cursor/`, `.claude/`, Codex, `.opencode/`) |
| `uninstall-meridian-kit.sh` | Remove Meridian adapters (and optionally kit + gitignore entries) — never touches `docs/` or `.meridian/` |
| `install-meridian-kit.sh` | Install `.agent/` into a target project |
| `package-kit.sh` | Build `meridian-kit-*.tar.gz` |

## CI / tests

| Script | Purpose |
| ------ | ------- |
| `run_kit_tests.py` | Run all `test/test_*.py` (CI + local) |
| `test_meridian_db_schema.py` | Shim → `test/test_meridian_db_schema.py` |
| `test_story_dependencies.py` | Shim → `test/test_story_dependencies.py` |
| `test_implement_gate.py` | Shim → `test/test_implement_gate.py` |

## Migration lane (`migrate/`)

Run once per project when importing from branch `meridian-v1-old`:

| Script | Purpose |
| ------ | ------- |
| `migrate_md_to_sqlite.py` | Import delivery `.md` → DB |
| `verify_md_sqlite_parity.py` | Gate before purge |
| `purge_delivery_md.py` | Remove delivery `.md` after verify |
| `backfill_summaries.py` | Fill empty `summary` columns |

## Dev (`dev/`)

| Script | Purpose |
| ------ | ------- |
| `seed_meridian_teste_db.py` | Minimal delivery rows for `meridian-teste` smoke |

## Who calls what

| Consumer | Scripts |
| -------- | ------- |
| **Kit HTML board** | `.agent/board` → `meridian_board_serve.py` |
| **Cursor / Claude agents** | `meridian_delivery.py`, `validate_meridian.py` |
| **VS Code extension** | `validate_meridian.py`, `meridian_db_export.py`, `meridian_delivery_form.py` (path check) |
| **GitHub Actions** | `validate_meridian.py --strict-kit-md`, `run_kit_tests.py`, extension `typecheck`/`lint`/`test` |
| **Pre-commit** | `bootstrap` + `validate_meridian.py --sqlite-only --strict-kit-md` |

## Python requirement

**Yes — Python 3 is required** for validate, SQLite tooling, and extension board when using the DB. Stdlib only — no virtualenv. See `docs/08_environments.md`.
