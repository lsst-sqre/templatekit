"""Pytest fixtures.
"""

import os

import pytest


@pytest.fixture(scope="session")
def templates_repo() -> str:
    """Directory path of the root of the templates repository."""
    repo_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "data/templates")
    )
    return repo_path
