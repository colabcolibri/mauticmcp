import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import type { MauticGateway, Query } from '../src/mautic/client.js';
import type { ToolContext } from '../src/tools/context.js';
import { createResource, upsertContact } from '../src/tools/write.js';

class FakeGateway implements MauticGateway {
  readonly calls: Array<{ method: string; path: string; body?: Record<string, unknown>; query?: Query }> = [];

  constructor(private readonly respond: (call: FakeGateway['calls'][number]) => unknown) {}

  get(path: string, query?: Query): Promise<unknown> {
    const call = { method: 'GET', path, query };
    this.calls.push(call);
    return Promise.resolve(this.respond(call));
  }

  send(method: 'POST' | 'PATCH' | 'PUT' | 'DELETE', path: string, body?: Record<string, unknown>): Promise<unknown> {
    const call = { method, path, body };
    this.calls.push(call);
    return Promise.resolve(this.respond(call));
  }
}

function context(gateway: MauticGateway): ToolContext {
  return {
    gateway,
    policy: { mode: 'operate', allowDelete: false, allowSend: false },
    log: { record() {} },
  };
}

describe('handlers', () => {
  it('upsert updates when the email already exists', async () => {
    const gateway = new FakeGateway((call) => {
      if (call.method === 'GET') {
        return { total: 1, contacts: { '8': { id: 8, email: 'ana@exemplo.com', firstname: 'Ana' } } };
      }
      return { contact: { id: 8, email: 'ana@exemplo.com', firstname: 'Ana Paula' } };
    });
    const result = await upsertContact(context(gateway), { email: 'ana@exemplo.com', firstname: 'Ana Paula' });
    assert.equal(result.isError, undefined);
    assert.equal(gateway.calls[1]?.method, 'PATCH');
    assert.equal(gateway.calls[1]?.path, '/api/contacts/8/edit');
  });

  it('upsert creates when the search is empty', async () => {
    const gateway = new FakeGateway((call) => {
      if (call.method === 'GET') return { total: 0, contacts: {} };
      return { contact: { id: 9, email: 'novo@exemplo.com' } };
    });
    await upsertContact(context(gateway), { email: 'novo@exemplo.com' });
    assert.equal(gateway.calls[1]?.method, 'POST');
    assert.equal(gateway.calls[1]?.path, '/api/contacts/new');
  });

  it('upsert does not write when the search returns someone else', async () => {
    const gateway = new FakeGateway(() => ({
      total: 1,
      contacts: { '8': { id: 8, email: 'outra@exemplo.com' } },
    }));
    const result = await upsertContact(context(gateway), { email: 'ana@exemplo.com' });
    assert.equal(result.isError, true);
    assert.equal(gateway.calls.length, 1);
  });

  it('creating a campaign sends the validated body', async () => {
    const gateway = new FakeGateway(() => ({ campaign: { id: 4, name: 'Boas-vindas', isPublished: false } }));
    const result = await createResource(context(gateway), {
      resource: 'campaigns',
      name: 'Boas-vindas',
      events: [{ id: 'new1', name: 'Enviar', type: 'email.send' }],
      lists: [3],
    });
    assert.equal(result.isError, undefined);
    assert.equal(gateway.calls[0]?.method, 'POST');
    assert.equal(gateway.calls[0]?.path, '/api/campaigns/new');
    assert.equal(gateway.calls[0]?.body?.isPublished, 0);
  });
});
