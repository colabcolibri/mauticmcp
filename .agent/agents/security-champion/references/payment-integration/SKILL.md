---
name: payment-integration
description: Payment and billing security contract — webhooks, PCI scope, idempotency. Stack-agnostic (Stripe, Adyen, etc. as examples only). Use for /payment-pass. Human owns provider dashboard and prod keys.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Payment integration (Meridian)

> **Scope:** `docs/02_security.md` § Payments + cross-refs in `06` / `07` webhooks. **Guidance only** — no provider SDK code in this skill.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/payment-pass` | Payment security contract — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/payment-checklist.md` | **Mandatory** |
| `docs/02_security.md`, `06_database.md`, `07_api_contracts.md` | When present |
| `docs/00_scope.md` | Billing in scope |
| Target US (`show US-XXXX --full`) | `us-align` mode |

## When to trigger

- Scope includes subscriptions, checkout, invoices, or marketplace payouts
- US touches webhooks, payment intents, or billing entities
- **HAR** for provider account, API keys, Connect onboarding, production mode


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on `02` § Payments |
| `bootstrap` | **bootstrap** | From scope → draft payment security skeleton |
| `US-XXXX` | **us-align** | Payment US → doc and webhook gaps |

---

## Procedure

```txt
- [ ] Confirm payments in scope — else skip
- [ ] payment-checklist.md
- [ ] Update 02 § Payments / billing (PCI scope, secrets, webhook verification, idempotency)
- [ ] Cross-check 06 retention for payment-related PII
- [ ] Cross-check 07 webhook rows if HTTP API
- [ ] prepend-decision on material payment architecture or subprocessors
```

## Output

```txt
Mode: full | bootstrap | us-align
02 payments section status:
Provider pattern (generic):
Webhook / idempotency gaps:
HAR items:
Next: /security-review | /api-pass | /refine-us | /implement-us
```
