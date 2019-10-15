"""Subcommand for checking a template repository for valid structure and
operation.
"""

__all__ = ('check',)

import sys

import click


@click.command(short_help='Check the template repository')
@click.pass_obj
def check(state):
    """Check the template repository for valid structure and operation.

    The following checks are performed:

    1. Test for untracked files in the Git repository.
    2. Test for modified, but uncommitted, changes in the Git repository.

    Note:

    - A non-zero status code is returned if the checks fail.
    - This command always recompiles the examples by running the scons
      command.
    """
    repo = state['repo']
    print('Testing template repository {0!s}'.format(repo.root))
    scons_result = repo.build()
    if scons_result.returncode > 0:
        message = (
            '"scons" failed with status {0!d}\n\nThis means that the examples '
            'could not be successfully generated because of an issue with the '
            'Cookiecutter templates. Check the scons output, above, for '
            'debugging hints.'
        )
        sys.exit(message.format(scons_result.returncode))

    error_count = 0
    error_count += _test_git_state(repo)

    if error_count == 1:
        sys.exit('\n❌ The template repository checks failed with '
                 '{0:d} error'.format(error_count))
    elif error_count > 1:
        sys.exit('\n❌ The template repository checks failed with '
                 '{0:d} errors'.format(error_count))
    else:
        print('✅ Passed!')


def _test_git_state(repo):
    """Test if the Git repository of the template repository is clean.
    (no modified files and no untracked files).
    """
    error_count = 0

    if repo.is_git_dirty():
        error_count += _test_untracked_files(repo)
        error_count += _test_uncommitted_changes(repo)

    return error_count


def _test_untracked_files(repo):
    untracked_paths = repo.untracked_files
    error_count = 0
    if len(untracked_paths) > 0:
        print('\n🔴 Untracked files:')
        for p in untracked_paths:
            print('  {}'.format(p))
            error_count += 1
    return error_count


def _test_uncommitted_changes(repo):
    error_count = 0
    # Get all uncommitted changes because we don't have a count of them
    # otherwise
    uncommitted_changes = []
    diffindex = repo.get_uncommitted_files()
    for changetype in diffindex.change_type:
        for change in diffindex.iter_change_type(changetype):
            # For deleted files, we want to use the original ("a") path.
            # Otherwise, we tend to want to show the user the new ("b") path
            if changetype in ('D',):
                uncommitted_changes.append(
                    '{0} {1}'.format(changetype, change.a_path)
                )
            else:
                uncommitted_changes.append(
                    '{0} {1}'.format(changetype, change.b_path)
                )
            error_count += 1
    if error_count > 0:
        print('\n🔴 Uncommitted changes:')
        for change in uncommitted_changes:
            print(change)
    return error_count
