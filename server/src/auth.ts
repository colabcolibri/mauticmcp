import type { AuthConfig } from './config.js';
import type { HttpTransport } from './http.js';
import { MauticApiError, readApiError } from './mautic/errors.js';
import { redact } from './redact.js';

export interface AuthProvider {
  headers(): Promise<Record<string, string>>;
  invalidate(): void;
}

export function createAuth(config: AuthConfig, transport: HttpTransport): AuthProvider {
  if (config.kind === 'basic') return new BasicAuth(config.username, config.password);
  return new OAuthClientCredentials(config, transport);
}

export class BasicAuth implements AuthProvider {
  constructor(
    private readonly username: string,
    private readonly password: string,
  ) {}

  headers(): Promise<Record<string, string>> {
    const token = Buffer.from(`${this.username}:${this.password}`, 'utf8').toString('base64');
    return Promise.resolve({ Authorization: `Basic ${token}` });
  }

  invalidate(): void {}
}

export class OAuthClientCredentials implements AuthProvider {
  private token: { accessToken: string; expiresAt: number } | null = null;

  constructor(
    private readonly config: Extract<AuthConfig, { kind: 'oauth' }>,
    private readonly transport: HttpTransport,
    private readonly now: () => number = Date.now,
  ) {}

  async headers(): Promise<Record<string, string>> {
    if (!this.token || this.now() >= this.token.expiresAt) {
      await this.fetchToken();
    }
    return { Authorization: `Bearer ${this.token?.accessToken ?? ''}` };
  }

  invalidate(): void {
    this.token = null;
  }

  private async fetchToken(): Promise<void> {
    const body = new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: this.config.clientId,
      client_secret: this.config.clientSecret,
    });
    const response = await this.transport.send({
      method: 'POST',
      url: this.config.tokenUrl.href,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: body.toString(),
      timeoutMs: 10_000,
    });
    if (response.status >= 400) {
      throw new MauticApiError(
        response.status,
        redact(readApiError(response.status, response.body), [this.config.clientSecret]),
      );
    }
    let payload: unknown;
    try {
      payload = JSON.parse(response.body) as unknown;
    } catch {
      throw new MauticApiError(response.status, 'Invalid token response');
    }
    if (!isToken(payload)) {
      throw new MauticApiError(response.status, 'Mautic did not return access_token');
    }
    const skew = Math.max(payload.expires_in - 60, 15);
    this.token = {
      accessToken: payload.access_token,
      expiresAt: this.now() + skew * 1000,
    };
  }
}

function isToken(value: unknown): value is { access_token: string; expires_in: number } {
  if (typeof value !== 'object' || value === null) return false;
  const record = value as Record<string, unknown>;
  return typeof record.access_token === 'string' && record.access_token.length > 0 && typeof record.expires_in === 'number';
}
