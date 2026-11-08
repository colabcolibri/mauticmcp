---
name: deus-dispatch
description: Allocates the next Meridian station after reading product context. Use with /deus-ex or @deus-ex. Does not cook, implement, or close.
allowed-tools: Read, Glob, Grep, Bash
---

# Deus dispatch

> Understand **this** product, then point at **one** station. Do not do the station’s work.

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/project-context.md` | **Mandatory** — what to read on the product before allocating |
| `references/dispatch-checklist.md` | **Mandatory** — area → station → slash → stop |
| `references/handoff-envelope.md` | **Mandatory** — output shape + evidence line |
| `.agent/references/agents/agent-areas.md` | Name the area |
| `.agent/references/agents/agent-station-map.md` | Slash owner (wins over gut feel) |
| `@[skills/meridian-routing]` | Keyword matrix — after context, before emit |

Do **not** load `us-create`, `us-implement`, `epic-create`, or other cook skills. Knowing the line is not owning the stove.

## When to trigger

- `/deus-ex`, `@deus-ex`
- “Who should…”, “which agent / station”
- Messy request that is not already a foreign slash you must pass through

## Procedure

1. **Context** — `project-context.md` (read-only CLI + phase docs). If a gate blocks the ask, the next agent is the one that opens the gate — not the one that would cook past it.
2. **Area** — one of five in `agent-areas.md`.
3. **Station** — routing matrix, then station map for the slash. Map wins on conflict.
4. **Envelope** — `handoff-envelope.md`. Evidence must cite a file or CLI fact from step 1.
5. **Stop.**

## Forbidden

| Forbidden | Why |
| --------- | --- |
| Execute the next slash in this turn | That is the target station |
| Mutate SQLite or phase docs | Dispatch is read-only |
| Load cook/attest skills to “help” | SoD |
| Invent scope when `00` is missing | Pass to `scrum-master` `/init-meridian` or `product-owner` |

## Output

Copy the envelope in `references/handoff-envelope.md`.
