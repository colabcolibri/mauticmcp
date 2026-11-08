# Close US contract — additive only (P0)

> **Read this before `/complete-us`.** This overrides any generic “copy the template” rule in `INDEX.md`.

---

## One sentence

**`/complete-us` adds what is missing — it never rebuilds the US from a template.**

---

## Source of truth

| Step | Command / file |
| ---- | ---------------- |
| 1 | `python3 .agent/scripts/meridian_delivery.py show US-XXXX --full` |
| 2 | Edit **that output** — add Record, flip acceptance `[x]`, update status |
| 3 | `patch-record` (preferred) or `update-us` with the **full edited document** |

The US body lives in SQLite. **Templates are not the US body on close.**

---

## What you ADD or UPDATE on close

| Area | Allowed change |
| ---- | ---------------- |
| Frontmatter | `status: ✅`, `tests_status: done` (and `tests_status: n/a` only when `tests: none`) |
| `## Record` | Replace placeholders with real paths, layers, Executed |
| `### Acceptance` | `[ ]` → `[x]` when evidence exists |
| `### Planned` | `[ ]` → `[x]` for steps you ran |
| `### Related decisions` | Add `YYYY-MM-DD — title` when you logged a decision |

Everything else from `/create-us` and `/refine-us` **stays as-is** unless the manager explicitly changed scope in-session.

---

## What you must NEVER do on close

| Forbidden | Why |
| --------- | --- |
| Copy `us-template.md` into `update-us` | Wipes Intent/Plan/Approach — empty template |
| Copy `implementation-template.md` into `update-us` | That file is **Record shape only**, not a full US |
| Send only `## Record` to `update-us` | `update-us` **replaces** entire `body_markdown` |
| Rebuild Why / Where / Approach from memory | Loses refined prose |
| Batch-close scripts (`.py` or loops) | Creates identical boilerplate across US |
| Shorten acceptance to one generic line | Destroys acceptance criteria |

---

## Persist (choose one)

### A — `patch-record` (default)

Send **only** frontmatter deltas + `## Record` + optional `### Acceptance` / Planned patches:

```bash
python3 .agent/scripts/meridian_delivery.py show US-0115 --full
python3 .agent/scripts/meridian_delivery.py patch-record US-0115 <<'EOF'
---
status: ✅
tests_status: done
---
## Record
### Files
- `path` — change
...
## Intent
### Acceptance
- [x] …
EOF
```

Intent/Plan/Approach in SQLite **remain untouched**.

### B — `update-us` (only if you must edit outside Record)

1. Run `show --full`.
2. Copy **the entire printed markdown** into your editor.
3. Change **only** the rows in the table above.
4. Pipe the **whole file** to `update-us`.

If the pasted body is shorter than `show --full` output, you are about to delete content — **stop**.

---

## Templates on close — what each file is for

| File | On `/complete-us` |
| ---- | ------------------- |
| `close-us-contract.md` | **This file** — rules |
| `implementation-template.md` | Example **headings** for Record — do not paste as US body |
| `us-template.md` | **Do not read for close body** — create/refine only |
| `section-contracts.md` | Which sections exist — Plan unchanged on close |

---

## Self-check before `patch-record` / `update-us`

- [ ] I ran `show --full` in this session
- [ ] Intent / Why / Where / Plan / Approach still match the refined US
- [ ] I am not pasting template markdown
- [ ] Record has real file paths (not “see git diff”)
- [ ] `patch-record` OR full `update-us` body includes preamble `**As**` … `**I want**` …

---

## Protocol failure

Deleting or replacing refined US content on close is equivalent to skipping `/refine-us` evidence — **blocked** by CLI close-quality gates when possible.
