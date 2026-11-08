#!/usr/bin/env python3
"""HTTP GET-only + fingerprint tests for the kit HTML monitor."""

from __future__ import annotations

import json
import socket
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS_ROOT = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPTS_ROOT / "lib"))

from meridian_board_http import make_server  # noqa: E402
from meridian_board_watch import db_fingerprint  # noqa: E402
from meridian_db import bootstrap  # noqa: E402


def _get(url: str) -> tuple[int, dict | str]:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        status = exc.code
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, raw


def _post(url: str) -> int:
    req = urllib.request.Request(url, data=b"{}", method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:  # noqa: S310
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code


def main() -> int:
    try:
        make_server(Path("."), "0.0.0.0")
        raise AssertionError("non-loopback bind must fail")
    except ValueError:
        pass

    with tempfile.TemporaryDirectory(prefix="meridian-board-http-") as tmp:
        root = Path(tmp) / "product"
        (root / "docs").mkdir(parents=True)
        (root / "docs" / "00_scope.md").write_text("---\nstatus: draft\n---\n# scope\n", encoding="utf-8")
        empty_fp = db_fingerprint(root)
        wal = root / ".meridian" / "meridian.db-wal"
        wal.parent.mkdir(parents=True, exist_ok=True)
        wal.write_bytes(b"x")
        assert db_fingerprint(root) != empty_fp

        httpd = make_server(root, "127.0.0.1")
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        port = httpd.server_address[1]
        base = f"http://127.0.0.1:{port}"
        try:
            status, health = _get(f"{base}/api/health")
            assert status == 200 and isinstance(health, dict)
            assert health.get("host") in ("127.0.0.1", "localhost")
            snap_status, snap = _get(f"{base}/api/snapshot")
            assert snap_status == 503 and isinstance(snap, dict) and "error" in snap
            assert _post(f"{base}/api/snapshot") == 405
            entity_status, entity_body = _get(f"{base}/api/entity")
            assert entity_status == 400 and isinstance(entity_body, dict)
            assert "type and id required" in str(entity_body.get("error"))
            doc_status, _ = _get(f"{base}/api/doc?path=../.meridian/meridian.db")
            assert doc_status == 404
            ok, body = _get(f"{base}/api/doc?path=00_scope.md")
            assert ok == 200 and isinstance(body, dict) and "raw" in body
            sock = socket.create_connection(("127.0.0.1", port), timeout=2)
            sock.close()

            page_status, page = _get(f"{base}/")
            assert page_status == 200
            css_status, css = _get(f"{base}/css/layout.css")
            assert css_status == 200 and isinstance(css, str) and "100dvh" in css

            bootstrap(root)
            ok2, snap2 = _get(f"{base}/api/snapshot")
            assert ok2 == 200 and isinstance(snap2, dict)
            assert "userStories" in snap2
        finally:
            httpd.shutdown()
            httpd.server_close()

    print("OK: board http")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
