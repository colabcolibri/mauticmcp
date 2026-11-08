import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { loadConfig, parseBaseUrl } from '../src/config.js';
import { baseEnv } from './scripted.js';

describe('config', () => {
  it('accepts https and strips a trailing /api', () => {
    const url = parseBaseUrl('https://mautic.example.com/api/', 'MAUTIC_BASE_URL');
    assert.equal(url.href, 'https://mautic.example.com/');
  });

  it('accepts http only on localhost', () => {
    assert.equal(parseBaseUrl('http://localhost:8080/mautic', 'MAUTIC_BASE_URL').origin, 'http://localhost:8080');
    assert.throws(() => parseBaseUrl('http://mautic.example.com', 'MAUTIC_BASE_URL'), /https/);
  });

  it('defaults to read, with delete enabled in policy and send disabled', () => {
    const config = loadConfig(baseEnv());
    assert.equal(config.policy.mode, 'read');
    assert.equal(config.policy.allowDelete, true);
    assert.equal(config.policy.allowSend, false);
    assert.equal(config.auth.kind, 'basic');
  });

  it('operate with flags enables delete and send', () => {
    const config = loadConfig(baseEnv({
      MAUTIC_MODE: 'operate',
      MAUTIC_ALLOW_DELETE: 'true',
      MAUTIC_ALLOW_SEND: 'yes',
    }));
    assert.equal(config.policy.mode, 'operate');
    assert.equal(config.policy.allowDelete, true);
    assert.equal(config.policy.allowSend, true);
  });

  it('rejects a basic username that contains a colon', () => {
    assert.throws(() => loadConfig(baseEnv({ MAUTIC_USERNAME: 'a:b' })), /must not contain/);
  });
});
