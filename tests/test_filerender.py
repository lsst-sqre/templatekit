"""Tests for the templatekit.filerender module.
"""

import os

from templatekit.filerender import render_file_template


def test_render_file_template(templates_repo: str) -> None:
    """Test render_file_template().

    This test uses file_templates/stack_license_preamble_txt/template.txt.jinja
    as an example project.
    """
    template_path = os.path.join(
        templates_repo,
        "file_templates/stack_license_preamble_txt/template.txt.jinja",
    )

    expected_content_path = os.path.join(
        templates_repo, "file_templates/stack_license_preamble_txt/example.txt"
    )
    with open(expected_content_path) as fh:
        expected_content = fh.read()

    content = render_file_template(template_path, use_defaults=True)
    assert expected_content == content
