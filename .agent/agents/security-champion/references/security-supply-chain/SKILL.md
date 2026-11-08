---
name: security-supply-chain
description: Reviews lockfiles, dependency policy, and supply-chain posture. Use with /dependency-audit. Report only.
allowed-tools: Read, Glob, Grep, Bash
---

# Security supply chain (Meridian)

> Lockfiles and install hygiene. Distinct from `security-doc` (policy in `02`) and `security-code` (app code).

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/dependency-audit` | Lockfiles and supply chain report |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/supply-chain-checklist.md` | **Mandatory** |
| `docs/02_security.md` | Declared dependency policy |
| Lockfiles | package-lock, pnpm-lock, poetry.lock, etc. |

## When to trigger

- `/dependency-audit`
- Material lockfile change on a US
- CVE / pin / unused dep questions


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Inventory lockfiles + manifest hygiene for active stack |
| `US-XXXX` | **us-scope** | Dependencies introduced or touched by that US |

---

## Procedure

1. Read `supply-chain-checklist.md`.
2. Report only — run audit CLIs when the manager approves.
3. Do not weaken pins without `update-decisions-log`.

## Output

```txt
Supply chain:
Lockfiles:
Findings:
Next: /security-pass | /implement-us
```

## Workflow steps (from `/dependency-audit`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: DEPENDENCY AUDIT

RULES:
1. Read 01_tech_stack.md, 02_security.md § dependencies, 08_environments.md
2. Locate lockfiles (package-lock, pnpm-lock, poetry.lock, Cargo.lock, go.sum, etc.)
3. Note: direct vs transitive risk, unpinned deps, known audit command for stack
4. Suggest 02/08 updates or US follow-ups — no silent approve
```

---
```
