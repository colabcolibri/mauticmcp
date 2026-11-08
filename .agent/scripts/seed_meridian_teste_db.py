#!/usr/bin/env python3
"""Shim — implementation in dev/seed_meridian_teste_db.py"""
import runpy
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
sys.path.insert(0, str(_root / "lib"))
runpy.run_path(str(_root / "dev" / "seed_meridian_teste_db.py"), run_name="__main__")
