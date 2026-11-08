# Flow triage — when to map (and when to skip)

Use at the start of every `/map-flow`. **No mandatory flow for simple work.**

## Skip (report only — handoff to `/refine-us` or `/implement-us`)

- Single screen, one primary action, no dialog/modal branch
- US Acceptance is one observable outcome and Plan already names one component area
- Change is copy, token, or layout tweak inside an existing flow row in `09`
- CLI / API-only US with no new navigation

Output: `Skip: yes` + one sentence why + optional link to existing `09` row.

## Light (`light`)

- 2–3 steps, one optional branch (confirm/cancel)
- Deliverable: Mermaid in chat **only** (no file)
- Enough for Penelope to paste into Plan during `/refine-us`

## Standard (`standard`)

- Dialog/sheet, 2+ branches, or multi-step with empty/error/loading
- Deliverable: `docs/architecture/diagrams/feature-{slug}.md` (`kind: feature-interaction`)
- Index row in `05` § Architecture diagrams when file is created
- Implementation mapping table allowed below the diagram

## Product (`product`)

- New job or primary navigation entry affecting `09` § Screen flows table
- Deliverable: update `09` (screens/states in mermaid — **not** component names in nodes)
- If also `standard` granularity needed, create feature file **and** slim `09` row

## Code-aligned (`code`)

- Brownfield or refactor; names in diagram must match repo evidence
- Run narrow read/grep first; consult `code-investigator` if depth > quick sample
- `standard` file + **Implementation** table (symbol → node label)

## Diagram rules

| Layer | Node labels |
| ----- | ----------- |
| `09` / product mermaid | Screens, dialogs, states (user language) |
| `feature-*.md` | Product labels on diagram; code symbols in table only |
| `kind: flow` (Daedalus) | Technical process, API sequence — not this skill |

## Handoff

| Next | When |
| ---- | ---- |
| `/refine-us` | Map done; cite path or paste mermaid in Plan |
| `/design-flow` | `product` mode gaps in whole IA |
| `/investigate` | Cannot name entry points with confidence |
| `/implement-us` | Only after `ready: true` — this skill does not code |
