# Security doc checklist

> Use when creating or reviewing `docs/02_security.md` — **document structure**, not code audit. Pair with `checklists.md` for `/security-pass full`.

## Document structure

- [ ] Frontmatter: `status`, `depends_on`, `blocks`
- [ ] § Security posture summary table filled
- [ ] § Data classification with PII inventory
- [ ] § Authentication — per surface or explicit “no auth”
- [ ] § Authorization — roles table aligned with `03_user_types`
- [ ] § Threat model — STRIDE table with ≥1 surface
- [ ] § Secrets — `.env` policy, rotation, vault strategy
- [ ] § Input validation — boundaries named
- [ ] § Data protection — transit, rest, logs
- [ ] § Rate limiting — or explicit out-of-scope reason
- [ ] § Audit and logging
- [ ] § Dependencies / supply chain policy
- [ ] § AI / automation safety (Meridian projects) — includes HAR cross-ref
- [ ] § Privacy — LGPD (Brazil) — filled or N/A with rationale
- [ ] § Privacy — GDPR (EU/EEA) — filled or N/A with rationale
- [ ] § OWASP mapping table — product-specific, not generic essay
- [ ] § Gaps / open questions — non-empty at init unless manager reviewed

## Init vs deepen

| Phase | Workflow | Checklist |
| ----- | -------- | --------- |
| Copy stub at init | `/init-meridian` | This file — structure |
| Bootstrap from stack | `/security-pass bootstrap` | + `security-bootstrap.md` |
| Full deepen | `/security-pass full` | + `checklists.md` all sections |
| Privacy deepen | `/privacy-pass` | + `privacy-compliance-checklist.md` (LGPD + GDPR) |
| Code audit | `/security-review` | `implementation-security-checklist.md` |

## Cross-doc consistency

- [ ] Auth model matches `01_tech_stack` surfaces
- [ ] Roles match `03_user_types` (or gap logged)
- [ ] API auth in `07_api_contracts` cites `02`
- [ ] Env secrets in `08_environments` — names only, no values

## Gate

- [ ] Human sets `status: approved`
- [ ] Critical gaps resolved or decision log entry for accepted risk

## Anti-patterns

- Empty “TBD” sections without row in Gaps
- Generic OWASP paste with no product surfaces
- “Secure by default” without controls listed
