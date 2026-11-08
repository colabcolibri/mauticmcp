# Phase doc templates — init registry

> **Single source:** `.agent/references/templates/phase-docs/*.md`  
> Each file = **agent contract** (top) + **document stub** (§ Document stub — copy to `docs/`).  
> **No duplicate stubs** elsewhere in the kit.

## Required frontmatter (every phase doc)

```yaml
---
title: Document name
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: []
blocks: []
---
```

## Init procedure (`/init-meridian`)

For each row below:

1. Open the template in `phase-docs/`.
2. **Read the agent guide** (everything above `## Document stub`):
   - *What this document is for* — role in the chain
   - *When to write and revisit* — init, deepen, mid-project triggers
   - *How to complete each section* — what to write in every stub `##`
   - *Depth checklist* — pass before human `approved`
3. Copy **only** § Document stub into the product path.
4. Fill placeholders using the guide — not from memory or generic filler.
5. Keep `status: draft` until human approves.

| Product path | Template | When to skip |
| ------------ | -------- | ------------ |
| `docs/README.md` | `phase-docs/docs-readme.md` | never |
| `docs/00_scope.md` | `phase-docs/00-scope.md` | never |
| `docs/01_tech_stack.md` | `phase-docs/01-tech-stack.md` | never |
| `docs/02_security.md` | `phase-docs/02-security.md` | never |
| `docs/03_user_types.md` | `phase-docs/03-user-types.md` | never |
| `docs/04_principles.md` | `phase-docs/04-principles.md` | never |
| `docs/05_architecture.md` | `phase-docs/05-architecture.md` | never |
| `docs/06_database.md` | `phase-docs/06-database.md` | never |
| `docs/07_api_contracts.md` | `phase-docs/07-api-contracts.md` | never |
| `docs/08_environments.md` | `phase-docs/08-environments.md` | never |
| `docs/09_design_system.md` | `phase-docs/09-design-system.md` | CLI-only / no UI |
| `docs/10_test_strategy.md` | `phase-docs/10-test-strategy.md` | no test mandate |
| `docs/12_marketing_seo.md` | `phase-docs/12-marketing-seo.md` | no public indexable web |
| `docs/11_decisions.md` | `phase-docs/11-decisions.md` | never |

After `meridian_delivery.py bootstrap`, prepend first decision (see `11-decisions.md` stub).

## Mid-project review (docs drift)

When stack, scope, auth, or code diverge from `docs/`:

1. Re-open the matching `phase-docs/{doc}.md` guide (same file as init).
2. Set product doc `status: review`.
3. Edit using *How to complete each section* + *Cross-doc checks*.
4. Log material changes via `/update-decisions-log`.
5. Human sets `approved` again.

Use `/audit-docs` for a full pass across all phase docs.

## Deepen after init (not init copy)

| Doc | Command |
| --- | ------- |
| `02_security` | `/security-pass bootstrap` → `full`; `/privacy-pass bootstrap` → `full` when PII |
| `05_architecture` | `/architecture` |
| `09_design_system` | `/design-pass bootstrap` then `/design-flow` and `/design-theme` |
| `10_test_strategy` | `/test-pass bootstrap` |
| `12_marketing_seo` | `/seo-pass bootstrap` → `full` (public web only) |

## Mode B only

`docs/inventory/as-is.md` — `.agent/references/templates/as-is-inventory-template.md` (not a phase doc stub).

## Prohibited at init

- `docs/templates/` mirror
- `docs/us/`, `docs/epics/`, `docs/kanban/board.json` as delivery source
- `status: approved` without human
- Copying agent contract sections into product `docs/`
