# MCP integration checklist — `/architecture mcp`

> Protocol-agnostic patterns for **Model Context Protocol**-style tool servers and agent bridges.

## Scope

- [ ] List of tools/resources/prompts exposed to external agents
- [ ] Each tool has single responsibility and documented input schema
- [ ] Read vs write tools separated; destructive tools require human gate in product policy

## Security

- [ ] Authentication model for MCP transport (token, OAuth, local-only)
- [ ] Authorization per tool — least privilege; no blanket “run shell”
- [ ] Secrets never returned in tool responses or resource payloads
- [ ] User data scope: which docs/rows each tool may read (align `02`)
- [ ] Rate limits and abuse logging for networked MCP
- [ ] Align with Meridian `02` § AI-agent safety when kit is consumer

## Architecture

- [ ] MCP server placement in runtime diagram (`05` / diagrams)
- [ ] Failure modes: timeout, partial results, idempotent retries
- [ ] Versioning when tool schemas change (breaking vs additive)
- [ ] Relationship to HTTP API in `07` when both exist

## US alignment

- [ ] New tools require US with security acceptance
- [ ] `/security-review` on Must agent-surface US before close

## Out of scope

- Implementing MCP SDK code (→ `/implement-us`)
- Publishing to third-party MCP marketplaces (human)
