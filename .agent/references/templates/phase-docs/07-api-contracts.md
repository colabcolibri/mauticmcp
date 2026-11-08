# Phase doc template — `07_api_contracts.md`

**Agent:** `technical-architect` (Daedalus) — `/api-pass`  
**Product path:** `docs/07_api_contracts.md`  
**Depends on:** `05`, `06`

---

## What this document is for

`07_api_contracts` documents **boundary contracts**: HTTP routes, GraphQL operations, CLI commands, or extension↔script protocols. If there is no network API, document the **internal** contract (e.g. Meridian extension spawning Python with argv/exit codes).

This is the reference for US that touch integrations and for `/security-review` on auth headers.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init | Stub endpoints or state `_n/a_` with reason |
| Each API epic | Add/update rows before US `ready` |
| Breaking change | Versioning section + decision log |
| New webhook | Fill webhooks table |

## How to complete each section

### API style and authentication

Must match `02_security`. State base URL pattern and versioning strategy.

### Error envelope

Show JSON shape or reference `04_principles`. Document stable error codes for clients.

### Endpoints table

Method, path, purpose, auth, request/response summary. Mode B: only list routes with file evidence. Mark `planned` rows clearly.

### Pagination, webhooks, rate limits

Fill or `_n/a_` with reason. Link rate limits to `02`.

### Internal contracts

Non-HTTP boundaries — scripts, IPC, message formats.

## Depth checklist

- [ ] Auth consistent with `02`
- [ ] Error format documented
- [ ] No invented endpoints (Mode B)
- [ ] Planned vs implemented distinguished


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- Entities in `06` support payloads
- `08` documents how to call API locally
- Security review can map US to routes

## Gate

`approved` when v1 public contract is stable enough for US Plan refs.

## Related

- `phase-docs/02-security.md`, `phase-docs/06-database.md`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: API Contracts
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [05_architecture.md, 06_database.md]
blocks: []
---

# 07 — API contracts

_If the product has no HTTP API, document CLI commands, extension message protocol, or internal module contracts — do not leave empty without explanation._

## API style

| Attribute | Value |
| --------- | ----- |
| **Style** | REST / GraphQL / gRPC / CLI / extension RPC / none |
| **Base URL** | `https://…` / local / n/a |
| **Versioning** | URL `/v1` / header / none |
| **Documentation** | OpenAPI path / inline / n/a |

## Authentication

| Mechanism | Header / param | Consistent with `02_security` |
| --------- | -------------- | ----------------------------- |
| | `Authorization: Bearer` | |

## Common headers

| Header | Required | Description |
| ------ | -------- | ----------- |
| `Content-Type` | | `application/json` |
| | | |

## Error envelope

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable",
    "details": []
  }
}
```

_Align with `04_principles` § Error handling._

## Endpoints (stub — expand before `approved`)

| Method | Path | Purpose | Auth | Request | Response |
| ------ | ---- | ------- | ---- | ------- | -------- |
| GET | `/health` | liveness | no | — | `200` |
| | | | | | |

## Pagination / filtering (if applicable)

| Param | Type | Default | Max |
| ----- | ---- | ------- | --- |
| `page` | | | |
| `limit` | | | |

## Webhooks / callbacks

| Event | Payload | Signature | Retry |
| ----- | ------- | --------- | ----- |
| | | | |

## Rate limits

_Link to `02_security` § Rate limiting._

## Internal contracts (non-HTTP)

| Consumer | Provider | Contract location |
| -------- | -------- | ----------------- |
| extension | `meridian_delivery.py` | argv, exit codes |

## Gaps / open questions

| # | Endpoint / contract missing | US / epic |
| - | ------------------------- | --------- |
| 1 | | |

## Gate

Paths must exist in repo (Mode B) or be explicitly `planned` before `approved`.

