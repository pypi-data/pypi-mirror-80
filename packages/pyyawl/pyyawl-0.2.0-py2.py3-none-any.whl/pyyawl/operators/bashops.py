import subprocess
from ..namedregistry import export


@export(name='echo')
def call_echo(value=None, verbose=False):
    subprocess.run(['echo', 'hello', value])
