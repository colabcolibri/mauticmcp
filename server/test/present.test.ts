import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { summarizeCollection, summarizePayload } from '../src/mautic/present.js';

describe('summary', () => {
  it('reads the Mautic contact map and hides fields', () => {
    const page = summarizeCollection('contacts', {
      total: '2',
      contacts: {
        '1': { id: 1, email: 'a@b.co', firstname: 'Ana', fields: { all: { city: 'x' } }, password: 'nope' },
        '2': { id: 2, email: 'c@d.co', firstname: 'Caio' },
      },
    });
    assert.equal(page.total, 2);
    assert.equal(page.items.length, 2);
    assert.equal(page.items[0]?.email, 'a@b.co');
    assert.equal('fields' in (page.items[0] ?? {}), false);
    assert.equal('password' in (page.items[0] ?? {}), false);
  });

  it('email search omits HTML and the detail includes it, truncated', () => {
    const html = 'h'.repeat(20_100);
    const list = summarizeCollection('emails', { emails: { '5': { id: 5, name: 'Oi', customHtml: html } } });
    assert.equal('customHtml' in (list.items[0] ?? {}), false);
    const detail = summarizePayload('emails', { email: { id: 5, name: 'Oi', customHtml: html } });
    assert.equal(typeof detail.customHtml, 'string');
    assert.equal((detail.customHtml as string).length, 20_000);
    assert.equal(detail.customHtmlTruncated, true);
  });

  it('a segment reads the lists key', () => {
    const page = summarizeCollection('segments', { total: 1, lists: { '3': { id: 3, name: 'Gmail', alias: 'gmail' } } });
    assert.equal(page.items[0]?.name, 'Gmail');
  });
});
