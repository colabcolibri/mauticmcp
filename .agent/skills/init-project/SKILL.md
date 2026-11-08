---
name: init-project
description: Initializes a project with Meridian phase docs, SQLite delivery profile, and minimum governance. Use when starting a new project or repairing a missing Meridian structure. Also handles existing codebases migrating into Meridian.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Init project (Meridian)

> Creates minimum structure in `docs/` for governance before any product code.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `references/doc-templates.md` | **Mandatory** — init registry and copy procedure |
| `.agent/references/templates/phase-docs/{doc}.md` | **Mandatory** — read **agent guide** (top), then copy § Document stub |
| `.agent/references/templates/init-interview-guide.md` | Before Phase 0 interview |
| `.agent/references/templates/as-is-inventory-template.md` | **Mode B only** — `docs/inventory/as-is.md` |
| `references/gitignore-baseline.md` | Before first commit |

## When to trigger

- New project with Meridian intent
- `.agent/` exists but `docs/` missing
- Incomplete or corrupted structure
- Agent tried to implement without document base
- **Existing codebase migrating to Meridian** (see Mode B below)

---

## Mode A — New project

### Phase 0 — context check

1. Read `.agent/MERIDIAN.md` if it exists.
2. Confirm target folder and user authorization to create files.
3. If project intent missing → ask the following questions (maximum **5** — do not ask all if context is already clear):
   - What problem does this product solve, and for whom?
   - Who are the primary users (role, context, technical level)?
   - What is explicitly out of scope for this version?
   - What are the main technology constraints or decisions already made?
   - Are there security, compliance, or data sensitivity concerns to document from the start?

### Procedure

1. Check if `docs/` exists.
2. If absent, create tree:

```txt
docs/
  README.md
  00_scope.md … 11_decisions.md
  architecture/       # optional — detail indexed from 05
  inventory/          # Mode B only — as-is.md
  discovery/          # optional — product discovery artifacts
.meridian/
  delivery.json       # created by bootstrap (meridian.db is gitignored)
```

3. Run delivery bootstrap:

```bash
python3 .agent/scripts/meridian_delivery.py bootstrap
```

4. **Phase docs:** for each template in `references/doc-templates.md`, read the **agent guide** in `phase-docs/{doc}.md` (sections *What / When / How / Depth checklist*), copy **§ Document stub** to the product path, and fill using *How to complete each section* — not blank headings. Do not copy the agent guide into `docs/`.
5. **UI products:** if stack has UI surfaces, also copy § Document stub from `phase-docs/09-design-system.md` → `docs/09_design_system.md`. Skip for CLI-only backends. Follow with `/design-flow` and `/design-theme` before treating `09` as complete.
6. **Tested products:** if scope includes automated tests, copy § Document stub from `phase-docs/10-test-strategy.md` → `docs/10_test_strategy.md`. Skip for throwaway prototypes.
7. `11_decisions.md` stub + initial decision via `prepend-decision` ("Project started with Meridian").
8. Validate `.gitignore` with `references/gitignore-baseline.md`.
9. **Do not** create US, epics, versions, sprints, `docs/templates/`, `docs/kanban/board.json`, app, API, database or migrations.

---

## Mode B — Existing codebase (migration)

Use when the user already has running code and wants to adopt Meridian governance.

### Phase 0 — code reading

Before asking any questions, read the repository to infer:

1. `package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent — technology stack.
2. Top-level folder structure — what are the main modules/apps?
3. Existing README (if any) — product description, setup, audience.
4. Any existing docs, ADRs, or architecture notes.
5. Open issues or PR titles if accessible — infer current priorities.

### Phase 1 — structured interview

After reading the codebase, ask (only what is still unclear after reading):

- Based on the code, this appears to be [your inference]. Is that accurate?
- Who are the primary users of this product, and what problem does it solve for them?
- What is in scope for the next release, and what are you explicitly deferring?
- Are there security or compliance requirements (auth model, PII, regulated data)?
- Are there architecture decisions already made that should be documented (DB choice, hosting, auth library)?

### Phase 2 — as-is inventory

Read `as-is-inventory-template.md`, then create `docs/inventory/as-is.md`:

1. One table row per **user-facing capability** (not per folder).
2. Evidence = real paths, routes, models, or docs.
3. Confidence = `high` | `medium` | `low` — never `high` without evidence.
4. Epic candidate column for significant blocks (ids only — do not create epics yet).
5. Assumptions section for anything the manager must confirm.

### Phase 3 — generate docs from code

Populate phase docs from inventory + observations — use **§ Document stub** from `phase-docs/*.md` as structure, replace placeholders with evidence (not blank headings):

1. `00_scope.md` — derive from README + inventory + interview answers. Include **current product state** from high-confidence rows.
2. `01_tech_stack.md` — list what was found (languages, frameworks, infra). Mark `status: draft`.
3. `02_security.md` — note what exists (auth libraries, env handling) and what is unknown. Mark gaps explicitly.
4. `03_user_types.md` — derive from code (admin routes, user models, role checks found in code).
5. `04_principles.md` — leave mostly blank with a note: "derived from existing code style; needs human review".
6. `05_architecture.md` — diagram the actual structure found. Mark `status: draft` — **not approved**.
7. Cross-check: every `high` inventory row appears in scope or architecture (or explain why not).

### Phase 4 — structure

Same as Mode A steps 3–8, applied to inferred content. Ensure `docs/inventory/` exists with `as-is.md`.

### Phase 5 — multi-product manifest (when applicable)

If discovery finds **more than one** `docs/` folder named exactly `docs` with Meridian fingerprint:

1. Read `projects-manifest-template.md`.
2. Propose `.meridian/projects.json` at kit root with one entry per product (`docs` path relative to kit root).
3. Ask manager for `qualitySiege` per product (`kit` | `standard` | `full`) — default `kit`; see `agentic-quality-model.md`.
4. Do **not** treat `docs-extra` or non-`docs` folder names as products.
5. Use `exclude` only for stray `docs/` folders that must not appear in the picker.
6. Set `default` after manager confirms which product is primary.

---

## Checkpoints (both modes)

| # | Check |
| - | ----------- |
| 1 | `docs/` phase docs (`00`–`11`), `00_scope`, `11_decisions` exist; `meridian.db` bootstrapped |
| 2 | `.meridian/delivery.json` exists; `meridian.db` bootstrapped |
| 3 | `.env*` and `.meridian/meridian.db` protected in `.gitignore` |
| 4 | No `docs/templates/` mirror |
| 5 | No product code created |
| 6 | (Mode B) `docs/inventory/as-is.md` exists with capability table |
| 7 | (Mode B) Inferences marked as assumptions — human must review and approve |

## Prohibitions

| Forbidden | Allowed |
| -------- | --------- |
| Mark phase docs as `approved` without human | `draft` + assumptions |
| Create US | Empty delivery — use `/create-epic` after architecture approved |
| Create retroactive US with `✅` for legacy | Inventory + epics `complete` + optional v0 |
| Implement features | Docs + initial decision |
| (Mode B) Replace existing README | Add `docs/README.md` alongside |
| (Mode B) Keep inventory after `05_architecture` approved | Archive or delete after promotion |

## Output

```txt
Meridian initialized:
Mode: new project | existing codebase
Created:
Inventory (Mode B): docs/inventory/as-is.md
Inferred (Mode B):
Assumptions requiring human review:
Pending:
Blocked:
Next human decision:
```
