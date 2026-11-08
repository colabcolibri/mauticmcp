# Phase doc template — `02_security.md`

**Agent:** `security-champion`  
**Product path:** `docs/02_security.md`  
**Deepen:** `/security-pass bootstrap` → `full` before `approved`  
**Depends on:** `00_scope`, `01_tech_stack` | **Blocks:** `03`, `04`, `05`

---

## What this document is for

`02_security` is the **security contract**: who may access what, what data is sensitive, how secrets are handled, what threats matter, and what is explicitly unknown. It is not a generic compliance checklist — every section must describe **this product** or mark a **gap**.

Agents and humans use this before architecture approval, during `/implement-us` on security-sensitive US, and at `/security-review` before close.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Copy stub; fill posture from scope + stack at high level |
| After `01` drafted | `/security-pass bootstrap` — infer auth, surfaces, secrets |
| After `01` drafted (PII in scope) | `/privacy-pass bootstrap` — infer LGPD/GDPR jurisdictions |
| Before `02` approved | `/security-pass full` + `/privacy-pass full` when PII or compliance cited |
| New integration, auth change, dependency spike | `status: review`; update tables; `/dependency-audit` if lockfiles changed |
| After security-related US | `/security-review`; update `02` if contract changed |

## How to complete each section

Read stub top to bottom. **No empty sections** — if unknown, write in **Gaps / open questions** with severity.

### Security posture summary

Set exposure (public / private / local-only), whether auth is required, sensitive data types, compliance regimes, and one-sentence trust boundary. This frames depth for the rest: local-only harness needs less than public SaaS.

### Data classification

Classify data you store or process. Fill PII inventory explicitly or state “no PII collected” with justification. Document minimization — what you refuse to collect in v1.

### Authentication model

One row per **surface** from `01` (web, API, admin, CLI). Name mechanism (session, JWT, OAuth2, API key, none). If none, explain what still needs protection (local files, agent writes).

Document password policy, MFA status, recovery flow, session expiry where applicable.

### Authorization model

Table: role/profile × can/cannot × where enforced (server mandatory for mutations). Must align with `03_user_types` — mismatch is a doc bug.

### Threat model (STRIDE)

For each major surface, identify actors, at least one STRIDE category, mitigation, residual risk. Add business-logic abuse notes (rate limits, state manipulation).

### Secrets and configuration

How secrets enter the system (env, vault). `.gitignore` for `.env`. `.env.example` policy. Rotation expectations.

### Input validation, data protection, rate limiting, audit

Fill tables or bullets per boundary. Reference validation library from `01`/`04` when chosen.

### Dependencies and supply chain

Lockfile policy, audit command, CI gate (fail vs warn).

### AI and automation safety

Required for Meridian-managed repos: what paths agents may write, forbidden actions, human gates (`ready`, `Record`, `approved`), and **HAR** (ação humana necessária) for external accounts and credentials — see `rules/MERIDIAN.md`.

### Privacy — LGPD (Brazil)

When the product processes **dados pessoais** of individuals in Brazil or data processed under Brazilian law:

- Identify **controlador** / **operador** roles (Art. 5º, VII–IX).
- Document **legal bases** (Art. 7 for regular data; Art. 11 for sensitive data) — not a copy of the law; map **this product’s** treatments.
- **Titular rights** (Art. 18): access, correction, anonymization, portability, deletion — how the product honors each channel.
- **Encarregado** (DPO): named contact or N/A with justification; see ANPD guias.
- **RIPD** when high-risk processing; consult encarregado during preparation.
- **Incidentes**: communication to ANPD when applicable — link official incident channel in references table.
- **Transferência internacional**: Res. CD/ANPD nº 19/2024 and subsequent norms when data leaves Brazil.

Mark section **N/A** only when manager confirms no Brazilian data subjects and no processing in Brazil.

### Privacy — GDPR (European Union / EEA)

When the product processes personal data of individuals in the **EU/EEA** or offers goods/services to them (Art. 3(2)):

- **Controller / processor** roles (Art. 4(7)–(8)); Art. 28 processor agreements when applicable.
- **Lawful bases** (Art. 6) — one row per processing purpose; special categories Art. 9 when relevant.
- **Data subject rights** (Arts. 12–23): access, rectification, erasure, portability, objection — product workflow.
- **DPO** (Arts. 37–39) when required or appointed voluntarily.
- **DPIA** (Art. 35) for high-risk processing.
- **Breach notification** (Arts. 33–34) to supervisory authority and data subjects when required.
- **Transfers** (Chapter V): adequacy, SCCs, or other mechanisms — name mechanism per destination.

Mark section **N/A** only when manager confirms no EU/EEA scope. **LGPD ≠ GDPR** — fill both sections when product serves Brazil and Europe.

### OWASP table

Per risk area: **this product’s** posture, not Wikipedia text. Link follow-up US if gap accepted.

### Gaps / open questions

Non-empty at init unless manager reviewed and accepted. Critical gaps block `05` approval unless decision log accepts risk.

## Depth checklist

- [ ] Posture summary complete
- [ ] Auth per surface or explicit “no auth” + protected assets listed
- [ ] Authorization aligns with `03_user_types`
- [ ] ≥1 threat model row per major surface
- [ ] Secrets policy names `.env.example` and gitignore
- [ ] Gaps table has owner for each open item
- [ ] LGPD section filled or N/A with manager rationale (Brazil)
- [ ] GDPR section filled or N/A with manager rationale (EU/EEA)
- [ ] Official reference URLs cited in doc or checklist when compliance applies

## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Roles match `03_user_types` permissions
- API auth in `07` matches authentication table
- Env secret **names** in `08`, never values
- `04_principles` security-aware coding consistent with this doc

## Gate

Human `approved` after `/security-pass full`. Critical gaps resolved or logged. Re-approval after material auth/data changes.

## Related

- `security-review/references/checklists.md`, `security-doc-checklist.md`, `security-bootstrap.md`, `privacy-compliance-checklist.md`, `privacy-bootstrap.md`
- `/security-pass`, `/security-review`, `/dependency-audit`, `/privacy-pass`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Security
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [00_scope.md, 01_tech_stack.md]
blocks: [03_user_types.md, 04_principles.md, 05_architecture.md]
---

# 02 — Security

> **Init:** copy this stub at `/init-meridian`. **Deepen:** `/security-pass bootstrap` after `01_tech_stack.md`, `/privacy-pass bootstrap` when PII in scope, then `/security-pass full` + `/privacy-pass full` before `approved`.

## Security posture summary

| Attribute | Value |
| --------- | ----- |
| **Exposure** | public internet / private network / local-only |
| **Auth required** | yes / no / partial (list surfaces) |
| **Sensitive data** | PII / payments / health / none — see § Data classification |
| **Compliance** | LGPD / GDPR / HIPAA / PCI / none |
| **Trust boundary** | _(one sentence: what is inside vs outside the system)_ |

## Data classification

| Class | Examples in this product | Storage | Retention | Encryption |
| ----- | ------------------------ | ------- | --------- | ---------- |
| Public | | | indefinite | n/a |
| Internal | | | | |
| Confidential | | | | at rest / in transit |
| Regulated | | | | |

**PII inventory:** _(name, email, phone, device id, … — or “none”)_

**Data minimization:** _(what we refuse to collect in v1)_

## Privacy — LGPD (Brazil)

_(Delete or mark N/A if no Brazilian data subjects — manager must confirm.)_

| Topic | This product |
| ----- | ------------ |
| Controlador / operador | |
| Bases legais (Art. 7 / 11) | |
| Direitos do titular (Art. 18) — como exercer | |
| Encarregado — contato | |
| RIPD necessário? | sim / não / em elaboração |
| Retenção e exclusão | |
| Transferência internacional | |
| Incidentes — procedimento | |

**Referências oficiais (consultar, não substituir assessoria jurídica):** ver checklist `privacy-compliance-checklist.md` § LGPD.

## Privacy — GDPR (EU/EEA)

_(Delete or mark N/A if no EU/EEA scope — manager must confirm.)_

| Topic | This product |
| ----- | ------------ |
| Controller / processor | |
| Lawful bases (Art. 6) per purpose | |
| Data subject rights — how to exercise | |
| DPO — contact or N/A | |
| DPIA required? | yes / no / in progress |
| Retention and erasure | |
| International transfers (Ch. V) | |
| Breach notification process | |

**Official references:** see `privacy-compliance-checklist.md` § GDPR.

## Authentication model

| Surface | Mechanism | Session / token | Expiry | Notes |
| ------- | --------- | --------------- | ------ | ----- |
| Web | none / session / JWT / OAuth2 / OIDC | | | |
| API | API key / Bearer / mTLS | | | |
| Admin | | | | |

**Password policy:** _(min length, complexity — or “N/A no passwords”)_

**MFA:** active / planned / N/A — scope: _

**Account recovery:** _(flow summary; anti-enumeration)_

**If no authentication:** state explicitly and list what still needs protection (files, agents, local data).

## Authorization model

| Role / profile | Can | Cannot | Enforced where |
| -------------- | --- | ------ | -------------- |
| | | | server / client / both |

**Model type:** RBAC / ABAC / ownership-based / hybrid

**Privileged operations:** _(delete, export, impersonate — who can?)_

**Multi-tenant isolation:** _(if applicable — how tenant id is enforced)_

_Align roles with `03_user_types.md`._

## Threat model (STRIDE summary)

For each **major surface** (API, admin, uploads, webhooks, jobs, extension host):

| Surface | Threat actors | Top STRIDE threats | Mitigation (doc or code) | Residual risk |
| ------- | ------------- | ------------------ | ------------------------ | ------------- |
| | anonymous / user / admin / dependency | | | low / medium / high |

**Business-logic abuse:** _(e.g. rate limits on bulk actions, price manipulation)_

## Secrets and configuration

| Secret type | Storage | Rotation | Never in Git |
| ----------- | ------- | -------- | ------------ |
| API keys | `.env` / vault | | yes |
| DB credentials | | | yes |
| Signing keys | | | yes |

- `.env` and `.env.*` in `.gitignore` before first commit
- `.env.example` committed — keys documented, no real values
- **Secrets manager:** _(AWS SSM / Vault / Doppler / local-only — name strategy)_

## Input validation and output encoding

| Boundary | Validation approach | Library (zod, pydantic, …) | Encoding notes |
| -------- | ------------------- | ---------------------------- | -------------- |
| HTTP API | server-side required | | JSON / HTML |
| Forms / UI | | | |
| File upload | size / type allowlist | | storage path |
| Webhooks | signature verification | | |

**Injection:** SQL/NoSQL parameterized; no shell interpolation with user input.

**Path traversal:** user paths normalized against allowlist base dirs.

## Data protection

- **In transit:** TLS version / local-only
- **At rest:** database encryption / disk encryption / n/a
- **Logs:** no tokens, passwords, or full PII in logs
- **Backups:** who can access; encryption

## Rate limiting and abuse

| Endpoint / action | Limit | Response | Notes |
| ----------------- | ----- | -------- | ----- |
| Login | | | |
| API global | | | |

_Out of scope only with explicit reason (e.g. local-only harness)._

## Audit and logging

| Event | Logged fields | Retention | Who can read |
| ----- | ------------- | --------- | ------------ |
| Auth success/fail | | | |
| Data export | | | |
| Admin actions | | | |

**Decision log:** material security changes → `/update-decisions-log`

## Dependencies and supply chain

| Concern | Policy |
| ------- | ------ |
| Lockfiles committed | yes / which |
| Audit command | `npm audit` / `pip-audit` / … |
| CI gate | fail / warn / manual |
| Copyleft / license review | |

_Run `/dependency-audit` when lockfiles change materially._

## AI and automation safety (Meridian / agents)

| Rule | Detail |
| ---- | ------ |
| Write scope | which paths agents may modify |
| Forbidden | secrets in prompts, `git push --force`, disable auth |
| Human gates | `ready: true`, `Record`, `approved` docs |
| HAR | external accounts, OAuth/PAT, billing, production creds — `⛔ Ação humana necessária` per `rules/MERIDIAN.md` |
| Extension / IDE | local disk only / network calls |

## OWASP and common risks

| Risk area | Posture for this product | Follow-up US / doc |
| --------- | ------------------------ | ------------------ |
| Broken access control | | |
| Cryptographic failures | | |
| Injection | | |
| Insecure design | | |
| Security misconfiguration | | |
| Vulnerable components | | |
| Auth failures | | |
| Data integrity | | |
| Logging failures | | |
| SSRF | | |

## Gaps / open questions

| # | Gap | Severity | Owner | Target |
| - | --- | -------- | ----- | ------ |
| 1 | | critical / high / medium | | |

_Non-empty at init unless manager reviewed — unknowns live here, not silent omission._

## Gate

Human sets `status: approved` before `/architecture` gate and backlog. Critical gaps must be resolved or accepted via decision log.

