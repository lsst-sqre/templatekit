"""Main command-line interface for templatekit.
"""

__all__ = ("main",)

from typing import Optional

import click

from ..repo import Repo
from .check import check
from .listtemplates import list_templates
from .make import make

# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-r",
    "--template-repo",
    "template_repo",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, resolve_path=True
    ),
    default=".",
    help="Path to the cloned templates Git repository, or a sub directory "
    "within the clone templates repository. Default is '.', the "
    "current working directory.",
)
@click.pass_context
def main(ctx: click.Context, template_repo: str) -> None:
    """templatekit is a CLI for lsst/templates, LSST's project template
    repository.

    Use templatekit to learn about available templates, and to create a new
    project or file snippet based on a template.
    """
    # Subcommands should use the click.pass_obj decorator to get this
    # ctx.obj object as the first argument. Subcommands shouldn't create their
    # own Repo instance.
    ctx.obj = {"repo": Repo.discover_repo(dirname=template_repo)}


# The help command implementation is taken from
# https://www.burgundywall.com/post/having-click-help-subcommand


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: Optional[str]) -> None:
    """Show help for any command."""
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic:
        if topic in main.commands:
            click.echo(main.commands[topic].get_help(ctx))
        else:
            raise click.UsageError(f"Unknown help topic {topic}", ctx)
    else:
        assert ctx.parent
        click.echo(ctx.parent.get_help())


# Add subcommands from other modules
main.add_command(list_templates, name="list")
main.add_command(make)
main.add_command(check)
