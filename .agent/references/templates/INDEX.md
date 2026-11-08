# Meridian templates — registry for agents

> **Mandatory:** before creating or closing any delivery artifact, the active agent MUST read this index, then read the **full template file** for that artifact **before** calling Write or Edit on the target path.

Templates are mirrored here from skills (`references/`) so every agent uses the same paths. **Do not invent structure** — copy the template and fill placeholders.

**Exception — `/complete-us`:** do **not** copy any template as the US body. Run `show US-XXXX --full`, then **add** Record + acceptance + status only. Read **`close-us-contract.md`** first. Never use `us-template.md` on close.

---

## Artifact → template → agent → skill

| Artifact | Template (read before Write) | Primary agent | Skill | Workflow |
| -------- | ---------------------------- | ------------- | ----- | -------- |
| Phase docs `00`–`11` | `doc-templates.md` | `technical-writer` | `init-project` | `/init-meridian` |
| Design (`09` flows) | `phase-docs/09-design-system.md` + skill `design-flow/references/screen-flow-checklist.md` | `design-system-owner` | `design-flow` | `/design-flow` |
| Design (`09` theme) | `phase-docs/09-design-system.md` + skill `design-theme/references/` | `design-system-owner` | `design-theme` | `/design-theme` |
| As-is inventory `docs/inventory/as-is.md` | `as-is-inventory-template.md` | `technical-writer` | `init-project` (Mode B) | `/init-meridian` |
| Projects manifest `.meridian/projects.json` | `projects-manifest-template.md` | `scrum-master` | `init-project` | `/init-meridian`, `/status` |
| Epic (SQLite) | `epic-template.md` + **`writing-guide.md`** | `product-owner` | `epic-create` | `/create-epic` |
| Version (SQLite) | `version-template.md` + **`writing-guide.md`** | `sprint-planner` | `version-create` | `/create-version` |
| Sprint (SQLite) | `sprint-template.md` | `sprint-planner` | `sprint-create` | `/plan-sprint` |
| Sprint (close) | `sprint-template.md` + **`retrospective-checklist.md`** | `sprint-planner` | `sprint-complete` | `/complete-sprint` |
| Epic (close) | `epic-template.md` + **`epic-close-checklist.md`** | `sprint-planner` | `epic-complete` | `/complete-epic` |
| User story (create) | `us-template.md` + **`writing-guide.md`** + **`code-quality-at-us-time.md`** | `story-maker` | `us-create` | `/create-us` |
| User story (review) | `review-checklist.md` + `us-template.md` + **`writing-guide.md`** + `section-contracts.md` | `story-checker` | `us-review` | `/review-us` |
| User story (refine) | `us-template.md` + `refine-checklist.md` + **`writing-guide.md`** + **`code-quality-at-us-time.md`** | `story-maker` | `us-refine` | `/refine-us` |
| User story (implement) | `implement-gate-checklist.md` + **`code-quality-at-us-time.md`** + target US | `developer` | `us-implement` | `/implement-us` |
| Architecture detail | `architecture-folder-guide.md` + `05` phase doc | `technical-architect` | — | `/architecture` |
| User story (close) | **`close-us-contract.md`** + `show --full` + `implementation-template.md` (Record shape only) | `story-checker` | `us-complete` | `/complete-us` |
| Decision entry | `decision-template.md` + `decision-schema.md` | any relevant agent | `update-decisions-log` | — |
| Board (legacy) | _(removed v11)_ | — | SQLite `board_snapshots` + planning export |

**Section contracts:** `section-contracts.md` — fixed `##` / `###` for US, epic, version.

**Canonical paths:** `TEMPLATE_SOURCES.md` — where to edit vs read (registry symlinks).

**Writing quality:** `writing-guide.md` — **mandatory** before creating or refining epics, versions, US.

All paths in this folder are relative to `.agent/references/templates/`.

---

## Agent loading protocol

When an agent from the table is activated:

1. Read `.agent/agents/{agent}/agent.md` (persona + prohibitions).
2. Read the skill `SKILL.md` listed in the table.
3. Read the **full template file** from this folder — not only frontmatter examples in `MERIDIAN.md`.
4. Read **`writing-guide.md`** when creating or refining epic, version, or US.
5. Read **`code-quality-at-us-time.md`** when creating, refining, or implementing US.
6. Read `section-contracts.md` when editing US, epic, or version structure.
7. Read **`architecture-folder-guide.md`** when editing `05_architecture.md` or `docs/architecture/`.
8. Only then create or edit the artifact.

If the request is **implement code** for a US (`developer` gate):

1. Read `implement-gate-checklist.md` + `meridian_delivery.py show US-XXXX --full`.
2. Block if `ready` is not `true` → `/review-us` first (after `/refine-us`).
3. Block if `## Plan` is empty or only placeholders.
4. Read every path listed under Plan / **Architecture refs** before writing code.
5. Read **`code-quality-at-us-time.md`** and `docs/04_principles.md` before writing code.
6. Prefer workflow `/implement-us US-XXXX` to document gate pass before coding.

---

## Lifecycle (which template when)

See `lifecycle.md` in this folder for the full create → refine → implement → close flow.

---

## Anti-patterns (protocol failure)

- Upserting US without reading `us-template.md` first (create/refine only)
- Closing US by copying `us-template.md` or `implementation-template.md` into CLI — **deletes refined content**
- Closing US with `✅` without reading `close-us-contract.md` first
- Creating epic/version/sprint from memory or from `MERIDIAN.md` excerpts only
- Partial template (frontmatter only, missing body sections)
