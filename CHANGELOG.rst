##########
Change log
##########

0.5.0 (unreleased)
==================

- Update build system to current SQuaRE standards.
- Add type annotations for all code.
- Unpin all dependencies for easier use as a library.

0.4.1 (2020-02-26)
==================

- The click dependency is no longer pinned.
  This fixes compatibility with cookiecutter 1.7, which requires click 7.

0.4.0 (2019-10-15)
==================

- Added a new ``templatekit check`` command.
  This command helps both developers and CI scripts ensure that the template repository is well-structured and that all examples are up-to-date.
  The ``templatekit check`` command runs ``scons`` to regenerate examples, and then checks the Git state to ensure that there are no untracked or modified files, which might indicate that there are uncommitted changes to examples.
- Internally, the ``templatekit.Repo`` class exposes a ``git.Repo`` instance from GitPython_.
  See ``templatekit.Repo.gitrepo``, ``templatekit.Repo.is_git_dirty``, and ``templatekit.Repo.untracked_files``.

0.3.0 (2019-10-08)
==================

- A new Jinja filter, ``escape_yaml_doublequoted``, is available as part of the ``templatekit.TemplatekitExtension``.
  This filter is meant to be used with template variables that are inside double-quoted string fields in a YAML file.
  The filter escapes both double quote characters (``"``) and backslash characters (``\``).
- There is a new "Template developer" guide, which lists the ``escape_yaml_doublequoted`` filter and provides tips on how to write YAML files in templates.
- The development procedure is now part of the documentation, rather than the README.

0.2.0 (2019-04-16)
==================

- New support for ``templatekit.yaml`` files.
  These files, which get added alongside ``cookiecutter.json`` files, refine the presentation of templates in Slack user interactions (see the Templatebot_ project).
  For example, templates have nice names (``name`` field) and can be grouped in selection menus (``group_name`` field).
  The ``dialog_fields`` field provides configuration for fields in the Slack dialogs where a user configures their new file or project.
- `Cerberus <http://docs.python-cerberus.org/en/stable/index.html>`_ is a new dependency of Templatekit.
  ``templatekit.yaml`` files are validated against a Cerberus schema.

0.1.1 (2019-01-07)
==================

- Fix typo in PyPI classifiers that prevented deployment to PyPI.
- Fix setup.py so that setuptools_scm is activated.

0.1.0 (2019-01-07)
==================

- Extracted Templatekit from https://github.com/lsst/templates.
  By splitting the Templatekit application from the templates repository, we can version Templatekit and release it through PyPI.

- Versioning with `setuptools_scm <https://pypi.org/project/setuptools_scm/>`__.

- Sphinx documentation site.

(`DM-16940 <https://jira.lsstcorp.org/browse/DM-16940>`__)

.. _Templatebot: https://github.com/lsst-sqre/templatebot
.. _GitPython: https://gitpython.readthedocs.io/en/stable/index.html
