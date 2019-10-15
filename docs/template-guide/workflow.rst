#############################
Template development workflow
#############################

This page describes the general workflow for developing and maintaining templates in a template repository.

.. note::

   Though this page uses the LSST template repository at https://github.com/lsst/templates as a specific example, these steps apply to any Templatekit-compliant repository.
   Substitute in your repository's URL and GitHub workflow as necessary.

Step 1: Clone the repository and install templatekit
====================================================

From a shell, clone the template repository:

.. code-block:: sh

   git clone https://github.com/lsst/templates
   cd templates

Install the version of Templatekit that's used by the repository:

.. code-block:: sh

   pip install -r requirements.txt

.. tip::

   Install Templatekit and other dependencies in a virtual environment, such as venv_.

Step 2: Make your changes
=========================

Before making any changes, it's a good idea to **create a new Git branch or work from a GitHub fork.**
Refer to the guidelines of your template repository or organization for a concrete workflow.

Refer to the :doc:`index` for guides on how to add and modify templates in a Templatekit-compliant repository.

Step 3: Regenerate examples
===========================

In a shell, run the :command:`scons` command to regenerate the examples:

.. code-block:: sh

   scons

Ensure that :command:`scons` ran properly.
If it didn't, there is likely an issue with either the templates or the ``SConstruct`` files.

Next, check for any modified files:

.. code-block:: sh

   git status

Review the changes for correctness.
If the generated examples don't look right, you'll need to adjust the templates and rerun :command:`scons`.

Once the changes are correct, commit the changes with Git.

Step 4: Check the repository
============================

In a shell, run Templatekit's repository validation command:

.. code-block:: sh

   templatekit check

The ``templatekit check`` command ensures that the structure of the template repository is correct and that the examples are consistent with the templates.

Step 5: Create a Pull Request
=============================

Your changes are ready to publish.
Follow the guidelines published by your template repository or organization.

.. _venv: https://docs.python.org/3/library/venv.html
