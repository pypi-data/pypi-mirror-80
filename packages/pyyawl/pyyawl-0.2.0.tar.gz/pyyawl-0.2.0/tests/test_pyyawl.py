#!/usr/bin/env python
"""Tests for `pyyawl` package."""

from pyyawl import pyyawl
from pathlib import Path

PATH = Path(__file__).parent


def test_simpleworkflow():
    definition = PATH / 'test_ops.yaml'
    pyyawl.execute(definition, False)
