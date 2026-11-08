import type { AuditLog } from '../audit.js';
import type { Policy } from '../config.js';
import type { MauticGateway } from '../mautic/client.js';

export interface ToolContext {
  gateway: MauticGateway;
  policy: Policy;
  log: AuditLog;
}
