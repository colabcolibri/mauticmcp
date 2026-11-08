---
name: release-ops
description: Maintains docs/08_environments.md — local run, env vars, CI/CD catalog, deploy and rollback runbooks. Use for /release-pass. Human executes git push and production deploy.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Release ops (Meridian)

> **Scope:** `docs/08_environments.md`. CI gate **definitions** coordinate with `quality-owner` (`10` + `ci-gates-catalog`); **pipelines** live here.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/release-pass` | Create/update `08` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/release-checklist.md` | **Mandatory** |
| `docs/01_tech_stack.md`, `05_architecture.md` | Always |
| `docs/10_test_strategy.md` | CI gates alignment |
| `quality-profile` CLI output | Tier caps for CI |
| Target US (`show US-XXXX --full`) | `us-align` |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist pass on entire `08` |
| `bootstrap` | **bootstrap** | Read `01` + `10` (if any) → env matrix + CI summary |
| `US-XXXX` | **us-align** | Load US `--full`; map deploy/test Acceptance → `08` gaps |

---

## Procedure

```txt
- [ ] Read 01, 05, 10 (if exists)
- [ ] release-checklist.md
- [ ] If no 08 → copy stub from phase-docs/08-environments.md
- [ ] Document local, staging, prod — no secret values in docs
- [ ] Rollback path per environment
- [ ] prepend-decision on material deploy or CI policy changes
```

## Forbidden in this skill

- `git push`, merge PR, production deploy execution — **human manager only**
- Product feature code

## Output

```txt
Mode: full | bootstrap | us-align
08_environments status:
Environments documented:
CI/CD rows:
Rollback:
US follow-ups:
Next: human approve 08 | /test-pass bootstrap | manager deploy
```
