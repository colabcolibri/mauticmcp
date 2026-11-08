---
name: map-interaction-flow
description: On-demand UI and feature interaction flows — triage simple work, light chat diagrams, or persisted feature maps. Use with /map-flow before refine-us on complex UI; not a mandatory gate for trivial US.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Map interaction flow (Meridian)

> **Specialist flows on demand.** Simple slices → **skip** or **light** (chat only). Complex slices → **standard** file or **product** row in `09`. Never blocks trivial US.

## Operator workflow

| Workflow | Purpose |
| -------- | ------- |
| `/map-flow` | Triage + draw UI/feature interaction maps |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/flow-triage.md` | **Mandatory** — every run |
| `references/feature-flow-template.md` | `standard` or `code` mode |
| `docs/09_design_system.md` § Screen flows | Always for UI products |
| `docs/05_architecture.md` § Architecture diagrams | When writing `feature-*.md` |
| US `show US-XXXX --full` | When `$ARGUMENTS` includes US |
| `design-flow/screen-flow-checklist.md` | `product` mode |

## When to trigger

- `/map-flow`, "desenhar fluxo", "mapa da feature", "fluxo da tela", before `/refine-us` on multi-step UI
- Manager pastes a mermaid draft (refine or replace)
- Brownfield: after `/investigate` for one feature

**Not** for:

- Whole-app IA pass → `/design-flow` (`design-system-owner`)
- System/runtime modules → `/architecture` + `generate-architecture-diagram`
- Product code → `/implement-us`

---

## Modes (`$ARGUMENTS`)

| Mode | Args | Action |
| ---- | ---- | ------ |
| **triage** | _(empty)_ or `triage` | Assess skip vs light vs standard; no file unless manager confirms |
| **light** | `light`, `light US-XXXX` | Mermaid in chat; 3–7 product nodes |
| **standard** | `standard {slug}`, `US-XXXX` | Write `feature-{slug}.md`; index in `05` |
| **product** | `product {flow-name}` | Update `09` table + slim mermaid |
| **code** | `code {slug}`, `code US-XXXX` | `standard` + implementation table from repo sample |

Default: run **triage** first unless mode is explicit.

---

## Procedure

### Phase 0 — triage

1. Read `flow-triage.md`.
2. If **skip** → output and stop (suggest `/refine-us` only).
3. If UI product missing `09` stub → handoff `/design-pass bootstrap`.

### Phase 1 — frame

1. Scope: US, epic name, or free-text feature (e.g. "ingressar minhas horas").
2. Read `03`, relevant `09` row, US Plan if present.
3. Choose mode (or confirm with manager when triage was ambiguous).

### Phase 2 — draw

1. Product-language nodes on diagram; code symbols only in **Implementation mapping** (`standard`/`code`).
2. Document empty, error, loading when mode ≥ `standard`.
3. `sequenceDiagram` only when API/async is the main story — note overlap with `07`; prefer UI `flowchart` for navigation.

### Phase 3 — persist (if not `light` / skip)

1. `standard`/`code`: use `feature-flow-template.md`; update `05` diagram index.
2. `product`: follow `screen-flow-checklist.md` rules for `09` (no component names in mermaid nodes).
3. `prepend-decision` only if navigation model or primary entry changes.

### Phase 4 — handoff

- Cite artifact in chat for `story-maker` → `/refine-us`
- Never set US `ready`

---

## Forbidden

| Forbidden | Why |
| --------- | --- |
| Product code | `developer` |
| `ready: true` / `/review-us` | `story-checker` |
| Approve `09` | Human only |
| Mandatory map for every US | Triage must allow skip |
| Replace `/design-flow` for full IA | `design-system-owner` |

---

## Output

```txt
Mode: skip | light | standard | product | code
Triage:
Artifact: chat only | docs/architecture/diagrams/feature-….md | 09 § Screen flows
Mermaid: (if light or summary)
Gaps:
Next agent: story-maker | design-system-owner | code-investigator
Next command: /refine-us US-XXXX | /design-flow | /investigate
Handoff:
  station: map-flow
  agent: flow-specialist
  done:
  blocker:
  next agent:
  next command:
  artifact id:
```
