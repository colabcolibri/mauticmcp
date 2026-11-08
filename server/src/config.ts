export type AuthConfig =
  | { kind: 'basic'; username: string; password: string }
  | { kind: 'oauth'; clientId: string; clientSecret: string; tokenUrl: URL };

export interface Policy {
  mode: 'read' | 'operate';
  allowDelete: boolean;
  allowSend: boolean;
}

export interface ServerConfig {
  baseUrl: URL;
  auth: AuthConfig;
  policy: Policy;
  timeoutMs: number;
  secrets: string[];
}

export function parseBaseUrl(raw: string, label: string): URL {
  let url: URL;
  try {
    url = new URL(raw);
  } catch {
    throw new Error(`${label} is invalid`);
  }
  const local = url.hostname === 'localhost' || url.hostname === '127.0.0.1';
  if (url.protocol !== 'https:' && !(url.protocol === 'http:' && local)) {
    throw new Error(`${label} must be https (http only on localhost)`);
  }
  const path = url.pathname.replace(/\/+$/, '').replace(/\/api$/, '');
  url.pathname = path === '' ? '/' : path;
  url.search = '';
  url.hash = '';
  url.username = '';
  url.password = '';
  return url;
}

export function loadConfig(env: NodeJS.ProcessEnv): ServerConfig {
  const baseUrl = parseBaseUrl(required(env, 'MAUTIC_BASE_URL'), 'MAUTIC_BASE_URL');
  const authKind = (env.MAUTIC_AUTH ?? 'basic').trim().toLowerCase();
  const mode = (env.MAUTIC_MODE ?? 'read').trim().toLowerCase();
  if (mode !== 'read' && mode !== 'operate') {
    throw new Error('MAUTIC_MODE must be read or operate');
  }

  let auth: AuthConfig;
  const secrets: string[] = [];
  if (authKind === 'basic') {
    const username = required(env, 'MAUTIC_USERNAME');
    const password = required(env, 'MAUTIC_PASSWORD');
    if (username.includes(':')) {
      throw new Error('MAUTIC_USERNAME must not contain ":"');
    }
    auth = { kind: 'basic', username, password };
    secrets.push(password);
  } else if (authKind === 'oauth') {
    const clientSecret = required(env, 'MAUTIC_CLIENT_SECRET');
    auth = {
      kind: 'oauth',
      clientId: required(env, 'MAUTIC_CLIENT_ID'),
      clientSecret,
      tokenUrl: parseBaseUrl(required(env, 'MAUTIC_TOKEN_URL'), 'MAUTIC_TOKEN_URL'),
    };
    secrets.push(clientSecret);
  } else {
    throw new Error('MAUTIC_AUTH must be basic or oauth');
  }

  const timeoutRaw = env.MAUTIC_TIMEOUT_MS?.trim();
  const timeoutMs = timeoutRaw ? Number(timeoutRaw) : 10_000;
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1000 || timeoutMs > 60_000) {
    throw new Error('MAUTIC_TIMEOUT_MS must be an integer between 1000 and 60000');
  }

  return {
    baseUrl,
    auth,
    policy: {
      mode,
      allowDelete: flag(env.MAUTIC_ALLOW_DELETE, true),
      allowSend: flag(env.MAUTIC_ALLOW_SEND, false),
    },
    timeoutMs,
    secrets,
  };
}

function required(env: NodeJS.ProcessEnv, key: string): string {
  const value = env[key]?.trim();
  if (!value) throw new Error(`Set ${key}`);
  return value;
}

function flag(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined || value.trim() === '') return fallback;
  const normalized = value.trim().toLowerCase();
  if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
  if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
  throw new Error(`Invalid boolean in a policy flag: ${normalized}`);
}
