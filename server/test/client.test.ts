import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { BasicAuth, OAuthClientCredentials } from '../src/auth.js';
import { MauticClient } from '../src/mautic/client.js';
import { ImmediateSleep, jsonResponse, ScriptedTransport } from './scripted.js';

const base = new URL('https://mautic.example.com/instalacao');

function client(transport: ScriptedTransport, sleep = new ImmediateSleep()) {
  return new MauticClient(base, new BasicAuth('api', 'super-secret-password'), transport, sleep, 10_000, [
    'super-secret-password',
  ]);
}

describe('client', () => {
  it('prefixes the install path and rejects a path outside /api', async () => {
    const transport = new ScriptedTransport(() => jsonResponse(200, { ok: true }));
    const api = client(transport);
    await api.get('/api/contacts', { limit: 1 });
    assert.equal(transport.calls[0]?.url, 'https://mautic.example.com/instalacao/api/contacts?limit=1');
    await assert.rejects(() => api.get('/etc/passwd'), /rejected/);
  });

  it('retries GET on 503 and does not retry POST', async () => {
    const sleep = new ImmediateSleep();
    let gets = 0;
    const transport = new ScriptedTransport((request) => {
      if (request.method === 'GET') {
        gets += 1;
        return gets === 1 ? jsonResponse(503, { errors: [{ message: 'busy' }] }) : jsonResponse(200, { contacts: {} });
      }
      return jsonResponse(503, { errors: [{ message: 'busy' }] });
    });
    const api = client(transport, sleep);
    await api.get('/api/contacts');
    assert.equal(gets, 2);
    assert.equal(sleep.waits.length, 1);
    await assert.rejects(() => api.send('POST', '/api/contacts/new', { email: 'a@b.co' }));
    const posts = transport.calls.filter((call) => call.method === 'POST');
    assert.equal(posts.length, 1);
  });

  it('redacts a secret echoed in an error', async () => {
    const transport = new ScriptedTransport(() => jsonResponse(400, { errors: [{ message: 'password super-secret-password rejected' }] }));
    const api = client(transport);
    await assert.rejects(() => api.get('/api/contacts'), /\[redacted\]/);
  });

  it('on 401 fetches another token and retries the call', async () => {
    let apiCalls = 0;
    const transport = new ScriptedTransport((request) => {
      if (request.url.includes('/oauth/')) return jsonResponse(200, { access_token: `tok-${transport.calls.length}`, expires_in: 30 });
      apiCalls += 1;
      return apiCalls === 1 ? jsonResponse(401, { error: { message: 'expired' } }) : jsonResponse(200, { contact: { id: 1 } });
    });
    const auth = new OAuthClientCredentials(
      {
        kind: 'oauth',
        clientId: 'cid',
        clientSecret: 'super-secret-password',
        tokenUrl: new URL('https://mautic.example.com/oauth/v2/token'),
      },
      transport,
    );
    const api = new MauticClient(base, auth, transport, new ImmediateSleep(), 10_000, []);
    const payload = await api.get('/api/contacts/1');
    assert.deepEqual(payload, { contact: { id: 1 } });
    assert.equal(transport.calls.filter((call) => call.url.includes('/oauth/')).length, 2);
  });
});
