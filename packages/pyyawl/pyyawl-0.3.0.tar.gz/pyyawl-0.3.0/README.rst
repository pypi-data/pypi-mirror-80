========================================
Yet Another Workflow Language for Python
========================================


.. image:: https://img.shields.io/pypi/v/pyyawl.svg
        :target: https://pypi.python.org/pypi/pyyawl

.. image:: https://img.shields.io/travis/fabiofumarola/pyyawl.svg
        :target: https://travis-ci.org/fabiofumarola/pyyawl

.. image:: https://readthedocs.org/projects/pyyawl/badge/?version=latest
        :target: https://pyyawl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/fabiofumarola/pyyawl/shield.svg
     :target: https://pyup.io/repos/github/fabiofumarola/pyyawl/
     :alt: Updates



Yet another simple workflow language for python


* Free software: Apache Software License 2.0
* Documentation: https://pyyawl.readthedocs.io.


Features
--------

Pyyawl is a simple yaml based workflow executor that let you define datascience pipelines using yaml.

* execute worfkflow defined in yaml
* simple and extensible


Usage 
-------

To use Yet Another Workflow Language for Python from command-line:

1. create a file .yaml file with the description of the workflow with its tasks::
    
    $ yawl --generate > my_workflow.yaml

    
2. execute the workflow from the commandline::

    $ yawl --f my_workflow.yaml --verbose


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
