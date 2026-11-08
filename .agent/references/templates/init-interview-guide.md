# Init interview guide — before writing phase docs

> Use during `/init-meridian` (Mode A or B) and `/discover`. **Do not Write** phase docs until the interview gate passes or the manager explicitly skips with written assumptions.

---

## Interview gate

| Situation | Action |
| --------- | ------ |
| Manager gave rich context in the same message | Confirm 1–2 inferences; skip redundant questions |
| Thin or missing context | Run **full bank** for the mode (below) |
| Mode B after code read | Lead with inferences; ask only gaps |

**Pass when:** you can draft `00_scope` Problem + Users + In scope with **no invented product facts**, or assumptions are listed in Open questions.

---

## Mode A — greenfield (max 8 questions, stop when clear)

1. **Problem** — What pain does this product solve? What happens today without it?
2. **Users** — Who uses it (role, context, technical level)? Primary vs secondary?
3. **Success** — What does “working” look like in 3–6 months?
4. **In scope (v1)** — What must ship in the first release?
5. **Out of scope** — What are you explicitly **not** building now?
6. **Stack** — Languages, frameworks, hosting, monorepo vs single app — fixed or open?
7. **Security / data** — Auth? PII? Payments? Compliance?
8. **Constraints** — Team size, deadline, budget, must-use tools?

Optional: recommend `/discover` first when the idea is still fuzzy → `docs/discovery/product-brief.md`.

---

## Mode B — existing codebase (max 6 questions after code read)

Present inferences first: “From the repo I see [X]. Correct?”

1. **Product intent** — Is the README accurate? What is the product **for** users?
2. **Users** — Who uses this in production or dev today?
3. **Current state** — What is already shipped vs WIP vs abandoned?
4. **Next release** — What is in scope for the **next** increment (not documenting everything as backlog)?
5. **Security** — Auth model, secrets, sensitive data — anything not visible in code?
6. **Documentation goal** — Document as-is only, or also capture planned direction?

**Never ask** to create US for legacy shipped work in this interview.

---

## After interview — which command creates what

| Step | Command / skill | Creates or updates |
| ---- | ----------------- | ------------------ |
| 1 | `/discover` (optional) | `docs/discovery/product-brief.md` |
| 2 | `/init-meridian` Mode A | Full `docs/` tree + **all** phase docs `00`–`08`, `11`, `README` from `phase-docs/` |
| 3 | `/init-meridian` Mode B | `docs/` tree + bootstrap; then **`/document-project`** |
| 4 | `/document-project` | `docs/inventory/as-is.md` + populate phase docs from code (**no US**) |
| 5 | Human review | Approve docs in order: `00` → `01` → `02` → `03` → `04` |
| 6 | `/architecture`, `/security-pass` | Deepen `05`, `02` |
| 7 | `/audit-docs` | Gap report vs `phase-docs/` guides; optional draft fixes when docs drift mid-project |

---

## Anti-patterns

- Creating phase docs with only `##` headings and no body
- Mode B: creating epics/US for every existing feature
- Skipping interview because “we’ll fill later” — mark **Open questions** instead
- Approving `05_architecture` before `04_principles` has real layer paths
