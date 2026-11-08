import { z } from 'zod';
import { jsonValue, type JsonObject } from '../json.js';
import { CREATABLE, RESOURCE_NAMES } from './catalog.js';

const id = z.number().int().positive();
const ids = z.array(id).max(50);

export const writeFieldsSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  title: z.string().min(1).max(255).optional(),
  alias: z.string().min(1).max(255).optional(),
  description: z.string().max(5_000).optional(),
  subject: z.string().min(1).max(255).optional(),
  email: z.string().email().max(255).optional(),
  firstname: z.string().max(255).optional(),
  lastname: z.string().max(255).optional(),
  phone: z.string().max(50).optional(),
  company: z.string().max(255).optional(),
  position: z.string().max(255).optional(),
  tags: z.array(z.string().min(1).max(50)).max(30).optional(),
  companyname: z.string().min(1).max(255).optional(),
  companyemail: z.string().email().max(255).optional(),
  companyphone: z.string().max(50).optional(),
  companywebsite: z.string().max(255).optional(),
  companycity: z.string().max(255).optional(),
  bundle: z.string().min(1).max(40).optional(),
  formType: z.string().min(1).max(40).optional(),
  template: z.string().max(255).optional(),
  metaDescription: z.string().max(500).optional(),
  fromAddress: z.string().email().max(255).optional(),
  fromName: z.string().max(255).optional(),
  replyToAddress: z.string().email().max(255).optional(),
  plainText: z.string().max(100_000).optional(),
  customHtml: z.string().max(200_000).optional(),
  emailType: z.enum(['template', 'list']).optional(),
  isPublished: z.boolean().optional(),
  categoryId: id.optional(),
  projects: ids.optional().describe('Project ids to link when the entity accepts them'),
  type: z.string().min(1).max(80).optional().describe('Focus type (notice, form, link) or point action type (email.open, form.submit, page.hit)'),
  style: z.string().min(1).max(40).optional().describe('Focus style: bar, modal, notification or page'),
  website: z.string().max(500).optional(),
  properties: z.record(z.string(), jsonValue).optional(),
  weight: z.number().int().min(0).max(1_000_000).optional().describe('Stage weight'),
  delta: z.number().int().min(-1_000_000).max(1_000_000).optional().describe('Points for the action. Negative removes points'),
  points: z.number().int().min(0).max(1_000_000).optional().describe('Point trigger threshold'),
  color: z.string().max(20).optional(),
  storageLocation: z.enum(['local', 'remote']).optional(),
  remotePath: z.string().max(2_000).optional().describe('Remote asset URL'),
  groupId: id.optional().describe('Point group id for a point action, or for mautic_adjust_points'),
  tag: z.string().min(1).max(255).optional().describe('Tag label. Mautic stores it in the tag field'),
  source: z.string().min(1).max(80).optional().describe('Report source, for example leads or email.stats'),
  columns: z.array(z.string().min(1).max(120)).max(40).optional().describe('Report column aliases'),
  lists: ids.optional(),
  forms: ids.optional(),
  events: z.array(z.record(z.string(), jsonValue)).max(40).optional(),
  canvasSettings: z.record(z.string(), jsonValue).optional(),
  filters: z.array(z.record(z.string(), jsonValue)).max(30).optional(),
  fields: z.array(z.record(z.string(), jsonValue)).max(40).optional(),
  extra: z.record(z.string(), jsonValue).optional(),
});

export type WriteFields = z.infer<typeof writeFieldsSchema>;

export const searchSchema = z.object({
  resource: z.enum(RESOURCE_NAMES).describe('Mautic resource name'),
  search: z.string().max(200).optional().describe('Mautic search filter. Example: email:ana@example.com or is:published'),
  limit: z.number().int().min(1).max(25).optional().describe('Page size, max 25'),
  start: z.number().int().min(0).max(10_000).optional().describe('Page offset'),
  orderBy: z.string().regex(/^[A-Za-z0-9_.]+$/).max(64).optional(),
  orderByDir: z.enum(['ASC', 'DESC']).optional(),
  publishedOnly: z.boolean().optional().describe('When true, appends is:published to the search'),
});

export const idSchema = z.object({
  resource: z.enum(RESOURCE_NAMES),
  id: id,
});

export const contactIdSchema = z.object({
  contactId: id,
  limit: z.number().int().min(1).max(50).optional(),
});

export const campaignContactsSchema = z.object({
  campaignId: id,
  limit: z.number().int().min(1).max(25).optional(),
  start: z.number().int().min(0).max(10_000).optional(),
});

export const upsertSchema = writeFieldsSchema
  .pick({
    email: true,
    firstname: true,
    lastname: true,
    phone: true,
    company: true,
    position: true,
    tags: true,
    extra: true,
  })
  .required({ email: true });

export const createSchema = writeFieldsSchema.extend({
  resource: z.enum(CREATABLE).describe('Resource to create. Contacts use mautic_upsert_contact. Includes tags and reports'),
});

export const updateSchema = writeFieldsSchema.extend({
  resource: z.enum(RESOURCE_NAMES),
  id: id,
});

export const membershipSchema = z.object({
  target: z.enum(['segment', 'campaign', 'stage']),
  action: z.enum(['add', 'remove']),
  targetId: id.describe('Segment, campaign or stage id'),
  contactId: id,
});

export const noteSchema = z.object({
  contactId: id,
  text: z.string().min(1).max(5_000),
  type: z.string().min(1).max(50).optional().describe('Mautic note type. Default general'),
});

export const cloneSchema = z.object({
  campaignId: id,
});

export const adjustPointsSchema = z.object({
  contactId: id,
  operator: z.enum(['plus', 'minus', 'times', 'divide']),
  delta: z.number().int().positive().max(1_000_000),
  groupId: id.optional().describe('When set, adjusts that point group balance'),
});

export const sendSchema = z.object({
  emailId: id,
  contactId: id,
  tokens: z.record(z.string().max(80), z.string().max(2_000)).optional().describe('Email {token} values. At most 20'),
});

export type CampaignEvent = JsonObject;
