# Meridian kit

Portable agent harness for **Cursor**, **Claude Code**, **Codex**, **OpenCode**, **Antigravity**, and other AI IDEs.

**This package contains only the kit** (`.agent/` + installer). The VS Code extension is optional — it adds the in-IDE board and graphs. Full repo: [Meridian](https://github.com/colabcolibri/meridian).

## Which IDE do you use?

| IDE | What install does | Invoke in chat |
| --- | ----------------- | -------------- |
| **Cursor** | Copies `.agent/` + `.cursor/skills/` + `.cursor/agents/` symlinks | `/us-create`, `@story-maker`, … |
| **Claude Code** | Copies `.agent/` + `.claude/agents/` symlinks | same skills/agents |
| **Codex** | Copies `.agent/` + `.agents/skills/` + `.codex/` | workflow skills |
| **OpenCode** | Copies `.agent/` + `.opencode/skills/` + `.opencode/agents/` | skills + agents |
| **Antigravity / ag-kit** | Copies `.agent/` only (`--no-sync`) | reads `.agent/skills/` directly |
| **Other `.agent` tools** | Copies `.agent/` only (`--no-sync`) | depends on tool |

Default `./install.sh` syncs Cursor, Claude Code, Codex, and OpenCode adapters. Only Meridian symlinks and generated files are created; your own `.cursor/rules/` are never deleted.

## What gets installed

The full `.agent/` tree — **17 agents**, **skills** (procedures), rules, scripts, references, and HTML board (`python3 .agent/board`). Kit v3 has **no workflows folder** — procedures live in `.agent/skills/{name}/SKILL.md`.

See [DISTRIBUTION.md](DISTRIBUTION.md) for kit vs extension.

## Install into your project

```bash
chmod +x install.sh
./install.sh /path/to/your-project
```

Current directory:

```bash
./install.sh .
```

**Antigravity-only:**

```bash
./install.sh --no-sync /path/to/your-project
```

**Single IDE:**

```bash
./install.sh --cursor-only .
./install.sh --claude-only .
./install.sh --codex-only .
./install.sh --opencode-only .
```

Do **not** commit `.cursor/`, `.claude/`, `.agents/skills/`, `.codex/`, `.opencode/`, or symlinked `AGENTS.md` — regenerated per machine.

## After install

1. Open your project in your IDE.
2. Run **`/init-meridian`** if `docs/` does not exist yet.
3. Read [agents-help.md](references/guides/agents-help.md) or run **`/project-status`**. Lost? **`/deus-ex`**.

## Update the kit

```bash
./install.sh --force .
```

`--force` replaces `.agent/` and refreshes IDE adapters. Previous kit is backed up to `agent-backup/harness-<timestamp>.zip` (folder fallback if zip unavailable).

Re-sync adapters only:

```bash
./.agent/scripts/sync_kit.sh
./.agent/scripts/sync_kit.sh --cursor-only
./.agent/scripts/sync_kit.sh --dry-run
```

## Validate

```bash
python3 .agent/scripts/validate_meridian.py .
```

## Optional: VS Code / Cursor extension

**[Meridian Harness](https://marketplace.visualstudio.com/items?itemName=colabcolibri.meridian-vscode)** bundles the kit and installs it via **Meridian: Install Harness**. Status bar `harness A → B` means upgrade available — use **Upgrade Harness**.

Details: [app-visual-studio/README.md](../app-visual-studio/README.md)

## Author

[Sergio Luciano Jr](https://github.com/colabcolibri) · [colabcolibri/meridian](https://github.com/colabcolibri/meridian)

## License

PolyForm Noncommercial 1.0.0 — see `LICENSE`.
