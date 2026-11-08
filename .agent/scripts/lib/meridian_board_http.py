"""Stdlib HTTP handler for the kit HTML delivery monitor. GET only."""

from __future__ import annotations

import json
import mimetypes
import posixpath
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from meridian_board_snapshot import build_snapshot
from meridian_board_watch import db_fingerprint
from meridian_db import db_exists, export_entity_markdown

ENTITY_TYPES = {
    "us": "us",
    "user_story": "us",
    "epic": "epic",
    "epics": "epic",
    "version": "version",
    "versions": "version",
    "sprint": "sprint",
    "sprints": "sprint",
}

def board_ui_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "board-ui"


def _json_bytes(payload: dict[str, Any], status: int = 200) -> tuple[int, bytes, str]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


def _safe_docs_path(package_root: Path, rel: str) -> Path | None:
    if not rel or rel.startswith("/") or "\\" in rel:
        return None
    docs = (package_root / "docs").resolve()
    target = (docs / rel).resolve()
    try:
        target.relative_to(docs)
    except ValueError:
        return None
    if not target.is_file():
        return None
    return target


def list_docs(package_root: Path) -> list[dict[str, str]]:
    docs = (package_root / "docs").resolve()
    if not docs.is_dir():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(docs).as_posix()
        if any(part.startswith(".") for part in path.relative_to(docs).parts):
            continue
        items.append({"path": rel, "title": path.stem})
    return items


class BoardHandler(BaseHTTPRequestHandler):
    server_version = "MeridianBoard/1.0"
    package_root: Path
    static_root: Path
    bind_host: str
    bind_port: int

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def handle(self) -> None:
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError):
            # Browser prefetch / cancelled tabs may connect then reset before the request line.
            return

    def _cors(self) -> None:
        origin = self.headers.get("Origin", "")
        allow = origin in ("null",) or origin.startswith("http://127.0.0.1") or origin.startswith(
            "http://localhost"
        )
        if allow:
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        self._reject_method()

    def do_PUT(self) -> None:  # noqa: N802
        self._reject_method()

    def do_DELETE(self) -> None:  # noqa: N802
        self._reject_method()

    def _reject_method(self) -> None:
        status, body, ctype = _json_bytes({"error": "method not allowed"}, 405)
        self._write(status, body, ctype)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        route = parsed.path
        query = parse_qs(parsed.query)
        if route == "/api/health":
            self._write(*_json_bytes(self._health()))
            return
        if route == "/api/snapshot":
            snap = build_snapshot(self.package_root)
            status = 503 if snap.get("error") else 200
            self._write(*_json_bytes(snap, status))
            return
        if route == "/api/entity":
            self._entity(query)
            return
        if route == "/api/docs":
            self._write(*_json_bytes({"docs": list_docs(self.package_root)}))
            return
        if route == "/api/doc":
            self._doc(query)
            return
        if route == "/api/events":
            self._events()
            return
        self._static(route)

    def _health(self) -> dict[str, Any]:
        return {
            "ok": True,
            "packageRoot": str(self.package_root),
            "host": self.bind_host,
            "port": self.bind_port,
            "pid": __import__("os").getpid(),
            "db": db_exists(self.package_root),
            "generation": db_fingerprint(self.package_root),
        }

    def _entity(self, query: dict[str, list[str]]) -> None:
        raw_type = (query.get("type") or ["us"])[0]
        entity = ENTITY_TYPES.get(raw_type.lower())
        entity_id = (query.get("id") or [""])[0].strip()
        if not entity or not entity_id:
            self._write(*_json_bytes({"error": "type and id required"}, 400))
            return
        if not db_exists(self.package_root):
            self._write(*_json_bytes({"error": "meridian.db not found"}, 503))
            return
        try:
            row = export_entity_markdown(self.package_root, entity, entity_id)
        except ValueError as exc:
            self._write(*_json_bytes({"error": str(exc)}, 400))
            return
        if not row:
            self._write(*_json_bytes({"error": "not found", "id": entity_id}, 404))
            return
        self._write(*_json_bytes(row))

    def _doc(self, query: dict[str, list[str]]) -> None:
        rel = unquote((query.get("path") or [""])[0])
        target = _safe_docs_path(self.package_root, rel)
        if target is None:
            self._write(*_json_bytes({"error": "not found"}, 404))
            return
        text = target.read_text(encoding="utf-8")
        self._write(*_json_bytes({"path": rel, "raw": text}))

    def _events(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Connection", "keep-alive")
        self._cors()
        self.end_headers()
        last = db_fingerprint(self.package_root)
        stop = getattr(self.server, "stop_event", None)
        try:
            self.wfile.write(f"event: connected\ndata: {last}\n\n".encode("utf-8"))
            self.wfile.flush()
            while stop is None or not stop.is_set():
                if stop is not None and stop.wait(0.4):
                    return
                if stop is None:
                    time.sleep(0.4)
                current = db_fingerprint(self.package_root)
                if current != last:
                    last = current
                    self.wfile.write(
                        f"event: planning-changed\ndata: {current}\n\n".encode("utf-8")
                    )
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError):
            return

    def _static(self, route: str) -> None:
        rel = posixpath.normpath(unquote(route)).lstrip("/")
        if rel in ("", "."):
            rel = "index.html"
        root = self.static_root.resolve()
        target = (root / rel).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            self._write(*_json_bytes({"error": "not found"}, 404))
            return
        if not target.is_file():
            self._write(*_json_bytes({"error": "not found"}, 404))
            return
        data = target.read_bytes()
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self._write(200, data, ctype)

    def _write(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)


def make_server(package_root: Path, host: str = "127.0.0.1") -> ThreadingHTTPServer:
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("bind host must be loopback")
    static_root = board_ui_dir()
    if not static_root.is_dir():
        raise FileNotFoundError(f"board-ui missing: {static_root}")

    class BoundHandler(BoardHandler):
        pass

    httpd = ThreadingHTTPServer((host, 0), BoundHandler)
    httpd.daemon_threads = True
    httpd.block_on_close = False
    httpd.stop_event = threading.Event()
    BoundHandler.package_root = package_root.resolve()
    BoundHandler.static_root = static_root
    BoundHandler.bind_host = httpd.server_address[0]
    BoundHandler.bind_port = httpd.server_address[1]
    return httpd
