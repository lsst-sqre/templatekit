"""Custom Jinja2 filters and tags.
"""

__all__ = ('convert_py_to_cpp_namespace_code',
           'convert_py_namespace_to_cpp_header_def',
           'convert_py_to_cpp_namespace')

from jinja2.ext import Extension


class TemplatekitExtension(Extension):
    """Custom Jinja2 extensions for use in LSST cookiecutter templates.

    Parameters
    ----------
    environment : `jinja2.Environment`
        Jinja2 environment.

    Notes
    -----
    **Using these extensions in cookiecutter**

    Use these extensions in Cookiecutter by adding the name of this class
    to the ``_extensions`` field array in the ``cookiecutter.json`` file.
    For example:

    .. code-block:: json

       {
         '_extensions': ['templatekit.TemplatekitExtension']
       }

    **Included filters**

    - ``convert_py_to_cpp_namespace_code`` (`convert_py_to_cpp_namespace`)
    - ``convert_py_namespace_to_cpp_header_def``
      (`convert_py_namespace_to_cpp_header_def`)
    - ``convert_py_to_cpp_namespace`` (`convert_py_to_cpp_namespace`)
    """

    def __init__(self, environment):
        super().__init__(environment)

        environment.filters['convert_py_to_cpp_namespace_code'] = convert_py_to_cpp_namespace_code  # noqa: E501
        environment.filters['convert_py_namespace_to_cpp_header_def'] = convert_py_namespace_to_cpp_header_def  # noqa: E501
        environment.filters['convert_py_to_cpp_namespace'] = convert_py_to_cpp_namespace  # noqa: E501


def convert_py_to_cpp_namespace_code(python_namespace):
    """Convert a Python namespace to C++ namespace code.

    Parameters
    ----------
    python_namespace : `str`
        A string describing a Python namespace. For example,
        ``'lsst.example'``.

    Returns
    -------
    cpp_namespace_code : `str`
        C++ namespace code block. For example, ``'lsst.example'`` becomes:

        .. code-block:: cpp

           namespace lsst { example {

           }} // lsst::example

    Notes
    -----
    Use this filter in a Cookiecutter template like this::

        {{ 'lsst.example' | convert_py_to_cpp_namespace_code }}
    """
    name = python_namespace.replace('.', '::')
    namespace_parts = python_namespace.split('.')
    opening = 'namespace ' + ' { '.join(namespace_parts) + ' {\n'
    closing = '}' * len(namespace_parts) + ' // {}'.format(name)
    return '\n'.join((opening, closing))


def convert_py_namespace_to_cpp_header_def(python_namespace):
    """Convert a Python namespace into a C++ header def token.

    Parameters
    ----------
    python_namespace : `str`
        A string describing a Python namespace. For example,
        ``'lsst.example'``.

    Returns
    -------
    cpp_header_def : `str`
        C++ header def, such as '`'LSST_EXAMPLE_H'``.
    """
    return python_namespace.upper().replace('.', '_') + '_H'


def convert_py_to_cpp_namespace(python_namespace):
    """Convert a Python namespace name to a C++ namespace.

    Parameters
    ----------
    python_namespace : `str`
        A string describing a Python namespace. For example,
        ``'lsst.example'``.

    Returns
    -------
    cpp_namespace : `str`
        A C++ namespace. For example: ``'lsst::example'``.
    """
    return python_namespace.replace('.', '::')
