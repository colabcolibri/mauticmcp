# Meridian architecture diagram — Mermaid format

**Path:** `docs/architecture/diagrams/{name}.md` (preferred) or `{name}.mmd`  
**Viewer:** VS Code extension → **Meridian: Open Architecture Diagram** (Meridian `meridian-mermaid` module — bundled Mermaid.js, pan/zoom, multi-diagram picker)

---

## Folder role

`docs/architecture/diagrams/` holds **all IDE visual structures** for the project:

- Runtime / system maps (`kind: runtime`)
- Database ER (`kind: database`) — companion to `docs/06_database.md`
- Integrations, security, flows — one bounded view per file

The extension loads **every** `*.md` / `*.mmd` in this folder. **Every file must appear** in `05` § Architecture diagrams. Remove stale index rows only after human confirms file deletion.

### Naming

- `{product}-{topic}.md` — e.g. `meridian-runtime.md`, `acme-billing-integration.md`
- `kind` in frontmatter drives picker label (`[Runtime]`, `[Database]`, …)

### When to add another file

| Signal | New file? |
| ------ | --------- |
| Same system map, small change | Update existing `runtime` file |
| New schema / tables | Update `database` or add `database-{domain}.md` if ER is huge |
| New external API or service | New `integration` file |
| New auth/trust boundary | New `security` file |
| One user journey or state machine | New `flow` file |

**Rule:** one Mermaid block per file. Need two views → two files.

---

## Preferred: Markdown + frontmatter

```markdown
---
title: Meridian runtime
subtitle: One-line description
updated: YYYY-MM-DD
source_doc: docs/05_architecture.md
kind: runtime
---

# Optional heading (not shown in viewer)

\`\`\`mermaid
flowchart LR
  A[Component] --> B[(Store)]
\`\`\`
```

| Frontmatter | Required | Notes |
| ----------- | -------- | ----- |
| `title` | yes | Shown in diagram picker |
| `kind` | recommended | `runtime`, `database`, `integration`, `security`, `flow`, `other` — picker label |
| `subtitle` | no | Shown when user opens **Notes** |
| `source_doc` | recommended | Opens via **Doc** button (`docs/05…`, `docs/06…`) |
| `updated` | no | Shown in Notes |

---

## Flow orientation — LR vs TB

| Syntax | Direction | Use when |
| ------ | --------- | -------- |
| `flowchart LR` / `graph LR` | Left → right | **Onboarding**, user journeys, data flow across components (default for runtime) |
| `flowchart RL` | Right → left | Rare; mirror of LR when source is on the right |
| `flowchart TB` / `TD` | Top → bottom | **Layers**, protocol stacks, trust zones (UI → API → DB) |
| `flowchart BT` | Bottom → top | Dependency direction “built on top of” |

**ER diagrams:** always `erDiagram` — layout is automatic; no LR/TB choice.

**Sequence / state:** use `sequenceDiagram` or `stateDiagram-v2` for single flows (`kind: flow`).

---

## Diagram kinds

| `kind` | Mermaid type | Source doc |
| ------ | ------------ | ---------- |
| `runtime` | `flowchart LR` or `TB` | `docs/05_architecture.md` |
| `database` | `erDiagram` | `docs/06_database.md` |
| `integration` | `flowchart` or `sequenceDiagram` | `05` or `07_api_contracts` |
| `security` | `flowchart TB` + `subgraph` | `docs/02_security.md` |
| `flow` | `sequenceDiagram`, `stateDiagram-v2` | relevant architecture detail |
| `feature-interaction` | `flowchart LR` (+ optional impl table in prose) | US / feature UI — skill `map-interaction-flow`, agent `flow-specialist` |

For ER companions: include entities and key relationships; omit rarely used columns (full contract stays in `06`).

---

## Alternative: pure `.mmd`

Entire file is Mermaid source. Title and `kind` are inferred from filename (`meridian-database.mmd` → Database kind).

```text
erDiagram
  A ||--o{ B : rel
```

---

## Styling (flowcharts)

```mermaid
classDef module fill:#0f766e,stroke:#2dd4bf,color:#ecfeff
classDef store fill:#065f46,stroke:#34d399,color:#ecfdf5
class kit,docs module
```

Keep **≤15 nodes** per flowchart; split large systems into multiple files.

---

## Examples (Meridian dogfood)

| File | Kind |
| ---- | ---- |
| `docs/architecture/diagrams/meridian-runtime.md` | runtime |
| `docs/architecture/diagrams/meridian-database.md` | database |

---

## Why Mermaid + Meridian renderer

- Same syntax as `05` / `06` gate docs and GitHub.
- Auto-layout — no manual coordinates.
- Renderer lives in the plugin (`src/meridian-mermaid/`) — **no external diagram npm for end users**.
- Bundled Mermaid.js + Meridian theme/polish; webview provides pan/zoom.
