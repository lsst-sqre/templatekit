"""Subcommand for checking a template repository for valid structure and
operation.
"""

from __future__ import annotations

__all__ = ("check",)

import sys

import click

from ..repo import Repo


@click.command(short_help="Check the template repository")
@click.option(
    "-i",
    "--ignore",
    "ignored_files",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Ignore a file when checking consistency of examples.",
)
@click.pass_obj
def check(state: dict[str, Repo], ignored_files: list[str]) -> None:
    """Check the template repository for valid structure and operation.

    The following checks are performed:

    1. Test for untracked files in the Git repository.
    2. Test for modified, but uncommitted, changes in the Git repository.

    Note:

    - A non-zero status code is returned if the checks fail.
    - This command always recompiles the examples by running the scons
      command.
    """
    repo = state["repo"]
    scons_result = repo.build()
    if scons_result.returncode > 0:
        message = (
            '"scons" failed with status {0:d}\n\nThis means that the examples '
            "could not be successfully generated because of an issue with the "
            "Cookiecutter templates. Check the scons output, above, for "
            "debugging hints."
        )
        sys.exit(message.format(scons_result.returncode))

    error_count = 0
    error_count += _test_git_state(repo, ignored_files)

    if error_count == 1:
        sys.exit(
            "\n❌ The template repository checks failed with "
            f"{error_count:d} error"
        )
    elif error_count > 1:
        sys.exit(
            "\n❌ The template repository checks failed with "
            f"{error_count:d} errors"
        )
    else:
        pass


def _test_git_state(repo: Repo, ignored_files: list[str]) -> int:
    """Test if the Git repository of the template repository is clean.
    (no modified files and no untracked files).
    """
    error_count = 0

    if repo.is_git_dirty():
        error_count += _test_untracked_files(repo)
        error_count += _test_uncommitted_changes(repo, ignored_files)

    return error_count


def _test_untracked_files(repo: Repo) -> int:
    untracked_paths = repo.untracked_files
    error_count = 0
    if len(untracked_paths) > 0:
        for _p in untracked_paths:
            error_count += 1
    return error_count


def _test_uncommitted_changes(repo: Repo, ignored_files: list[str]) -> int:
    error_count = 0
    # Get all uncommitted changes because we don't have a count of them
    # otherwise
    uncommitted_changes = []
    diffindex = repo.get_uncommitted_files()
    for changetype in diffindex.change_type:
        for change in diffindex.iter_change_type(changetype):
            if change.a_path in ignored_files:
                continue
            # For deleted files, we want to use the original ("a") path.
            # Otherwise, we tend to want to show the user the new ("b") path
            if changetype == "D":
                uncommitted_changes.append(f"{changetype} {change.a_path}")
            else:
                uncommitted_changes.append(f"{changetype} {change.b_path}")
            error_count += 1
    if error_count > 0:
        for change in uncommitted_changes:
            pass
    return error_count
