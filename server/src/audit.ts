export interface AuditEntry {
  tool: string;
  status: 'ok' | 'error';
  resource?: string;
  id?: number;
}

export interface AuditLog {
  record(entry: AuditEntry): void;
}

export class StderrAuditLog implements AuditLog {
  record(entry: AuditEntry): void {
    console.error(JSON.stringify({ ts: new Date().toISOString(), ...entry }));
  }
}
