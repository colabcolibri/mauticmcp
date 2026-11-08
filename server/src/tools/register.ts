import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import {
  campaignContactsSchema,
  cloneSchema,
  contactIdSchema,
  createSchema,
  idSchema,
  membershipSchema,
  adjustPointsSchema,
  noteSchema,
  searchSchema,
  sendSchema,
  updateSchema,
  upsertSchema,
} from '../mautic/schema.js';
import { enabledTools } from '../policy.js';
import type { ToolContext } from './context.js';
import { campaignContacts, capabilities, contactActivity, getOne, pointTypes, search } from './read.js';
import {
  addNote,
  adjustPoints,
  cloneCampaign,
  createResource,
  membership,
  removeResource,
  sendEmail,
  updateResource,
  upsertContact,
} from './write.js';

const readOnly = { readOnlyHint: true, destructiveHint: false, openWorldHint: true };
const write = { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: true };

export function registerTools(server: McpServer, ctx: ToolContext): void {
  const enabled = new Set(enabledTools(ctx.policy));

  if (enabled.has('mautic_capabilities')) {
    server.registerTool(
      'mautic_capabilities',
      {
        description: 'Returns the current mode, what can be created, and what this server refuses. Does not call Mautic.',
        inputSchema: z.object({}).shape,
        annotations: readOnly,
      },
      async () => capabilities(ctx),
    );
  }

  if (enabled.has('mautic_search')) {
    server.registerTool(
      'mautic_search',
      {
        description: 'Searches a Mautic resource. The response is short and omits HTML.',
        inputSchema: searchSchema.shape,
        annotations: readOnly,
      },
      async (args) => search(ctx, args),
    );
  }

  if (enabled.has('mautic_get')) {
    server.registerTool(
      'mautic_get',
      {
        description: 'Loads one resource by id. Emails, pages and report runs include their body, truncated when huge. Getting a report executes it.',
        inputSchema: idSchema.shape,
        annotations: readOnly,
      },
      async (args) => getOne(ctx, args),
    );
  }

  if (enabled.has('mautic_contact_activity')) {
    server.registerTool(
      'mautic_contact_activity',
      {
        description: 'Recent activity for a contact.',
        inputSchema: contactIdSchema.shape,
        annotations: readOnly,
      },
      async (args) => contactActivity(ctx, args),
    );
  }

  if (enabled.has('mautic_campaign_contacts')) {
    server.registerTool(
      'mautic_campaign_contacts',
      {
        description: 'Contacts in a campaign.',
        inputSchema: campaignContactsSchema.shape,
        annotations: readOnly,
      },
      async (args) => campaignContacts(ctx, args),
    );
  }

  if (enabled.has('mautic_point_types')) {
    server.registerTool(
      'mautic_point_types',
      {
        description: 'Lists point action types and point trigger event types accepted by this instance.',
        inputSchema: z.object({}).shape,
        annotations: readOnly,
      },
      async () => pointTypes(ctx),
    );
  }

  if (enabled.has('mautic_upsert_contact')) {
    server.registerTool(
      'mautic_upsert_contact',
      {
        description: 'Creates or updates a contact by email. If it already exists and no other field was sent, returns the contact without writing again.',
        inputSchema: upsertSchema.shape,
        annotations: { ...write, idempotentHint: true },
      },
      async (args) => upsertContact(ctx, args),
    );
  }

  if (enabled.has('mautic_create')) {
    server.registerTool(
      'mautic_create',
      {
        description: [
          'Creates a campaign, email, segment, form, company, category, page, asset, focus item, point action, point trigger, point group, stage, tag or report.',
          'Campaigns, emails, assets, focus items and points are created unpublished. Segments and stages are created published.',
          'A campaign requires name, events (id, name, type) and lists or forms.',
          'Without canvasSettings the server builds a linear flow. type email.send with properties.email set to the email id sends that email inside the campaign.',
          'An email requires name and subject. emailType list requires lists. A template email uses emailType template.',
          'A segment accepts filters: [{ glue, field, object, type, operator, properties: { filter } }].',
          'A category requires title and bundle (campaign, email, form, page, asset, focus, point or stage).',
          'An asset requires title and remotePath. A focus item requires name and type (notice, form or link).',
          'A point action (points) requires name, type and delta. A trigger (pointTriggers) requires name and points.',
          'A tag uses the tag field. A report requires name and source.',
          'projects, when the entity accepts it, is a list of ids.',
          'This tool does not send email and does not execute a campaign.',
        ].join(' '),
        inputSchema: createSchema.shape,
        annotations: write,
      },
      async (args) => createResource(ctx, args),
    );
  }

  if (enabled.has('mautic_update')) {
    server.registerTool(
      'mautic_update',
      {
        description: 'Updates a resource. On a campaign, events triggers PUT and replaces the whole canvas: resend name, events and lists or forms.',
        inputSchema: updateSchema.shape,
        annotations: { ...write, idempotentHint: true },
      },
      async (args) => updateResource(ctx, args),
    );
  }

  if (enabled.has('mautic_membership')) {
    server.registerTool(
      'mautic_membership',
      {
        description: 'Adds or removes a contact from a segment, a campaign or a stage.',
        inputSchema: membershipSchema.shape,
        annotations: write,
      },
      async (args) => membership(ctx, args),
    );
  }

  if (enabled.has('mautic_add_note')) {
    server.registerTool(
      'mautic_add_note',
      {
        description: 'Adds a note to a contact.',
        inputSchema: noteSchema.shape,
        annotations: write,
      },
      async (args) => addNote(ctx, args),
    );
  }

  if (enabled.has('mautic_adjust_points')) {
    server.registerTool(
      'mautic_adjust_points',
      {
        description: 'Adds, subtracts, multiplies or divides a contact point balance. With groupId, changes that point group balance.',
        inputSchema: adjustPointsSchema.shape,
        annotations: write,
      },
      async (args) => adjustPoints(ctx, args),
    );
  }

  if (enabled.has('mautic_clone_campaign')) {
    server.registerTool(
      'mautic_clone_campaign',
      {
        description: 'Clones a campaign. The copy keeps isPublished. Check the result and unpublish it if the copy should not be live.',
        inputSchema: cloneSchema.shape,
        annotations: write,
      },
      async (args) => cloneCampaign(ctx, args),
    );
  }

  if (enabled.has('mautic_delete')) {
    server.registerTool(
      'mautic_delete',
      {
        description: 'Deletes a resource. Only registered when MAUTIC_ALLOW_DELETE=true.',
        inputSchema: idSchema.shape,
        annotations: { ...write, destructiveHint: true },
      },
      async (args) => removeResource(ctx, args),
    );
  }

  if (enabled.has('mautic_send_email')) {
    server.registerTool(
      'mautic_send_email',
      {
        description: 'Sends one email to one contact. Only registered when MAUTIC_ALLOW_SEND=true. Does not send to a whole segment.',
        inputSchema: sendSchema.shape,
        annotations: { ...write, destructiveHint: true },
      },
      async (args) => sendEmail(ctx, args),
    );
  }
}

export function registerPrompts(server: McpServer): void {
  server.registerPrompt(
    'create_campaign',
    {
      title: 'Create campaign',
      description: 'Safe order to create a segment, an email and a campaign without sending',
      argsSchema: { goal: z.string().min(1).max(500).describe('What the campaign should do') },
    },
    ({ goal }) => ({
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: [
              `Goal: ${goal}`,
              '1. Call mautic_capabilities.',
              '2. If canWrite is false, stop and ask for MAUTIC_MODE=operate.',
              '3. Create or find the segment. A new segment is published.',
              '4. Create the email with subject and customHtml. Leave isPublished false until review.',
              '5. Create the campaign unpublished with one email.send event pointing at the email id and lists set to the segment id.',
              '6. Show names, ids and a short HTML summary. Do not send and do not publish without an explicit yes.',
              '7. Sending to one contact exists only when canSend is true. Sending to a whole segment does not exist on this server.',
            ].join('\n'),
          },
        },
      ],
    }),
  );
}
