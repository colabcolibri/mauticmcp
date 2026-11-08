import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { BasicAuth, OAuthClientCredentials } from '../src/auth.js';
import { jsonResponse, ScriptedTransport } from './scripted.js';

describe('auth', () => {
  it('basic builds the header', async () => {
    const auth = new BasicAuth('api', 'super-secret-password');
    const headers = await auth.headers();
    const expected = Buffer.from('api:super-secret-password', 'utf8').toString('base64');
    assert.equal(headers.Authorization, `Basic ${expected}`);
  });

  it('oauth sends a form body, not JSON', async () => {
    const transport = new ScriptedTransport(() => jsonResponse(200, { access_token: 'tok', expires_in: 3600 }));
    const auth = new OAuthClientCredentials(
      {
        kind: 'oauth',
        clientId: 'cid',
        clientSecret: 'super-secret-password',
        tokenUrl: new URL('https://mautic.example.com/oauth/v2/token'),
      },
      transport,
      () => 1_000,
    );
    const headers = await auth.headers();
    const call = transport.calls[0];
    assert.ok(call);
    assert.equal(call.headers['Content-Type'], 'application/x-www-form-urlencoded');
    assert.equal(call.body?.startsWith('{'), false);
    assert.match(call.body ?? '', /grant_type=client_credentials/);
    assert.match(call.body ?? '', /client_id=cid/);
    assert.equal(headers.Authorization, 'Bearer tok');
  });
});
