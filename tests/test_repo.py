"""Test the templatekit.repo.Repo class.
"""

import contextlib
import os

import pytest

from templatekit.repo import FileTemplate, ProjectTemplate, Repo


@contextlib.contextmanager
def work_dir(workdirname):
    """Temporarily change the current working directory (as a context
    manager).
    """
    prev_cwd = os.getcwd()
    os.chdir(workdirname)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def test_discovery_repo_at_root(templates_repo):
    """Test Repo.discover_repo given the root directory itself."""
    with work_dir(templates_repo):
        repo = Repo.discover_repo(dirname=".")
        assert isinstance(repo, Repo)


def test_discover_repo_in_subdir(templates_repo):
    """Test Repo.discover_repo given a subdirectory of the root."""
    with work_dir(templates_repo):
        repo = Repo.discover_repo(dirname="file_templates")
        assert isinstance(repo, Repo)


def test_discover_repo_invalid(templates_repo):
    """Test Repo.discover_repo an invalid starting directory."""
    with work_dir(templates_repo):
        with pytest.raises(OSError):
            Repo.discover_repo(dirname=os.path.abspath(".."))


def test_file_templates_dirname(templates_repo):
    """Test the file_templates_dirname property."""
    with work_dir(templates_repo):
        repo = Repo(".")
        assert os.path.isdir(repo.file_templates_dirname)


def test_project_templates_dirname(templates_repo):
    """Test the project_templates_dirname property."""
    with work_dir(templates_repo):
        repo = Repo(".")
        assert os.path.isdir(repo.project_templates_dirname)


def test_iter_file_templates(templates_repo):
    """Test the iter_file_templates() method."""
    with work_dir(templates_repo):
        repo = Repo(".")
        file_templates = list(repo.iter_file_templates())
        assert len(file_templates) > 0
        for file_template in file_templates:
            assert isinstance(file_template, FileTemplate)


def test_iter_project_templates(templates_repo):
    """Test the iter_project_templates() method."""
    with work_dir(templates_repo):
        repo = Repo(".")
        project_templates = list(repo.iter_project_templates())
        assert len(project_templates) > 0
        for project_template in project_templates:
            assert isinstance(project_template, ProjectTemplate)


def test_getitem(templates_repo):
    """Test key access for templates."""
    with work_dir(templates_repo):
        repo = Repo(".")
        with pytest.raises(KeyError):
            repo["whatwhat"]

        copyright_template = repo["copyright"]
        assert isinstance(copyright_template, FileTemplate)
        assert copyright_template.name == "copyright"

        example_project_template = repo["example_project"]
        assert isinstance(example_project_template, ProjectTemplate)
        assert example_project_template.name == "example_project"


def test_contains(templates_repo):
    """Test contains delegated through __iter__."""
    with work_dir(templates_repo):
        repo = Repo(".")

        assert "copyright" in repo
        assert "example_project" in repo
        assert "whatwhat" not in repo
