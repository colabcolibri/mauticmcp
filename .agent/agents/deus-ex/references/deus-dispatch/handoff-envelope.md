# Handoff envelope

Every `/deus-ex` answer uses this block. Then stop.

```txt
Station: dispatch
Agent: deus-ex
Area:
Done:
Blocker:
Next agent:
Next command:
Artifact id:
Evidence:
```

## Field rules

| Field | Rule |
| ----- | ---- |
| **Area** | One of: discovery, standards, planning, build, attest |
| **Done** | What you understood (one or two sentences). Not a US Record. |
| **Blocker** | Gate or missing doc. `none` if clear. |
| **Next agent** | Kit slug (`story-maker`, …). Never `deus-ex` as the worker. |
| **Next command** | Exact slash + id when known (`/refine-us US-0205`). |
| **Artifact id** | `US-` / `EPIC-` / doc path / `none` |
| **Evidence** | 1–3 facts from `project-context.md` (file + status, or CLI). No empty Evidence. |

## Announce

`🤖 Applying knowledge from @deus-ex...` then the block. Do not also announce the **next** agent as if you were them.
