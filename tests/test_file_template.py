"""Test the FileTemplate class.

See also: test_base_template.py for testing the base class.
"""

import os
from templatekit.repo import FileTemplate


def _make_repo_path(repo_rel_path):
    """Make an absolute path to a template directory given a
    repo-relative path.
    """
    return os.path.join(os.path.dirname(__file__), '..', repo_rel_path)


def test_source_path(templates_repo):
    template_path = os.path.join(templates_repo, 'file_templates/copyright')
    template = FileTemplate(template_path)
    source_path = template.source_path

    assert os.path.basename(source_path) == 'COPYRIGHT.jinja'
