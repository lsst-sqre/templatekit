#################
Development guide
#################

This page describes how to develop Templatekit, the Python package.
For information on developing templates *in* a template repository, see the :doc:`template-guide/index`.

Building and testing
====================

Clone Templatekit with test data (`lsst/templates`_):

.. code-block:: bash

   git clone --recursive-submodules https://github.com/lsst-sqre/templatekit

Install the package for development (do this in a `virtual environment`_):

.. code-block:: bash

   cd templatekit
   pip install -e ".[dev]"

Run tests:

.. code-block:: bash

   pytest

You can also run tests without installing Templatekit first:

.. code-block:: bash

   python setup.py test

Occasionally you may need to update the ``tests/data/templates`` submodule:

.. code-block:: bash

   git submodule update --recursive

Release process
===============

.. note::

   Releases are generally only done by Templatekit's lead engineer (Jonathan Sick).

Starting from a development branch:

1. Ensure that the change log (``CHANGELOG.rst``) is up-to-date.
2. Ensure that the Travis CI tests pass.
   The ``master`` branch is protected on GitHub to assure this.
3. Merge to master using a non-fast-forward merge.
4. Tag using a :pep:`440`-compatible version identifier.

   .. code-block:: bash

      git tag -s X.Y.Z -m "X.Y.Z"
      git push --tags

   Travis CI will create a new release on PyPI.
5. Update projects that depend on Templatekit:

   - https://github.com/lsst/templates
   - https://github.com/lsst-sqre/templatebot

.. _virtual environment: https://docs.python.org/3/library/venv.html
