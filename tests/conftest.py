"""Pytest fixtures.
"""

import os

import pytest


@pytest.fixture
def templates_repo(scope="session"):
    """Directory path of the root of the templates repository."""
    repo_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "data/templates")
    )
    return repo_path
