# Review checklist — audit US quality (read-only)

Use with skill `us-review` and workflow `/review-us`. **Do not edit the US** unless the manager explicitly asks to fix in the same turn.

**Canonical refine gates:** `.agent/agents/story-maker/references/us-refine/refine-checklist.md` (same rows — review reports pass/fail; refine fixes Plan; **`ready: true` only via `/review-us` DoR attest**).

**Prose bar:** `.agent/references/templates/writing-guide.md`

**Structure bar:** `.agent/references/templates/section-contracts.md`

**INVEST / Scrum mapping:** `.agent/references/scrum/scrum-meridian-map.md` (agents — not `scrum-guide-complete.md` unless manager asks)

---

## Audit rows (mark pass | fail | warn)

| ID | Check | Pass when |
| -- | ----- | --------- |
| R1 | Validator | `validate_meridian.py` — 0 errors on this US (warnings listed separately) |
| R2 | Section contract | All required `##` / `###` present per `section-contracts.md` |
| R3 | Why | 2+ sentences; slice clear; not epic paste |
| R4 | Where | 2+ sentences; version/deps/unblocks |
| R5 | Approach | **required** for DoR — ≥2 explanatory bullets; no bare paths (see refine-checklist) |
| R6 | Architecture refs | Exact `§ heading` from `05_architecture.md` (not `§ TBD` / placeholder) |
| R7 | API / DB / Security | `_n/a_` with phrase **or** concrete impact |
| R8 | Acceptance | Each item observable; not vague |
| R9 | Plan / Planned | Numbered steps or exact commands (if `tests: required`) |
| R10 | `done_when` | One measurable sentence in frontmatter |
| R11 | Epic link | `epic:` in frontmatter only — body explains slice |
| R12 | `ready` flag | `true` only if R3–R9 would all pass (review does not set it) |
| R13 | Record section | Empty or placeholder OK before code; must be filled before ✅ |
| R14 | INVEST (qualitative) | Slice valuable, small enough for one session, testable acceptance; deps justified |
| R15 | Privacy refs | PII/LGPD/GDPR in acceptance → Plan cites `02_security` privacy § or `/privacy-pass` noted |

---

## Placeholder patterns (automatic fail on R5–R9)

Same list as refine-checklist: `_(fill in`, `§ [section name`, `path/to/…`, `add when implementation scope is known`, Approach bullets under 6 words with no verb.

---

## Recommendation matrix

| Situation | Next step |
| --------- | --------- |
| R3–R9 failures, `ready: false` | `/refine-us US-XXXX` |
| All R3–R9 pass, `ready: false` | `/refine-us US-XXXX` (to set ready and sync board) |
| All pass, `ready: true`, status ❌ | Implement (`developer` gate) |
| Code done, R13 fail | `/complete-us US-XXXX` |
| Structural errors (R1/R2) | Fix structure first; may need manual edit + re-review |

---

## Output template

```txt
US review: US-XXXX
ID: US-XXXX
Validator: ...
Checklist: 11/13 pass

| ID | Result | Note |
| R3 | pass | |
| R5 | fail | Approach bullet 2 is bare path only |

Recommendation: /refine-us US-XXXX
```
