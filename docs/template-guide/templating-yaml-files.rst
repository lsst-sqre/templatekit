##############################
Tips for templating YAML files
##############################

Use double-quoted string fields with the escape_yaml_doublequoted filter
========================================================================

If you are templating a string field in a YAML file, it's a good idea to make it an double-quoted string field.
Double-quoted string fields are the only style of YAML `capable of holding arbitrary content <https://yaml.org/spec/1.2/spec.html#id2787109>`_.
You do need to ensure that double quote (``"``) and backslash (``\``) characters are escaped, though.
You can do this with the :ref:`escape_yaml_doublequoted` filter:

.. code-block:: jinja

   ---
   my_field: "{{ cookiecutter.my_variable | escape_yaml_doublequoted }}"
