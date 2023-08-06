=====
Usage
=====

To use Yet Another Workflow Language for Python from command-line:

1. create a file .yaml file with the description of the workflow with its tasks::

    $ yawl --generate > my_workflow.yaml

    
2. execute the workflow from the commandline::

    $ yawl --f my_workflow.yaml --verbose

