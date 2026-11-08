---
name: document-existing-project
description: Documents an existing codebase in Meridian phase docs and as-is inventory without creating epics or user stories. Use with /document-project for brownfield adoption or refreshing docs from code.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Document existing project (Meridian)

> Captures **current state** in `docs/` — inventory + phase docs `00`–`08`. **No** epics, versions, sprints, or US.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/init-interview-guide.md` | **Mandatory** — interview gate (Mode B bank) |
| `.agent/references/templates/as-is-inventory-template.md` | **Mandatory** before `as-is.md` |
| `.agent/skills/init-project/references/doc-templates.md` | **Mandatory** — flow + depth bar |
| `.agent/references/templates/phase-docs/*.md` | **Mandatory** — one per phase doc you Write |
| `docs/discovery/product-brief.md` | If present — align intent |
| Existing `docs/*.md` | Merge, do not blindly overwrite approved content |

## When to trigger

- Existing codebase adopting Meridian (`/init-meridian` Mode B **next step**)
- `docs/` exists but phase docs are thin or empty
- Manager asks: document as-is, baseline, inventory, brownfield, “what we have today”
- Workflow `/document-project`

**Do not** use for: `/create-us`, retroactive ✅ on legacy work, or marking docs `approved`.

---

## Preconditions

| Check | Action |
| ----- | ------ |
| `docs/` missing | Run `/init-meridian` first (structure + bootstrap only) |
| `.agent/` present | Required |
| Manager authorization | Confirm target package root |

---

## Procedure

### Phase 0 — code reading (before interview)

1. Manifest files: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.
2. Top-level structure — apps, packages, `src/`.
3. README, existing docs, ADRs.
4. Auth, routes, models, DB configs, CI workflows.

### Phase 1 — interview

Follow `init-interview-guide.md` Mode B. Lead with inferences.

### Phase 2 — as-is inventory

Create or refresh `docs/inventory/as-is.md`:

- One row per **user-facing capability**
- Evidence = paths, routes, tests
- Confidence `high` \| `medium` \| `low`
- Epic **candidates** as labels only — **do not** create `EPIC-XX` rows

### Phase 3 — populate phase docs

For each `docs/0X_*.md` missing or thinner than depth bar, read matching `phase-docs/*.md` and Write:

| Doc | Source |
| --- | ------ |
| `00_scope` | README + inventory + interview; include **Current product state** |
| `01_tech_stack` | Manifests + folder structure |
| `02_security` | Auth libs, env, write scopes |
| `03_user_types` | Roles, routes, user models |
| `04_principles` | Infer layers from repo; mark `(review)` where uncertain |
| `05_architecture` | Actual structure — **draft**, not approved |
| `06_database` | Schema, migrations, SQLite paths |
| `07_api_contracts` | Routes, GraphQL, CLI — or `_n/a_` |
| `08_environments` | README setup + CI |

Keep `status: draft`. If a section was `approved`, only append **Assumptions** or propose edits in output — do not downgrade status without manager ask.

### Phase 4 — cross-check

- Every `high` inventory row appears in `00_scope` or `05_architecture`
- `03_user_types` matches `00_scope` audience
- `04_principles` layer table matches `05` layers
- Run `validate_meridian.py <root> --sqlite-only`

### Phase 5 — decisions

`update-decisions-log` if documentation materially changed product understanding.

---

## Prohibitions

| Forbidden | Allowed |
| -------- | --------- |
| Create US / epics / versions | Inventory + phase docs |
| `status: approved` on any doc | `draft` + assumptions |
| Retroactive US with ✅ | Optional epic **candidates** in inventory only |
| Delete manager-approved content without ask | Merge + gap notes |

---

## Output

```txt
Document project complete:
Package root:
Inventory: created | updated | unchanged
Phase docs updated: [list paths]
High-confidence capabilities: N
Assumptions requiring human review:
Gaps (thin sections):
Next: human review 00→04 | /audit-docs | /security-pass | /architecture
```
