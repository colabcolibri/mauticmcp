---
name: security-privacy
description: Deepens LGPD (Brazil) and GDPR (EU/EEA) sections in docs/02_security.md. Use with /privacy-pass. Not legal advice.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Security privacy (Meridian)

> Privacy contract inside `02`. Same champion as security-doc; different procedure.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/privacy-pass` | LGPD + GDPR sections in `02` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/privacy-compliance-checklist.md` | **Mandatory** |
| `references/privacy-bootstrap.md` | **Mandatory** — bootstrap |
| `docs/02_security.md` | Existing privacy sections |
| `docs/03_user_types.md` | Roles vs data subjects |

## When to trigger

- `/privacy-pass`
- PII, consent, DPO/encarregado, data-subject rights in discovery or `02`


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Walk full `privacy-compliance-checklist.md` (LGPD + GDPR) |
| `bootstrap` | **bootstrap** | Read `00` + `01` → `privacy-bootstrap.md` → draft privacy § in `02` |
| `US-XXXX` | **us-align** | Load US `--full`; map PII acceptance → privacy sections |

---

## Procedure

1. Treat LGPD and GDPR as **separate** sections; N/A needs manager rationale.
2. Official URLs only (ANPD, Planalto, EUR-Lex, EDPB).
3. HAR for regulator portals or consoles that need a human login.
4. Product endpoints for export/delete → `/implement-us`, not this skill.

## Output

```txt
Privacy pass:
LGPD: filled | N/A (rationale)
GDPR: filled | N/A (rationale)
HAR:
Next: /security-pass | /security-review
```

## Workflow steps (from `/privacy-pass`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: PRIVACY PASS

RULES:
1. security-champion Phase 0
2. Determine jurisdictions (BR, EU, both, neither)
3. Run checklist per active jurisdiction
4. Update § Privacy — LGPD and § Privacy — GDPR in 02_security.md
5. Log material scope changes via prepend-decision
6. Report gaps — never claim legal compliance
```

---
```
