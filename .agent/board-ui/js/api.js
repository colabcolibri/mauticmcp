const DEFAULT_PORT_HINT = "python3 .agent/board";

export function apiBase() {
  if (location.protocol === "http:" || location.protocol === "https:") {
    return "";
  }
  return "";
}

export async function getJson(path) {
  const url = `${apiBase()}${path}`;
  const res = await fetch(url, { cache: "no-store" });
  const text = await res.text();
  let data = null;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }
  return { ok: res.ok, status: res.status, data };
}

export function subscribe(onChange) {
  if (location.protocol === "file:") {
    return () => {};
  }
  let es;
  let delay = 1000;
  let stopped = false;

  function connect() {
    if (stopped) return;
    es = new EventSource(`${apiBase()}/api/events`);
    es.addEventListener("planning-changed", () => {
      delay = 1000;
      onChange();
    });
    es.addEventListener("connected", () => {
      delay = 1000;
    });
    es.onerror = () => {
      es.close();
      onChange({ disconnected: true });
      if (stopped) return;
      setTimeout(connect, delay);
      delay = Math.min(delay * 2, 8000);
    };
  }
  connect();
  return () => {
    stopped = true;
    es?.close();
  };
}

export { DEFAULT_PORT_HINT };
