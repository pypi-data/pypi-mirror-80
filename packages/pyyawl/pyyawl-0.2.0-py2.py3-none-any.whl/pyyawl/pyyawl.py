"""Main module."""
from pyyawl.namedregistry import registry
from tqdm import tqdm
from omegaconf import OmegaConf


def execute(file, verbose):
    """Console script for pyyawl."""
    workflow = OmegaConf.load(file)
    execute_pipeline(workflow, verbose)
    return 0


def execute_pipeline(workflow, verbose):
    print('starting workflow', workflow.name)
    for task in tqdm(workflow.tasks):
        if task.operator in registry:
            registry[task.operator](verbose=verbose, **task.arguments)


def generate():
    return """
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
