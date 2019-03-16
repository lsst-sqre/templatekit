"""Tests for the templatekit.repo.TemplateConfig class.
"""

from pathlib import Path

import cerberus
import pytest

from templatekit.repo import (TemplateConfig, get_config_validator,
                              FileTemplate)


def test_get_config_validator():
    validator = get_config_validator()
    assert isinstance(validator, cerberus.Validator)

    # Test caching
    validator2 = get_config_validator()
    assert validator == validator2


def test_templateconfig_valid():
    c = {
        'name': 'Python',
        'group': 'Stack license preamble'
    }
    config = TemplateConfig(c)

    # Test mapping methods
    assert config['name'] == 'Python'
    assert len(config) == 3
    assert set(['name', 'group', 'dialog_title']) == set([k for k in config])


def test_templateconfig_invalid():
    c = {
        'name': ''
    }
    with pytest.raises(RuntimeError):
        TemplateConfig(c)


def test_templateconfig_normalize_name():
    class MockTemplate:
        name = 'my_template'

    configdata = {
        'dialog_fields': []
    }

    mock_template = MockTemplate()
    c = TemplateConfig(configdata)
    assert 'name' not in c

    c2 = c.normalize(mock_template)
    assert c2['name'] == 'my_template'
    assert c2['group'] == 'General'


def test_implicitselect():
    """Test building a configuration from tests/data/config/implicitselect

    This shows how a select menu would work.
    """
    template_path = Path(__file__).parent / 'data' / 'config' \
        / 'implicitselect'
    template = FileTemplate(str(template_path))
    c = template.config

    assert c['name'] == 'COPYRIGHT file'
    assert c['group'] == 'General'  # normalized
    assert c['dialog_title'] == 'Create a COPYRIGHT'
    assert c['dialog_fields'][0]['label'] == 'Copyright holder'
    assert len(c['dialog_fields']) == 1  # don't add extra variables as fields
    assert 'options' in c['dialog_fields'][0]


def test_preset():
    """Test building a configuration from tests/data/config/preset.

    This shows the "preset_options" feature.
    """
    template_path = Path(__file__).parent / 'data' / 'config' / 'preset'
    template = FileTemplate(str(template_path))
    c = template.config

    assert 'preset_options' in c['dialog_fields'][0]
