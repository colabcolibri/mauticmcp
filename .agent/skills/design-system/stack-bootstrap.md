# Stack bootstrap — from `01_tech_stack` to `09_design_system`

> Run during `/design-pass` when `09` is `draft` or after stack change in `01_tech_stack.md`.

## Procedure

```txt
Task progress:
- [ ] Read docs/01_tech_stack.md (frontend + styling lines)
- [ ] Pick stack id from ui-stack-catalog.md
- [ ] Read component-composition-pattern.md (mandatory)
- [ ] Fill 09 tokens using stack-native theme mechanism
- [ ] Record primitive vs composed paths in 09 § Components
- [ ] Optional: mood pass from DESIGN.md / awesome-design-md (tokens only)
- [ ] Suggest showcase US via /design-showcase when UI product
```

## Step 1 — Detect stack

See `ui-stack-catalog.md` table → open **`stacks/{id}.md`** (full implementation model).

## Step 2 — Write paths into `09`

```markdown
## Components

- **Primary UI stack:** `ts-shadcn` (see kit `ui-stack-catalog.md` § ts-shadcn)
- **Primitives (read-only):** `components/ui/`
- **Composed templates:** `components/app/`
- **Composition pattern:** config-driven props (`title`, `description`, `body`, `footer`, `variant`, `size`)
```

## Step 3 — Token bootstrap

Read **`stacks/{id}.md` § Theme** — copy structure into `09` § Colors; implement theme files in **implement-us** (DS-S1), not in `/design-pass`.

| Stack | Theme file(s) — see stack ref |
| ----- | ------------------------------- |
| All | Listed in `stacks/{id}.md` |

Map semantics: `primary`, `secondary`, `muted`, `accent`, `destructive`, `border`, `ring`, `background`, `foreground`.

## Step 4 — Optional mood (aesthetic only)

After stack is fixed:

1. Browse [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) for **density and tone** similar to `00_scope`.
2. Translate mood into **your** semantic tokens — never ship "Linear purple" or "Stripe gradient" as product identity unless scope says so.
3. Copy section **names** from [DESIGN.md spec](https://github.com/google-labs-code/design.md) into `09` prose.

## Step 5 — Composed inventory seed

Minimum templates to plan (implement in showcase US):

- `AppDialog`
- `AppSheet` / drawer (if stack has it)
- `AppButton` (only if product needs consistent labels/icons wrapper)
- `AppFormField` (label + control + error)
- `AppEmptyState`
- `AppPageHeader` (title + actions slot)
- `AppDataTable` or list row (if data-heavy UI)

## Output block (paste after `/design-pass`)

```txt
Stack id:
Primitive path:
Composed path:
Theme file(s):
Composed templates planned:
Showcase routes (if any):
09 status:
Next: /design-showcase | /refine-us US-XXXX | human review
```
