# Template sources — where files really live

> Agents should **read** from `.agent/references/templates/` (registry). They should **edit** only the **canonical** path in the third column.

---

## How the mirror works

```txt
CANONICAL (edit here)                    REGISTRY (agents read)              IDE ADAPTER (read-only mirror)
.agent/agents/{slug}/references/{pass}/  →  .agent/references/templates/  →  .cursor/references/templates/
```

- **Registry** = symlinks + kit-owned files (`INDEX.md`, `writing-guide.md`, `section-contracts.md`, `lifecycle.md`, `TEMPLATE_SOURCES.md`).
- **Never** edit symlinks in `.cursor/` — they point at `.agent/`.
- **No `docs/templates/`** — removed in v11 (Onda C). Do not recreate under `docs/`.
- After adding a new template file: update `INDEX.md`, edit the canonical skill `references/` path, then run `./.agent/scripts/sync_kit.sh` (syncs `.cursor/references/templates/` only).

---

## Delivery artifacts

| Template | Canonical (edit) | Registry | Used by |
| -------- | ---------------- | -------- | ------- |
| `us-template.md` | `.agent/agents/story-maker/references/us-create/us-template.md` | `.agent/references/templates/us-template.md` | `/create-us`, `/refine-us`, `/review-us`, `/implement-us` — **not** `/complete-us` body |
| `refine-checklist.md` | `.agent/agents/story-maker/references/us-refine/refine-checklist.md` | `.agent/references/templates/refine-checklist.md` | `/refine-us` |
| `implement-gate-checklist.md` | `.agent/agents/developer/references/us-implement/implement-gate-checklist.md` | `.agent/references/templates/implement-gate-checklist.md` | `/implement-us` |
| `review-checklist.md` | `.agent/agents/story-checker/references/us-review/review-checklist.md` | `.agent/references/templates/review-checklist.md` | `/review-us` |
| `implementation-template.md` | `.agent/agents/story-checker/references/us-complete/implementation-template.md` | `.agent/references/templates/implementation-template.md` | `/complete-us` (Record shape only) |
| `close-us-contract.md` | `.agent/agents/story-checker/references/us-complete/close-us-contract.md` | `.agent/references/templates/close-us-contract.md` | `/complete-us` (**read first**) |
| `epic-template.md` | `.agent/agents/product-owner/references/epic-create/epic-template.md` | `.agent/references/templates/epic-template.md` | `/create-epic` |
| `version-template.md` | `.agent/agents/sprint-planner/references/version-create/version-template.md` | `.agent/references/templates/version-template.md` | `/create-version` |
| `sprint-template.md` | `.agent/agents/sprint-planner/references/sprint-create/sprint-template.md` | `.agent/references/templates/sprint-template.md` | `/plan-sprint` |
| `board-schema.md` | _(removed v11)_ | — | use `meridian_db_export --format planning` |
| `decision-template.md` | `.agent/skills/update-decisions-log/references/decision-template.md` | `.agent/references/templates/decision-template.md` | `update-decisions-log` |
| `decision-schema.md` | `.agent/skills/update-decisions-log/references/decision-schema.md` | `.agent/references/templates/decision-schema.md` | `update-decisions-log` (validation) |
| `doc-templates.md` | `.agent/skills/init-project/references/doc-templates.md` | `.agent/references/templates/doc-templates.md` | `/init-meridian` |
| `as-is-inventory-template.md` | *(kit-owned — edit in registry)* | `.agent/references/templates/as-is-inventory-template.md` | `/init-meridian` (Mode B) |

---

## Kit-owned (edit in registry folder)

| File | Purpose |
| ---- | ------- |
| `.agent/references/templates/as-is-inventory-template.md` | Mode B as-is map — `docs/inventory/as-is.md` |
| `.agent/references/templates/projects-manifest-template.md` | Multi-product monorepo — `.meridian/projects.json` |
| `.agent/references/templates/INDEX.md` | Registry table artifact → template → agent → workflow |
| `.agent/references/templates/writing-guide.md` | Prose quality — Intent, Plan, epic paragraphs |
| `.agent/references/templates/code-quality-at-us-time.md` | DRY, SRP at create / refine / implement |
| `.agent/references/templates/architecture-folder-guide.md` | `05` index + `docs/architecture/` detail |
| `.agent/references/templates/section-contracts.md` | Fixed headings — validated by Python + monitor |
| `.agent/references/templates/lifecycle.md` | create → review → refine → implement → close |
| `.agent/references/templates/TEMPLATE_SOURCES.md` | This file — canonical paths |

---

## User story — which template when

| Step | Command | Read before acting |
| ---- | ------- | ------------------- |
| Create | `/create-us` | `writing-guide.md` + `code-quality-at-us-time.md` + `us-template.md` |
| Review | `/review-us` | `review-checklist.md` + `writing-guide.md` + `section-contracts.md` + `us-template.md` |
| Refine | `/refine-us` | `refine-checklist.md` + `writing-guide.md` + `code-quality-at-us-time.md` + `us-template.md` + `04_principles.md` |
| Implement | `/implement-us` | `implement-gate-checklist.md` + `code-quality-at-us-time.md` + target US + `04_principles.md` |
| Architecture | `/architecture` | `architecture-folder-guide.md` + phase docs 00–04 |
| Close | `/complete-us` | **`close-us-contract.md`** + `show --full` + `implementation-template.md` (Record shape) + `section-contracts.md` — **not** `us-template.md` |

**Review vs refine:** `/refine-us` (`us-refine`) cooks Plan and **leaves `ready: false`**. `/review-us` (`us-review`) is the only path that sets `ready: true` (DoR attest). Report-only review does not flip `ready`.

---

## Humans and managers

Templates for **reading** (not copying into `docs/`):

- Registry: `.agent/references/templates/INDEX.md`
- Extension **Agents Help** / kit reference panels read the same paths at runtime.

Regenerate Cursor mirrors after clone:

```bash
./.agent/scripts/sync_kit.sh
```
