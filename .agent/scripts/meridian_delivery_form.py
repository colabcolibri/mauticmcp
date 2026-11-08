#!/usr/bin/env python3
"""Compatibility shim — implementation in lib/meridian_delivery_form.py."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_IMPL = Path(__file__).resolve().parent / "lib" / "meridian_delivery_form.py"
_spec = importlib.util.spec_from_file_location("meridian_delivery_form_lib", _IMPL)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load {_IMPL}")
_mod = importlib.util.module_from_spec(_spec)
sys.modules["meridian_delivery_form_lib"] = _mod
_spec.loader.exec_module(_mod)

for _name in dir(_mod):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_mod, _name)
