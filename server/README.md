# mautic-mcp

Local MCP server for the Mautic v1 API. Cursor talks to it over stdio. It creates, updates and deletes campaigns, emails, segments, forms, companies, categories, pages, assets, focus items, points, stages, tags, reports and contacts.

Campaigns and emails are created unpublished. Sending to one contact stays off until you turn the flag on. Sending to a whole segment and executing a campaign are not in this server.

The contract is in `docs/architecture/mcp.md`.

## Use it in Cursor

Cursor starts `server/dist/index.js` from `.cursor/mcp.json` at the repository root. Credentials live only in `server/.env`, which is not committed.

1. In Mautic: gear, Configuration, API Settings. Turn on API enabled and HTTP basic auth. Use a user whose role can access the resources the agent will change.
2. Open `server/.env` and set `MAUTIC_BASE_URL`, `MAUTIC_USERNAME` and `MAUTIC_PASSWORD`. `MAUTIC_MODE` is already `operate`, so the agent can create, edit and delete. Sending email stays off.
3. In Cursor: Settings, MCP. The `mautic` server should turn green. If it says a variable is missing, `.env` is still empty. After saving `.env`, toggle the server off and on.

In chat, ask it to list campaigns or use the `create_campaign` prompt.

`read` only looks up. `operate` creates, updates and deletes. `MAUTIC_ALLOW_DELETE=true` and `MAUTIC_ALLOW_SEND=true` both require `operate`.

To develop, from `server/`:

```bash
pnpm install
pnpm test
pnpm build
```

OAuth2 uses `MAUTIC_AUTH=oauth`, `MAUTIC_CLIENT_ID`, `MAUTIC_CLIENT_SECRET` and `MAUTIC_TOKEN_URL`. The token request is form-encoded `client_credentials`, not JSON. It works only when the instance grants that grant type.

The `create_campaign` prompt follows segment, email, campaign, and does not send.
