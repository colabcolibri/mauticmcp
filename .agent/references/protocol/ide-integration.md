# IDE integration and defensive posture

Meridian is **not** a generic “run everything” AI framework. It is a **defensive delivery protocol**: phase docs, SQLite backlog, specialist agents per station, and gates before code ships.

This document states what each IDE can enforce, what stays in chat/CLI, and how external harnesses can connect without replacing Meridian.

---

## Design principle: specialists, not a mega-agent

| Layer | Role |
| ----- | ---- |
| **P0 rules** | Non-negotiable gates (`ready`, architecture approved, evidence on close) |
| **Workflows** (`/create-us`, `/implement-us`, …) | What the human types — routes to one station |
| **`@deus-ex`** | Orchestration only — allocates the next agent/slash; does not cook stories or code |
| **Specialist agents** | `story-maker`, `developer`, `quality-owner`, … — one job each |
| **Extension (optional)** | Read-mostly: board, graphs, doctor, harness install — not the source of truth |

Meridian already provides **agentic flow** through workflow → agent → skill. You do not need a second orchestration engine on top unless you want cross-repo automation; use `/deus-ex` inside the protocol first.

---

## IDE capability matrix (honest)

| IDE / CLI | Meridian adapters | Runtime hooks | Practical impact |
| --------- | ----------------- | ------------- | ---------------- |
| **Cursor / VS Code** | `.cursor/` via `sync_kit.sh` | No lifecycle hooks like Claude Code | Rules + slash commands + extension UI; gates enforced by agent discipline + `validate_meridian.py` |
| **Claude Code** | `.claude/` | Strongest hook story in the ecosystem | Same kit; optional future: hook helpers for implement/close gates |
| **Codex** | `.agents/skills/`, `.codex/` | Skills + subagents | Workflow skills mirror slash commands |
| **OpenCode** | `.opencode/` | Plugin kanban possible | Commands/agents synced from kit |
| **Antigravity / .agent-native** | Read `.agent/` directly | Varies | No sync required |

**Meridian is more defensive than most harnesses** because:

- Backlog lives in **SQLite**, not editable story markdown alone
- **Structural validators** (`validate_meridian.py`, section contracts) run in CI and locally
- **Implement and close gates** are protocol law, not suggestions
- **Extension does not auto-install** the kit — explicit Install/Upgrade Harness

---

## Adapter parity contract

Source of truth: **`.agent/`** only.

Generated (gitignored): `.cursor/`, `.claude/`, `.agents/skills/`, `.codex/`, `.opencode/`, `AGENTS.md`.

After changing workflows or agents in `.agent/`:

```bash
./.agent/scripts/sync_kit.sh
python3 .agent/scripts/validate_kit_parity.py .
```

CI on the Meridian monorepo runs parity in strict mode after sync.

---

## Connecting an external harness

Another kit (e.g. domain-specific agents, custom CLI) can **sit beside** Meridian without merging into one mega-framework:

1. **Keep Meridian as delivery SOT** — `docs/`, `.meridian/meridian.db`, slash workflows for plan/refine/implement/close.
2. **Use external tools for execution only** — e.g. codegen, infra, research — behind `/deus-ex` or a named specialist agent you add under `.agent/agents/`.
3. **Do not duplicate backlog** — external task lists should map to US rows in SQLite or be treated as ephemeral; Meridian board stays canonical.
4. **Run doctor before sprint work** — `python3 .agent/scripts/meridian_doctor.py` or **Meridian: Doctor** in the extension.

Optional pattern: a thin **orchestration skill** that calls your external CLI and then returns control to Meridian workflows (`/complete-us`, `/status`). See `orchestration.md`.

---

## First-value checklist (10 minutes)

Binary “ready to deliver” for a new workspace:

1. **Install harness** — `.agent/` present (extension or kit script)
2. **Init docs** — `/init-meridian` → `docs/00_scope.md` exists
3. **Delivery DB** — `.meridian/meridian.db` exists
4. **Adapters synced** — `.cursor/commands/` (or your IDE’s adapter) matches `.agent/workflows/`

Then: **Open Board** + `/status` in chat. Extension **Welcome** tab shows live checklist state.

---

## Commands

| Tool | Command |
| ---- | ------- |
| Doctor | `python3 .agent/scripts/meridian_doctor.py [project-root]` |
| Parity | `python3 .agent/scripts/validate_kit_parity.py [project-root]` |
| Structure | `python3 .agent/scripts/validate_meridian.py [project-root]` |
| Sync adapters | `./.agent/scripts/sync_kit.sh` |

Extension: **Meridian: Doctor**, **Meridian: Validate Project**, **Meridian: Upgrade Harness** (backs up `.agent/` before overwrite).
