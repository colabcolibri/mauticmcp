# Project areas — cycles, not extra agents

> **Stations** (who cooks vs who attests) live in [agent-station-map.md](./agent-station-map.md).  
> **Areas** are the cycles a product walks. Do not invent a new agent because an area feels empty.

Slash commands stay verb-first (`/create-us`). Skills are object-prefixed (`us-create`). There is no second folder for the old skill slug.

## The five areas

| Area | What it is | Phase (start-here) | Typical owners | Typical commands |
| ---- | ---------- | ------------------ | -------------- | ---------------- |
| **Discovery** | What problem, for whom, what is out | Before / during phase 1 | `product-owner`, `ux-researcher` | `/discover`, `/ux-pass` |
| **Standards** | How we build and protect (docs `01`–`10`, `02`, `06`, `08`, `09`) | writer, security, architect, ux-researcher, data-engineer, design, quality, devops | `/database-pass`, `/release-pass`, `/architecture`, `/security-pass`, `/design-pass`, `/test-pass` |
| **Planning** | What we will build in what order | Phase 3 | PO, planner, `story-maker`, `backlog-surveyor` | `/create-epic`, `/create-version`, `/plan-sprint`, `/survey-backlog`, `/create-us`, `/refine-us` |
| **Build** | The increment | Phase 4 | `developer` | `/implement-us` |
| **Attest** | Recipe ready + dish done + specialist reviews | Phase 3 end + phase 4 | `story-checker`, security-code, test-review, design-review | `/review-us`, `/security-review`, `/test-review`, `/design-review`, `/complete-us` |

Human `approved` on phase docs and git commit stay **outside** the agent line.

## Discovery vs document-project

| `/discover` | `/document-project` |
| ----------- | ------------------- |
| Product **intent** (`docs/discovery/product-brief.md`) | Code **as-is** (`docs/inventory/` + phase docs) |
| `product-owner` | `technical-writer` |
| May run with thin `docs/` | Brownfield documentation |

Mode B discovery **must** read the inventory (or record that it is missing). Do not treat the two commands as duplicates.

## What is not an area (do not staff it)

| Temptation | Why not |
| ---------- | ------- |
| Extra security or test or design agents | Same champion; **skills** split (`security-doc` vs `security-code`, `test-strategy` vs `test-review`, `design-flow` vs `design-theme` vs `design-system`) |
| Second PO for discovery | Same product judgment |
| Commit / push bot | Human git; `devops-engineer` documents `08` only |

## How to use this file

1. Name the area the project is in (`/deus-ex` allocates; `/status` reports).
2. Open the station map for cook vs attest **inside** that area.
3. If depth is missing, add a **skill** under the existing owner — do not add a station without updating `agent-station-map` and `agent-personas`.
