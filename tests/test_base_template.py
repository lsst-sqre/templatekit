"""Test the templatekit.repo.BaseTemplate class.
"""

import os
import pytest
from templatekit.repo import BaseTemplate


def test_validation(templates_repo):
    """Test basic BaseTemplate instantiation/validation checks.

    Uses the actual templates repository data.
    """
    file_template_exists = BaseTemplate(
        os.path.join(templates_repo, 'file_templates/license_gplv3'))
    assert isinstance(file_template_exists, BaseTemplate)

    project_template_exists = BaseTemplate(
        os.path.join(templates_repo, 'file_templates/license_gplv3'))
    assert isinstance(project_template_exists, BaseTemplate)

    with pytest.raises(OSError):
        BaseTemplate(os.path.join(templates_repo, 'file_templates/not_here'))

    with pytest.raises(OSError):
        BaseTemplate(
            os.path.join(templates_repo, 'project_templates/not_here'))


@pytest.mark.parametrize('path,expected', [
    ('file_templates/license_gplv3', 'license_gplv3'),
    ('project_templates/example_project', 'example_project')
])
def test_name(templates_repo, path, expected):
    """Test BaseTemplate.name.
    """
    full_path = os.path.join(templates_repo, path)
    template = BaseTemplate(full_path)
    assert expected == template.name


@pytest.mark.parametrize('path', [
    'file_templates/license_gplv3',
    'project_templates/example_project',
])
def test_cookiecutter_json_path(templates_repo, path):
    """Test BaseTemplate.cookiecutter_json_path.
    """
    full_path = os.path.join(templates_repo, path)
    template = BaseTemplate(full_path)
    assert os.path.isfile(template.cookiecutter_json_path)
