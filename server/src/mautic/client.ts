import type { AuthProvider } from '../auth.js';
import type { HttpTransport, InboundResponse, Sleeper } from '../http.js';
import { redact } from '../redact.js';
import { resolveApiUrl } from './paths.js';
import { MauticApiError, readApiError } from './errors.js';

export interface Query {
  [key: string]: string | number;
}

export interface MauticGateway {
  get(path: string, query?: Query): Promise<unknown>;
  send(method: 'POST' | 'PATCH' | 'PUT' | 'DELETE', path: string, body?: Record<string, unknown>): Promise<unknown>;
}

export class MauticClient implements MauticGateway {
  constructor(
    private readonly baseUrl: URL,
    private readonly auth: AuthProvider,
    private readonly transport: HttpTransport,
    private readonly sleeper: Sleeper,
    private readonly timeoutMs: number,
    private readonly secrets: readonly string[],
  ) {}

  get(path: string, query?: Query): Promise<unknown> {
    return this.request('GET', path, undefined, query, false, false);
  }

  send(
    method: 'POST' | 'PATCH' | 'PUT' | 'DELETE',
    path: string,
    body?: Record<string, unknown>,
  ): Promise<unknown> {
    return this.request(method, path, body, undefined, false, false);
  }

  private async request(
    method: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE',
    path: string,
    body: Record<string, unknown> | undefined,
    query: Query | undefined,
    retriedAuth: boolean,
    retriedTransient: boolean,
  ): Promise<unknown> {
    const url = resolveApiUrl(this.baseUrl, path);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        url.searchParams.set(key, String(value));
      }
    }
    const headers: Record<string, string> = {
      Accept: 'application/json',
      ...(await this.auth.headers()),
    };
    let encoded: string | undefined;
    if (body !== undefined) {
      headers['Content-Type'] = 'application/json';
      encoded = JSON.stringify(body);
    }
    const response = await this.transport.send({
      method,
      url: url.href,
      headers,
      body: encoded,
      timeoutMs: this.timeoutMs,
    });

    if (response.status === 401 && !retriedAuth) {
      this.auth.invalidate();
      return this.request(method, path, body, query, true, retriedTransient);
    }
    if (method === 'GET' && isTransient(response.status) && !retriedTransient) {
      await this.sleeper.sleep(retryDelay(response));
      return this.request(method, path, body, query, retriedAuth, true);
    }
    if (response.status >= 400) {
      throw new MauticApiError(response.status, redact(readApiError(response.status, response.body), this.secrets));
    }
    if (response.body.trim() === '') return {};
    try {
      return JSON.parse(response.body) as unknown;
    } catch {
      throw new MauticApiError(response.status, 'Mautic response is not JSON');
    }
  }
}

function isTransient(status: number): boolean {
  return status === 429 || status === 503;
}

function retryDelay(response: InboundResponse): number {
  const raw = response.headers['retry-after'];
  const seconds = raw === undefined ? Number.NaN : Number(raw);
  if (Number.isFinite(seconds) && seconds >= 0 && seconds <= 2) return seconds * 1000;
  return 200;
}
