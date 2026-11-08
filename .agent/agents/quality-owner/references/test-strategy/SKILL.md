---
name: test-strategy
description: Maintains docs/10_test_strategy.md and stack-aware test bootstrap — Vitest, Jest, Playwright, pytest. Use for /test-pass, test pyramid, coverage. Not /test-review (skill test-review).
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Test strategy (Meridian)

> **Escopo:** `docs/10_test_strategy.md`. Evidence audit is skill `test-review`.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/test-pass` | Create/update `10` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/test-strategy-checklist.md` | **Mandatory** — any pass on `10` |
| `references/test-stack-catalog.md` | **Mandatory** — pick test stack id |
| `references/ci-gates-catalog.md` | **Mandatory** at bootstrap |
| `references/stacks/{id}.md` | **Mandatory** — runner layout |
| Target US (`show US-XXXX --full`) | `us-align` mode |

## When to trigger

- `/test-pass`
- Create or deepen `10_test_strategy.md`
- Before `/refine-us` on Must US with `tests: required` (strategy refs in Plan)
- Stack change in `01_tech_stack.md`


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist pass on entire `10` |
| `bootstrap` | **bootstrap** | Run `quality-profile` → read `01_tech_stack.md` → pick test stack id → fill pyramid + runners; use `ci-gates-catalog.md` (gates **up to** profile) → coordinate with `devops-engineer` for CI rows in `08` |
| `US-XXXX` | **us-align** | Load US `--full`; map Acceptance tests → strategy sections |

---

## Procedure (test-pass)

```txt
Task progress:
- [ ] quality-profile — note qualitySiege; read agentic-quality-model.md if tier unclear
- [ ] Read 00_scope, 01_tech_stack, 04_principles, 08_environments
- [ ] test-stack-catalog.md → stacks/{id}.md
- [ ] ci-gates-catalog.md → CI/CD rows in docs/08 (up to profile tier)
- [ ] test-strategy-checklist.md → update 10
- [ ] US Plan refs / review follow-ups
```

## Output

```txt
Test strategy:
10_test_strategy status:
Stack id:
Sections updated:
US follow-ups:
Next: /test-review | /refine-us US-XXXX
```

## Workflow steps (from `/test-pass`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: TEST PASS

RULES:
0. Resolve profile: `python3 .agent/scripts/meridian_delivery.py quality-profile` — read `agentic-quality-model.md` when tier is unclear
1. If no 10_test_strategy.md → copy § Document stub from `.agent/references/templates/phase-docs/10-test-strategy.md`
2. Run mode procedure (full | bootstrap | us-align)
3. Walk test-strategy-checklist.md
4. Recommend /refine-us if Must US Plan missing test strategy refs
5. prepend-decision on material runner or coverage policy changes
```

---
```
