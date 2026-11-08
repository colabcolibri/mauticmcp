---
name: performance-budget
description: Performance budgets and measurement contract — CWV, bundle/size targets, CI gates. Stack-agnostic. Use for /perf-pass on 10_test_strategy. Doc only.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Performance budget (Meridian)

> **Scope:** `docs/10_test_strategy.md` § Performance budgets (and CI rows in `08` when gates exist). Complements `/test-pass` — does not replace unit/e2e pyramid.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/perf-pass` | Performance contract — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/performance-checklist.md` | **Mandatory** |
| `docs/10_test_strategy.md`, `08_environments.md` | Current runners and CI |
| `docs/12_marketing_seo.md` | CWV when public web |
| `docs/09_design_system.md` | UI weight assumptions |
| Target US (`show US-XXXX --full`) | `us-align` mode |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on `10` performance section |
| `bootstrap` | **bootstrap** | Draft budgets after `/test-pass bootstrap` |
| `US-XXXX` | **us-align** | Perf Acceptance → measurable criteria in `10` |

---

## Procedure

```txt
- [ ] performance-checklist.md
- [ ] Update 10 § Performance budgets (metrics, targets, tools, environments)
- [ ] Align CI advisory or blocking gates in 08 per quality-profile
- [ ] prepend-decision on material budget or gate change
```

## Output

```txt
Mode: full | bootstrap | us-align
10 performance section status:
Budgets defined:
CI gates:
Gaps:
Next: /test-pass | /implement-us | /seo-pass
```
