"""Rendering file templates with Cookiecutter.
"""

__all__ = ("render_file_template", "render_and_write_file_template")

import io
import logging
import os
import shutil
from typing import Any, Dict, Optional

from cookiecutter.environment import StrictEnvironment
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError


def render_file_template(
    template_path: str,
    use_defaults: bool = False,
    extra_context: Optional[Dict[str, Any]] = None,
) -> str:
    """Render a single-file template with Cookiecutter.

    Currently this function only renders a file using default values defined
    in a ``cookiecutter.json`` file.

    Parameters
    ----------
    template_path : `str`
        Path to the file template. There should be a
        ``cookecutter.json`` in the same directory as the template file.
        This JSON file is used to define a provide defaults for the template's
        variables.
    use_defaults : `bool`, optional
        Disables Sphinx from interactively prompting for context variables, if
        `True`.
    extra_context : `dict`, optional
        Optional dictionary of key-value pairs that override defaults in the
        ``cookiecutter.json`` file.

    Returns
    -------
    rendered_text : `str`
        Content rendered from the template and ``cookiecutter.json`` defaults.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Rendering file template %s", template_path)

    # Get variables for rendering the template
    template_dir = os.path.dirname(template_path)
    context_file = os.path.join(template_dir, "cookiecutter.json")
    context = generate_context(context_file=context_file)
    context["cookiecutter"] = prompt_for_config(context, use_defaults)

    if extra_context is not None:
        context["cookiecutter"].update(extra_context)

    # Jinja2 template rendering environment
    env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )
    env.loader = FileSystemLoader(template_dir)

    try:
        tmpl = env.get_template(os.path.basename(template_path))
    except TemplateSyntaxError as exception:
        # Disable translated so that printed exception contains verbose
        # information about syntax error location
        exception.translated = False
        raise
    rendered_text = tmpl.render(**context)

    return rendered_text


def render_and_write_file_template(
    template_path: str,
    output_path: str,
    extra_context: Optional[Dict[str, Any]] = None,
) -> None:
    """Render a single-file template and write it to the filesystem.

    Parameters
    ----------
    template_path : `str`
        Path to the file template.
    output_path : `str`
        Path to write the rendered file.
    extra_context : `dict`, optional
        Optional dictionary of key-value pairs that override defaults in the
        ``cookiecutter.json`` file.

    See also
    --------
    render_file_template
    """
    logger = logging.getLogger(__name__)

    rendered_text = render_file_template(
        template_path, use_defaults=True, extra_context=extra_context
    )

    logger.debug("Writing rendered file to {}".format(output_path))
    with io.open(output_path, "w", encoding="utf-8") as fh:
        fh.write(rendered_text)

    # Apply file permissions to output file
    shutil.copymode(template_path, output_path)
