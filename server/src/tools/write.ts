import type { z } from 'zod';
import { LIMITS } from '../limits.js';
import {
  adjustPointsPath,
  cloneCampaignPath,
  collectionPath,
  createPath,
  deletePath,
  editPath,
  membershipPath,
  notePath,
  sendEmailPath,
} from '../mautic/paths.js';
import { entitiesOf, summarizeEntity, summarizePayload } from '../mautic/present.js';
import {
  adjustPointsSchema,
  cloneSchema,
  createSchema,
  idSchema,
  membershipSchema,
  noteSchema,
  sendSchema,
  updateSchema,
  upsertSchema,
} from '../mautic/schema.js';
import { buildCreate, buildUpdate, contactBody } from '../mautic/write-model.js';
import type { ToolContext } from './context.js';
import { fail, ok, type ToolResult } from './result.js';
import { runTool } from './run.js';

export async function upsertContact(ctx: ToolContext, args: z.infer<typeof upsertSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_upsert_contact', resource: 'contacts' }, async () => {
    const found = await ctx.gateway.get(collectionPath('contacts'), {
      search: `email:${args.email}`,
      limit: 1,
    });
    const page = entitiesOf(found, ['contacts']);
    const match = page.items.find((item) => String(item.email ?? '').toLowerCase() === args.email.toLowerCase());
    if (page.total > 1 || (page.items.length > 0 && !match)) {
      return fail('Search did not find a single contact with that email. Use mautic_update with the id.');
    }
    const body = contactBody(args);
    if (!body.ok) return fail(body.message);
    if (match) {
      const id = Number(match.id);
      if (!Number.isInteger(id) || id <= 0) return fail('Contact has no id');
      const mutable = Object.keys(body.value).filter((key) => key !== 'email');
      if (mutable.length === 0) return ok({ updated: false, contact: summarizeEntity('contacts', match, 'detail') });
      const updated = await ctx.gateway.send('PATCH', editPath('contacts', id), body.value);
      return ok({ updated: true, contact: summarizePayload('contacts', updated) });
    }
    const created = await ctx.gateway.send('POST', createPath('contacts'), body.value);
    return ok({ created: true, contact: summarizePayload('contacts', created) });
  });
}

export async function createResource(ctx: ToolContext, args: z.infer<typeof createSchema>): Promise<ToolResult> {
  const { resource, ...fields } = args;
  return runTool(ctx.log, { tool: 'mautic_create', resource }, async () => {
    const built = buildCreate(resource, fields);
    if (!built.ok) return fail(built.message);
    const payload = await ctx.gateway.send(built.value.method, built.value.path, built.value.body);
    return ok({ created: true, [resource]: summarizePayload(resource, payload) });
  });
}

export async function updateResource(ctx: ToolContext, args: z.infer<typeof updateSchema>): Promise<ToolResult> {
  const { resource, id, ...fields } = args;
  return runTool(ctx.log, { tool: 'mautic_update', resource, id }, async () => {
    const built = buildUpdate(resource, id, fields);
    if (!built.ok) return fail(built.message);
    const payload = await ctx.gateway.send(built.value.method, built.value.path, built.value.body);
    return ok({ updated: true, [resource]: summarizePayload(resource, payload) });
  });
}

export async function membership(ctx: ToolContext, args: z.infer<typeof membershipSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_membership', resource: args.target, id: args.targetId }, async () => {
    await ctx.gateway.send('POST', membershipPath(args.target, args.action, args.targetId, args.contactId));
    return ok({
      target: args.target,
      action: args.action,
      targetId: args.targetId,
      contactId: args.contactId,
      success: true,
    });
  });
}

export async function adjustPoints(ctx: ToolContext, args: z.infer<typeof adjustPointsSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_adjust_points', resource: 'contacts', id: args.contactId }, async () => {
    const payload = await ctx.gateway.send(
      'POST',
      adjustPointsPath(args.contactId, args.operator, args.delta, args.groupId),
    );
    return ok({ contactId: args.contactId, operator: args.operator, delta: args.delta, groupId: args.groupId ?? null, result: payload });
  });
}

export async function addNote(ctx: ToolContext, args: z.infer<typeof noteSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_add_note', resource: 'contacts', id: args.contactId }, async () => {
    await ctx.gateway.send('POST', notePath(args.contactId), {
      text: args.text,
      type: args.type ?? 'general',
    });
    return ok({ contactId: args.contactId, noted: true });
  });
}

export async function cloneCampaign(ctx: ToolContext, args: z.infer<typeof cloneSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_clone_campaign', resource: 'campaigns', id: args.campaignId }, async () => {
    const payload = await ctx.gateway.send('POST', cloneCampaignPath(args.campaignId));
    return ok({
      cloned: true,
      campaign: summarizePayload('campaigns', payload),
      warning: 'The copy keeps isPublished. Unpublish it with mautic_update if it should not be live.',
    });
  });
}

export async function removeResource(ctx: ToolContext, args: z.infer<typeof idSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_delete', resource: args.resource, id: args.id }, async () => {
    await ctx.gateway.send('DELETE', deletePath(args.resource, args.id));
    return ok({ resource: args.resource, id: args.id, deleted: true });
  });
}

export async function sendEmail(ctx: ToolContext, args: z.infer<typeof sendSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_send_email', resource: 'emails', id: args.emailId }, async () => {
    const tokens = args.tokens ?? {};
    const keys = Object.keys(tokens);
    if (keys.length > LIMITS.tokenCount) return fail(`At most ${LIMITS.tokenCount} tokens`);
    const body = keys.length > 0 ? { tokens } : undefined;
    const payload = await ctx.gateway.send('POST', sendEmailPath(args.emailId, args.contactId), body);
    const success = !isFailure(payload);
    const result = ok({ emailId: args.emailId, contactId: args.contactId, success });
    return success ? result : { ...result, isError: true };
  });
}

function isFailure(payload: unknown): boolean {
  return typeof payload === 'object' && payload !== null && 'success' in payload && payload.success === false;
}
