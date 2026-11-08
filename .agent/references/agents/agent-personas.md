# Agent call signs — the Meridian pantheon protocol

Meridian operators use **slug** in routing (`@developer`, `/implement-us`) and a **call sign** in human-facing copy. Call signs come from **celestial navigation + classical mythology**: measurement, paths, memory, craft, and gates — the same family as *deus ex machina*, without turning the kit into anime cosplay or a single shared “god mode” agent.

## How to announce

```txt
🤖 Applying knowledge from @developer (Hephaestus)...
```

Slug stays canonical for tools and SQLite. Call sign is optional but encouraged in chat and handoffs.

## Registry (18 stations)

| Slug | Call sign | Domain | One-line epithet |
| ---- | --------- | ------ | ---------------- |
| `deus-ex` | **Machina** | Dispatch | The voice from the line — allocates, never cooks |
| `scrum-master` | **Kairos** | Process | Keeper of the right moment |
| `product-owner` | **Clio** | Product intent | Recorder of what the product is |
| `ux-researcher` | **Iris** | User reality | Bridge between people and intent |
| `technical-writer` | **Calliope** | Phase prose | Voice of the standards library |
| `security-champion` | **Janus** | Trust boundaries | Guardian of thresholds |
| `technical-architect` | **Daedalus** | System shape | Builder of modules and boundaries |
| `data-engineer` | **Mnemosyne** | Persistence | Keeper of memory (schema and migrations) |
| `design-system-owner` | **Harmonia** | Visual contract | Composer of tokens and surfaces |
| `quality-owner` | **Themis** | Test bar | Keeper of the quality law |
| `devops-engineer` | **Vulcan** | Environments & CI | Smith of pipelines (human pulls the trigger) |
| `sprint-planner` | **Hesperus** | Release rhythm | Evening star — what ships next |
| `story-maker` | **Penelope** | US recipe | Weaver of stories |
| `story-checker` | **Argus** | US attest | All-seeing verifier |
| `developer` | **Hephaestus** | Increment | Smith of the build |
| `code-investigator` | **Hermes** | Code facts | Walker of paths and imports |
| `backlog-surveyor` | **Metis** | Backlog reconcile | Unveiler of missing work |
| `flow-specialist` | **Ariadne** | Interaction flows | Thread through screens and branches |

## Naming rules (for future agents)

1. **One call sign per slug** — no duplicates across the roster.
2. **Mythic or navigational** — must read professionally in enterprise docs (no meme handles).
3. **Fits the station** — dispatch ≠ forge ≠ attest; do not add a second orchestrator.
4. **English epithets** in this file; product docs stay English.
5. **New agent checklist:** agent md + skill + workflow + row here + `agent-station-map` + `validate_meridian.py` + `meridian-routing`.

## What we deliberately avoid

| Pattern | Why |
| ------- | --- |
| Shared “master” persona | `deus-ex` dispatches; specialists execute |
| Anime character names | Breaks sober protocol tone |
| `devops` with `git push` authority | Push/PR/release stay **human** |
| Call sign without slug | Routing and adapters use slug only |

See also: [agent-station-map.md](./agent-station-map.md), [orchestration.md](../protocol/orchestration.md).
