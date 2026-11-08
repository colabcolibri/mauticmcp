---
name: test-review
description: Audits US tests field and Record evidence against docs/10_test_strategy.md. Use with /test-review. Report only — no product test code.
allowed-tools: Read, Glob, Grep, Bash
---

# Test review (Meridian)

> Attest **evidence** on the US. The document `10` is `test-strategy` (`/test-pass`). Execution of tests is `developer` inside `/implement-us`.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/test-review` | Audit US tests vs strategy (no code) |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/test-review-checklist.md` | **Mandatory** |
| `docs/10_test_strategy.md` | When the product uses automated tests |
| Target US | `meridian_delivery.py show US-XXXX --full` |

## When to trigger

- `/test-review`
- Before `/complete-us` on Must US with `tests: required`


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| `US-XXXX` | **us-scope** | Compare US Planned/Executed vs strategy (default) |
| `sprint` | **sprint** | All open Must US in active sprint with `tests: required` |

---

## Procedure

1. Load US from SQLite.
2. Walk `test-review-checklist.md`.
3. Report only. Route: strategy → `/test-pass`; plan → `/refine-us`; missing tests → `/implement-us`.
4. Do not set `tests_status: done` without Record evidence.

## Output

```txt
Test review:
US:
Gaps (doc):
Gaps (US):
Gaps (code):
Next: /test-pass | /refine-us | /implement-us | /complete-us
```

## Workflow steps (from `/test-review`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: TEST REVIEW

RULES:
1. Read 10_test_strategy.md (if exists) + test-review-checklist.md
2. Load US from SQLite — check tests, tests_status, Planned vs Executed
3. Verify pyramid level matches strategy (unit vs e2e)
4. Classify gaps: doc (/test-pass) | US (/refine-us) | code (/implement-us)
```

---
```
