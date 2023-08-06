import papermill as pm
from ..namedregistry import export
from pathlib import Path


@export(name='papermill')
def call_papermill(input_path: Path,
                   output_path: Path,
                   verbose=False,
                   **kwargs):
    if verbose:
        print('executing papermill', input_path, output_path, kwargs)
    return pm.execute_notebook(input_path,
                               output_path,
                               parameters=dict(kwargs['parameters']))
