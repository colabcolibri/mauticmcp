---
name: security-code
description: Audits implemented code against docs/02_security.md and US acceptance. Use with /security-review. Report only — no product code.
allowed-tools: Read, Glob, Grep, Bash
---

# Security code (Meridian)

> Attest the **increment** against the standard in `02`. Do not rewrite `02` here (`security-doc`). Do not run a pentest exploit.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/security-review` | Audit code vs `02` + US (no code) |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/implementation-security-checklist.md` | **Mandatory** |
| `references/offensive-checklist.md` | **Mandatory** — `offensive` mode or STRIDE walk |
| `docs/02_security.md` | Contract |
| Target US | `meridian_delivery.py show US-XXXX --full` when scoped |

## When to trigger

- `/security-review`
- Before `/complete-us` on Must US with security acceptance
- Suspected leak, missing authz, injection surface in **code**


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Audit codebase surfaces vs `02` + open Must US |
| `US-XXXX` | **us-scope** | Audit code and acceptance for that US only |
| `offensive` | **offensive** | Threat-model walk + abuse scenarios — read `offensive-checklist.md` (checklist-only, no exploits) |

---

## Procedure

1. Require `02` at least `draft`.
2. Walk `implementation-security-checklist.md` (use `offensive-checklist.md` when mode is `offensive` or STRIDE requested).
3. Report only. Route: doc → `/security-pass`; plan → `/refine-us`; code → `/implement-us`; lockfile → `/dependency-audit`.
4. `technical-architect` may **consult** this skill; must not run `/security-review` as owner or set `ready`/`✅`.

## Output

```txt
Security code review:
US:
Critical findings:
Route: /security-pass | /refine-us | /implement-us | /dependency-audit
```

## Workflow steps (from `/security-review`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: SECURITY REVIEW

RULES:
1. Read 02_security.md + implementation-security-checklist.md
2. Check: secrets, authz, input validation, logging, dependencies cited in Plan
3. Compare US Acceptance security criteria vs code paths (grep/read)
4. Classify gaps: doc fix (/security-pass) | code fix (US) | both
5. Never mark 02 approved — human only
```

---
```
