# Phase doc template — `12_marketing_seo.md` (public web only)

**Agent:** `technical-writer` + `seo-strategy` skill  
**Product path:** `docs/12_marketing_seo.md`  
**Skip:** CLI-only, private APIs, desktop apps without indexable pages  
**Deepen:** `/seo-pass bootstrap` → `full` before public go-live

---

## What this document is for

`12_marketing_seo` is the **discoverability contract** for public, indexable surfaces: metadata, URLs, sitemaps, robots, Core Web Vitals targets, structured data, and i18n/hreflang when applicable. It does not replace `09_design_system` (visual UX) or privacy/cookie compliance in `02_security`.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Only when `00_scope` includes public website, landing, blog, or marketing app routes |
| New public routes | Update route table + sitemap |
| Pre go-live | `/seo-pass full` |
| Stack change (SSR framework) | Review rendering strategy (SSG/SSR/CSR) |

## How to complete each section

Document **indexable routes** explicitly. Meta title/description patterns per template type. Sitemap path and generation (static vs dynamic). `robots.txt` policy. CWV budgets (LCP, INP, CLS). Schema.org types per page type. hreflang only when multi-locale is in scope.

## Depth checklist

- [ ] Public routes listed with canonical URLs
- [ ] Meta pattern documented per route type
- [ ] Sitemap + robots strategy defined
- [ ] CWV targets or N/A with reason
- [ ] Structured data types named per template

## Mid-project review (doc drift)

Re-open when marketing routes, domain, or locale strategy changes.

## Cross-doc checks

- Public app paths match `05_architecture`
- UI performance aligns with `09` if present
- Cookie/analytics consent cross-ref `02` privacy sections

## Related

- `seo-strategy` skill, `/seo-pass`
- Secondary: [Google Search Central](https://developers.google.com/search/docs) (implementation hints, not law)

---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section.

---
title: Marketing SEO
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [00_scope.md, 01_tech_stack.md, 05_architecture.md]
blocks: []
---

# 12 — Marketing SEO

> **Optional.** Skip for non-indexable products. **Deepen:** `/seo-pass bootstrap` after public routes known.

## Indexable surfaces

| Route / path | Page type | Index? | Canonical URL pattern |
| ------------ | --------- | ------ | --------------------- |
| `/` | landing | yes | |
| | | | |

## Metadata policy

| Page type | Title pattern | Description pattern | OG image |
| --------- | ------------- | ------------------- | -------- |
| | | | |

## Technical SEO

| Concern | Approach |
| ------- | -------- |
| Sitemap | path + update frequency |
| robots.txt | allow/disallow rules |
| SSR/SSG/CSR | rendering per route |
| Canonical tags | strategy |
| hreflang | locales or N/A |

## Core Web Vitals targets

| Metric | Target | Measurement |
| ------ | ------ | ----------- |
| LCP | | |
| INP | | |
| CLS | | |

## Structured data

| Page type | Schema.org type | Notes |
| --------- | --------------- | ----- |
| | Organization / WebSite / Product | |

## Gaps / open questions

| # | Gap | Owner |
| - | --- | ----- |

## Gate

Human `approved` before public marketing go-live when SEO is in scope.
