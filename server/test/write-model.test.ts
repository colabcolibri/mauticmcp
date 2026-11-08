import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { buildCreate, buildUpdate } from '../src/mautic/write-model.js';

const event = { id: 'new1', name: 'Enviar', type: 'email.send', properties: { email: 12 } };

describe('writes', () => {
  it('a campaign without events or a source fails before HTTP', () => {
    const missingEvents = buildCreate('campaigns', { name: 'Boas-vindas', lists: [3] });
    assert.equal(missingEvents.ok, false);
    const missingSource = buildCreate('campaigns', { name: 'Boas-vindas', events: [event] });
    assert.equal(missingSource.ok, false);
  });

  it('a new campaign is unpublished and gets a linear canvas', () => {
    const built = buildCreate('campaigns', { name: 'Boas-vindas', events: [event], lists: [3] });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.method, 'POST');
    assert.equal(built.value.path, '/api/campaigns/new');
    assert.equal(built.value.body.isPublished, 0);
    assert.deepEqual(built.value.body.lists, [{ id: 3 }]);
    const canvas = built.value.body.canvasSettings as { nodes: Array<{ id: string }>; connections: Array<{ sourceId: string }> };
    assert.equal(canvas.nodes[0]?.id, 'new1');
    assert.equal(canvas.connections[0]?.sourceId, 'lists');
  });

  it('a segment email requires lists and is created unpublished', () => {
    const missing = buildCreate('emails', { name: 'Oi', subject: 'Oi', emailType: 'list' });
    assert.equal(missing.ok, false);
    const built = buildCreate('emails', { name: 'Oi', subject: 'Oi', emailType: 'list', lists: [4] });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.body.isPublished, 0);
    assert.deepEqual(built.value.body.lists, [4]);
  });

  it('a new segment is published', () => {
    const built = buildCreate('segments', { name: 'Gmail', filters: [{ glue: 'and', field: 'email' }] });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.body.isPublished, 1);
  });

  it('blocks a password in extra and refuses to override a real field', () => {
    const secret = buildCreate('segments', { name: 'A', extra: { password: 'x' } });
    assert.equal(secret.ok, false);
    const reserved = buildCreate('segments', { name: 'A', extra: { name: 'B' } });
    assert.equal(reserved.ok, false);
  });

  it('changing campaign events uses PUT and replaces the canvas', () => {
    const built = buildUpdate('campaigns', 9, { name: 'Boas-vindas', events: [event], forms: [2] });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.method, 'PUT');
    assert.equal(built.value.path, '/api/campaigns/9/edit');
    const canvas = built.value.body.canvasSettings as { connections: Array<{ sourceId: string }> };
    assert.equal(canvas.connections[0]?.sourceId, 'forms');
  });

  it('a remote asset requires the URL and rejects a local file', () => {
    const missing = buildCreate('assets', { title: 'PDF' });
    assert.equal(missing.ok, false);
    const local = buildCreate('assets', { title: 'PDF', storageLocation: 'local', remotePath: 'https://cdn.exemplo.com/a.pdf' });
    assert.equal(local.ok, false);
    const built = buildCreate('assets', { title: 'PDF', remotePath: 'https://cdn.exemplo.com/a.pdf' });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.body.storageLocation, 'remote');
    assert.equal(built.value.body.isPublished, 0);
  });

  it('a point action requires type and delta', () => {
    const missing = buildCreate('points', { name: 'Abriu e-mail' });
    assert.equal(missing.ok, false);
    const built = buildCreate('points', { name: 'Abriu e-mail', type: 'email.open', delta: 5 });
    assert.equal(built.ok, true);
  });

  it('changing only the name uses PATCH', () => {
    const built = buildUpdate('campaigns', 9, { name: 'Novo nome' });
    assert.equal(built.ok, true);
    if (!built.ok) return;
    assert.equal(built.value.method, 'PATCH');
    assert.deepEqual(built.value.body, { name: 'Novo nome' });
  });
});
