const MIN_SECRET = 8;

export function redact(text: string, secrets: readonly string[]): string {
  let out = text;
  for (const secret of secrets) {
    if (secret.length < MIN_SECRET) continue;
    out = out.split(secret).join('[redacted]');
  }
  return out;
}
