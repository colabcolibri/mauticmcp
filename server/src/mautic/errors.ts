import { isRecord } from '../guards.js';

export class MauticApiError extends Error {
  constructor(
    readonly status: number,
    readonly safeMessage: string,
  ) {
    super(safeMessage);
    this.name = 'MauticApiError';
  }
}

export function readApiError(status: number, body: string): string {
  try {
    const message = extractMessage(JSON.parse(body) as unknown);
    if (message) return clip(message, 400);
  } catch {
    return `HTTP ${status}`;
  }
  return `HTTP ${status}`;
}

function extractMessage(payload: unknown): string | undefined {
  if (!isRecord(payload)) return undefined;
  if (typeof payload.error_description === 'string') return payload.error_description;
  if (typeof payload.message === 'string') return payload.message;
  if (typeof payload.detail === 'string') return payload.detail;
  const error = payload.error;
  if (typeof error === 'string') return error;
  if (isRecord(error) && typeof error.message === 'string') return error.message;
  const errors = payload.errors;
  if (!Array.isArray(errors) || errors.length === 0) return undefined;
  const first = errors[0];
  if (typeof first === 'string') return first;
  if (isRecord(first) && typeof first.message === 'string') return first.message;
  return undefined;
}

function clip(text: string, max: number): string {
  return text.length <= max ? text : text.slice(0, max);
}
