# i18n checklist — `/i18n-pass`

> Stack-agnostic contract. Name the **strategy** (e.g. message catalogs, ICU, resource files); do not mandate a single library.

## Bootstrap

- [ ] Locales in scope listed (BCP 47 tags)
- [ ] Default locale and fallback chain documented
- [ ] Single-locale product states `_n/a_` with reason — skip deep pass

## Full pass

- [ ] String extraction strategy (where keys live; who owns copy)
- [ ] Pluralization and gender rules noted when grammar requires
- [ ] Date, time, number, currency formatting policy per locale
- [ ] RTL layout rule when Arabic, Hebrew, or other RTL in scope
- [ ] Locale switcher UX (persist preference; no silent wrong locale)
- [ ] Server vs client locale resolution documented for web/app
- [ ] Content not in UI (emails, PDFs, push) included or explicitly out of scope
- [ ] hreflang / URL locale strategy cross-linked to `12` when public SEO applies

## US alignment

- [ ] Acceptance locale criteria map to documented locales
- [ ] No hardcoded user-visible strings in Plan without i18n note

## Out of scope

- Professional translation vendor selection (human procurement)
- Legal translation of contracts (legal review)
