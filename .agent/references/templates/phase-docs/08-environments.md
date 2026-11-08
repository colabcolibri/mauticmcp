# Phase doc template — `08_environments.md`

**Agent:** `devops-engineer` (Vulcan)  
**Product path:** `docs/08_environments.md`  
**Depends on:** `01`, `05` | **Feeds:** `10_test_strategy`

---

## What this document is for

`08_environments` explains **how to run, configure, test, and deploy** the product: local setup, environment variables, staging/production, CI/CD. A new developer clones and runs without tribal knowledge. Agents use this for test commands and deploy context.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Document local path from README or discover it (Mode B) |
| CI workflow change | Update CI/CD table |
| New required env var | Update table + `.env.example` in same PR |
| Release process change | Update production deploy section |

## How to complete each section

### Environment matrix

Rows: local, staging, production — purpose, URL, data policy, deploy trigger.

### Local development

**Prerequisites** table with versions. **First-time setup** — copy-paste commands in order. **Daily commands** — dev, test, lint. Test by following your own steps on clean clone when possible.

### Environment variables

Table: name, required, secret?, purpose, example non-secret value. Must mirror `.env.example`. Never paste production secrets.

### Staging / production

Hosting, deploy mechanism, rollback, smoke URL.

### CI/CD

Workflow file paths, jobs, merge gates. Link test commands to `10` when it exists.

### Deploy and release

Document **who approves** production deploys, **how** rollback works, and **where** secrets enter CI (OIDC, env secrets — never in repo). First-time cloud console or production key setup → **HAR** (`rules/MERIDIAN.md`). Cross-ref `02` secrets policy.

## Depth checklist

- [ ] Local setup is copy-pasteable
- [ ] Env table matches `.env.example`
- [ ] CI path exists in repo
- [ ] Deploy matrix names environment, trigger, approver, rollback
- [ ] No contradiction with root README (merge if needed)


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- Production host or CI pipeline changes
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Commands use package manager from `01`
- Test runners match `10`
- Secrets policy matches `02`

## Gate

`approved` when onboarding steps verified.

## Related

- `phase-docs/10-test-strategy.md`, `gitignore-baseline.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Environments
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [01_tech_stack.md, 05_architecture.md]
blocks: [10_test_strategy.md]
---

# 08 — Environments

## Environment matrix

| Environment | Purpose | URL / access | Data | Deploy trigger |
| ----------- | ------- | ------------ | ---- | -------------- |
| local | dev | localhost | synthetic / anonymized | manual |
| staging | pre-prod | | copy of prod / seed | |
| production | live | | real | |

## Local development

### Prerequisites

| Tool | Version | Install |
| ---- | ------- | ------- |
| Node / Python / … | | |
| Database | | |
| | | |

### First-time setup

```bash
# clone
git clone …
cd …

# install dependencies
# e.g. pnpm install

# environment
cp .env.example .env
# edit .env — never commit

# database (if applicable)
# migration command

# run
# dev server command
```

### Daily commands

| Task | Command |
| ---- | ------- |
| Start dev | |
| Run tests | |
| Lint | |
| Validate Meridian | `python3 .agent/scripts/validate_meridian.py .` |

## Environment variables

| Variable | Required | Secret | Purpose | Example (non-secret) |
| -------- | -------- | ------ | ------- | -------------------- |
| `DATABASE_URL` | | yes | | `postgres://localhost:5432/app` |
| | | | | |

**Rules:** document in `.env.example`; never commit real values; see `02_security`.

## Staging

| Attribute | Value |
| --------- | ----- |
| Host | |
| Deploy | |
| Smoke test URL | |

## Production

| Attribute | Value |
| --------- | ----- |
| Host | |
| Deploy | manual / CI on tag |
| Rollback | _(command or revert procedure)_ |
| Production approver | _(human role — deploy uses HAR for first-time creds)_ |

## Deploy and release

| Step | Environment | Trigger | Approver | Rollback |
| ---- | ----------- | ------- | -------- | -------- |
| Build artifact | CI | PR merge / tag | automated | n/a |
| Promote staging | staging | | | |
| Promote production | production | | manager | |

**Secrets in CI:** _(OIDC / provider secrets UI — names only; values via HAR)_

**Smoke test after deploy:** _(URL + command)_

## CI/CD

| Pipeline file | Triggers | Jobs |
| ------------- | -------- | ---- |
| `.github/workflows/ci.yml` | PR, push main | lint, test, build |

| Gate | Blocking | Tool |
| ---- | -------- | ---- |
| Lint | yes | |
| Unit tests | yes | |
| E2E | | |
| Security audit | warn / fail | `npm audit` |

_Link test commands to `10_test_strategy.md`._

## Observability (optional at init)

| Signal | Tool | Dashboard |
| ------ | ---- | --------- |
| Logs | | |
| Metrics | | |
| Errors | Sentry / … | |

## Gaps / open questions

| # | Gap | Owner |
| - | --- | ----- |
| 1 | | |

## Gate

Local setup must be copy-pasteable before `approved`.

