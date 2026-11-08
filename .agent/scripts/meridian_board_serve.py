#!/usr/bin/env python3
"""Foreground kit HTML board — 127.0.0.1, ephemeral port, Ctrl+C stops."""

from __future__ import annotations

import argparse
import signal
import sys
import threading
import webbrowser
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))

from meridian_board_http import make_server  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Meridian HTML delivery monitor")
    parser.add_argument(
        "package_root",
        nargs="?",
        default=".",
        help="product root (folder that contains .meridian/ and docs/)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="loopback only (default 127.0.0.1)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="print URL only",
    )
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    try:
        httpd = make_server(root, args.host)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    host, port = httpd.server_address[0], httpd.server_address[1]
    url = f"http://{host}:{port}/"
    print(url, flush=True)
    print("Ctrl+C stops the monitor.", flush=True)
    if not args.no_browser:
        webbrowser.open(url)

    def _stop(_signum: int | None = None, _frame: object = None) -> None:
        httpd.stop_event.set()
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        _stop()
    finally:
        httpd.stop_event.set()
        httpd.server_close()
        print("Stopped.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
