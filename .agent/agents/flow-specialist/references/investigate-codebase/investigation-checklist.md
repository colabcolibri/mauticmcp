# Investigation checklist — `/investigate`

## Depth levels

| Level | When | Actions |
| ----- | ---- | ------- |
| `quick` | Single symbol, one file, "where is" | Grep + read 1–3 files |
| `medium` | Flow across 2–4 layers | Entry point + main path + one test |
| `thorough` | Unknown subsystem, refactor prep | Multiple entry points, error paths, config, related tests |

## Evidence bar

Every non-trivial claim needs at least one of:

- File path + line range or symbol name
- CLI command output (read-only: `rg`, `ls`, `git log -1 -- path`)
- Test file demonstrating behavior

Label **assumptions** explicitly when code is ambiguous.

## Report template

```txt
Pergunta: {restatement}
Resposta: {1–3 sentences}
Evidência:
  - path/to/file.ts:42 — {what it shows}
  - path/to/other.py — {symbol or route}
Fluxo:
  {entry} → {layer} → {layer} → {exit}
Confiança: high | medium | low
Lacunas:
  - {what was not verified}
Handoff: nenhum | /refine-us US-XXXX | /architecture | spike US | /update-decisions-log
Next: {single recommended step}
```

## Modes (`$ARGUMENTS`)

| Argument | Scope |
| -------- | ----- |
| _(empty)_ | Question from user message |
| `US-XXXX` | Plan + Acceptance + cited arch refs only |
| `path:src/foo/` | Limit search to prefix |
| `quick` / `medium` / `thorough` | Override default depth |
| `US-XXXX thorough` | Combine US scope + depth |

## Handoff guide

| Finding | Suggest |
| ------- | ------- |
| Plan unclear for implement | `/refine-us US-XXXX` with evidence summary |
| Missing arch doc | `technical-architect` → `/architecture` |
| Needs timeboxed research in backlog | Spike US (`scrum-meridian-map.md`) |
| Changes product truth | `/update-decisions-log` |
| Ready to build | `/refine-us` then `/implement-us` |

## vs other workflows

| Workflow | Use instead when |
| -------- | ---------------- |
| `/document-project` | Document entire codebase in phase docs |
| `/audit-docs` | Phase docs stale vs code |
| `/security-review` | Security compliance vs `02` |
| `/discover` | Product problem/users — not code trace |
