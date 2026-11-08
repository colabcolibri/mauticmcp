# Dispatch checklist

Run in order. Skip a step only when the ask already is a foreign slash (then pass that owner — do not execute).

## 1. Context

Follow `project-context.md`. Record facts for Evidence.

## 2. Human-only (HAR)

Account, OAuth, PAT, billing, production deploy, accept terms → **HAR stop**. Next agent is none. Next command is the human.

## 3. Area

Pick one from `agent-areas.md`: discovery | standards | planning | build | attest.

If two areas fight, pick the **gate** that is still closed (e.g. no `05` approved → standards, not planning).

## 4. Station

1. `meridian-routing` matrix from the **ask**.
2. Confirm slash owner in `agent-station-map.md`.
3. Conflict → **map wins**.

## 5. Gates (override a naive matrix hit)

| Fact | Do not send to | Send to |
| ---- | -------------- | ------- |
| No `docs/` | any cook | `scrum-master` `/init-meridian` |
| `05` not `approved` and ask is US or product code | `story-maker`, `developer` | `technical-architect` `/architecture` (or human approve) |
| US `ready` false and ask is implement | `developer` | `story-maker` `/refine-us` then `story-checker` `/review-us` (name the **first** missing step) |
| Cook vs attest on the same US | one agent for both | maker **or** checker per map |
| Need a code fact to choose | `developer` | `code-investigator` `/investigate` |
| Missing US / backlog holes / after brownfield doc | `story-maker` `/create-us` alone | `backlog-surveyor` `/survey-backlog` (report first) |
| UI flow clarity (complex slice) | `design-system-owner` `/design-flow` for whole IA | `flow-specialist` `/map-flow` (triage; skip ok) |
| Linked US still ❌/🔶 | `sprint-planner` `/complete-sprint` | Finish US (`story-checker`) or keep sprint open |
| Sprint US all terminal | — | `sprint-planner` `/complete-sprint` after human review + real Retrospective |

Name **one** next command. If two steps are required, the second is a note in Blocker, not a second Next command.

## 6. Scrum master vs you

| Ask | Owner |
| --- | ----- |
| Counts, phase table, “can we advance?” as a **report** | `scrum-master` `/status` |
| “Who should run this?” | you (`deus-ex`) |
| Init, daily ritual | `scrum-master` |

You may **read** `counts` to allocate. You do not replace `/status`.

## 7. Emit and stop

Fill `handoff-envelope.md`. Do not start the next workflow in this turn.
