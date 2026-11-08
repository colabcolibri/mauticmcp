---
name: accessibility
description: Accessibility baseline (WCAG-oriented) for UI products. Stack-agnostic. Use for /a11y-pass on 09. Not pixel QA — /design-review attests implementation.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Accessibility (Meridian)

> **Scope:** `docs/09_design_system.md` § Accessibility baseline. **Doc only** — patterns and acceptance criteria, not component library APIs.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/a11y-pass` | Create/update a11y baseline in `09` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/a11y-checklist.md` | **Mandatory** — any `/a11y-pass` |
| `docs/09_design_system.md` | Theme, type, screen flows |
| `docs/03_user_types.md` | Assistive-tech or disability-facing personas |
| Target US (`show US-XXXX --full`) | `us-align` mode |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on `09` a11y baseline |
| `bootstrap` | **bootstrap** | Draft baseline after `/design-pass bootstrap` |
| `US-XXXX` | **us-align** | Map UI US Acceptance → a11y gaps |

---

## Procedure

```txt
- [ ] Confirm UI in scope — else report skip
- [ ] a11y-checklist.md
- [ ] Update 09 § Accessibility baseline (target level, focus, motion, forms, status)
- [ ] Align with design-theme (contrast uses semantic tokens)
- [ ] prepend-decision on material a11y level or legal accessibility commitment
```

## Output

```txt
Mode: full | bootstrap | us-align
09 a11y baseline status:
Target level:
Gaps:
Next: /design-review | /implement-us | human approve 09
```
