# Performance budget checklist — `/perf-pass`

> Stack-agnostic. Name **metrics and thresholds**; tools are examples (Lighthouse, WebPageTest, bundle analyzer).

## Bootstrap

- [ ] Product surfaces with perf risk identified (web UI, mobile, API latency, batch jobs)
- [ ] Measurement environment documented (local, staging, production-like)
- [ ] Baseline “advisory only” vs “CI blocking” stated per quality-profile

## Web / UI (when applicable)

- [ ] Core Web Vitals targets (LCP, INP, CLS) or documented N/A
- [ ] Initial load / route transition budget (quantified or tier: strict / standard)
- [ ] Bundle or asset size budget per major entry (if SPA/extension)
- [ ] Image/media lazy-load policy in `09` or here by reference

## API / backend (when applicable)

- [ ] p95 latency targets for critical endpoints
- [ ] Timeout and retry policy cross-ref `07`
- [ ] N+1 / query budget notes cross-ref `06`

## CI / process

- [ ] Perf check tool named in `10` and row in `08` when gate exists
- [ ] Regression rule: when budget exceeded, US or decision required to waive
- [ ] Load test scope: which flows, how often (release vs nightly)

## US alignment

- [ ] Perf-sensitive US Acceptance cites measurable criteria
- [ ] `/test-review` can verify evidence against budgets

## Out of scope

- Production capacity planning (infra sizing) — note in `08` runbook only
- Vendor APM account setup — **HAR**
