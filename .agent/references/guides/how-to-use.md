# How to use Meridian

> **Start here.** One page — extension vs chat, what you type, and where to read next.  
> This file does not list every command; use [agents-help.md](./agents-help.md) as lookup (Ctrl+F).

---

## Two surfaces, one manager (you)

| You want to… | Use | Example |
| ------------ | --- | ------- |
| See kanban, versions, epics | **Extension** (views) | Meridian: Open Board |
| Validate structure | **Extension** | Meridian: Validate Project |
| Workspace health (kit, DB, adapters) | **Extension** | Meridian: Doctor |
| Create or change docs / backlog | **Chat slash command** | `/init-meridian`, `/create-us`, `/survey-backlog` |
| Health check and next step | **Chat** | `/status` |
| Unsure which station is next | **Chat** | `/deus-ex` |

**Rule:** extension = **see and validate**; chat = **create and change**.

---

## What you type (and what you do not)

```txt
YOU type          →  /us-create  or  @story-maker    skill / agent  (.agent/skills/)
workflow routes   →  @story-maker            agent     (.agent/agents/{slug}/agent.md)
agent loads       →  references/us-create/   station   (.agent/agents/{slug}/references/)
shared only       →  init-project, …         skill     (.agent/skills/)  ← cross-station only
output lands in   →  docs/ + .meridian/meridian.db
```

| Layer | You invoke? |
| ----- | ----------- |
| **Workflow** (`/…`) | **Yes** — normal entry |
| **Agent** (`@name`) | Override or direct station call |
| **Station references** | **No** — agent loads from `agents/{slug}/references/` |
| **Shared skill** | **No** — agent loads when cross-station |

---

## First-time setup

1. Install **Meridian Harness** extension and reload.
2. Open your project folder.
3. **Meridian: Install Harness** — copies `.agent/` (agents, skills, workflows). Later, if the status bar shows `harness A → B`, run **Meridian: Upgrade Harness** (backs up the previous kit to `agent-backup/harness-<timestamp>.zip` before overwrite; reload does not copy a new kit).
4. **Meridian: Open Welcome** — first-value checklist (kit, docs, delivery DB, adapters).
5. In chat: **`/init-meridian`** if `docs/` does not exist yet.
6. Brownfield: then **`/document-project`** (documents code — no US for legacy); optional **`/survey-backlog`** (`@backlog-surveyor`) to draft missing US after `05` is approved.
7. **Meridian: Open Board** — reads `.meridian/meridian.db`. Columns are **not** separate fields: 📋 Backlog = `ready: false` + `status: ❌`; 📌 Todo = `ready: true` + `status: ❌`; agents only edit `status` and `ready` in chat/CLI.

Optional anytime: **`/audit-docs`** — gap report on phase docs.

---

## Reading order (human guides)

| Order | File | Purpose |
| ----- | ---- | ------- |
| **1** | **This file** (`how-to-use.md`) | Entry — surfaces, layering, setup |
| **2** | [start-here.md](./start-here.md) | **Concepts** — phases, gates, artifacts (no command lists) |
| **3** | [usage-guide.md](./usage-guide.md) | **Recipes** — “if situation X, do Y” |
| **4** | [agents-help.md](./agents-help.md) | **Reference** — all slash commands, agents, steps 1–20 (lookup, not linear read) |
| — | [ide-integration.md](../protocol/ide-integration.md) | IDE matrix, adapter parity, external harness bridge |
| — | [orchestration.md](../protocol/orchestration.md) | Specialist flow, `/deus-ex`, thin layers above Meridian |
| — | [artifact-reference.md](../protocol/artifact-reference.md) | Field-level US / epic / version / sprint detail |

In the IDE: Meridian sidebar → **Commands** → guide entries open the same kit files.

---

## Bootstrap once per product

| Situation | Commands |
| --------- | -------- |
| New idea, no `docs/` | `/discover` (optional) → `/init-meridian` |
| Existing code, no `docs/` | `/init-meridian` → `/document-project` |
| `docs/` already exists | Skip init — use `/audit-docs` or [usage-guide](./usage-guide.md) |

Init is **not** every session — only when the Meridian tree is missing.

---

## Related

| Audience | File |
| -------- | ---- |
| Kit maintainers | [instruction-surfaces.md](../protocol/instruction-surfaces.md), [station-references.md](../protocol/station-references.md) |
| Agents (protocol) | `.agent/MERIDIAN.md`, `.agent/rules/MERIDIAN.md` |
| Extension command list | Meridian: **Extension commands** (palette) |
