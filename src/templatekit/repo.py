"""Template repository APIs."""

from __future__ import annotations

__all__ = (
    "Repo",
    "FileTemplate",
    "ProjectTemplate",
    "BaseTemplate",
    "TemplateConfig",
)

import collections.abc
import functools
import itertools
import json
import logging
import os
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

import cerberus
import git
import yaml


class Repo(object):
    """Template repository.

    Parameters
    ----------
    root : `str`
        Path to the root directory of the template repository. Use ``'.'``
        as the current working directory.
    """

    def __init__(self, root: str):
        super().__init__()
        self._log = logging.getLogger(__name__)
        self._gitrepo: Optional[git.Repo] = None
        self.root = root

    @classmethod
    def discover_repo(cls, dirname: str = ".") -> Repo:
        """Create a Repo instance by discovering the template repo's
        root directory.

        Parameters
        ----------
        dirname : `str`
            Relative or absolute path of a directory. This directory should
            either be the root of a template repository, or a subdirectory
            of the template repository.

        Returns
        -------
        repo : `Repo`
            The Repo instance corresponding to the given directory.

        Raises
        ------
        OSError
            Raised if ``dirname`` is not, or is not contained by, a
            recognizable templates repository.
        """
        original_dirname = dirname
        dirname = os.path.abspath(dirname)

        while dirname != "/":
            if cls._is_repo_dir(dirname):
                return cls(dirname)

            # Repeat with the parent directory
            dirname = os.path.split(dirname)[0]

        message = (
            "The directory {0!r} is not contained by a recognizable "
            "template repository."
        )
        raise OSError(message.format(original_dirname))

    @staticmethod
    def _is_repo_dir(dirname: str) -> bool:
        if not os.path.isdir(os.path.join(dirname, "file_templates")):
            return False

        if not os.path.isdir(os.path.join(dirname, "project_templates")):
            return False

        return True

    def __repr__(self) -> str:
        return "Repo({0!r})".format(self.root)

    def __str__(self) -> str:
        return "{0!r}\nProject templates: {1!s}\nFile templates: {2!s}".format(
            self,
            ", ".join([t.name for t in self.iter_project_templates()]),
            ", ".join([t.name for t in self.iter_file_templates()]),
        )

    def __iter__(self) -> Iterator[str]:
        """Iterate over the names of all templates in the repository.

        ``__contains__`` delegates to this method.
        """
        for template in self.iter_templates():
            yield template.name

    def __getitem__(self, key: str) -> BaseTemplate:
        """Get either a file or project template by name."""
        for template in self.iter_templates():
            if template.name == key:
                return template

        message = "Template {0!r} not found".format(key)
        raise KeyError(message)

    @property
    def file_templates_dirname(self) -> str:
        """Path of the ``file_templates`` directory in the repository
        (`str`).
        """
        return os.path.join(self.root, "file_templates")

    @property
    def project_templates_dirname(self) -> str:
        """Path of the ``project_templates`` directory in the repository
        (`str`)."""
        return os.path.join(self.root, "project_templates")

    def iter_templates(self) -> Iterator[BaseTemplate]:
        """Iterate over all templates in the repository (both file and
        project).

        Yields
        ------
        template : `FileTemplate` or `ProjectTemplate`
            Template object.
        """
        file_iterator = self.iter_file_templates()
        project_iterator = self.iter_project_templates()
        for template in itertools.chain(project_iterator, file_iterator):
            yield template

    def iter_file_templates(self) -> Iterator[FileTemplate]:
        """Iterate over file templates in the repository.

        These templates are in the ``file_templates`` directory of the
        repository and either template a single file, or a snippet of one.

        Yields
        ------
        template : `FileTemplate`
            Template object.
        """
        dir_items = self._list_directory_items(self.file_templates_dirname)
        for template_dir in dir_items:
            try:
                template = FileTemplate(template_dir)
            except (OSError, ValueError) as err:
                # Not a template directory
                message = (
                    "Found file_template directory {0!r} but it is not "
                    "a recognizable template. {1!s}"
                )
                logging.warning(message.format(template_dir, err))
                continue
            yield template

    def iter_project_templates(self) -> Iterator[ProjectTemplate]:
        """Iterate over project templates in the repository.

        These templates are in the ``project_templates`` directory of the
        repository and template full project directory trees and contents.

        Yields
        ------
        template : `ProjectTemplate`
            Template object.
        """
        dir_items = self._list_directory_items(self.project_templates_dirname)
        for template_dir in dir_items:
            try:
                template = ProjectTemplate(template_dir)
            except (OSError, ValueError) as err:
                # Not a template directory
                message = (
                    "Found project_template directory {0!r} but it is "
                    "not a recognizable template. {1!s}"
                )
                logging.warning(message.format(template_dir, err))
                continue
            yield template

    def _list_directory_items(self, dirname: str) -> List[str]:
        fs_items = os.listdir(dirname)
        fs_items.sort()
        fs_items = [os.path.join(dirname, item) for item in fs_items]
        return [fs_item for fs_item in fs_items if os.path.isdir(fs_item)]

    def build(self) -> subprocess.CompletedProcess:
        """Run a scons build of the template repository.

        This method runs the ``scons`` command, and thus regenerates examples
        for each template.

        Returns
        -------
        result : `subprocess.CompletedProcess`
            The result of the ``scons`` execution. See
            `subprocess.CompletedProcess` for details.
        """
        return subprocess.run(["scons"], shell=True, cwd=self.root)

    @property
    def gitrepo(self) -> git.Repo:
        """The template repository's Git repository (`git.Repo`)."""
        if self._gitrepo is None:
            self._gitrepo = git.repo.base.Repo(path=self.root)
        return self._gitrepo

    def is_git_dirty(self) -> bool:
        """Test if the Git repository has uncommitted state (including
        untracked files.

        Returns
        -------
        dirty : `bool`
            `True` if the Git repository is "dirty;" `False` otherwise.
        """
        return self.gitrepo.is_dirty(
            index=True,
            working_tree=True,
            untracked_files=True,
            submodules=True,
        )

    @property
    def untracked_files(self) -> List[str]:
        """The list of files not tracked by the Git repository (and not
        ignored).
        """
        return self.gitrepo.untracked_files

    def get_uncommitted_files(self) -> git.diff.DiffIndex:
        """Get a DiffIndex with all changes of the template repository
        compared to the committed state.

        Returns
        -------
        diffindex : `git.diff.DiffIndex`
            A `~DiffIndex` of all changes that are not committed.
        """
        return self.gitrepo.head.commit.diff(None)


class BaseTemplate(object):
    """Template (file or project) in the templates repo.

    Parameters
    ----------
    path : `str`
        Path of the template's directory.

    Raises
    ------
    OSError
        Raised if ``path`` is not a directory.
    ValueError
        Raised if ``path`` is a directory that does not contain a recognizable
        template.
    """

    def __init__(self, path: str):
        super().__init__()
        self._cookiecutter_data: Optional[Dict[str, Any]] = None
        self._log = logging.getLogger(__name__)
        self.path = os.path.abspath(path)

        self._validate_template_dir()

        with open(self.templatekit_yaml_path, "r") as f:
            config_data = yaml.safe_load(f)
        config = TemplateConfig(config_data)
        # Add default from cookiecutter.json
        self.config = config.normalize(self)

    def _validate_template_dir(self) -> None:
        """Run a quick set of checks that this is in fact a template
        repository, with a cookiecutter.json directory, etc.
        """
        if not os.path.isdir(self.path):
            message = "File template directory {} not found.".format(self.path)
            raise ValueError(message)

        if not os.path.isfile(self.cookiecutter_json_path):
            message = "cookiecutter.json not found in {}".format(self.path)
            raise ValueError(message)

        if not os.path.isfile(self.templatekit_yaml_path):
            message = "templatekit.yaml not found in {}".format(self.path)
            raise ValueError(message)

    def __str__(self) -> str:
        return "{0!s}({1!r})".format(self.__class__.__name__, self.name)

    def __repr__(self) -> str:
        return "{0!s}({1!r})".format(self.__class__.__name__, self.name)

    @property
    def name(self) -> str:
        """Name of the template (`str`)."""
        return os.path.split(self.path)[-1]

    @property
    def templatekit_yaml_path(self) -> str:
        """Path of the templatekit.yaml file (`str`)."""
        return os.path.join(self.path, "templatekit.yaml")

    @property
    def cookiecutter_json_path(self) -> str:
        """Path of the cookiecutter.json file (`str`)."""
        return os.path.join(self.path, "cookiecutter.json")

    @property
    def cookiecutter(self) -> Dict[str, Any]:
        """The data from the ``cookiecutter.json`` file."""
        if self._cookiecutter_data is None:
            with open(self.cookiecutter_json_path) as f:
                self._cookiecutter_data = json.load(f)
        return self._cookiecutter_data


class FileTemplate(BaseTemplate):
    """File template.

    Parameters
    ----------
    path : `str`
        Path of the template's directory.

    Raises
    ------
    OSError
        Raised if ``path`` is not a directory.
    ValueError
        Raised if ``path`` is a directory that does not contain a recognizable
        template.
    """

    @property
    def source_path(self) -> str:
        """Path to the template source file (a .jinja extension) (`str`)."""
        items = os.listdir(self.path)
        for item in items:
            if os.path.splitext(item)[-1] == ".jinja":
                return os.path.join(self.path, item)
        raise ValueError(f"No template source file found in {self.path}")


class ProjectTemplate(BaseTemplate):
    """Project template.

    Parameters
    ----------
    path : `str`
        Path of the template's directory.

    Raises
    ------
    OSError
        Raised if ``path`` is not a directory.
    ValueError
        Raised if ``path`` is a directory that does not contain a recognizable
        template.
    """


@functools.lru_cache()
def get_config_validator() -> cerberus.Validator:
    """Get a validator for ``templatekit.yaml`` configuration files.

    This function is cached.

    Returns
    -------
    validator : `cerberus.Validator`
        A Cerberus validator based on the ``configschema.yaml`` schema.
    """
    configpath = Path(__file__).parent / "configschema.yaml"
    schema = yaml.safe_load(configpath.read_text())
    validator = cerberus.Validator(schema, purge_unknown=True)
    return validator


class TemplateConfig(collections.abc.Mapping):
    """Represents the configuration for a template, derived from a
    templatekit.yaml file.

    Parameters
    ----------
    data : `dict`
        Configuration, parsed from a ``templatekit.yaml`` file.

    Notes
    -----
    Access individual configurations on a ``TemplateConfig`` instance like
    keys in a dictionary.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self._validator = get_config_validator()

        if self._validator.validate(data) is False:
            print("Validation errors:")
            print(json.dumps(self._validator.errors, sort_keys=True, indent=2))
            print("Data:")
            print(json.dumps(data, sort_keys=True, indent=2))
            raise RuntimeError("Configuration syntax error")

        # Apply Cereberus's schema-based normalization
        self.data = self._validator.normalized(self.data)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[str]:
        for k in self.data:
            yield k

    def normalize(self, template: BaseTemplate) -> TemplateConfig:
        """Normalize the template configuration by adding defaults for any
        missing configurations.

        Parameters
        ----------
        template : `BaseTemplate`
            A template instance.

        Returns
        -------
        template_config : `TemplateConfig`
            A new template configuration instance where all defaults are set.
        """
        data = deepcopy(self.data)

        if "name" not in data:
            data["name"] = template.name

        if "group" not in data:
            data["group"] = "General"

        if "dialog_fields" not in data:
            # Need to get the dialog fields from the cookiecutter.json file
            data["dialog_fields"] = []
            for key in template.cookiecutter:
                if key.startswith("_"):
                    # skip things like "_extensions"
                    continue
                elif isinstance(template.cookiecutter[key], str):
                    data["dialog_fields"].append(
                        {
                            "key": key,
                            "label": self._truncate(key, 75),
                            "component": "text",
                        }
                    )
                elif isinstance(template.cookiecutter[key], list):
                    data["dialog_fields"].append(
                        {
                            "key": key,
                            "label": self._truncate(key, 75),
                            "component": "select",
                        }
                    )

        for field in data["dialog_fields"]:
            if field["component"] == "select":
                self._normalize_select_field(field, template)
            elif field["component"] == "text":
                self._normalize_text_field(field, template)

        return TemplateConfig(data)

    def _normalize_select_field(
        self, field: Dict[str, Any], template: BaseTemplate
    ) -> None:
        """Normalize a "select" component field.

        - Add options that exist in the cookiecutter.json file if the options
          aren't explicitly set.
        """
        if "preset_options" in field or "preset_groups" in field:
            # The schemas force these to be fully specified in templatekit.yaml
            return
        elif "options" not in field:
            # Add options from cookiecutter.json
            field["options"] = []
            for option_value in template.cookiecutter[field["key"]]:
                # Enforce Slack length limit on the label
                option_label = self._truncate(option_value, 75)
                field["options"].append(
                    {
                        "label": option_label,
                        "value": option_label,  # also needs truncation
                        "template_value": option_value,
                    }
                )

    def _normalize_text_field(
        self, field: Dict[str, Any], template: BaseTemplate
    ) -> Dict[str, Any]:
        """Normalize text field components.

        - Add placeholder information found in the cookiecutter.json file
          if an explicit placeholder isn't set.
        """
        if "placeholder" not in field or len(field["placeholder"]) == 0:
            field["placeholder"] = template.cookiecutter[field["key"]]
        return field

    def _truncate(self, text: str, length: int) -> str:
        if isinstance(text, str) and len(text) > length:
            return text[: length - 1] + "…"
        else:
            return text
