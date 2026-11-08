---
name: investigate-codebase
description: Read-only codebase investigation — trace flows, map dependencies, explain behavior with evidence. Use with /investigate before refine-us, spike US, or architecture updates.
allowed-tools: Read, Glob, Grep, Bash
---

# Investigate codebase (Meridian)

> Answers **one concrete question** about how the code works — with paths, flow, and confidence. **No** product code, **no** delivery rows unless manager asks.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/investigate` | Read-only trace and explanation report |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/investigation-checklist.md` | **Mandatory** — every `/investigate` run |
| Target US via `meridian_delivery.py show US-XXXX --full` | When `$ARGUMENTS` is `US-XXXX` |
| `docs/05_architecture.md` | When question touches boundaries or modules |
| `docs/inventory/as-is.md` | Brownfield — known capabilities |

## When to trigger

- `/investigate` or "how does X work?", "where is Y?", "trace this flow"
- Before `/refine-us` when Plan needs code facts
- Spike prep (timeboxed US optional — see `scrum-meridian-map.md`)
- Manager asks to compare implementation vs assumption

**Do not** use for:

- Full brownfield documentation → `/document-project`
- Phase doc drift → `/audit-docs`
- Backlog gap matrix / missing US → `/survey-backlog` (`backlog-surveyor`)
- Security audit → `/security-review`
- Implementing a fix → `/implement-us` after `/refine-us`

---

## Procedure

### Phase 0 — frame the question

1. Restate the question in one sentence.
2. Set depth: `quick` | `medium` | `thorough` (default `medium`).
3. Set scope: whole repo, path prefix, or US Plan boundaries.
4. If question is vague → ask **one** clarifying question, then proceed with stated assumptions.

### Phase 1 — orient

1. Manifests (`package.json`, `pyproject.toml`, etc.) and top-level layout.
2. README and `docs/05_architecture.md` if present.
3. Grep for symbols, routes, env keys, feature names from the question.

### Phase 2 — trace

1. Identify entry points (HTTP route, CLI, job, event handler).
2. Follow call chain: handler → service → store → external API.
3. Note config, feature flags, and test files as evidence.
4. For `thorough`: check alternate paths, error handling, and one consumer.

### Phase 3 — report

Use output template in `references/investigation-checklist.md`.

1. Answer first (plain language).
2. Evidence: `path:line` or path + symbol.
3. Flow diagram (text): `A → B → C`.
4. Confidence: `high` | `medium` | `low` + what would raise it.
5. Handoff: none | `/refine-us` | `/architecture` | spike US | `/update-decisions-log`.

### Phase 4 — persistence (optional)

- Material product understanding change → `update-decisions-log` (run `date` first).
- Implementation needed → suggest spike US or `/create-us` — **do not** create without manager ask.

---

## Forbidden

| Forbidden | Why |
| --------- | --- |
| Product code | `developer` + `/implement-us` |
| Create US/epic/version | `story-maker` / `product-owner` |
| Mark docs `approved` | Human only |
| Guess without labeling `low` confidence | Report integrity |

---

## Output

```txt
Pergunta:
Resposta:
Evidência:
Fluxo:
Confiança: high | medium | low
Lacunas:
Handoff:
Next:
```
