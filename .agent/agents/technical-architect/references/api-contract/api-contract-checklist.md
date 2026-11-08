# API contract checklist — `/api-pass`

> Stack-agnostic. Document **shape and rules**; OpenAPI/GraphQL schema files are implementation artifacts via `/implement-us`.

## Bootstrap

- [ ] API style chosen with rationale (REST, GraphQL, gRPC, tRPC, CLI-only, mixed)
- [ ] Base URL / versioning strategy documented
- [ ] Authentication matches `02` § Authentication
- [ ] No HTTP API → internal contract section filled (IPC, argv, exit codes)

## Full pass

- [ ] Error envelope: stable codes, client-safe messages, no stack leaks
- [ ] Endpoints table: method, path, purpose, auth, request/response summary
- [ ] Pagination strategy documented or `_n/a_`
- [ ] Filtering/sorting conventions when list APIs exist
- [ ] Idempotency for unsafe retries (POST payments, creates)
- [ ] Webhooks: events, signature, retry, ordering expectations
- [ ] Rate limits linked to `02` / `08`
- [ ] Deprecation policy and sunset headers when versioning
- [ ] Brownfield: every row has file/route evidence or marked `planned`

## Cross-doc

- [ ] Consistent with `05` module boundaries
- [ ] Data entities in responses align with `06`
- [ ] Payment webhooks cross-check `/payment-pass` when billing in scope

## US alignment

- [ ] API US Plan cites 07 rows touched
- [ ] Breaking changes have version bump note + decision log
