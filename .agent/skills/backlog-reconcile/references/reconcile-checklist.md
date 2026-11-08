# Reconcile checklist — `/survey-backlog`

Use on every run. Each gap row needs **evidence** (path, doc §, CLI output, or report quote).

## Dimension 1 — Phase doc gaps

- Scan `## Gaps` / `Gaps / open questions` in `docs/02_security.md` through `docs/10_test_strategy.md`, `docs/05_architecture.md`, `docs/09_design_system.md` when present.
- Rows marked as blocking backlog or "US" / "code fix" → candidate gap.
- Skip rows already cited in an open US Plan (`meridian_delivery.py show --full`).

## Dimension 2 — Inventory (brownfield)

- `docs/inventory/as-is.md` — capabilities with confidence `high` or `medium` without a US id in the row or Plan.
- Epic candidate labels → map to existing `EPIC-XX` only; do not create epics here.

## Dimension 3 — SQLite delivery

```bash
python3 .agent/scripts/meridian_delivery.py list epics
python3 .agent/scripts/meridian_delivery.py list versions
python3 .agent/scripts/meridian_delivery.py list us --limit 500
python3 .agent/scripts/meridian_delivery.py counts
```

- Epics with zero child US (when epic is `active` or `planned`).
- US with broken `depends_on` targets.
- Open US (`status: ❌`) whose Acceptance clearly duplicates a closed sibling — flag for human merge, do not auto-close.

## Dimension 4 — Specialist pass outputs (chat context)

When the manager pasted or referenced recent reports:

- `/audit-docs`, `/design-review`, `/security-review`, `/test-review` lines that say **code fix (US)** or **US fix**.
- Tie each line to evidence; do not resurrect stale reports without asking.

## Dimension 5 — Code vs backlog (sample)

- Only when `apply` or manager asked for code cross-check.
- Use narrow grep/read — full traces stay with `code-investigator` `/investigate`.
- Flag: merged feature paths with no open US covering that slice.

## Prioritization

| Priority | Signal |
| -------- | ------ |
| P0 | `05` § Gaps marked blocks backlog; security/test Must gaps |
| P1 | Inventory `high` without US; epic with no US |
| P2 | Doc gaps non-blocking; duplicate-slice warnings |

## Apply gate

Before `create-us` in **`apply`** mode:

1. `05_architecture` frontmatter `status: approved`.
2. Target `EPIC-XX` and `version` exist in SQLite.
3. Manager confirmed gap ids (same turn explicit "apply" or listed gap ids in `$ARGUMENTS`).
4. Every created US: `ready: false`; full Intent per `us-create` + `writing-guide.md`.
5. `prepend-decision` when batch size ≥ 3 or scope/epic mapping was ambiguous (run `date` first).

## Gap row id format

`GAP-001`, `GAP-002`, … per run — stable within the report for manager approval.
