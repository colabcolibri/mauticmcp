---
name: us-review
description: Audits a Meridian user story against DoR. Report-only or attest ready true. Use with /us-review US-XXXX. Does not cook Plan (story-maker).
allowed-tools: Read, Glob, Grep, Bash
---

# Review user story (Meridian)

> You are `story-checker`. Compare the US to `writing-guide.md` refine example and `refine-checklist.md`.

## Modes

| Mode | `ready` |
| ---- | ------- |
| Report-only | unchanged |
| DoR attest | `set-ready true` when Intent + Plan are implementable without guessing |

**DoR bar:** preamble is user language; Why and Where are full sentences; Approach has ≥2 explanatory bullets; Planned has verifiable steps. If any section is still a label, a title repeat, or a bare path, report it and send back to `/us-refine` — do not rewrite Plan yourself unless the manager asks.

## Commands

```bash
python3 .agent/scripts/meridian_delivery.py show US-XXXX --full
python3 .agent/scripts/meridian_delivery.py set-ready US-XXXX --ready true
```

## Output

```txt
US review: US-XXXX
Mode: report-only | DoR attest
Gaps: (section + what is missing)
Next: /us-refine | /us-implement US-XXXX
```
