---
title: MCP Mautic
updated: 2026-11-08
---

# MCP Mautic

Server contract. Overview in `docs/05_architecture.md`.

## Policy

| Env | Default | Effect |
| --- | --- | --- |
| `MAUTIC_MODE` | `read` | `operate` enables create, update, upsert, membership, notes, points and clone |
| `MAUTIC_ALLOW_DELETE` | `true` | Enables `mautic_delete`. Requires `operate` |
| `MAUTIC_ALLOW_SEND` | `false` | Enables `mautic_send_email` for one contact. Requires `operate` |

A disabled tool is absent from `tools/list`. The agent does not see it.

## Tools

| Tool | Action |
| --- | --- |
| `mautic_capabilities` | Effective policy and resources. Does not call Mautic |
| `mautic_search` | Paged search, limit 25 |
| `mautic_get` | One id. Getting a report executes it |
| `mautic_contact_activity` | Recent contact events |
| `mautic_campaign_contacts` | Contacts in a campaign |
| `mautic_point_types` | Point action types and trigger event types |
| `mautic_upsert_contact` | Create or update by `email` |
| `mautic_create` | Campaign, email, segment, form, company, category, page, asset, focus, points, trigger, group, stage, tag, report |
| `mautic_update` | Update a resource. Campaign events replace the canvas (PUT) |
| `mautic_membership` | Add or remove a contact from a segment, campaign or stage |
| `mautic_adjust_points` | Add, subtract, multiply or divide a contact point balance |
| `mautic_add_note` | Note on a contact |
| `mautic_clone_campaign` | Copy of the campaign, including published state |
| `mautic_delete` | Delete a resource |
| `mautic_send_email` | `POST /api/emails/{id}/contact/{contactId}/send` |

Prompt `create_campaign`: segment, then email, then campaign, without sending.

## Writes Mautic requires

Campaign (`POST /api/campaigns/new`, and `PUT` when `events` are present):

- `events` with `id`, `name` and `type`
- `lists` or `forms`
- `canvasSettings` together with events, otherwise Mautic stores the campaign without the flow. If the argument is omitted, the server builds a linear flow: source `lists` or `forms`, then the events in order

A segment email (`emailType: list`) requires `lists`. A template email does not.

Campaign source ids are sent as `{ "id": n }`. Email list ids are sent as a number array, which is the stable shape for that route.

A tag is stored in the `tag` field. A report requires `name` and `source`. `mautic_get` on a report returns the executed rows, capped at 25.

## Publish defaults on create

| Resource | `isPublished` omitted |
| --- | --- |
| Campaign, email, form, page, asset, focus, point action, point trigger | 0 |
| Segment, category, company, stage | 1 |
| Tag, point group, report | field omitted |

## Out of the server

- `POST /api/emails/{id}/send` (whole segment)
- execute a campaign
- local file upload
- API v2 `/api/v2/projects` (this instance returned 403)

## Auth

Basic: API username and password, `Authorization: Basic`.

OAuth2: `POST` to the token endpoint with `application/x-www-form-urlencoded` and `grant_type=client_credentials`. The body is `URLSearchParams`, not JSON. There is no `refresh_token`. A 401 fetches another access token and retries the call once.
