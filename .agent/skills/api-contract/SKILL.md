---
name: api-contract
description: API and boundary contract design — REST, GraphQL, RPC, CLI, IPC. Stack-agnostic. Use for /api-pass on 07_api_contracts. Not app code.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# API contract (Meridian)

> **Scope:** `docs/07_api_contracts.md`. Matches `02` auth and `05` boundaries. **No invented endpoints** in brownfield — evidence from repo.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/api-pass` | Create/update `07` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/api-contract-checklist.md` | **Mandatory** |
| `.agent/references/templates/phase-docs/07-api-contracts.md` | Structure |
| `docs/02_security.md`, `05_architecture.md`, `06_database.md` | Cross-check |
| Target US (`show US-XXXX --full`) | `us-align` mode |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on entire `07` |
| `bootstrap` | **bootstrap** | Stub `07` from `05` + repo evidence |
| `US-XXXX` | **us-align** | API US → contract rows and gaps |

---

## Procedure

```txt
- [ ] api-contract-checklist.md
- [ ] Update 07 (style, auth, errors, endpoints, pagination, webhooks, rate limits)
- [ ] Internal contracts when no HTTP API (CLI, extension IPC, scripts)
- [ ] prepend-decision on breaking API or versioning policy change
```

## Output

```txt
Mode: full | bootstrap | us-align
07_api_contracts status:
API style:
Gaps vs 02/05:
Next: /security-review | /payment-pass | /refine-us | /implement-us
```
