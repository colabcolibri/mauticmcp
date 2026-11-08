# IDE adapters (Meridian kit)

The kit source lives in **`.agent/`** (committed). How you wire it depends on your IDE.

## Quick reference

| IDE | Adapter folder | Sync needed? | Install flag |
| --- | -------------- | ------------ | ------------ |
| **Cursor** | `.cursor/` | Yes | default, or `--cursor-only` |
| **Claude Code** | `.claude/` | Yes | default, or `--claude-only` |
| **Codex** | `.agents/skills/`, `.codex/`, `AGENTS.md` | Yes | default, or `--codex-only` |
| **OpenCode** | `.opencode/` (+ `AGENTS.md` via Codex sync) | Yes | default, or `--opencode-only` |
| **Antigravity / ag-kit** | _(none)_ | No | `--no-sync` |
| **Other `.agent` indexers** | _(none)_ | No | `--no-sync` |

**Antigravity and similar tools read `.agent/` directly** — workflows, agents, and skills work without `.cursor/` or `.claude/`. Only install `.agent/`:

```bash
./install.sh --no-sync /path/to/project
```

## Sync script (all adapters — one command)

```bash
chmod +x .agent/scripts/sync_kit.sh   # once
./.agent/scripts/sync_kit.sh
```

`sync_cursor_kit.sh` still exists as a deprecated shim that forwards to `sync_kit.sh`.

### Surgical sync policy

- Never deletes adapter folders wholesale
- Creates/replaces **Meridian symlinks** (targets containing `.agent/`)
- Removes **orphan** Meridian symlinks when a workflow/agent/skill was removed from the kit
- **Never touches** real files or symlinks pointing outside `.agent/`

Options: `--cursor-only`, `--claude-only`, `--codex-only`, `--opencode-only`, `--no-prune`, `--dry-run`

## Uninstall

```bash
./.agent/scripts/uninstall-meridian-kit.sh          # remove IDE adapters only
./.agent/scripts/uninstall-meridian-kit.sh --all    # adapters + .agent/ + gitignore entries
```

Same surgical policy as sync: removes only Meridian symlinks, generated Codex TOMLs, and empty adapter dirs. Real files, foreign symlinks, `docs/`, and `.meridian/` are never touched.

## Install kit into another project

```bash
chmod +x /path/to/meridian/.agent/scripts/install-meridian-kit.sh
/path/to/meridian/.agent/scripts/install-meridian-kit.sh /path/to/my-project
```

Or from a project that already has `.agent/`:

```bash
./.agent/scripts/install-meridian-kit.sh .          # refresh copy + sync adapters
./.agent/scripts/install-meridian-kit.sh --force .  # overwrite .agent from source
./.agent/scripts/install-meridian-kit.sh --no-sync . # .agent only (Antigravity)
```

Set `MERIDIAN_KIT_SRC=/path/to/meridian/.agent` when the installer script is not run from the kit repo.

## Distribution (kit only — no app-desktop)

Build a release tarball:

```bash
# From meridian monorepo root
chmod +x .agent/scripts/package-kit.sh
KIT_VERSION=1.0.0 ./.agent/scripts/package-kit.sh
# → dist/meridian-kit-1.0.0.tar.gz
```

**Tarball contents:** `README.md`, `LICENSE`, `VERSION`, `install.sh`, `.agent/`  
**Not included:** `app-desktop/`, `app-visual-studio/`, extension VSIX.

**User install:**

```bash
tar -xzf meridian-kit-1.0.0.tar.gz
cd meridian-kit-1.0.0
./install.sh /path/to/my-project
```

**Future channels:** GitHub Releases (`kit-v*` + `extension-v*` tags with `.tar.gz` and `.vsix` assets). See [DISTRIBUTION.md](DISTRIBUTION.md).

Always edit in `.agent/` first; then run `./.agent/scripts/sync_kit.sh` for IDE adapters (`.cursor/references/templates/` included).

## What gets generated

| Adapter | Path | Contents |
| ------- | ---- | -------- |
| **Cursor** | `.cursor/` | rules, skills, agents, slash commands, template registry |
| **Claude Code** | `.claude/` | agents, slash commands |
| **Codex** | `.agents/skills/`, `.codex/`, `AGENTS.md` | skills (workflows + kit skills), subagent TOMLs, project guidance |
| **OpenCode** | `.opencode/` | slash commands, agents, skills |

Both adapters symlink workflows from `.agent/workflows/` as slash commands. Agents: flat `.cursor/agents/{slug}.md` → `.agent/agents/{slug}/agent.md` (persona); `references/` stays in `.agent/` only.

### Cursor mapping

| Cursor | Canonical source |
| ------ | ------------------ |
| `.cursor/rules/meridian.mdc` | `.agent/rules/meridian.mdc` |
| `.cursor/skills/` | `.agent/skills/` |
| `.cursor/agents/{slug}.md` | symlink → `.agent/agents/{slug}/agent.md` |
| `.cursor/commands/` | `.agent/workflows/` |
| `.cursor/references/templates/` | `.agent/references/templates/` |

### Claude Code mapping

| Claude Code | Canonical source |
| ----------- | ------------------ |
| `.claude/commands/` | `.agent/workflows/` |
| `.claude/agents/{slug}.md` | symlink → `.agent/agents/{slug}/agent.md` |

Claude Code does not mirror skills, rules, or templates — workflows and agents read `.agent/skills/` and templates from the repo when needed.

### Codex mapping

| Codex | Canonical source |
| ----- | ------------------ |
| `.agents/skills/<name>/` | `.agent/skills/<name>/` |
| `.agents/skills/workflow-<name>/SKILL.md` | `.agent/workflows/<name>.md` |
| `.agents/skills/meridian-authoring/SKILL.md` | `.agent/skills/doc.md` |
| `.codex/agents/<name>.toml` | generated from `.agent/agents/<name>/agent.md` |
| `AGENTS.md` (repo root, when safe) | `.agent/rules/AGENTS.md` |

Codex deprecated custom prompts (`~/.codex/prompts/`) in favor of skills — Meridian workflows are exposed as skills under `.agents/skills/`. Subagent TOMLs are generated (not symlinked) because Codex expects TOML, not Markdown.

### OpenCode mapping

| OpenCode | Canonical source |
| -------- | ---------------- |
| `.opencode/commands/<name>.md` | `.agent/workflows/<name>.md` |
| `.opencode/agents/<name>.md` | symlink → `.agent/agents/<name>/agent.md` |
| `.opencode/skills/<name>/` | `.agent/skills/<name>/` |
| `AGENTS.md` (repo root) | `.agent/rules/AGENTS.md` — read natively by OpenCode |

Notes:

- Workflows become `/commands` (symlinked); agents are **symlinked** like Cursor and Claude — canonical `agent.md` carries `mode: subagent` and `permission:` frontmatter (OpenCode-native; Cursor/Claude ignore extra keys).
- OpenCode has **no Meridian plugins** — agents use Bash/CLI (`meridian_delivery.py`) like other IDEs. Board UI stays in the VS Code extension.
- Kit skills already carry valid `SKILL.md` frontmatter (`name` + `description`). The `meridian-authoring` entry point (`.agent/skills/doc.md`) is intentionally not mirrored — it has no SKILL.md frontmatter and OpenCode validates strictly.
- OpenCode also reads `.agents/skills/*/SKILL.md` natively, so the Codex sync doubles as an extra skill surface.

## Git

`.cursor/`, `.claude/`, `.agents/skills/`, `.codex/`, `.opencode/`, and `AGENTS.md` (when symlinked) are in `.gitignore` — local adapters, not versioned duplicates. Do not commit them. Canonical source stays in `.agent/` (including `.agent/rules/AGENTS.md`).

## Native `.agent/` IDEs

Antigravity, ag-kit, and other tools that index `.agent/` directly need **no adapter** — use `--no-sync` on install and skip `sync_kit.sh`. Workflows, agents, and skills work from the committed folder.

See also: `.agent/KIT_README.md` (distribution package README).
