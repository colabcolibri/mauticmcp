import { isRecord } from '../guards.js';
import { LIMITS } from '../limits.js';
import { resourceSpec, type ResourceName } from './catalog.js';

const SECRET = /password|secret|token|credential/i;
const CONTACT_SKIP = new Set([
  'id',
  'email',
  'firstname',
  'lastname',
  'points',
  'phone',
  'company',
  'tags',
  'owner',
  'stage',
  'fields',
  'ipAddresses',
  'doNotContact',
  'notes',
  'color',
  'lastActive',
  'dateIdentified',
  'dateModified',
  'dateAdded',
  'createdBy',
  'createdByUser',
  'modifiedBy',
  'modifiedByUser',
]);

export interface EntityPage {
  total: number;
  items: Record<string, unknown>[];
}

export function entitiesOf(payload: unknown, keys: string[]): EntityPage {
  if (!isRecord(payload)) return { total: 0, items: [] };
  let raw: unknown;
  for (const key of keys) {
    if (key in payload) {
      raw = payload[key];
      break;
    }
  }
  const items = asRecords(raw);
  const totalRaw = payload.total;
  const parsed = typeof totalRaw === 'number' ? totalRaw : typeof totalRaw === 'string' ? Number(totalRaw) : items.length;
  return { total: Number.isFinite(parsed) ? parsed : items.length, items };
}

export function summarizeCollection(resource: ResourceName, payload: unknown) {
  const spec = resourceSpec(resource);
  const page = entitiesOf(payload, spec.collectionKeys);
  return {
    resource,
    total: page.total,
    items: page.items.slice(0, LIMITS.searchMax).map((item) => summarizeEntity(resource, item, 'list')),
  };
}

export function summarizePayload(resource: ResourceName, payload: unknown) {
  if (resource === 'reports' && isRecord(payload) && Array.isArray(payload.data)) {
    const rows = payload.data.filter(isRecord).slice(0, LIMITS.searchMax).map((row) => primitives(row));
    return {
      totalResults: typeof payload.totalResults === 'number' ? payload.totalResults : rows.length,
      dataColumns: payload.dataColumns ?? null,
      rows,
      report: isRecord(payload.report) ? summarizeEntity('reports', payload.report, 'detail') : undefined,
    };
  }
  const spec = resourceSpec(resource);
  return summarizeEntity(resource, pickEntity(payload, spec.itemKeys), 'detail');
}

export function summarizeEntity(
  resource: ResourceName,
  entity: Record<string, unknown>,
  mode: 'list' | 'detail',
): Record<string, unknown> {
  const spec = resourceSpec(resource);
  const fields = mode === 'list' ? spec.listFields : spec.detailFields;
  const out: Record<string, unknown> = {};
  for (const field of fields) {
    if (!(field in entity) || SECRET.test(field)) continue;
    const compact = compactField(field, entity[field], mode);
    if (compact !== undefined) out[field] = compact;
  }
  if (
    mode === 'detail' &&
    typeof entity.customHtml === 'string' &&
    entity.customHtml.length > LIMITS.htmlMax &&
    'customHtml' in out
  ) {
    out.customHtmlTruncated = true;
  }
  if (resource === 'contacts' && mode === 'detail') {
    const custom = contactPrimitives(entity);
    if (Object.keys(custom).length > 0) out.custom = custom;
  }
  return out;
}

export function summarizeRows(payload: unknown, keys: string[], limit: number) {
  const page = entitiesOf(payload, keys);
  return {
    total: page.total,
    items: page.items.slice(0, limit).map((item) => primitives(item)),
  };
}

function primitives(entity: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(entity)) {
    if (SECRET.test(key)) continue;
    if (typeof value === 'string') out[key] = value.slice(0, 300);
    else if (typeof value === 'number' || typeof value === 'boolean' || value === null) out[key] = value;
    if (Object.keys(out).length >= 12) break;
  }
  return out;
}

export function pickEntity(payload: unknown, keys: string[]): Record<string, unknown> {
  if (!isRecord(payload)) throw new Error('Empty Mautic response');
  for (const key of keys) {
    const value = payload[key];
    if (isRecord(value)) return value;
  }
  if ('id' in payload) return payload;
  throw new Error('Mautic response has no entity');
}

function compactField(field: string, value: unknown, mode: 'list' | 'detail'): unknown {
  if (field === 'customHtml' && typeof value === 'string') {
    if (mode === 'list') return undefined;
    if (value.length <= LIMITS.htmlMax) return value;
    return value.slice(0, LIMITS.htmlMax);
  }
  if (field === 'plainText' && typeof value === 'string') {
    return value.length <= LIMITS.plainTextMax ? value : value.slice(0, LIMITS.plainTextMax);
  }
  if (field === 'columns' && Array.isArray(value)) {
    return value.slice(0, 40).filter((item) => typeof item === 'string');
  }
  if (field === 'properties' && isRecord(value)) {
    const text = JSON.stringify(value);
    return text.length <= 4_000 ? value : { truncated: true };
  }
  if (field === 'tags') return compactTags(value);
  if (field === 'events') return asRecords(value).slice(0, LIMITS.eventsMax).map(compactEvent).filter(isRecord);
  if (field === 'filters') return asRecords(value).slice(0, 30).map(compactFilter).filter(isRecord);
  if (field === 'fields') return asRecords(value).slice(0, 40).map(compactFormField).filter(isRecord);
  if (field === 'lists' || field === 'forms' || field === 'category' || field === 'owner' || field === 'stage') {
    return compactRelation(value);
  }
  if (typeof value === 'string') return value.length > 500 ? value.slice(0, 500) : value;
  if (typeof value === 'number' || typeof value === 'boolean' || value === null) return value;
  return undefined;
}

function compactEvent(value: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const key of ['id', 'name', 'type', 'eventType', 'order', 'triggerMode']) {
    const field = value[key];
    if (typeof field === 'string' || typeof field === 'number') out[key] = field;
  }
  if (isRecord(value.properties)) {
    const props: Record<string, string | number | boolean> = {};
    for (const [key, prop] of Object.entries(value.properties)) {
      if (typeof prop === 'string' || typeof prop === 'number' || typeof prop === 'boolean') props[key] = prop;
    }
    out.properties = props;
  }
  return out;
}

function compactFilter(value: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const key of ['glue', 'field', 'object', 'type', 'operator']) {
    if (typeof value[key] === 'string') out[key] = value[key];
  }
  if (isRecord(value.properties) && (typeof value.properties.filter === 'string' || typeof value.properties.filter === 'number')) {
    out.filter = value.properties.filter;
  }
  return out;
}

function compactFormField(value: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const key of ['id', 'label', 'alias', 'type']) {
    if (typeof value[key] === 'string' || typeof value[key] === 'number') out[key] = value[key];
  }
  return out;
}

function compactRelation(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.slice(0, 20).map(compactRelation).filter((item) => item !== undefined);
  }
  if (!isRecord(value) || value.id === undefined) return undefined;
  const label = value.name ?? value.title ?? value.email ?? value.username;
  return label === undefined ? { id: value.id } : { id: value.id, name: label };
}

function compactTags(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  const tags: string[] = [];
  for (const item of value) {
    if (typeof item === 'string') tags.push(item);
    else if (isRecord(item) && typeof item.tag === 'string') tags.push(item.tag);
    if (tags.length >= 30) break;
  }
  return tags;
}

function contactPrimitives(entity: Record<string, unknown>): Record<string, string | number | boolean> {
  const out: Record<string, string | number | boolean> = {};
  for (const [key, value] of Object.entries(entity)) {
    if (CONTACT_SKIP.has(key) || SECRET.test(key)) continue;
    if (typeof value === 'string') out[key] = value.slice(0, 300);
    else if (typeof value === 'number' || typeof value === 'boolean') out[key] = value;
    if (Object.keys(out).length >= 20) break;
  }
  return out;
}

function asRecords(value: unknown): Record<string, unknown>[] {
  if (Array.isArray(value)) return value.filter(isRecord);
  if (isRecord(value)) return Object.values(value).filter(isRecord);
  return [];
}
