import { CREATABLE, RESOURCE_NAMES } from './mautic/catalog.js';
import type { Policy } from './config.js';

export type ToolName =
  | 'mautic_capabilities'
  | 'mautic_search'
  | 'mautic_get'
  | 'mautic_contact_activity'
  | 'mautic_campaign_contacts'
  | 'mautic_point_types'
  | 'mautic_upsert_contact'
  | 'mautic_create'
  | 'mautic_update'
  | 'mautic_membership'
  | 'mautic_add_note'
  | 'mautic_adjust_points'
  | 'mautic_clone_campaign'
  | 'mautic_delete'
  | 'mautic_send_email';

const READ_TOOLS: ToolName[] = [
  'mautic_capabilities',
  'mautic_search',
  'mautic_get',
  'mautic_contact_activity',
  'mautic_campaign_contacts',
  'mautic_point_types',
];

const OPERATE_TOOLS: ToolName[] = [
  'mautic_upsert_contact',
  'mautic_create',
  'mautic_update',
  'mautic_membership',
  'mautic_add_note',
  'mautic_adjust_points',
  'mautic_clone_campaign',
];

export function enabledTools(policy: Policy): ToolName[] {
  if (policy.mode === 'read') return [...READ_TOOLS];
  const tools = [...READ_TOOLS, ...OPERATE_TOOLS];
  if (policy.allowDelete) tools.push('mautic_delete');
  if (policy.allowSend) tools.push('mautic_send_email');
  return tools;
}

export function describePolicy(policy: Policy) {
  const canWrite = policy.mode === 'operate';
  return {
    mode: policy.mode,
    canWrite,
    canDelete: canWrite && policy.allowDelete,
    canSend: canWrite && policy.allowSend,
    resources: RESOURCE_NAMES,
    create: CREATABLE,
    defaults: {
      newCampaignIsPublished: false,
      newEmailIsPublished: false,
      newSegmentIsPublished: true,
    },
    notAvailable: [
      'send email to a whole segment',
      'manual campaign execution',
      'local file upload',
      'projects: API v2 on this instance returned 403',
    ],
  };
}
