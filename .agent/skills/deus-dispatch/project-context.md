# Project context — what deus-ex must read

Read **only** what you need to allocate. Do not ingest the whole `docs/` tree.

## Resolve where you are

1. Kit root. Monorepo: `.meridian/projects.json` → **active** product folder.
2. If no `docs/` → next is `scrum-master` `/init-meridian`. Stop after the envelope.

## Product (always, when `docs/` exists)

| Read | Why |
| ---- | --- |
| `docs/00_scope.md` (in/out, status) | What this product is. Without it, discovery — not build. |
| `docs/README.md` **or** frontmatter `status` on `00`–`05` | Which gate is open. |
| `docs/05_architecture.md` frontmatter `status` | `approved` before new US or product code. If not, next is `technical-architect` `/architecture` (or human approve). |

Do not read `01`–`04`, `06`–`11` unless the **manager’s ask** names that doc. Then you still **pass** to the owner; you do not rewrite it.

## Brownfield

If the ask is about existing code or “as-is”:

| Read | Why |
| ---- | --- |
| `docs/inventory/as-is.md` | Mode B map. If **missing**, say so in Evidence and prefer `technical-writer` `/document-project` (or `product-owner` `/discover` only for **intent**, not inventory). |

Do not run `/investigate` yourself. If you lack a code fact to choose writer vs developer, **pass** to `code-investigator` `/investigate` first.

## Delivery (read-only)

Use `meridian_delivery.py` — never raw SQL, never `update-*`.

| Command | Why |
| ------- | --- |
| `counts` | Open vs terminal load. |
| `lifecycle-hygiene` | Finished containers still open → `sprint-planner` close commands. |
| `list us --epic EPIC-XX` or `show US-XXXX` | Only when the ask names an id. |

Do not set `ready`, `in_progress`, or `status`.

## What you never treat as context

- Guessing stack from memory instead of `01` when the ask is explicitly stack — still **pass** to `technical-writer`.
- Opening every US in the version “to be thorough”.
- Secrets, `.env`, credentials.

## Enough vs not enough

**Enough:** you can fill Evidence with 1–3 facts (scope clause, `05` status, a count, an inventory miss).

**Not enough:** you cannot name the area. Ask the manager one question (problem / now vs later / which version) — then allocate or pass to `product-owner` `/discover`.
