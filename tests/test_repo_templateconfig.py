"""Tests for the templatekit.repo.TemplateConfig class.
"""

import cerberus
import pytest

from templatekit.repo import TemplateConfig, get_config_validator


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
    assert len(config) == 2
    assert set(['name', 'group']) == set([k for k in config])


def test_templateconfig_invalid():
    c = {
        'name': ''
    }
    with pytest.raises(RuntimeError):
        TemplateConfig(c)


def test_templateconfig_normalize_name():
    class MockTemplate:
        name = 'my_template'

    mock_template = MockTemplate()
    c = TemplateConfig({})
    assert 'name' not in c

    c2 = c.normalize(mock_template)
    assert c2['name'] == 'my_template'
    assert c2['group'] == 'General'
