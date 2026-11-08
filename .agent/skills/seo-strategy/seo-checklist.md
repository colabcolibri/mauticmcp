# SEO checklist — `/seo-pass`

> Secondary implementation reference: [Google Search Central documentation](https://developers.google.com/search/docs). Primary contract remains `docs/12_marketing_seo.md`.

## Bootstrap

- [ ] Product has public indexable routes in scope
- [ ] `12_marketing_seo.md` stub copied from `phase-docs/12-marketing-seo.md`
- [ ] Indexable routes table started from `05_architecture` or app router

## Full pass

- [ ] Every public route has canonical URL policy
- [ ] Title/description patterns defined per template
- [ ] `sitemap.xml` strategy (static path or generator)
- [ ] `robots.txt` documented
- [ ] No staging URLs in examples
- [ ] CWV targets or documented N/A
- [ ] Schema.org types per major page type
- [ ] hreflang documented if multi-locale
- [ ] Analytics/search console setup noted — **HAR** for human login

## Out of scope

- Paid ads / SEM
- Legal cookie consent text (see `/privacy-pass` + `02`)
