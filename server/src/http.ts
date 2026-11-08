export interface OutboundRequest {
  method: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';
  url: string;
  headers: Record<string, string>;
  body?: string;
  timeoutMs: number;
}

export interface InboundResponse {
  status: number;
  body: string;
  headers: Record<string, string>;
}

export interface HttpTransport {
  send(request: OutboundRequest): Promise<InboundResponse>;
}

export class FetchTransport implements HttpTransport {
  async send(request: OutboundRequest): Promise<InboundResponse> {
    const response = await fetch(request.url, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      signal: AbortSignal.timeout(request.timeoutMs),
    });
    const headers: Record<string, string> = {};
    response.headers.forEach((value, key) => {
      headers[key.toLowerCase()] = value;
    });
    return {
      status: response.status,
      body: await response.text(),
      headers,
    };
  }
}

export interface Sleeper {
  sleep(ms: number): Promise<void>;
}

export const realSleep: Sleeper = {
  sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
};
