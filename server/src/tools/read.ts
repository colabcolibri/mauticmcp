import type { z } from 'zod';
import { LIMITS } from '../limits.js';
import { activityPath, campaignContactsPath, collectionPath, itemPath, POINT_ACTION_TYPES_PATH, POINT_TRIGGER_EVENT_TYPES_PATH } from '../mautic/paths.js';
import { summarizeCollection, summarizePayload, summarizeRows } from '../mautic/present.js';
import type { Query } from '../mautic/client.js';
import { campaignContactsSchema, contactIdSchema, idSchema, searchSchema } from '../mautic/schema.js';
import { describePolicy } from '../policy.js';
import type { ToolContext } from './context.js';
import { ok, type ToolResult } from './result.js';
import { runTool } from './run.js';

export async function capabilities(ctx: ToolContext): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_capabilities' }, async () => ok(describePolicy(ctx.policy)));
}

export async function search(ctx: ToolContext, args: z.infer<typeof searchSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_search', resource: args.resource }, async () => {
    const query: Query = { limit: Math.min(args.limit ?? LIMITS.searchDefault, LIMITS.searchMax) };
    if (args.start !== undefined) query.start = args.start;
    if (args.orderBy !== undefined) query.orderBy = args.orderBy;
    if (args.orderByDir !== undefined) query.orderByDir = args.orderByDir;
    const searchText = [args.search, args.publishedOnly ? 'is:published' : undefined].filter(Boolean).join(' ');
    if (searchText) query.search = searchText;
    const payload = await ctx.gateway.get(collectionPath(args.resource), query);
    return ok(summarizeCollection(args.resource, payload));
  });
}

export async function getOne(ctx: ToolContext, args: z.infer<typeof idSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_get', resource: args.resource, id: args.id }, async () => {
    const payload = await ctx.gateway.get(itemPath(args.resource, args.id));
    return ok(summarizePayload(args.resource, payload));
  });
}

export async function contactActivity(ctx: ToolContext, args: z.infer<typeof contactIdSchema>): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_contact_activity', resource: 'contacts', id: args.contactId }, async () => {
    const limit = Math.min(args.limit ?? 20, LIMITS.activityMax);
    const payload = await ctx.gateway.get(activityPath(args.contactId), { limit });
    const rows = summarizeRows(payload, ['events', 'activity'], limit);
    return ok({ contactId: args.contactId, ...rows });
  });
}

export async function campaignContacts(
  ctx: ToolContext,
  args: z.infer<typeof campaignContactsSchema>,
): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_campaign_contacts', resource: 'campaigns', id: args.campaignId }, async () => {
    const limit = Math.min(args.limit ?? LIMITS.searchDefault, LIMITS.searchMax);
    const query: Query = { limit };
    if (args.start !== undefined) query.start = args.start;
    const payload = await ctx.gateway.get(campaignContactsPath(args.campaignId), query);
    return ok({ campaignId: args.campaignId, ...summarizeRows(payload, ['contacts'], limit) });
  });
}

export async function pointTypes(ctx: ToolContext): Promise<ToolResult> {
  return runTool(ctx.log, { tool: 'mautic_point_types', resource: 'points' }, async () => {
    const actions = await ctx.gateway.get(POINT_ACTION_TYPES_PATH);
    const events = await ctx.gateway.get(POINT_TRIGGER_EVENT_TYPES_PATH);
    return ok({ pointActionTypes: recordOf(actions, 'pointActionTypes'), eventTypes: recordOf(events, 'eventTypes') });
  });
}

function recordOf(payload: unknown, key: string): Record<string, unknown> {
  if (typeof payload !== 'object' || payload === null || !(key in payload)) return {};
  const value = (payload as Record<string, unknown>)[key];
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}
