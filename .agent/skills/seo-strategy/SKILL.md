---
name: seo-strategy
description: Maintains optional docs/12_marketing_seo.md and seo-pass workflow for public indexable web products. Use with /seo-pass when scope includes marketing sites or public app routes.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# SEO strategy (Meridian)

> **Optional operator** — skip for CLI-only or private products.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/phase-docs/12-marketing-seo.md` | **Mandatory** — guide + stub |
| `references/seo-checklist.md` | **Mandatory** — `/seo-pass` modes except `geo` |
| `../geo-optimization/references/geo-checklist.md` | **Mandatory** — `/seo-pass geo` |

## When to trigger

- `/seo-pass` workflow (modes: full, bootstrap, review, geo)
- `/seo-pass geo` — load `geo-optimization` procedure for AI discoverability section
- Public routes, sitemap, meta tags, Core Web Vitals before release
- Manager asks for SEO audit (doc only — code via `/implement-us`)


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on entire `12` |
| `bootstrap` | **bootstrap** | Infer routes from `05` + stack → create `12` from stub |
| `review` | **review** | Pre go-live gap report |
| `geo` | **geo** | GEO / AI discoverability section in `12` — read `geo-checklist.md` |

---

## Procedure

1. Confirm product has indexable public web in `00_scope` — else report skip.
2. **bootstrap:** infer routes from `05` + repo; draft `12_marketing_seo.md` from stub.
3. **full:** walk `seo-checklist.md`; report gaps.
4. **HAR** for Search Console / analytics account setup.
5. Never set `approved` — human only.

## Output

```txt
SEO pass:
12_marketing_seo status:
Routes documented:
Gaps:
Next: /implement-us | human approved
```
