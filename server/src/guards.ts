export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export function entityId(value: number): number {
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error('Invalid id');
  }
  return value;
}
