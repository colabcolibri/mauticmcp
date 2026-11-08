import { entityId } from '../guards.js';
import { resourceSpec, type ResourceName } from './catalog.js';

function idPath(slug: string, id: number, suffix: string): string {
  return `/api/${slug}/${entityId(id)}${suffix}`;
}

export function collectionPath(resource: ResourceName): string {
  return `/api/${resourceSpec(resource).slug}`;
}

export function itemPath(resource: ResourceName, id: number): string {
  return idPath(resourceSpec(resource).slug, id, '');
}

export function createPath(resource: ResourceName): string {
  return `/api/${resourceSpec(resource).slug}/new`;
}

export function editPath(resource: ResourceName, id: number): string {
  return idPath(resourceSpec(resource).slug, id, '/edit');
}

export function deletePath(resource: ResourceName, id: number): string {
  return idPath(resourceSpec(resource).slug, id, '/delete');
}

export function activityPath(contactId: number): string {
  return idPath('contacts', contactId, '/activity');
}

export function notePath(contactId: number): string {
  return idPath('contacts', contactId, '/notes/new');
}

export function campaignContactsPath(campaignId: number): string {
  return idPath('campaigns', campaignId, '/contacts');
}

export function cloneCampaignPath(campaignId: number): string {
  return `/api/campaigns/clone/${entityId(campaignId)}`;
}

const MEMBERSHIP_SLUG = {
  segment: 'segments',
  campaign: 'campaigns',
  stage: 'stages',
} as const;

export function membershipPath(
  target: keyof typeof MEMBERSHIP_SLUG,
  action: 'add' | 'remove',
  targetId: number,
  contactId: number,
): string {
  return `/api/${MEMBERSHIP_SLUG[target]}/${entityId(targetId)}/contact/${entityId(contactId)}/${action}`;
}

export function adjustPointsPath(
  contactId: number,
  operator: 'plus' | 'minus' | 'times' | 'divide',
  delta: number,
  groupId?: number,
): string {
  if (groupId === undefined) {
    return `/api/contacts/${entityId(contactId)}/points/${operator}/${entityId(delta)}`;
  }
  return `/api/contacts/${entityId(contactId)}/points/groups/${entityId(groupId)}/${operator}/${entityId(delta)}`;
}

export const POINT_ACTION_TYPES_PATH = '/api/points/actions/types';
export const POINT_TRIGGER_EVENT_TYPES_PATH = '/api/points/triggers/events/types';

export function sendEmailPath(emailId: number, contactId: number): string {
  return `/api/emails/${entityId(emailId)}/contact/${entityId(contactId)}/send`;
}

export function resolveApiUrl(base: URL, apiPath: string): URL {
  if (!/^\/api\/[a-z0-9/_-]+$/i.test(apiPath)) {
    throw new Error('API path rejected');
  }
  const url = new URL(base.href);
  const prefix = url.pathname.replace(/\/$/, '');
  url.pathname = `${prefix}${apiPath}`;
  url.search = '';
  url.hash = '';
  return url;
}
