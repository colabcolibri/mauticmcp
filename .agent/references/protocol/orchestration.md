# Orchestration without losing specialists

Meridian does **not** need to become a monolithic “AI OS”. Orchestration is already split:

```txt
YOU → /workflow (slash command)
   → @specialist-agent (one station)
   → skill (procedure)
   → docs/ + meridian.db (evidence)
```

`/deus-ex` is the **dispatch chief**: reads product context and points you to the next station (`/refine-us`, `/architecture`, `/implement-us`, …). It does not write US bodies, close sprints, or ship code.

---

## Why this beats a single super-agent

| Approach | Risk | Meridian |
| -------- | ---- | -------- |
| One agent does plan + code + QA | Scope drift, weak gates | Separate maker/checker, architect, developer |
| Markdown backlog only | Drift, no queries | SQLite + `board_snapshots` |
| Autonomous execution loops | Human loses control | `/implement-us` requires `ready: true`; `/complete-us` requires Record |
| Copy another framework wholesale | Identity loss | Borrow **patterns** (doctor, parity, backup), keep protocol |

---

## Agentic flow (native)

Typical delivery loop:

1. `/discover` or `/document-project` → phase docs
2. `/architecture` → `05_architecture.md` approved
3. `/create-epic`, `/create-us`, `/refine-us`, `/review-us`
4. `/implement-us US-XXXX` → `@developer`
5. `/complete-us US-XXXX` → `@story-checker`
6. `/status` anytime

For “what next?” without choosing yourself: **`/deus-ex`**.

---

## Layer above Meridian (external harness)

Use a **thin bridge**, not a fork of the protocol:

### Pattern A — External CLI as a station reference

Add a folder under `.agent/agents/{owner}/references/your-bridge/` with `PROCEDURE.md` that:

1. Runs your external tool (npm CLI, internal agent API)
2. Writes outputs into `docs/` or patches US via `meridian_delivery.py`
3. Hands off back to Meridian (`/review-us`, `/complete-us`)

The owning agent loads that reference; **deus-ex** still routes when unsure. Use `.agent/skills/` only if 2+ agents share the bridge.

### Pattern B — Parallel harness, Meridian owns delivery

- External kit handles domain automation (e.g. infra, design gen)
- Meridian owns **what** is in scope (US, acceptance, Record)
- Sync rule: every external “task done” must link to a US id in SQLite

### Pattern C — CI orchestration

- `validate_meridian.py` + `validate_kit_parity.py` in pipeline
- Fail PR if architecture gate violated or adapters drift
- No autonomous merge without human `/complete-us`

---

## What we deliberately do not build

- **Autonomous dev engine** that merges without human close
- **Generic squad marketplace** inside core — keep core Scrum; optional squads stay separate repos
- **Replacing specialist agents** with one orchestrator prompt

Borrow from other projects: **doctor**, **adapter parity**, **safe upgrade backup**, **first-value checklist**. Keep: **gates, SQLite, evidence, deus-ex dispatch, specialist roster**.
