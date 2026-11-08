import type { JsonObject, JsonValue } from '../json.js';
import { LIMITS } from '../limits.js';
import type { CreatableName, ResourceName } from './catalog.js';
import { createPath, editPath } from './paths.js';
import type { WriteFields } from './schema.js';

export interface ApiCall {
  method: 'POST' | 'PATCH' | 'PUT';
  path: string;
  body: Record<string, unknown>;
}

export type DomainResult<T> = { ok: true; value: T } | { ok: false; message: string };

const SECRET_KEY = /password|secret|token|credential|authorization/i;
const KEY_NAME = /^[A-Za-z][A-Za-z0-9_]*$/;

const PUBLISHED_ON_CREATE: Partial<Record<ResourceName, 0 | 1>> = {
  campaigns: 0,
  emails: 0,
  forms: 0,
  pages: 0,
  segments: 1,
  categories: 1,
  companies: 1,
  assets: 0,
  focus: 0,
  points: 0,
  pointTriggers: 0,
  stages: 1,
};

export function buildCreate(resource: CreatableName, input: WriteFields): DomainResult<ApiCall> {
  const built = buildBody(resource, input, true);
  if (!built.ok) return built;
  return { ok: true, value: { method: 'POST', path: createPath(resource), body: built.value } };
}

export function buildUpdate(resource: ResourceName, id: number, input: WriteFields): DomainResult<ApiCall> {
  if (resource === 'campaigns' && (input.events !== undefined || input.canvasSettings !== undefined)) {
    if (input.name === undefined || input.name.trim() === '') {
      return { ok: false, message: 'Replacing events requires name. PUT replaces the whole canvas.' };
    }
    const built = buildCampaign(input, undefined);
    if (!built.ok) return built;
    return { ok: true, value: { method: 'PUT', path: editPath(resource, id), body: built.value } };
  }
  const built = buildBody(resource, input, false);
  if (!built.ok) return built;
  if (Object.keys(built.value).length === 0) {
    return { ok: false, message: 'Provide at least one field to change' };
  }
  return { ok: true, value: { method: 'PATCH', path: editPath(resource, id), body: built.value } };
}

export function contactBody(input: WriteFields): DomainResult<Record<string, unknown>> {
  return finish(input, {
    email: input.email,
    firstname: input.firstname,
    lastname: input.lastname,
    phone: input.phone,
    company: input.company,
    position: input.position,
    tags: input.tags,
  });
}

function buildBody(resource: ResourceName, input: WriteFields, creating: boolean): DomainResult<Record<string, unknown>> {
  const published = publishedBit(input.isPublished, creating ? PUBLISHED_ON_CREATE[resource] : undefined);
  switch (resource) {
    case 'campaigns':
      if (!creating && (input.lists?.length === 0 || input.forms?.length === 0)) {
        return { ok: false, message: 'lists and forms cannot be empty. Omit the field to keep the current source.' };
      }
      return creating ? buildCampaign(input, published) : finish(input, campaignPatch(input, published));
    case 'emails':
      return buildEmail(input, published, creating);
    case 'segments':
      return buildSegment(input, published, creating);
    case 'forms':
      return buildNamed(input, 'name', creating, {
        name: input.name,
        description: input.description,
        isPublished: published,
        formType: input.formType,
        fields: input.fields,
      });
    case 'companies':
      return buildCompany(input, published, creating);
    case 'categories':
      return buildCategory(input, published, creating);
    case 'pages':
      return buildNamed(input, 'title', creating, {
        title: input.title ?? input.name,
        alias: input.alias,
        description: input.description,
        isPublished: published,
        template: input.template,
        metaDescription: input.metaDescription,
        customHtml: input.customHtml,
      });
    case 'assets':
      return buildAsset(input, published, creating);
    case 'focus':
      return buildFocus(input, published, creating);
    case 'points':
      return buildPointAction(input, published, creating);
    case 'pointTriggers':
      return buildPointTrigger(input, published, creating);
    case 'pointGroups':
      return buildNamed(input, 'name', creating, {
        name: input.name,
        description: input.description,
      });
    case 'tags':
      return buildTag(input, creating);
    case 'reports':
      return buildReport(input, creating);
    case 'stages':
      return buildNamed(input, 'name', creating, {
        name: input.name,
        description: input.description,
        weight: input.weight,
        isPublished: published,
        category: input.categoryId === undefined ? undefined : { id: input.categoryId },
      });
    case 'contacts':
      return contactBody(input);
    default:
      return { ok: false, message: 'This resource cannot be written' };
  }
}

function buildCampaign(input: WriteFields, published: 0 | 1 | undefined): DomainResult<Record<string, unknown>> {
  if (input.name === undefined || input.name.trim() === '') {
    return { ok: false, message: 'A campaign requires name.' };
  }
  if (!input.events || input.events.length === 0) {
    return { ok: false, message: 'A campaign requires events with id, name and type, plus lists or forms.' };
  }
  const events = normalizeEvents(input.events);
  if (!events.ok) return events;
  const lists = input.lists ? idObjects(input.lists, 'lists') : undefined;
  if (lists && !lists.ok) return lists;
  const forms = input.forms ? idObjects(input.forms, 'forms') : undefined;
  if (forms && !forms.ok) return forms;
  if ((!lists || lists.value.length === 0) && (!forms || forms.value.length === 0)) {
    return { ok: false, message: 'A campaign requires lists or forms as the contact source.' };
  }
  const canvas = input.canvasSettings ?? linearCanvas(events.value, lists && lists.value.length > 0 ? 'lists' : 'forms');
  return finish(input, {
    name: input.name,
    description: input.description,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
    events: events.value,
    lists: lists?.value,
    forms: forms?.value,
    canvasSettings: canvas,
  });
}

function campaignPatch(input: WriteFields, published: 0 | 1 | undefined): Record<string, unknown> {
  const lists = input.lists ? input.lists.map((item) => ({ id: item })) : undefined;
  const forms = input.forms ? input.forms.map((item) => ({ id: item })) : undefined;
  return {
    name: input.name,
    description: input.description,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
    lists,
    forms,
  };
}

function buildEmail(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  const emailType = input.emailType ?? (creating ? 'template' : undefined);
  if (emailType === 'list' && (!input.lists || input.lists.length === 0)) {
    return { ok: false, message: 'A segment email (emailType list) requires lists with segment ids.' };
  }
  if (creating && (input.name === undefined || input.subject === undefined)) {
    return { ok: false, message: 'An email requires name and subject.' };
  }
  return finish(input, {
    name: input.name,
    subject: input.subject,
    emailType,
    isPublished: published,
    customHtml: input.customHtml,
    plainText: input.plainText,
    fromAddress: input.fromAddress,
    fromName: input.fromName,
    replyToAddress: input.replyToAddress,
    template: input.template,
    lists: input.lists,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
  });
}

function buildSegment(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  if (creating && input.name === undefined) return { ok: false, message: 'A segment requires name.' };
  return finish(input, {
    name: input.name,
    alias: input.alias,
    description: input.description,
    isPublished: published,
    filters: input.filters,
  });
}

function buildCompany(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  const companyname = input.companyname ?? input.name;
  if (creating && companyname === undefined) return { ok: false, message: 'A company requires companyname (or name).' };
  return finish(input, {
    companyname,
    companyemail: input.companyemail,
    companyphone: input.companyphone,
    companywebsite: input.companywebsite,
    companycity: input.companycity,
    isPublished: published,
  });
}

function buildCategory(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  const title = input.title ?? input.name;
  if (creating && title === undefined) return { ok: false, message: 'A category requires title.' };
  if (creating && input.bundle === undefined) {
    return { ok: false, message: 'A category requires bundle, for example campaign, email, form or page.' };
  }
  return finish(input, {
    title,
    alias: input.alias,
    bundle: input.bundle,
    description: input.description,
    isPublished: published,
  });
}

function buildNamed(
  input: WriteFields,
  label: 'name' | 'title',
  creating: boolean,
  body: Record<string, unknown>,
): DomainResult<Record<string, unknown>> {
  const value = label === 'title' ? (input.title ?? input.name) : input.name;
  if (creating && value === undefined) return { ok: false, message: `This resource requires ${label}.` };
  return finish(input, body);
}

function buildAsset(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  const title = input.title ?? input.name;
  if (creating && title === undefined) return { ok: false, message: 'An asset requires title.' };
  const storageLocation = input.storageLocation ?? (creating ? 'remote' : undefined);
  if (creating && storageLocation === 'remote' && (input.remotePath === undefined || input.remotePath.trim() === '')) {
    return { ok: false, message: 'A remote asset requires remotePath with the file URL. Local file upload is not available.' };
  }
  if (storageLocation === 'local') {
    return { ok: false, message: 'Local file upload is not available. Use storageLocation remote and remotePath.' };
  }
  return finish(input, {
    title,
    alias: input.alias,
    description: input.description,
    storageLocation,
    remotePath: input.remotePath,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
  });
}

function buildFocus(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  if (creating && input.name === undefined) return { ok: false, message: 'A focus item requires name.' };
  if (creating && input.type === undefined) {
    return { ok: false, message: 'A focus item requires type: notice, form or link.' };
  }
  return finish(input, {
    name: input.name,
    type: input.type,
    style: input.style,
    website: input.website,
    description: input.description,
    properties: input.properties,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
  });
}

function buildPointAction(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  if (creating && input.name === undefined) return { ok: false, message: 'A point action requires name.' };
  if (creating && input.type === undefined) {
    return { ok: false, message: 'A point action requires type. Call mautic_point_types.' };
  }
  if (creating && input.delta === undefined) return { ok: false, message: 'A point action requires delta.' };
  return finish(input, {
    name: input.name,
    type: input.type,
    delta: input.delta,
    description: input.description,
    properties: input.properties,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
    group: input.groupId,
  });
}

function buildPointTrigger(
  input: WriteFields,
  published: 0 | 1 | undefined,
  creating: boolean,
): DomainResult<Record<string, unknown>> {
  if (creating && input.name === undefined) return { ok: false, message: 'A point trigger requires name.' };
  if (creating && input.points === undefined) return { ok: false, message: 'A point trigger requires points, the threshold that fires it.' };
  return finish(input, {
    name: input.name,
    description: input.description,
    points: input.points,
    color: input.color,
    events: input.events,
    isPublished: published,
    category: input.categoryId === undefined ? undefined : { id: input.categoryId },
    group: input.groupId,
  });
}

function buildTag(input: WriteFields, creating: boolean): DomainResult<Record<string, unknown>> {
  const tag = input.tag ?? input.name;
  if (creating && tag === undefined) return { ok: false, message: 'A tag requires tag (or name).' };
  return finish(input, { tag, description: input.description });
}

function buildReport(input: WriteFields, creating: boolean): DomainResult<Record<string, unknown>> {
  if (creating && input.name === undefined) return { ok: false, message: 'A report requires name.' };
  if (creating && input.source === undefined) {
    return { ok: false, message: 'A report requires source, for example leads or email.stats.' };
  }
  return finish(input, {
    name: input.name,
    source: input.source,
    description: input.description,
    columns: input.columns,
    filters: input.filters,
  });
}

function finish(input: WriteFields, body: Record<string, unknown>): DomainResult<Record<string, unknown>> {
  if (input.projects !== undefined && input.projects.length > 0) body.projects = input.projects;
  const cleaned = dropUndefined(body);
  return mergeExtra(cleaned, input.extra);
}

function normalizeEvents(events: JsonObject[]): DomainResult<JsonObject[]> {
  if (events.length > LIMITS.eventsMax) return { ok: false, message: 'events exceeds the limit' };
  const normalized: JsonObject[] = [];
  for (let index = 0; index < events.length; index += 1) {
    const event = events[index];
    if (!event) return { ok: false, message: 'Missing event' };
    const idValue = event.id;
    if ((typeof idValue !== 'string' && typeof idValue !== 'number') || typeof event.name !== 'string' || typeof event.type !== 'string') {
      return { ok: false, message: `Event ${index} requires id, name and type` };
    }
    const next: JsonObject = { ...event };
    if (next.eventType === undefined) next.eventType = 'action';
    if (next.order === undefined) next.order = index + 1;
    if (next.parent === undefined) {
      const previous = events[index - 1];
      next.parent = index === 0 || !previous ? null : String(previous.id);
    }
    normalized.push(next);
  }
  return { ok: true, value: normalized };
}

function linearCanvas(events: JsonObject[], source: 'lists' | 'forms'): JsonObject {
  const nodes: JsonValue[] = events.map((event, index) => ({
    id: String(event.id),
    positionX: 520,
    positionY: 80 + index * 140,
  }));
  const connections: JsonValue[] = [];
  const first = events[0];
  if (first) {
    connections.push({
      sourceId: source,
      targetId: String(first.id),
      anchors: { source: 'leadsource', target: 'top' },
    });
  }
  for (let index = 0; index < events.length - 1; index += 1) {
    const current = events[index];
    const next = events[index + 1];
    if (!current || !next) continue;
    connections.push({
      sourceId: String(current.id),
      targetId: String(next.id),
      anchors: { source: 'bottom', target: 'top' },
    });
  }
  return { nodes, connections };
}

function idObjects(ids: number[], label: string): DomainResult<JsonObject[]> {
  if (ids.length > LIMITS.idsMax) return { ok: false, message: `${label} exceeds the limit` };
  const value: JsonObject[] = [];
  for (const item of ids) {
    if (!Number.isInteger(item) || item <= 0) return { ok: false, message: `${label} contains an invalid id` };
    value.push({ id: item });
  }
  return { ok: true, value };
}

function publishedBit(value: boolean | undefined, fallback: 0 | 1 | undefined): 0 | 1 | undefined {
  if (value === undefined) return fallback;
  return value ? 1 : 0;
}

function dropUndefined(body: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(body)) {
    if (value !== undefined) out[key] = value;
  }
  return out;
}

function mergeExtra(
  body: Record<string, unknown>,
  extra: Record<string, JsonValue> | undefined,
): DomainResult<Record<string, unknown>> {
  if (!extra) return { ok: true, value: body };
  const encoded = JSON.stringify(extra);
  if (encoded.length > LIMITS.extraMaxChars) return { ok: false, message: 'extra is too large' };
  const keys = Object.keys(extra);
  if (keys.length > 40) return { ok: false, message: 'extra has too many fields' };
  for (const key of keys) {
    if (!KEY_NAME.test(key)) return { ok: false, message: `Invalid extra field: ${key}` };
    if (SECRET_KEY.test(key)) return { ok: false, message: `Blocked field: ${key}` };
    if (key in body || key === 'id') return { ok: false, message: `Use the dedicated field, not extra.${key}` };
    body[key] = extra[key];
  }
  return { ok: true, value: body };
}
