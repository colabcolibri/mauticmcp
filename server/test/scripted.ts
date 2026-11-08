import type { HttpTransport, InboundResponse, OutboundRequest } from '../src/http.js';
import type { Sleeper } from '../src/http.js';

export class ScriptedTransport implements HttpTransport {
  readonly calls: OutboundRequest[] = [];

  constructor(private readonly handle: (request: OutboundRequest, index: number) => InboundResponse) {}

  send(request: OutboundRequest): Promise<InboundResponse> {
    const index = this.calls.length;
    this.calls.push(request);
    return Promise.resolve(this.handle(request, index));
  }
}

export function jsonResponse(
  status: number,
  body: unknown,
  headers: Record<string, string> = {},
): InboundResponse {
  return { status, body: JSON.stringify(body), headers };
}

export class ImmediateSleep implements Sleeper {
  readonly waits: number[] = [];

  sleep(ms: number): Promise<void> {
    this.waits.push(ms);
    return Promise.resolve();
  }
}

export function baseEnv(overrides: Record<string, string> = {}): NodeJS.ProcessEnv {
  return {
    MAUTIC_BASE_URL: 'https://mautic.example.com',
    MAUTIC_AUTH: 'basic',
    MAUTIC_USERNAME: 'api',
    MAUTIC_PASSWORD: 'super-secret-password',
    ...overrides,
  };
}
