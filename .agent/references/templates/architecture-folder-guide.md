# Architecture folder — `docs/architecture/`

Use with `/architecture` and agent `technical-architect`. Read before creating or splitting architecture detail files.

---

## Roles

| Path | Role |
| ---- | ---- |
| `docs/05_architecture.md` | Phase doc + **gate** (`status: approved` unlocks backlog). Overview, context diagram, cross-cutting rules, **index** of detail files. |
| `docs/architecture/*.md` | Deep dives when one file is too large or domains are distinct. |
| `docs/architecture/diagrams/*.{md,mmd}` | Mermaid visual maps — runtime, database ER, flows; rendered in VS Code extension (`meridian-mermaid` module, pan/zoom). **One mermaid block per file.** Index in `05` § Architecture diagrams. |

One approved `05_architecture.md` is enough for the validator. Detail files do not need their own `approved` status — they are in scope when listed in the `05` index at approval time. Diagram files are indexed in `05` § Architecture diagrams when present.

---

## When to split into `architecture/`

- A section would exceed ~40 lines or is a distinct domain (extension vs monitor vs sidecar vs database).
- Parallel edits would constantly conflict in one file.
- A US needs stable citations to a module spec that changes often.

Keep short cross-cutting content (layers table, gate rules, repo layout summary) in `05_architecture.md`.

---

## Required index in `05_architecture.md`

When any detail file exists, add:

```markdown
## Architecture detail files

| File | Scope |
| ---- | ----- |
| `architecture/desktop-monitor.md` | Vite app, loading, HTTP path |
| `architecture/vscode-extension.md` | Webviews, sync board, activation |
```

Each detail file should have frontmatter (`title`, `updated`) and link back to the relevant § in `05`.

---

## Architecture diagrams (`diagrams/`)

**Agent:** `technical-architect` · **Skill:** `generate-architecture-diagram` · **Viewer:** VS Code **Meridian: Open Architecture Diagram**

| Rule | Detail |
| ---- | ------ |
| One file per view | `meridian-runtime.md`, `meridian-database.md`, `{integration}.md`, … |
| One ` ```mermaid ` block per file | Extension uses first block only |
| Index in `05` | § **Architecture diagrams** — required for every file on disk |
| Kinds | `runtime`, `database`, `integration`, `security`, `flow`, `other` (frontmatter `kind`) |

### Required index in `05_architecture.md`

When any diagram file exists:

```markdown
## Architecture diagrams

| File | Kind | Scope |
| ---- | ---- | ----- |
| `architecture/diagrams/meridian-runtime.md` | runtime | Kit, docs, SQLite, extension |
| `architecture/diagrams/meridian-database.md` | database | ER companion to 06 |
```

Add a row for **each** new file. Remove rows when files are deleted (after human confirms).

### Multi-file maintenance

1. **Inventory** — `Glob` `diagrams/*.{md,mmd}` and diff against `05` table (skill Phase 0).
2. **Update** — edit existing file when the same bounded view changed.
3. **Add** — new file + new `05` row when a new domain appears (new API, module, schema).
4. **Refresh all** — `/architecture diagrams` or "update architecture maps": run skill Phase 5 across indexed files.
5. **Drift** — file without index = add row; index without file = report stale row (do not delete without human).

Template and orientation (LR vs TB vs ER): skill `references/mermaid-diagram-template.md`.

---

## Workflow

1. `/architecture` — draft or review `05` and/or create `architecture/*.md`.
2. Cross-check `02_security`; load `security-review` when auth, data, or agent boundaries change.
3. Material change when `05` is `approved` → bump `05` version, set `review`, run `/update-decisions-log` (`date` before Write).

---

## US architecture refs

| Style | When |
| ----- | ---- |
| `docs/05_architecture.md — § exact heading` | Default — heading may summarize and link to detail |
| `docs/architecture/name.md — § exact heading` | At `/refine-us` when detail lives only in the folder |

Implement gate: every ref in the US must resolve before product code.
