#!/usr/bin/env node
import { startServer } from './server.js';

startServer(process.env).catch((error: unknown) => {
  const message = error instanceof Error ? error.message : 'Failed to start mautic-mcp';
  console.error(message);
  process.exit(1);
});
