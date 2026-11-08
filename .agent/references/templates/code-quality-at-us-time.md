# Code quality at US time — DRY and single responsibility

Team conventions live in `docs/04_principles.md`. Agents **read** that file at refine and implement — do not invent parallel rules in chat.

---

## DRY (don't repeat yourself)

### At `/create-us`

- **Out of scope** — state when the slice must not duplicate logic that already exists elsewhere.
- **Why / Where** — if the problem is “two places do the same thing”, name the consolidation goal.

### At `/refine-us` (Approach)

- Name **existing** module, hook, context, or validator to **reuse** before adding code.
- One source of truth per constant, filter state, and validation rule (per `04_principles`).
- If a new shared module is required, say where it lives (layer/path) and what it replaces.

### At `/implement-us`

- Extend existing functions and components; avoid copy-paste variants unless the US accepts them.
- Shared logic → domain or shared module per `04_principles` and Architecture refs.
- Do not re-implement protocol rules already in kit scripts or domain validators.

---

## Single responsibility (SRP)

### At `/create-us`

- One US = one slice. If the request bundles UI + API + migration, split or narrow before Write.
- **Out of scope** — list adjacent work that would violate SRP if included.

### At `/refine-us` (Approach)

- Each bullet maps to **one** layer or concern (domain vs feature vs UI vs script).
- Fail refine if a bullet mixes unrelated layers without splitting the US.
- Align with layer table in `04_principles` and `05_architecture.md`.

### At `/implement-us`

- New files follow layer boundaries from `04_principles` and Architecture refs.
- Do not expand scope into refactors outside the US — open a follow-up US instead.

---

## Checklist (refine + implement)

| # | Check | Pass when |
| - | ----- | --------- |
| DRY | Approach names reuse targets **or** justifies a new shared module with path |
| SRP | Slice + Approach stay one concern; Out of scope lists creep risks |
| Principles read | Agent read `docs/04_principles.md` (DRY + SRP sections) this session |

---

## Anti-patterns

- Approach bullet: “add helper in component” when domain already has the rule
- One US changing monitor filter + board export + extension activation
- New `utils.ts` dumping unrelated functions “for later”
