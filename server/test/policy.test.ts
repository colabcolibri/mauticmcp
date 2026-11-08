import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { describePolicy, enabledTools } from '../src/policy.js';

describe('policy', () => {
  it('read mode does not create, delete or send', () => {
    const tools = enabledTools({ mode: 'read', allowDelete: true, allowSend: true });
    assert.equal(tools.includes('mautic_create'), false);
    assert.equal(tools.includes('mautic_delete'), false);
    assert.equal(tools.includes('mautic_send_email'), false);
    assert.equal(tools.includes('mautic_search'), true);
  });

  it('operate creates, and delete/send exist only with the flag', () => {
    const plain = enabledTools({ mode: 'operate', allowDelete: false, allowSend: false });
    assert.equal(plain.includes('mautic_create'), true);
    assert.equal(plain.includes('mautic_clone_campaign'), true);
    assert.equal(plain.includes('mautic_delete'), false);
    const armed = enabledTools({ mode: 'operate', allowDelete: true, allowSend: true });
    assert.equal(armed.includes('mautic_delete'), true);
    assert.equal(armed.includes('mautic_send_email'), true);
    assert.equal(describePolicy({ mode: 'operate', allowDelete: false, allowSend: true }).canSend, true);
  });
});
