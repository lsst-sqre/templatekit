##############################
Templatekit's Jinja extensions
##############################

Templatekit provides several custom Jinja extensions that you can use to process content in your templates.
To use these extensions, remember to enable them by adding ``templatekit.TemplatekitExtension`` to the ``_extensions`` array in your template's ``cookiecutter.json`` file:

.. code-block:: json

   {
     "_extensions": ["templatekit.TemplatekitExtension"]
   }

If the ``_extensions`` field doesn't already exist, you can add it.
For more information, see :ref:`Template extensions <cookiecutter:template extensions>` in the Cookiecutter_ documentation.

.. _escape_yaml_doublequoted:

escape\_yaml\_doublequoted
==========================

This filter to escapes content that you add to double-quoted string fields in a YAML file.
Consider this YAML template:

.. code-block:: jinja

   ---
   my_field: "{{ cookiecutter.my_variable | escape_yaml_doublequoted }}"

The ``escape_yaml_doublequoted`` filter escapes double quote (``"``) and backslash (``\``) characters.
For example, if the value of ``my_variable`` is ``Hello "world" \ Bonjour!``, the rendered YAML will be:

.. code-block:: yaml

   ---
   my_field: "Hello \"world\" \\ Bonjour!"
