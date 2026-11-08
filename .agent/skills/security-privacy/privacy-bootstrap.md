# Privacy bootstrap — infer jurisdictions from scope and stack

Use with `/privacy-pass bootstrap` after `01_tech_stack.md` is drafted.

---

## Read first

1. `docs/00_scope.md` — audiences, geography, in-scope data features
2. `docs/01_tech_stack.md` — auth, analytics, payments, hosting region
3. `docs/02_security.md` — existing posture and PII inventory

---

## Inference table

| Signal in docs | Likely jurisdiction | Action |
| -------------- | ------------------- | ------ |
| Users in Brazil, PT-BR primary, BRL, `.com.br` | LGPD | Fill § Privacy — LGPD |
| EU/EEA users, GDPR cited, EUR, multi-language EU | GDPR | Fill § Privacy — GDPR |
| Global SaaS without clarity | Both possible | List assumption in Gaps; ask manager |
| Local-only CLI, no PII | Neither | Mark both N/A with justification |
| Stripe + email auth | Both often apply | Draft subprocessors row; do not skip |

---

## Bootstrap procedure

1. Copy stub sections **Privacy — LGPD** and **Privacy — GDPR** if missing from `phase-docs/02-security.md`.
2. Fill PII inventory and minimization first — privacy sections depend on it.
3. For each jurisdiction **in scope**, complete table rows with `_TBD_` only where interview gap exists — move unknowns to **Gaps / open questions**.
4. Link official references from `privacy-compliance-checklist.md` (do not paste statute text).
5. **HAR:** if bootstrap requires logging into ANPD or cloud console to verify settings → stop per `rules/MERIDIAN.md`.

---

## Output

```txt
Privacy bootstrap:
LGPD: required | N/A — reason
GDPR: required | N/A — reason
Sections updated in 02:
Gaps added:
Official refs pointed:
Next: /privacy-pass full | manager interview | /refine-us
```
