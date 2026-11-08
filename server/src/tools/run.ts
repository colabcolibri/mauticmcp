import type { AuditEntry, AuditLog } from '../audit.js';
import { MauticApiError } from '../mautic/errors.js';
import { fail, type ToolResult } from './result.js';

export async function runTool(
  log: AuditLog,
  entry: Omit<AuditEntry, 'status'>,
  action: () => Promise<ToolResult>,
): Promise<ToolResult> {
  try {
    const result = await action();
    log.record({ ...entry, status: result.isError ? 'error' : 'ok' });
    return result;
  } catch (error) {
    log.record({ ...entry, status: 'error' });
    if (error instanceof MauticApiError) {
      return fail(`Mautic refused (${error.status}): ${error.safeMessage}`);
    }
    if (error instanceof Error && (error.message.startsWith('Empty Mautic') || error.message.startsWith('Mautic response') || error.message === 'Invalid id')) {
      return fail(error.message);
    }
    console.error(error instanceof Error ? error.name : 'error');
    return fail('Unexpected failure talking to Mautic.');
  }
}
