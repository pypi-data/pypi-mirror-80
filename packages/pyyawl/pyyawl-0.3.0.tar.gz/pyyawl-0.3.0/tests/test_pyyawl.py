#!/usr/bin/env python
"""Tests for `pyyawl` package."""

import pytest
from pyyawl import pyyawl
from pathlib import Path

PATH = Path(__file__).parent


def test_simpleworkflow():
    definition = PATH / 'test_ops.yaml'
    pyyawl.execute(definition, True)


def test_simpleworkflow_from_str():
    content = """
name: test
description: test description

tasks:
  - operator: echo
    arguments:
      value: yawl
  - operator: echo
    arguments:
      value: world
  - operator: papermill
    arguments:
      input_path: tests/notebooks/sum_test.ipynb
      output_path: tests/notebooks/sum_test_out.ipynb
      parameters:
        a: 8
        b: 4
    """
    pyyawl.execute(content, True)


def test_simpleworkflow_mkdir():
    content = """
name: test
description: test description

tasks:
  - operator: mkdir
    arguments:
      path: test_dir
  - operator: rmdir
    arguments:
      path: test_dir
  - operator: ls
    arguments:
      path: .
    """
    results = pyyawl.execute(content, True)
    assert 'test_dir' not in [p.as_posix() for p in results['ls']]


@pytest.mark.xfail(raises=AssertionError)
def test_simpleworkflow_missing_ops():
    content = """
name: test
description: test description

tasks:
  - operator: echo2
    arguments:
      value: yawl
  - operator: echo
    arguments:
      value: world
  - operator: papermill
    arguments:
      input_path: tests/notebooks/sum_test.ipynb
      output_path: tests/notebooks/sum_test_out.ipynb
      parameters:
        a: 8
        b: 4
    """
    pyyawl.execute(content, True)


def test_show_registry():
    assert pyyawl.show_registry(names=True) == [
        'echo', 'mkdir', 'rmdir', 'ls', 'papermill'
    ]
