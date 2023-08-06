__all__ = ['call_echo']

import subprocess
from pathlib import Path
import shutil
from ..namedregistry import export


@export(name='echo')
def call_echo(value, verbose=False):
    subprocess.run(['echo', 'hello', value])


@export(name='mkdir')
def call_mkdir(path, verbose=False):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)


@export(name='rmdir')
def call_rmdir(path, force=False, verbose=False):
    shutil.rmtree(path, True, None)


@export(name='ls')
def call_ls(path, verbose=False):
    path = Path(path)
    result = list(path.iterdir())
    print(result)
    return result