##########
Change log
##########

0.3.0 (2019-10-08)
==================

- A new Jinja filter, ``escape_yaml_doublequoted``, is available as part of the `templatekit.TemplatekitExtension`.
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
