import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { createAuth } from './auth.js';
import { loadConfig } from './config.js';
import { StderrAuditLog } from './audit.js';
import { FetchTransport, realSleep, type HttpTransport } from './http.js';
import { MauticClient } from './mautic/client.js';
import { registerPrompts, registerTools } from './tools/register.js';

export async function startServer(
  env: NodeJS.ProcessEnv,
  transport: HttpTransport = new FetchTransport(),
): Promise<void> {
  const config = loadConfig(env);
  const auth = createAuth(config.auth, transport);
  const gateway = new MauticClient(config.baseUrl, auth, transport, realSleep, config.timeoutMs, config.secrets);
  const server = new McpServer({ name: 'mautic-mcp', version: '0.1.0' });
  const ctx = { gateway, policy: config.policy, log: new StderrAuditLog() };
  registerTools(server, ctx);
  registerPrompts(server);
  console.error(
    `mautic-mcp ready mode=${config.policy.mode} delete=${config.policy.allowDelete} send=${config.policy.allowSend}`,
  );
  await server.connect(new StdioServerTransport());
}
