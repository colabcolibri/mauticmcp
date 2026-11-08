---
name: i18n-localization
description: Internationalization contract for UI products — locales, fallbacks, RTL, string strategy, formats. Stack-agnostic. Use for /i18n-pass. Doc only; implementation via /implement-us.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# i18n localization (Meridian)

> **Scope:** `docs/09_design_system.md` § Internationalization (and cross-links to `12` hreflang when public web). **Stack-agnostic** — document patterns, not framework APIs.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/i18n-pass` | Create/update i18n contract in `09` — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/i18n-checklist.md` | **Mandatory** — any `/i18n-pass` |
| `docs/00_scope.md`, `03_user_types.md` | Locales in scope |
| `docs/09_design_system.md` | Current contract |
| `docs/12_marketing_seo.md` | hreflang when indexable web |
| Target US (`show US-XXXX --full`) | `us-align` mode |

## When to trigger

- UI product with more than one locale or future locale expansion
- `/i18n-pass` after `/design-pass bootstrap` or before `/design-flow` on multi-locale products
- US Acceptance mentions translation, locale, or RTL


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on `09` i18n section |
| `bootstrap` | **bootstrap** | From `00` + `03` → draft locale policy in `09` |
| `US-XXXX` | **us-align** | Map US Acceptance locale criteria → doc gaps |

---

## Procedure

```txt
- [ ] Confirm UI in scope — else report skip
- [ ] i18n-checklist.md
- [ ] Update 09 § Internationalization (locales, default, fallback, RTL, string source of truth)
- [ ] Note hreflang / routing expectations for /seo-pass when public web
- [ ] prepend-decision on material locale or compliance-facing language policy
```

## Output

```txt
Mode: full | bootstrap | us-align
09 i18n section status:
Locales:
Gaps:
Skipped: yes | no — reason
Next: /design-flow | /seo-pass | /implement-us | human approve 09
```
