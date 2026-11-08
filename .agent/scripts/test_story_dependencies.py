#!/usr/bin/env python3
"""Shim — implementation in test/test_story_dependencies.py"""
import runpy
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
sys.path.insert(0, str(_root / "lib"))
runpy.run_path(str(_root / "test" / "test_story_dependencies.py"), run_name="__main__")
