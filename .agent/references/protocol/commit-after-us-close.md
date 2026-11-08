# Commit after US close (Meridian)

> Git snapshot **after** documentation closure — not a substitute for `/complete-us`.

## Position in the flow

```txt
/refine-us → implement → /complete-us → commit (human) → next US
```

| Step | Meridian `status: ✅` | Git |
| ---- | --------------------- | --- |
| `/complete-us` | Yes — Record filled in SQLite (**additive** — Intent/Plan preserved; see `close-us-contract.md`) | Diff read for evidence only |
| **Commit (human)** | Unchanged | One commit per closed US |

US closure and repository snapshot are **two done signals**. A story can be ✅ in SQLite while the working tree is still dirty until the manager commits.

## Who commits

| Actor | Rule |
| ----- | ---- |
| **Human manager** | Default — after reviewing diff and Record |
| **Agent** | Only when the manager explicitly asks |

Agents must **not** run `git commit` in the same turn that sets `status: ✅` unless explicitly requested.

## When to commit

- **After** `/complete-us` for that US.
- **Before** starting the next US in the same repo.
- **Not** during partial work (`🔶`).

## Scope (one US = one commit)

Include every file that US delivery justified:

- Product code touched by the slice
- Phase docs if that US changed them
- Kit changes if dogfooding Meridian itself

Delivery state lives in `.meridian/meridian.db` (gitignored) — not in the commit unless you export intentionally.

Do **not** mix two US ids in one commit unless the manager explicitly batches.

## Message format

```txt
<type>(<scope>): <short summary> (US-XXXX)
```

## Agent on `/complete-us`

Add under `### Executed`:

```md
- **suggested commit:** `feat(scope): short summary (US-XXXX)`
```

After human commit (optional):

```md
- **git commit:** `abc1234` — feat(scope): short summary (US-XXXX)
```

## Anti-patterns

- ✅ in US without ever committing
- Commit before Record is filled
- Agent auto-commit on `/complete-us` without explicit request
