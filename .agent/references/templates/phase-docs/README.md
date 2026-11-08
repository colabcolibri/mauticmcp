# Phase doc templates — single source for init and review

Each file here is **two layers in one path**. Agents read the **whole file**; only § Document stub is copied to `docs/`.

## 1. Agent guide (top — stays in kit)

Instructions for writing and **maintaining** the product doc:

| Section | Purpose |
| ------- | ------- |
| **What this document is for** | Role in the 00→11 chain |
| **When to write and revisit** | Init, deepen workflows, triggers mid-project |
| **How to complete each section** | What to write in every `##` of the stub — not just examples |
| **Depth checklist** | Pass/fail before `approved` |
| **Mid-project review** | When docs drift; `review` → edit → decision log → re-approve |
| **Cross-doc checks** | Consistency with sibling phase docs |
| **Gate** | Human `approved` rules |

Use the guide at **init** (`/init-meridian`), **deepen** (`/security-pass`, `/architecture`, …), and **audit** (`/audit-docs`).

## 2. Document stub (§ Document stub — copy to `docs/`)

Frontmatter + tables + placeholders. Fill using the guide above, then copy to the product repo.

**No duplicate stubs** under `init-project/references/`.

| Product path | Template |
| ------------ | -------- |
| `docs/README.md` | `docs-readme.md` |
| `docs/00_scope.md` | `00-scope.md` |
| `docs/01_tech_stack.md` | `01-tech-stack.md` |
| `docs/02_security.md` | `02-security.md` |
| `docs/03_user_types.md` | `03-user-types.md` |
| `docs/04_principles.md` | `04-principles.md` |
| `docs/05_architecture.md` | `05-architecture.md` |
| `docs/06_database.md` | `06-database.md` |
| `docs/07_api_contracts.md` | `07-api-contracts.md` |
| `docs/08_environments.md` | `08-environments.md` |
| `docs/09_design_system.md` | `09-design-system.md` (UI) |
| `docs/10_test_strategy.md` | `10-test-strategy.md` (tests) |
| `docs/12_marketing_seo.md` | `12-marketing-seo.md` (public web SEO — optional) |
| `docs/11_decisions.md` | `11-decisions.md` |

**Registry:** `.agent/skills/init-project/references/doc-templates.md`  
**Interview:** `init-interview-guide.md`  
**Audit:** skill `audit-phase-docs` + `/audit-docs`
