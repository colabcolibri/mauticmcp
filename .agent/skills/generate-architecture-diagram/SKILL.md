---
name: generate-architecture-diagram
description: Create or update Meridian architecture Mermaid diagrams for the VS Code extension viewer. Use when mapping system architecture, database ER, integrations, visualizing docs/05 or docs/06, refreshing diagram inventory, or when the user asks for an architecture diagram, system map, or interactive graph in the plugin.
allowed-tools: Read, Glob, Grep, Edit, Write
---

# Generate architecture diagram (Meridian)

> Write **Mermaid** to `docs/architecture/diagrams/*.md` or `*.mmd`. The VS Code extension renders with the **Meridian diagram renderer** (`app-visual-studio/src/meridian-mermaid/`) — **Meridian: Open Architecture Diagram** (pan, zoom, multi-file picker).

## Meridian chain (do not skip)

```txt
Human: /architecture [diagrams | runtime | database | …]
  → workflow: .agent/workflows/architecture.md
  → agent: technical-architect
  → this skill: generate-architecture-diagram
  → docs: 05 index + docs/architecture/diagrams/*
```

- **Workflow** sets scope and gates (00–04 read, 05 status, no product code unless asked).
- **Agent** owns consistency of `05` + `architecture/` + diagram index.
- **This skill** owns Mermaid files, kinds, orientation, and sync with `05` § Architecture diagrams.

Do not author diagram files without reading the inventory step below when the folder already exists.

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/mermaid-diagram-template.md` | **Mandatory** — format, orientation, kinds |
| `docs/05_architecture.md` | System shape, **diagram index table** |
| `docs/06_database.md` | ER for `kind: database` diagrams |
| `docs/07_api_contracts.md` | `kind: integration` when APIs exist |
| `docs/architecture/*.md` | Detail specs when splitting domains |

## Purpose of `docs/architecture/diagrams/`

Central folder for **all IDE visual structures** — not only runtime:

| Kind (`kind` frontmatter) | When | Typical diagram | Source doc |
| ------------------------- | ---- | ----------------- | ------------ |
| `runtime` | System components, kit, extension | `flowchart LR` or `TB` | `05` |
| `database` | Schema, ER, storage | `erDiagram` | `06` |
| `integration` | APIs, external systems | `flowchart` or `sequenceDiagram` | `05` / `07` |
| `security` | Trust zones, auth flows | `flowchart TB` + subgraphs | `02` |
| `flow` | Single process, state machine | `sequenceDiagram`, `stateDiagram-v2` | detail file |

**Multiple files:** one file = one view. The extension loads **every** `*.{md,mmd}` in the folder (picker). Projects commonly have several: `runtime`, `database`, per-integration, per-module.

**One Mermaid block per file** — two views → two files.

## When to trigger

| Situation | Action |
| --------- | ------ |
| User asks for diagram / system map / ER map | Create or update matching file(s) |
| `/architecture` with diagram intent | Run full agent pass + this skill |
| `06_database` schema changed | Update `kind: database` companion(s); check index |
| `05` structure changed (new module, tab, service) | Update `kind: runtime` or add new file |
| New integration in `07` | Add or update `kind: integration` file |
| Drift: files on disk ≠ `05` index | Reconcile index **or** remove orphan files (human confirms delete) |

**Do not** replace Mermaid in `05` / `06` gate sections — diagrams here are **companion** IDE views.

## Procedure

### Phase 0 — inventory (mandatory if folder exists)

1. `Glob` `docs/architecture/diagrams/*.{md,mmd}`.
2. Read `05` § **Architecture diagrams** table.
3. Report:

```txt
On disk: [files]
In 05 index: [rows]
Missing index: …
Stale index (file deleted): …
Action: create | update | reconcile index
```

4. If project has **no** diagrams yet, plan the minimum set (usually `runtime` + `database` when `06` exists).

### Phase 1 — scope one diagram

1. One diagram = one bounded view (≤15 nodes on main path; ER = entities + keys, not every column).
2. Read evidence from phase docs and code paths.
3. Prefer `.md` with frontmatter + single ` ```mermaid ` block.
4. **Update vs new file:** same bounded view → edit existing file; new domain → new `{topic}.md` + new `05` row.

### Phase 2 — author Mermaid

1. Copy template from `references/mermaid-diagram-template.md`.
2. Set `title`, `subtitle`, `kind`, `source_doc`, `updated` in frontmatter.
3. Orientation: `LR` journeys, `TB` layers, `erDiagram` for DB (see template).
4. `classDef` + `class` on flowcharts for role colors.
5. Label only non-obvious edges.

### Phase 3 — validate

- Unique node ids, closed fences, one mermaid block per file.
- Filename kebab-case: `{product}-{topic}.md` (e.g. `meridian-runtime.md`).

### Phase 4 — index in 05

Update § **Architecture diagrams** — **every** file on disk must have a row:

```markdown
| File | Kind | Scope |
| ---- | ---- | ----- |
| `architecture/diagrams/meridian-runtime.md` | runtime | … |
```

If `05` is `approved`, set `status: review` and log via `/update-decisions-log`.

### Phase 5 — multi-file refresh (when “update all architecture”)

When user or `/architecture` asks to refresh the whole visual set:

1. Complete Phase 0 inventory.
2. For each indexed row, open file → compare with source doc → update Mermaid or mark `Missing:` in report.
3. Do not batch unrelated views into one file.
4. Output summary table: file | kind | updated yes/no | notes.

## Forbidden

| Forbidden | Why |
| --------- | --- |
| JSON diagram IR (`*.json` in diagrams/) | Replaced by Mermaid |
| Multiple ` ```mermaid ` blocks in one file | Extension loads first block only |
| Diagram file not listed in `05` | Index is contract for humans and agents |
| 25+ nodes in one flowchart | Split into multiple files |
| Archify / external diagram CLI as requirement | Native Mermaid in repo |
| Product code in this skill | Extension already renders; skill writes docs only |

## Output

```txt
Inventory: on disk N | index M | drift: …
Diagram(s): docs/architecture/diagrams/{name}.md (created | updated)
Kind: runtime | database | …
05 index: updated | reconciled
View: Meridian: Open Architecture Diagram
```
