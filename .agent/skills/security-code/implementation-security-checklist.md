# Implementation security checklist

> Use with `/security-review`. Read-only audit — fixes go to other workflows.

## Preconditions

- [ ] `02_security.md` exists
- [ ] Target US loaded from SQLite when `US-XXXX` mode
- [ ] Architecture refs in US Plan read before judging code

## Secrets and config

- [ ] No secrets in source, tests, or committed config
- [ ] Env vars documented in `.env.example` where used
- [ ] Logs do not print tokens or passwords on error paths

## Auth and access

- [ ] Auth model in code matches `02` § Authentication
- [ ] Authorization checks on mutating routes (not only UI hiding)
- [ ] Session/token expiry enforced as documented

## Input and output

- [ ] User input validated at trust boundary (API, forms, webhooks)
- [ ] SQL/command injection surfaces parameterized or ORM-safe
- [ ] File upload limits and type checks if applicable

## Data handling

- [ ] PII fields match classification in `02`
- [ ] Error responses do not leak stack traces or internal ids to clients

## Dependencies (spot-check)

- [ ] New deps in US scope justified in Plan
- [ ] Run `/dependency-audit` when lockfiles changed materially

## US acceptance alignment

- [ ] Each security-related Acceptance item has code path or test evidence
- [ ] `tests: required` US has Executed steps for security scenarios

## Gap classification

| Type | Route to |
| ---- | -------- |
| Doc outdated | `/security-pass` |
| US missing 02 refs | `/refine-us` |
| Code gap | `/implement-us` |
| Supply chain | `/dependency-audit` |

## Offensive mode extras

- [ ] Full walk: `offensive-checklist.md` (STRIDE + business logic abuse)
