"""Connector registry for meridian_delivery facade."""

from __future__ import annotations

from typing import Protocol

from meridian_delivery_config import SUPPORTED_CONNECTORS


class DeliveryDriver(Protocol):
    name: str

    def dispatch(self, package_root: str, argv: list[str]) -> int: ...


_DRIVERS: dict[str, type] = {}


def register_driver(name: str):
    def decorator(cls: type) -> type:
        _DRIVERS[name] = cls
        return cls

    return decorator


def get_driver(connector: str) -> DeliveryDriver:
    if connector not in _DRIVERS:
        if connector not in SUPPORTED_CONNECTORS:
            raise ValueError(
                f"Unknown connector {connector!r}. "
                f"Supported: {', '.join(sorted(SUPPORTED_CONNECTORS))}"
            )
        raise ValueError(f"Connector {connector!r} is declared but has no driver implementation")
    return _DRIVERS[connector]()  # type: ignore[call-arg]


def list_connectors() -> list[str]:
    return sorted(_DRIVERS.keys())


# Register built-in drivers on import
from meridian_delivery import sqlite_driver as _sqlite_driver  # noqa: E402, F401
