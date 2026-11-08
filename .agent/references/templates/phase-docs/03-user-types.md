# Phase doc template — `03_user_types.md`

**Agent:** `technical-writer` + `product-owner` review  
**Product path:** `docs/03_user_types.md`  
**Depends on:** `02_security.md`

---

## What this document is for

`03_user_types` defines **actors**: who uses the system, through which surface, with which permissions and data visibility. It connects scope audiences to security roles and informs architecture flows and API authorization.

One generic “User” profile is never sufficient for a multi-role product.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init (after `02` draft) | One profile block per audience from `00_scope` |
| New role in epic/US | Add profile or extend permissions; sync `02` |
| Auth model change | Update Session + permissions; set `review` |
| `/audit-docs` | Verify routes/models still match permissions |

## How to complete each section

### Profile index

Summary table: profile name, primary surface, auth required, mapping to `02_security` authorization row. Use this as a map before writing full blocks.

### Each profile block (repeat per persona)

Copy the stub block for **every** audience in scope. Fill every field — do not skip “Restrictions” or “Edge cases”.

- **Description:** job context, frequency, skill level
- **Origin:** URL, CLI command, extension host — how they reach the product
- **Goals:** 2–3 jobs-to-be-done, not feature wishes
- **Permissions — can:** actionable verbs (“approve PO > limit”, “export CSV”)
- **Permissions — cannot:** explicit denials (prevents IDOR and UI-only security)
- **Session:** must match `02` authentication for that surface
- **Visible data:** fields, records, scopes they see
- **Edge cases:** table for no permission, empty state, expired session
- **Evidence (Mode B):** file paths for roles, middleware, models

### Anonymous / public access

If public pages exist, table capabilities allowed. If none, state “no anonymous access” explicitly.

### Service accounts

Document integrations (cron, webhooks, partner API) with auth method and scopes.

### Gaps / open questions

Missing role clarity, conflicting permissions — before `approved`.

## Depth checklist

- [ ] Every `00_scope` audience has a profile block
- [ ] Can/cannot lists are testable
- [ ] Session column consistent with `02`
- [ ] Edge cases cover denial paths
- [ ] PO reviewed persona names and permissions


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Authorization table in `02` has one row per profile
- `05` key flows use named profiles
- `07` API auth reflects privileged vs standard users

## Gate

PO confirms personas match business reality. `approved` before detailed user journeys in `05`.

## Related

- `phase-docs/02-security.md`, `phase-docs/00-scope.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: User Types
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [02_security.md]
blocks: [04_principles.md, 05_architecture.md, 06_database.md, 07_api_contracts.md]
---

# 03 — User types

_Every audience named in `00_scope` § Who it is for must have a profile below._

## Profile index

| Profile | Primary surface | Auth required | Maps to role in `02_security` |
| ------- | --------------- | ------------- | ----------------------------- |
| | | yes / no | |

---

## [Primary profile name]

**Description:** _(who they are, job context, frequency of use)_

**Origin:** how they reach the product (web URL, CLI, IDE extension, API client)

**Goals:** _(2–3 jobs-to-be-done)_

**Permissions — can:**

- _
- _

**Restrictions — cannot:**

- _
- _

**Session:** _(session cookie / JWT / API key / none — link `02_security` § Authentication)_

**Visible data:** _(what records, fields, or scopes they see)_

**Edge cases:**

| Situation | Expected behavior |
| --------- | ----------------- |
| No permission | |
| Empty state | |
| Session expired | |

**Evidence (Mode B):** _(routes, `User` model, role checks — file paths)_

---

## [Secondary profile name]

_(Copy block above for each additional profile.)_

## Anonymous / public access

| Capability | Allowed | Notes |
| ---------- | ------- | ----- |
| | yes / no | |

## Service accounts / integrations

| Actor | Auth method | Scopes | Owner |
| ----- | ----------- | ------ | ----- |
| | | | |

## Gaps / open questions

| # | Question | Blocks |
| - | -------- | ------ |
| 1 | | `05_architecture` / US |

## Gate

Permissions here must match `02_security` § Authorization before `approved`.

