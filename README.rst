###########
Templatekit
###########

Templatekit is a Python library and command-line app for using and maintaining a centralized repository of project and file templates.
Templates are built with Cookiecutter_ and Jinja_.
https://github.com/lsst/templates is the primary repository that Templatekit is built for, but Templatekit can be used for other template repository projects.

Development
===========

Clone Templatekit with test data (`lsst/templates`_)::

   git clone --recursive-submodules https://github.com/lsst-sqre/templatekit

Install the package for development (do this in a `virtual environment`_)::

   cd templatekit
   pip install -e ".[dev]"

Run tests::

   pytest

You can also run tests without installing Templatekit first::

   python setup.py test

Occasionally you may need to update the ``tests/data/templates`` submodule::

   git submodule update --recursive

.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
.. _Jinja: http://jinja.pocoo.org
.. _lsst/templates: https://github.com/lsst/templates
.. _virtual environment: https://docs.python.org/3/library/venv.html
