import { LIMITS } from '../limits.js';

export interface ToolResult {
  [key: string]: unknown;
  content: Array<{ type: 'text'; text: string }>;
  isError?: boolean;
}

export function ok(data: unknown): ToolResult {
  let text = JSON.stringify(data, null, 2);
  if (text.length > LIMITS.responseMax) {
    text = `${text.slice(0, LIMITS.responseMax)}\n…(response truncated)`;
  }
  return { content: [{ type: 'text', text }] };
}

export function fail(message: string): ToolResult {
  return { content: [{ type: 'text', text: message }], isError: true };
}
