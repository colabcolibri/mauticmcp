---
name: mcp-integration
description: MCP and agent-tool boundary design for agentic products. Stack-agnostic. Use with /architecture mcp mode. Doc in 05 and optional docs/architecture/ detail.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# MCP integration (Meridian)

> **Scope:** `05_architecture.md` § Agent tools / MCP (and optional `docs/architecture/mcp.md`). **Contract only** — server implementation via `/implement-us`.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/architecture mcp` | MCP tool surface, auth, data boundaries |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/mcp-checklist.md` | **Mandatory** |
| `docs/02_security.md` | Agent safety, secrets, data classification |
| `docs/05_architecture.md` | System boundaries |
| `docs/07_api_contracts.md` | When MCP wraps HTTP |

## When to trigger

- Product exposes MCP server, agent tools, or IDE plugin bridges
- US adds tools/resources callable by external agents
- Cross-check with `02` AI-agent safety section

## Procedure

```txt
- [ ] mcp-checklist.md
- [ ] Update 05 § Agent tools / MCP index
- [ ] Optional detail file docs/architecture/mcp.md for tool catalog
- [ ] prepend-decision on new tool surface or expanded agent permissions
```

## Output

```txt
Mode: mcp
05 MCP section status:
Tools/resources catalogued:
Auth and data boundaries:
Next: /security-pass | /security-review | /implement-us
```
