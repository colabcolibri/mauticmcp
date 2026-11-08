# mautic-mcp

A local MCP server for a self-hosted Mautic. Your agent creates, edits and deletes campaigns, emails and the rest of the marketing objects. The process stays on your machine. Nothing listens on a port, and the API password never leaves `server/.env`.

Campaigns and emails are created unpublished. Sending one email to one contact is off until you turn it on. Sending to a whole segment, and firing a campaign, are not in this server.

## What it can do

Every resource below can be searched and opened. In `operate` mode the agent can also create, edit and delete each one, except contacts: a contact is created or updated by email with `mautic_upsert_contact`.

| Resource | Also |
| --- | --- |
| Contacts | Upsert by email, recent activity, add a note, add or remove from a segment, campaign or stage, adjust points |
| Campaigns | List its contacts, clone it (the copy keeps the published flag), replace the whole canvas when events are sent |
| Emails | Send one email to one contact, only with `MAUTIC_ALLOW_SEND=true` |
| Segments | Add or remove a contact |
| Forms | Create, edit, delete. New forms are unpublished |
| Companies | Create, edit, delete. New companies are published |
| Categories | Bundle is campaign, email, form, page, asset, focus, point or stage |
| Pages | Landing pages. The detail includes the HTML, truncated when it is huge |
| Assets | Remote URL only. `title` and `remotePath`. No local file upload |
| Focus | Type is notice, form or link |
| Point actions | `name`, `type` and `delta`. Types come from `mautic_point_types` |
| Point triggers | `name` and the points threshold. Event types come from `mautic_point_types` |
| Point groups | Create, edit, delete |
| Stages | Add or remove a contact. New stages are published |
| Tags | The label is the `tag` field |
| Reports | `name` and `source`. Opening one by id runs it and returns up to 25 rows |

New campaigns, emails, forms, pages, assets, focus items, point actions and point triggers are unpublished. New segments, categories, companies and stages are published.

| Tool | What it does |
| --- | --- |
| `mautic_capabilities` | Current mode, the resource list, and what this server refuses. Does not call Mautic |
| `mautic_search` | Search any resource. At most 25 rows, no HTML |
| `mautic_get` | One record by id |
| `mautic_contact_activity` | Recent events for a contact |
| `mautic_campaign_contacts` | Contacts in a campaign |
| `mautic_point_types` | Point action types and trigger event types on this instance |
| `mautic_upsert_contact` | Create or update a contact by email |
| `mautic_create` | Create any resource except a contact |
| `mautic_update` | Edit any resource. Campaign events use PUT and replace the canvas |
| `mautic_delete` | Delete any resource. On by default. Requires `operate` |
| `mautic_membership` | Add or remove a contact from a segment, campaign or stage |
| `mautic_add_note` | Add a note to a contact |
| `mautic_adjust_points` | Add, subtract, multiply or divide a contact's points, or one point group's balance |
| `mautic_clone_campaign` | Clone a campaign |
| `mautic_send_email` | Send one email to one contact. Off until `MAUTIC_ALLOW_SEND=true` |
| `create_campaign` | Prompt. Builds a segment, an email and an unpublished campaign. Does not send |

`read` mode registers only the first six tools.

## What it will not do

- Open a network port or accept a connection from another machine
- Send an email to a segment
- Execute a campaign
- Talk to the projects API. On the instance this was built against, v1 returns 404 and v2 returns 403

## Connect it

Requires Node 20 or newer and pnpm.

1. In Mautic, open the gear, then Configuration, then API Settings. Enable the API and HTTP basic auth. Use a user whose role can touch the resources the agent will change.
2. Copy `server/.env.example` to `server/.env`. Set `MAUTIC_BASE_URL`, `MAUTIC_USERNAME` and `MAUTIC_PASSWORD`.
3. From `server/`:

```bash
pnpm install
pnpm build
```

4. Point the agent at the built file. The command is `node`, not `pnpm`. A package manager printing on stdout breaks the protocol. Use the absolute path to `node` when the app does not inherit your shell.

```json
{
  "mcpServers": {
    "mautic": {
      "command": "node",
      "args": [
        "--env-file=/absolute/path/mautic-mcp/server/.env",
        "/absolute/path/mautic-mcp/server/dist/index.js"
      ]
    }
  }
}
```

The same block goes in every client. Only the file changes.

| Client | Where it goes |
| --- | --- |
| Cursor | `.cursor/mcp.json` |
| Claude Code | `.mcp.json` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| VS Code | `.vscode/mcp.json` |
| Codex | `~/.codex/config.toml`, same `command` and `args` |

Restart the MCP entry after you edit `.env` or rebuild. Then ask the agent to list campaigns, or use the `create_campaign` prompt. That prompt builds a segment, an email and an unpublished campaign. It does not send.

## Modes

| Variable | Default | Effect |
| --- | --- | --- |
| `MAUTIC_MODE` | `read` | `operate` unlocks create, update, delete, membership, notes, points and clone |
| `MAUTIC_ALLOW_DELETE` | `true` | `mautic_delete`. Requires `operate` |
| `MAUTIC_ALLOW_SEND` | `false` | One email to one contact. Requires `operate` |

Basic auth is the mode to use: the API username and password on every request, over HTTPS. OAuth2 `client_credentials` is in the code (`MAUTIC_AUTH=oauth`) and the token body is form-encoded. Mautic's grant is fragile. Leave it alone unless you already know that grant works on your instance.

The write contract is in `server/docs/architecture/mcp.md`.

## Develop

From `server/`:

```bash
pnpm test
pnpm build
```

Tests use fake HTTP. They do not call your Mautic.
