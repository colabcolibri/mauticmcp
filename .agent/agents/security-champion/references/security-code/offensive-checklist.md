# Offensive security checklist — `/security-review offensive`

> **Checklist-only posture** — threat modeling and abuse scenarios. **No exploitation**, no automated attacks, no production probing without explicit human authorization.

## Preconditions

- [ ] `02_security.md` at least `draft`
- [ ] `implementation-security-checklist.md` base pass understood
- [ ] Scope: full codebase, `US-XXXX`, or named surface in `$ARGUMENTS`

## STRIDE (per major trust boundary)

For each boundary (browser↔API, API↔DB, agent↔tool, webhook↔app, admin↔user):

| Threat | Question |
| ------ | -------- |
| **S**poofing | Can actor pretend to be another user or service? |
| **T**ampering | Can data in transit or at rest be altered undetected? |
| **R**epudiation | Are security events logged with actor and time? |
| **I**nformation disclosure | What leaks on error, logs, or IDOR? |
| **D**enial of service | What is unbounded (upload, query, webhook flood)? |
| **E**levation of privilege | Can user become admin or agent gain extra tools? |

## Abuse scenarios (business logic)

- [ ] IDOR on object ids (orders, files, orgs)
- [ ] Privilege escalation via role flags or missing server checks
- [ ] Rate-limit and quota bypass on expensive operations
- [ ] Replay of webhooks or idempotent operations
- [ ] Mass assignment / unexpected fields on write APIs
- [ ] Agent tool abuse: exfiltration paths, prompt injection to tools
- [ ] Payment edge cases: double spend, negative quantity, refund abuse

## Reporting

| Finding | Route |
| ------- | ----- |
| Doc gap | `/security-pass` |
| US missing scenario | `/refine-us` |
| Code gap | `/implement-us` |
| Dependency | `/dependency-audit` |

## Forbidden

- Running exploit payloads against production
- Storing real credentials in reports
- Marking `02` approved
