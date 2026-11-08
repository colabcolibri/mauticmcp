"""SQLite file fingerprint for the kit HTML monitor (db + WAL + SHM)."""

from __future__ import annotations

from pathlib import Path


def resolve_db_files(package_root: str | Path) -> tuple[Path, Path, Path]:
    db = Path(package_root).resolve() / ".meridian" / "meridian.db"
    return db, Path(str(db) + "-wal"), Path(str(db) + "-shm")


def _stat_tuple(path: Path) -> tuple[str, int, int]:
    try:
        st = path.stat()
        return (path.name, int(st.st_mtime_ns), int(st.st_size))
    except OSError:
        return (path.name, 0, 0)


def db_fingerprint(package_root: str | Path) -> str:
    db, wal, shm = resolve_db_files(package_root)
    parts = [_stat_tuple(db), _stat_tuple(wal), _stat_tuple(shm)]
    return "|".join(f"{n}:{mtime}:{size}" for n, mtime, size in parts)
